##@file cutGeo.py  
#splits geo ex: arm or leg using selected transforms
##

##
#@author Nathaniel Anozie
#ogbonnawork at gmail.com
#

##
#@note Inspired by Jason Schleifer's Animator Friendly Rigging
#@note Inspired by Hamish Mckenzie (macaronikazoo dot com) learning about for zip in python
#@note Inspired by Kyle Mistlin-Rude (kylemr dot blogspot dot com), learning python list comprehension
##

#last updated: 07/17/2013 -- fixed wrong direction splitting bug
#last updated: 07/15/2013 -- fixed cutting last user location bug
#last updated: 07/12/2013 -- removed extra stuff and consolidated short and non repeatable defs

import maya.cmds as cmds
import maya.mel as mel

    
##splits geo ex: arm or leg using selected transforms
#
##
def cutGeo(character = 'pCube1'):
    
    print("[cutGeo] Starting split geo ex: arm or leg using selected transforms ...\n")
    print("[cutGeo] Warning requires order of selected transforms in sequence ...\n")
    print("[cutGeo] Warning Would need to do for arm then for leg separately !!!\n")
    sel = []
    sel = cmds.ls(selection=True)
    
    if( len(sel) < 2 ):
        print("[cutGeo] Warning Does Not Make Cuts With Only One Selected Thing, Need to select two or more transforms !!!\n")
        return 1
    
    try:
        cmds.select(cmds.ls(selection=True),replace=True)
    except TypeError:
        print 'Requires either cvs,locators ... selected so it has positions to cut geometry >>%s'
        return 1
    try:
        cmds.select(character,replace=True)
    except TypeError:
        print 'Requires a piece of geometry as input>>'
        return 1
    
    #so control can be in okay direction, make 1 joint chain using all selected and have it ok orientation
    #
    
    ##
    print("[cutGeo] Computing Cut Positions...\n")
    t = []
    cmds.select(sel,replace=True)
    patches = cmds.ls(sl=True)
    t = [cmds.xform(obj, q=True, ws=True, translation = True )  for obj in patches  ]
    #double the end position so can cut up to last user location
    tLast = t[len(t) - 1]
    t.append( tLast)
    ##
       
    
    ###
    print("[cutGeo] Computing Cut Rotations...\n")
    guideJoints = [] 
    cmds.select(replace=True, clear = True)
    map( lambda x: guideJoints.append( cmds.joint(p=t[x]) ), range(0,len(t)))
    cmds.select(guideJoints[0],replace=True)
    print "[makeGuideJoint] Warning Using Default Orientation xzy \n"
    mel.eval('joint -e -oj xzy -secondaryAxisOrient yup -ch -zso;') 

       
    

    splitR = [[]] #will hold all cut of geo rotation
    splitT= [[]] #will hold all cut of geo translation
    
    print('Beginning loop for cut points <<<\n')
    for i in range(0,len(guideJoints)-1):
        jnt = guideJoints[i] #looking at one joint
        #saving data for splitting of geo
        splitRot = cmds.xform(jnt,query=True,ws=True,rotation=True)
        rx = 0
        ry = 90
        rz = splitRot[2]
       
        print('Joint %s --> %d %d %d\n' %(jnt,rx,ry,rz) )
        splitRotate = [rx,ry,rz]
        splitTranslate = cmds.xform(jnt,query=True,ws=True,translation=True)         
        splitR.append(splitRotate)
        splitT.append(splitTranslate)   
            
     
    #make all geo cuts at once so dont have trouble finding separated geos
    #
    splitR = splitR[1:] #need everything but first empty thing
    splitT = splitT[1:]
    splitGeo(character,translation = splitT,rotation = splitR )
    ##
    
    #possibly remove guide joints
    print "[cutGeo] Warning Assumes can easily clean up cut setup joints\n"
    if len(guideJoints) > 0:
        mel.eval('delete '+guideJoints[0])
        #map( lambda x: mel.eval('delete '+guideJoints[x]), range(0,len(guideJoints)))
        
            
       
def cutGeo_unitTest():  
    print "[cutGeo_unitTest] Not Implemented"
    
        
        
##cut a polygon geo at given points. the rotation helps determine normals for cuts try a couple.
#
#@param character poly
#@param world translation for cut
#@param world euler rotation for cut
#
#
##
def splitGeo(character='pCube1',translation = [[0,0,0]],rotation = [[0,90,0]]):
    for t, r in zip(translation,rotation):
        print '[splitGeo]  Warning Using Rotation %d,%d,%d\n' %(r[0],r[1],r[2])
        cmds.polyCut(character,ch=1,pc=t,ro=r)
        
        
    cmds.select(character, replace=True)
    cmds.pickWalk(direction='down')
    print("[splitGeo] Only Supporting Mesh\n")
    characterShape = cmds.ls(selection=True, type = "mesh") #check size is 1,or nurbsSurface
    
    #finish with all cuts --change offsets to 0 and change extract faces to true
    pCutConnections = cmds.listConnections(characterShape,type = 'polyCut')
    
    pCut=[]
    if pCutConnections is not None:
        pCut = pCutConnections
    else:
        print "<<Requires PolyCuts To Separate Geo>>"
        return 1
        
    if len(pCut) > 0:
        pCut = list(set(pCut)) #remove duplicates python 2.5 >
        
        for obj in pCut:
            cmds.setAttr( obj+'.extractOffsetX', 0.0 )
            cmds.setAttr( obj+'.extractOffsetY', 0.0 )
            cmds.setAttr( obj+'.extractOffsetZ', 0.0 )
            cmds.setAttr( obj+'.extractFaces', 1 )

        #separate the shape ex:  polySeparate -ch 1 pCubeShape2;    
        cmds.polySeparate( characterShape, ch = 1)
            
def splitGeo_unitTest(): 
    character = cmds.polyCube(w=5)
    splitGeo(character,tSplit = [0,0,0],rSplit = [0,90,0] )
    

    
    
    
    
    
  
    
    
