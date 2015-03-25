##@file na_editJoint.py
#@author Nathaniel Anozie (ogbonnawork at gmail dot com)
#@brief joint editing and drawing tool
#
##

import maya.cmds as cmds

##set local rotations axis to specified rotations on specified objects
#@note default 0.0, 0.0, 0.0
#
##
def setLocalRotationAxisOfObjectList( objects=[], rx=0.0, ry=0.0, rz=0.0 ):
    if all(x is not None for x in objects):  
        map( lambda x: setLocalRotationAxisOfObject(objects[x]+'.rotateAxis',[rx,ry,rz]), range(0,len(objects)))           

##set local rotations axis to specified rotations on specified object
#
##
def setLocalRotationAxisOfObject( obj, rotation ):
    cmds.rotate(rotation[0],rotation[1],rotation[2], obj,objectSpace=True)
    
    
def setLocalRotationAxisOfObjectList_unitTest():
    j1=cmds.joint(p=[0,4,0])
    j2=cmds.joint(p=[0,3,0])
    j3=cmds.joint(p=[0,2,0])
    j4=cmds.joint(p=[0,1,0])
    setLocalRotationAxisOfObjectList( [j1,j2,j3,j4], rx=0.0,ry=90.0,rz=0.0)
