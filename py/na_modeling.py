##@file na_modeling.py
#
#Modeling tools
#
#@author Nathaniel Anozie
#
#@defgroup modeling Modeling
#@{
#Modeling Tools
#
#Mirror Mesh utitlities, outline model for presentation utitlities etc
##

import maya.cmds as cmds

##
#move selected polygon vertices to origin in chosen axis
#@note default x
##
def alignSelectedPolyVertexToOrigin(x=True,y=False, z=False):
    selected = cmds.ls(sl = True)
    component = cmds.filterExpand( sm=(28,31) )
    
    if component is not None:
        isX = x
        isY = y
        isZ = z
        
        for obj in component:
            cmds.select(obj, replace = True)
            worldPosition = cmds.xform(obj,translation = True, query=True, worldSpace = True)
            offSet = map( lambda x: -1*x, worldPosition )
            cmds.move(offSet[0],offSet[1],offSet[2],obj,x=isX,y=isY,z=isZ,relative=True,worldSpace=True)
            cmds.select(selected, replace = True)
    else:
        print '\nRequires Polygon Vertices Selected\n'

def alignSelectedPolyVertexToOrigin_unitTest():
    cube = cmds.polyCube()
    vtx=map( lambda x: cube[0]+x, [ '.vtx[0]', '.vtx[2]', '.vtx[4]', '.vtx[6]' ] )
    cmds.select(vtx,replace=True)
    alignSelectedPolyVertexToOrigin(x=True,y=False, z=False)
##
#@}
##
