##@file na_duplicatejointAttributeOnNode.py
#
#Duplicate joint Attribute On Node (Tested Maya 2008)
#
#@author Nathaniel Anozie
#
#@note inspired by Hamish Mckenzie (macaronikazoo) for learning about for zip in python to operate on multiple lists
#simultaneously
#
#@defgroup joint Joint editing tools
#@{
#ex: use blend color to Connect translate, rotate attributes between fk chain and result chain
#
##

import maya.cmds as cmds

def jointAttributeOnNode_unitTest():
    j1=cmds.joint(p=[0,4,0])
    cmds.select(clear=True)
    j2=cmds.joint(p=[0,3,0])
   
    jointAttributeOnNode(result=[j2], joint1=[j1], nameBlend=['myNode'])

def jointAttributeOnNode_unitTest_1():
    j1=cmds.joint(p=[0,4,0])
    j2=cmds.joint(p=[1,4,0])
    cmds.select(clear=True)
    j3=cmds.joint(p=[0,4,0])
    j4=cmds.joint(p=[1,4,0])
    cmds.select(clear=True)
    r1=cmds.joint(p=[0,4,0])
    r2=cmds.joint(p=[1,4,0])
    
    cmds.select(clear=True)
    jointAttributeOnNode(result=[r1,r2], joint1=[j1,j2], joint2=[j3,j4], nameBlend=['r1Node','r2Node'],isTwoChain=True)
    
##get two joint chains to feed information to a third result joint chain of same length
#@note it will create needed blend color nodes
#@note it defaults to connect only joint1
#@param isTranslate = True should we connect translation to result
#@param isRotate = True  should we connect rotation to result
#@param result=[] this is required result joint chain
#@param joint1=[] this is required first joint chain
#@param joint2=[] this is optional second joint chain
#@param nameBlend=[] what should the prefix of backend node be
#@param isTwoChain = False should we connect to joint chains 
##
def jointAttributeOnNode(isTranslate = True, isRotate = True, result=[], joint1=[], joint2=[], nameBlend=[], isTwoChain = False):
    
    status = 1 #default its okay to start running code
 
            
    #node names
    tSuffix = "_tBlend"
    nameBlendTranslate = map( lambda x: x+tSuffix, nameBlend)
    rSuffix = "_rBlend"
    nameBlendRotate = map( lambda x: x+rSuffix, nameBlend)
    
    if isTwoChain == False:
        status = errorCheck(isExist=True, isDontExist=True, isLength=True, isType=True, exist=[result,joint1], dontExist=[nameBlendTranslate+nameBlendRotate],
        sameLength=[result,joint1,nameBlend],sameType=[result+joint1],type='joint')        
    else:
        status = errorCheck(isExist=True, isDontExist=True, isLength=True, isType=True, exist=[result,joint1,joint2], dontExist=[nameBlendTranslate+nameBlendRotate],
        sameLength=[result,joint1,joint2,nameBlend],sameType=[result+joint1+joint2],type='joint')  
   
        
    if status == 1:
        if isTranslate:
            nodeArray = []
            for i in range(len(nameBlend)):    
                backend = nameBlendTranslate[i]
                node = cmds.createNode('blendColors', name=backend)
                nodeArray.append(node) 
            #if we were connecting two sets of joints to result add a similar line to
            #this below with isColor1=False
            duplicatejointAttributeOnNode(isTranslate = True, result=result, joint=joint1, nameBlend=nodeArray, isColor1=True) 
            if isTwoChain:
                duplicatejointAttributeOnNode(isTranslate = True, result=result, joint=joint2, nameBlend=nodeArray, isColor1=False)
             
        print isRotate
        print 'Great Day\n'    
        if isRotate:
            nodeArray = []
            for i in range(len(nameBlend)):    
                backend = nameBlendRotate[i]
                node = cmds.createNode('blendColors', name=backend)
                nodeArray.append(node)
            #add similar line if connecting two joints
            print nodeArray
            print 'Great Day\n'
            duplicatejointAttributeOnNode(isTranslate = False, result=result, joint=joint1, nameBlend=nodeArray, isColor1=True)
            if isTwoChain:
                duplicatejointAttributeOnNode(isTranslate = False, result=result, joint=joint2, nameBlend=nodeArray, isColor1=False)            
            
            

##put translate or rotate of joint as input into a blend colors color 1 or color 2 attribute
#@note requires result joint chain and one another joint chain which can feed its attribute to the result
#@note does not create blend color nodes
##
def duplicatejointAttributeOnNode(isTranslate = True, result=[], joint=[], nameBlend=[], isColor1=True ):

    status = 1 #default its okay to start running code
    print 'performing input checking...\n'
    status = errorCheck(isExist=True, isLength=True, isType=True, exist=[result,joint,nameBlend],
    sameLength=[result,joint,nameBlend],sameType=[result+joint],type='joint')    
    if status == 1:
        status = errorCheck(isType=True,sameType=[nameBlend],type='blendColors') 
            
    #check exist joint, result, all must exist
    """
    if getExist( [result,joint,nameBlend] ) == 0:
        print 'Requires Input Exist\n'
        status = 0
    
    #check for identical length in result, joint, and nodes
    if getSameLen( [result,joint,nameBlend] ) == 0:
        print 'Requires Input Same Length\n'
        status = 0

    #check node type blend color. all must be blend color
    if getType( [nameBlend],type='blendColors') == 0:
        print 'Requires BlendColor Input\n'
        status = 0
        
    #check for node type joint in joint, result.  all must be joint
    if getType( [result+joint] ,type='joint') == 0:
        print 'Requires Joint Input\n'
        status = 0
    """
    
    if status == 1:
        print 'completed input checking...\n computing result\n'
        
        #bug only working on one index
        for i in range(len(result)):
            duplicatejointAttributeOnNodeByJoint( isTranslate = isTranslate, result=result, joint=joint, nameBlend=nameBlend, isColor1=isColor1, jointIndex=i)
        
        
        print 'completed result\n'

        
        
