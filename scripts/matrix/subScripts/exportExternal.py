import json, os, ctypes.wintypes
CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value

try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass
import batchExport
import maya.cmds as cmds

if cmds.pluginInfo("fbxmaya", query=True, loaded=True) == False:
    cmds.loadPlugin("fbxmaya")
    print 'fbxmaya has just been loaded'
else:
    print 'fbxmaya is already loaded'

if cmds.pluginInfo("MayaXMDExportPlugin2016", query=True, loaded=True) == False:
    cmds.loadPlugin("MayaXMDExportPlugin2016")
    print 'MayaXMDExportPlugin2016 has just been laoded'
else:
    print 'MayaXMDExportPlugin2016 is already loaded'

def get_export_list(exportFile):
    with open(exportFile) as exportFile:
        exportData = json.load(exportFile)

    sourceFiles = []
    exportFiles = []

    for i in exportData:
        sourceFiles.append(i)
        exportFiles.append(exportData[i])

    return sourceFiles, exportFiles

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_custom_data():
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    documents = buf.value

    return documents

def main():
    presets = load_custom_data()

    sourceFiles, exportFiles = get_export_list('R:/Jx4/tools/internal/animationExplorer/data/xmd.json')
    for i in exportFiles:
        ensure_dir(i)
    batchExport.BATCHEXPORT(sourceFiles, exportFiles, presets, "none")
    print 'export finished'

main()