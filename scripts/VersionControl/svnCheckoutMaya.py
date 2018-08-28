#!/usr/bin/python
#  -*- coding: iso-8859-15 -*

import sys, svnPy, locale, subprocess, _winreg
from PySide import QtCore, QtGui, QtUiTools

HKCU_USERENV = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'Environment')
PROJECTPATH = _winreg.QueryValueEx(HKCU_USERENV,'SEASUNTOOLS')[0]
SCRIPTPATH = PROJECTPATH + 'DCC/Maya/scripts/VersionControl/'


class svnCheckout():
    # constructor
    def __init__(self):

        self.uiFilePath = SCRIPTPATH + 'svnSubmit_UI.ui'
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
        self.MainWindow.btn_submit.clicked.connect(self.submitSig)
        self.MainWindow.btn_cancel.clicked.connect(self.close)
        self.MainWindow.btn_revert.clicked.connect(self.revertSig)
        self.MainWindow.actionChinese.triggered.connect(self.chineseSig)
        self.MainWindow.actionEnglish.triggered.connect(self.englishSig)
        self.MainWindow.actionDeleteSVN.triggered.connect(self.deleteSVN)
        self.MainWindow.actionSVNLogin.triggered.connect(self.SVNLogin)

    def chineseSig(self):
        print "changing language to chinese"
        self.MainWindow.menuLanguage.setTitle(b'语言'.decode(encoding='utf-8'))
        self.MainWindow.l_file.setText(b'文件'.decode(encoding='utf-8'))
        self.MainWindow.l_info.setText(b'信息'.decode(encoding='utf-8'))
        self.MainWindow.l_comment.setText(b'提交描述 （请尽量使用英文)'.decode(encoding='utf-8'))
        self.MainWindow.btn_submit.setText(b'提交'.decode(encoding='utf-8'))
        self.MainWindow.btn_cancel.setText(b'取消'.decode(encoding='utf-8'))
        self.MainWindow.btn_revert.setText(b'回滚'.decode(encoding='utf-8'))
        self.MainWindow.menuExtraOptions.setTitle(b'更多选项'.decode(encoding='utf-8'))
        self.MainWindow.actionDeleteSVN.setText(b'从SVN删除'.decode(encoding='utf-8'))

    def englishSig(self):
        self.MainWindow.menuLanguage.setTitle('Language')
        self.MainWindow.l_file.setText('File:')
        self.MainWindow.l_info.setText('Information:')
        self.MainWindow.l_comment.setText('Comment (Please use English as much as possible)')
        self.MainWindow.btn_submit.setText('Submit')
        self.MainWindow.btn_cancel.setText('Cancel')
        self.MainWindow.btn_revert.setText('Revert')
        self.MainWindow.menuExtraOptions.setTitle('Extra Options')
        self.MainWindow.actionDeleteSVN.setText('Delete from SVN')

    def submitSig(self):
        message = self.MainWindow.s_comment.toPlainText().encode('utf8')
        messageLength = len(message)
        if messageLength < 5:
            self.messageBox("Error", "Comment is too short\nPlease give more description")
        else:
            filePath = self.MainWindow.s_file.text()
            fileName = (filePath.split('/'))[-1]
            svnPy.commit(filePath, message)
            self.messageBox("SVN", fileName + " has been submitted to SVN")
            self.close()

    def deleteSVN(self):
        filePath = self.MainWindow.s_file.text()
        fileName = (filePath.split('/'))[-1]
        svnPy.delete(filePath)
        svnPy.commit(filePath, fileName + " has been deleted")
        self.messageBox("Delete", fileName + " has been deleted")
        self.close()

    def revertSig(self):
        filePath = self.MainWindow.s_file.text()
        fileName = (filePath.split('/'))[-1]
        svnPy.revert(filePath)
        self.messageBox("Revert", fileName + " has been reverted")
        self.close()


    def SVNLogin(self):
        global SCRIPTPATH

        subprocess.Popen('python "' + SCRIPTPATH + 'svnLogin.py"', shell=True)


    def firstUpdate(self):
        Lang = locale.getdefaultlocale()[0]

        if Lang == 'en-CH':
            self.chineseSig()
        else:
            self.englishSig()

        args = sys.argv
        if len(args) < 2:
            print "yay"
        else:
            fileURL = args[1]
            fileName = (fileURL.split('/'))[-1]
            self.MainWindow.s_info.setText(fileName)
            self.MainWindow.s_file.setText(fileURL)


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
        self.firstUpdate()
        app.exec_()

    def close(self):
        if self.MainWindow != None:
            self.MainWindow.close()
            self.MainWindow = None


loginWin = svnCheckout()
loginWin.show()
