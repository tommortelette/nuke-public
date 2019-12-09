# Select a node and run this in the script editor in Nuke
# to add the callback to the group

'''
import lutselect
reload(lutselect)
nuke.root().begin()
sel = nuke.selectedNode()
sel.begin()
n = nuke.toNode('LUT_Select_Controller')
n['knobChanged'].setValue('lutselect.knobChanged()')
n['onCreate'].setValue('lutselect.setup()')
sel.end()
'''

import nuke
import os
from core import shotgunutils as su
import ast


__author__ = 'Tom Mortelette'
__description__ = 'LUT Selector'


# callback
def knobChanged():
    k = nuke.thisKnob()     # knob that was just changed
    # LUT selection changed, update LUT node file path
    if k.name() == 'lut_pulldown':
        _main().setLut()
    # project set, load list of luts
    elif k.name() == 'project':
        _main().getLuts()


def addFromMenu(project=''):
    if not project:
        group = nuke.nodePaste(
            '/Volumes/resources/tool_archive/internal/nuke/python/lutselect/LUT_Select_1.2.nk')
    elif project == 'Emma':
        group_path = '/Volumes/resources/tool_archive/internal/nuke/python/lutselect/LUT_Select_' + project + '.nk'
        group = nuke.nodePaste(group_path)
    setup(node=group, project='')


def setup(node={}, project=''):
    global active_projects
    global n
    n = ''
    _main(node=node, project=project).setup()
    active_projects = {}


class _main:
    def __init__(self, node='', project=''):
        self.project = project
        global n
        if not n:
            if node:
                print('main.setup node: {0}'.format(node['name'].value()))
                thisNode = node
            else:
                # print 'no node arg, using nuke.thisNode()'
                thisNode = nuke.thisNode()
                print('main.__init__ node: {0}'.format(node['name'].value()))
            if thisNode.Class() == 'NoOp' and 'LUT_Select_Controller' in thisNode['name'].value():
                n = thisNode
            elif thisNode.Class() == 'Group' and 'LUT_Select' in thisNode['name'].value():
                thisNode.begin()
                n = nuke.toNode('LUT_Select_Controller')
                # thisNode.end()
            else:
                nuke.alert(
                    'Unable to find LUT_Select or LUT_Select_Controller')
                return

        self.shot_lut_node = nuke.toNode('SHOT_LUT')
        self.show_lut_node = nuke.toNode('SHOW_LUT')
        self.u_shot = os.environ['U_SHOT']
        # print 'Called on {0}'.format(n['name'].value())

    # called by button in UI or callback
    def setup(self):
        global n
        self.sg_current_project = su.get_project(os.environ['U_PROJECT'])
        # populate projects list
        active_projects = su.get_projects()
        global tank_names
        tank_names = {}
        for project in active_projects:
            tank_names[project] = active_projects[project]['sg_data']['tank_name']
        n['project'].setValues([])
        n['project'].setValues(sorted(active_projects.keys()))
        n['lut_dict'].setValue('')
        # set active projst
        if self.project:
            n['project'].setValue(self.project)
        elif self.sg_current_project:
            n['project'].setValue(self.sg_current_project['name'])
            print 'Current project: {0}'.format(self.sg_current_project['name'])
        else:
            print 'Unable to detect project!'

        # set lut to current shot
        if self.u_shot:
            n['lut_pulldown'].setValue(self.u_shot)
        else:
            n['lut_pulldown'].setValue(0)
        self.setLut()

    def setLut(self):
        global n
        global tank_names
        shot = n['lut_pulldown'].value()
        if shot:
            try:
                shot = shot.split('/')[1]
                print 'Setting lut for {0}'.format(shot)
            except:
                print "Shot not part of a sequence, this shouldn't happen"
            lut_dict_string = n['lut_dict'].value()
            if lut_dict_string:
                lut_dict = ast.literal_eval(lut_dict_string)
                try:
                    lutfile = lut_dict[shot]
                except Exception as e:
                    print "Could not get lut file for shot {0}. Error: {1}".format(shot, e)
                    return
                project = n['project'].value()
                lutdir = '/Volumes/projects/{0}/assets/in/luts/'.format(
                    tank_names[project])
                lutpath = os.path.join(lutdir, lutfile)
                print 'lutpath: {0}'.format(lutpath)
                if not self.shot_lut_node:
                    print 'NO SHOT LUT NODE'
                    return
                self.shot_lut_node['file'].setValue(lutpath)
            # else:
            #     print 'lut_dict_string knob is empty'
        else:
            print "No shot, clearing LUT"
            self.shot_lut_node['file'].setValue('')

    def getLuts(self):
        # Project changed, build LUT list and set show LUT
        pulldown_items = []
        sg = su.Shotgun()
        project = n['project'].value()
        print 'Getting the list of shots for {0}'.format(project)
        sg_project = su.get_project(project)
        filters = [['project', 'is', sg_project]]
        fields = ['code', 'sg_sequence', 'sg_lut', 'sg_show_lut']
        shots = sg.find('Shot', filters=filters, fields=fields)
        lut_dict = {}
        if shots:
            print 'Getting the list of luts for {0}'.format(project)
            for shot in shots:
                if shot['sg_lut']:
                    lut_dict[shot['code']] = shot['sg_lut']
                    shots_by_sequence = str(
                        shot['sg_sequence']['name']) + '/' + str(shot['code'])
                    pulldown_items.append(str(shots_by_sequence))
                show_lut = shot['sg_show_lut']
            pulldown_items.sort()
            if lut_dict:
                n['lut_dict'].setValue(str(lut_dict))
                n['lut_pulldown'].setValues(pulldown_items)
                n['lut_pulldown'].setValue(pulldown_items[0])
                self.setLut()
            else:
                n['lut_pulldown'].setValues(['No LUTs found!'])
                n['lut_pulldown'].setValue('No LUTs found!')
                n['lut_dict'].setValue('EMPTY')
                self.shot_lut_node['file'].setValue('')
                print 'No LUTs found!'
            # set show lut
            if self.show_lut_node:
                if show_lut:
                    show_lut_path = os.path.join(
                        self.getLutDir(project), show_lut)
                    self.show_lut_node['file'].setValue(show_lut_path)
                else:
                    self.show_lut_node['file'].setValue('')
            else:
                print 'No SHOW_LUT node, not setting'
        else:
            n['lut_pulldown'].setValues(['No shots found!'])
            n['lut_pulldown'].setValue('No shots found!')
            self.shot_lut_node['file'].setValue('')
            print 'No shots found!'
