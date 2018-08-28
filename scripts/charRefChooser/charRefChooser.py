import maya.cmds as cmds
import json

def getCharList(dataPath):
    with open(dataPath) as dataFile:
        data = json.load(dataFile)
    return data['Characters']

CHARLIST = getCharList('R:/Jx4/tools/dcc/maya/scripts/DataFiles/character_rig_list.json')

def updateCharList():
    global CHARLIST

    for i in CHARLIST:
        cmds.textScrollList('charList', edit=True, append=i, selectIndexedItem=1)


def referenceCharacter():
    global CHARLIST

    character = cmds.textScrollList('charList', query=True, si=True)
    cmds.file(CHARLIST[character[0]], r=True, type="mayaAscii", ignoreVersion=True, gl=True,
              mergeNamespacesOnClash=True, namespace="inputFile", options="v=0;")

def charSelectWin():
    if cmds.window('charSelWin', exists=True):
        cmds.deleteUI('charSelWin', window=True)

    cmds.window('charSelWin', title='Character Select')

    cmds.columnLayout()
    cmds.textScrollList('charList', numberOfRows=8, allowMultiSelection=False)
    cmds.button(label='Reference Character', command='referenceCharacter()')
    cmds.showWindow('charSelWin')
    updateCharList()