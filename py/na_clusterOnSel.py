##@file na_clusterOnSel.py Cluster Syntax
#updated    nate 02/10/15   --adding warnnig if select unsupported object
#updated    nate 09/04/14   --added lattice support
#updated    nate 05/30/13   --added cluster all option, fixed empty case bug
#@author Nathaniel Anozie


import maya.cmds as cmds


##put one cluster per each selected vertex or cv
#
#@pre components selected on scene
#@param isClusterAll --true means cluster everthing selected otherwise it makes a cluster for each thing
#
def na_clusterOnSelected(isClusterAll = False):
    selected = cmds.ls(sl = True)
    component = cmds.filterExpand( selected, sm=(28,31,46) )
    if component is not None:
        #only considers poly vertices or cvs or lattice points
        #component = cmds.filterExpand( sm=(28,31,46) )
        
        #can cluster everthing or each thing
        if not isClusterAll:
            for obj in component:
                cmds.select(obj, replace = True)
                cmds.cluster(relative = True, envelope = 1)
        else:
            cmds.select(component, replace = True)
            cmds.cluster(relative = True, envelope = 1)        
            
        cmds.select(selected, replace = True)
    else:
        print("Requires Components ex. cvs selected!!!\n");
