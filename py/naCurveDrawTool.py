"""

    This file is part of naCurveDrawTool.

    naCurveDrawTool is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/lgpl.html>.

    Author:     Nathaniel Anozie      ogbonnawork at gmail dot com
    Url:        nathananozie dot blogspot dot com
    Date:       2015 / 02 / 17

"""

#02-17-2015     --  working on initial release

import maya.cmds as cmds
import maya.OpenMaya as om #for error checking
import maya.mel as mel #used for drawing curve

def help():
    help="""##examples
import naCurveDrawTool
naCurveDrawTool.increaseJointRadiusOnSelected()  #needs joints selected #optional: .05 , -.05 delta to use
naCurveDrawTool.drawCurveByWorldPositionOnSelected() #needs transforms selected
naCurveDrawTool.overwriteSelectionByOrdering( cmds.ls(selection = True) )#optional: ,worldPositionIndex = 0, isPlusLastSelected = 1 #x,y,z are index (0,1,2)
    """
    print help
    
def drawCurveByWorldPositionOnSelected( worldPositionIndex = 0, isPlusLastSelected = 1 ):
    """
    worldPositionIndex -- 0,1,2 correspond to x,y,z
    isPlusLastSelected -- if 0 plus would be first thing selected
    """
    sel  = cmds.ls(selection = True)

    if len(sel) != 0:
        orderedSelection = sortByWorldPosition( argToSort = sel, worldPositionIndex = 0, isPlusLastSelected = 1   )
        drawCubicCurve( orderedSelection ) #draws in order of input
    else:
        om.MGlobal.displayError("Nothing Selected.  First select some dag things")    

    
def drawCubicCurve( arg = [] ):
    """
    note: should be parameterized 0-1 (I think Currently this is not supported)
    note: should return the curve transform name
    """
    curve = drawCurve( places = arg, curveType = 'cubic')
    setCurveParameterZeroOne( curve, 'cubic' )
    
    
def increaseJointRadiusOnSelected( delta = 0.05 ):
    """
    repeatedly calling increases joint radius by delta
    """
    sel  = cmds.ls(selection = True, type = 'joint')
    if sel is not None:
        for arg in sel:
            cRadius = cmds.getAttr( arg+'.radius' )
            amount = cRadius + delta
            if amount < 0:
                cmds.setAttr( arg+'.radius', 0.01 ) #minum radius
            else:
                cmds.setAttr( arg+'.radius', amount )
    else:
        om.MGlobal.displayError("Joint not Provided.  Select joint(s) to edit radius")
    
    
def overwriteSelectionByOrdering( argToSort = [], worldPositionIndex = 0, isPlusLastSelected = 1   ):
    newSel = sortByWorldPosition( cmds.ls(selection=True), worldPositionIndex = 0, isPlusLastSelected = 1   )
    cmds.select(newSel,replace = True)
    
def sortByWorldPosition( argToSort = [], worldPositionIndex = 0, isPlusLastSelected = 1   ):
    """
    returns list of sorted argument dag names
    
    worldPositionIndex -- 0,1,2 correspond to x,y,z
    isPlusLastSelected -- if 0 plus would be first thing selected
    """

    result = [] #ordered selection
    
    #sel  = cmds.ls(selection = True)
    sel = argToSort
    componentExpand = cmds.filterExpand( sel, sm=(28,31) )
    
    expandSel = sel #to support component would need to check if filterExpand gave something
    if componentExpand is not None:
        expandSel = componentExpand
    
    #worldPositionIndex = 0 
    #isPlusLastSelected = 1
    
    worldPosition = []
    for arg in expandSel:
        pos = (cmds.xform( arg, translation = True, ws = True, query = True))[worldPositionIndex]
        tup = (pos, arg) #position needs to be first because sorting using first item
        worldPosition.append( tup )
    
    #sort tuple
    sortedWorldPosition = sorted(worldPosition)
    if isPlusLastSelected == 0:
        sortedWorldPosition = sorted(worldPosition,reverse = True)
        
    result = map( lambda x: x[1], sortedWorldPosition)
    
    return result
    
    
def setCurveParameterZeroOne( curve = None, curveType = 'linear' ):
    """
    preserve editpoints and parameterize curve to 0-1.
    
    curve -- transform curve name
    curveType -- linear(default) or cubic
    
    """
    result = []
    if curve is not None:
        curveDegree = 1 #defaults to linear
        if curveType == 'cubic':
            curveDegree = 3
            
        #make a duplicate to be used for knots
        knotCurve = cmds.duplicate( curve )
        cmds.rebuildCurve( curve, knotCurve, rpo = 1, rebuildType = 2, endKnots = 1, keepRange = 0, keepControlPoints = 1, keepEndPoints = 1, keepTangents = 0,  d= curveDegree)
        cmds.delete(knotCurve) #no longer needed        
    else:
        om.MGlobal.displayError("Curve not Provided.  Provide curve to parameterize at 0-1")
        
    return result        
    
def drawCurve( places = None, curveType = 'linear'):
    """
    draw cvs on places provided
    
    curveType -- linear(default) or cubic
    
    this is useful for buiding dynamic cloth, ears etc. or drawing spines
    """
    result = []
    if places is not None:

        #curve -d 1 -p 0 0 0 -p 5 0 0
        curveDegree = 1 #defaults to linear
        if curveType == 'cubic':
            curveDegree = 3
        cmd = 'curve -d %d ' %curveDegree
        
        #go through dag names forming command for making cvs in order
        for i in range( len(places) ):
            pos = cmds.xform(places[i], query = True, translation = True, ws = True)
            #curve -d 1 -p 0 0 0 -p 5 0 0
            cmd += '-p %f %f %f ' %(pos[0],pos[1],pos[2]) 
            
        cmd+= ";"
        result = mel.eval(cmd)
    else:
        om.MGlobal.displayError("Curve points not Provided.  Provide dag names for where to make editpoints")
        
    return result    