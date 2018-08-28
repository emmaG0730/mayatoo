fbxSettings = 'W:/ToolBox/External/DCC/Other/fbxpresets/'

mayaFbxAttr = {'b_smoothingGrps': 'FBXExportSmoothingGroups -v ',
               'b_splitVertNrms': 'FBXExportHardEdges -v ',
               'b_tanBiNrms': 'FBXExportTangents -v ',
               'b_smoothMesh': 'FBXExportSmoothMesh -v ',
               'b_preserveInst': 'FBXExportInstances -v ',
               #'b_convertNullObjs': 'FBXProperty Export|IncludeGrp|Geometry|ContainerObjects -v ',
               'b_triangulate': 'FBXExportTriangulate -v ',
               'b_refAssetCont': 'FBXExportReferencedAssetsContent -v ',
               'b_anim': 'FBXProperty Export|IncludeGrp|Animation -v ',
               'b_useSceneName': 'FBXExportUseSceneName -v ',
               #'b_removeSingleKey': 'FBXProperties Export|IncludeGrp|Animation|ExtraGrp|RemoveSingleKey -v ',
               'b_bakeAnim': 'FBXExportBakeResampleAnimation -v ',
               'i_startFrame': 'FBXExportBakeComplexStart -v ',
               'i_endFrame': 'FBXExportBakeComplexEnd -v ',
               'i_stepFrame': 'FBXExportBakeComplexStep -v ',
               #'b_resampleAnim': 'FBXProperty Export|IncludeGrp|Animation|BakeComplexAnimation|ResampleAnimationCurves -v ',
               #'b_def': 'FBXProperty Export|IncludeGrp|Animation|Deformation -v ',
               'b_skins': 'FBXExportSkins -v ',
               'b_morphs': 'FBXExportShapes -v ',
               #'b_curveFilters': 'FBXProperty Export|IncludeGrp|Animation|CurveFilter -v ',
               'b_constKeyReduce': 'FBXExportApplyConstantKeyReducer -v ',
               #'f_transPrecision': 'FBXProperty Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedTPrec -v ',
               #'f_rotPrecision': 'FBXProperty Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedRPrec -v ',
               #'f_scalePrecision': 'FBXProperty Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedSPrec -v ',
               #'f_otherPrecision': 'FBXProperty Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedOPrec -v ',
               #'b_autoTangents': 'FBXProperty Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|AutoTangentsOnly -v ',
               #'b_constraints': 'FBXProperty Export|IncludeGrp|Animation|ConstraintsGrp|Constraint  -v ',
               #'b_skelDef': 'FBXProperty Export|IncludeGrp|Animation|ConstraintsGrp|Character  -v ',
               'b_cam': 'FBXExportCameras -v ',
               'b_lights': 'FBXExportLights -v ',
               'b_embedMedia': 'FBXExportEmbeddedTextures -v ',
               #'b_autoUnits': 'FBXProperty Export|AdvOptGrp|UnitsGrp|DynamicScaleConversion -v ',
               'a_unitType': 'FBXExportConvertUnitString -v ',
               'a_axis': 'FBXExportUpAxis ',
               #'b_showWarningManager': 'FBXProperty Export|AdvOptGrp|UI|ShowWarningsManager -v ',
               'b_genLogData': 'FBXExportGenerateLog -v ',
               'a_fileType': 'FBXExportInAscii -v ',
               'a_version': 'FBXExportFileVersion -v '
               }

