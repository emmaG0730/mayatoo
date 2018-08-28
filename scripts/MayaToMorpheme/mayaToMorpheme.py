from PySide import QtCore, QtGui, QtUiTools
import shiboken
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import MayaToMorpheme.mayaToMorpheme_maya as maya2m

## This class is used to open a Qt window in Maya using PySide
class xmdExportWindow():

    ## Constructor
    def __init__(self):
        self.uiFilePath = 'Y:/ToolBox/DCC/Maya/scripts/MayaToMorpheme/mayaToMorpheme_ui.ui'
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
        self.MainWindow.btn_dir.clicked.connect(self.dirSig)
        self.MainWindow.btn_animRange.clicked.connect(self.animRangeSig)
        self.MainWindow.btn_curRange.clicked.connect(self.curRangeSig)
        self.MainWindow.btn_fbxRig.clicked.connect(self.fbxRigSig)
        self.MainWindow.btn_fbxAnm.clicked.connect(self.fbxAnmSig)
        self.MainWindow.btn_xmdRig.clicked.connect(self.xmdRigSig)
        self.MainWindow.btn_xmdAnm.clicked.connect(self.xmdAnmSig)

    # ----------------------------- Signals ---------------------------------
    def dirSig(self):
        print 'get directory'
        directory = self.findDir()
        self.MainWindow.s_dir.setText(directory)

    def animRangeSig(self):
        start, end = maya2m.getAnimRange()
        self.MainWindow.i_start.setValue(start)
        self.MainWindow.i_end.setValue(end)

    def curRangeSig(self):
        start, end = maya2m.getCurRange()
        self.MainWindow.i_start.setValue(start)
        self.MainWindow.i_end.setValue(end)

    def fbxRigSig(self):
        dir = self.getData()

        if dir == '':
            print 'no directory selected'
        else:
            filename = maya2m.getSceneName()
            maya2m.selectRig()
            maya2m.exportFBX(dir, filename)

    def fbxAnmSig(self):
        dir = self.getData()

        if dir == '':
            print 'no directory selected'
        else:
            filename = maya2m.getSceneName()
            maya2m.selectAnim()
            maya2m.exportFBX(dir, filename)

    def xmdRigSig(self):
        dir = self.getData()

        if dir == '':
            print 'no directory selected'
        else:
            start = self.MainWindow.i_start.value()
            end = self.MainWindow.i_end.value()
            filename = maya2m.getSceneName()
            maya2m.selectAnim()
            maya2m.exportFBX(dir, filename, 1, start, end)

    def xmdAnmSig(self):
        dir = self.getData()

        if dir == '':
            print 'no directory selected'
        else:
            start = self.MainWindow.i_start.value()
            end = self.MainWindow.i_end.value()
            filename = maya2m.getSceneName()
            maya2m.selectAnim()
            maya2m.exportXMD(dir, filename, 2, start, end)

    # Launches directory dialogue box and returns the destination directory
    def findDir(self):

        startingDir = ''
        destDir = QtGui.QFileDialog.getExistingDirectory(None, 'Open working directory', startingDir, QtGui.QFileDialog.ShowDirsOnly)
        destDir = destDir.replace('\\', '/')
        return destDir

    def getData(self):
        dir = self.MainWindow.s_dir.text()
        return dir

    def loadPlugins(self):
        maya2m.loadFBXPlugin()
        maya2m.loadXMDPlugin()

    def update(self):
        start, end = maya2m.getAnimRange()
        self.MainWindow.i_start.setValue(start)
        self.MainWindow.i_end.setValue(end)

    # Show the dialog
    def show(self):
        self.close()
        app = QtGui.QApplication.instance()
        self.MainWindow = self.loadUiWidget(self.uiFilePath)
        self.connectSignals()
        self.loadPlugins()
        self.MainWindow.show()
        self.update()
        app.exec_()

    # Dispose the dialog
    def close(self):
        if self.MainWindow != None:
            self.MainWindow.close()
            self.MainWindow = None

# Open the Qt Dialog
dialog = xmdExportWindow()
dialog.show()