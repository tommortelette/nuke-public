import nuke
import PySide2
import nukescripts

app = PySide2.QtWidgets.QApplication.instance()
busy_cursor = PySide2.QtGui.QCursor(PySide2.QtCore.Qt.WaitCursor)

def makeAOVPaths(aov_type):
    pass_list = nuke.getFileNameList(render_dir)
    arnold_lighting_aovs = ['diffuse_direct', 'diffuse_indirect', 'specular_direct', 'specular_indirect', 'emission', 'transmission', 'sss', 'coat']
    arnold_utility_aovs = ['N', 'P', 'Z', 'shadow_matte', 'shadow', 'motionVector']
    arnold_crypto_aovs = ['crypto_asset', 'crypto_material', 'crypto_object']
    lighting_paths = []
    utility_paths = []
    crypto_paths = []
    beauty_path = ''
    lightgroups_paths = []

    if aov_type == 'lighting':
        for aov in arnold_lighting_aovs:
            this_pass = [p for p in pass_list if aov in p]
            if this_pass != []:
                lighting_paths.append(str(this_pass[0]))
        return lighting_paths


    elif aov_type == 'utility':
        for aov in arnold_utility_aovs:
            this_pass = [p for p in pass_list if aov in p]
            if this_pass != []:
                utility_paths.append(str(this_pass[0]))
        return utility_paths

    elif aov_type == 'crypto':
        for aov in arnold_crypto_aovs:
            this_pass = [p for p in pass_list if aov in p]
            if this_pass != []:
                crypto_paths.append(str(this_pass[0]))
        return crypto_paths

    elif aov_type == 'beauty':
        for p in pass_list:
            if 'beauty' in p:
                beauty_path = p
                break
        return beauty_path

    elif aov_type == 'lightgroups':
        for p in pass_list:
            if 'RGBA' in p:
                lightgroups_paths.append(p)
        return lightgroups_paths

    else:
        return None



def deSelectAll():
    if nuke.selectedNodes():
        for n in nuke.selectedNodes():
            n['selected'].setValue(False)

x_offset = 0

def setOffset(node):
    global x_offset
    node.setXpos(node.xpos() + x_offset )
    x_offset =+ 110

def makeBackdrop(label):
    backdrop = nukescripts.autobackdrop.autoBackdrop()
    backdrop['label'].setValue(label)
    backdrop.setYpos(backdrop.ypos())
    backdrop['bdheight'].setValue(backdrop['bdheight'].getValue() + 100)
    deSelectAll()


def buildTemplate():
    global render_dir 
    render_dir = nuke.getClipname('Select Render folder', '*.exr')
    if render_dir:
        try:
            app.setOverrideCursor(busy_cursor)
            deSelectAll()
            if makeAOVPaths('beauty'):
                beauty_read = nuke.nodes.Read()
                beauty_read['file'].fromUserText(render_dir + makeAOVPaths('beauty'))
                beauty_read.setSelected(True)
                setOffset(beauty_read)
                makeBackdrop('Beauty')


            lighting_nodes = []
            lighting_nodes_xpos = []
            lighting_nodes_ypos = []

            if makeAOVPaths('lighting'):
                for filepath in makeAOVPaths('lighting'):
                    read = nuke.nodes.Read()
                    read['file'].fromUserText(render_dir + filepath)
                    setOffset(read)
                    read.setSelected(True)
                    lighting_nodes.append(read)
                    lighting_nodes_xpos.append(read.xpos())
                    lighting_nodes_ypos.append(read.ypos())
                if len(lighting_nodes) >= 1:
                    lighting_nodes_xcenter = sum(lighting_nodes_xpos) / len(lighting_nodes)
                    lighting_nodes_ycenter = sum(lighting_nodes_ypos) / len(lighting_nodes)
                    lighting_merge = nuke.nodes.Merge2(operation = 'plus', selected = True, inputs = lighting_nodes, xpos = lighting_nodes_xcenter, ypos = lighting_nodes_ycenter + 500)
                    makeBackdrop('Lighting AOVs')



            lightgroups_nodes = []
            lightgroups_nodes_xpos = []
            lightgroups_nodes_ypos = []
            
            if makeAOVPaths('lightgroups'):
                for filepath in makeAOVPaths('lightgroups'):
                    read = nuke.nodes.Read()
                    read['file'].fromUserText(render_dir + filepath)
                    setOffset(read)
                    read.setSelected(True)
                    lightgroups_nodes.append(read)
                    lightgroups_nodes_xpos.append(read.xpos())
                    lightgroups_nodes_ypos.append(read.ypos())
                if len(lightgroups_nodes)>=1:
                    lightgroups_nodes_xcenter = sum(lightgroups_nodes_xpos) / len(lightgroups_nodes)
                    lightgroups_nodes_ycenter = sum(lightgroups_nodes_ypos) / len(lightgroups_nodes)
                    lightgroups_merge = nuke.nodes.Merge2(operation = 'plus', selected= True, inputs = lightgroups_nodes, xpos = lightgroups_nodes_xcenter, ypos = lightgroups_nodes_ycenter + 500)
                makeBackdrop('Lightgroups')

            
            if makeAOVPaths('utility'):
                for filepath in makeAOVPaths('utility'):
                    read = nuke.nodes.Read()
                    read['file'].fromUserText(render_dir + filepath)
                    setOffset(read)
                    read.setSelected(True)
                makeBackdrop('Utility')

            if makeAOVPaths('crypto'):
                for filepath in makeAOVPaths('crypto'):
                    read = nuke.nodes.Read()
                    read['file'].fromUserText(render_dir + filepath)
                    setOffset(read)
                    read.setSelected(True)
                makeBackdrop('Cryptomatte')


            switch_inputs = [beauty_read, lighting_merge, lightgroups_merge]
            switch = nuke.nodes.Switch(inputs = switch_inputs, xpos = lighting_merge.xpos(), ypos = lighting_merge.ypos() + 500, label = '[if {[numvalue this.which] == 0} {return "BEAUTY"}\nif {[numvalue this.which] == 1} {return "AOVs"}\nif {[numvalue this.which] == 2} {return Lightgroups}] ')
            app.restoreOverrideCursor()
        except:
            app.restoreOverrideCursor()
    else:
        return