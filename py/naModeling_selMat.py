import maya.cmds as cmds

def naModeling_selMat():
    """
    select faces that have selected materials
    """
    sel = cmds.ls(selection=True) #should be materials no error checking
    result = []
    for mat in sel:
        cmds.hyperShade(objects = mat)
        for arg in cmds.ls(selection=True):
            result.append(  arg )

    cmds.select(result,replace=True)    