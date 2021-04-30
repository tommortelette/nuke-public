# coding=utf-8
# Unicode is required for the degree symbol ° in the Transform label

import nuke


def set_labels_on_existing_nodes():
    for node_class in default_labels:
        for n in nuke.allNodes(filter=node_class, group=nuke.root()):
            n["label"].setValue(default_labels[node_class])


def set_default_labels():
    for l in default_labels:
        knob = "{0}.label".format(l)
        nuke.knobDefault(knob, default_labels[l])


def set_default_knobs():
    for k in default_knobs:
        nuke.knobDefault(k, default_knobs[k])


# Labels are defined separately so they can be set separately after node creation via a menu in the GUI
default_labels = {

    # Image
    "Read": "[value first]-[value last]",

    # Draw
    # "Roto": "[if {[value replace]} {return \"replace\"}]",
    "RotoPaint": "[if {[value outputMask]!=\"none\"} {return \"outputMask\"}]",

    # Channels
    "ChannelMerge": "",  # Ovverrides Union default
    "Shuffle": "[value in 1]",

    # Color
    "Multiply": "[value value]",
    "Colorspace": "[value colorspace_in] to [value colorspace_out]",
    "OCIOColorSpace": "[value in_colorspace] to [value out_colorspace]",

    # Filter
    "Blur": "[value size]px",
    "Defocus": "[value defocus]px",
    "Median": "[value size]px",

    # Transform
    "Tracker4": "[if {[value transform]!=\"none\"} {return \"[value transform] ([value reference_frame])\"}]",
    "Transform": "[expr {[value translate.x] !=0 ? \"[format %.f [value translate.x]]x \" : \"\"}][expr {[value translate.y] !=0 ? \"[format %.f [value translate.y]]y \" : \"\"}][expr {[value rotate] !=0 ? \"[format %.1f [value rotate]]° \" : \"\"}][expr {[value scale.w] != [value scale.h] ? \"scale: [format %.2f [value scale.w]]x [format %.2f [value scale.h]]y \" : [value scale] !=1 ? \"x[format %.2f [value scale.h]] \" : \"\"}][expr {[value skewX] !=0 ? \"Skew X: [format %.2f [value skewX]] \" : \"\"}][expr {[value skewY] !=0 ? \"Skew Y: [format %.2f [value skewY]]\" : \"\" }]\n[if {[value invert_matrix]} {return \"inverted\"}]",
    "CornerPin2D": "[if {[value invert]} {return \"inverted\"}]",
    "VectorDistort": "[value referenceFrame]",

    # Time
    "TimeClip": "[value first]-[value last]",
    "TimeOffset": "[value time_offset]",

    # Stereo
    "Oneview": "[value view]",

    # Gizmos
    "key_chew": "[if {[value chew] > 0} {return \"+\"}][value chew] / [value soften]",
}

default_knobs = {

    # testing area #
    # "Read.mov.colorspace": nuke.Root()['int8Lut'].value(),

    # Deadline submitter
    "Root.Threads": "0",
    "Root.ConcurrentTasks": "2",
    "Root.ChunkSize": "8",
    "Root.ContinueOnError": "False",

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
    "Grade.channels": "rgb",
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
    "Tracker4.zoom_window_behaviour": "2",
    "Tracker4.adjust_for_luminance_changes": "1",
    "Tracker4.warp": "affine",
    "Tracker4.clamp_footage": "0",
    "Tracker4.hide_progress_bar": "1",
    "Tracker4.shutteroffset": "center",
    "Transform.shutteroffset": "center",
    "CornerPin2D.shutteroffset": "center",

    # 3D
    "RayRender.AOV_Point": "__Pworld",
    "RayRender.AOV_Normal": "__Nworld",
    "RayRender.AOV_Motion": "__motion",
    "RayRender.AOV_Point": "_Pworld",
    "RayRender.AOV_Direct_Diffuse": "__direct_diffuse",
    "RayRender.AOV_Direct_Specular": "__direct_specular",
    "RayRender.AOV_Reflection": "__indirect_specular",
    "RayRender.AOV_Emissive": "__incandescance",
    "RayRender.output_shader_vectors": "1",
    "Project3D.crop": "false",

    # Deep
    "DeepReformat.pbb": "1",

    # Other
    "Dot.note_font_size": "20",
    "Dot.note_font_color": "0x00FF0000",
    "Dot.note_font": "Bitstream Vera Sans",
    "BackdropNode.note_font_size": "72",
    # "Expression.expr3": "a==0?0:1",
}
