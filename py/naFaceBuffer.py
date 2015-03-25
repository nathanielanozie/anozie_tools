#######
#Help with building Facial Rig User interface buffer
#By
#Nathaniel O. Anozie (ogbonnawork at gmail dot com)
#
#Inspired by Jason Osipa
#
#see also na_faceIt.py (more ui based)
#######

#01-23                  working on connection bug to skip if connection exists
#01-22                  added direct connection between two nulls support
#01-22                  added attribute making from mesh with targets support
#created: 01-21-2015    initial release

import maya.cmds as cmds

def help():
    help = """
    #puts bs onto null
    naFaceBuffer.addBSOnFirstToSecondSelected()
    
    #given a few null we wish to combine output to face rig, this links them per plug
    naFaceBuffer.layerControl_addInput()
    
    #given a few nulls selected with identical attributes, this puts their combined ouput onto an ouput null
    naFaceBuffer.layerControl_addOutput( output = 'OuputName' )
    
    #given two nulls same attributes, direct connect them
    naFaceBuffer.layerControl_connectFirstToSecond()
    """
    print help
    
    
def addBSOnFirstToSecondSelected( min = 0, max = 10 ):
    """
    given first mesh with blendshapes, then select second a null
    put an attribute of same name as target on null
    --can change range for each attribute
    --assumes no duplicate names
    """   
    sel = cmds.ls(selection = True)
    if sel is not None and len(sel) == 2:
        obj = sel[0]
        null = sel[1]
        history = cmds.listHistory(obj)#cmds.listHistory(obj[0])  #IndexError
        bsHistory =  cmds.ls(history, type = 'blendShape')
        blendNode = ''
        blendTargets = []
        try:
            blendNode = bsHistory[0] #assuming exists, would change this to allow multiple blendnodes on selected
            #get target weights
            blendTargets = cmds.blendShape(blendNode, target = True, query = True)
        except IndexError:
            print 'Cannot find blendshapes to use check input !'
        
        #add attribute
        for i in range(len(blendTargets)):      
            target = blendTargets[i]
            #this bit makes sure to skip if attribute already at destination
            if cmds.attributeQuery( target, node=null, exists=True ) == 0:
                cmds.addAttr( null, ln = target, at = 'double', min = min, max = max, dv = 0 )
                cmds.setAttr( null+'.'+target,edit = True, keyable = True )
            else:
                print 'Skipping %s.%s >> attribute exists' %(null,target)
    else:
        print 'Make sure a mesh is selected that has blendshapes, and a destination null'    
       
def layerControl_addOutput( output = ''  ):
    """
    assumes selected are nulls with existing blendnodes hooked up
    it finds blendweighted nodes from selected it finds name of attribute 
    looking for and puts them onto argument.
    (it uses the first blendweighted node slot only to figure out plug name) 
    -- if ouput is connected already it skips that plug and moves on
    """
    #not supporting
    #no output given
    #finding wrong blendweighted nodes to use , possibly because of nested networks
    #blendweighted nodes dont match with attributes of incoming
    
    if cmds.objExists(output):
        sel = cmds.ls(selection = True)
        transform = []
        transform = sel
        
        #select blendweighted nodes from selected
        nodes = []
        nodes = cmds.listConnections( transform[0], type = 'blendWeighted', source = False, destination = True)#assumes no duplicates
        if nodes is not None:
            #get plugs off nodes so order matches
            plugs = []
            for j in range(len(nodes)):
                myNode = nodes[j]
                mySource = cmds.listConnections( myNode+'.input[0]', source = True, destination = False,plugs = True)#assumes length 1
                p = []
                p = mySource[0].split('.')[-1:] #get attribute name by split by dot and give back last part
                plugs.append(p[0])
                
            #hook up output for each blendweighted 
            myOutput = ''
            myOutput = output
            for i in range(len(nodes)):
                myNode = nodes[i]
                myPlug = plugs[i]
            
                #skip if destination is connected already
                destinationInput = cmds.listConnections( myOutput+'.'+myPlug,source=True,destination=False)
                if destinationInput is None:
                    cmds.connectAttr(myNode+'.'+'output',myOutput+'.'+myPlug)
                    print 'Connecting %s.output >> %s.%s\n' %(myNode,myOutput,myPlug)
                else:
                    print 'skipping >> %s ouput already connected' %(myPlug)
        else:
            print 'Make sure you have selected transforms with blendweighted connections!'

def layerControl_connectFirstToSecond(plugs = []):
    """
    direct connect all first plugs to second
    --assumes both have identical plugs
    --if no plugs given it assumes to connect all user defined plugs of first thing
    --not supporting locked or connected plugs
    """
    sel = cmds.ls(selection = True)
    if sel is not None and len(sel) == 2:
        mySource = sel[0]
        myDestination = sel[1]        
        #plugs = ['left','right']
        if len(plugs) == 0:
            #use all user defined attribute of first thing selected
            userDefined = cmds.listAttr( mySource,  ud = True )
            plugs = userDefined
            
       #link both transforms with identical attributes
        for m in range(len(plugs)):
            myPlug = plugs[m]      
            try:
                cmds.connectAttr(mySource+'.'+myPlug,myDestination+'.'+myPlug) #might want a force, no error checking
                print 'Connecting >> %s' %(myPlug)
            except RuntimeError:
                print 'Skipping >> %s -- check locked or connected plugs not supported' %(myPlug)
    else:
        print 'Make sure you have selected 2 transforms with identical attributes!'


def layerControl_addInput( plugs = [], isRangeTen = True ):
    """    
    given selected transforms, it makes one blendweighted node for each plug and feeds selected into them
    --if you dont specify any plugs it will try to use all user defined attributes
    --if you put false on 0-10 range get 0-1 ranges
    --if you want to do just for a specific new plug enter it in argument
    --assumes every plug exists on each thing selected
    --order of selected transform is order of node inputs
    --if 0,1 selected do nothing
    """
    #not supporting
    #if 2 or more selected
                 
    #get selection that has plugs on them
    sel = []
    sel = cmds.ls(selection = True)
    if len(sel) > 1:
        transform = []
        transform = sel
        
        #plugs = ['left','right']
        
        if len(plugs) == 0:
            #use all user defined attribute of first thing selected
            userDefined = cmds.listAttr( transform[0],  ud = True )
            plugs = userDefined
        
        #plugs = layerControlHelp_getPlugs( plugs, transform[0] )
            
        #create one blend node for each plug
        #it doesnt know how to reuse existing work
        bweight = []
        for i in range(len(plugs)):
            node = []
            node = cmds.createNode('blendWeighted')
            bweight.append(node)
            
        #for each blend node hook each selected into blendnode by default order
        for m in range(len(bweight)):
            myPlug = plugs[m]      
            myNode = bweight[m]
            for n in range(len(transform)):
                myTransform = transform[n]
                
                """ 
                cmds.connectAttr('null1'+'.'+'left',node+'.input['+str(0)+']') 
                cmds.connectAttr('null2'+'.'+'left',node+'.input['+str(1)+']') 
                """
                print 'Connecting %s.%s >> %s\n' %(myTransform,myPlug,myNode)
                cmds.connectAttr(myTransform+'.'+myPlug,myNode+'.input['+str(n)+']') #might want a force
                cmds.setAttr( (myNode+'.weight['+str(n)+']'), 1.0 )#default 0-1 range
                
        if not isRangeTen:
            #allow 0-10 range
            myNode = bweight[0]
            cmds.setAttr( (myNode+'.weight['+str(0)+']'), 0.1 )
            
##############            
help() 
##############