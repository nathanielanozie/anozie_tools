##@file na_addToLayer.py Tools to find Maya scene transforms and put them into a display Layer.
#@note ex put all the transforms in group1 into layer1.
#@code import na_addToLayer as na @endcode
#@code na.addToLayer( 'group1', ['transform'], 'layer1' ) @endcode
#
#@author Nathaniel Anozie


import maya.cmds as cmds
import maya.mel as mel


##add all objects in hierarchy of specified type to an existing layer chosen
#
##
def addToLayer( hierarchyParent = "group1", types = [], layer = "layer1" ):
    
    #verify input
    if cmds.objExists(layer) == 0:
        print 'Requires '+layer+' Exist';
        return 0
        
    if cmds.objectType(layer) != 'displayLayer':
        print 'Requires '+layer+' type displayLayer';
        return 0
    
    sel = cmds.ls(sl = True)
    
    if cmds.objExists(hierarchyParent) == 0:
        print 'Requires '+hierarchyParent+' exists';
        return 0
        
    cmds.select(clear=True)
    cmds.select(hierarchyParent, hierarchy=True)
    #done verifying input
    
    
    #put certain scene objects into given layer
    #
    selected = cmds.ls(sl = True)
    #make sure the objects are only of the types we specified in order to add them
    addToLayerObjects = []
    for obj in selected:
        if getIsTypeSupported( obj, types ) == 1:
            addToLayerObjects.append(obj)
            
    #putting them into layer here i thought
    #i had to use mel for it
    #
    tempcmd = "layerEditorAddObjects %s" %layer
    for ob in addToLayerObjects:
        cmds.select(ob,replace = True)
        print ob
        mel.eval(tempcmd)
        
    #restore user scene
    if len(sel) > 0:
        cmds.select(sel,replace = True)
    
        
##
#
##
def addToLayer_unitTest():
    cube = cmds.polyCube()
    layerName = cmds.createDisplayLayer(number=1, empty = True)
    addToLayer( hierarchyParent = cube[0], types = ['transform'], layer = layerName )
    
def addToLayer_unitTest_1():
    cube = cmds.polyCube()
    layerName = cmds.createDisplayLayer(number=1, empty = True)
    addToLayer( hierarchyParent = cube[0], types = ['transform'], layer = 'idontExist' )    
    
    
    
    
    
##get 1 if type of single object input is in specified type list zero otherwise
#
##
def getIsTypeSupported( obj = "", supportedTypes = []):
    result = 0

    
    for i in range( len(supportedTypes) ):
        if cmds.objectType(obj) == supportedTypes[i]: 
            result = 1
            break
            
    return result
    
def getIsTypeSupported_unitTest():
    
    cube = cmds.polyCube()
    print getIsTypeSupported( cube[0], ['transform'] )
    print "\n"
    print getIsTypeSupported( cube[0], ['joint'] )
    print "\n"
  
