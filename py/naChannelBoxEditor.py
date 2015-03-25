#######
#Help with building Facial Rig User interface
#By
#Nathaniel O. Anozie (ogbonnawork at gmail dot com)
#
#Inspired by Nathan Horne (nathanhorne dot com) -- learning about query channel box from his online tutorials
#
#see also na_faceIt.py (more ui based) ,naFaceBuffer (more backend based)
#######

#created: 01-23-2015    initial release

import maya.cmds as cmds
import maya.mel as mel

def help():
    help ="""
    #set limits of selected channels
    naChannelBoxEditor.setLimit(min = 0, max = 10)
    
    #set value of selected channels to argument
    naChannelBoxEditor.set(0)
    """
    print help

def getSelectedChannel():
    """
    returns list of currently selected channels
    """
    result = []
    channelBox = mel.eval( 'global string $gChannelBoxName; $temp = $gChannelBoxName;'  ) #get maya main channelbox
    result = cmds.channelBox( channelBox, query = True, selectedMainAttributes = True )
    return result
    
def setLimit( min = 0, max = 10 ):
    """
    set limit of selected channels to arguments
    -- defaults [0,10]
    
    usage hotkey:
    python( "import naChannelBoxEditor" );
    python( "naChannelBoxEditor.setLimit(0,10)" );
    """
    sel = cmds.ls( selection = True )
    if sel is not None and len(sel) == 1:
        channel = getSelectedChannel()
        #set limit
        for at in channel:
            cmds.addAttr(  (sel[0]+'.'+at), edit = True, min = min, max = max, dv = 0 )
    
def set( value = 0 ):
    """
    set value of selected channels to argument
    --- defaults 0
    --- assumes user setting to a value in proper range
    
    usage hotkey:
    python( "import naChannelBoxEditor" );
    python( "naChannelBoxEditor.set(0)" );
    """
    sel = cmds.ls( selection = True )
    if sel is not None and len(sel) == 1:
        channel = getSelectedChannel()
        #set limit
        for at in channel:
            cmds.setAttr( (sel[0]+'.'+at), value )
    else:
        print 'Requires an object selected'