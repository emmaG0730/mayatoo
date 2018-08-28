## XMDBatchConvert.py
## Scripted By: Linh Nguyen

try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass

from PySide import QtCore, QtGui, QtUiTools
import shiboken
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import csv

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

def readCSV():
    xmdfbxpaths = []
    with open ('XMDExport.csv', 'rb') as csvfile:
        xmdpathreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in xmdpathreader:
            xmdfbxpaths.append(row)
    return xmdfbxpaths

def autoXMDBatch():
    xmdfbxpaths = readCSV()

    for i in xmdfbxpaths:
        fbxpath = i[0].replace('\\', '/')
        xmdpath = i[1].replace('\\', '/')
        XMDBatchConvert(fbxpath, xmdpath)

## This class is used to open a Qt window in Maya using PySide
class xmdExportWindow():

    ## Constructor
    def __init__(self):
        self.uiFilePath = 'R:/SeasunProjects/JX4_Data/Jx4/tools/dcc/maya/scripts/XMDExporter/XMDExportergui.ui'
        self.MainWindow = None

    ## Obtain the maya window wrapper to ensure correct window focusing
    def getMayaWindow():
        omui.MQtUtil.mainWindow()
        ptr = omui.MQtUtil.mainWindow()
        if ptr is not None:
            return shiboken.wrapInstance(long(ptr), QtGui.QWidget)

    ## Use PySide to load the ui file, converting it into a PySide QDialog object
    def loadUiWidget(self, uifilename, parent=getMayaWindow()):
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        ui = loader.load(uifile, parent)
        uifile.close()
        return ui

    ## Connect any signals in the ui file to required methods
    def connectSignals(self):
        self.MainWindow.xmdBtn.clicked.connect(self.xmdLocBtnSig)
        self.MainWindow.curDirBtn.clicked.connect(self.getCurDirSig)
        self.MainWindow.curRangeBtn.clicked.connect(self.getCurRangeSig)
        self.MainWindow.animRangeBtn.clicked.connect(self.getAnimRangeSig)
        self.MainWindow.exportRigBtn.clicked.connect(self.exportRigSig)
        self.MainWindow.exportAnimBtn.clicked.connect(self.exportAnimSig)
        self.MainWindow.fbxMaBtn.clicked.connect(self.fbxMaFileLocBtnSig)
        self.MainWindow.singleExportBtn.clicked.connect(self.exportSingleSig)
        self.MainWindow.fbxMaDirBtn.clicked.connect(self.fbxMaDirLocBtnSig)
        self.MainWindow.batchExportBtn.clicked.connect(self.batchExportSig)

    # ----------------------------- Signals ---------------------------------

    ## Signal method for when button is pushed
    def xmdLocBtnSig(self):
        xmdloc = self.findDir()
        self.MainWindow.xmdLocFld.setText(xmdloc)

    def getCurDirSig(self):
        curDir = self.getCurrentDir()
        self.MainWindow.xmdLocFld.setText(curDir[0])

    def getCurRangeSig(self):
        startFrame, endFrame = self.getCurRange()
        self.setRange(startFrame,endFrame)

    def getAnimRangeSig(self):
        try:
            startFrame, endFrame = self.getAnimRange()
            self.setRange(startFrame, endFrame)
        except:
            print"Error: Cannot set range to animation range"

    def exportRigSig(self):
        print "export rig"

    def exportAnimSig(self):
        print "export anim"
        self.exportAnim()

    def fbxMaFileLocBtnSig(self):
        fbxMaLoc = self.findFile()
        self.MainWindow.fbxMaFileFld.setText(fbxMaLoc)

    def exportSingleSig(self):
        self.exportSingleAnim()

    def fbxMaDirLocBtnSig(self):
        fbxMaDirLoc = self.findDir()
        self.MainWindow.fbxMaDirFld.setText(fbxMaDirLoc)

    def batchExportSig(self):
        xmdloc = self.MainWindow.xmdLocFld.text()
        fbxmadir = self.MainWindow.fbxMaDirFld.text()

        if xmdloc == '':
            print "Error: No XMD export location has been set.  Please set an XMD export location"
        elif fbxmadir == '':
            print "Error: No FBX/MA Directory has been set.  Please set an FBX/MA import location"
        else:

            self.XMDBatchConvert(fbxmadir, xmdloc)

    # ----------------------------- Methods ---------------------------------

    def getCurrentDir(self):
        filePath = cmds.file(query = True, loc = True)
        if filePath == 'unknown':
            print "Error: This file has not been saved"
            dirPath = ''
            fileName = ''
            return dirPath, fileName
        else:
            dirPath = filePath.split('/')
            fileName = dirPath[-1]
            dirPath.remove(dirPath[-1])
            dirPath = '/'.join(dirPath)

            return dirPath, fileName

    def exportAnim(self):
        startFrame = self.MainWindow.rangeStartFld.value()
        endFrame = self.MainWindow.rangeEndFld.value()
        xmdloc = self.MainWindow.xmdLocFld.text()
        rigCheck = cmds.objExists('b_M_pelvis_v1_JNT')

        if rigCheck == False:
            print "Error: No rig to export"
        elif xmdloc == '':
            print 'Error: Please select an XMD export location'
        else:
            print xmdloc, startFrame, endFrame
            self.XMDCurrentConvert(xmdloc, startFrame, endFrame)


    def exportSingleAnim(self):
        fileName = self.MainWindow.fbxMaFileFld.text()
        xmdloc = self.MainWindow.xmdLocFld.text()

        if fileName == '':
            print 'Error: Please select an FBX or MA file'
        elif xmdloc == '':
            print 'Error: Please select an XMD export location'
        else:
            print fileName, xmdloc, startFrame, endFrame
            self.XMDSingleConvert(fileName, xmdloc)

    # Launches directory dialogue box and returns the destination directory
    def findDir(self):

        startingDir = ''
        destDir = QtGui.QFileDialog.getExistingDirectory(None, 'Open working directory', startingDir, QtGui.QFileDialog.ShowDirsOnly)
        destDir = destDir.replace('\\', '/')
        return destDir

    # Launches a file dialogue box and returns the selected file
    def findFile(self):
        fileTypes = "Filmbox (*.fbx);;Maya Ascii (*.ma);;Maya Binary (*.mb)"
        startingDir = ''
        file = QtGui.QFileDialog.getOpenFileName( None, 'Open File',startingDir, fileTypes )

        return file[0]

    # Gets the current playback time range and returns the start and end values
    def getCurRange(self):
        startFrame = cmds.playbackOptions(query=True, min=True)
        endFrame = cmds.playbackOptions(query=True, max=True)
        print startFrame, endFrame
        return startFrame, endFrame

    # Gets the animation range based on the pelvis keyframes and returns the start and end values
    def getAnimRange(self):
        try:
            startFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="first")
            endFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="last")
            return startFrame, endFrame
        except:
            print "No object name b_m_pelvis_v1_JNT was found"

    # Sets the range to the input values
    def setRange(self, startRange, endRange):
        self.MainWindow.rangeStartFld.setValue(startRange)
        self.MainWindow.rangeEndFld.setValue(endRange)

    # Exports the current file to XMD
    def XMDCurrentConvert(self, xmdpath, startFrame, endFrame):
        filePath = cmds.file(query = True, loc = True)
        fileName = (((filePath.split('/'))[-1]).split('.'))[0]
        xmdoptions = self.XMDAnimSettings(startFrame, endFrame)

        cmds.file(xmdpath + '/' + fileName + '.xmd', type='XMD Export', ea=True, options=xmdoptions, force=True)

        print xmdpath + '/' + filename + '.xmd', 'has been generated'

    # Reads the fbxfile and exports it to XMD
    def XMDSingleConvert(self, fbxfile, xmdpath):
        filename = (((fbxfile.split('/'))[-1].split('.'))[0])

        cmds.file (fbxfile, force=True, open=True)
        cmds.currentUnit (time='ntsc')
        startFrame, endFrame = self.getAnimRange()
        xmdoptions = self.XMDAnimSettings(startFrame, endFrame)
        cmds.file(xmdpath + '/' + filename + '.xmd', type='XMD Export', ea=True, options=xmdoptions, force=True)

        print xmdpath + '/' + filename + '.xmd', 'has been generated'

    # Batch converts FBX files into XMD files
    def XMDBatchConvert(self, fbxpath, xmdpath):

        fbxfiles = cmds.getFileList(folder=fbxpath, filespec='*.fbx')

        if len(fbxfiles) < 1:
            print "Error: There are no FBX/MA files in this directory, Please select one that does"
        else:
            for i in fbxfiles:

                self.XMDSingleConvert(fbxpath + '/' + i, xmdpath)

            print 'Exporting Finished!'

    # Settings for XMD Rigs
    def XMDRigSettings(self):
        xmdoptions = ("-ascii=1;"                      # 0 = binary output, 1 = ascii output
                      "-layers=0;"                     # Display Layers
                      "-rlayers=0;"                    # Render Layers
                      "-sets=0;"                       # Object Sets
                      "-stripNamespaces=1;"            # If true, namespaces are stripped from node names on export (including References)
                      "-dynamic_keyable_attrs=1;"      # If true, dynamic attributes are exported
                      "-dynamic_nonkeyable_attrs=0;"   # If true, dynamic non keyable attributes are exported
                      "-remove_scale=1;"               # Remove scale on export
                      "-scaling_factor=1.0;"           # Scaling Factor
                      "-material=0;"                   # Materials
                      "-textures=0;"                   # Texturing
                      "-shaders=0;"                    # Hardware Shaders
                      "-texture_filtering=0;"          # Extra Texture Info
                      "-camera=0;"                     # Cameras
                      "-light=0;"                      # Lights
                      "-locator=0;"                    # Locators
                      "-mesh=1;"                       # Meshes
                      "-nurbscurve=0;"                 # Nurbs Curves
                      "-nurbssurface=0;"               # Nurbs Surfaces
                      "-volumes=0;"                    # Volume Primitives
                      "-vtxcolours=0;"                 # Export Vertex Colours
                      "-vtxnormals=1;"                 # Export Vertex Normals
                      "-vtxuvs=0;"                     # Export Texture Coordinates
                      "-selective=0;"                  # Extract Important Xforms only
                      "-constraints=0;"                # Constraints
                      "-ik=0;"                         # Ik Chains
                      "-compact=0;"                    # Remove Orients & Pivots
                      "-blendshape=1;"                 # Blend Shapes
                      "-clusters=0;"                   # Clusters
                      "-jiggle=0;"                     # Jiggle deformers
                      "-lattice=0;"                    # Lattices (FFD's)
                      "-jointcluster=0;"               # Rigid Skinning
                      "-skinning=1;"                   # Smooth Skinning (SkinClusters)
                      "-nonlinear=0;"                  # Non-Linear Deformers
                      "-wire=0;"                       # Wire Deformers
                      "-wrap=0;"                       # Wrap Deformers
                      "-sculpt=0;"                     # Sculpt Deformers
                      "-field=0;"                      # Dynamics Fields
                      "-particles=0;"                  # Particles
                      "-anim=0;"                       # Animation
                      #"-sampled=1;"                   # Sampled animation
                      #"-animcurves=0;"                # Animation Curves
                      "-timeline=1;"                   # Use Timeline
                      "-start=1;"                      # Start Frame
                      "-end=25;")                      #End Frame

        return xmdoptions

    ## Settings for XMD Animations
    def XMDAnimSettings(self, start, end):
        xmdoptions = ("-ascii=1;"                      # 0 = binary output, 1 = ascii output
                      "-layers=0;"                     # Display Layers
                      "-rlayers=0;"                    # Render Layers
                      "-sets=0;"                       # Object Sets
                      "-stripNamespaces=1;"            # If true, namespaces are stripped from node names on export (including References)
                      "-dynamic_keyable_attrs=1;"      # If true, dynamic attributes are exported
                      "-dynamic_nonkeyable_attrs=0;"   # If true, dynamic non keyable attributes are exported
                      "-remove_scale=1;"               # Remove scale on export
                      "-scaling_factor=1.0;"           # Scaling Factor
                      "-material=0;"                   # Materials
                      "-textures=0;"                   # Texturing
                      "-shaders=0;"                    # Hardware Shaders
                      "-texture_filtering=0;"          # Extra Texture Info
                      "-camera=0;"                     # Cameras
                      "-light=0;"                      # Lights
                      "-locator=0;"                    # Locators
                      "-mesh=0;"                       # Meshes
                      "-nurbscurve=0;"                 # Nurbs Curves
                      "-nurbssurface=0;"               # Nurbs Surfaces
                      "-volumes=0;"                    # Volume Primitives
                      "-vtxcolours=0;"                 # Export Vertex Colours
                      "-vtxnormals=0;"                 # Export Vertex Normals
                      "-vtxuvs=0;"                     # Export Texture Coordinates
                      "-selective=0;"                  # Extract Important Xforms only
                      "-constraints=0;"                # Constraints
                      "-ik=0;"                         # Ik Chains
                      "-compact=0;"                    # Remove Orients & Pivots
                      "-blendshape=1;"                 # Blend Shapes
                      "-clusters=0;"                   # Clusters
                      "-jiggle=0;"                     # Jiggle deformers
                      "-lattice=0;"                    # Lattices (FFD's)
                      "-jointcluster=0;"               # Rigid Skinning
                      "-skinning=1;"                   # Smooth Skinning (SkinClusters)
                      "-nonlinear=0;"                  # Non-Linear Deformers
                      "-wire=0;"                       # Wire Deformers
                      "-wrap=0;"                       # Wrap Deformers
                      "-sculpt=0;"                     # Sculpt Deformers
                      "-field=0;"                      # Dynamics Fields
                      "-particles=0;"                  # Particles
                      "-anim=1;"                       # Animation
                      #"-sampled=1;"                   # Sampled animation
                      #"-animcurves=0;"                # Animation Curves
                      "-timeline=0;"                   # Use Timeline
                      "-start=" + str(start) + ";"     # Start Frame
                      "-end=" + str(end) + ";")        # End Frame
        return xmdoptions

    # Show the dialog
    def show(self):
        self.close()
        app = QtGui.QApplication.instance()
        self.MainWindow = self.loadUiWidget(self.uiFilePath)
        self.connectSignals()
        self.MainWindow.show()
        app.exec_()

    # Dispose the dialog
    def close(self):
        if self.MainWindow != None:
            self.MainWindow.close()
            self.MainWindow = None

# Open the Qt Dialog
dialog = xmdExportWindow()
dialog.show()