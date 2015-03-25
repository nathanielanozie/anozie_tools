##@file na_dataType.py Add function parameter (list or string) flexibility
#@author Nathaniel Anozie
#


from types import*

##get argument string or unicode as string list
#@param objects  a string, string list, or unicode list
#@pre given any of valid types
#@post list of strings
#@author Nathaniel Anozie
#@bug changes float or ints to string
def getArgStringAsList( objects = [] ):
    result = []
    
    if type(objects) is not ListType:
        if type(objects) is StringType:
            objects = [objects]
        elif type(objects) is UnicodeType:
            objects = [str(objects)]
            
        result = objects
    else:
        for i in range(len(objects)):
            result.append( str(objects[i]) )
            
    return result
    
def getArgStringAsList_unitTest():
    print getArgStringAsList(['ab','cd'])
    print getArgStringAsList('ab')
