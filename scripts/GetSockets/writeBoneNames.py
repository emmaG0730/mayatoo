import maya.cmds as cmds
import _winreg, os

HKCU_SEASUNTOOLS = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Environment')
SEASUNTOOLS = _winreg.QueryValueEx(HKCU_SEASUNTOOLS,'SEASUNTOOLS')[0]
SCRIPTPATH = SEASUNTOOLS + 'DCC\\Maya\\scripts\\GetSockets\\'


def writeBoneNames(fileName):
    global SCRIPTPATH
    cmds.select(hi = True)
    list = cmds.ls(sl = True)

    file = open(SCRIPTPATH + fileName + '.csv','wb')
    for i in list:
        if i != list[-1]:
            file.write(i + '\n')
        else:
            file.write(i)

    file.close()

def readBoneNames(fileName):
    if os.path.isfile(SCRIPTPATH + fileName + '.csv') == False:
        cmds.confirmDialog( title='Error', message='Missing ' + fileName + '.  Please generate a joint list.', button=['OK'], cancelButton='OK', dismissString='No' )
        return None
    else:
        file = open(SCRIPTPATH + fileName + '.csv', 'r')
        for line in file:
            jointList = line.split('\n')
        print jointList
        return jointList

def readJointTag(fileName):
    jointTagList = {}
    print SCRIPTPATH + fileName + '.csv'
    if os.path.isfile(SCRIPTPATH + fileName + '.csv') == False:
        cmds.confirmDialog( title='Error', message='Missing ' + fileName + '.  Please generate a joint tag list.', button=['OK'], cancelButton='OK', dismissString='No' )
        return None
    else:
        file = open(SCRIPTPATH + fileName + '.csv', 'r')
        for line in file:
            lineSplit = line.split('\n')
            jointTag = lineSplit[0].split(',')
            jointTagList [jointTag[0]] = jointTag[1].replace('\r', '')
        print jointTagList
        return jointTagList

readJointTag('jointTag')