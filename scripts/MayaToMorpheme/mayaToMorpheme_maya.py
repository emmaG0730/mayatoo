import maya.cmds as cmds
import maya.mel as mel
import MayaToMorpheme.exportFBX as efbx
import MayaToMorpheme.exportXMD as exmd


# loads the FBX plugin
def loadFBXPlugin():
    if cmds.pluginInfo("fbxmaya", query=True, loaded=True) == False:
        cmds.loadPlugin("fbxmaya")
        print 'fbxmaya has just been loaded'
    else:
        print 'fbxmaya is already loaded'


# loads the XMD plugin
def loadXMDPlugin():
    if cmds.pluginInfo("MayaXMDExportPlugin2016", query=True, loaded=True) == False:
        cmds.loadPlugin("MayaXMDExportPlugin2016")
        print 'MayaXMDExportPlugin2016 has just been laoded'

    else:
        if cmds.pluginInfo("MayaXMDImportPlugin2016", query=True, loaded=True) == False:
            cmds.loadPlugin("MayaXMDImportPlugin2016")
            print 'MayaXMDImportPlugin2016 has just been loaded'
        else:
            print 'MayaXMDExportPlugin2016 is already loaded'
            print 'MayaXMDImportPlugin2016 is already loaded'
    if cmds.pluginInfo("MayaXMDImportPlugin2016", query=True, loaded=True) == False:
        cmds.loadPlugin("MayaXMDImportPlugin2016")
        print 'MayaXMDImportPlugin2016 has just been loaded'
    else:
        print 'MayaXMDImportPlugin2016 is already loaded'


# Gets the current playback time range and returns the start and end values
def getCurRange():
    startFrame = cmds.playbackOptions(query=True, min=True)
    endFrame = cmds.playbackOptions(query=True, max=True)
    return startFrame, endFrame


# Gets current animation range based on the b_M_pelvis_v1_JNT
def getAnimRange():
    try:
        startFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="first")
        endFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="last")
        return startFrame, endFrame
    except:
        print "No object name b_M_pelvis_v1_JNT was found"
        return 0, 0


# returns a list of joints with the inputted namespace
def getJoints(namespace):
    allJoints = cmds.ls(type='joint')
    mainJoints = [x for x in allJoints if "_JNT" in x]
    exportJoints = [x for x in mainJoints if namespace + ":" in x]
    return exportJoints


# returns a list of geometry that follows the naming convention
def getGeo():
    transforms = cmds.ls(transforms=True)
    geometry = cmds.filterExpand(transforms, sm=12)
    exportGeo = [x for x in geometry if "_GEO" in x]

    return exportGeo


# returns a list of blend shapes tied to the rig
def getShapes():
    transforms = cmds.ls(transforms=True)
    geometry = cmds.filterExpand(transforms, sm=12)
    exportShp = [x for x in geometry if "_SHP" in x]

    return exportShp


# returns a list of controllers that are part of the rig
def getControls():
    transforms = cmds.ls(transforms=True)
    geometry = cmds.filterExpand(transforms, sm=12)
    exportCtrl = [x for x in geometry if "_CTRL" in x]

    return exportCtrl


# selects objects require to export an animation
def selectAnim():
    joints = getJoints('RiGGiE')
    cmds.select(d=True)
    cmds.select(joints)


# selects objects required to export a rig
def selectRig():
    joints = getJoints('RiGGiE')
    geo = getGeo()

    cmds.select(d=True)
    cmds.select(joints)
    cmds.select(geo, add=True)


# selects objects required to export a rig with blend shapes
def selectRigBlend():
    joints = getJoints('RiGGiE')
    geo = getGeo()
    shapes = getShapes()

    cmds.select(d=True)
    cmds.select(joints)
    cmds.select(geo, add=True)
    cmds.select(shapes, add=True)


# returns the file name without a path or extension
def getSceneName():
    filepath = cmds.file(q=True, sn=True)
    filename = (((filepath.split('/'))[-1]).split('.'))[0]
    return filename


def loadFBXPreset(preset):
    fbxData = efbx.getFbxData('maya',preset)
    mel.eval(fbxData)


def exportFBX(filePath, fileName):
    print filePath
    print fileName
    print 'FBXExport -file "' + filePath + '/' + fileName + '" -s;'
    mel.eval('FBXExport -file "' + filePath + '/' + fileName + '" -s;')


# Exports the current file to XMD
def exportXMD(filepath, filename, xmdoption, start, end):

    if xmdoption == 1:
        print 'rig'
        xmdoptions = exmd.XMDRigSettings()
        cmds.file(filepath + '/' + filename + '.xmd', type='XMD Export', ea=True, options=xmdoptions, force=True)
        print filepath + '/' + filename + '.xmd', 'has been generated'

    elif xmdoption == 2:
        print 'anim'
        xmdoptions = exmd.XMDAnimSettings(start, end)
        cmds.file(filepath + '/' + filename + '.xmd', type='XMD Export', ea=True, options=xmdoptions, force=True)
        print filepath + '/' + filename + '.xmd', 'has been generated'

    else:
        print 'XMD option is not recognized'
