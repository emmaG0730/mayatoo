# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'XMDExporterExternal.ui'
#
# Created: Wed Dec 09 13:55:23 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass

from PySide import QtCore, QtGui
import sys
import maya.cmds as cmds

class Ui_xmdExportWin(object):
    def setupUi(self, xmdExportWin):
        xmdExportWin.setObjectName("xmdExportWin")
        xmdExportWin.resize(800, 570)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(xmdExportWin.sizePolicy().hasHeightForWidth())
        xmdExportWin.setSizePolicy(sizePolicy)
        xmdExportWin.setMinimumSize(QtCore.QSize(800, 570))
        xmdExportWin.setMaximumSize(QtCore.QSize(800, 570))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(96, 81, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 181, 155))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(236, 232, 226))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(96, 81, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 181, 155))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(236, 232, 226))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 181, 155))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(236, 232, 226))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(236, 232, 226))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        xmdExportWin.setPalette(palette)
        xmdExportWin.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(xmdExportWin)
        self.centralwidget.setObjectName("centralwidget")
        self.exportTxt = QtGui.QLabel(self.centralwidget)
        self.exportTxt.setGeometry(QtCore.QRect(10, 10, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.exportTxt.setFont(font)
        self.exportTxt.setScaledContents(False)
        self.exportTxt.setObjectName("exportTxt")
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 120, 781, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.xmdLocTxt = QtGui.QLabel(self.centralwidget)
        self.xmdLocTxt.setGeometry(QtCore.QRect(10, 60, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.xmdLocTxt.setFont(font)
        self.xmdLocTxt.setScaledContents(False)
        self.xmdLocTxt.setObjectName("xmdLocTxt")
        self.xmdBtn = QtGui.QPushButton(self.centralwidget)
        self.xmdBtn.setGeometry(QtCore.QRect(690, 50, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.xmdBtn.setFont(font)
        self.xmdBtn.setStyleSheet("background-color: rgb(165, 152, 126);\n"
"color: rgb(255, 255, 255);\n"
"border:none")
        self.xmdBtn.setObjectName("xmdBtn")
        self.singleTxt = QtGui.QLabel(self.centralwidget)
        self.singleTxt.setGeometry(QtCore.QRect(10, 150, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.singleTxt.setFont(font)
        self.singleTxt.setScaledContents(False)
        self.singleTxt.setObjectName("singleTxt")
        self.fbxMaBtn = QtGui.QPushButton(self.centralwidget)
        self.fbxMaBtn.setEnabled(True)
        self.fbxMaBtn.setGeometry(QtCore.QRect(690, 210, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.fbxMaBtn.setFont(font)
        self.fbxMaBtn.setAutoFillBackground(False)
        self.fbxMaBtn.setStyleSheet("background-color: rgb(165, 152, 126);\n"
"color: rgb(255, 255, 255);\n"
"border:none")
        self.fbxMaBtn.setObjectName("fbxMaBtn")
        self.fbxMaFileTxt = QtGui.QLabel(self.centralwidget)
        self.fbxMaFileTxt.setGeometry(QtCore.QRect(10, 220, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.fbxMaFileTxt.setFont(font)
        self.fbxMaFileTxt.setScaledContents(False)
        self.fbxMaFileTxt.setObjectName("fbxMaFileTxt")
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 320, 781, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.fbxMaDirBtn = QtGui.QPushButton(self.centralwidget)
        self.fbxMaDirBtn.setGeometry(QtCore.QRect(690, 400, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.fbxMaDirBtn.setFont(font)
        self.fbxMaDirBtn.setStyleSheet("background-color: rgb(165, 152, 126);\n"
"color: rgb(255, 255, 255);\n"
"border:none")
        self.fbxMaDirBtn.setObjectName("fbxMaDirBtn")
        self.batchTxt = QtGui.QLabel(self.centralwidget)
        self.batchTxt.setGeometry(QtCore.QRect(10, 340, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.batchTxt.setFont(font)
        self.batchTxt.setScaledContents(False)
        self.batchTxt.setObjectName("batchTxt")
        self.fbxMaDirTxt = QtGui.QLabel(self.centralwidget)
        self.fbxMaDirTxt.setGeometry(QtCore.QRect(10, 410, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.fbxMaDirTxt.setFont(font)
        self.fbxMaDirTxt.setScaledContents(False)
        self.fbxMaDirTxt.setObjectName("fbxMaDirTxt")
        self.batchExportBtn = QtGui.QPushButton(self.centralwidget)
        self.batchExportBtn.setGeometry(QtCore.QRect(290, 470, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.batchExportBtn.setFont(font)
        self.batchExportBtn.setStyleSheet("background-color: rgb(165, 152, 126);\n"
"color: rgb(255, 255, 255);\n"
"border:none")
        self.batchExportBtn.setObjectName("batchExportBtn")
        self.xmdLocFld = QtGui.QLineEdit(self.centralwidget)
        self.xmdLocFld.setGeometry(QtCore.QRect(170, 50, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.xmdLocFld.setFont(font)
        self.xmdLocFld.setStyleSheet("border:none;\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.xmdLocFld.setReadOnly(True)
        self.xmdLocFld.setObjectName("xmdLocFld")
        self.fbxMaFileFld = QtGui.QLineEdit(self.centralwidget)
        self.fbxMaFileFld.setGeometry(QtCore.QRect(160, 210, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.fbxMaFileFld.setFont(font)
        self.fbxMaFileFld.setStyleSheet("border:none;\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.fbxMaFileFld.setReadOnly(True)
        self.fbxMaFileFld.setObjectName("fbxMaFileFld")
        self.fbxMaDirFld = QtGui.QLineEdit(self.centralwidget)
        self.fbxMaDirFld.setGeometry(QtCore.QRect(160, 400, 511, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.fbxMaDirFld.setFont(font)
        self.fbxMaDirFld.setStyleSheet("border:none;\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.fbxMaDirFld.setReadOnly(True)
        self.fbxMaDirFld.setObjectName("fbxMaDirFld")
        self.singleExportBtn = QtGui.QPushButton(self.centralwidget)
        self.singleExportBtn.setGeometry(QtCore.QRect(290, 270, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.singleExportBtn.setFont(font)
        self.singleExportBtn.setStyleSheet("background-color: rgb(165, 152, 126);\n"
"color: rgb(255, 255, 255);\n"
"border:none")
        self.singleExportBtn.setObjectName("singleExportBtn")
        xmdExportWin.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(xmdExportWin)
        self.statusbar.setObjectName("statusbar")
        xmdExportWin.setStatusBar(self.statusbar)

        self.retranslateUi(xmdExportWin)
        QtCore.QMetaObject.connectSlotsByName(xmdExportWin)

    def retranslateUi(self, xmdExportWin):
        xmdExportWin.setWindowTitle(QtGui.QApplication.translate("xmdExportWin", "XMD Exporter", None, QtGui.QApplication.UnicodeUTF8))
        self.exportTxt.setText(QtGui.QApplication.translate("xmdExportWin", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.xmdLocTxt.setText(QtGui.QApplication.translate("xmdExportWin", "XMD Location", None, QtGui.QApplication.UnicodeUTF8))
        self.xmdBtn.setText(QtGui.QApplication.translate("xmdExportWin", "···", None, QtGui.QApplication.UnicodeUTF8))
        self.singleTxt.setText(QtGui.QApplication.translate("xmdExportWin", "Single", None, QtGui.QApplication.UnicodeUTF8))
        self.fbxMaBtn.setText(QtGui.QApplication.translate("xmdExportWin", "···", None, QtGui.QApplication.UnicodeUTF8))
        self.fbxMaFileTxt.setText(QtGui.QApplication.translate("xmdExportWin", "FBX/MA File", None, QtGui.QApplication.UnicodeUTF8))
        self.fbxMaDirBtn.setText(QtGui.QApplication.translate("xmdExportWin", "···", None, QtGui.QApplication.UnicodeUTF8))
        self.batchTxt.setText(QtGui.QApplication.translate("xmdExportWin", "Batch", None, QtGui.QApplication.UnicodeUTF8))
        self.fbxMaDirTxt.setText(QtGui.QApplication.translate("xmdExportWin", "FBX/MA Dir", None, QtGui.QApplication.UnicodeUTF8))
        self.batchExportBtn.setText(QtGui.QApplication.translate("xmdExportWin", "Batch Export", None, QtGui.QApplication.UnicodeUTF8))
        self.singleExportBtn.setText(QtGui.QApplication.translate("xmdExportWin", "Export Animation", None, QtGui.QApplication.UnicodeUTF8))

    def connectSignals(self):
        self.xmdBtn.clicked.connect(self.xmdLocBtnSig)
        self.fbxMaBtn.clicked.connect(self.fbxMaBtnSig)
        self.singleExportBtn.clicked.connect(self.singleExportSig)
        self.fbxMaDirBtn.clicked.connect(self.fbxMaDirLocBtnSig)
        self.batchExportBtn.clicked.connect(self.batchExportSig)

    def xmdLocBtnSig(self):
        xmdloc = self.findDir()
        self.xmdLocFld.setText(xmdloc)

    def fbxMaBtnSig(self):
        fbxMaLoc = self.findFile()
        self.fbxMaFileFld.setText(fbxMaLoc)

    def singleExportSig(self):
        self.exportSingleAnim()

    def fbxMaDirLocBtnSig(self):
        fbxMaDirLoc = self.findDir()
        self.fbxMaDirFld.setText(fbxMaDirLoc)

    def batchExportSig(self):
        xmdloc = self.xmdLocFld.text()
        fbxmadir = self.fbxMaDirFld.text()

        if xmdloc == '':
            print "Error: No XMD export location has been set.  Please set an XMD export location"
        elif fbxmadir == '':
            print "Error: No FBX/MA Directory has been set.  Please set an FBX/MA import location"
        else:

            self.XMDBatchConvert(fbxmadir, xmdloc)

    def exportSingleAnim(self):
        fileName = self.fbxMaFileFld.text()
        xmdloc = self.xmdLocFld.text()

        if fileName == '':
            print 'Error: Please select an FBX or MA file'
        elif xmdloc == '':
            print 'Error: Please select an XMD export location'
        else:
            print fileName, xmdloc, startFrame, endFrame
            self.XMDSingleConvert(fileName, xmdloc)

    def findDir(self):

        startingDir = ''
        destDir = QtGui.QFileDialog.getExistingDirectory(None, 'Open working directory', startingDir, QtGui.QFileDialog.ShowDirsOnly)
        destDir = destDir.replace('\\', '/')
        return destDir

    def findFile(self):
        fileTypes = "Filmbox (*.fbx);;Maya Ascii (*.ma);;Maya Binary (*.mb)"
        startingDir = ''
        file = QtGui.QFileDialog.getOpenFileName( None, 'Open File',startingDir, fileTypes )

        return file[0]

    # Gets the animation range based on the pelvis keyframes and returns the start and end values
    def getAnimRange(self):
        try:
            startFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="first")
            endFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="last")
            return startFrame, endFrame
        except:
            print "No object name b_m_pelvis_v1_JNT was found"

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

def showWin():
        if __name__ == "__main__":
            app = QtGui.QApplication(sys.argv)
            xmdExportWin = QtGui.QMainWindow()
            ui = Ui_xmdExportWin()
            ui.setupUi(xmdExportWin)
            Ui_xmdExportWin.connectSignals(ui)
            xmdExportWin.show()
            sys.exit(app.exec_())

showWin()