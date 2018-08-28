import _winreg
import maya.cmds as cmds


class reBindPose():
    def __init__(self, skeleton):
        self.skeleton = skeleton
        self.RIGPATH = 'W:/JX4/Animation/MaleAdult/AnimationSource/Rigs/'

    # Combs through skeleton and returns the name and transforms
    def getBindPose(self):
        cmds.select(self.skeleton, hi=True)
        selection = cmds.ls(sl=True)
        shapes = cmds.ls(sl=True, shapes=True)
        fullSkeleton = [x for x in selection if x not in shapes]
        skeletonData = []

        for i in fullSkeleton:
            boneT = float("{0:.4f}".format(cmds.getAttr(i + '.translateX'))), \
                    float("{0:.4f}".format(cmds.getAttr(i + '.translateY'))), \
                    float("{0:.4f}".format( cmds.getAttr(i + '.translateZ')))

            boneR = float("{0:.4f}".format(cmds.getAttr(i + '.rotateX'))), \
                    float("{0:.4f}".format(cmds.getAttr(i + '.rotateY'))), \
                    float("{0:.4f}".format(cmds.getAttr(i + '.rotateZ')))

            boneData = i, boneT, boneR

            skeletonData.append(boneData)
        return skeletonData

    # Writes skeletal data
    def writeFile(self, data):

        file = open(self.RIGPATH + 'bindPose.txt', 'wb')
        for i in data:
            file.write(str(i) + "\n")

        file.close()

    # Reads skeletal data
    def readFile(self):
        file = open(self.RIGPATH + 'bindPose.txt', 'r')
        fileData = []

        for i in file:
            data = eval(i)
            fileData.append(data)
        return fileData

    # Sets current skeleton to the stored bind pose
    def setBindPose(self):
        bindPose = self.readFile()
        for i in bindPose:
            print i[0]
            print i[1][0]
            print '---------------------'
            cmds.setAttr(i[0] + '.translateX', i[1][0])
            cmds.setAttr(i[0] + '.translateY', i[1][1])
            cmds.setAttr(i[0] + '.translateZ', i[1][2])
            cmds.setAttr(i[0] + '.rotateX', i[2][0])
            cmds.setAttr(i[0] + '.rotateY', i[2][1])
            cmds.setAttr(i[0] + '.rotateZ', i[2][2])

            cmds.setKeyframe(i[0] + '.translateX')
            cmds.setKeyframe(i[0] + '.translateY')
            cmds.setKeyframe(i[0] + '.translateZ')
            cmds.setKeyframe(i[0] + '.rotateX')
            cmds.setKeyframe(i[0] + '.rotateY')
            cmds.setKeyframe(i[0] + '.rotateZ')

    # Sets the new control rig to bind pose
    def setContBind(self, namespace):
        file = open(self.RIGPATH + 'controlList.txt', 'r')
        for i in file:
            controller = i.replace('\r\n', '')
            cmds.setAttr(namespace + ':' + controller + '.translateX', 0)
            cmds.setAttr(namespace + ':' + controller + '.translateY', 0)
            cmds.setAttr(namespace + ':' + controller + '.translateZ', 0)
            cmds.setAttr(namespace + ':' + controller + '.rotateX', 0)
            cmds.setAttr(namespace + ':' + controller + '.rotateY', 0)
            cmds.setAttr(namespace + ':' + controller + '.rotateZ', 0)

            cmds.setKeyframe(namespace + ':' + controller + '.translateX')
            cmds.setKeyframe(namespace + ':' + controller + '.translateY')
            cmds.setKeyframe(namespace + ':' + controller + '.translateZ')
            cmds.setKeyframe(namespace + ':' + controller + '.rotateX')
            cmds.setKeyframe(namespace + ':' + controller + '.rotateY')
            cmds.setKeyframe(namespace + ':' + controller + '.rotateZ')

    # Writes the current bind pose data to a file
    def writeBindPose(self):
        data = self.getBindPose()
        self.writeFile(data)

reBind = reBindPose('Bip001')
reBind.setContBind('RiGGiE')
#reBind.setBindPose()