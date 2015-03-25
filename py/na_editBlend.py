##@file na_editBlend.py  
#make realtime edits of right blendshape by editing left blendshape. 
#@note if left blendshape is other x axis change mirrorAx to 'Y' or 'Z' it should still work
##

##
#@author Nathaniel Anozie
#ogbonnawork at gmail.com
#Modify at your own risk

#how to use this sucker
"""
import na_editBlend
import maya.cmds as cmds
reload(na_editBlend)
from na_editBlend import Face

#finalMeshArg = 'pCube1'
defaultMeshArg = 'pCube2'
rightBlendArg = 'pCube3'
leftBlendArg = 'pCube4'

sel = [leftBlendArg,rightBlendArg,defaultMeshArg]
cmds.select(sel,replace=True)
smoothFace = Face()
smoothFace.startSculpting()

smoothFace.stopSculpting()
"""
#

#last updated: 08/10/2013 -- working on cleaning
#last updated: 08/09/2013 -- working on cleaning
#last updated: 08/09/2013 -- initial release
#last updated: 08/08/2013 -- working on initial release
#last updated: 08/07/2013 -- working on initial release
#last updated: 08/02/2013 -- working on initial release

import maya.cmds as cmds
import maya.mel as mel
import sys
from pprint import pprint


class Face(object):

    def __init__(self, mirrorAx = 'X'):
        
        sel = cmds.ls(selection=True)
        if len(sel) == 3:
            leftBlendArg = sel[0]
            rightBlendArg = sel[1]
            defaultMeshArg = sel[2]
        else:
            cmds.error('Select Left Mesh, Right Mesh, then Default Mesh!!!\n')
            sys.exit()
        
        self.mirrorAx = mirrorAx #could be Y or Z
        #self.finalMeshArg = finalMeshArg #cmds.duplicate(finalMeshArg)
        self.defaultMeshArg = defaultMeshArg
        self.rightBlendArg = rightBlendArg
        self.rightBlendNodeName = 'right_blend' #should error out if a blend node is name this already
        self.leftBlendArg = leftBlendArg

        #duplicate defaultMesh twice making intermediate1, and scaleMinusMesh
        intermediate1Ar = cmds.duplicate(defaultMeshArg)
        intermediate1 = intermediate1Ar[0]
        scaleMinusMeshAr = cmds.duplicate(defaultMeshArg)
        scaleMinusMesh = scaleMinusMeshAr[0]
        dupRightBlendAr = cmds.duplicate(rightBlendArg)
        dupRightBlend = dupRightBlendAr[0]
        ##
        
        self.intermediate1 = intermediate1
        self.scaleMinusMesh = scaleMinusMesh
        self.dupRightBlend = dupRightBlend
        
        #brainstorming how to clean up all the mess this makes and still have clean meshes that have edits
        print('it might make sense to copy meshes from scene. and have something to replace a blendshape with a different mesh. replacement should preserve blendshape use of animator controls ex: expressions, connections ... \n')
        
    def startSculpting(self):
        print('[startSculpting] Begin Presetup for sculpting on blendshape ...\n') 

        ##
        mirrorAxis = self.mirrorAx 
        #finalMesh = self.finalMeshArg 
        defaultMesh = self.defaultMeshArg
        rightBlend = self.rightBlendArg
        rightBlendNodeName = self.rightBlendNodeName
        leftBlend = self.leftBlendArg
        intermediate1 = self.intermediate1
        scaleMinusMesh = self.scaleMinusMesh
        dupRightBlend = self.dupRightBlend
        ##
        #pprint( [defaultMesh,rightBlend,leftBlend,intermediate1] )
        
        #move to rightBlend, intermediate1 and scaleMinusMesh (world space)
        cntAr1 = cmds.parentConstraint(rightBlend,intermediate1, mo = 0)
        cmds.delete( cntAr1[0] )
        cntAr2 = cmds.parentConstraint(rightBlend,scaleMinusMesh, mo = 0)
        cmds.delete( cntAr2[0] )
        cntAr3 = cmds.parentConstraint(rightBlend,dupRightBlend, mo = 0)
        cmds.delete( cntAr3[0] )
        
        #set scaleX -1 scaleMinusMesh
        cmds.setAttr(  (scaleMinusMesh + ".scale"+mirrorAxis), -1.0 )
        
        #make leftBlend -> intermediate1 (via intermediate1_blend)
        cmds.blendShape(leftBlend,intermediate1,n = 'intermediate1_blend')
        
        #make intermediate1 -> scaleMinusMesh (via scaleMinusMesh_blend)
        cmds.blendShape(intermediate1,scaleMinusMesh,n = 'scaleMinusMesh_blend')
        #Try moving scale Here ????
        
        #put intermediate1 blendWeight at 1 (via intermediate1_blend)
        cmds.setAttr( 'intermediate1_blend.w[0]', 1.0 )
        
        #put scaleMinusMesh blendWeight at 1 (via scaleMinusMesh_blend)
        cmds.setAttr( 'scaleMinusMesh_blend.w[0]', 1.0 )
        
        ##This should make right blendshape be edited in realtime
        ####
        ##can connect scale - mesh directly to right blend need a mesh in between
        #make scaleMinusMesh -> dupRightBlend via wrap, because vertex order different
        #make sure duplicate right blendshape mesh looks like the right blendshape
        print '[startSculpting] Making scaled mesh %s -- drive duplicate of right blendshape %s \n' %(scaleMinusMesh,dupRightBlend)
        cmds.select(dupRightBlend,replace = True)
        cmds.select(scaleMinusMesh,add = True)
        mel.eval("CreateWrap")
        #cmds.deformer( scaleMinusMesh, type = 'wrap' ) #LOOK UP THE CORRECT WRAP DEFORMER COMMAND
        ####
        
        #make dupRightBlend -> rightBlend (via rightBlend_blend), put rightBlend blendWeight at 1 (via rightBlend_blend)
        cmds.blendShape(dupRightBlend,rightBlend,n = rightBlendNodeName)
        cmds.setAttr( 'right_blend.w[0]', 1.0 )
        
        #so can start editing left blend hide some things, should only see finalMesh and leftBlend, finalMesh should get updated on both sides in realtime
        hideAr = [rightBlend,defaultMesh,intermediate1,scaleMinusMesh,dupRightBlend]
        [ cmds.setAttr( (x+'.visibility'),0 ) for x in hideAr ]
        
    def stopSculpting(self):
        #delete wraps, blendshapes, extra meshes, okay to delete history on meshes
        print('[stopSculpting] Begin Finishing ...\n') 
        
        """
        self.intermediate1 = intermediate1
        self.scaleMinusMesh = scaleMinusmesh
        self.dupRightBlend = dupRightBlend
        self.rightBlendNodeName = 'right_blend'
        """
        
        #clean up right blendshape not messing with its outputs
        rightBlendShapeAr = cmds.pickWalk(self.rightBlendArg, direction = 'down')
        rightBlendShape = rightBlendShapeAr[0]
        cmds.disconnectAttr( self.rightBlendNodeName+'.'+'outputGeometry[0]', rightBlendShape+'.'+'inMesh'  )
        
        #remove extras
        cmds.delete(self.rightBlendNodeName)
        cmds.delete(self.intermediate1)
        cmds.delete(self.scaleMinusMesh)
        cmds.delete(self.dupRightBlend)
        

