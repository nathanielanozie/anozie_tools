##@file getFile.py
#
#(Tested Maya 2008)
#
#@author Nathaniel Anozie
#
##

##given a directory print all the maya files, note it will look in all sub directories of that directory to
#
#@note inspired by Alex Martelli's example on recursive file searching aleax dot it
#
##
def getAllFileInDirectory(d = '/Users/noa/Desktop/temp', ext = '*.ma'):
    import os,fnmatch

    #hold all the file names
    result = []
    
    if os.path.isdir(d):
        print 'Great Found Directory >> %s\n' %d
        
        #files = os.listdir(d)
        for base, dirs, files in os.walk(d):
            
            #print good files only, files with proper extension
            mayaFiles = fnmatch.filter( files, ext )
            
            #add a good files to result
            result.extend(  os.path.join(base,f) for f in mayaFiles  )
            
    else:
        print 'Requires Directory >> %s' %d   
    
    return result

