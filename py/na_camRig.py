##@file na_camRig.py  
#makes a simple camera rig that can be used for deep or flat space shots
##

##
#@author Nathaniel Anozie
#ogbonnawork at gmail.com
#Modify at your own risk

##
#@note Inspired by Bruce Block's The Visual Story
#@note Inspired by Jason Schleifer's Animator Friendly Rigging (jasonschleifer dot com)
#@note Inspired by Ryan Trowbridge's online tutorials on playblast (rtrowbridge dot com)
#@note Inspired by Richie Hindle (entrian dot com) online tutorials on zip
##


#HOW TO USE THIS WUUPIE...
"""
import maya.cmds as cmds
import na_camRig as na
reload(na)
cam = na.na_camRig(startFrame = 1, endFrame = 20)
"""

"""
cmds.select(cam)
na.na_camRig_lookThroughSelectedCam()
"""

"""
na.na_camRig_playblast(cams = ['shot_010','shot_030'], path = '/Users/noa/Desktop' )
"""
##

#last updated: 07/26/2013 -- added a playblast function
#last updated: 07/23/2013 -- made a fix for unwanted camera twisting, added some rig organization, added look through ability
#last updated: 07/22/2013 -- made initial release


import maya.cmds as cmds
import maya.mel as mel
#for exiting program if needed
import sys
#for directory stuff
import os

            
def na_camRig(name = 'shot_010', startFrame = 1, endFrame = 30):
    """
    na.na_camRig_playblast(cams = ['shot_010','shot_030'], path = '/Users/noa/Desktop' )
    """
    ###extra attributes on shape
    startAttribute = 'startFrame'
    endAttribute = 'endFrame'
    ###
    
    print('[na_camRig] Begin Making Camera Rig ...\n') 
    
    ##for making camera
    if cmds.objExists(name):
        print('[na_camRig] Error Making Camera Rig ! Check that camera name doesnt exist on scene already \n')
        sys.exit()       
    cam = name
    obj = cmds.camera()
    cmds.rename(obj[0],cam)
    camPar = cmds.group(cam)
    camGrp = cmds.group(camPar)
    
    
    ##for pan and tilt
    #makes a setup via an ik sc two joint chain where 
    #translate of the ikhandle rotates camera
    cmds.select(cl=True)
    
    start = cmds.joint(p=[0,0,0])
    end = cmds.joint(p=[0,0,-1])
    orientTempEnd = cmds.joint(p=[0,0,-2])
    cmds.setAttr(  (orientTempEnd + ".translateZ"), 0.0 )
    cmds.joint(start, edit=True, oj = 'xyz', secondaryAxisOrient = 'yup', ch=True, zso = True)
    print('[na_camRig]'+'Setting Rotation Orders...\n')
    cmds.setAttr( (start+ ".rotateOrder"), 2 )
    cmds.setAttr( (end+".rotateOrder"), 2 )
    aimIk = cmds.ikHandle( sj = start, ee = end, sol = 'ikRPsolver' )
    cmds.setAttr(  (aimIk[0] + ".visibility"), 0 )
    flatSpaceGrp = cmds.group(aimIk[0])
    all_ikGrp_1 = cmds.group(flatSpaceGrp, n = (cam+'_flatSpace_ik_grp') )
    
    print('[na_camRig]'+'Preparing where we parent Camera Node to...\n')
    print('[na_camRig]'+'Warning Missing Offset Camera Rotations...\n')   
    startDup = cmds.duplicate(start)
    #cmds.parent(startDup[0],world=True)
    cmds.pointConstraint(start,startDup[0], mo=True, weight = 1)
    ##orientConstraint -mo -skip x -weight 1 #skipping x
    cmds.orientConstraint(start,startDup[0], skip = 'x', mo=True, weight = 1)
    print('[na_camRig]'+'Parenting Camera Node...\n')
    cmds.parent( camGrp, startDup[0] )
    all_ikGrp_2 = cmds.group(startDup[0], n = (cam+'_flatSpace_jnt_grp') )   
    
    
    ##for dolly,track,boon
    #can translate a piece of the rig (ex: something like start joint in ik sc chain) up and down
    
    #####
    print('[na_camRig] Adding Controls ...\n') 
    mel.eval( "source \"cubeIcon.mel\";" )
    allAnim = mel.eval("cubeIcon(1.0)")
    startGrp = cmds.group(start)
    cmds.parent( startGrp, allAnim )
    cmds.rename(allAnim, (cam+'_deepSpace_anim') )
    all_animGrp_1 = cmds.group((cam+'_deepSpace_anim'), n = (cam+'_deepSpace_anim_grp') )
    #
    mel.eval( "source \"cubeIcon.mel\";" )
    flatSpaceAnim = mel.eval("sphereIcon()")
    #cmds.parent( flatSpaceGrp, flatSpaceAnim )
    cmds.pointConstraint(flatSpaceAnim, flatSpaceGrp, mo=True, weight = 1)
    cmds.rename(flatSpaceAnim, (cam+'_flatSpace_anim') )
    all_animGrp_2 = cmds.group((cam+'_flatSpace_anim'), n = (cam+'_flatSpace_anim_grp') )
    ######
    
    
    ##for general settings
    shapeAr = cmds.pickWalk(cam, direction = 'down')
    shape = shapeAr[0]
    print('[na_camRig] Adding general settings for --> %s ...\n' %shape) 
    cmds.setAttr(  (shape + ".focalLength"), 35.0 ) #35 mm
    fixHeight =  0.446
    cmds.setAttr(  (shape + ".verticalFilmAperture"), fixHeight) #fix height
    cmds.setAttr(  (shape + ".horizontalFilmAperture"), fixHeight*1.85) #make it wider than height

    
    ##for extra attributes
    print('[na_camRig]'+'Warning Missing Randomizing Non Overlapping Frame Range...\n')
    cmds.addAttr(shape, ln = startAttribute, at = 'double', dv = 1.0)
    cmds.setAttr(  (shape+"."+startAttribute), edit = True, keyable = False )
    cmds.setAttr(  (shape+"."+startAttribute), startFrame )
    cmds.addAttr(shape, ln = endAttribute, at = 'double', dv = 1.0)
    cmds.setAttr(  (shape+"."+endAttribute), edit = True, keyable = False )        
    cmds.setAttr(  (shape+"."+endAttribute), endFrame )
    
    ##for rig organization
    print('[na_camRig] Adding rig organization ...\n') 
    toOrganize = [all_animGrp_1, all_animGrp_2, all_ikGrp_1, all_ikGrp_2]
    all_cam_grp = cmds.group(toOrganize, n = (cam+'_grp') )
    print('[na_camRig]'+'Parenting to an overall group...\n') 
    if cmds.objExists( 'all_na_cams' ):
        pass
    else:
        cmds.select( clear=True )
        cmds.group(empty = True, name = 'all_na_cams')
    cmds.parent( all_cam_grp, 'all_na_cams' )    
    
    
    print('[na_camRig] Complete! \n') 
    return cam
        
