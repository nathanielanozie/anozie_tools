##@file na_correctiveMaker.py
##given a default,posed and sculpted mesh make a sculpted - posed mesh. this is so we can add on shapes to old ones already created

#last updated: 11/24/2014 -- added ui function
#last updated: 04/08/2014 -- working on initial release for use on Smooth's facial brow shapes and body deformation correctives

import maya.cmds as cmds

   

def na_correctiveMaker(default = '', sculpted = '', posed = ''):
    """given a default,posed and sculpted mesh make a sculpted - posed mesh.
    default             -- this is mesh with no changes from its starting vtx locations
    posed/subtractThis  -- this is mesh we want to remove 
    sculpted            -- this is mesh we want to keep after we remove posed    
    """

    print("[na_correctiveMaker] Beginning")
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
    cmds.blendShape(posedArg,sculptedArg,dupDefault,n = 'na_correctiveMaker_blend') #if error out just remove any old correctiveMaker blendnodes on scene
    
    #put blendshape weight on blendnode to -1 on posed, find where to put weight based on ordering of targets. 
    cmds.setAttr( 'na_correctiveMaker_blend.w[0]', -1.0 )
    
    #put blendshape weight on blendnode to 1 on sculpted
    cmds.setAttr( 'na_correctiveMaker_blend.w[1]', 1.0 )
    
    #duplicate dupdefault and call it result
    resultMesh = ''
    resultMesh = cmds.duplicate(dupDefault)
    
    #translate result's transform to where sculpted currently is
    #move to sculpted, result
    constraint = cmds.parentConstraint(sculpted,resultMesh, mo = 0)
    
    cmds.delete(constraint)
    #remove the blendshape created and no longer needed
    cmds.delete(dupDefault)
    
    print("[na_correctiveMaker] Done !")
    return dupDefault
    
    
def na_correctiveMakerUI():
    """
    make corrective, select sculpted, then posed, then the default
    """
    
    sel = []
    sel = cmds.ls(selection = True)
    if len(sel) == 3:
        na_correctiveMaker(default=sel[2], sculpted=sel[0], posed=sel[1])
    else:
        print "select sculpted, then posed, then the default mesh!"