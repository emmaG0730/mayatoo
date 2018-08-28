import maya.cmds as cmds

# Parses through the socket data file and returns a list of data
def importSocketData(filename):
    socketFile = open(filename, 'r')
    socketFileList = []
    socketDataList = {}
    counter = 0
    socketCounter = 0
    socketData = {}

    for line in socketFile:
        data = line.split('{')[0].replace('\r\n', '')
        socketFileList.append(data)

    socketFileList = filter (None, socketFileList)

    new_list = [i for i in socketFileList if i != '}']


    for i in range (len(new_list)):
        keyInfo = new_list[i].split(':')
        counter += 1
        if counter == 3:
            counter = 0
            socketData [keyInfo[0].replace('"', '')] = keyInfo[1].replace('"','')
            socketDataList [socketCounter] = socketData
            socketData = {}
            socketCounter += 1
        else:
            socketData [keyInfo[0].replace('"', '')] = keyInfo[1].replace('"','')

    return socketDataList

# Cleans up the socket offset data and returns translate, rotation, and scale
def getPosition(offset):
    offsetData = offset.split('),')
    offsetT = offsetData[0].replace('[(','')
    offsetR = offsetData[1].replace('(','')
    offsetS = offsetData[2].replace('(','')
    offsetS = offsetS.replace(')]','')

    print "offsetT", offsetT
    print "offsetR", offsetR
    print "offsetS", offsetS

    return offsetT, offsetR, offsetS

# Creates a locator and places them based on the socket offset data
def createSockets(socketName, socketParent, offsetT, offsetR, offsetS, extraOffset):
    offsetTX, offsetTY, offsetTZ = offsetT.split(',')
    offsetRX, offsetRY, offsetRZ = offsetR.split(',')
    offsetSX, offsetSY, offsetSZ = offsetS.split(',')

    print offsetTX, offsetTY, offsetTZ


    socketLoc = cmds.spaceLocator(p=(0, 0,0), name = socketName)
    socketGrp = cmds.group (socketLoc[0], name = socketName + '_grp')

    myPConst = cmds.parentConstraint(socketParent, socketGrp, name = socketName + '_parentConst')
    cmds.setAttr(socketLoc[0] + '.translateX', float(offsetTX))
    cmds.setAttr(socketLoc[0] + '.translateY', float(offsetTY))
    cmds.setAttr(socketLoc[0] + '.translateZ', float(offsetTZ))

    cmds.setAttr(socketLoc[0] + '.rotateX', float(offsetRX) + extraOffset[0])
    cmds.setAttr(socketLoc[0] + '.rotateY', float(offsetRY) + extraOffset[1])
    cmds.setAttr(socketLoc[0] + '.rotateZ', float(offsetRZ) + extraOffset[2])

    cmds.setAttr(socketLoc[0] + '.scaleX', float(offsetSX))
    cmds.setAttr(socketLoc[0] + '.scaleY', float(offsetSY))
    cmds.setAttr(socketLoc[0] + '.scaleZ', float(offsetSZ))

    cmds.delete(myPConst)
    cmds.parent(socketLoc[0], socketParent)
    cmds.delete(socketGrp)

def placeSockets():
    fbxFileName = cmds.textFieldButtonGrp('socketFileLoc', query = True, text = True)
    extraOffset = cmds.floatFieldGrp('extraOffset', query= True, value = True)
    socketDataList = importSocketData(fbxFileName)

    for i in range(len(socketDataList)):
        offsetT, offsetR, offsetS = getPosition(socketDataList[i]['socketOffset'])
        createSockets(socketDataList[i]['socketName'], socketDataList[i]['socketParentName'], offsetT, offsetR, offsetS, extraOffset)

def getSocketFile():
    basicFilter = "*.txt"
    fbxFileName = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, cap = 'Select FBX File to Import', okc = 'Load', fm = 1)
    cmds.textFieldButtonGrp('socketFileLoc', edit = True, text = fbxFileName[0])

def loadSocketWin():
    if cmds.window('loadSocketWin', exists=True):
        cmds.deleteUI('loadSocketWin', window = True)

    cmds.window ('loadSocketWin', title = 'Load Sockets')
    cmds.columnLayout()
    cmds.textFieldButtonGrp('socketFileLoc', label = 'Socket File', buttonLabel = 'File', bc = 'getSocketFile()', cl3 = ('left', 'left', 'left'), cw3 = (75, 250, 75))
    cmds.floatFieldGrp('extraOffset', label='Additional Rotate Offset', nf = 3, cl4 = ('left', 'left', 'left', 'left'), cw4 = (130, 74, 74,74) )
    cmds.button(label = 'Place Sockets', command = 'placeSockets()')
    cmds.showWindow('loadSocketWin')

loadSocketWin()