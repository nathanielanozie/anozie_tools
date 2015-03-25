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