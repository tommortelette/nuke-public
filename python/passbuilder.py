import os.path
import PySide2
import nuke
import nukescripts.autobackdrop as abd

# Made by Tom Mortelette
# September 2019

# This tool creates a template that compares the beauty recreated by
# combining aovs as well as lightgroups against the original beauty pass
# All aov file sequences must be in the same folder
# This currenty supports renders using Arnold's naming convention

'''
To install add this to your menu.py :

import passbuilder
TMmenu = nuke.menu('Nuke').addMenu('TM Tools')
TMmenu.addCommand('Build Arnold QC Template', 'passbuilder.buildTemplate()')

'''


app = PySide2.QtWidgets.QApplication.instance()
busy_cursor = PySide2.QtGui.QCursor(PySide2.QtCore.Qt.WaitCursor)
createdNodes = []


def makeAOVPaths(aov_type):
    pass_list = nuke.getFileNameList(_render_dir)
    arnold_lighting_aovs = [
        'diffuse_direct', 'diffuse_indirect', 'specular_direct',
        'specular_indirect', 'emission', 'transmission', 'sss', 'coat']
    arnold_utility_aovs = ['N', 'P', 'Z', 'shadow_matte', 'shadow', 'motionVector']
    arnold_crypto_aovs = ['crypto_asset', 'crypto_material', 'crypto_object']
    arnold_lightgroups_aovs = ['emission', 'transmission', 'RGBA_']
    aov_groups = {
        'lighting': arnold_lighting_aovs,
        'lightgroups': arnold_lightgroups_aovs,
        'utility': arnold_utility_aovs,
        'crypto': arnold_crypto_aovs
        }
    aov_paths = []

    if aov_type == 'beauty':
        for p in pass_list:
            if 'beauty' in p:
                aov_paths = [p]
                break
        return aov_paths
    # search for aov name in sequence path and add it to path list
    if aov_type in aov_groups.keys():
        for aov in aov_groups[aov_type]:
            aov_paths.extend([p for p in pass_list if aov in p])
        return aov_paths
    else:
        return None


def deSelectAll():

    if nuke.selectedNodes():
        for n in nuke.selectedNodes():
            n['selected'].setValue(False)


# makes backdrop and add nodes to list to set everything as selected at the end to allow moving around in teh DAG more easily
def makeBackdrop(label):
    global createdNodes
    for n in nuke.selectedNodes():
        createdNodes.append(n)
    backdrop = abd. kdrop()
    backdrop['label'].setValue(label)
    backdrop['bdheight'].setValue(backdrop['bdheight'].value() + 110)
    if label == 'Utility' or label == 'Cryptomatte':
        backdrop['bdwidth'].setValue(backdrop['bdwidth'].value() + 110)
    createdNodes.append(backdrop)
    deSelectAll()


