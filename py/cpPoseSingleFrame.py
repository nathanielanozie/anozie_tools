#cpPoseSingleFrame.py copy pose from one frame to another
#
#@author Nathaniel Anozie
#
##

#@note inspired by James Park (arcsecond dot net) learning about making python Maya ui from online tutorials



#modify at own risk

#last updated: 02/19/2014 -- adding better integration with Maya, fixed ui bug finding global variables
#last updated: 02/18/2014 -- initial release


import maya.cmds as cmds




def cpPoseSingleFrame():
	#global toField, fromField, winName
	winName = 'cpPoseSingleFrame'
	if( cmds.windowPref(winName, exists = True) ):
	    cmds.windowPref(winName, remove = True)
	if( cmds.window(winName, exists = True ) ):
	    cmds.deleteUI(winName)
	cmds.window(winName, t = "Copy pose on single fr", wh=(100,70),rtf=1)
	cmds.columnLayout(adjustableColumn = True, columnAttach = ["both",5], rowSpacing = 8, columnWidth = 100)
	#fromField = cmds.intFieldGrp( numberOfFields=1, label='From Frame', value1=1 )
	#toField = cmds.intFieldGrp( numberOfFields=1, label='To Frame', value1=1 )	
	cmds.intFieldGrp( "fromField", numberOfFields=1, label='From Frame', value1=1 )
	cmds.intFieldGrp( "toField", numberOfFields=1, label='To Frame', value1=1 )	
	cmds.button( "poseButton", label='Copy Pose', command=("cpPoseCollectAndCall()") )
	cmds.showWindow( winName )

	
#global toField, fromField, winName

def cpPoseCollectAndCall():
	#global toField, fromField, winName
	toArg = cmds.intFieldGrp( "toField", value = True, query = True)
	fromArg = cmds.intFieldGrp( "fromField", value = True, query = True)
	anim = cmds.ls(selection = True)
	posePaste( fromFrame = fromArg[0] ,toFrame = toArg[0], anim = anim )

	
#copies animation between two frames -- copying from into to	
def posePaste(fromFrame = 35,toFrame = 21, anim = []):
	#fromFrame = 35
	fromFrameRange = ( fromFrame, (fromFrame+1) )
	#toFrame = 21
	toFrameRange = (toFrame,toFrame)

	cmds.copyKey( anim, time = fromFrameRange, float = fromFrameRange, option = 'keys', hierarchy = 'none',
	controlPoints = 0, shape = 1)

	cmds.pasteKey( anim, time = toFrameRange, float = toFrameRange, option = 'merge', copies = 1, connect = 0,
	timeOffset = 0, floatOffset = 0, valueOffset=0 )

	

