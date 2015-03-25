#updated 11-11-2014 nate --- initial release
#created 11-11-2014 nate

"""
Why? Fingers and Toes.  all the junctions between fingers could be almost 15*2 clicks per finger.  With tool its about 3 clicks for user per finger.  12 instead of 120 clicks is a major saving. (Works with looping fingers/toes which is mostly expected for rigging, works if there is just one side missing so can loop around finger)


user

click right on border edge to select all border edge,deselect edges dont want to close should be one window drag of all non top edges, click on tool (it should close all faces --looping selected edge (up), pickwalk up get end, using append tool to close face)

algorithm:

loop selected expanded e
	find top edge --easy
	find bottom edge 
		clean selection
		find all edge "parallel or around the edge in direction want to close"
		find end edge of the "around edges", this is the bottom edge 
	draw face between them
cleanup

"""


import maya.cmds as cmds
import maya.mel as mel #for polyAppend multiple edges
import re #for getting ids of edge

def na_closeFaceFromSelectedEdge():
    
    """
    close face from selected poly edge, multi edge selection all horiz or all vertical
    """
    
    sel = cmds.ls(selection=True)
    
    if len(sel) > 0:
        topEdges = cmds.filterExpand( sm=(32) )
        poly = topEdges[0].split('.')[0]  #removed the .e to get poly name
        polyShape = cmds.pickWalk(poly, direction = 'down') #assumes this is the right shape
        print "Start Computing Closing for >>> poly: %s shape: %s\n" %(poly,polyShape)

        for e in topEdges:
            topE = e
            topE_index = int(re.search(re.escape('[')+"(.*)"+re.escape(']'),topE).group(1))
            #polySelect -edgeRing 41;
            bottomE_index = cmds.polySelect(poly,edgeRing = topE_index )[-1] #the last thing of the edgering
            #this keeps the order which is why using this over pickWalk
            
            """oldstuff
            #find all edge around top edge in direction want to close
            #cmds.pickWalk(topE, direction = 'up', type = 'edgering')
            #aroundEdges = cmds.filterExpand( sm=(32) )
            bottomE = aroundEdges[-1]
            #print "top: %s, bot: %s" %(topE,bottomE)
            
            bottomE_index = re.search(re.escape('[')+"(.*)"+re.escape(']'),bottomE).group(1)
            """
            print "top: %s, bot: %s" %(topE_index,bottomE_index )
            
            #polyAppend -ch on -s 1 -tx 1 -ed 44 -ed 43 polySurfaceShape20
            mel.eval('polyAppend -ch on -s 1 -tx 1 -ed %s -ed %s %s;' %(topE_index,bottomE_index,polyShape[0]) )
        
        
        #cleanup so no duplicate edges
        cmds.select(poly,replace=True)
        cmds.polySewEdge()
        #cleanup so no history
        cmds.delete(poly, ch = True )
        
    else:
        print "Requires one or more edges selected. multi edge selection all horiz or all vertical\n"