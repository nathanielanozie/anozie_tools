#@author Nathaniel Anozie (ogbonnawork at gmail dot com)
#
#Inspired by:
#Jesse Capper (learning about blendshape painted weights edit and query from his online tutorials)
##

#modify at own risk

#last updated: 09/05/2014 -- working on allowing specify of target id
#last updated: 08/29/2014 -- initial release

import maya.cmds as cmds
import maya.mel as mel
mel.eval( "source \"naMirrorSelectedVerts.mel\";" ) #needed for math
import re

def na_mirrorBSPaintedWeight(defaultArg = 'pCube3', targetID = 0):
    """
    mirror painted blendshape weights from selected, defaults to first blendshape target input.edits selected mesh
    defaultArg -- undeformed mesh, at origin  
    targetID   -- target index, 0 means first target
    """
    sel = []
    sel = cmds.filterExpand( sm=(28,31) ) #get expanded selection no error checking
    
    #assumes mesh has only one blendshape target input
    past = []
    past = cmds.listHistory( sel[0] ) #no error checking
    blend = cmds.ls( past, type = 'blendShape' )
    blendWeightInfo = ''
    #blendWeightInfo = blend[0]+'.'+'inputTarget[0].inputTargetGroup[0]' #used for getting and setting weights
    #blendWeightInfo = blend[0]+'.'+'inputTarget['+str(targetID)+'].inputTargetGroup['+str(targetID)+']' #used for getting and setting weights
    blendWeightInfo = blend[0]+'.'+'inputTarget[0].inputTargetGroup['+str(targetID)+']' #used for getting and setting weights
    #small error info 
    targets = cmds.blendShape( blend[0], query = True, target = True)
    if len(targets) > 0:
        print 'Warning -- Mirroring across target %s' %targets[targetID]
        
    default = defaultArg#'pCube3' #helps mirror math, undeformed mesh
    
    for vtx in sel:
        #vtx = 'pCube1.vtx[5]'
        vtxID = re.search(re.escape('[')+"(.*)"+re.escape(']'),str(vtx) ).group(1)
        vtxID = int(vtxID) #int needed for maya
        #vtxID = 5
        cmds.select(default+'.vtx['+str(vtxID)+']',replace = True)#for selecting area we want to copy over to other side
        #get the mirror side thing
        mvtxTemp = mel.eval("naMirrorSelectedVerts(1,0.01)") #mirror in X, how close is close enough
        
        #get the vertex number
        mvtxID = re.search(re.escape('[')+"(.*)"+re.escape(']'),str(mvtxTemp[0]) ).group(1) #str needed for python
        mvtxID = int(mvtxID) #int needed for maya
        
        #get weight we need, uses id
        wt = cmds.getAttr(  blendWeightInfo+'.'+'targetWeights[%d]' %vtxID  )
        #put weight we want on mirror side, uses id
        cmds.setAttr( blendWeightInfo+'.'+'targetWeights[%d]' %(mvtxID), wt)
