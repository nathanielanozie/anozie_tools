##@file rename.py
#
#(Tested Maya 2008)
#
#@author Nathaniel Anozie
#
#@note Inspired By Steven F.Lott (slott-softwarearchitect dot blogspot dot com) for learning about raising notimplementedError
#@note Inpired By James Parks (arcsecond dot net) for learning about list handling
#@note Inspired By Matt Estela (tokeru dot com) for learning about IndexError exception
#
#@defgroup name Renaming naming tools
#@{
#ex: renameJointHierarchyByRoot(root = cmds.ls(selection = True), prefix='joint') names all joints in h 
##


import maya.cmds as cmds


def renameJointHierarchyByRoot_unitTest():
    j1=cmds.joint(p=[0,0,0])
    j2=cmds.joint(p=[1,0,0])
    j3=cmds.joint(p=[2,0,0])
    cmds.select(j1,replace=True)
    renameJointHierarchyByRoot()
    
##rename joint hierarchy inserting number note requires root to be selected on scene
#@note underscore automatically included
##
def renameJointHierarchyByRoot( prefix='pre', suffix='joint'):
    
    curSel = cmds.ls(selection=True)
    root = cmds.ls(selection = True)
    
    #hold all the joints in hiearchy here
    allJoint = [] 
    
    try:
        base = root[0]
        cmds.select(base,replace=True)
        allHierarchy = cmds.select(hierarchy=True)
        allJoint = cmds.ls(selection = True, type = 'joint')
    except IndexError:
        print "Requires a root input (root) or selection"
    
    #add increasing integer to name giving format prefix_integer_suffix
    allJointName=[]
    for i in range(len(allJoint)):
        try:
            joint = allJoint[i]
            cmds.select(joint,replace=True)
            
            try:
                jointName = prefix+'_'+str(i+1)+'_'+suffix
                allJointName.append(jointName)
                cmds.rename(joint,jointName)
            except RuntimeError:
                print "Require Single Occurence of Joint >> %s" %joint
  
        except TypeError:
            print "Require Existence of Joint >> %s" %joint

            
    #replace current selection        
    if len(allJointName) > 0:
        try:
            cmds.select(allJointName[0],replace=True)
        except TypeError:
            print "Skipping Restore Selection, Requires Single Occurence of Joint >> %s" %allJointName[0]            
            
##
#@}
##
        
