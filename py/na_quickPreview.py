#na_quickPreview.py make a movie preview for current Maya window
#
#@author Nathaniel Anozie
#
##



#modify at own risk

#last updated: 02/19/2014-02/20/2014 -- added ui fix, added directory specification option, fixed ui bug finding global variables

import maya.cmds as cmds
import os

def na_quickPreviewPlayblast ( f = '_1', dir = '/Users/noa/Desktop/' ):
    f = cmds.textFieldGrp( "oofileName", text = True, query = True)
    dir = cmds.textFieldGrp( "oodirName", text = True, query = True)
    filePath = dir+f
    #will overwrite file if one is already there
    if os.path.isdir(dir):
        cmds.playblast( format = 'movie', filename = filePath, clearCache = 1, viewer = 0, showOrnaments = 1, fp = 4, percent = 100, compression = 'none')
    else:
        print 'Cannot find output directory!!!'
    cmds.deleteUI("na_quickPreview")
def na_quickPreview():
	#global toField, fromField, winName
	winName = 'na_quickPreview'
	if( cmds.windowPref(winName, exists = True) ):
	    cmds.windowPref(winName, remove = True)
	if( cmds.window(winName, exists = True ) ):
	    cmds.deleteUI(winName)
	cmds.window(winName, t = "playblast window", wh=(100,70),rtf=1)
	cmds.columnLayout(adjustableColumn = True, columnAttach = ["both",5], rowSpacing = 8, columnWidth = 100)
	#fromField = cmds.intFieldGrp( numberOfFields=1, label='From Frame', value1=1 )
	#toField = cmds.intFieldGrp( numberOfFields=1, label='To Frame', value1=1 )	
	cmds.textFieldGrp( "oofileName",label='File', text='' )
	cmds.textFieldGrp( "oodirName",label='Directory', text='/Users/noa/Desktop/' )	
	cmds.button( "previewButton", label='OK', command=("na_quickPreviewPlayblast()") )
	cmds.showWindow( winName )

