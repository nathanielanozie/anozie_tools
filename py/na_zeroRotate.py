#author: Nathaniel Anozie (ogbonnawork at gmail dot com)
#
#modify at own risk

# updated 08-18-2014 nate ----- initial commit

import maya.cmds as cmds

def na_zeroRotate():
    """
    set rxyz to 0 for all selected, assumes channels are unlocked
    """
    sel = []
    sel = cmds.ls(sl=True)

    #does what it can
    for arg in sel:
        try:
            cmds.setAttr( (arg+".rotateX"),0)
        except RuntimeError:
            pass
        try:
            cmds.setAttr( (arg+".rotateY"),0)
        except RuntimeError:
            pass
        try:
            cmds.setAttr( (arg+".rotateZ"),0)
        except RuntimeError:
            pass