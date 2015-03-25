##@file na_animatorControl.py  Set Animator Control To Fit Character
#@note draw a circular animator curve example
#@code circleDraw([1.23,0,0]) @endcode
#@note rotate cv example
#@code rotateCV( arg = 'nurbsCircle1',rotateXYZ=[0.0,0.0,90.0] ) @endcode
#@author Nathaniel Anozie
#

import maya.cmds as cmds
import maya.mel as mel

from na_assertGeneral import*
from na_dataType import*

##make a circle at specified position
#@param centerPosition [float]  worldspace center to draw circle
#@note uses maya defaults on rotation of circle, history etc
#@result name of circle (string) 
def circleDraw( centerPosition = [0.0,0.0,0.0] ):
    sel = []
    sel = cmds.ls(selection = True)
    name = cmds.circle(center=centerPosition)
    cmds.select(sel,replace=True)    
    return str(name[0])
    
def circleDraw_unitTest():
    print circleDraw([1.23,0,0])
    
##rotate all cv to specified euler angle
#@param arg [string] transform
#@note default obect center pivot
#@bug not checking whether type is in fact a curve
def rotateCV( arg = [] ,rotateXYZ = [90.0,0.0,0.0] ):
    
    assertObjectExist(objects = arg)
    assertSizeEqualArg(objects = arg, lenRequired = 1)
    
    sel = []
    sel = cmds.ls(selection = True)
    
    #select curve and rotate its cvs
    objectList = getArgStringAsList(arg)
    assertSizeEqualArg(objects = objectList, lenRequired = 1)
    
    cmds.select(objectList[0], replace=True)
    mel.eval( 'selectCurveCV("all")')
    cv = []
    cv = cmds.ls(selection = True)
    if len(cv) > 0:
        cmds.select(cv,replace=True)
        cmds.rotate(rotateXYZ[0], rotateXYZ[1], rotateXYZ[2],relative=True,euler=True,objectCenterPivot=True)      
    
    if(len(sel) > 0):
        cmds.select(sel,replace=True)
        
        
def rotateCV_unitTest():
    name = cmds.circle(center=[0,0,0])
    rotateCV( arg = name[0] )
    name = cmds.circle(center=[0,0,0])
    rotateCV( arg = name[0],rotateXYZ=[0.0,0.0,90.0] )
