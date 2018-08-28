import maya.cmds as cmds
global allSelections
global currentSelection
global trailName
global trailNamesAll
global keyAttribs
global dictCheck
keyAttribs = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ']

def setVariables():
    global allSelections
    global trailNamesAll
    global dictCheck
    try:
        allSelections
    except NameError:
        allSelections = {}
        trailNamesAll = []
        dictCheck = {}
    else:
        addCurrentSelection()

def addCurrentSelection():
    global allSelections 
    global currentSelection
    global trailName
    global trailNamesAll
    global keyAttribs
    global dictCheck
    #allSelections = {}
    #trailNamesAll = []
    #dictCheck = {}
    currentSelection = cmds.ls(sl=True)
    #if currentSelection in allSelections.keys():
        #print "already in all selections list"
        #print "this is where to toggle vis"
    #else:
    if checkIfRedo() == False:
        print "adding the new selection to all selections list"
        allKeys = cmds.keyframe( currentSelection, attribute=keyAttribs, query=True )
        amountKeys = len(allKeys)
        nameKey=''.join(currentSelection)
        allSelections[nameKey] = amountKeys
        startFrame = allKeys[0]
        endFrame = allKeys[-1]
        cmds.snapshot( currentSelection, constructionHistory=True, startTime=startFrame, endTime=endFrame, increment=1 , u= "animCurve", mt=True)
        print allSelections
    else: 
        print "that item has not been changed"
        visTrailName = cmds.listConnections(currentSelection, t= "motionTrail")
        visTrailNameHandle= cmds.listConnections(visTrailName[0], t="shape")
        print visTrailNameHandle[0]
        if cmds.getAttr(visTrailNameHandle[0] + ".visibility") == 0:
            cmds.setAttr(visTrailNameHandle[0] + ".visibility", 1)
            
        elif cmds.getAttr(visTrailNameHandle[0] + ".visibility") == 1:
            cmds.setAttr(visTrailNameHandle[0] + ".visibility", 0)
            
def checkIfRedo():
    global currentSelection
    global keyAttribs
    global allSelections
    global dictCheck
    global trailNamesAll
    shared_items = None
    currentSelection = cmds.ls(sl=True)
    allNamesCheck = ''.join(currentSelection)
    allKeysCheck = cmds.keyframe( currentSelection, attribute=keyAttribs, query=True )
    amountAllKeysCheck = len(allKeysCheck)
    dictCheck[allNamesCheck] = amountAllKeysCheck
    shared_items = set(dictCheck.items()) ^ set(allSelections.items())
    print dictCheck
    if len(shared_items) != 0:
        trailName = cmds.listConnections(currentSelection, t= "motionTrail")
        if trailName == None:
            return False
        else:
            trailNameHandle= cmds.listConnections(trailName[0], t="shape")
            cmds.delete(trailNameHandle[0])
            return False
    else:
        return True
        

setVariables()

