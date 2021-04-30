import nuke

# Defaults
import knob_defaults

nuke.tprint("Setting Tom's label defaults")
knob_defaults.set_default_labels()

nuke.tprint("Setting Tom's knob defaults")
knob_defaults.set_default_knobs()

# Shortcuts
nuke.toolbar('Nodes').addCommand('Channel/ChannelMerge', 'nuke.createNode("ChannelMerge")', 'shift+c', shortcutContext=dagContext)
nuke.toolbar('Nodes').addCommand('Transform/TransformMasked', 'nuke.createNode("TransformMasked")', 'shift+t', shortcutContext=dagContext)

# Tom's Python stuff
import tm_tools

tomsMenu = nuke.menu('Nuke').addMenu('Tom\'s tools')

tomsMenu.addCommand('Set Corner Pin reference frame', 'tm_tools.setCornerPinRefFrame()', icon='CornerPin.png')
tomsMenu.addCommand('Enable Tracker TRS checkboxes', 'tm_tools.enable_Tracker_TRS()', icon='Tracker.png')
tomsMenu.addCommand('Set colorspace on selected Read nodes', 'tm_tools.change_colorspace_menu()', icon='ColorSpace.png')
tomsMenu.addCommand('Unhide inputs for selected nodes', 'tm_tools.unhideInput()', icon='Input.png')
# tomsMenu.addSeparator()
tomsMenu.addCommand('Disable selected in GUI', "tm_tools.disable_in_gui(action='enable')", icon='Switch.png')
tomsMenu.addCommand('Enable selected in GUI', "tm_tools.disable_in_gui(action='disable')", icon='Switch.png')
tomsMenu.addCommand('Set Frame Range to scan', 'tm_tools.setFrameRange()', icon='Render.png')
tomsMenu.addCommand('Show Node Classes', 'tm_tools.showNodeByClass()', icon='Assert.png')
# lm.addCommand('Clear Channelmerge labels', "tm_tools.clearLabels(nodeClass='ChannelMerge')", icon='StickyNote.png')
tomsMenu.addCommand("Set Tom's label defaults", "knob_defaults.set_labels_on_existing_nodes()", icon='StickyNote.png')

# tomsMenu.addCommand('Global Motionblur Controller', 'moblur_controller.moblur_controller()')

# nuke.knobDefault('Read.label', "Fr. range: [value first] - [value last]\nRes: [value width] * [value height]")
# nuke.knobDefault('Switch.label', "Which: [value which]")
# nuke.knobDefault('Dissolve.label', "Which: [value which]")
# nuke.knobDefault('Blur.label', "Size: [value size]")
# nuke.knobDefault('Defocus.label', "Size: [value defocus]")
# nuke.knobDefault('ZDefocus2.label', "Size: [value size]")
# nuke.knobDefault('Multiply.label', "Value: [value value]")
# nuke.knobDefault('Saturation.label', "Value: [value saturation]")
# nuke.knobDefault('TimeOffset.label', "Value: [value time_offset]")
# nuke.knobDefault('Crop.label', "Box: x:[value box.x]  y:[value box.y] r:[value box.r] t:[value box.t]")
# nuke.knobDefault('Constant.label', "Res: [value width] * [value height]")
# nuke.knobDefault('CheckerBoard2.label', "Res: [value width] * [value height]")
# nuke.knobDefault('Soften.label', "Size: [value size]")
# nuke.knobDefault('Sharpen.label', "Size: [value size]")
# nuke.knobDefault('IDistort.label', "Scale: [value uv_scale]")
# nuke.knobDefault('Retime.label', "Out: [value output.first] - [value output.last]")
# nuke.knobDefault('EdgeBlur.label', "Size: [value size]")
# nuke.knobDefault('STMap.label', "UV: [value uv]")
# nuke.knobDefault('Camera2.label', "File: [file tail [value file]]")
# nuke.knobDefault('nuke_dispatch.label', "Range: [value framestart] - [value frameend]")
# nuke.knobDefault('nuke_dispatch.batch', "1")
# nuke.knobDefault('Merge.bbox', 'B')