def buildTemplate():
    global _render_dir
    global _x_offset
    try:
        _render_dir = os.path.dirname(nuke.getClipname('Select Render folder or file', '*.exr')) + '/'
    except Exception as e:
        print('Error: {0}'.format(e))
    else:
        app.setOverrideCursor(busy_cursor)
        for n in nuke.selectedNodes():
            n.setSelected(False)

        # start by making the beauty, which should be there if it is the only file
        if makeAOVPaths('beauty'):
            beauty_read = nuke.nodes.Read()
            beauty_read['file'].fromUserText(_render_dir + makeAOVPaths('beauty')[0])
            beauty_read.setSelected(True)
            _x_offset = beauty_read.xpos()
            makeBackdrop('Beauty')

        # create nodes for lighting aovs
        lighting_nodes = []
        if makeAOVPaths('lighting'):
            for filepath in makeAOVPaths('lighting'):
                read = nuke.nodes.Read()
                read['file'].fromUserText(_render_dir + filepath)
                read.setXpos(read.xpos() + 110)
                read.setSelected(True)
                lighting_nodes.append(read)
            if len(lighting_nodes) >= 1:
                # calculate average position of nodes to place the merge in the center
                avgxpos = sum([n.xpos() for n in lighting_nodes])/len(lighting_nodes)
                avgypos = sum([n.ypos() for n in lighting_nodes])/len(lighting_nodes)
                # create merge
                lighting_merge = nuke.nodes.Merge2(
                    operation='plus',
                    output='rgb',
                    selected=True,
                    xpos=avgxpos,
                    ypos=avgypos + 400)
                # set read nodes as merge inputs, with hack to avoid connecting mask input (# 2)
                i = 0
                for input in lighting_nodes:
                    if i == 2:
                        i += 1
                    lighting_merge.setInput(i, input)
                    i += 1
                makeBackdrop('Lighting AOVs')
            else:
                lighting_merge = lighting_nodes  # if only one lighting node connect to the switch anyway

        # same thing for lightgroups
        lightgroups_nodes = []
        if makeAOVPaths('lightgroups'):
            for filepath in makeAOVPaths('lightgroups'):
                read = nuke.nodes.Read()
                read['file'].fromUserText(_render_dir + filepath)
                read.setXpos(read.xpos() + 110)
                read.setSelected(True)
                lightgroups_nodes.append(read)
            if len(lightgroups_nodes) >= 1:
                avgxpos = sum([n.xpos() for n in lightgroups_nodes])/len(lightgroups_nodes)
                avgypos = sum([n.ypos() for n in lightgroups_nodes])/len(lightgroups_nodes)
                lightgroups_merge = nuke.nodes.Merge2(
                    operation='plus',
                    output='rgb',
                    selected=True,
                    xpos=avgxpos,
                    ypos=avgypos + 400)
                i = 0
                for input in lightgroups_nodes:
                    if i == 2:
                        i += 1
                    lightgroups_merge.setInput(i, input)
                    i += 1
                makeBackdrop('Lightgroups')
            else:
                lightgroups_merge = lightgroups_nodes

        # same for utility passes
        if makeAOVPaths('utility'):
            _x_offset = 220
            for filepath in makeAOVPaths('utility'):
                read = nuke.nodes.Read()
                read['file'].fromUserText(_render_dir + filepath)
                read.setXpos(beauty_read.xpos() + _x_offset)
                _x_offset += 220
                read.setYpos(read.ypos() - 500)  # put utility above main passes, as in the current template
                read.setSelected(True)
            makeBackdrop('Utility')

        # same for cryptomatte
        if makeAOVPaths('crypto'):
            if not makeAOVPaths('utility'):
                _x_offset = 220
            for filepath in makeAOVPaths('crypto'):
                read = nuke.nodes.Read()
                read['file'].fromUserText(_render_dir + filepath)
                read.setXpos(beauty_read.xpos() + _x_offset)
                _x_offset += 220
                read.setYpos(read.ypos() - 500)  # put crypto above main passes, as in the current template
                read.setSelected(True)
            makeBackdrop('Cryptomatte')

        # add a switch connected to merge nodes and beauty to compare
        switch = nuke.nodes.Switch(
            inputs=[beauty_read, lighting_merge, lightgroups_merge],
            xpos=lighting_merge.xpos(),
            ypos=lighting_merge.ypos() + 400,
            label='[if {[numvalue this.which] == 0} {return "BEAUTY"}\nif {[numvalue this.which] == 1} {return "AOVs"}\nif {[numvalue this.which] == 2} {return Lightgroups}]'
            )
        createdNodes.append(switch)
        # set everything to selected so the user can move the template more easily
        for n in createdNodes:
            n.setSelected(True)
        app.restoreOverrideCursor()


def updateTemplate():
    thisNode = nuke.thisNode()
    # nuke.root().begin()
    if nuke.selectedNodes():
        for sel_node in nuke.selectedNodes():
            if sel_node.Class() == 'Read':
                # oldpass = sel_node['file'].getValue().split('_')[-2]
                nuke.root().end()
                new_path = thisNode['new_path'].getValue()
                pass_list = nuke.getFileNameList(new_path)
                thisknob = nuke.thisKnob().name()

                if thisknob == 'custom':
                    pass_name = thisNode.knob('pass_name').getValue()
                else:
                    pass_name = thisknob
                our_pass = [s for s in pass_list if pass_name in s]

                if our_pass == []:
                    nuke.message('Pass not found !')
                else:
                    sel_node['file'].fromUserText(new_path + str(our_pass[0]))

            elif sel_node:
                if sel_node.name() == thisNode.name():
                    nuke.message('Don\'t select this node !')
            else:
                nuke.message("Select a node first.")
