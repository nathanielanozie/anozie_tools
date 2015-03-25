#######
#Help with previewing animation
#ex: phonemes of Facial Rig
#By
#Nathaniel O. Anozie (ogbonnawork at gmail dot com)
#
#Inspired by
#
#see also 
#######

#01-29                  added frame range preview
#created: 01-29-2015    initial release



import maya.cmds as cmds

#TODO
#setIdenticalFrames     #put identical frames at current values on all things selected 
#-- uses logical or -- any frame on anything selected means a frame needs to be on all things selected
#
#find keyframe with any frame on anything selected
#put keyframe on everything selected on every frame (not specifying value so using defaults)

def help():
    help = """
    #puts keyframe at value on all keyable attributes of selected
    naAutoAnimate.keyableKeyAtValueByFrameRange(keyframes = range(0,100,5), value = 10)
    """
    print help
        

def keyableKeyAtValueByFrameRange( keyframes = [], value = 10 ):
    """
    set all keyable keys of selected, and for given framerange, to value
    
    #user needs to do the frame holds
    #user needs to specify a list range of where to set keyframes
    #users frame range list length should be at least as big as keyable attributes
    #should support blendshape nodes too
    """
    
    sel = cmds.ls(sl=True)
    
    if sel is not None and len(sel) > 0:
        obj = sel[0]
        #
        if cmds.objectType(obj) == 'blendShape':
            blendTargets = cmds.blendShape( obj, target = True, query = True)
            #cmds.setAttr( (myNode+'.weight['+str(n)+']'), 1.0 )#default 0-1 range
            attr = ['weight['+str(x)+']' for x in range(0,len(blendTargets)) ]
        else:
            attr = cmds.listAttr( obj,  keyable= True ) #key all keyable attribute
            
        #keyframes = range(0,50,5) #where to set keyframes
        #keyframes = [5, 10, 15, 20, 25, 30, 35, 40, 45] #minimum is frame 1
        myValue = value #10 #key this value on every frame
        
        #set keyframe at 0 on frame zero
        #set keyframe at value on every valid place
        #set keyframe at 0 on the other valid places  
        ##one frame prior
        keyframesValue = keyframes
        #keyframeZero = [ x-1 for x in keyframes ]
        #keyframeZero.append(0) #[4, 9, 14, 19, 24, 29, 34, 39, 44, 0]
        
        if len(keyframes) > len(attr):
            #key all frames at frame zero to zero
            for m in range(0,len(attr)):
                at = attr[m]
                cmds.setKeyframe( obj+'.'+at, time = 0, value = 0 ) 
                cmds.keyTangent( obj+'.'+at, inAngle = 0, time = (0,0 ), edit = True ) 
                cmds.keyTangent( obj+'.'+at, outAngle = 0, time = (0,0 ), edit = True ) 
                cmds.keyTangent( obj+'.'+at, ott = 'step', time = (0,0 ), edit = True ) #check step
                        
            #keys at my values
            for i in range(0,len(attr)):
                at = attr[i]
                cmds.setKeyframe( obj+'.'+at, time = keyframesValue[i], value = myValue ) 
                cmds.keyTangent( obj+'.'+at, inAngle = 0, time = (keyframesValue[i],keyframesValue[i] ), edit = True ) 
                cmds.keyTangent( obj+'.'+at, outAngle = 0, time = (keyframesValue[i],keyframesValue[i] ), edit = True ) 
                cmds.keyTangent( obj+'.'+at, ott = 'step', time = (keyframesValue[i],keyframesValue[i] ), edit = True ) #check step
                
                #key all other frames at zero (might want to optimize can do less than since going in order)
                for j in range(0,len(attr)):
                    if j != i:
                        at = attr[j]
                        cmds.setKeyframe( obj+'.'+at, time = keyframesValue[i], value = 0 ) 
                        cmds.keyTangent( obj+'.'+at, inAngle = 0, time = (keyframesValue[i],keyframesValue[i] ), edit = True ) 
                        cmds.keyTangent( obj+'.'+at, outAngle = 0, time = (keyframesValue[i],keyframesValue[i] ), edit = True ) 
                        cmds.keyTangent( obj+'.'+at, ott = 'step', time = (keyframesValue[i],keyframesValue[i] ), edit = True ) #check step
        else:
            print 'skipping -- try increasing length of keyframe range'        
    else:
        print 'please select a transform with keyable attributes'