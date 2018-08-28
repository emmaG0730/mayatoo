import maya.standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds

class shiftKeyframes():

    # Constructor
    def __init__(self, objects, animStart):
        self.selection = objects
        self.animStart = animStart
        self.keyedObjects = self.getObjectsWithKeys()
        self.animBlendType = ['animBlendNodeAdditiveDL',
                              'animBlendNodeAdditiveRotation',
                              'animBlendNodeAdditiveScale',
                              'animBlendNodeBoolean']
        self.animCurveType = ['animCurveTL',
                              'animCurveTA',
                              'animCurveTU']

    # Finds which objects within the selection has keyframes
    def getObjectsWithKeys(self):
        keyedObjects = []

        for i in self.selection:
            startFrame = cmds.findKeyframe(i, which="first")
            endFrame = cmds.findKeyframe(i, which="last")

            if startFrame == endFrame:
                pass

            else:
                keyedObjects.append(i)

        return keyedObjects

    # Returns the starting and ending frame of the entire animation
    def getKeyframeData(self):
        startFrameIndex = []
        endFrameIndex = []

        for i in self.keyedObjects:
            startFrame = cmds.findKeyframe(i, which="first")
            endFrame = cmds.findKeyframe(i, which="last")

            startFrameIndex.append(startFrame)
            endFrameIndex.append(endFrame)

        print startFrameIndex
        print endFrameIndex
        return min(startFrameIndex), max(endFrameIndex)

    # Gets the difference between the any two frames
    def getFrameDiff(self, animStart, startFrame):
        frameDiff = animStart - startFrame
        return frameDiff

    # Shifts the keyframes to desired frame
    def shiftKeyFrames(self, curve, startFrame):
        frameDiff = (self.animStart - startFrame)
        keyCount = cmds.keyframe(curve, query=True)
        for i in range(len(keyCount)):
            cmds.keyframe(curve, edit=True, r=True, o='over', tc=frameDiff, t=(keyCount[i]))

    # Adjusts the time range to fit the animation
    def adjustTimeRange(self, startFrame, endFrame):
        cmds.playbackOptions(edit=True, minTime=startFrame, maxTime=endFrame)

    # Returns a list of all the animation curves
    def getAnimCurves(self):
        animAttrList = []
        curveList = []
        for i in self.keyedObjects:
            animNodes = []
            for x in self.animBlendType:
                animNode = cmds.listConnections(i, sh=True, t=x)
                animNodes = animNodes + animNode
                animNodes = list(set(animNodes))
            animAttrList.append(animNodes)

        for i in animAttrList:

            for x in self.animCurveType:
                connection = cmds.listConnections(i, sh=True, t=x)
                if connection == None:
                    pass
                else:
                    curveList += connection
        return curveList

    def main(self):
        minKey ,maxKey = self.getKeyframeData()
        curveList = self.getAnimCurves()
        for i in curveList:
            print i
            print minKey
            self.shiftKeyFrames(i, minKey)
        self.adjustTimeRange(self.animStart, maxKey-minKey)

def main():
    cmds.select('RiGGiE:c_M_character_v1_GRP')
    cmds.select(hi=True)
    mySel = cmds.ls(sl=True)
    Character = shiftKeyframes(mySel, 0)
    Character.main()