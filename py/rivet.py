##@file rivet.py
#
#ConnectAttr commands with pointOnSurfaceNode (Tested Maya 2008)
#
#@author Nathaniel Anozie
#
#@note inspired by Matt Estela (tokeru dot com) for learning about node based surface constraint techniques
#
#@defgroup rivet Surface Constraint tools
#@{
#ex: setUVToSurfaceInfo and setPositionToSurfaceInfo
#LocatorRivet -- transformName
##

import maya.cmds as cmds
from sceneInfo import getExist,getDontExist,getType

##support communicate with a pointOnSurfaceInfo node requires a locator name
#
##  
class LocatorRivet():
    def __init__(self, locator=''):
        self.__locator = locator

        
    ##set the u and v parameter on locator to lead surface info node, its supports changing the locator u,v parameter names
    #
    ##    
    def setUVToSurfaceInfo(self,infoNode='',paramU='parameterU',paramV='parameterV'):
        #parameterU and parameterV must exist on locator
        #surfaceInfo must be a Maya pointOnSurface info node     
        name = self.__locator
        plugU = self.__locator+'.'+paramU
        plugV = self.__locator+'.'+paramV
        statusExist = getExist( [[name,plugU,plugV]] )
        statusType = getType( [[infoNode]],'pointOnSurfaceInfo' )
        
        if statusExist & statusType:
            statusAttributeU = cmds.listConnections(infoNode+'.parameterU',source=True,destination=False)
            statusAttributeV = cmds.listConnections(infoNode+'.parameterV',source=True,destination=False)
            if (statusAttributeU is None) & (statusAttributeV is None):
                cmds.connectAttr(plugU,infoNode+'.parameterU')  
                cmds.connectAttr(plugV,infoNode+'.parameterV')
            else:
                print 'Requires no inputs to destination'
        else:
            print 'Requires pointOnSurfaceInfo, and valid u and v parameters on locator\n'

    ##set the tx,ty,and tz parameters on surface info node to lead to locator
    #
    ##  
    def setPositionToSurfaceInfo(self,infoNode=''):
        print 'my name is '+self.__locator
        name = self.__locator
        plugX = self.__locator+'.'+'translateX'
        plugY = self.__locator+'.'+'translateY'
        plugZ = self.__locator+'.'+'translateZ'
        statusExist = getExist( [[name,plugX,plugY,plugZ]] )
        statusType = getType( [[infoNode]],'pointOnSurfaceInfo' )
        
        if statusExist & statusType:
            statusAttributeX = cmds.listConnections(plugX,source=True,destination=False)
            statusAttributeY = cmds.listConnections(plugY,source=True,destination=False)
            statusAttributeZ = cmds.listConnections(plugZ,source=True,destination=False)            
            if (statusAttributeX is None) & (statusAttributeY is None) & (statusAttributeZ is None):
                cmds.connectAttr(infoNode+'.positionX',plugX)  
                cmds.connectAttr(infoNode+'.positionY',plugY) 
                cmds.connectAttr(infoNode+'.positionZ',plugZ) 
            else:
                print 'Requires no inputs to destination'
        else:
            print 'Requires pointOnSurfaceInfo, and valid u and v parameters on locator\n'

            
###add two float attributes to locator
#
##
def addUVAttributeToLocator(name='',paramU='parameterU',paramV='parameterV'):
    statusExist = getExist( [[name]] )
    statusDontExist = getDontExist( [[ (name+'.'+paramU), (name+'.'+paramV)]] )   
    
    if statusExist & statusDontExist:
        cmds.addAttr(name,at = 'float', keyable=True,ln = paramU)
        cmds.addAttr(name,at = 'float', keyable=True,ln = paramV)
    else:
        print 'Requires no attribute of same name exist'
        
def addUVAttributeToLocator_unitTest():        
    locator1 = cmds.spaceLocator()
    name = locator1[0]
    addUVAttributeToLocator(name)
    
def setUVToSurfaceInfo_unitTest():
    locator1 = cmds.spaceLocator()
    name = locator1[0]
    cmds.addAttr(name,at = 'float', keyable=True,ln = 'parameterU')
    cmds.addAttr(name,at = 'float', keyable=True,ln = 'parameterV')
    loc = LocatorRivet(locator = name)
    infoName = name+'_'+'infoNd'
    info = cmds.createNode('pointOnSurfaceInfo',name=infoName)
    loc.setUVToSurfaceInfo(info)
    
def setPositionToSurfaceInfo_unitTest():
    locator1 = cmds.spaceLocator()
    name = locator1[0]
    cmds.addAttr(name,at = 'float', keyable=True,ln = 'parameterU')
    cmds.addAttr(name,at = 'float', keyable=True,ln = 'parameterV')
    loc = LocatorRivet(locator = name)
    infoName = name+'_'+'infoNd'
    info = cmds.createNode('pointOnSurfaceInfo',name=infoName)
    loc.setPositionToSurfaceInfo(info)
    
  