maxFbxAttr = {'b_smoothingGrps': 'FBXExporterSetParam "SmoothingGroups" ',
              'b_splitVertNrms': 'FBXExporterSetParam "NormalsPerPoly" ',
              'b_tanBiNrms': 'FBXExporterSetParam "TangentSpaceExport" ',
              'b_smoothMesh': 'FBXExporterSetParam "SmoothMeshExport" ',
              'b_preserveInst': 'FBXExporterSetParam "Preserveinstances" ',
              'b_selSets': 'FBXExporterSetParam "SelectionSetExport" ',
              'b_convertNullObjs': 'FBXExporterSetParam "GeomAsBones" ',
              'b_triangulate': 'FBXExporterSetParam "ColladaTriangulate" ',
              'b_preserveEdgeOrient': 'FBXExporterSetParam "Export|IncludeGrp|Geometry|PreserveEdgeOrientation" ',
              'b_anim': 'FBXExporterSetParam "Animation" ',
              'b_useSceneName': 'FBXExporterSetParam "UseSceneName" ',
              'b_removeSingleKey': 'FBXExporterSetParam "Removesinglekeys" ',
              'b_bakeAnim': 'FBXExporterSetParam "BakeAnimation" ',
              'i_startFrame': 'FBXExporterSetParam "BakeFrameStart" ',
              'i_endFrame': 'FBXExporterSetParam "BakeFrameEnd" ',
              'i_stepFrame': 'FBXExporterSetParam "BakeFrameStep" ',
              'b_resampleAnim': 'FBXExporterSetParam "BakeResampleAnimation" ',
              'b_def': 'FBXExporterSetParam "Export|IncludeGrp|Animation|Deformation" ',
              'b_skins': 'FBXExporterSetParam "Skin" ',
              'b_morphs': 'FBXExporterSetParam "Shape" ',
              'b_curveFilters': 'FBXExporterSetParam "Export|IncludeGrp|Animation|CurveFilter" ',
              'b_constKeyReduce': 'FBXExporterSetParam "FilterKeyReducer" ',
              'f_transPrecision': 'FBXExporterSetParam "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedTPrec" ',
              'f_rotPrecision': 'FBXExporterSetParam "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedRPrec"',
              'f_scalePrecision': 'FBXExporterSetParam "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedSPrec" ',
              'f_otherPrecision': 'FBXExporterSetParam "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedOPrec" ',
              'b_autoTangents': 'FBXExporterSetParam "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|AutoTangentsOnly" ',
              'b_cam': 'FBXExporterSetParam "Cameras" ',
              'b_lights': 'FBXExporterSetParam "Lights" ',
              'b_embedMedia': 'FBXExporterSetParam "EmbedTextures" ',
              'b_autoUnits': 'FBXExporterSetParam "Export|AdvOptGrp|UnitsGrp|DynamicScaleConversion" ',
              'a_unitType': 'FBXExporterSetParam "ConvertUnit" ',
              'a_axis': 'FBXExporterSetParam "UpAxis" ',
              'b_showWarningManager': 'FBXExporterSetParam "ShowWarnings" ',
              'b_genLogData': 'FBXExporterSetParam "GenerateLog" ',
              'a_fileType': 'FBXExporterSetParam "ASCII" ',
              'a_version': 'FBXExporterSetParam "FileVersion" '
              }

def readPreset(fbxPreset,fbxAttr):
    fileData = {}
    file =  open(fbxPreset, 'rb')
    for line in file:
        data = line.rstrip('\r\n').split('=')
        fileData[data[0].strip()]=data[1].strip().lower()
    return fileData[fbxAttr]

def getFbxData(dcc,preset):
    units = {'0':'mm',
             '1':'dm',
             '2':'cm',
             '3':'m',
             '4':'km',
             '5':'In',
             '6':'ft',
             '7':'yd',
             '8':'mi'}

    version = {'0':'FBX201600',
               '2':'FBX201400',
               '3':'FBX201300',
               '4':'FBX201200',
               '5':'FBX201100',
               '6':'FBX201000',
               '7':'FBX200900'}

    axis = {'0':'y',
            '1':'z'}

    data = ''

    if dcc == 'maya':
        print "DCC = " + dcc
        for i in mayaFbxAttr:
            fbxData = readPreset(fbxSettings + preset + '.fbxpreset', i)
            if i == 'a_unitType':
                fbxData = '"' + units[fbxData] + '"'
            elif i == "a_version":
                fbxData = '"' + version[fbxData] + '"'
            elif i == 'a_axis':
                fbxData = '"' + axis[fbxData] + '"'
            else:
                pass
            mayaData = mayaFbxAttr[i] + fbxData +';'
            data += mayaData
    elif dcc == 'max':
        for i in maxFbxAttr:
            fbxData = readPreset(fbxSettings + preset + '.fbxpreset', i)
            if i == 'a_unitType':
                fbxData = '"' + units[fbxData] + '"'
            elif i == "a_version":
                fbxData = '"' + version[fbxData] + '"'
            elif i == 'a_axis':
                fbxData = '"' + axis[fbxData] + '"'
            else:
                pass
            maxData =  maxFbxAttr[i] + fbxData +';'
            data += maxData
    else:
        print 'Unknown DCC'
    return data

def getDCC(filename):
    extension = (filename.split('.'))[-1]
    if extension.lower() == '.max':
        return 'max'
    if extension.lower() == '.ma' or extension.lower() == '.mb':
        return 'maya'
    else:
        return 'unknown DCC'

def getFileName(filepath):
    filepath = filepath.replace('\\', '/')
    filename = filepath.split('/')[-1]
    print filename
    return filename