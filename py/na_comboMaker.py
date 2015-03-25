##@file na_comboMaker.py
##given a default,posed and sculpted mesh make a sculpted + posed mesh. this is so we can fix combo shape parts more quickly

#last updated -- nate -- 07/15/2014 -- working on initial release
#Modify At your Own Risk

import maya.cmds as cmds

def na_comboMaker(default = '', sculpted = '', posed = ''):
    """given a default,posed and sculpted mesh make a sculpted + posed mesh.
    default             -- this is mesh with no changes from its starting vtx locations
    posed/addThis       -- this is mesh we want to add
    sculpted            -- this is mesh we want to keep after we add posed    
    """

    print("[na_comboMaker] Beginning")
    #make sure arguments exist may need to bring in sys
    defaultArg = ''
    sculptedArg = ''
    posedArg = ''
    
    defaultArg = default
    sculptedArg = sculpted
    posedArg = posed
    
    dupDefault = ''
    #duplicate default (dupdefault)
    dupDefault = cmds.duplicate(defaultArg)
    
    #make blendshape into dupdefault with posed and sculpted
    cmds.blendShape(posedArg,sculptedArg,dupDefault,n = 'na_comboMaker_blend') #if error out just remove any old correctiveMaker blendnodes on scene
    
    #put blendshape weight on blendnode to 1 on posed, find where to put weight based on ordering of targets. 
    cmds.setAttr( 'na_comboMaker_blend.w[0]', 1.0 )
    
    #put blendshape weight on blendnode to 1 on sculpted
    cmds.setAttr( 'na_comboMaker_blend.w[1]', 1.0 )
    
    #duplicate dupdefault and call it result
    resultMesh = ''
    resultMesh = cmds.duplicate(dupDefault)
    
    #translate result's transform to where sculpted currently is
    #move to sculpted, result
    constraint = cmds.parentConstraint(sculpted,resultMesh, mo = 0)
    
    cmds.delete(constraint)
    #remove the blendshape created and no longer needed
    cmds.delete(dupDefault)
    
    print("[na_comboMaker] Done !")
    return dupDefault