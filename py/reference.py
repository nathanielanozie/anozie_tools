##@file reference.py
#
#(Tested Maya 2008)
#
#@author Nathaniel Anozie
#
#@note Inpired By Bryan Ewert (xyz2 dot net) for learning about deferred reference node and load state
#
#
##


import os
import maya.cmds as cmds


##reference specified maya file of form .ma in a currently opened maya scene, use given namespace
#
#@note by default it will skip any non .ma files
#
##
def referenceFile( f = '/Users/noa/Desktop/temp/untitled1.ma', name = 'temp1'):

    #is file referenced
    #
    isFileReferenced = False
    """
    #this was here if didnt want to allow referencing in the same file multiple times
    #but becuasue i thought it may be helfpul to do that i commented this out
    #
    allReferencedFiles = cmds.file(query=True,reference=True)
    #using python's sets to find whether our maya file is in list of all referenced files
    if len( set(allReferencedFiles).intersection([f]) ) == 1:
        isFileReferenced = True
    """
    
    #search of file
    #
    isMayaFile = False
    isMayaFile = getIsFile(file=f,maya=True)
            
    if not isFileReferenced:
        print 'Great, looking for file >>%s since it is not referenced' %f
        if isMayaFile:
            print 'Great, referencing file >>%s' %f
            cmds.file(f,reference=True,namespace=name)
        else:
            'Requires existing .ma file to Reference >> %s' %f



##set load state of specified referenced file with option to completely remove it
#
#@note when referencing from the same file multiple times get something like
#[u'/Users/noa/Desktop/temp/untitled1.ma', u'/Users/noa/Desktop/temp/untitled1.ma{1}'] and the one with
#parenthesis needs to be fed to this
##
def setLoadOnReferencedFile( f = '/Users/noa/Desktop/temp/untitled1.ma', load = True ):
        
    #loading of file
    #    
    isLoaded = False
    
    #get loaded code
    #
    refNode = ''
    try:
        refNode = cmds.referenceQuery(f,rfn=True)
        
        #if reference node not deferred then it is loaded
        if not cmds.file(rfn = refNode, q = True, dr = True):
            isLoaded = True
        
        if (isLoaded == False) and load:
            print 'Great, loading file from unloaded state'
            cmds.file(rfn = refNode, lr = True)
        elif isLoaded and (load == False):
            print 'Great, un loading file from loaded state'
            cmds.file(rfn = refNode, ur = True)        
        
    except RuntimeError:
        print 'Requires a referenced maya file >> %s in open scene to check load status' %f
        

   
        
##remove a referenced file completely from scene (unloads and removes it)
#
##
def removeReferencedFile( f = '/Users/noa/Desktop/temp/untitled1.ma' ):        
    #loading of file
    #    
    isLoaded = False
    isMayaFile = False
    isMayaFile = getIsFile(file=f,maya=True)
    
    if isMayaFile:   
        #get loaded code
        #
        try:
            refNode = cmds.referenceQuery(f,rfn=True)
        except RuntimeError:
            print 'Requires a referenced maya file >> %s in open scene' %f
            
        #removing file from scene         
        #cmds.file(rfn = refNode, ur = True)
        cmds.file(f,removeReference = True)
    else:
        print 'Requires existing .ma file for removal>> %s' %f   
        
        
        
##get True only when file is existing and is of good type, currently only supports Maya type
#
##
def getIsFile( file = '/Users/noa/Desktop/temp/untitled1.ma', maya=True):
    mayaExt = '.ma'
    
    result = False
    
    #doing this so dont overwrite a directory or file etc
    filePath, fileName = os.path.split(file)
    
    #make sure have a maya file were writing to
    fileBaseName, fileExtension = os.path.splitext(fileName)
    
    if os.path.isdir(filePath) & (fileExtension == mayaExt):
        if os.path.isfile(file):
            print 'Great Found Maya File To Reference >> %s\n' %fileName
            result = True
            
    return result        
    
 