##put translate or rotate of joint as input into a blend colors color 1 or color 2 attribute
#@note requires jointIndex of which joints to connect
#@note does not create blend color nodes
##        
def duplicatejointAttributeOnNodeByJoint( isTranslate = True, result=[], joint=[], nameBlend=[], isColor1=True, jointIndex=0):
    fromAttribute = []
    toAttribute = [] 
    
    if isTranslate:
        fromAttribute = ['translateX','translateY','translateZ'] #all for one joint index
    else:
        fromAttribute = ['rotateX','rotateY','rotateZ']
        

    if isColor1:
        toAttribute = 'color1'
    else:
        toAttribute = 'color2'
             
    fromObject = joint[jointIndex]
    fromPlug = map( lambda x: fromObject+'.'+x, fromAttribute)
    node = nameBlend[jointIndex]
    blendAttribute = ['R','G','B']
    toPlug = map( lambda x: node+'.'+toAttribute+x, blendAttribute )
    for x, y in zip( fromPlug, toPlug ):
        #its okay for the to plug to send info out but it wont be modified if it has anything coming in
        statusAttribute = cmds.listConnections(y,source=True,destination=False)
        if statusAttribute is None:
            cmds.connectAttr(x,y)  

    fromResultPlug = []
    toResultPlug = []
    #bug when this is called but they are already connected
    fromResultPlug = map( lambda x: node+'.'+'output'+x, blendAttribute )
    toResultPlug = map( lambda x: result[jointIndex]+'.'+x, fromAttribute)
    for x, y in zip( fromResultPlug,toResultPlug ):
        print x+' '+y+'\n'
        statusAttribute = cmds.listConnections(y,source=True,destination=False)
        if statusAttribute is None:
            cmds.connectAttr(x,y)  
  
    #optional make color1 controlling result,0.0 would be for color2
    cmds.setAttr(node+'.'+'blender',1.0)
    
    
    
def duplicatejointAttributeOnNode_unitTest():
    j1=cmds.joint(p=[0,4,0])
    cmds.select(clear=True)
    j2=cmds.joint(p=[0,3,0])
    
    backend = j2+'_'+'blendNd'
    node = cmds.createNode('blendColors',name=backend)
    duplicatejointAttributeOnNode(result=[j2], joint=[j1], nameBlend=[node])

    
def duplicatejointAttributeOnNode_unitTest_1():
    j1=cmds.joint(p=[0,4,0])
    cmds.select(clear=True)
    j2=cmds.joint(p=[0,3,0])
    
    backend = j2+'_'+'blendNd'
    node = cmds.createNode('blendColors',name=backend)
    duplicatejointAttributeOnNode(isTranslate = True, result=[j2], joint=[j1], nameBlend=[node], isColor1=True)
    duplicatejointAttributeOnNode(isTranslate = False, result=[j2], joint=[j1], nameBlend=[node], isColor1=False)
    
def duplicatejointAttributeOnNode_unitTest_2():
    j1=cmds.joint(p=[0,4,0])
    cmds.select(clear=True)
    j2=cmds.joint(p=[0,3,0])
    
    duplicatejointAttributeOnNode(result=[j2], joint=[j1], nameBlend=[])        
        
def duplicatejointAttributeOnNode_unitTest_3():
    j1=cmds.joint(p=[0,4,0])
    cmds.select(clear=True)
    j2=cmds.joint(p=[0,3,0])
    
    backend = j2+'_'+'blendNd'
    node = cmds.createNode('blendColors',name=backend)
    duplicatejointAttributeOnNode(result=[j2], nameBlend=[node])
    
def duplicatejointAttributeOnNode_unitTest_4():
    j1=cmds.joint(p=[0,4,0])
    cmds.select(clear=True)
    j2=cmds.joint(p=[0,3,0])
    cmds.select(clear=True)
    j3=cmds.joint(p=[0,3,0])
    
    backend = j2+'_'+'blendNd'
    node = cmds.createNode('blendColors',name=backend)
    duplicatejointAttributeOnNode(result=[j2], joint=[j1,j3], nameBlend=[node])    
##
#@}
##



















##given list of lists have options to do exist same length and type check, get 1 if success 0 otherwise
#@note defaults to not checking any
##
def errorCheck(isExist=False, isDontExist=False, isLength=False, isType=False, exist=[],dontExist=[],sameLength=[],sameType=[],type=''):
    
    #check exist, all must exist
    if isExist:
        if getExist( exist ) == 0:
            print 'Requires Input Exist\n'
            return(0)
            
    #check exist, all must not exist
    if isDontExist:
        if getDontExist( dontExist ) == 0:
            print 'Requires Input Dont Exist\n'
            return(0)
        
    #check for identical length in result, joint, and nodes
    if isLength:
        if getSameLen( sameLength ) == 0:
            print 'Requires Input Same Length\n'
            return(0)
        
    #check for node type all must be same type
    if isType:
        if getType( sameType ,type=type) == 0:
            print 'Requires Joint Input\n'
            return(0)
        
    return 1
    
    




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
    