def na_camRig_lookThroughSelectedCam():
    
    ###extra attributes on shape
    startAttribute = 'startFrame'
    endAttribute = 'endFrame'
    ###
    
    print('[na_camRig_lookThroughSelectedCam] Start ...\n') 
    
    ##for look through
    print('[na_camRig_lookThroughSelectedCam] Looking through camera ... \n') 
    panel = "modelPanel4"  
    sel = cmds.ls(selection=True)
    #if camera is only selection look through it in chosen panel
    if( len(sel) == 1 ):
        if( len(cmds.listRelatives(children = True, type = "camera")) == 1 ):
            mel.eval("lookThroughModelPanel "+sel[0]+" "+panel)  
            
        else:
            print("[na_camRig_lookThroughSelectedCam] Error Check that selection is a Camera made with na_camRig \n")
            sys.exit() #sys.exit(0)    
    else:
        print("[na_camRig_lookThroughSelectedCam] Error Check that selection is a Camera made with na_camRig \n")
        sys.exit() #sys.exit(0)
        
        
    #if camera is only selection set its frame range
    if( len(sel) == 1 ):
        if( len(cmds.listRelatives(children = True, type = "camera")) == 1 ):
            ##for set camera frame range
            print('[na_camRig_lookThroughSelectedCam] Setting Frame Range and Updating time Slider ... \n') 
            shapeAr = cmds.pickWalk(sel[0], direction = 'down')
            shape = shapeAr[0]
            
            if( (cmds.objExists((shape + "." + startAttribute)) == 0) or (cmds.objExists((shape + "." + endAttribute)) == 0) ):
                print("[na_camRig_lookThroughSelectedCam] Cannot find attributes --> %s,%s on %s !!!\n" %(startAttribute,endAttribute,shape))
                sys.exit()
        
            start = cmds.getAttr(  (shape + "." + startAttribute) )
            end = cmds.getAttr(  (shape + "." + endAttribute) )
            cmds.playbackOptions(edit = True, min = start, max = end )
            cmds.currentTime( start )          
        else:
            print("[na_camRig_lookThroughSelectedCam] Error Check that selection is a Camera made with na_camRig \n")
            sys.exit() #sys.exit(0)   

    
    print('[na_camRig_lookThroughSelectedCam] Complete! \n') 
    
    
    


