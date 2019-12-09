import nuke
import os
import tm_tools
import knob_defaults
import passbuilder

# nuke.toolbar('Nodes').addCommand("Draw/ColorTexturePaint", "nuke.createNode('ColorTexturePaint')", icon='ColorTexturePaint.png')
nuke.toolbar("Nodes").addCommand("Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue(nuke.frame())")

# import readFromWrite
# nuke.toolbar("Nodes").addCommand("Image/Read from Write", "readFromWrite.ReadFromWrite()", "alt+r")

nuke.knobDefault('Root.format', 'DCI_Scope_2.39')
nuke.knobDefault('Root.first_frame', '1001')
nuke.knobDefault('Root.last_frame', '1100')

tomsMenu = nuke.menu('Nuke').addMenu('Tom\'s stuff')
tomsMenu.addCommand('Set Corner Pin reference frame', 'tm_tools.setCornerPinRefFrame()', icon='CornerPin.png')
tomsMenu.addCommand('Clear Channelmerge labels', "tm_tools.clearLabels(nodeClass='ChannelMerge')", icon='StickyNote.png')
tomsMenu.addCommand("Set default labels", "knob_defaults.set_default_labels()", icon='StickyNote.png')
tomsMenu.addCommand('Show Node Classes', 'tm_tools.showNodeByClass()', icon='Assert.png')
tomsMenu.addCommand('Unhide inputs for selected nodes', 'tm_tools.unhideInput()', icon='Input.png')
tomsMenu.addCommand('set $gui flag', "tm_tools.dollarGUIselected(action='enable')", icon='Switch.png')
tomsMenu.addCommand('remove $gui flag', "tm_tools.dollarGUIselected(action='disable')", icon='Switch.png')
tomsMenu.addCommand('Set Frame Range to scan', 'tm_tools.setFrameRange()', icon='Render.png')

# Tom Mortelette's CG template builder
tomsMenu.addSeparator()
tomsMenu.addCommand('CG Tools/Create QC template', 'passbuilder.buildTemplate()')
tomsMenu.addCommand('CG Tools/Update selected CG renders', 'passbuilder.updateTemplate()')
tomsMenu.addSeparator()
