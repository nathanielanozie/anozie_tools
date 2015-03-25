#na_follow.py copy and paste what it shows here to begin getting our thing to move
#
#@author Nathaniel Anozie
#
##

#modify at own risk

#last updated: 04/18/2014-04/22/2014 -- initial release, fixed a grouping bug

#how to use
#na_follow()        --  select driver then driven then copy and paste result of this to begin getting our thing to move
#na_unFollow()      --  select driver then driven then copy and paste result of this to stop getting our thing to move



import maya.cmds as cmds
import sys
def na_follow():
	"""given driver and driven selected in that order print command to create 3 groupings to be used with external driver rig"""
	suffix_grpInDeformation = "_naMocapGrp" #these 3 names should be unique but can be whatever you like
	suffix_grpInMocap = "_naMocap"
	suffix_grpDeformationDriver = "_naMocapDrv"

	allSel = []
	allSel = cmds.ls(selection=True) #note if two things are named the same but in different hierarchies this tool may not work
	
	if len(allSel) != 2:
		sys.exit("Requires driver (ex:mocap) then driven selected")

	driver = allSel[0]
	object = allSel[1]

	#print " leave in deformation rig >> %s\n parent to mocap/driver rig joint >> %s\n parent constrain to group on selection >> %s\n" %(suffix_grpInDeformation,suffix_grpInMocap,suffix_grpDeformationDriver)


	#start printing to command line the command
	print "#start COPY >>>>>>>>>>"
	print "import maya.cmds as cmds"
	print "object = '%s'" %(object)
	print "driver = '%s'" %(driver)
	print "suffix_grpInDeformation = '%s'" %(suffix_grpInDeformation)
	print "suffix_grpInMocap = '%s'" %(suffix_grpInMocap)
	print "suffix_grpDeformationDriver = '%s'" %(suffix_grpDeformationDriver)

	otherCmdA = """
	#pivoting and grouping
	positionToMove = cmds.xform(object, q=True, translation = True, ws = True) 
	#grpInDeformation = cmds.group(object)
	grpInDeformation = cmds.group(empty = True)
	#do parenting of created group
	parentObject = []
	parentObject = cmds.listRelatives(object, parent = True)
	"""
	ifCmd = """
if parentObject is not None:
    cmds.parent(grpInDeformation, parentObject[0])
    """	
	otherCmdB = """
	cmds.makeIdentity(grpInDeformation, t = True, r = True, s = True, n = False, apply = True)
	cmds.parent(object, grpInDeformation)
	cmds.move( positionToMove[0],positionToMove[1],positionToMove[2], grpInDeformation+'.rotatePivot', absolute = True  )
	cmds.move( positionToMove[0],positionToMove[1],positionToMove[2], grpInDeformation+'.scalePivot', absolute = True  )
	grpInMocap = cmds.duplicate( grpInDeformation,parentOnly=True )
	grpDeformationDriver = cmds.duplicate( grpInDeformation,parentOnly=True  )
	cmds.parent(grpDeformationDriver,grpInMocap) #needs to be done before renaming

	#naming, for duplicate named things in outliner may need to do more work here
	name_grpInDeformation = object+suffix_grpInDeformation
	name_grpInMocap = object+suffix_grpInMocap
	name_grpDeformationDriver = object+suffix_grpDeformationDriver

	cmds.rename(grpInDeformation,name_grpInDeformation)
	cmds.rename(grpInMocap,name_grpInMocap)
	cmds.rename(grpDeformationDriver,name_grpDeformationDriver)

	#constraining things and doing parenting so our thing moves
	cnt = cmds.parentConstraint(name_grpDeformationDriver,name_grpInDeformation, mo = 1)
	cmds.parent(name_grpInMocap, driver)
	"""	
	#strip leading tabs for all lines to print
	for l in otherCmdA.splitlines():
		print l.lstrip()
	print ifCmd
	for l in otherCmdB.splitlines():
		print l.lstrip()		
	print "#END COPY >>>>>>>>>>"

	
#copy and paste what it shows here to begin getting our thing not to move
def na_unFollow():
	"""given driver and driven selected in that order print command to undo the created 3 groupings and movement to be used with external driver rig.  it should put us back at the pose we started with initially on our character. copy and paste what it shows here to begin getting our thing not to move"""
	suffix_grpInDeformation = "_naMocapGrp" #these 3 names should be unique but can be whatever you like but needs to be same as installation
	suffix_grpInMocap = "_naMocap"
	suffix_grpDeformationDriver = "_naMocapDrv"

	allSel = []
	allSel = cmds.ls(selection=True) #note if two things are named the same but in different hierarchies this tool may not work
	
	if len(allSel) != 2:
		sys.exit("Requires driver (ex:mocap) then driven selected")

	driver = allSel[0]
	object = allSel[1]

	#print " leave in deformation rig >> %s\n parent to mocap/driver rig joint >> %s\n parent constrain to group on selection >> %s\n" %(suffix_grpInDeformation,suffix_grpInMocap,suffix_grpDeformationDriver)


	#start printing to command line the command
	print "#start COPY >>>>>>>>>>"
	print "import maya.cmds as cmds"
	print "object = '%s'" %(object)
	print "driver = '%s'" %(driver)
	print "suffix_grpInDeformation = '%s'" %(suffix_grpInDeformation)
	print "suffix_grpInMocap = '%s'" %(suffix_grpInMocap)
	print "suffix_grpDeformationDriver = '%s'" %(suffix_grpDeformationDriver)

	otherCmd = """

	#naming, for duplicate named things in outliner may need to do more work here
	name_grpInDeformation = object+suffix_grpInDeformation
	name_grpInMocap = object+suffix_grpInMocap

	#make our thing not move, this probably wont work if two things have same name in dag
	#can either parent to the world or parent to the parent of our thing
	parent_name_grpInDeformation = cmds.listRelatives( name_grpInDeformation, parent = True)

	#do cleaning , break t,r connections	
	cmds.delete(name_grpInMocap)	
	#set grp translation to zero
	cmds.setAttr(name_grpInDeformation+'.'+'translateX',0.0)
	cmds.setAttr(name_grpInDeformation+'.'+'translateY',0.0)
	cmds.setAttr(name_grpInDeformation+'.'+'translateZ',0.0)
	cmds.setAttr(name_grpInDeformation+'.'+'rotateX',0.0)
	cmds.setAttr(name_grpInDeformation+'.'+'rotateY',0.0)
	cmds.setAttr(name_grpInDeformation+'.'+'rotateZ',0.0)
	"""
	ifCmd = """
if parent_name_grpInDeformation is None:
	cmds.parent(object, world = True)
		
else:
	cmds.parent(object, parent_name_grpInDeformation[0])
cmds.delete(name_grpInDeformation)
	"""
		
	#strip leading tabs for all lines to print
	for l in otherCmd.splitlines():
		print l.lstrip()
	print ifCmd+"\n"+"#END COPY >>>>>>>>>>"





