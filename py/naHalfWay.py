##
# naHalfWay.py
#
#by
#
#Nathaniel O. Anozie (nathananozie dot blogspot dot com)
#ogbonnawork at gmail dot com
#
#
##

#11-30-2014     initial release

import maya.cmds as cmds

"""
#Put file in script path > select things want to make a halfway in between
import naHalfWay
reload(naHalfWay)

naHalfWay.naHalfWay()
"""

def naHalfWay():
    """
    make half way locator in between 2 or more selected components or transforms
    (doesnt support selecting both components and transforms at same time)
    
    This is useful for things like equal spacing in rigging, centering a pivot for cloth simulation, 
    adding new inbetween vertex in modeling etc
    """
    
    result = []
    selOrig = cmds.ls(selection = True, dag = True,type = 'transform')
    sel = []
    sel = cmds.filterExpand( sm=(28,31,46) )#more than 2 vertices required
    #if cant find component it assumes ok to use as transform
    if sel is None and len(selOrig) >= 2:
        sel = selOrig
    
    if sel is not None and len(sel) >= 2:   
        locatorsMade = []
        
        #does making things we use for figuring out math
        for arg in sel:
            pos1 = cmds.xform(arg, q=True, ws=True, translation = True )
            locator1 = cmds.spaceLocator()
            cmds.xform(locator1, ws=True, translation = [pos1[0],pos1[1],pos1[2]])
            locatorsMade.append(locator1)
            
        result = cmds.spaceLocator() #default naming
        #print locatorsMade
        
        #does the spacing
        for driver in locatorsMade:
            cmds.pointConstraint(driver,result, mo=False, weight = 1)
        
        #cleanup
        for driver in locatorsMade:    
            cmds.delete(driver)
    else:
        print 'Requires 2 or more selected components or transforms'
    
    return result
      