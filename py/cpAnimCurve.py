#cpAnimCurve copy selected animation curves onto current scene animator controls
#
#@author Nathaniel Anozie
#
#Inspired by:
#Rik Poggi (learning about python rfind command from online tutorial)
#Peter Mortensen (learning about python string operations from online tutorial)
##

#@note


#modify at own risk

#last updated: 08/08/2014 -- added some notes, working on ability to work with imported animator controls
#last updated: 03/21/2014 -- initial release



import maya.cmds as cmds
import sys


def cpAnimCurve( control_namespace = [] ):
    """requires animation curves selected first, requires namespace parameter if imported or referenced animator controls
    control_namespace -- if you have a namespace on animator controls you need to provide it (no semicolons)
    --controls must not have animation
    --assumes animcurve names have the channel (translateX etc). the channel is the last piece of name after last underscore
    --i dont think this works with referencing im not sure though, i dont think this works with nested imports
    """
    allSelAnimCurve = cmds.ls(sl=True, type = 'animCurve')
    
    curveArg = ""
    curve = ""
    for curveArg in allSelAnimCurve:
        #ex: curve = "r_low_eyeLid_anim_translateZ" or "greatDay:r_low_eyeLid_anim_translateZ"
        curve = curveArg.rstrip('_') #remove trailing underscores for precaution
        curveParts = curve.split("_")
        firstPartOfAnimCurveNameWithNoUnderScore = curveParts[0]
        
        lenCurveParts = len(curveParts) #do error checking, should be at least 2
        if( lenCurveParts < 2):
            sys.exit("Animation Curve should have at least two parts in name separated by _")
        
        channel = ""
        animObject = ""
        channel = curveParts[lenCurveParts-1] #need to verify this is an okay channel, tx,ty etc
        
        #if imported or referenced animation curve do extra stuff
        if not ":" in firstPartOfAnimCurveNameWithNoUnderScore:
            animObject = "_".join(curveParts[:lenCurveParts-1])
        else:
            #if object imported strip out its namespace, and possibly use user provided namespace to get object
            print 'calculating for namespace animator curve --> %s' %curve
            lastIndexSemiColon = firstPartOfAnimCurveNameWithNoUnderScore.rfind(':')
            animObjectNoNameSpace = ""
            animObjectNoNameSpace = firstPartOfAnimCurveNameWithNoUnderScore[lastIndexSemiColon+1:]+"_"+("_".join(curveParts[1:lenCurveParts-1]))
            #use user namespace if we wanted
            if len(control_namespace) == 1:
                animObject = control_namespace[0]+":"+animObjectNoNameSpace
            else:
                animObject = animObjectNoNameSpace
            
        #connect the channel to animObject if it exists
        if( not cmds.objExists(animObject+'.'+channel) ):
            print 'skipping cannot find animator control --> %s channel: %s' %(animObject,channel)
            pass #continue with loop
        else:
            ###for cleaning breaking this channel before trying to connect
            arg = ''
            arg = animObject+'.'+channel #'openJaw1:pCone1.rotateY'
            input = []
            input = cmds.listConnections( arg, plugs = True)
            #animator control is not always connected but if it is then we clean that channel
            if input is not None:
                cmds.disconnectAttr(input[0],arg)
                #cmds.delete( animObject,c = True, at = channel) #does not preserve input in scene
            ######
            
            cmds.connectAttr( curveArg+'.'+'output', animObject+'.'+channel, force=True  ) #add error checking on locked channel

      
        
        