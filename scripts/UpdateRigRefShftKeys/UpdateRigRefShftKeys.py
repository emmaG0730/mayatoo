#!/usr/bin/python
#  -*- coding: iso-8859-15 -*

import sys, _winreg
from PySide import QtCore, QtGui, QtUiTools

HKCU_USERENV = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Environment')
PROJECTPATH = _winreg.QueryValueEx(HKCU_USERENV,'SEASUNTOOLS')[0]
SCRIPTPATH = 'R:/Jx4/tools/dcc/maya/scripts/UpdateRigRefShftKeys/'


class updateRigAnim():
    # constructor
    def __init__(self):
        self.uiFilePath = SCRIPTPATH + 'UpdateRigReference.ui'
        self.MainWindow = None

    # loading the ui element
    def loadUiWidget(self, uifilename):
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        ui = loader.load(uifile)
        uifile.close()
        return ui

    # Connects the signals from the UI
    def connectSignals(self):
        self.MainWindow.btn_export.clicked.connect(self.exportLocSig)
        self.MainWindow.btn_refRig.clicked.connect(self.findRefRigSig)
        self.MainWindow.btn_singleFile.clicked.connect(self.findSingleFileSig)
        self.MainWindow.btn_singleConvert.clicked.connect(self.singleConvertSig)
        self.MainWindow.btn_batchFile.clicked.connect(self.findBatchDirSig)
        self.MainWindow.btn_batchConvert.clicked.connect(self.batchConvertSig)
        self.MainWindow.actionChinese.triggered.connect(self.chineseSig)
        self.MainWindow.actionEnglish.triggered.connect(self.englishSig)

    # Updates the window to display chinese text
    def chineseSig(self):
        print "changing language to chinese"
        #self.MainWindow.menuLanguage.setTitle(b'语言'.decode(encoding='utf-8'))

    # Updates the window to display english text
    def englishSig(self):
        print "changing language to english"

    # Launches window to select export location
    def exportLocSig(self):
        print "Sets the export location"
        exportDir = self.findDirectory()
        self.MainWindow.s_exportLoc.setText(exportDir)

    # Launches window to select the reference rig
    def findRefRigSig(self):
        print "finds the reference rig"
        refFile = self.findFile("Maya Ascii (*.ma);;Maya Binary (*.mb)")
        self.MainWindow.s_refRig.setText(refFile)

    # Launches window to select animation to be converted
    def findSingleFileSig(self):
        print "finds the single file"
        singleFile = self.findFile("Maya Ascii (*.ma);;Maya Binary (*.mb)")
        self.MainWindow.s_singleFileLoc.setText(singleFile)

    # Converts single animation and exports the data
    def singleConvertSig(self):
        print "converts a single animation"
        singleFileLoc = self.getUIData('singleFileLoc')
        exportLoc = self.getUIData('exportLoc')
        controlNode = self.getUIData('controlNode')
        refLoc = self.getUIData('refLoc')

        if singleFileLoc == "":
            self.messageBox('Select a File', 'Error: No File Selected.\nPlease select an animation file to be converted')
        elif exportLoc == "":
            self.messageBox('Select a Directory', 'Error: No Export Directory Selected.\nPlease select an export directory')
        elif controlNode == "":
            self.messageBox('Missing Control Node', 'Error: No Control Node Set\nPlease enter top control node')
        elif refLoc == "":
            self.messageBox('Select a Reference Rig', 'Error: No Reference Rig Selected.\nPlease select a reference rig')
        else:
            singleFBX = self.getUIData('singleFBX')
            startFrame = self.getUIData('startFrame')
            print 'FBX:', singleFBX
            print 'Export Location:', exportLoc
            print 'Start Frame:', startFrame
            print 'Control Node:', controlNode
            print 'Animation File:', singleFileLoc

    # Launches window to select directory location of animation files
    def findBatchDirSig(self):
        print "finds the batch directory"
        batchDir = self.findDirectory()
        self.MainWindow.s_batchDirLoc.setText(batchDir)

    # Batch converts animations and exports them
    def batchConvertSig(self):
        batchDirLoc = self.getUIData('batchDirLoc')
        exportLoc = self.getUIData('exportLoc')
        controlNode = self.getUIData('controlNode')
        refLoc = self.getUIData('refLoc')

        if batchDirLoc == "":
            self.messageBox('Select a File', 'Error: No Directory Selected.\nPlease select a directory containing animations\nto be converted')
        elif exportLoc == "":
            self.messageBox('Select a Directory', 'Error: No Export Directory Selected.\nPlease select an export directory')
        elif controlNode == "":
            self.messageBox('Missing Control Node', 'Error: No Control Node Set\nPlease enter top control node')
        elif refLoc == "":
            self.messageBox('Select a Reference Rig', 'Error: No Reference Rig Selected.\nPlease select a reference rig')
        else:
            b_batchFBX = self.getUIData('batchFBX')
            startFrame = self.getUIData('startFrame')
            print 'FBX:', b_batchFBX
            print 'Export Location:', exportLoc
            print 'Start Frame:', startFrame
            print 'Control Node:', controlNode
            print 'Animation File:', batchDirLoc

    # Launches file directory explorer and retuns directory path
    def findDirectory(self):
        startingDir = ''
        destDir = QtGui.QFileDialog.getExistingDirectory(None, 'Open working directory', startingDir, QtGui.QFileDialog.ShowDirsOnly)
        destDir = destDir.replace('\\', '/')
        return destDir

    # Launches file explorer and returns file path
    def findFile(self, fileTypes):
        startingDir = ''
        file = QtGui.QFileDialog.getOpenFileName( None, 'Open File',startingDir, fileTypes )

        return file[0]

    # Returns the data from the UI that has been requested
    def getUIData(self, uiDataIndex):
        uiData = {'exportLoc':self.MainWindow.s_exportLoc.text(),
                  'refLoc':self.MainWindow.s_refRig.text(),
                  'startFrame':self.MainWindow.i_startFrame.value(),
                  'controlNode':self.MainWindow.s_contNode.text(),
                  'singleFileLoc':self.MainWindow.s_singleFileLoc.text(),
                  'singleFBX':self.MainWindow.b_singleExportFBX.isChecked(),
                  'batchDirLoc':self.MainWindow.s_batchDirLoc.text(),
                  'batchFBX':self.MainWindow.b_batchExportFBX.isChecked()
                  }

        return uiData[uiDataIndex]

    # Processes data to convert animation data
    def pipelineProcessor(self, exportLoc, refRig, startFrame, controlNode, b_batch, b_fbx, sourceLoc):
        print "process pipeline"

    # Launches a message box with information
    def messageBox(self, title, message):
        self.msgBox = QtGui.QMessageBox()
        self.msgBox.setWindowTitle(title)
        self.msgBox.setText(message)
        self.msgBox.exec_()

    # ---------------------------- Show UI -----------------------------
    def show(self):
        self.close()
        app = QtGui.QApplication(sys.argv)
        self.MainWindow = self.loadUiWidget(self.uiFilePath)
        self.MainWindow.setWindowFlags(self.MainWindow.windowFlags())  # | QtCore.Qt.WindowStaysOnTopHint)
        self.connectSignals()
        self.MainWindow.show()
        app.exec_()

    def close(self):
        if self.MainWindow != None:
            self.MainWindow.close()
            self.MainWindow = None

animConvertWin = updateRigAnim()
animConvertWin.show()
