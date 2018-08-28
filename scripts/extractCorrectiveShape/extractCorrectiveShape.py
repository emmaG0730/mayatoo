import maya.cmds as cmds
import maya.mel as mel

dup1=[]
dup2=[]
baseDup = []

def errorWin(text):
    cmds.promptDialog()

def unlockAttr(object):
    attributes = ['.translate','.rotate','.scale']
    axis = ['X','Y','Z']

    [cmds.setAttr(object + x + y, lock=False) for x in attributes for y in axis]

def duplicateShape():
    global dup1
    global dup2
    global baseDup

    sel = cmds.ls(sl=True)
    if len(sel) > 1 or len(sel) < 1:
        errorWin('Select only 1 object')
    else:
        dup1 = cmds.duplicate(sel, rr=True)
        unlockAttr(dup1[0])

        dup2 = cmds.duplicate(dup1, rr=True)
        cmds.setAttr(dup1[0] + '.visibility', False)

        skin = mel.eval('findRelatedSkinCluster '+sel[0])
        cmds.setAttr(skin + '.envelope', 0)
        baseDup = cmds.duplicate(sel, rr=True)
        cmds.setAttr(baseDup[0] + '.visibility', False)
        cmds.setAttr(skin + '.envelope', 1)

        bs = cmds.blendShape(dup1[0], dup2[0], baseDup[0], name='correctiveShapes')
        cmds.setAttr(bs[0] + '.' + dup1[0], -1)
        cmds.setAttr(bs[0] + '.' + dup2[0], 1)

        cmds.select(dup2)

def generateShape():
    global baseDup

    corShape = cmds.duplicate(baseDup, rr=True)

    unlockAttr(corShape[0])
    cmds.setAttr(corShape[0] + '.visibility', 1)

    cmds.select(d=True)
    cmds.select(corShape)

def cleanShapes():
    global dup1
    global dup2
    global baseDup

    cmds.select(d=True)
    cmds.select(dup1)
    cmds.select(dup2, add=True)
    cmds.select(baseDup, add=True)

    cmds.delete()