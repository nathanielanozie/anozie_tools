#######
#help with building face ui of blendshape based rig
#By
#Nathaniel O. Anozie (ogbonnawork at gmail dot com)
#
#inspired by: Phil Sloggett's online tutorials for learning about set driven keys in python 
#inspired by: Autodesk online documentation examples on promptDialog
#######

#created: 12-26-2014    initial release

import maya.cmds as cmds
import maya.mel as mel

"""usage example
import na_faceIt
reload(na_faceIt)

anim = na_faceIt.getAnim( option = 'both' )  #makes face control

#first select blendshapes in order, ex: left, right, up, dn, base
na_faceIt.setBlendShapeFromAnim( anim, option = 'both' )   #makes blendshape and connections
"""

def getAnim( option = 'both' ):
    """
    build and return a face control string
    assumes tx, ty  usable of face control.
    
    option = 'both'     square
    option = 'up'       half square in +y
    option = 'dn'       half square in -y
    """
    
    #so dont lose current selection
    sel = cmds.ls(selection = True)
    
    ########################
    #icon drawing in +y  -- user could add own custom face contols here as mel commands
    #then tweak the user section to add additional option if wanted
    boxCurveCmd = "curve -d 1 -p -1 0 -1 -p 1 0 -1 -p 1 0 1 -p -1 0 1 -p -1 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4;"
    halfBoxCurveCmdUp = "curve -d 1 -p -1 0 0 -p -1 0 -1 -p 1 0 -1 -p 1 0 0 -p -1 0 0 -k 0 -k 1 -k 2 -k 3 -k 4;"
    halfBoxCurveCmdDn = "curve -d 1 -p -1 0 0 -p 1 0 0 -p 1 0 1 -p -1 0 1 -p -1 0 0 -k 0 -k 1 -k 2 -k 3 -k 4;"
    animCurveCmd = "circle -ch on -o on -nr 0 1 0 -r 0.1;" #used to animate with
    
    ###user may tweak this with additional controls
    txLim = () #face control limits
    tyLim = ()
    bgIcon = ""
    if option == 'both':
        bgIcon = mel.eval(boxCurveCmd) #or halfBoxCurveCmdUp, or halfBoxCurveCmdDn
        txLim = (-1,1)  #(-1,1) says translate x limit from -1 to 1
        tyLim = (-1,1)        
    elif option == 'up':
        bgIcon = mel.eval(halfBoxCurveCmdUp)
        txLim = (-1,1)
        tyLim = (0,1)         
    elif option == 'dn':
        bgIcon = mel.eval(halfBoxCurveCmdDn)
        txLim = (-1,1)
        tyLim = (-1,0)                      
    ###
    animIcon = mel.eval(animCurveCmd)
    
    #does position so facing in positive z
    allIconGrp = cmds.group(bgIcon,animIcon)
    cmds.setAttr( allIconGrp+'.rotateX', 90 )
    cmds.makeIdentity(allIconGrp,apply=True)
    
    #does face control channels cleaning
    [ cmds.setAttr( animIcon[0]+'.'+x, lock = True, keyable = False, channelBox = False) for x in ["tz","rx","ry","rz","sx","sy","sz"] ]
    
    #does face control limits
    cmds.transformLimits(animIcon[0], tx =txLim, etx =(1,1) )
    cmds.transformLimits(animIcon[0], ty =tyLim, ety =(1,1) )
    ########################
    
    #restore selection
    cmds.select(sel, replace = True)
    
    return animIcon[0]


def setBlendShapeFromAnim( faceControl = '', option = 'both' ):
    """
    make face blendshapes connected to animator control given in input
    
    doesnt work if users input meshes are already part of a blendnode
    
    assumes selected sculpted meshes in order:
    left, right, up, dn, base     option = 'both'
    left, right, up,     base     option = 'up'
    left, right, dn,     base     option = 'dn'
    
    faceControl -- name of animator control to use for driving blendshapes
    
    """
    
    help = """check selection!
    assumes selected sculpted meshes in order:
    left, right, up, dn, base     if option = 'both'
    left, right, up,     base     if option = 'up'
    left, right, dn,     base     if option = 'dn'
    """
    
    #get animator control so can make sdks
    anim = faceControl #'locator1'
    
    #blendshapes/base
    up = dn = left = right = default = ''    
    sel = cmds.ls(selection = True)
    if sel is None or len(sel) < 2:
        print help
        return 1
        
    ###get blendshapes from user selection
    if option == 'both':
        try:
            left = sel[0]
            right = sel[1]
            up = sel[2]
            dn = sel[3]
            default = sel[4]
        except IndexError:
            print help
    elif option == 'up':
        try:
            left = sel[0]
            right = sel[1]
            up = sel[2]
            default = sel[3]
        except IndexError:
            print help                
    elif option == 'dn':
        try:
            left = sel[0]
            right = sel[1]
            dn = sel[2]
            default = sel[3]
        except IndexError:
            print help                        
    ###
    
    
    #make blendNode
    blendShapes = []
    [blendShapes.append(x) for x in [up,dn,left,right] if cmds.objExists(x) ]
    blendNode = cmds.blendShape( blendShapes, default) #last is default shape
    
    ####drive blendshapes via set driven key
    driver = anim
    #up
    #setAttr "blendShape1.up" 1;
    #below should skip any blendshapes that dont exist
    if cmds.objExists(up):
        cmds.setDrivenKeyframe( blendNode, at= up, cd= driver+'.translateY', dv=0,v=0 ) #anim default, up off
        cmds.setDrivenKeyframe( blendNode, at= up, cd= driver+'.translateY', dv=1,v=1 ) #anim up +1, up on
    
    #dn
    if cmds.objExists(dn):
        cmds.setDrivenKeyframe( blendNode, at= dn, cd= driver+'.translateY', dv=0,v=0 )  #anim default, dn off
        cmds.setDrivenKeyframe( blendNode, at= dn, cd= driver+'.translateY', dv=-1,v=1 ) #anim up -1, dn on
        
    #left
    if cmds.objExists(left):
        cmds.setDrivenKeyframe( blendNode, at= left, cd= driver+'.translateX', dv=0 , v= 0 )  #anim default, left off
        cmds.setDrivenKeyframe( blendNode, at= left, cd= driver+'.translateX', dv=-1, v= 1 ) #anim left -1, left on
        
    #right
    if cmds.objExists(right):
        cmds.setDrivenKeyframe( blendNode, at= right, cd= driver+'.translateX', dv=0 , v= 0 )  #anim default, right off
        cmds.setDrivenKeyframe( blendNode, at= right, cd= driver+'.translateX', dv=1,  v= 1 ) #anim right +1, right on
        
    ########
    

def getIconText():
    """
    create curve icon from typed text. it gives a dialogue box to type text into
    """
    myText = ''
    #makes UI
    result = cmds.promptDialog(
            title='getIconText',
            message='Enter Text:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
    
    if result == 'OK':
        myText = cmds.promptDialog(query=True, text=True)
        cmds.textCurves( ch = 0, f = "Arial-Regular", text = myText )    
