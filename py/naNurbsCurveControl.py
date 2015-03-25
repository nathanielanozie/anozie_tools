#######
#Help with building Facial Rig User interface secondary movers
#By
#Nathaniel O. Anozie (ogbonnawork at gmail dot com)
#
#Inspired by Andy Van Straten -- learning about joints riding on curves
#Inspired by Fabio Bonvicini -- i was inspiredy by his curve based online tutorials on facial rigs
#
#
#see also naNurbsSurfaceControl, naFaceBuffer (more phoneme based) na_faceIt.py (more ui based)
#######

#02-16                  working on adding orientation
#02-13                  initial release
#02-05                  working on initial release -- currently it will also snap to cv location, adding template ui
#added template ui, added main and help usability functions
#02-04                  working on initial release -- added oop template start
#created: 02-04-2015    created


import maya.cmds as cmds
import re #used for ui

def help():
    help = """
    #This tool helps with getting nulls following a curves movement
    import naNurbsCurveControl
    reload(naNurbsCurveControl)
    
    #run this after selecting in order below
    #1. nulls want to rivet
    #2. cluster widget want to help move nulls (identical number as nulls, identical order as nulls, one cv per cluster)
    #3. last the single Nurbs curve transform you want nulls to follow
    
    naNurbsCurveControl.main()
    """
    print help
    
def main():
    """
    just have selected all the nulls, all cluster widgets, last surface kind of like blendshapes. this allows nulls to follow surface
    """
    #get selection new naNurbsCurveControlUI() 
    surf = ''
    nullList = []
    clusterWidgetList = []
    cvIndexList = []

    sel = cmds.ls(selection = True)
    ui = naNurbsCurveControlUI(  sel  )
    curve = ui.getCurve()
    nullList = ui.getNull()
    clusterWidgetList = ui.getClusterWidget()   
    cvIndexList = ui.getCVIndexList()  

    #loop selection 
    #--initialize-- create new naNurbsCurveControl() 
    #--go           do the backend stuff
    for null, anim, cvID in zip( nullList, clusterWidgetList, cvIndexList):
        ctrl = naNurbsCurveControl(null,curve, cvID) 
        ctrl.go()




class naNurbsCurveControlUI(object):
    def __init__(self, sel = []):
        self.selection = sel
        self.curve = ''
        self.null = []
        self.clusterWidget = []
        self.cvIndexList = []
        
        self.go()
        
    def go(self):
        print '[naNurbsCurveControlUI] parsing user selection'
        selectionDict = self.splitSelectionTwoHalfAndLast()
        self.setCurve( selectionDict[ 'last' ] )
        self.setNull( selectionDict[ 'first' ] )
        self.setClusterWidget( selectionDict[ 'second' ] )
        self.setCVIndexList() #this should populate cv index
        print '[naNurbsCurveControlUI] DONE parsing user selection'
        #now data should populated to be used externally
         
    #basics    
    def getCurve(self):
        return self.surface
    def setCurve(self, arg = ''):
        self.surface = arg
    def getNull(self):
        return self.null
    def setNull(self, arg = []):
        self.null = arg
    def getClusterWidget(self):
        return self.clusterWidget
    def setClusterWidget(self, arg = []):
        self.clusterWidget = arg
    def getCVIndexList(self):
        return self.cvIndexList
    def setCVIndexList(self):
        """
        given cluster list it sets cv index list, order preserved
        """
        result = []
        clusterList = self.getClusterWidget()
        
        for clusterHandle in clusterList:
            #print 'COMPUTING CV INDEX for %s' %(clusterHandle)
            cvIndex = 0
            clusterAr = []
            clusterHandleShapeAr = []
            clusterSetAr = []
            #get cluster handle shape from cluster handle
            #listRelatives -children -type "clusterHandle" cluster3Handle
            clusterHandleShapeAr = cmds.listRelatives( clusterHandle, children = True, type = "clusterHandle" )
            
            #get cluster from cluster handle shape
            #listConnections -type "cluster" cluster3HandleShape;
            clusterAr = cmds.listConnections( clusterHandleShapeAr[0], type = "cluster")
            clusterSetAr = cmds.listConnections( clusterAr[0], type = "objectSet")
            
            #print 'using cluster set %s' %(clusterSetAr[0])
            cvAllAr = cmds.sets( clusterSetAr[0], query = True ) #no error checking
            cvIndex = re.search(re.escape('[')+"(.*)"+re.escape(']'),str(cvAllAr[0]) ).group(1)
            result.append( int(cvIndex) )
            #print 'DONE COMPUTING CV INDEX for %s' %(clusterHandle)
        self.cvIndexList = result #no error checking
        
    def getSelection(self):
        return self.selection
    def setSelection(self, arg = []):
        self.selection = arg   


        
    def splitSelectionTwoHalfAndLast(self):    
        """
        returns dictionary of first half of selection, last half of selection, then last element
        no error checking assumes length >=3, and length odd
        """
        result = {'last':'', 'first':[], 'second':[] }
        sel = self.getSelection() #
        #remove last element and save
        #split into two the remaining part

        #NO ERROR CHECKING        
        result[ 'last' ] = sel[-1:]
        half = (len(sel)-1)/2
        result[ 'first' ] = sel[:half]
        result[ 'second' ] = sel[half:(len(sel)-1)]

        return result

        
        
