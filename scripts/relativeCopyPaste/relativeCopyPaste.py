# script: relativeCopyPaste.py
# scripted by: Linh Nguyen
# description: Copies the relative offset between one object and a series of other objects
# and allows to paste that difference

import maya.cmds as cmds

R_OFFSET = None

class relativeOffset(object):

    def __init__(self, targetObj, relativeObjs):
        self.targetObj = targetObj
        self.relativeObjs = relativeObjs
        self.objectOffsets = {}

    def getDifference(self, objectA, objectB):
        print 'calculates the difference between two objects'
        offsets = {}

        objectAT = list(cmds.getAttr(objectA + '.translate'))
        objectAO = list(cmds.getAttr(objectA + '.rotate'))

        objectBT = list(cmds.getAttr(objectB + '.translate'))
        objectBO = list(cmds.getAttr(objectB + '.rotate'))

        translateOffset = [(objectAT[0][0] - objectBT[0][0]),
                           (objectAT[0][1] - objectBT[0][1]),
                           (objectAT[0][2] - objectBT[0][2])]
        rotateOffset = [(objectAO[0][0] - objectBO[0][0]),
                        (objectAO[0][1] - objectBO[0][1]),
                        (objectAO[0][2] - objectBO[0][2])]
        offsets['translate'] = translateOffset
        offsets['rotate'] = rotateOffset

        return offsets

    def validateData(self):
        if len(self.relativeObjs) == 0:
            cmds.invViewMessage(message='No previous offset data', pos = 'midCenter', fade=True)
            return False
        else:
            return True

    def copyPosition(self):
        for i in self.relativeObjs:
            objOffset = self.getDifference(self.targetObj,i)
            self.objectOffsets[i] = objOffset
        return self.objectOffsets

    def pasteOffsets(self):
        validation = self.validateData()
        if validation:
            for i in self.relativeObjs:
                targetT = cmds.getAttr(self.targetObj + '.translate')
                targetO = cmds.getAttr(self.targetObj + '.rotate')

                cmds.setAttr(i + '.translateX', targetT[0][0] - self.objectOffsets[i]['translate'][0])
                cmds.setAttr(i + '.translateY', targetT[0][1] - self.objectOffsets[i]['translate'][1])
                cmds.setAttr(i + '.translateZ', targetT[0][2] - self.objectOffsets[i]['translate'][2])

                cmds.setAttr(i + '.rotateX', targetO[0][0] - self.objectOffsets[i]['rotate'][0])
                cmds.setAttr(i + '.rotateY', targetO[0][1] - self.objectOffsets[i]['rotate'][1])
                cmds.setAttr(i + '.rotateZ', targetO[0][2] - self.objectOffsets[i]['rotate'][2])
        else:
            pass

def main():
    global R_OFFSET

    selectedObjs = cmds.ls(sl=True)
    target = selectedObjs[0]
    relatives = selectedObjs[1::]

    R_OFFSET = relativeOffset(target, relatives)

main()

def copyPose():
    global R_OFFSET
    global OBJECT_OFFSETS

    R_OFFSET.copyPosition()

def pastePose():
    global R_OFFSET


    R_OFFSET.pasteOffsets()