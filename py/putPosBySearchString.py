import maya.cmds as cmds

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