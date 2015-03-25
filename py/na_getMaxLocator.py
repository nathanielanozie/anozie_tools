#author: Nathaniel Anozie (ogbonnawork at gmail dot com)
#
#Inspired by Martijn Pieters -- learning about joining list from his online tutorials
#Inspired by Patrick Westerhoff -- learning about unique list from his online tutorials
#modify at own risk

# updated 08-15-2014 nate ----- initial commit

import maya.cmds as cmds

def na_getMaxLocator():
    """
    get largest integer of locator, useful when making quick animator controls and dont want to overlap with any so far
    """
    result = []
    for _arg in cmds.ls("*locatorShape*"): #using shape so get hopefully one thing per locator, this wont work with referenced things
        
        #arg = 'eyeLid_TECH|r_locator1|r_locatorShape1'
        #print _arg
        
        arg = ''
        arg = _arg.split('|')[-1] #if argument like eyeLid_TECH|r_locator1|r_locatorShape1 just use the end part
        digits = [int(x) for x in arg if x.isdigit()]
        if len(digits) > 0:
            #digit = digits[0]
            digit = ''
            digit = ''.join(str(e) for e in digits) #puts list like [2,5] into '25'
            result.append( int(digit) ) #so can sort it
        else:
            pass
    result = list(set(result)) #remove duplicates
    result.sort()
    print "locator indexes --->"
    print result