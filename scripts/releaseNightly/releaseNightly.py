#-----------------------------------------------------------------------------------#
# Scripted By: Linh Nguyen                                                          #
# Description: Allows for switching the Maya tools, Rigs, and Characters to         #
# Release or Nightly builds                                                         #
#-----------------------------------------------------------------------------------#

import sys
sys.path.append('../../../../')
import internal.qdarkstyle as style
import releaseNightly_UI
from PySide import QtGui
import checkReleaseStatus

class ReleaseNightly():

    # Constructs the QPaint device
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.ui = releaseNightly_UI.Ui_MainWindow()

    # Connects the buttons to the methods
    def connect_signals(self):
        self.ui.btn_releaseTools.clicked.connect(self.releaseTools)
        self.ui.btn_releaseRig.clicked.connect(self.releaseRig)
        self.ui.btn_nightlyTools.clicked.connect(self.nightlyTools)
        self.ui.btn_nightlyRig.clicked.connect(self.nightlyRig)

    # Sets Maya tools to release mode
    def releaseTools(self):
        self.ui.statusbar.showMessage('processing...')
        checkReleaseStatus.toolsRelease()
        self.ui.l_toolsMode.setText('Release')
        self.ui.statusbar.showMessage('Tools mode is now in Release')


    # Sets rig and character to release mode
    def releaseRig(self):
        self.ui.statusbar.showMessage('processing...')
        output = checkReleaseStatus.rigRelease()
        self.ui.l_rigMode.setText('Release')
        self.ui.statusbar.showMessage(output)

    # Sets Maya tools to nightly mode
    def nightlyTools(self):
        self.ui.statusbar.showMessage('processing...')
        checkReleaseStatus.toolsNightly()
        self.ui.l_toolsMode.setText('Nightly')
        self.ui.statusbar.showMessage('Tools mode is now in Nightly')

    # Sets rig and character to nightly mode
    def nightlyRig(self):
        self.ui.statusbar.showMessage('processing...')
        output = checkReleaseStatus.rigNightly()
        self.ui.l_rigMode.setText('Nightly')
        self.ui.statusbar.showMessage(output)

    # Calls the UI
    def main(self):
        self.MainWindow = QtGui.QMainWindow()
        self.ui.setupUi(self.MainWindow)
        self.app.setStyleSheet(style.load_stylesheet(pyside=True))
        self.connect_signals()
        self.MainWindow.show()
        sys.exit(self.app.exec_())

rn = ReleaseNightly()
rn.main()