#na_orientByNameSpace.py get local rotation info on a skeleton
#
#@author Nathaniel Anozie
#
##

#modify at own risk

#last updated: 04/23/2014-04/23/2014 -- initial release

#how to use
#na_orientByNameSpace()        --  put in driver and thing want to move name spaces.  select everything want to possible get to have local rotation information



import maya.cmds as cmds

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
          
