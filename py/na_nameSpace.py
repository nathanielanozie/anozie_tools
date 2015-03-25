##@file na_nameSpace.py 
#
#Tools changing names
#
#@author Nathaniel Anozie

import maya.cmds as cmds


##change part of name to opposite of specified 
#@note ex: (root='group1',inputIsLeft=True) would change lefts into right using ':l_' as left symbol
#
##
def oppositeNameSpace( root = '', inputIsLeft = True, leftSymbol=':l_',rightSymbol=':r_' ):
    sel = cmds.ls(sl = True)
    
    cmds.select(clear=True)
    cmds.select(root, hierarchy=True)
    selected = cmds.ls(sl = True)
    
    param = [leftSymbol,rightSymbol]
 
    reverseSelected = selected
    reverseSelected.reverse() #so we can start renaming child nodes before parent
    
    if inputIsLeft:
        for obj in reverseSelected:
            name = obj
            newName = name.replace(param[0],param[1])
            cmds.rename(obj,newName)
        
    else:
        for obj in reverseSelected:
            name = obj
            newName = name.replace(param[1],param[0])
            cmds.rename(obj,newName)
            
    cmds.select(clear=True)
    
        
def oppositeNameSpace_unitTest():
    j1=cmds.joint(p=[0,4,0],n='b_l_hand_joint1')
    j2=cmds.joint(p=[0,3,0],n='bs_l_hand_joint2')
    j3=cmds.joint(p=[0,2,0],n='ab_l_hand_joint3')
    j4=cmds.joint(p=[0,1,0],n='a_l_hand_joint4')
    oppositeNameSpace(j1,inputIsLeft=True, leftSymbol='l_',rightSymbol='r_')
