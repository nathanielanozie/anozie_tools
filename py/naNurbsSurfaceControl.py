#######
#Help with building Facial Rig User interface secondary movers
#By
#Nathaniel O. Anozie (ogbonnawork at gmail dot com)
#
#Inspired by Matt Estella (tokeru dot com) -- learning about constraint methods from his online tutorials
#Inspired by Hamish Mckenzie (macaronikazoo dot com) -- learning about zip for loops from his online tutorials
#Inspired by Chris Hickman -- i was inspired by his facial rigging work and online tutorials
#
#
#see also naFaceBuffer (more phoneme based) na_faceIt.py (more ui based)
#######

#02-04                  working on initial release -- added ability to work with a user selection
#02-03                  working on initial release -- added attr in channel,
#added rest info saving, added layer control, added final uv values
#02-02                  working on initial release -- added template
#created: 02-02-2015    created

import maya.cmds as cmds

def help():
    help = """
    import naNurbsSurfaceControl
    reload(naNurbsSurfaceControl)
    
    #run this after selecting in order below
    #1. nulls want to rivet
    #2. animator widget want to help move nulls (identical number as nulls, identical order as nulls)
    #3. last the single Nurbs surface transform you want nulls to follow
    
    naNurbsSurfaceControl.main()
    """
    print help
    

def main():
    """
    just have selected all the nulls, all animator widgets, last surface kind of like blendshapes. this allows nulls to follow surface
    """
    #get selection new naNurbsSurfaceControlUI() 
    surf = ''
    nullList = []
    animatorWidgetList = []
    
    sel = cmds.ls(selection = True)
    ui = naNurbsSurfaceControlUI(  sel  )
    surf = ui.getSurface()
    nullList = ui.getNull()
    animatorWidgetList = ui.getAnimatorWidget()   

    #loop selection 
    #--initialize-- create new naNurbsSurfaceControl() 
    #--go           do the backend stuff
    for null, anim in zip( nullList, animatorWidgetList):
        ctrl = naNurbsSurfaceControl(null,surf) 
        ctrl.setAnimatorWidget( anim )
        ctrl.go()


        
class naNurbsSurfaceControlUI(object):
    def __init__(self, sel = []):
        self.selection = sel #user selection list
        self.surface = ''
        self.null = []
        self.animatorWidget = []
    
        self.go()

    def go(self):
        print '[naNurbsSurfaceControlUI] parsing user selection'
        selectionDict = self.splitSelectionTwoHalfAndLast()
        self.setSurface( selectionDict[ 'last' ] )
        self.setNull( selectionDict[ 'first' ] )
        self.setAnimatorWidget( selectionDict[ 'second' ] )
        print '[naNurbsSurfaceControlUI] DONE parsing user selection'
        #now data should populated to be used externally
        
    def getSurface(self):
        return self.surface
    def setSurface(self, arg = ''):
        self.surface = arg
    def getNull(self):
        return self.null
    def setNull(self, arg = []):
        self.null = arg
    def getAnimatorWidget(self):
        return self.animatorWidget
    def setAnimatorWidget(self, arg = []):
        self.animatorWidget = arg
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

