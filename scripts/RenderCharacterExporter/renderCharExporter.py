# script: renderCharExporter.py
# scripted by: Linh Nguyen
# description: This script exports the character for runtime
try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass

import maya.cmds as cmds
import maya.mel as mel
import json

dataPath = '../DataFiles/runtime_char_data.json'

def loadFBXPlugin():
    if cmds.pluginInfo("fbxmaya", query=True, loaded=True) == False:
        cmds.loadPlugin("fbxmaya")
        print 'fbxmaya has just been loaded'
    else:
        print 'fbxmaya is already loaded'

class renderCharExport(object):
    def __init__(self, charName, parentJoint, exportDirectory, controls):
        self.charName = charName
        self.parentJoint = parentJoint
        self.meshList = []
        self.jointList = []
        self.exportList = []
        self.exportDirectory = ((exportDirectory.split('.'))[0]) + '.fbx'
        self.controls = controls

    def getJointList(self):
        cmds.select('b_M_origin_v1_JNT', hi=True)
        self.jointList = cmds.ls(sl=True)

    def getMeshList(self):
        cmds.select(self.charName)
        objectList = cmds.ls(sl=True, type='mesh', dag=True)
        for i in objectList:
            p = cmds.pickWalk(i, direction='up')
            self.meshList.append(p[0])

        self.meshList = list(set(self.meshList))

    def getExportList(self):
        self.exportList = self.meshList + self.jointList

    def removeConstraints(self):
        constraints = ['parentConstraint', 'pointConstraint', 'orientConstraint', 'aimConstraint']
        constraintList = []
        for i in self.jointList:
            for y in constraints:
                if cmds.objectType(i) == y:
                    constraintList.append(i)
        self.jointList = [x for x in self.jointList if x not in constraintList]
        cmds.delete(constraintList)


    def selectObjectsForExport(self):
        print "exports the character"
        self.getJointList()
        self.removeConstraints()
        self.getMeshList()
        self.getExportList()

    def fbxSettings(self):
        mel.eval('FBXExportFileVersion "FBX201200";')
        mel.eval('FBXExportInAscii -v true;')
        mel.eval('FBXExportSmoothingGroups -v true;')
        mel.eval('FBXExportHardEdges -v false;')
        mel.eval('FBXExportTangents -v true;')
        mel.eval('FBXExportSmoothMesh -v true;')
        mel.eval('FBXExportTriangulate -v false;')
        mel.eval('FBXExportAnimationOnly -v false;')
        mel.eval('FBXExportSkins -v true;')
        mel.eval('FBXExportShapes -v true;')
        mel.eval('FBXExportCameras -v false;')
        mel.eval('FBXExportConvertUnitString "cm"')
        mel.eval('FBXExportInputConnections -v true')

    def export(self):
        self.selectObjectsForExport()
        self.exportFBX(self.exportList)
        self.openFBX()
        self.removeControls()
        self.exportFBX(self.exportList)

    def exportFBX(self, exportList):
        cmds.select(exportList)
        self.fbxSettings()
        mel.eval('FBXExport -f "' + self.exportDirectory + '" -s;')
        print 'file has been exported'

    def openFBX(self):
        cmds.file(new=True, force=True)
        mel.eval('FBXImport - file "' +  self.exportDirectory  +  '"')

    def removeControls(self):
        cmds.delete(self.controls)

def exportChar(charName, parentJoint, exportDirectory, controls):
    print 'Exporting Character'
    rce = renderCharExport(charName, parentJoint, exportDirectory, controls)
    rce.export()

def getCharData(character):
    with open(dataPath) as dataFile:
        data = json.load(dataFile)
    return data[character]

def main(character):
    loadFBXPlugin()
    data = getCharData(character)
    cmds.file(data['file'], force=True, open=True)
    print data['character_meshes']
    print data['root_joint']
    print data['export_path']
    print data['group']
    exportChar(data['character_meshes'], data['root_joint'], data['export_path'], data['group'])