##@file na_scaleGeometry.py
#
#Scaling Geometry tools (Tested Maya 2008)
#
#@author Nathaniel Anozie
#
#@defgroup scaleGeometry Scaling Geometry tools
#@{
#Node based scaling of geometry
#
#Example given an attribute use it to figure out scale for geometry
##

import maya.cmds as cmds


##change scale of geometry using a node.  Assumes given from(joint1), fromAttribute(translateX), to(geo1),toAttr(scaleX)
#@note default source attribute translateX, default destination attribute scaleX (error if destination occupied)
#@note ex it:
#make divide node and set option divide
#connect plug joint.translateX into input1X
#enter joint.translateX in input2X
#connect plug dividenode.outputX into geo.scaleX
#
##
def setScaleByTranslation(fromObject = '', fromAttribute='translateX', toObject = '', toAttribute='scaleX'):
    
    backend = toObject+'_'+'scaleNd'
    if cmds.objExists(backend):
        print 'Requires '+backend+'doesnt exist\n'
    else:
        fr =  fromObject+'.'+fromAttribute
        to =  toObject+'.'+toAttribute
        if cmds.objExists(fr) & cmds.objExists(to):
            node = cmds.createNode('multiplyDivide',name=backend)
            cmds.setAttr(node+'.'+'operation',2)
            defaultLength = cmds.getAttr(fr)
            cmds.connectAttr(fr,node+'.'+'input1X')
            cmds.setAttr(node+'.'+'input2X',defaultLength)
            cmds.connectAttr( node+'.'+'outputX',to)
        else:
            print 'Requires Objects To Exist on Scene\n'
     
def setScaleByTranslation_unitTest():
    cube = cmds.polyCube()
    cmds.select(clear=True)
    j1 = cmds.joint(p=[0,0,0])
    j2 = cmds.joint(p=[1,0,0])
    cmds.select(clear=True)
    setScaleByTranslation(fromObject=j2,toObject=cube[0])
