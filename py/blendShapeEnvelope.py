#01-22-2015 added turn off all targets
#11-24-2014 created

import maya.cmds as cmds

def blendShapeEnvelopeOff():
    """
    turn off envelope of selected
    """
    obj = cmds.ls(selection = True)
    history = cmds.listHistory(obj)
    bsHistory =  cmds.ls(history, type = 'blendShape')
    for bs in bsHistory:
        cmds.setAttr(bs+'.'+'envelope',0.0) #note not changing blend target weights
        
        
def blendShapeTargetOff():
    """
    turn off target weights of selected base mesh
    assumes only one blendshape node input. (could later extend to allow multiple blendnodes on mesh)
 
    usage hotkey:
    python( "import blendShapeEnvelope" );
    python( "blendShapeEnvelope.blendShapeTargetOff()" );
    """
    obj = cmds.ls(selection = True)
    try:
        history = cmds.listHistory(obj)#cmds.listHistory(obj[0])  #IndexError
        bsHistory =  cmds.ls(history, type = 'blendShape')
        blendNode = bsHistory[0] #assuming exists, would change this to allow multiple blendnodes on selected
        
        #get target weights
        blendTargets = cmds.blendShape(blendNode, target = True, query = True)
        #setAttr blendShape3.weight[1] 0;
        for i in range(len(blendTargets)):
            #print ''+blendNode+'.weight['+str(i)+']\n'
            cmds.setAttr(blendNode+'.weight['+str(i)+']',0.0)
        """below was used if want to enforce that scene names of meshes match blend target names
        for target in blendTargets:
            try:
                cmds.setAttr(blendNode+'.'+target,0.0)
            except RuntimeError:
                print 'skipping >> %s ! Make sure it has same name on blendshape node >> %s' %(target,blendNode)
        """
    except TypeError:
        print 'Make sure a mesh is selected that has blendshapes'