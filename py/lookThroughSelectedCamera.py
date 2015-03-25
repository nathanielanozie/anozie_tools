##@file lookThroughSelectedCamera.py Camera Syntax
#@author Nathaniel Anozie

import maya.cmds as cmds
import maya.mel as mel


##look through selected camera
#
#@pre camera selected on scene
#
#
def lookThroughSelectedCamera():
    panel = "modelPanel4"  
    sel = cmds.ls(selection=True)

    #if camera is only selection look through it in chosen panel
    if( len(sel) == 1 ):
        if( len(cmds.listRelatives(children = True, type = "camera")) == 1 ):
            mel.eval("lookThroughModelPanel "+sel[0]+" "+panel)        
    
    
