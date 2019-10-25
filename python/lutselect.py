
__author__ = 'Tom Mortelette'
__description__ = 'LUT Selector'


#Select a node and run this in the script editor in Nuke to add the callback to the group

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
import pprint


# callback
def knobChanged():
    k = nuke.thisKnob()     # knob that was just changed
    
    # LUT selection changed, update LUT node file path
    if k.name() == 'lut_pulldown':
        main().setLut()

    # project set, load list of luts
    elif k.name() == 'project':
        main().getLuts()


def setup(node={}, project=''):
    _main(node=node, project=project).setup()
    

class _main:

    def __init__(self, node={}, project=''):
        self.project = project
        if node:
            print 'main.setup node: {0}'.format(node['name'].value())
            thisNode = node
        else:
            # print 'no node arg, using nuke.thisNode()'
            thisNode = nuke.thisNode()
            print 'main.setup node: {0}'.format(node['name'].value())
        if thisNode.Class() == 'NoOp' and 'LUT_Select_Controller' in thisNode['name'].value():
            self.n = thisNode
        elif thisNode.Class() == 'Group' and 'LUT_Select' in thisNode['name'].value():
            thisNode.begin()
            self.n = nuke.toNode('LUT_Select_Controller')
            # thisNode.end()
        else:
            nuke.alert('Unable to find LUT_Select or LUT_Select_Controller')
            return
        self.shot_lut_node = nuke.toNode('SHOT_LUT')
        self.show_lut_node = nuke.toNode('SHOW_LUT')
        if self.shot_lut_node:
            print 'FOUND SHOT LUT NODE'
        else:
            print 'NOT FOUND SHOT LUT NODE'
        self.u_shot = os.environ['U_SHOT']
        print 'Called on {0}'.format(thisNode['name'].value())




    # called by button in UI or callback 
    def setup(self):
        self.sg_current_project = su.get_project(os.environ['U_PROJECT'])
        # populate projects list
        global active_projects
        active_projects = su.get_projects()
        self.n['project'].setValues(sorted(active_projects.keys()))
        self.n['lut_dict'].setValue('')
        #set active projst
        if self.project:
            self.n['project'].setValue(self.project)
        elif self.sg_current_project:
            self.n['project'].setValue(self.sg_current_project['name'])
            print 'Current project: {0}'.format(self.sg_current_project['name'])
        else:
            print 'Unable to detect project!'

        #set lut to current shot
        if self.u_shot:
            self.n['lut_pulldown'].setValue(self.u_shot)
        else:
            self.n['lut_pulldown'].setValue(0)
        self.setLut()


    def setLut(self):
        global active_projects
        shot = self.n['lut_pulldown'].value()
        if shot:
            try:
                shot = shot.split('/')[1]
                print 'Setting lut for {0}'.format(shot)
            except:
                print "Shot not part of a sequence?"
            lut_dict_string = self.n['lut_dict'].value()
            if lut_dict_string:
                lut_dict = ast.literal_eval(lut_dict_string)
                try:
                    lutfile = lut_dict[shot]
                except Exception as e:
                    print "Could not get lut file for shot {0}. Error: {1}".format(shot, e)
                    return
                project = self.n['project'].value()
                lutdir = '/Volumes/projects/{0}/assets/in/luts/'.format(active_projects[project]['sg_data']['tank_name'])
                lutpath = os.path.join(lutdir, lutfile)
                print 'lutpath: {0}'.format(lutpath)
                if self.shot_lut_node:
                    print 'self.shot_lut_node'
                    pprint.pprint(self.shot_lut_node['name'].value()) 
                else:
                    print 'NO SHOT LUT NODE'               
                self.shot_lut_node['file'].setValue(lutpath)
            # else:
            #     print 'lut_dict_string knob is empty'
        else:
            print "No shot, clearing LUT"
            self.shot_lut_node['file'].setValue('')


    def getLuts(self):
        #Project changed, build LUT list and set show LUT
        pulldown_items = []
        sg = su.Shotgun()
        project = self.n['project'].value()
        sg_project = su.get_project(project)
        filters = [['project', 'is', sg_project]]
        fields = ['code', 'sg_sequence', 'sg_lut', 'sg_show_lut']
        shots = sg.find('Shot', filters=filters, fields=fields)
        lut_dict = {}
        print 'Getting luts for {0}'.format(project)
        if shots:
            for shot in shots:
                if shot['sg_lut']:
                    lut_dict[shot['code']] = shot['sg_lut']
                    shots_by_sequence = str(shot['sg_sequence']['name']) + '/' + str(shot['code'])
                    pulldown_items.append(str(shots_by_sequence))
                show_lut = shot['sg_show_lut']
            pulldown_items.sort()
            if lut_dict:
                self.n['lut_dict'].setValue(str(lut_dict))
                self.n['lut_pulldown'].setValues(pulldown_items)
                self.n['lut_pulldown'].setValue(pulldown_items[0])
                self.setLut()
            else:
                self.n['lut_pulldown'].setValues(['No LUTs found!'])
                self.n['lut_pulldown'].setValue('No LUTs found!')
                self.n['lut_dict'].setValue('EMPTY')
                self.shot_lut_node['file'].setValue('')
                print 'No LUTs found!'
            #set show lut
            if self.show_lut_node:
                if show_lut:
                    show_lut_path = os.path.join(self.getLutDir(project), show_lut)
                    self.show_lut_node['file'].setValue(show_lut_path)
                else:
                    self.show_lut_node['file'].setValue('')
            else:
                print 'No SHOW_LUT node, not setting'
        else:
            self.n['lut_pulldown'].setValues(['No shots found!'])
            self.n['lut_pulldown'].setValue('No shots found!')
            self.shot_lut_node['file'].setValue('')
            print 'No shots found!'