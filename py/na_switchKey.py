#na_switchKey.py
#
#@author Nathaniel Anozie
#
##

#modify at own risk

#last updated: 05/08/2014-05/08/2014 -- initial release

#how to use
#select two objects want to switch keys between example left and right hand control.
#na_switchKey()

import maya.cmds as cmds
import sys

def na_switchKey():
    """switch keys between first selected and second selected (keys not set automatically so need to key them)"""
    
    #assumption names of attributes are identical for both
    firstObj = ''
    secondObj = ''
    firstAttr = []
    firstVal = []
    secondAttr = []
    secondVal = []
    
    sel = cmds.ls(sl = True)
    if len(sel) != 2:
        sys.exit("Requires two objects selected!!")
        
    firstObj = sel[0]
    secondObj = sel[1]
    
    #get current keyframe info for both selected before we do the switch
    #ex: {u'translateX': 2.7141762512786562, u'translateY': 0.0, u'translateZ': 0.0}
    firstAttr = cmds.listAttr(firstObj, keyable = True) 
    firstLockedAttr = cmds.listAttr(firstObj, locked = True)
    if firstLockedAttr is not None:
        for locked in firstLockedAttr:
            try:
                firstAttr.remove(locked) #remove locked attributes
            except ValueError:
                pass
    
    firstVal = [ cmds.getAttr( firstObj + "." + at ) for at in firstAttr  ]
    firstData = {}
    attr = ''
    val = 0.0
    for i in xrange( len(firstAttr) ):
        attr = firstAttr[i]
        val = firstVal[i]
        firstData[attr] = val
    #
    secondAttr = cmds.listAttr(secondObj, keyable = True) 
    secondLockedAttr = cmds.listAttr(secondObj, locked = True)
    if secondLockedAttr is not None:
        for locked in secondLockedAttr:
            try:
                secondAttr.remove(locked) #remove locked attributes
            except ValueError:
                pass
    
    secondVal = [ cmds.getAttr( secondObj + "." + at ) for at in secondAttr  ]
    secondData = {}
    attr = ''
    val = 0.0
    for i in xrange( len(secondAttr) ):
        attr = secondAttr[i]
        val = secondVal[i]
        secondData[attr] = val
    
    
    #switch keyframe info
    #print firstData
    #{u'translateX': 2.7141762512786562, u'translateY': 0.0, u'translateZ': 0.0, u'scaleX': 1.0, u'scaleY': 1.0, u'visibility': 1, u'rotateX': 0.0, u'rotateY': 0.0, u'scaleZ': 1.0, u'toe': 0.0}
    for a, v in firstData.items():
        cmds.setAttr( (secondObj+"."+a),v )
    for a, v in secondData.items():
        cmds.setAttr( (firstObj+"."+a),v )
        
    #now pose is set but if you move in timeline we will lose info so set a key to save it    