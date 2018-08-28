import maya.cmds as cmds
import GetSockets.writeBoneNames as wbn

class socketInfo(object):

    # constructor
    def __init__(self, layerName, fbxFile, extraOffset):
        self.layerName = layerName
        self.oldBoneList = wbn.readJointTag('jointTag')
        self.fbxFile = fbxFile
        self.extraoffset = extraOffset

    # gets the object list from the layer passed in
    def getSocketNames(self, layerName):
        layerObjects = cmds.editDisplayLayerMembers(layerName, query = True, fn = True)
        return layerObjects


    def getNewJointName(self, oldJointName):
        name = oldJointName.split('|')[-1]

        for i in self.oldBoneList:
            if name == i:
                newJnt = self.oldBoneList[i]
                print newJnt
                return newJnt
            else:
                print "does not exist"

    # finds the offset of the socket based on the grandparent and parent location
    def getSocketOffset(self, socketName, grandparentName):
        jointName = self.getNewJointName(grandparentName)

        myLoc = cmds.spaceLocator(p=(0, 0, 0))
        myGrp = cmds.group (myLoc)

        cmds.parentConstraint(jointName, myGrp)
        cmds.parentConstraint(socketName, myLoc[0])

        socketOffsetT = cmds.getAttr(myLoc[0] + '.translate')
        socketOffsetRX = cmds.getAttr(myLoc[0] + '.rotateX') + self.extraoffset[0]
        socketOffsetRY = cmds.getAttr(myLoc[0] + '.rotateY') + self.extraoffset[1]
        socketOffsetRZ = cmds.getAttr(myLoc[0] + '.rotateZ') + self.extraoffset[2]
        socketOffsetR = (socketOffsetRX, socketOffsetRY, socketOffsetRZ)
        socketOffsetS = cmds.getAttr(myLoc[0] + '.scale')

        socketOffset = [socketOffsetT[0], socketOffsetR, socketOffsetS[0]]

        cmds.delete(myGrp)


        return socketOffset

    # gets the ancestor joint information from the socket full path
    def getAncestors(self, objectsInLayer):
        parentList = []
        grandparentList = []

        for i in objectsInLayer:
            nameSplit = i.split ('|')
            nameSplit.remove(nameSplit[-1])
            parent = '|'.join(nameSplit)
            nameSplit.remove(nameSplit[-1])
            grandparent = '|'.join(nameSplit)
            parentList.append(parent)
            grandparentList.append(grandparent)

        return parentList, grandparentList

    # gets the current file path and file name
    def getFileLocation(self):
        filePath = cmds.file(query = True, sceneName = True)
        fileSplit = filePath.split('/')
        fileName = ((fileSplit[-1]).split('.'))[0]
        fileSplit.remove(fileSplit[-1])
        filePath = '/'.join(fileSplit)

        return filePath, fileName

    # writes the data passed in to a file
    def writeData(self, layerObjects, grandparentList, offsetList):
        filePath, fileName = self.getFileLocation()

        file = open(filePath + '/' + fileName + '.txt', 'wb')

        for i in range(len(layerObjects)):
            socketName = (layerObjects[i].split('|'))[-1]
            oldGrandparentName = (grandparentList[i].split('|'))[-1]

            grandparentName = self.getNewJointName(oldGrandparentName)

            file.write('"socketName": "' + socketName + '"\r\n')
            file.write('{\r\n')
            file.write('"socketParentName": "' + grandparentName + '"\r\n')
            file.write('"socketOffset": ' + str(offsetList[i]) + '\r\n')
            file.write('}\r\n\r\n')
        file.close()


    def importFBX(self, filename):

        namespace = (filename.split('/')[-1]).split('.')[0]
        self.fbxFileContents = cmds.file (filename, i = True, type = "FBX", ignoreVersion = True, ra = True, mergeNamespacesOnClash = False, namespace = namespace, options = "mo-0", pr = True)


    def main(self):
        self.importFBX(self.fbxFile)
        layerObjects = self.getSocketNames(self.layerName)
        parentList, grandparentList = self.getAncestors(layerObjects)
        listRange = len(layerObjects)
        offsetList = []

        for i in range(listRange):
            offset = self.getSocketOffset(layerObjects[i], grandparentList[i])
            offsetList.append(offset)

        self.writeData(layerObjects, grandparentList, offsetList)


def getFbxFile():
    basicFilter = "*.fbx"
    fbxFileName = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, cap = 'Select FBX File to Import', okc = 'Load', fm = 1)
    cmds.textFieldButtonGrp('fbxFileLoc', edit = True, text = fbxFileName[0])

def getSockets():
    fbxFileName = cmds.textFieldButtonGrp('fbxFileLoc', query = True, text = True)
    layer = cmds.optionMenuGrp('socketLayer', query = True, value = True)
    extraOffset = cmds.floatFieldGrp('extraOffset', query= True, value = True)

    sockets = socketInfo(layer, fbxFileName, extraOffset)
    sockets.main()


def main():
    dispLayers = cmds.ls (type = 'displayLayer')

    if cmds.window ('getSocketsWin', exists = True):
        cmds.deleteUI ('getSocketsWin', window = True)

    cmds.window('getSocketsWin', title = 'Get Sockets')
    cmds.columnLayout()
    cmds.optionMenuGrp('socketLayer', label='Socket Layer', cl2 = ('left', 'left'), cw2 = (75, 250))
    for layer in dispLayers:
        cmds.menuItem( label=layer )
    cmds.textFieldButtonGrp('fbxFileLoc', label = 'FBX File', buttonLabel = 'File', bc = 'getFbxFile()', cl3 = ('left', 'left', 'left'), cw3 = (75, 250, 75))
    cmds.floatFieldGrp('extraOffset', label='Additional Rotate Offset', nf = 3, cl4 = ('left', 'left', 'left', 'left'), cw4 = (130, 74, 74,74) )
    cmds.button(label = 'Get Sockets', command = 'getSockets()')
    cmds.showWindow('getSocketsWin')

main()