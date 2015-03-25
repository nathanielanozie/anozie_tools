#11-30      working on fix to sort by world position of locators along an axis to prevent for weird results depending on where parent is
#last updated   11-28-2014      working on initial release

#inspired by Matt Gilson (github dot com/mgilson)  learning about tuples from online tutorials
#inspired by Stephen (stackoverflow dot com how-to-sort-list-tuple-of-lists-tuples) learning about sorting tuples from online tutorial
#inspired by Abhijit Rao learing about list reverse in python

import maya.cmds as cmds

#from getOrderByTranslate import *
#cmds.select( getOrderByTranslate(attr = 'translateX'), replace = True)
#could use this ordering to draw curves, joints, name stuff, etc

def getOrderByTranslate( attr = 'translateX', reverseResult = False ):
    """
    This could be helpful for quickly naming a whole bunch of locators/and or 
    joints in a group. It automatically figures out chain sequence of nonchain things. 

    assumes user selected group with things we want ordered
    attr: is the axis that is used to figure out order of elements in world space
    reverseResult: is boolean to say if result should be returned in reverse order
    """
    
    grp = ''
    result = []
    sel = cmds.ls(selection = True)
    if sel is not None and len(sel) == 1:
        grp = sel[0]    #no checking on types and length
        allTransform = cmds.listRelatives( grp, children = True, fullPath = True )
        
        #save out grp rotation
        #startRot = []
        #startRot = cmds.xform( grp, query = True, ws = True, rotation = True)
        
        #zero out grp rot
        #cmds.xform( grp, rotation = [0,0,0], ws = True )
        
        #save out translates to tuple
        info = [] 
        for arg in allTransform:
            #t = cmds.getAttr( arg+'.'+attr ) #local space
            tAll = cmds.xform( arg, query = True, ws = True, translation = True)
            if attr == 'translateX':
                t = tAll[0]
            elif attr == 'translateY':
                t= tAll[1]
            else:
                t = tAll[2]  #default is Z
            
            info.append( (arg, t) ) #save tuple
        
        #compute order
        info.sort(key = lambda x: x[1]) #sort by second element of tuple
        
        #restore grp rotation
        #cmds.xform( grp, rotation = startRot, ws = True )
        
        #return list of all locators in grp but ordered
        result = [ e[0] for e in info ]
        
        if reverseResult:
            result = list(reversed(result)) #reverse result if user asks for it, also L[::-1]
            
        cmds.select(result,replace = True)
    else:
        print 'Error, make sure to select group with things we want ordered'
        
    return result
