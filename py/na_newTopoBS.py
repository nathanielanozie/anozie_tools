# updated 11-24-2014 nate ----- added ui
# updated 08-06-2014 nate ----- initial release

#Modify At your Own Risk


import maya.cmds as cmds
import maya.mel as mel
mel.eval( "source \"facerigMakeSelSectionIntoFullBlendshape.mel\";" ) #needed for mesh creation

def na_newTopoBS(newTopo = '', oldDefaultNewTopo = '', oldDefault = ''):
    """given some selected blendshapes an old/new topo mesh, and a new topo mesh shaped like old make new topo bs
    newTopo			-- this is new topology but not shaped like old mesh  
    oldDefaultNewTopo 	-- this is new topolgy but shaped like old mesh
    oldDefault		-- this is old topology base mesh, selected bs should have this topology
    """
    result = []
    
    ##get input
    sel = cmds.ls(selection = True) #no checking that these are all meshes and more than one selected
    oldTopoBS = []
    oldTopoBS = sel
    #newTopo = 'pCube2'
    #oldDefaultNewTopo = 'pCube2a'
    #oldDefault = 'pCube1'
    isExist = all( map( lambda x: cmds.objExists(x), [newTopo,oldDefaultNewTopo,oldDefault]) )
    if not isExist or len(oldTopoBS) == 0:
        print "\nInput Error-- try --> help(na_newTopoBS)\n"
        return 0
        
    #############DO THIS ONCE -- make mesh to help us with the math
    #so not potentially overwriting input
    dupNewTopo = ''
    dupOldDefaultNewTopo = ''
    dupOldDefault = ''
    dupNewTopoAr = cmds.duplicate(newTopo)
    dupOldDefaultNewTopoAr = cmds.duplicate(oldDefaultNewTopo)
    dupOldDefaultAr = cmds.duplicate(oldDefault)
    dupNewTopo = dupNewTopoAr[0]
    dupOldDefaultNewTopo =dupOldDefaultNewTopoAr[0]
    dupOldDefault=dupOldDefaultAr[0]
    #done getting input
    
    ####make mesh to help us with the math
    #make blendshape into newTopo with oldDefaultNewTopo
    cmds.blendShape(dupOldDefaultNewTopo,dupNewTopo,n = 'na_newTopoBS_blend') #fix name ok because cleanup
    #put blendshape weight on blendnode, find where to put weight based on ordering of targets. 
    cmds.setAttr( 'na_newTopoBS_blend.w[0]', -1.0 )
    #duplicate it and call it result
    enterNewTopoSpaceMesh = ''
    enterNewTopoSpaceMeshAr = cmds.duplicate(dupNewTopo)
    enterNewTopoSpaceMesh = enterNewTopoSpaceMeshAr[0]        
    
    
    #cleanup
    cmds.delete(dupNewTopo)
    cmds.delete(dupOldDefaultNewTopo)
    cmds.delete(dupOldDefault)
    ###############  
    
    
    #############DO THIS ONCE -- get new topo meshes shaped like old blendshapes
    print "[start] get new topo meshes shaped like old blendshapes"
    newTopoShapedLikeSelectedBS = []
    #so not potentially overwriting input
    dupNewTopo = ''
    dupOldDefaultNewTopo = ''
    dupOldDefault = ''
    dupNewTopoAr = cmds.duplicate(newTopo)
    dupOldDefaultNewTopoAr = cmds.duplicate(oldDefaultNewTopo)
    dupOldDefaultAr = cmds.duplicate(oldDefault)
    dupNewTopo = dupNewTopoAr[0]
    dupOldDefaultNewTopo =dupOldDefaultNewTopoAr[0]
    dupOldDefault=dupOldDefaultAr[0]
    #done getting input
       
    ##get new topo meshes shaped like old blendshapes
    cmd = 'facerigMakeSelSectionIntoFullBlendshape' #no exist check
    arg1 = '"%s"' %dupOldDefaultNewTopo
    arg2 = '"%s"' %dupOldDefault
    newTopoShapedLikeSelectedBSCmd = "%s(%s,%s)" %(cmd,arg1,arg2)   
    try:
        cmds.select(oldTopoBS,replace=True)#need to select bs
        newTopoShapedLikeSelectedBS = mel.eval(newTopoShapedLikeSelectedBSCmd)  #no checking whether these are in fact good to go 
    except RuntimeError:
        print 'Error >> %s >> mesh creation' %cmd
    
    #cleanup
    cmds.delete(dupNewTopo)
    cmds.delete(dupOldDefaultNewTopo)
    cmds.delete(dupOldDefault)
    print "[done] get new topo meshes shaped like old blendshapes"
    #############
    
    
    #############DO THIS FOR EACH SELECTED BS -- shape new topo bs like we want them
    for arg in newTopoShapedLikeSelectedBS:
        #so not potentially overwriting input
        dupNewTopo = ''
        dupNewTopoAr = cmds.duplicate(newTopo)
        dupNewTopo = dupNewTopoAr[0]
        #done getting input
        
        #get our final result
        #feed it and "topoSpaceMesh" into "newTopo" mesh both at 1 weight and duplicate out mesh
        ####make mesh to help us with shaping
        #make blendshape into new topology with space math mesh and rough shaped mesh
        cmds.blendShape(enterNewTopoSpaceMesh,arg,dupNewTopo,n = 'na_newTopoBS_blend') #fix name ok because cleanup
        #put blendshape weight on blendnode, find where to put weight based on ordering of targets. 
        cmds.setAttr( 'na_newTopoBS_blend.w[0]', 1.0 )
        cmds.setAttr( 'na_newTopoBS_blend.w[1]', 1.0 )
        #duplicate it and call it result
        resultShapedMesh = ''
        resultShapedMeshAr = cmds.duplicate(dupNewTopo,name = arg+'NA')
        resultShapedMesh = resultShapedMeshAr[0]                
        
        #save
        result.append(resultShapedMesh)
        
        #cleanup
        cmds.delete(dupNewTopo)
        #translate result's transform to where sculpted currently is
        #move to arg, result
        constraint = cmds.parentConstraint(arg,resultShapedMesh, mo = 0)
        cmds.delete(constraint)
    
    #############END DO THIS FOR EACH SELECTED BS

    
    
    #overall cleanup
    cmds.delete(newTopoShapedLikeSelectedBS)
    cmds.delete(enterNewTopoSpaceMesh)
    
    
def na_newTopoBSUI():
    """
    select new topology, then posed, then the default mesh
    """
    
    sel = []
    sel = cmds.ls(selection = True)
    if len(sel) == 3:
        print "\nSELECT BS ONLY --- run in PYTHON editor:\n"
        print "na_newTopoBS(newTopo = '%s', oldDefaultNewTopo = '%s', oldDefault = '%s')" %(sel[0], sel[1],sel[2])
        cmds.select(clear=True)
    else:
        print "select new topology, then posed, then the default mesh!"