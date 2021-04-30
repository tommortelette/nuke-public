# Tom Mortelette's various Python tools and things
import nuke
import nukescripts

# This sets the 'from' values to the 'to' values of the current frame,
# which is equivalent to the 'set reference frame' in the built-in Tracker node
# This is meant for  using Mocha tracks exported as 'Nuke Corner Pin'


def setCornerPinRefFrame():
    corners = ['1', '2', '3', '4']   # the corner pin corners
    for node in nuke.selectedNodes():
        if node.Class() == 'CornerPin2D':
            for corner in corners:
                node['from' + corner].clearAnimated()     # clear old 'from' values
                newFrom = node['to' + corner].getValue()  # copy 'to' values
                node['from' + corner].setValue(newFrom)   # paste them to 'from'


def unhideInput():
    for node in nuke.selectedNodes():
        try:
            node['hide_input'].setValue(False)
        except Exception:
            pass


def showNodeByClass():
    namesAndClasses = ''
    for n in nuke.selectedNodes():
        namesAndClasses = namesAndClasses + n.name() + ': ' + n.Class() + '\n'
    nuke.message(namesAndClasses)


def disable_in_gui(action):
    if action == 'enable':
        for n in nuke.selectedNodes():
            n['disable'].setExpression('![python nuke.executing()]')

    elif action == 'disable':
        for n in nuke.selectedNodes():
            if n['disable'].hasExpression():
                if n['disable'].animations()[0].expression() in ['$gui', '![python nuke.executing()]']:
                    n['disable'].clearAnimated()
                    n['disable'].setValue(False)
    else:
        print('Invalid action specified: %s', action)


def setFrameRange():
    if not nuke.selectedNodes():
        nuke.message('Select a node !')
    elif len(nuke.selectedNodes()) > 1:
        nuke.message('Select only one node !')
    else:
        n = nuke.selectedNode()
        if n.Class() != 'Read':
            nuke.message('Select a read node !')
        else:
            newFirst = n['first'].getValue()
            newLast = n['last'].getValue()
            nuke.root()['first_frame'].setValue(newFirst)
            nuke.root()['last_frame'].setValue(newLast)


def clearLabels(nodeClass=None):
    if not nodeClass:
        nuke.alert("No node class specified!")
    else:
        for n in nuke.allNodes(nodeClass):
            n.knob('label').setValue('')


# ENABLE TRANSLATE, ROTATE AND SCALE IN SELECTED TRACKER
def enable_Tracker_TRS():

    # magic numbers
    t = [8, 39, 70, 101, 132, 163, 194, 225, 256, 287, 318, 7, 38, 69, 100, 131, 162,
         193, 224, 255, 286, 317, 6, 37, 68, 99, 130, 161, 192, 223, 254, 285, 316, 349, 380, 411,
         442, 473, 504, 535, 566, 597, 628, 659, 348, 379, 410, 441, 472, 503, 534, 565, 596, 627,
         658, 347, 378, 409, 440, 471, 502, 533, 564, 595, 626, 657]

    try:
        nuke.selectedNode()
    except Exception:
        return

    if nuke.selectedNode().Class() == 'Tracker4':
        nuke.selectedNode()['reference_frame'].setValue(nuke.frame())
        for n in t:  # dark magic
            nuke.selectedNode()['tracks'].setValue(True, n)


class ColorspaceMenu(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Select a colorspace')
        sel = nuke.selectedNodes(filter='Read')

        # Read list of available colorspaces from first read node. Probably a better way to do this
        self.cs_list = sel[0]['colorspace'].values()
        self.cs_knob = nuke.CascadingEnumeration_Knob('out_cs', 'target colorspace: ', self.cs_list)
        self.raw_knob = nuke.Boolean_Knob('out_raw', 'RAW')
        self.raw_knob.setFlag(nuke.STARTLINE)
        self.addKnob(self.cs_knob)
        self.addKnob(self.raw_knob)

    def knobChanged(self, knob):
        # disable cs_list if raw is selected
        if knob is self.raw_knob:
            raw_false = not self.raw_knob.value()
            self.cs_knob.setEnabled(raw_false)


def change_colorspace_menu():
    # Changes selected read/writes nodes to the specified colorspace
    selection = nuke.selectedNodes(filter='Read')
    if selection:
        # show the UI
        cs_menu = ColorspaceMenu()
        if cs_menu.showModalDialog():
            if cs_menu.raw_knob.value():
                for n in selection:
                    n['raw'].setValue(True)
            else:
                for n in selection:
                    n['raw'].setValue(False)
                    n['colorspace'].setValue(cs_menu.cs_knob.value())
    else:
        nuke.alert('No Read nodes selected!')


def motionblur_master_control(action):

    classes_2d = ["CameraShake", "CornerPin2D", "Transform", "TransformMasked", "Tracker4"]
    classes_3d = ["ScanlineRender", "RayRender"]
    all_classes = classes_2d + classes_3d
    linked_knobs = ("shutteroffset", "motionblur", "shutter")

    if action == "destroy":
        for node in nuke.allNodes():
            # if node.Class() in 2d_classes or node.Class() in 3d_classes:
            for knob in linked_knobs:
                node[knob].clearAnimated()

        master = nuke.toNode("TM_MotionBlurMaster")
        nuke.delete(master)

    elif action == "create":
        # if master control already exists skip creating it
        nodes_names = [['name'].value() for n in nuke.allNodes()]

        if 'TM_MotionBlurMaster' not in nodes_names:
            master = nuke.createNode('NoOp')

        for node in nuke.allNodes():
            if node.Class() in []:
                node["shutteroffset"].setValue("centered")
                node["motionblur"].setExpression("NoOp1.samples")
                node["shutter"].setExpression("NoOp1.shutter")
                # maybe also more nodes, transform etc


for v in nuke.allNodes(filter='Viewer'):
    if v['downrez'].value() != '1':
        is_downrez = True
        break
    else:
        is_downrez = False

is_proxy = nuke.Root()['proxy'].value()

if is_proxy and is_downrez:
    nuke.alert('<font size=6 color=red>NOT FULL SIZE !!!!!')
