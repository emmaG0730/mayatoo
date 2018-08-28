import sys, _winreg
from PySide import QtCore, QtGui, QtUiTools
import svnPy

HKCU_USERENV = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Environment')
PROJECTPATH = _winreg.QueryValueEx(HKCU_USERENV,'SEASUNTOOLS')[0]
SCRIPTPATH = PROJECTPATH + 'DCC/Maya/scripts/VersionControl/'

class svnCheckout():
    # constructor
    def __init__(self):

        self.uiFilePath = SCRIPTPATH + 'svnLogin_UI.ui'
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
        self.MainWindow.btn_ok.clicked.connect(self.okSig)
        self.MainWindow.btn_cancel.clicked.connect(self.close)

    def okSig(self):
        svnPy.writeUserData(self.getUserData())
        self.close()

    # Gets the user data from the UI
    def getUserData(self):
        username = self.MainWindow.str_username.text()
        password = self.MainWindow.str_password.text()

        if username == 'username':
            print "Please enter username"

        elif password == 'password':
            print "Please enter password"

        else:
            print username, password

            return username, password

    # Updates the data on the window
    def updateData(self):
        encryptedData = svnPy.readUserData()

        if encryptedData == None:
            svnPy.readUserData()
            self.updateData()
        else:

            username, password = svnPy.decryptData(encryptedData)

            self.MainWindow.str_username.setText(username)
            self.MainWindow.str_password.setText(password)


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
        self.updateData()
        app.exec_()

    def close(self):
        if self.MainWindow != None:
            self.MainWindow.close()
            self.MainWindow = None


loginWin = svnCheckout()
loginWin.show()
