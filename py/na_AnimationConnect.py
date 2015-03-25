#na_AnimationConnect.py
#Author: Nathaniel Anozie (ogbonnawork at gmail dot com)
#Description:  Set of tools to help with connecting different skeletons up.  
#Useful for relating mocap skeleton to deformation joints, or relating skeletons with different namespaces by search and replace
#modify at own risk

#12-22-2014     working on add skeleton tool
#12-18-2014     added put rotate connections by search string - added my other animation connect tools into this module
#12-01-2014     created

import maya.cmds as cmds

def putAllConstraintBySearchString(searchStr = '', replaceStr = ''):
    """
    puts translates,rotates constraint from somewhere else onto selected using search and replace string, it wont work with duplicate names.
    """
    
    sel = cmds.ls(selection=True)
    search = searchStr
    replace = replaceStr
    #search = 'TRC_1:' #that is this should be in name of our selected 
    #replace = 'TRC:'    
    
    for arg in sel:
        #only if can find a source otherwise skip
        #'TRC_1:LfFtHead'.replace('TRC_1:','TRC:')  # Result: TRC:LfFtHead # 
        sourceName = arg.replace(search,replace)
        if cmds.objExists(sourceName):
            #print 'putting info on: %s from: %s\n' %(arg,sourceName
            constraint = cmds.parentConstraint(sourceName,arg, mo = 1) #offset ON

        else:
            print 'skipping: %s, cannot find source: %s\n' %(arg,sourceName)
            

def putAddRotateBySearchString(searchStr = '', replaceStrA = '', replaceStrB = ''):
    """
    put addition of two rotation from somewhere else onto selected using search and replace string, it wont work with duplicate names or connected rotates.
    
    ex:
    import na_AnimationConnect
    reload(na_AnimationConnect)
    #result search,  left replace, right replace,  it gives  left + right = result
    na_AnimationConnect.putAddRotateBySearchString( 'Result_', 'myA_', 'myB_' )
    """
    
    sel = cmds.ls(selection=True)
    search = searchStr
    replaceLeft = replaceStrA
    replaceRight = replaceStrB
    #search = 'TRC_1:' #that is this should be in name of our selected 
    #replace = 'TRC:'    
    
    for arg in sel:
        #only if can find a source otherwise skip
        #'TRC_1:LfFtHead'.replace('TRC_1:','TRC:')  # Result: TRC:LfFtHead # 
        sourceNameLeft = arg.replace(search,replaceLeft)
        sourceNameRight = arg.replace(search,replaceRight)
        if cmds.objExists(sourceNameLeft) and cmds.objExists(sourceNameRight):
            #print 'putting info on: %s from: %s,%s \n' %(arg,sourceNameLeft,sourceNameRight)
            ###DOING THE ADDITION HERE
            left = sourceNameLeft    #left summand
            right = sourceNameRight
            result = arg
            attrArray = ['rotate'] #the attr to be added, could use: translate
            
            addNode = cmds.createNode('plusMinusAverage')
            #connectAttr -f locator2.translate myPlus2.input3D[0];
            cmds.connectAttr( left+'.'+attrArray[0], addNode+'.'+'input3D[0]', force = True )
            cmds.connectAttr( right+'.'+attrArray[0], addNode+'.'+'input3D[1]', force = True )
            
            #make result happy
            #connectAttr -f myPlus.output3D pCone1.rotate;
            cmds.connectAttr( addNode+'.'+'output3D', result+'.'+attrArray[0], force = True )
            ###
        else:
            print 'skipping: %s, cannot find sources: %s, %s\n' %(arg,sourceNameLeft,sourceNameRight)
  
            

