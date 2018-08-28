import maya.cmds as cmds
RELOFFSET = None

class relOffset(object):
    def __init__(self, targetObj, relativeObjs):
        self.targetObj = targetObj
        self.relativeObjs = relativeObjs
        self.objLocators = {}
        self.locatorConstraints = []

    # gets the world transform of any object passed in and returns the world translate and rotation
    def getWorldTransforms(self, obj):
        print 'getting world transforms'
        objWT = cmds.xform(obj, q=True, t=True, ws=True)
        objWO = cmds.xform(obj, q=True, ro=True, ws=True)

        return objWT, objWO

    # moves an objects world translate and rotate based on the stored world transforms
    def pasteWorldTrans(self, obj, objWT, objWO):
        print 'pasting world transforms'
        cmds.xform(obj, t=objWT, ws=True)
        cmds.xform(obj, ro=objWO, ws=True)

    # creates a locator and matches the objects translation and rotation
    def createLocator(self, objA):
        print 'creating space locator'
        objA_loc = cmds.spaceLocator(p=(0, 0, 0), name=objA + '_location')
        objA_pc = cmds.parentConstraint(objA, objA_loc, mo=False)

        self.objLocators[objA] = objA_loc
        self.locatorConstraints.append(objA_pc[0])

    def checkScene(self):
        if len(self.objLocators) != 0:
            print 'deleting ' + self.previousTarget + '_location'
            cmds.delete(self.objLocators[self.previousTarget + '_location'])
        else:
            pass

    # loops through selection and creates locators at the location of each objects and parents the reletive locators to
    # the target locator
    def copyLocation(self):
        print 'copying location'
        self.checkScene()
        self.previousTarget = self.targetObj
        self.createLocator(self.targetObj)

        for i in self.relativeObjs:
            print 'creating locator for ' + i
            self.createLocator(i)
            cmds.parent(self.objLocators[i], self.objLocators[self.targetObj])

        cmds.delete(self.locatorConstraints[1::])

    # loops through the relative objects and gets the relative locators transforms and transfers the data to the
    # relative objects
    def pasteLocation(self):
        print 'pasting location'
        for i in self.relativeObjs:
            objWT, objWO = self.getWorldTransforms(self.objLocators[i])
            self.pasteWorldTrans(i, objWT, objWO)

def copyPos():
    global RELOFFSET

    selection = cmds.ls(sl=True)
    RELOFFSET = relOffset(selection[0], selection[1::])
    RELOFFSET.copyLocation()

def pastePos():
    global RELOFFSET

    if RELOFFSET == None:
        cmds.inViewMessage(message='No previous copy data')
    else:
        RELOFFSET.pasteLocation()

copyPos()
pastePos()