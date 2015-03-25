import maya.cmds as cmds

def putLocalScaleAndTranslateOnSelected():
    """
    put local info onto all but last selected (info: scale and translate)
    """
    
    sel = cmds.ls(selection=True)
    
    argList = sel[:-1]
    lastSelected = sel[-1]
    
    t = cmds.xform(lastSelected,query=True,ws=False,translation=True)
    s = cmds.xform(lastSelected,query=True,os=True,scale=True)
    
    for arg in argList:
        print 'putting info on: %s from: %s\n' %(arg,lastSelected)
        cmds.xform( arg, translation = t, ws = False)
        cmds.xform( arg, scale = s, os = True)