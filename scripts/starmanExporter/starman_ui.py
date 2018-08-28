# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\SeasunProjects\JX4_Data\Jx4\tools\dcc\maya\scripts\starmanExporter\starman_ui.ui'
#
# Created: Mon Aug 22 16:10:29 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(381, 241)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_file = QtGui.QPushButton(Dialog)
        self.btn_file.setObjectName("btn_file")
        self.gridLayout.addWidget(self.btn_file, 0, 2, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.s_sman_data = QtGui.QLineEdit(Dialog)
        self.s_sman_data.setMinimumSize(QtCore.QSize(200, 0))
        self.s_sman_data.setObjectName("s_sman_data")
        self.gridLayout.addWidget(self.s_sman_data, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.s_export_loc = QtGui.QLineEdit(Dialog)
        self.s_export_loc.setObjectName("s_export_loc")
        self.gridLayout.addWidget(self.s_export_loc, 1, 1, 1, 1)
        self.btn_directory = QtGui.QPushButton(Dialog)
        self.btn_directory.setObjectName("btn_directory")
        self.gridLayout.addWidget(self.btn_directory, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.s_namespace = QtGui.QLineEdit(Dialog)
        self.s_namespace.setObjectName("s_namespace")
        self.horizontalLayout.addWidget(self.s_namespace)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cb_loop = QtGui.QCheckBox(Dialog)
        self.cb_loop.setObjectName("cb_loop")
        self.horizontalLayout_3.addWidget(self.cb_loop)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 75))
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")
        self.radio_integer = QtGui.QRadioButton(self.groupBox)
        self.radio_integer.setGeometry(QtCore.QRect(20, 30, 89, 16))
        self.radio_integer.setChecked(True)
        self.radio_integer.setObjectName("radio_integer")
        self.radio_float = QtGui.QRadioButton(self.groupBox)
        self.radio_float.setGeometry(QtCore.QRect(20, 50, 89, 16))
        self.radio_float.setObjectName("radio_float")
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalSlider = QtGui.QSlider(Dialog)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_2.addWidget(self.horizontalSlider, 0, 3, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.i_reduce_keys = QtGui.QSpinBox(Dialog)
        self.i_reduce_keys.setMinimumSize(QtCore.QSize(40, 0))
        self.i_reduce_keys.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.i_reduce_keys.setMinimum(1)
        self.i_reduce_keys.setMaximum(100)
        self.i_reduce_keys.setObjectName("i_reduce_keys")
        self.gridLayout_2.addWidget(self.i_reduce_keys, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        self.btn_export = QtGui.QPushButton(Dialog)
        self.btn_export.setObjectName("btn_export")
        self.gridLayout_4.addWidget(self.btn_export, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL("valueChanged(int)"), self.i_reduce_keys.setValue)
        QtCore.QObject.connect(self.i_reduce_keys, QtCore.SIGNAL("valueChanged(int)"), self.horizontalSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Starman Exporter", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_file.setText(QtGui.QApplication.translate("Dialog", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Starman Data", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Export Location", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_directory.setText(QtGui.QApplication.translate("Dialog", "Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Namespace", None, QtGui.QApplication.UnicodeUTF8))
        self.cb_loop.setText(QtGui.QApplication.translate("Dialog", "Loop", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Data Type", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_integer.setText(QtGui.QApplication.translate("Dialog", "Integer", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_float.setText(QtGui.QApplication.translate("Dialog", "Float", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Keep Keys", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export.setText(QtGui.QApplication.translate("Dialog", "Export", None, QtGui.QApplication.UnicodeUTF8))