class naNurbsCurveControl(object):
    def __init__(self, null = '', curve = '', cvIndex = 0 ):
        self.cvIndex = cvIndex
        self.curve = curve
        #reason curveInfo not a private variable is because it could change on the maya scene vary easily
        self.name = null

    def go(self):
        """
        This is primarily what the user calls after initialization
        """
        null = self.getName()
        print 'setting translation attachment for <-- %s' %(null)
        self.attachCurveInfo()
        
        print 'setting orientation attachment for <-- %s' %(null)
        self.orientToTangentCurve()
        
        print ' naNurbsSurfaceControl.go complete '
        
    #typical variable related    
    def getCvIndex(self):
        return self.cvIndex
    def setCvIndex(self, arg = 0):
        self.cvIndex = arg
    def getCurveName(self):
        return self.curve
    def getName(self):
        return self.name
        
    
    def getCurveInfo(self):
        """
        given a curve find whether it has a curve info or not, if it does return its name in list
        if it doesnt it returns an empty list
        """
        result = []
        curveShape = self.getCurveShapeName()
        #check whether input is a curve info
        curveInfo = cmds.listConnections( curveShape+'.'+'worldSpace[0]', type = "curveInfo", source=False, destination=True)
        if curveInfo is not None:
            result = curveInfo
            
        return result
        
    def attachCurveInfo(self):
        """
        depending on wether or not curve has an info node it will build a curve info and attach
        to proper null with proper cv index
        """
        curveShape = self.getCurveShapeName()
        curveInfo = ''
        curveInfoCheck = []
        curveInfoCheck = self.getCurveInfo() #if it is not empty use its first element as curve info,
        #if its empty make a curve info node 
        if len(curveInfoCheck) == 0:
            #make and attach curve info
            info = cmds.createNode('curveInfo')
            cmds.connectAttr(curveShape+'.'+'worldSpace[0]', info+'.'+'inputCurve')
            #make movability of null from curve
            curveInfo = info
            self.addNullToCVIndex( curveInfo )
        else:
            curveInfo = curveInfoCheck[0]
            #make movability of null from curve
            self.addNullToCVIndex( curveInfo )

    def orientToTangentCurve(self):
        """
        make null orient to tangent of curve
        """
        null = self.getName()
        curveShape = self.getCurveShapeName()
        cmds.tangentConstraint( curveShape, null, weight= 1, aimVector=[1,0,0], upVector=[0,1,0], worldUpVector = [0, 1, 0], worldUpType = "vector")
        
    def addNullToCVIndex(self, curveInfo = ''):
        """
        make null move when proper cv is moved, needs a curve info node.
        """
        null = self.getName()
        index = self.getCvIndex() #no error checking
        myCurveInfo = curveInfo
        if cmds.objectType(myCurveInfo) == 'curveInfo':
            #add null to cv using curve info
            cmds.connectAttr(myCurveInfo+'.'+'controlPoints['+str(index)+']', null+'.'+'translate')        
        
    #extras    
    def getCurveShapeName(self):
        """
        returns empty string if it cannot find one
        """
        result = ''
        myCurve = self.getCurveName()
        myCurveShapeAr = cmds.pickWalk(myCurve, direction = 'down') #double check selection not changed
        myCurveShape = myCurveShapeAr[0]
        if cmds.objectType(myCurveShape) == 'nurbsCurve':
            result = myCurveShape
            
        return result