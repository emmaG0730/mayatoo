from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as omui
import starmanExporter.starman_ui as starman_ui
import starmanExporter.sm_exportRig as sm_exportRig
import logging
import datetime
import maya.cmds as cmds

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class ControlMainWindow(QtGui.QDialog):

    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.ui = starman_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.namespace = 'inputFile:'
        self.startingDir = 'R:/Jx4/tools/dcc/maya/scripts/starmanExporter/starman_settings/'
        self.export_starting_dir = 'R:/Jx4/client/GameWorld/Character/starMan/'
        self.sm_settings_file = self.startingDir + 'sm_data.json'
        self.logpath = 'R:/Jx4/tools/dcc/maya/scripts/starmanExporter/logs/'
        self.current_time = datetime.datetime.now()
        self.logging = logging.getLogger(__name__)
        hdlr = logging.FileHandler(self.logpath + 'starman_'
                                   + str(self.current_time.year) + '_'
                                   + str(self.current_time.month) + '_'
                                   + str(self.current_time.day) + '_'
                                   + str(self.current_time.hour) + '_'
                                   + str(self.current_time.minute) + '_'
                                   + str(self.current_time.second) + '_' + '.log')
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logging.addHandler(hdlr)
        self.logging.setLevel(logging.INFO)

        self.ui.btn_file.clicked.connect(self.file_signal)
        self.ui.btn_directory.clicked.connect(self.directory_signal)
        self.ui.btn_export.clicked.connect(self.export_signal)

        self.update_gui()

    def file_signal(self):
        fileTypes = "JSON (*.json)"

        self.sm_settings_file = QtGui.QFileDialog.getOpenFileName( self, 'Open File',self.startingDir, fileTypes )[0]
        print self.sm_settings_file

    def directory_signal(self):
        destDir = QtGui.QFileDialog.getExistingDirectory(None, 'Open working directory', self.export_starting_dir,
                                                         QtGui.QFileDialog.ShowDirsOnly)
        destDir = destDir.replace('\\', '/')
        self.ui.s_export_loc.setText(destDir)

    def export_signal(self):
        self.get_gui_data()
        self.get_file_name()
        self.get_character_version()
        self.get_export_location()
        print '----------------------------'
        print self.sm_settings_file
        print self.filename
        print self.namespace
        print self.type
        print self.master_controller
        print self.export_location
        print self.logging
        print '----------------------------'
        sm_export = sm_exportRig.sm_export_rig(self.sm_settings_file, self.filename, self.namespace, self.type,
                                               self.master_controller, self.export_location, self.logging)
        sm_export.check_scene()
        sm_export.get_animation_data()

    def get_file_name(self):
        print 'gets the current file name'
        self.filename = cmds.file(query = True, sceneName = True, shortName = True)

    def get_export_location(self):
        self.export_location = self.ui.s_export_loc.text()

    def get_character_version(self):
        if cmds.objExists('c_M_master_v1_CTRL') or cmds.objExists(self.namespace + 'c_M_master_v1_CTRL'):
            self.master_controller = 'c_M_master_v1_CTRL'
            self.char_version = 'current'
        elif cmds.objExists('b_M_pelvis_v1_JNT'):
            self.master_controller = 'b_M_pelvis_v1_JNT'
            self.char_version = 'legacy'

    def update_gui(self):
        self.ui.s_sman_data.setText(self.sm_settings_file)
        self.ui.s_namespace.setText(self.namespace)
        self.ui.s_export_loc.setText(self.export_starting_dir)

    def get_gui_data(self):
        self.sm_settings_file = self.ui.s_sman_data.text()
        self.namespace = self.ui.s_namespace.text()
        self.b_loop = self.ui.cb_loop.isChecked()
        print self.b_loop
        if self.ui.radio_integer.isChecked():
            self.type = 'integer'
        else:
            self.type = 'float'


myWin = ControlMainWindow(parent=maya_main_window())
myWin.show()