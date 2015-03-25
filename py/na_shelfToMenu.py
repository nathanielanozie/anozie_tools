"""
# na_shelfToMenu.py
#
#By
#
#Nathaniel O. Anozie
#www.nathananozie.blogspot.com
#
#
#Inspired by
#Brian Ewert (http://ewertb.soundlinker.com)  learning about working with shelves from his online tutorials 
#David Keegan (http://davidkeegan.com) learning about working with shelves from his online tutorials 
#Markus Jarderot (mizardx.blogspot.com) learning about some string operations in python
"""

#last updated: 11-24-2014       initial release

import maya.cmds as cmds

def na_shelfToMenu( shelf = '', shelfButtonList = ['']):
    """
    get menu item command, given a shelf, and imageOverlayLabel list (icon names)
    assumes each line can be run with command (no procs/loops etc in shelf that take more than one line)
    
    shelf = 'naModeling'
    shelfButtonList = ['origin', 'jnX', 'cPiv', 'cube', 'sew' ] #note it skips if cannot find name
    """
    
    if cmds.shelfLayout( shelf, q = True, exists = True):
        #need to make sure shelf is a shelve and exists
        #need to make sure it has buttons
        allButton = cmds.shelfLayout( shelf, q = True, childArray = True)
        
        for arg in allButton:
            name = cmds.shelfButton(arg, q = True,  imageOverlayLabel = True) 
            #a = list( set( ['great','day', 'wonderful'] ).intersection( set(  ['wonder'] ) ) )
            #print len(a) #0 means no intersection
            intersect = list( set( shelfButtonList ).intersection( set(  [name] ) ) )
            if len(intersect) != 0:
                #print "Great Calculating menuItem for: %s\n" %name
                
                ###command
                uneditCmd = cmds.shelfButton(arg, q = True,  command = True) 
                #putting a semicolon for new line
                #joining all lines into one
                uneditCmdB = ";".join(  uneditCmd.split("\n")  )	#not checking whether starting with semicolon
                uneditCmdB = uneditCmdB.rstrip()#assuming can remove trailling new line
                
                #menuitem cmd
                description = cmds.shelfButton(arg, q = True,  label = True) 
                c_cmd = 'menuItem -l (\"%s\") -c (\"%s\") -ann (\"%s\")' %(name,uneditCmdB,description)
                print c_cmd