def na_camRig_playblast(cams = ['shot010','shot030'], path = '/Users/noa/Desktop' ):
    
    #make sure all input are camera transforms and are on scene
    objFound = [ cams[x] for x in range(0,len(cams)) if( (cmds.objExists(cams[x]) == 1) and (len(cmds.listRelatives(cams[x],children = True, type = "camera")) == 1) ) ]
    if len(objFound) != len(cams):
        print '[na_camRig_playblast] Error  !!! Check All Input Are Camera Transforms!\n'
        sys.exit() #sys.exit(0)    
        
    #make sure we have a place to write to
    if os.path.isdir(path):
        print '[na_camRig_playblast] Great Found Output Directory >> %s\n' %path
    else:
        print '[na_camRig_playblast] Error No Output Directory !>> %s\n' %path
        sys.exit() #sys.exit(0)

    #make the full path file name, not using usual string adding because of backslashes 
    fileName = [ os.path.join( path , (cams[x]+'_'+str(x+1)) ) for x in range(0,len(cams)) ]
    
    #look through camera and playblast
    for arg,file in zip(cams,fileName):
        print '[na_camRig_playblast] Warning !! Assuming %s, was created by na_camRig\n' %arg    
        cmds.select(arg,replace = True)
        print '[na_camRig_playblast] Warning !! Assumes [na_camRig_lookThroughSelectedCam] this sets frame range and looks through camera and errors out if any problems\n'
        na_camRig_lookThroughSelectedCam()  
        ####standard turn off panel display stuff and other settings could remove or add in here
        #joints
        window = 'modelPanel4' #using perspecitve
        #window = cmds.getPanel(withFocus = True)
        cmds.modelEditor( window, edit = True, joints = 0)
        #cameras
        cmds.modelEditor( window, edit = True, cameras = 0)
        #grid
        cmds.modelEditor( window, edit = True, grid = 0)
        #bg black
        cmds.displayRGBColor("background", 0, 0, 0)
        ####
        print '[na_camRig_playblast] PLAYBLASTING --> camTransform: %s ,fileName: %s \n' %(arg,file)
        cmds.playblast( format = 'movie', viewer = 0, clearCache = 1, showOrnaments = 1, fp = 4, percent = 100, compression = 'none', filename = file)

    ###restore display stuff
    #restore background
    cmds.displayRGBColor("background", 0.688, 0.688, 0.688) 
    ###
