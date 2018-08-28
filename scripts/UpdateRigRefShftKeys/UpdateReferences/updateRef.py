import sys
import _winreg
import subprocess
from PySide import QtCore, QtGui, QtUiTools

HKLM_MAYA_PATH = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Autodesk\\Maya\\2016\\Setup\\InstallPath')
MAYAPATH = _winreg.QueryValueEx(HKLM_MAYA_PATH,'MAYA_INSTALL_LOCATION')[0]

class updateReference():
    # constructor
    def __init__(self):
        self.uiFilePath = 'R:/Jx4/tools/dcc/maya/scripts/UpdateRigRefShftKeys/UpdateReferences/UpdateRef_UI.ui'
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
        self.MainWindow.btn_dir.clicked.connect(self.findDirSig)
        self.MainWindow.btn_file.clicked.connect(self.findFileSig)
        self.MainWindow.btn_batchUpdate.clicked.connect(self.batchSig)

    # Returns the directory path
    def findDirSig(self):
        startingDir = 'w:'
        destDir = QtGui.QFileDialog.getExistingDirectory(None, 'Open working directory', startingDir, QtGui.QFileDialog.ShowDirsOnly)
        destDir = destDir.replace('\\', '/')
        self.MainWindow.s_animDir.setText(destDir)

    # Returns the file selected
    def findFileSig(self):
        fileTypes = "Maya Ascii (*.ma)"
        startingDir = 'w:'
        file = QtGui.QFileDialog.getOpenFileName(None, 'Open File', startingDir, fileTypes )
        self.MainWindow.s_refRig.setText(file[0])

    # batch update the files
    def batchSig(self):

        animDir = self.MainWindow.s_animDir.text()
        refRig = self.MainWindow.s_refRig.text()
        namespace = self.MainWindow.s_namespace.text()

        if animDir == '':
            self.messageBox('Missing Directory', 'No animation directory selected.\nPlease select an animation directory')
        elif refRig == '':
            self.messageBox('Missing File', 'No reference rig selected.\nPlease select a reference rig')
        elif namespace == '':
            self.messageBox('No Namespace', 'No namespace set.\nPlease type in a namespace')
        else:
            print ('"' + MAYAPATH + '\\bin\\mayapy.exe" ' +
                             '"R:/Jx4/tools/dcc/maya/scripts/UpdateRigRefShftKeys/UpdateReferences/updateReferences.py" ' +
                             animDir + ' ' + refRig + ' ' + namespace)
            subprocess.Popen('"' + MAYAPATH + '\\bin\\mayapy.exe" ' +
                             '"R:/Jx4/tools/dcc/maya/scripts/UpdateRigRefShftKeys/UpdateReferences/updateReferences.py" ' +
                             animDir + ' ' + refRig + ' ' + namespace)


    # Creates a message box
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

refWin = updateReference()
refWin.show()