def putRotateConnectionBySearchString(searchStr = '', replaceStr = '', channel = ['rotateX','rotateY','rotateZ']):
    """
    puts rotate connections from somewhere else onto selected using search and replace string, it wont work with duplicate names.
    it wont work with source having different local axis than selected. it supports flexibility what channel to connect
    """
    
    sel = cmds.ls(selection=True)
    search = searchStr
    replace = replaceStr
    #search = 'TRC_1:' #that is this should be in name of our selected 
    #replace = 'TRC:'    
    
    for arg in sel:
        #only if can find a source otherwise skip
        #'TRC_1:LfFtHead'.replace('TRC_1:','TRC:')  # Result: TRC:LfFtHead # 
        sourceName = arg.replace(search,replace)
        if cmds.objExists(sourceName):
            #print 'putting info on: %s from: %s\n' %(arg,sourceName)
            for ch in channel:
                try:
                    cmds.connectAttr( sourceName+'.'+ch, arg+'.'+ch )
                except RuntimeError:
                    print 'Error putting info on: %s from: %s, using: %s\n' %(arg,sourceName,ch)
        else:
            print 'skipping: %s, cannot find source: %s\n' %(arg,sourceName)
            

            
def putPosBySearchString(searchStr = '', replaceStr = ''):
    """
    puts local translates from somewhere else onto selected using search and replace string, it wont work with duplicate names.
    it uses world space positions.
    """
    
    sel = cmds.ls(selection=True)
    search = searchStr
    replace = replaceStr
    #search = 'TRC_1:' #that is this should be in name of our selected 
    #replace = 'TRC:'    
    
    for arg in sel:
        #only if can find a source otherwise skip
        #'TRC_1:LfFtHead'.replace('TRC_1:','TRC:')  # Result: TRC:LfFtHead # 
        sourceName = arg.replace(search,replace)
        if cmds.objExists(sourceName):
            t = []
            t = cmds.xform(sourceName,query=True,ws=True,translation=True)
            #print 'putting info on: %s from: %s\n' %(arg,sourceName)
            cmds.xform( arg, translation = t, ws = True)
        else:
            print 'skipping: %s, cannot find source: %s\n' %(arg,sourceName)
            
                    
##
def putLocalScaleAndTranslateOnSelected():
    """
    put local info onto all but last selected (info: scale and translate)
    """
    
    sel = cmds.ls(selection=True)
    
    argList = sel[:-1]
    lastSelected = sel[-1]
    
    t = cmds.xform(lastSelected,query=True,ws=False,translation=True)
    s = cmds.xform(lastSelected,query=True,os=True,scale=True)
    
    for arg in argList:
        print 'putting info on: %s from: %s\n' %(arg,lastSelected)
        cmds.xform( arg, translation = t, ws = False)
        cmds.xform( arg, scale = s, os = True)
        
    
##            
def na_orientByNameSpace(nameSpaceDriver = '_13_asExport', nameSpace = '_13_asExport1'):
    """Given selection and two namespace get one thing to follow other via rotation. useful for getting mocap data and setdriven keys to work by having local channel info on joints that can talk with driven keys."""
    sel = []
    sel = cmds.ls(selection = True)
    
    for arg in sel:          
        if arg.startswith(nameSpaceDriver) or arg.startswith(nameSpace):
            #objStart = "_13_asExport1:l_wrist"
            objStart = arg
            
            ### all this stuff is to convert our selection into something we can use
            objDriver = ''
            obj = ''
            objNoNameSpace = ''
            
            if objStart.startswith(nameSpaceDriver):
                objNoNameSpace = objStart[(len(nameSpaceDriver)+2):] #plus for semicolon
            elif objStart.startswith(nameSpace):
                objNoNameSpace = objStart[(len(nameSpace)+2):]
             
            objDriver = nameSpaceDriver+':'+objNoNameSpace
            obj = nameSpace+':'+objNoNameSpace
            ###
            
            if cmds.objExists(objDriver) & cmds.objExists(obj):
                cmds.orientConstraint(objDriver,obj, mo=True, weight = 1)
                #does not clean up if constraint already exists
            else:
                print 'Warning <<< Skipping %s, cannot find on Scene, check naming namespaces' %(arg)
        else:
            print 'Warning <<< Skipping %s, it does not have a valid name space' %(arg)
          
