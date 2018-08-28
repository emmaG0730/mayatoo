import maya.cmds as cmds

def setAnimTransforms(jnt, trn, rot, scl):
    
    cmds.setAttr(jnt + '.translateX', trn[0])
    cmds.setAttr(jnt + '.translateY', trn[1])
    cmds.setAttr(jnt + '.translateZ', trn[2])
    cmds.setAttr(jnt + '.rotateX', rot[0])
    cmds.setAttr(jnt + '.rotateY', rot[1])
    cmds.setAttr(jnt + '.rotateZ', rot[2])
    cmds.setAttr(jnt + '.scaleX', scl[0])
    cmds.setAttr(jnt + '.scaleY', scl[1])
    cmds.setAttr(jnt + '.scaleZ', scl[2])
    
def getCurrentTransforms(jnt):
    
    tx = cmds.getAttr(jnt + '.translateX')
    ty = cmds.getAttr(jnt + '.translateY')
    tz = cmds.getAttr(jnt + '.translateZ')
    rx = cmds.getAttr(jnt + '.rotateX')
    ry = cmds.getAttr(jnt + '.rotateY')
    rz = cmds.getAttr(jnt + '.rotateZ')
    sx = cmds.getAttr(jnt + '.scaleX')
    sy = cmds.getAttr(jnt + '.scaleY')
    sz = cmds.getAttr(jnt + '.scaleZ')
    
    jntTrn = [tx,ty,tz]
    jntRot = [rx,ry,rz]
    jntScl = [sx,sy,sz]

    return jntTrn, jntRot, jntScl

def getJnt():
    sel = cmds.ls(sl=True)
    
    if (len(sel) != 1):
        return 'error'
    else:
        return sel

def updateWin():
    min = cmds.playbackOptions(query = True, min = True)
    max = cmds.playbackOptions(query = True, max = True)
    print min
    print max
    
    cmds.intFieldGrp('start', edit = True, v1 = min)
    cmds.intFieldGrp('end', edit = True, v1 = max)

def getFrames(min, max):
    
    frames = [min]
    
    frame = min
    
    while frame < max:
        frame += 1
        frames.append(frame)
        
    return frames

def singleOffset():
    jnt = getJnt()
    
    if jnt == 'error':
        cmds.error('Please select only one joint')
    else:
        otx = cmds.floatFieldGrp('trnx',query = True, v1 = True)
        oty = cmds.floatFieldGrp('trny',query = True, v1 = True)
        otz = cmds.floatFieldGrp('trnz',query = True, v1 = True)
        orx = cmds.floatFieldGrp('rotx',query = True, v1 = True)
        ory = cmds.floatFieldGrp('roty',query = True, v1 = True)
        orz = cmds.floatFieldGrp('rotz',query = True, v1 = True)
        osx = cmds.floatFieldGrp('sclx',query = True, v1 = True)
        osy = cmds.floatFieldGrp('scly',query = True, v1 = True)
        osz = cmds.floatFieldGrp('sclz',query = True, v1 = True)
        
        jntTrn, jntRot, jntScl = getCurrentTransforms(jnt[0])
        
        setAnimTransforms(jnt[0],
                          [jntTrn[0] + otx, jntTrn[1] + oty, jntTrn[2] + otz],
                          [jntRot[0] + orx, jntRot[1] + ory, jntRot[2] + orz],
                          [jntScl[0] + osx, jntScl[1] + osy, jntScl[2] + osz])

def batchOffset():
    min = cmds.intFieldGrp('start', query = True, v1 = True)
    max = cmds.intFieldGrp('end', query = True, v1 = True)
    
    frames = getFrames (min, max)
    
    for f in frames:
        cmds.currentTime(f)
        singleOffset()
    
def offsetAnimTransformsGUI():
    if cmds.window('offsetAnimTrans', exists = True):
        cmds.deleteUI('offsetAnimTrans', window = True)
        
    cmds.window('offsetAnimTrans', title = 'Offset Animation Transforms')
    cmds.columnLayout()
    
    cmds.floatFieldGrp('trnx', nf = 1, label = 'Translate X', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('trny', nf = 1, label = 'Translate Y', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('trnz', nf = 1, label = 'Translate Z', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('rotx', nf = 1, label = 'rotate X', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('roty', nf = 1, label = 'rotate Y', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('rotz', nf = 1, label = 'rotate Z', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('sclx', nf = 1, label = 'scale X', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('scly', nf = 1, label = 'scale Y', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.floatFieldGrp('sclz', nf = 1, label = 'scale Z', pre = 3, v1=0, cal = (1,"left"), cw2 = (50,60))
    cmds.text(' ')
    
    cmds.intFieldGrp('start', label = 'Start Frame', v1 = 0, cal = (1,"left"), cw2 = (50,60))
    cmds.intFieldGrp('end', label = 'End Frame', v1 = 0, cal = (1,"left"), cw2 = (50,60))
    cmds.text(' ')
    cmds.button(label = 'Offset Frame', width = 100, c = 'singleOffset()')
    cmds.button(label = 'Batch Offset', width = 100, c = 'batchOffset()')
    
    cmds.showWindow('offsetAnimTrans')
    
    updateWin()
    
offsetAnimTransformsGUI()