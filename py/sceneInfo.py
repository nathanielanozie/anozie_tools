##@file sceneInfo.py
#
#Maya scene status commands (Tested Maya 2008)
#
#@author Nathaniel Anozie
#
#@note inspired by Matt Estela (tokeru dot com) for learning about node based surface constraint techniques
#
#@defgroup sceneInfo help other parts with simplyfing error checking
#@{
#ex: check existence 
##

import maya.cmds as cmds

##get if object of specified type of list of form [ ['strA','strrA'],['strB',...] ] return 1 if all items of type zero otherwise
#
##
def getType(objectArray=[],type='joint'):

    result = 1
    
    if len(objectArray) == 0:
        result = 0
    else:
        for obj in objectArray:
            isExist = map( lambda x: 1 - na_nodeType(x,type), obj)
            
            if any(isExist) or len(obj)==0:
                result = 0
                break
       
    return result

    
##given a string and a type return 0 if not of correct type or doesn't exist, 1 otherwise
#@note i made this because nodeType could give none which would give an error if was evaluated
##
def na_nodeType(obj='',type = 'joint'):
    result = 0
    value = cmds.nodeType(obj)
    if value is not None:
        result = (value == type)
    else:
        result = 0
        
    return result


##get if exists of list of form [ ['strA','strrA'],['strB',...] ] return 1 if all items exist zero otherwise
#
##
def getExist(objectArray=[]):
    result = 1

            
    if len(objectArray) == 0:
        result = 0
    else:
        for obj in objectArray:
            isExist = map( lambda x: 1 - cmds.objExists(x), obj)
            
            if any(isExist) or len(obj)==0:
                result = 0
                break
       
    return result
  

##get if all don't exist of list of form [ ['strA','strrA'],['strB',...] ] return 1 if all items dont exist zero otherwise
#
##
def getDontExist(objectArray=[]):
    result = 1
       
    if len(objectArray) == 0:
        result = 0
    else:
        for obj in objectArray:
            isExist = map( lambda x: cmds.objExists(x), obj)
            
            if any(isExist) or len(obj)==0:
                result = 0
                break
       
    return result


    
##get if same length of list of form [ ['strA','strrA'],['strB',...] ] return 1 if all items same length zero otherwise
#@note should work if given a list of form [ 'strA', 'strB',... ]
## 
def getSameLen(objectArray=[]):
    result = 1
        
    if(len(objectArray) >= 2 ):
        sz = len(objectArray[0])  

        isExist = map( lambda x: 1 - (len(x) == sz), objectArray)
        
        if any(isExist):
            result = 0
       
    return result  

