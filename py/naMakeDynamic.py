
#12-10-2014     added better chance of unique names in the dynamic drawing tool by using the root joint in name
#12-09-2014     added a attractCurve hook up to animator control
#11-30-2014     working on initial release, figure out why animating control joint doesnt move dynamic joints
#11-27-2014     working on initial release, check why source curve dissapears

import maya.cmds as cmds
import maya.mel as mel

#usage dynamic chain building
"""
import naMakeDynamic
reload(naMakeDynamic)

naMakeDynamic.naMakeDynamic( prefix = 'l_', name = 'shortAnim_01_jnt_' )
"""

#usage anim control attract hookup
"""
import naMakeDynamic
reload(naMakeDynamic)

#select a root that contains hair systems somewhere below it
naMakeDynamic.naHookUpDynamic( animatorControl = 'short_sim_anim', animatorAttribute = 'l_attract' )
"""

def naMakeDynamic( prefix = 'l_', name = 'naControl_jnt_'):
    """
    select root joint then select curve (kind of like making spine ik with custom curve)
    tool duplicates source chain > puts hair dynamics on selected curve >
    puts spine ik on selected joint chain using the dynamic output >
    puts animation control duped chain onto the source hair curve
    (via binding, it skips binding end joint of chain)
    """
    
    #no error checking on input
    sel = cmds.ls(selection = True) #check length 2, and first selected is joint, next selected curve
    if sel is not None and len(sel) == 2:
        curve = sel[1]
        dynRootJnt = sel[0]  #this will become dynamic when done
        
        #do error check here
        
        
        #make dynamic curve
        #needs curve to make dynamic, using hair system
        cmds.select( curve, replace = True)
        mel.eval('MakeCurvesDynamic');
        
        #build spine ik
        #needs start, end, and dynamic curve to use
        startJnt = dynRootJnt
        cmds.select( startJnt, hierarchy = True )
        endJnt = cmds.ls( selection = True, dag = True, leaf = True ) #this selects end of chain
        dynCurve = getDynamicCurveFromSourceCurve( curve = curve )
        if cmds.objExists(dynCurve) == 1:
            ###does the spineik drawing
            cmds.select( startJnt, replace = True )
            cmds.select( endJnt ,add = True )
            cmds.select( dynCurve, add = True )
            cmds.ikHandle( sol = 'ikSplineSolver', ccv = False )
            ###
            
            #make control chain moving source of dynamic curve
            #needs control chain, needs source of dynamic curve
            controlRootJntTemp = cmds.duplicate( dynRootJnt, renameChildren = True, returnRootsOnly = True ) #skipping naming check
            ##naming
            
            cmds.select( controlRootJntTemp, hierarchy = True )
            allDup = cmds.ls( selection = True,type = 'joint' )#by having unique children
            #can ommit dag option and makes renaming easier
            for count in range(0,len(allDup)):
                arg = allDup[count]
                #print arg
                myName = prefix+name+'_'+dynRootJnt+'_'+str(count)#trying to give better chance of unique name
                cmds.rename(arg,myName) #rrenaming happens here no checking unique names
                if count == 0:
                    controlRootJnt = myName #assumes this is the root joint
                count += 1
            
            #controlRootJnt = controlRootJntTemp
            ##
            sourceCurve = curve
            bindJnt = [] #skip end joint of control joints
            #bind joints to curve
            cmds.select( controlRootJnt, hierarchy = True )
            endJnt = cmds.ls( selection = True, dag = True, leaf = True ) #this selects end of chain
            cmds.select( controlRootJnt, hierarchy = True )
            cmds.select( endJnt, tgl = True ) #remove end joint
            bindJnt = cmds.ls(selection = True, dag = True, type = 'joint') #need dag
            #print bindJnt
            #print sourceCurve
            cmds.select(bindJnt, replace = True)
            cmds.select(sourceCurve, add = True)
            
            #TRY uncommenting this bit
            cmds.skinCluster( bindJnt, sourceCurve, toSelectedBones = True )
            #print bindJnt
        else:
            print "Make sure hair has been created.  Couldn't find dynamic Curve."


def getDynamicCurveFromSourceCurve( curve = 'curve1' ):
        
    """
    get dynamic curve transform given src curve transform where a hair system has been hooked up
    assumes hair system already hooked up, no error checking
    """
    
    ### get src curve shape > get follicle transform > get follicle shape > get dyn curve shape
    result = ['']
    curveShape =  cmds.listRelatives( curve, children = True, type = 'nurbsCurve')
    
    curveShapeLocalConnects = cmds.listConnections( curveShape )
    if curveShapeLocalConnects is not None:
        curveShapeAllConnects = cmds.listHistory( curveShapeLocalConnects )   
        cmds.select( curveShapeAllConnects , replace = True) #no checking for none
        follicleShapeAr = cmds.ls( selection = True , type = 'follicle' )# no checking for none
        follicleShapeOutputs = cmds.listConnections(follicleShapeAr[0], source = False, destination = True)
        dynCurveShapeAr = cmds.listRelatives(follicleShapeOutputs,children = True, type = 'nurbsCurve') #no checking none
        #check for length 1
        result = cmds.listRelatives( dynCurveShapeAr[0], parent = True ) #no error checking
       
    return result[0]
    
    
def naHookUpDynamic( animatorControl = '', animatorAttribute = '' ):
    """
    add some dynamics options to an animator control
    add attract -- with a high value can use setdriven keys to alter dynamics of cloth
    needs: selected hierarchy with hair system(s) in it,  get animator control, get animator attr (unlocked,unconnected)
    """
    
    dynamicType = 'hairSystem' #assumes can find this in selection, maya 2008 tested
    dynamicNode =  cmds.ls(selection = True, dag = True, type = dynamicType)
    animCtrl = animatorControl
    animAttr = animatorAttribute
    
    if len(dynamicNode) > 0 and cmds.objExists(animCtrl+'.'+animAttr) == 1: #a little error checking
        dynamicsAttr = 'startCurveAttract' #this is the dynamic attribute were connecting to
        
        for arg in dynamicNode:
            cmds.connectAttr( animCtrl+'.'+animAttr, arg+'.'+dynamicsAttr)
    else:
        print 'Error, make sure selected root with hair system - make sure put animator control and attr exists on scene'
        