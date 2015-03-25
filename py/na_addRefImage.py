#automatically bring in a reference image into maya so no longer have to do this again ::: ))
#
#@author Nathaniel Anozie
#
##

#@note inspired by Ricardo Viana (mayapy dot wordpress dot com) tutorials on shading groups
#@note inspired by Brian Ewert (xyz2 dot net) tutorials on texutres and materials
#@note inspire by Will Zhou's online tutorials on Open Maya and MImage (python inside maya, googe groups)
#@note inspired by Autodesk (Autodesk.com) online tutorials on MImage api 
#
#
#Modify at your own risk
##

#last updated: 02/15/2014 -- initial release -- working on setting Hardware Texture Resolution via api




import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
#import os


def addRefImage():
    """add reference image in maya from file path at origin with front plane in +z"""

    filePath = cmds.fileDialog()
    #print filePath
    #filePath = '/Users/noa/Desktop/testImage.jpg'
    na_addRefImage(filePath)
    


def na_addRefImage(filePath = "/Users/noa/Desktop/testImage.jpg" ):
    print '[na_addRefImage] Building Reference Image for Modeling ...\n'
    ##get Image size at a path :)))) hurraay
    image = OpenMaya.MImage()
    #image.readFromFile( r"/Users/noa/Desktop/testImage.jpg" )  ## image.getSize( widthPtr, heightPtr), width = scriptUtil.getUint(widthPtr)
    image.readFromFile( filePath )
    
    #we will use these later to point to Maya backend data, and be able to get numbers can actually use in script
    wScriptUtil = OpenMaya.MScriptUtil()
    widthPtr = wScriptUtil.asUintPtr() #these are pointing no where .. they do say we will later be getting numbers though Uint
    
    hScriptUtil = OpenMaya.MScriptUtil()
    heightPtr = hScriptUtil.asUintPtr()
    
    wScriptUtil.setUint(widthPtr, 0)
    hScriptUtil.setUint(heightPtr, 0) #i think this is necessary
    
    image.getSize(widthPtr,heightPtr) #aha now they are pointing to something reason we need an MImage to begin width
    widthInt = wScriptUtil.getUint(widthPtr) #getting an int from a pointer is reason we needed the MScriptUtil
    heightInt = hScriptUtil.getUint(heightPtr)
    
    width = float(widthInt)
    height = float(heightInt)
    
    #print width,height
    #########done getting dimensions for maya plane
    
    
    #make geo for ref image
    #
    w = width/100 #could make 100, 1000 to get it smaller
    h = height/100
    meshRefImage, meshRefImageShape = cmds.polyPlane( width = w, height = h, sx = 1, sy = 1, ax = [0,0,1], cuv = 2, ch = 1)
    ##MATERIAL STUFF
    ##make material and make shading group
    shaderForRefImage = cmds.shadingNode(  'lambert', asShader = True )
    sgForRefImage = cmds.sets(renderable=True,noSurfaceShader=True,empty=True, name = 'myShadingGroup')
    ##assign material
    cmds.connectAttr('%s.outColor' %shaderForRefImage ,'%s.surfaceShader' %sgForRefImage)
    cmds.select(meshRefImage, replace = True)
    cmds.sets( e = True, forceElement = sgForRefImage )
    
    
    #put ref image on ref geo
    #setup
    fileNode = cmds.shadingNode( 'file', asTexture = True) #Create a file texture node
    placeTexture = cmds.shadingNode('place2dTexture', asUtility = True)  #shadingNode -asUtility place2dTexture;
    attr  = ['coverage','translateFrame','rotateFrame','mirrorU','mirrorV','stagger','wrapU','wrapV','repeatUV','offset','rotateUV','noiseUV','vertexUvOne','vertexUvTwo','vertexUvThree','vertexCameraOne']
    
    for at in attr:
        cmds.connectAttr( placeTexture+'.'+at, fileNode+'.'+at )#connectAttr -f place2dTexture1.coverage file1.coverage;
    cmds.connectAttr( placeTexture+'.outUV', fileNode+'.uv' )
    cmds.connectAttr( placeTexture+'.outUvFilterSize', fileNode+'.uvFilterSize' )
    cmds.connectAttr( fileNode+'.outColor', shaderForRefImage+'.color' )
    #actually put ref image on ref geo
    cmds.setAttr(  fileNode+'.fileTextureName', filePath, type = 'string' ) #setAttr -type "string" ( $fileNode + ".fileTextureName" ) $filepath;
    
    ##place image to cover mesh exactly
    maxLength = max(width,height)
    cmds.setAttr(  placeTexture+'.coverageU', round( width/maxLength,2 ) )
    cmds.setAttr(  placeTexture+'.coverageV', round( height/maxLength,2) )
    #setAttr "place2dTexture1.coverageU" 1.41;
    
    """
    #CHECK THIS PART AGAIN
    #make the texture resolution of file node higher
    #tip this makes the resolution attribute showing in Maya , without this this attribute wouldnt exist
    mel.eval("AEhardwareTextureQualityCB \"color transparency ambientColor incandescence normalCamera diffuse translucence\" "+shaderForRefImage+".message")
    ##
    cmds.setAttr(fileNode+'.resolution', 256 ) #setAttr ($texture+".resolution") 256; #32,64
    """
    #change alpha of image
    alpha = 0.75
    cmds.setAttr(shaderForRefImage+'.materialAlphaGain', alpha ) #setAttr "lambert2.materialAlphaGain" 0.7523;
    #show texuture in perspective view
    cmds.modelEditor('modelPanel4', edit = True, displayAppearance = "smoothShaded")
    cmds.modelEditor('modelPanel4',edit = True, displayTextures = 1)
    cmds.select(shaderForRefImage,replace=True)
    print '[na_addRefImage] Complete! ... If needed increase Resolution under Hardware Texturing of: %s ...\n' %shaderForRefImage
    