class naNurbsSurfaceControl(object):

    def __init__(self, name = '', surface = ''):
        #major variables
        self.surfaceName = "" #this should be a dag surface that is not only used by this null but any others that are part of this facial area example a lip surface
        self.name = "" #should be full dag name if there are duplicates
        
        #animator widget variables
        self.animatorWidgetName = ""
        self.animatorWidgetUAttribute = "translateX"#change if surface oriented
        self.animatorWidgetVAttribute = "translateY"
        #
        
        #visible attributes
        self.restU_at = "parameterU_rest"
        self.restV_at = "parameterV_rest"
        self.localU_at = "paramterU_local"
        self.localV_at = "parameterV_local"        
        self.comboU_at = "paramterU_combo"
        self.comboV_at = "parameterV_combo"
        self.finalU_at = "parameterU"
        self.finalV_at = "parameterV"
        
        """
        #i dont think need to store these as variables as i think where they are created they are used immediately and not used again
        #plusUNodeName = name+"plusU"   //these 4 nodes are left on scene for every instance of this
        #plusVNodeName = name+"plusV"
        #blendWeightedNodeName = name+"bwNode"
        #pointOnSurfaceNode = name+"surfaceNode"
        """
        
        print 'naNurbsSurfaceControl -- setting name and surface ' 
        self.setName( name )
        self.setSurfaceName( surface )
        print 'naNurbsSurfaceControl -- DONE setting name and surface '
        
        print 'naNurbsSurfaceControl -- setting channel info ' 
        self.setChannelInfo()
        print 'naNurbsSurfaceControl -- DONE setting channel widget '
        
        #print 'naNurbsSurfaceControl -- setting animation widget ' 
        #self.setExternalWidgetInfo()
        #print 'naNurbsSurfaceControl -- DONE setting animation widget '
        
        
    def go(self):
        """
        This is primarily what the user calls after initialization
        """
        null = self.getName()
        
        print 'setting addition <-- %s' %(null)
        self.addLayeredControlToRestInfo()
        print 'setting layered animation <-- %s' %(null)
        self.setLayeredControl()
        print 'setting movability on suface to on <-- %s' %(null)
        self.setPosition()
        print ' naNurbsSurfaceControl.go complete '

        
    def setName(self, arg = ''):
        """
        this should set its name to what the null is named in the DAG
        """
        self.name = arg #NO ERROR CHECKING
    def getName(self, arg = ''):
        """
        this should get its dag name
        """
        return self.name  
        
    def setSurfaceName(self, arg = ''):
        """
        this should set surface to the one used for facial part
        """
        self.surfaceName = arg #NO ERROR CHECKING
    def getSurfaceName(self, arg = ''):
        """
        this should get surface to the one used for facial part
        """
        return self.surfaceName
        
    def setChannelInfo(self):
        """
        find and set animator widget for this structure
        """
        null = self.getName()
        print 'adding uv attributes for %s' %(null)
        self.addUVAttribute()
        print 'adding rest info for %s' %(null)
        self.setRestInfo()
    """    
    def setExternalWidgetInfo(self):
        
        #find and set animator widget for this structure
        #-if it cant find it it does nothing
        
        null = self.getName()
        print 'setting animator widget for %s' %(null)
        widgetFound = self.findAnimatorWidget() #NO ERROR CHECKING
        if cmds.objExists(widgetFound):
            self.setAnimatorWidget(widgetFound)   #only change it if it exists on scene
    """
    def setAnimatorWidget(self, arg):
        """
        this should tell this structure what the name of the animator widget that should be driving this is (we only need this temporarily so reason not saving it onto visible structure)
        """
        self.animatorWidgetName = arg
    def getAnimatorWidget(self):
        """
        """
        return self.animatorWidgetName
    
    """    
    def findAnimatorWidget(self):
        
        #this uses assumption of following a constraint to figure out what the driving widget is
        
        result = ''
        #NOT IMPLEMENTED
        print 'NOT IMPLEMENTED'
        return result
    """
    
    def addUVAttribute(self):
        """
        puts needed parameterUV and rest, float attributes on nulls
        """
        null = self.getName()
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getRestU())
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getRestV())
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getLocalU())
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getLocalV())        
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getComboU())
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getComboV())
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getFinalU())
        cmds.addAttr(null,at = 'float', keyable=True,ln = self.getFinalV())
    #####

    def setRestInfo(self):
        """
        when done this should have used the surface associate with this and this structure dag version to set restU and restV attribute to proper values (clean up any node use for this)
        """
        null = self.getName() #NO ERROR CHECKING expecting: transform

        mySurfaceShape = self.getSurfaceShapeName()
        restU = self.getRestU()  #NO ERROR CHECKING expecting: it exists in channel editor
        restV = self.getRestV()
        info = cmds.createNode('closestPointOnSurface')

        print 'MY SHAPE %s' %mySurfaceShape
        cmds.connectAttr(mySurfaceShape+'.worldSpace[0]',info+'.inputSurface')
        cmds.connectAttr(null+'.translate',info+'.inPosition')
        
        #putting rest uv onto this nulls proper channel in channel editor
        restUValue = cmds.getAttr( info+'.'+"parameterU" ) #NO ERROR CHECKING
        cmds.setAttr( (null+'.'+restU), restUValue )
        restVValue = cmds.getAttr( info+'.'+"parameterV" )
        cmds.setAttr( (null+'.'+restV), restVValue )
        
        cmds.delete(info) #no longer needed

    def addLayeredControlToRestInfo(self):
        """
        this should allow user to use the final attributes as uv's to drive surface
        """
        null = self.getName()
        finalU = self.getFinalU() #this will be used to drive nulls position
        finalV = self.getFinalV()
        comboU = self.getComboU() #these will have combined result either blendweighted input or driven key input 
        comboV = self.getComboV()        
        restU = self.getRestU()  #NO ERROR CHECKING expecting: it exists in channel editor
        restV = self.getRestV()
        
        #this should be able to have animation info, local uv, and rest info combined into single channel in channel editor

        #u
        infoU = cmds.createNode('plusMinusAverage')
        cmds.setAttr( (infoU+".input1D[0]"),0)
        cmds.setAttr( (infoU+".input1D[1]"),0)
        cmds.connectAttr(null+'.'+comboU, infoU+'.'+'input1D[0]')
        cmds.connectAttr(null+'.'+restU, infoU+'.'+'input1D[1]')
        cmds.connectAttr(infoU+'.'+'output1D', null+'.'+finalU)
        
        #v
        infoV = cmds.createNode('plusMinusAverage')
        cmds.setAttr( (infoV+".input1D[0]"),0)
        cmds.setAttr( (infoV+".input1D[1]"),0)
        cmds.connectAttr(null+'.'+comboV, infoV+'.'+'input1D[0]')
        cmds.connectAttr(null+'.'+restV, infoV+'.'+'input1D[1]')
        cmds.connectAttr(infoV+'.'+'output1D', null+'.'+finalV)
                

    def setLayeredControl(self):
        """
        this should combine local (u,v based) and external animation info (translate based)
        
        if no animator widget found i want this to still work !!!
        """
        null = self.getName()
        localU = self.getLocalU()
        localV = self.getLocalV()
        comboU = self.getComboU() #these will have combined result either blendweighted input or driven key input 
        comboV = self.getComboV()
        
        #do the local layer
        #u
        cmds.setDrivenKeyframe( null, at= comboU, cd= null+'.'+localU, dv=-0.5,  v= -0.5 ) #local -0.5, combo -0.5
        cmds.setDrivenKeyframe( null, at= comboU, cd= null+'.'+localU, dv=0.5,  v= 0.5 )
        #v
        cmds.setDrivenKeyframe( null, at= comboV, cd= null+'.'+localV, dv=-0.5,  v= -0.5 ) #local -0.5, combo -0.5
        cmds.setDrivenKeyframe( null, at= comboV, cd= null+'.'+localV, dv=0.5,  v= 0.5 )
        #cmds.setDrivenKeyframe( blendNode, at= right, cd= driver+'.translateX', dv=1,  v= 1 ) #anim right +1, right on
        
        #do external layer IF IT EXISTS
        widget = self.getAnimatorWidget()
        widgetU = self.getAnimatorWidgetUAttribute()
        widgetV = self.getAnimatorWidgetVAttribute()
        if cmds.objExists(widget):
            #u
            cmds.setDrivenKeyframe( null, at= comboU, cd= widget+'.'+widgetU, dv=-0.5,  v= -0.5 ) #local -0.5, combo -0.5
            cmds.setDrivenKeyframe( null, at= comboU, cd= widget+'.'+widgetU, dv=0.5,  v= 0.5 )
            #v
            cmds.setDrivenKeyframe( null, at= comboV, cd= widget+'.'+widgetV, dv=-0.5,  v= -0.5 ) #local -0.5, combo -0.5
            cmds.setDrivenKeyframe( null, at= comboV, cd= widget+'.'+widgetV, dv=0.5,  v= 0.5 )            
        
        #do proper interpolation of frames
        #ex:set linear keyframes with post and pre infinity linear
        print "setLayeredControl -- proper interpolation of frames NOT IMPLEMENTED"
        
    def setPosition(self):
        """
        this should be able to translate this structure based on its finalU and finalV attributes
        """
        #NO ERROR CHECKING
        null = self.getName()
        mySurfaceShape = self.getSurfaceShapeName()
        finalU = self.getFinalU()
        finalV = self.getFinalV()

        info = cmds.createNode('pointOnSurfaceInfo')
        cmds.setAttr( (info+".turnOnPercentage"),1)
        cmds.connectAttr(mySurfaceShape+'.worldSpace[0]',info+'.inputSurface')
        cmds.connectAttr(info+'.position',null+'.translate')
        cmds.connectAttr(null+'.'+finalU,info+'.parameterU')
        cmds.connectAttr(null+'.'+finalV,info+'.parameterV')
         
    #for attributes added to null    
    def getRestU(self):
        return self.restU_at
    def getRestV(self):
        return self.restV_at
    def getLocalU(self):
        return self.localU_at
    def getLocalV(self):
        return self.localV_at        
    def getComboU(self):
        return self.comboU_at
    def getComboV(self):
        return self.comboV_at
    def getFinalU(self):
        return self.finalU_at
    def getFinalV(self):
        return self.finalV_at

    #for proper control that is relative to the surface    
    def getAnimatorWidgetUAttribute(self):
        return self.animatorWidgetUAttribute
    def setAnimatorWidgetUAttribute(self, arg):
        self.animatorWidgetUAttribute = arg #NO ERROR CHECKING: expecting translateX, or Y or Z
    def getAnimatorWidgetVAttribute(self):
        return self.animatorWidgetVAttribute
    def setAnimatorWidgetVAttribute(self, arg):
        self.animatorWidgetVAttribute = arg #NO ERROR CHECKING: expecting translateX, or Y or Z
    
    #extras    
    def getSurfaceShapeName(self):
        """
        returns empty string if it cannot find one
        """
        result = ''
        mySurface = self.getSurfaceName()
        mySurfaceShapeAr = cmds.pickWalk(mySurface, direction = 'down') #double check selection not changed
        mySurfaceShape = mySurfaceShapeAr[0]
        if cmds.objectType(mySurfaceShape) == 'nurbsSurface':
            result = mySurfaceShape
            
        return result        