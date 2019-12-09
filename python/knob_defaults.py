# coding=utf-8
import nuke

nuke.knobDefault("TimeClip.label", "[value first]-[value last]")
nuke.knobDefault("Dot.note_font", "Bitstream Vera Sans Bold")
nuke.knobDefault("Dot.note_font_size", "21")
nuke.knobDefault("BackdropNode.note_font_size", "72")
nuke.knobDefault("TimeOffset.label", "[value time_offset]")
nuke.knobDefault("Colorspace.label", "[value colorspace_in] > [value colorspace_out]")
nuke.knobDefault("ChannelMerge.label", "")

# Excludes labels, which are defined below
default_knobs = {
    # Draw
    "Roto.toolbox": "createBSpline",
    "Roto.output": "alpha",
    "Roto.cliptype": "no_clip",
    # "Roto.postage_stamp": "1"
    "RotoPaint.toolbox": "clone",
    "RotoPaint.cliptype": "no_clip",
    # Image
    # "Write.channels": "rgb",
    # Channels
    # "Copy.bbox": "A"
    "Remove.operation": "keep",
    "Remove.channels": "rgb",
    # Color
    "Multiply.channels": "alpha",
    "Invert.channels": "alpha",
    "Gamma.channels": "alpha",
    "HueShift.ingray": "0.18",
    "HueShift.outgray": "0.18",
    "Clamp.channels": "rgba",
    # "Saturation.mode": "Ccir 601",
    "Grade.channels": "rgba",
    "ColorLookup.channels": "rgb",
    "Add.channels": "rgb",
    "SoftClip.conversion": "logarithmic compress",
    "SoftClip.softclip_min": "1",
    "OCIOLogConvert.operation": "lin to log",
    "RolloffContrast.soft_clip": "1",
    # Filter
    "Blur.channels": "rgba",
    "Blur.size": "2",
    "EdgeBlur.channels": "rgba",
    "EdgeBlur.size": "2",
    "Defocus.channels": "rgba",
    "Defocus.size": "2",
    "DirBlurWrapper.channels": "rgba",
    "Soften.channels": "rgba",
    "Dilate.channels": "rgba",  # who uses dilate
    "Convolve2.channels": "rgba",
    "Convolve2.use_input_channels": "1",
    "VectorBlur.uv": "forward",
    "VectorBlur.scale": "1",
    "VectorBlur.channels": "rgba",
    "VectorBlur2.channels": "rgba",
    "VectorBlur2.scale": "1",
    "Sharpen.channels": "rgb",
    "ZDefocus2.channels": "rgba",
    "GodRays.channels": "rgba",
    # Merge
    "Keymix.channels": "rgba",
    "Keymix.bbox": "B",
    "Dissolve.channels": "rgba",
    "ContactSheet.roworder": "TopBottom",
    "ContactSheet.width": "root.format.w",
    "ContactSheet.height": "root.format.h",
    "Merge.bbox": "B",
    # "Merge.bbox":  "union",
    # Transform
    # "Crop.intersect": "1",
    "Splinewarp3.splinetools": "createBspline",
    "STMap.channels": "rgba",
    "STMap.uv": "rgb",
    # "Tracker.zoom_window_behaviour": "4",
    # "Tracker.zoom_window_filter_behaviour": "2",
    # "Tracker.keyframe_display": "3",
    "Tracker4.zoom_window_behaviour": "2",
    "Tracker4.adjust_for_luminance_changes": "1",
    "Tracker4.warp": "affine",
    # 3D
    "RayRender.AOV_Point": "__Pworld",
    "RayRender.AOV_Normal": "__Nworld",
    "RayRender.AOV_Motion": "__motion",
    "RayRender.AOV_Point": "__Pworld",
    "RayRender.AOV_Direct_Diffuse": "__direct_diffuse",
    "RayRender.AOV_Direct_Specular": "__direct_specular",
    "RayRender.AOV_Reflection": "__indirect_specular",
    "RayRender.AOV_Emissive": "__incandescance",
    "RayRender.output_shader_vectors": "1",
    "Project3D.crop":  "false",
    # Deep
    "DeepReformat.pbb": "1",
    # Other
    "Dot.note_font_size": "50",
    "Dot.note_font_color": "0x00FF0000",
    "Dot.note_font":  "Bitstream Vera Sans",
    "BackdropNode.note_font_size":  "72",
    # "Expression.expr3": "a==0?0:1",
    # Result:
}

default_labels = {
    # Image
    "Read": "[value first]-[value last]",
    # Draw
    # "Roto": "[if {[value replace]} {return \"replace\"}]",
    "RotoPaint": "[if {[value outputMask]!=\"none\"} {return \"outputMask\"}]",
    # Channels
    "Shuffle": "[value in 1]",
    # Color
    "Multiply": "[value value]",
    "Colorspace": "[value colorspace_in] to [value colorspace_out]",
    # Filter
    "Blur": "[value size]px",
    "Defocus": "[value defocus]px",
    # Transform
    "Tracker4": "[if {[value transform]!=\"none\"} {return \"[value transform] ([value reference_frame])\"}]",
    "Transform": "[expr {[value translate.x] !=0 ? \"[format %.f [value translate.x]]x \" : \"\"}][expr {[value translate.y] !=0 ? \"[format %.f [value translate.y]]y \" : \"\"}][expr {[value rotate] !=0 ? \"[format %.1f [value rotate]]° \" : \"\"}][expr {[value scale.w] != [value scale.h] ? \"scale: [format %.2f [value scale.w]]x [value scale.h]y\" : [value scale] !=1 ? \"x[format %.2f [value scale.h]]\" : \"\"}]\n[expr {[value skewX] !=0 ? \"Skew X: [format %.2f [value skewX]] \" : \"\"}][expr {[value skewY] !=0 ? \"Skew Y: [format %.2f [value skewY]]\" : \"\" }][expr {[value inverted_matrix] ? \" inverted\" : \"\"}]",
    "CornerPin2D": "[if {[value invert]} {return \"inverted\"}]",
    "VectorDistort": "[value referenceFrame]",
    # Time
    "TimeClip": "[value first]-[value last]",
    "TimeOffset": "[value time_offset]",
    # Stereo
    "Oneview": "[value view]",
    # Other
    # "Expression": "Alpha = [value expr3]",
}

# actually set stuff
nuke.tprint("Setting Tom's knob defaults")
for i in default_knobs:
    nuke.knobDefault(i, default_knobs[i])

nuke.tprint("Setting Tom's label defaults")
for i in default_labels:
    knob = "{0}.label".format(i)
    nuke.knobDefault(knob, default_labels[i])


# Having the labels separately allows to set them after creation
# i.e. on existing scripts, via this function:
def set_default_labels():
    for this_class in default_labels:
        for n in nuke.allNodes(filter=this_class, group=nuke.root()):
            n["label"].setValue(default_labels[this_class])
