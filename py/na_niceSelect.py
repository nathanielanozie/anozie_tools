#select all history and materials of selected, helpful for exporting in Maya
#author: Nathaniel Anozie (ogbonnawork at gmail dot com)
#
#
#Inspired by Alex Martelli, learning about expand list of lists in python from his online tutorials
#Inspired by Irakli Khakhviashvili, learning about selecting shaders from his online tutorials
#Inspired by Patrick Westerhoff, learning about list uniqueness in python from his online tutorials

#modify at own risk

# updated 08-13-2014 nate ----- initial commit

import maya.cmds as cmds

def na_niceSelect():
    """
    select all history and materials of selected, helpful for exporting in Maya
    """
    result = []
    
    
    sel = cmds.ls(selection = True)
    print "start --- calculating"
    tmpResult = []
    for _arg in sel:
        tmpResult.append( _arg )#important to have everything in lists
        #ex 'openJaw1:new_topology53'
    
        #compute past
        past = []
        past = cmds.listHistory(_arg)
        for _past in past:
            tmpResult.append(_past)  
            #if its a mesh also adds its materials
            shader = []
            shader = cmds.listConnections( _past, type = "shadingEngine")
            if shader is not None:
                tmpResult.append( shader )
    print "done --- calculating"                  
    #
    #concluding 
    #result = [item for sublist in tmpResult for item in sublist]  
    #result = list(set(result)) #remove possible duplicates
    #cmds.select(result, replace = True, ne = True) #selecting results

    #selecting
    cmds.select(clear = True)
    for _result in tmpResult:
        cmds.select(_result, add = True, ne = True) #ne is so can select shaders
        
    result = cmds.ls(selection = True)
    return result
    