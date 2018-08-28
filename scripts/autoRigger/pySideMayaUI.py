import os
import sys
import glob
import json
import getpass
import platform
import datetime
import maya.cmds as cmds
import maya.mel as mel
import shiboken
import maya.OpenMayaUI as mui
import os
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
try:
    from PyQt4 import QtCore as qtc
    from PyQt4 import QtGui as qt
except ImportError:
    from PySide import QtCore as qtc
    from PySide import QtGui as qt
try:
    _fromUtf8 = qt.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

global uiIsBuildable
global scaleVar

scaleVar = ''
uiIsBuildable = True;
path = "R:/Jx4/tools/dcc/maya/scripts/autoRigger/"
width = 500
height = 700
width1 = 1200
height1 = 1000
officialTitle = "window"

##################################################################
#                         MODULES                                #
##################################################################
module = path+'locCreate.py'
print module
sys.path.append(os.path.dirname(os.path.expanduser(module)))
import locCreate
reload (locCreate)

module = path+'jointRecreate.py'
print module
sys.path.append(os.path.dirname(os.path.expanduser(module)))
import jointRecreate

module = path+'jx4/createControllers.py'
print module
sys.path.append(os.path.dirname(os.path.expanduser(module)))
import createControllers

SCRIPT_LOC = "R:/Jx4/tools/dcc/maya/scripts/autoRigger/"

def get_maya_window():
        """Get the maya main window as a QMainWindow instance"""
        ptr = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(ptr), qt.QWidget)
class theWindow(MayaQWidgetDockableMixin,qt.QWidget):    
    def __init__(self, *args, **kwargs):   
        global uiIsBuildable;
        global scaleVar
        if(uiIsBuildable == True):
            super(theWindow, self).__init__(*args, **kwargs);
            #PARENT WIDGET UNDER MAYA'S MAIN WINDOW       
            self.setParent(get_maya_window());  
            self.setWindowFlags(qtc.Qt.Window);
            self.setGeometry(500, 500, width, height);   
            self.setWindowTitle(officialTitle);
            mainLayout = qt.QVBoxLayout();
            self.setLayout(mainLayout);
            tabs = qt.QTabWidget();
            ############################################################
            #                        ADD TABS                          #
            ############################################################
            bipedTab	= qt.QWidget();
            bipedHandTab = qt.QWidget();
            quadrupedTab	= qt.QWidget();
            tabs.addTab(bipedTab, "BIPED");
            tabs.addTab(bipedHandTab, "BIPED HAND");
            tabs.addTab(quadrupedTab, "QUADRUPED");
            mainLayout.addWidget(tabs);
            ############################################################
            #                        ADD MAIN LAYOUTS                  #
            ############################################################
            bipedMidLayout = qt.QVBoxLayout();
            bipedHandLayout = qt.QVBoxLayout();
            quadrupedMidLayout = qt.QVBoxLayout();
            
            ############################################################
            #                        ADD IMAGE CALL                    #
            ############################################################
            tabs.setStyleSheet('QTabBar::tab:first {background-color: skyblue;}QTabWidget>QWidget{border-image: url("R:/Jx4/tools/dcc/maya/scripts/autoRigger/charPickerUI/pickerBackground.png");}')
            tabs.currentChanged.connect(lambda: setImage());

            ############################################################
            #                        ADD BUTTONS                       #
            ############################################################
            
            #  BIPED BUTTONS  #
            self.generateRigButton = qt.QPushButton("GENERATE RIG!")
            self.generateRigButton.setMaximumWidth(150)
            self.generateRigButton.setMinimumHeight(20)
            self.generateRigButton.setStyleSheet('QPushButton {backgroundColor: white;}QPushButton {color: black;}')
            
            self.optionsDropdown = qt.QComboBox()
            self.optionsDropdown.addItem("Adult")
            self.optionsDropdown.addItem("Child")
            self.optionsDropdown.addItem("Female")
            self.optionsDropdown.setStyleSheet('QComboBox {color: black;}')
            
            self.finishButton = qt.QPushButton("FINISHED PLACING JOINTS!")
            self.finishButton.setMaximumWidth(150)
            self.finishButton.setMinimumHeight(20)
            self.finishButton.setStyleSheet('QPushButton {backgroundColor: white;}QPushButton {color: black;}')
            self.headButton = qt.QPushButton("HEAD")
            self.headButton.setMaximumWidth(50)
            self.headButton.setMinimumHeight(50)
            self.headButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.neckButton = qt.QPushButton("NECK")
            self.neckButton.setMaximumWidth(40)
            self.neckButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.chestButton = qt.QPushButton("CHEST")
            self.chestButton.setMaximumWidth(100)
            self.chestButton.setMinimumHeight(30)
            self.chestButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.spine3Button = qt.QPushButton("SPINE 3")
            self.spine3Button.setMaximumWidth(50)
            self.spine3Button.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.spine2Button = qt.QPushButton("SPINE 2")
            self.spine2Button.setMaximumWidth(50)
            self.spine2Button.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.spine1Button = qt.QPushButton("SPINE 1")
            self.spine1Button.setMaximumWidth(50)
            self.spine1Button.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.rootButton = qt.QPushButton("ROOT")
            self.rootButton.setMaximumWidth(75)
            self.rootButton.setMinimumHeight(30)
            self.rootButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.clavButton = qt.QPushButton("CLAV")
            self.clavButton.setMaximumWidth(50)
            self.clavButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.shoulderButton = qt.QPushButton("SHOULDER")
            self.shoulderButton.setMaximumWidth(75)
            self.shoulderButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.elbowButton = qt.QPushButton("ELBOW")
            self.elbowButton.setMaximumWidth(50)
            self.elbowButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.wristButton = qt.QPushButton("WRIST")
            self.wristButton.setMaximumWidth(50)
            self.wristButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.thighButton = qt.QPushButton("THIGH")
            self.thighButton.setMaximumWidth(50)
            self.thighButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.kneeButton = qt.QPushButton("KNEE")
            self.kneeButton.setMaximumWidth(50)
            self.kneeButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.ankleButton = qt.QPushButton("ANKLE")
            self.ankleButton.setMaximumWidth(50)
            self.ankleButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.ballButton = qt.QPushButton("BALL")
            self.ballButton.setMaximumWidth(50)
            self.ballButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            
            #  HAND BUTTONS  #
            self.HBIndex1Button = qt.QPushButton("Index 1")
            self.HBIndex1Button.setMaximumWidth(50)
            self.HBIndex1Button.setMinimumWidth(50)
            self.HBIndex1Button.setStyleSheet('QPushButton {background-color: ivory;}QPushButton {color: black;}')
            self.HBIndex2Button = qt.QPushButton("Index 2")
            self.HBIndex2Button.setMaximumWidth(50)
            self.HBIndex2Button.setMinimumWidth(50)
            self.HBIndex2Button.setStyleSheet('QPushButton {background-color: ivory;}QPushButton {color: black;}')
            self.HBIndex3Button = qt.QPushButton("Index 3")
            self.HBIndex3Button.setMaximumWidth(50)
            self.HBIndex3Button.setMinimumWidth(50)
            self.HBIndex3Button.setStyleSheet('QPushButton {background-color: ivory;}QPushButton {color: black;}')
            self.HBMiddle1Button = qt.QPushButton("Middle 1")
            self.HBMiddle1Button.setMaximumWidth(50)
            self.HBMiddle1Button.setMinimumWidth(50)
            self.HBMiddle1Button.setStyleSheet('QPushButton {background-color: lightCyan;}QPushButton {color: black;}')
            self.HBMiddle2Button = qt.QPushButton("Middle 2")
            self.HBMiddle2Button.setMaximumWidth(50)
            self.HBMiddle2Button.setMinimumWidth(50)
            self.HBMiddle2Button.setStyleSheet('QPushButton {background-color: lightCyan;}QPushButton {color: black;}')
            self.HBMiddle3Button = qt.QPushButton("Middle 3")
            self.HBMiddle3Button.setMaximumWidth(50)
            self.HBMiddle3Button.setMinimumWidth(50)
            self.HBMiddle3Button.setStyleSheet('QPushButton {background-color: lightCyan;}QPushButton {color: black;}')
            self.HBRing1Button = qt.QPushButton("Ring 1")
            self.HBRing1Button.setMaximumWidth(50)
            self.HBRing1Button.setMinimumWidth(50)
            self.HBRing1Button.setStyleSheet('QPushButton {background-color: lightSalmon;}QPushButton {color: black;}')
            self.HBRing2Button = qt.QPushButton("Ring 2")
            self.HBRing2Button.setMaximumWidth(50)
            self.HBRing2Button.setMinimumWidth(50)
            self.HBRing2Button.setStyleSheet('QPushButton {background-color: lightSalmon;}QPushButton {color: black;}')
            self.HBRing3Button = qt.QPushButton("Ring 3")
            self.HBRing3Button.setMaximumWidth(50)
            self.HBRing3Button.setMinimumWidth(50)
            self.HBRing3Button.setStyleSheet('QPushButton {background-color: lightSalmon;}QPushButton {color: black;}')
            self.HBPinky1Button = qt.QPushButton("Pinky 1")
            self.HBPinky1Button.setMaximumWidth(50)
            self.HBPinky1Button.setMinimumWidth(50)
            self.HBPinky1Button.setStyleSheet('QPushButton {background-color: orchid;}QPushButton {color: black;}')
            self.HBPinky2Button = qt.QPushButton("Pinky 2")
            self.HBPinky2Button.setMaximumWidth(50)
            self.HBPinky2Button.setMinimumWidth(50)
            self.HBPinky2Button.setStyleSheet('QPushButton {background-color: orchid;}QPushButton {color: black;}')
            self.HBPinky3Button = qt.QPushButton("Pinky 3")
            self.HBPinky3Button.setMaximumWidth(50)
            self.HBPinky3Button.setMinimumWidth(50)
            self.HBPinky3Button.setStyleSheet('QPushButton {background-color: orchid;}QPushButton {color: black;}')
            self.HBThumb1Button = qt.QPushButton("Thumb 1")
            self.HBThumb1Button.setMaximumWidth(50)
            self.HBThumb1Button.setMinimumWidth(50)
            self.HBThumb1Button.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.HBThumb2Button = qt.QPushButton("Thumb 2")
            self.HBThumb2Button.setMaximumWidth(50)
            self.HBThumb2Button.setMinimumWidth(50)
            self.HBThumb2Button.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.HBThumb3Button = qt.QPushButton("Thumb 3")
            self.HBThumb3Button.setMaximumWidth(50)
            self.HBThumb3Button.setMinimumWidth(50)
            self.HBThumb3Button.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            
            #  QUADRUPED BUTTONS  #
            self.qGenerateRigButton = qt.QPushButton("GENERATE Q-RIG!")
            self.qGenerateRigButton.setMaximumWidth(150)
            self.qGenerateRigButton.setMinimumHeight(20)
            self.qGenerateRigButton.setStyleSheet('QPushButton {backgroundColor: gray;}QPushButton {color: black;}')
            
            self.qOptionsDropdown = qt.QComboBox()
            self.qOptionsDropdown.addItem("Horse")
            self.qOptionsDropdown.setStyleSheet('QComboBox {color: black;}')
            
            self.qFinishButton = qt.QPushButton("FINISHED PLACING Q-JOINTS!")
            self.qFinishButton.setMaximumWidth(150)
            self.qFinishButton.setMinimumHeight(20)
            self.qFinishButton.setStyleSheet('QPushButton {backgroundColor: gray;}QPushButton {color: black;}')
            self.qHeadButton = qt.QPushButton("HEAD")
            self.qHeadButton.setMaximumWidth(50)
            self.qHeadButton.setMinimumHeight(50)
            self.qHeadButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qNeckButton = qt.QPushButton("NECK")
            self.qNeckButton.setMaximumWidth(40)
            self.qNeckButton.setMinimumHeight(20)
            self.qNeckButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qNeckButton1 = qt.QPushButton("NECK1")
            self.qNeckButton1.setMaximumWidth(40)
            self.qNeckButton1.setMinimumHeight(20)
            self.qNeckButton1.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qNeckButton2 = qt.QPushButton("NECK2")
            self.qNeckButton2.setMaximumWidth(40)
            self.qNeckButton2.setMinimumHeight(20)
            self.qNeckButton2.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qChestButton = qt.QPushButton("CHEST")
            self.qChestButton.setMaximumWidth(100)
            self.qChestButton.setMinimumHeight(25)
            self.qChestButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qSpine3Button = qt.QPushButton("SPINE 3")
            self.qSpine3Button.setMaximumWidth(50)
            self.qSpine3Button.setMinimumHeight(25)
            self.qSpine3Button.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qSpine2Button = qt.QPushButton("SPINE 2")
            self.qSpine2Button.setMaximumWidth(50)
            self.qSpine2Button.setMinimumHeight(25)
            self.qSpine2Button.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qSpine1Button = qt.QPushButton("SPINE 1")
            self.qSpine1Button.setMaximumWidth(50)
            self.qSpine1Button.setMinimumHeight(25)
            self.qSpine1Button.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qRootButton = qt.QPushButton("PELVIS")
            self.qRootButton.setMaximumWidth(75)
            self.qRootButton.setMinimumHeight(25)
            self.qRootButton.setStyleSheet('QPushButton {background-color: yellow;}QPushButton {color: black;}')
            self.qShoulderButton = qt.QPushButton("SHOULDER")
            self.qShoulderButton.setMaximumWidth(80)
            self.qShoulderButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.qElbowButton = qt.QPushButton("ELBOW")
            self.qElbowButton.setMaximumWidth(50)
            self.qElbowButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.qWristButton = qt.QPushButton("WRIST")
            self.qWristButton.setMaximumWidth(50)
            self.qWristButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.qHandButton = qt.QPushButton("HAND")
            self.qHandButton.setMaximumWidth(50)
            self.qHandButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.qHandEndButton = qt.QPushButton("HAND END")
            self.qHandEndButton.setMaximumWidth(80)
            self.qHandEndButton.setStyleSheet('QPushButton {background-color: tomato;}QPushButton {color: black;}')
            self.qHipButton = qt.QPushButton("HIP")
            self.qHipButton.setMaximumWidth(50)
            self.qHipButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.qStifleButton = qt.QPushButton("STIFLE")
            self.qStifleButton.setMaximumWidth(50)
            self.qStifleButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.qHockButton = qt.QPushButton("HOCK")
            self.qHockButton.setMaximumWidth(50)
            self.qHockButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.qFetlockButton = qt.QPushButton("HIND FETLOCK")
            self.qFetlockButton.setMaximumWidth(80)
            self.qFetlockButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.qCoronetButton = qt.QPushButton("HIND CORONET")
            self.qCoronetButton.setMaximumWidth(100)
            self.qCoronetButton.setStyleSheet('QPushButton {background-color: skyblue;}QPushButton {color: black;}')
            self.qTailButton = qt.QPushButton("TAIL")
            self.qTailButton.setMaximumWidth(20)
            self.qTailButton.setMaximumHeight(20)
            self.qTailButton.setStyleSheet('QPushButton {background-color: red;}QPushButton {color: black;}')
            self.qTailButton1 = qt.QPushButton("TAIL1")
            self.qTailButton1.setMaximumWidth(20)
            self.qTailButton1.setMaximumHeight(20)
            self.qTailButton1.setStyleSheet('QPushButton {background-color: red;}QPushButton {color: black;}')
            self.qTailButton2 = qt.QPushButton("TAIL2")
            self.qTailButton2.setMaximumWidth(20)
            self.qTailButton2.setMaximumHeight(20)
            self.qTailButton2.setStyleSheet('QPushButton {background-color: red;}QPushButton {color: black;}')
            self.qTailButton3 = qt.QPushButton("TAIL3")
            self.qTailButton3.setMaximumWidth(20)
            self.qTailButton3.setMaximumHeight(20)
            self.qTailButton3.setStyleSheet('QPushButton {background-color: red;}QPushButton {color: black;}')
            self.qTailButton4 = qt.QPushButton("TAIL4")
            self.qTailButton4.setMaximumWidth(20)
            self.qTailButton4.setMaximumHeight(20)
            self.qTailButton4.setStyleSheet('QPushButton {background-color: red;}QPushButton {color: black;}')
            self.qTailButton5 = qt.QPushButton("TAIL5")
            self.qTailButton5.setMaximumWidth(20)
            self.qTailButton5.setMaximumHeight(20)
            self.qTailButton5.setStyleSheet('QPushButton {background-color: red;}QPushButton {color: black;}')

            
            ############################################################
            #                        ADD DIVIDER                       #
            ############################################################
            
            #    BIPED DIVIDERS    #
            chestDivider = qt.QFrame();
            chestDivider.setFrameShape(qt.QFrame.HLine);
            chestDivider.setMaximumWidth(55)
            chestDivider.setFrameShadow(qt.QFrame.Sunken);
            
            spine3Divider = qt.QFrame();
            spine3Divider.setFrameShape(qt.QFrame.HLine);
            spine3Divider.setMaximumWidth(70)
            spine3Divider.setFrameShadow(qt.QFrame.Sunken);
            
            spine1Divider = qt.QFrame();
            spine1Divider.setFrameShape(qt.QFrame.HLine);
            spine1Divider.setMaximumWidth(40)
            spine1Divider.setFrameShadow(qt.QFrame.Sunken);
            
            legDivider = qt.QFrame();
            legDivider.setFrameShape(qt.QFrame.HLine);
            legDivider.setMaximumWidth(40)
            legDivider.setFrameShadow(qt.QFrame.Sunken);
            
            legDivider1 = qt.QFrame();
            legDivider1.setFrameShape(qt.QFrame.HLine);
            legDivider1.setMaximumWidth(50)
            
            legDivider2 = qt.QFrame();
            legDivider2.setFrameShape(qt.QFrame.HLine);
            legDivider2.setMaximumWidth(30)
            
            verticalDivider = qt.QFrame()
            verticalDivider.setFrameShape(qt.QFrame.VLine)
            verticalDivider.setMaximumHeight(50)
            
            armDivider = qt.QFrame();
            armDivider.setFrameShape(qt.QFrame.HLine);
            armDivider.setMaximumWidth(55)
            
            armDivider1 = qt.QFrame();
            armDivider1.setFrameShape(qt.QFrame.HLine);
            armDivider1.setMaximumWidth(55)
            
            armDivider2 = qt.QFrame();
            armDivider2.setFrameShape(qt.QFrame.HLine);
            armDivider2.setMaximumWidth(25)
            
            utilDivider = qt.QFrame()
            utilDivider.setFrameShape(qt.QFrame.HLine)
            
            #    HAND DIVIDERS    #
            handDivider = qt.QFrame();
            handDivider.setFrameShape(qt.QFrame.HLine);
            handDivider.setMaximumHeight(50)
            handDivider1 = qt.QFrame();
            handDivider1.setFrameShape(qt.QFrame.HLine);
            handDivider1.setMaximumHeight(10)
            handDivider2 = qt.QFrame();
            handDivider2.setFrameShape(qt.QFrame.HLine);
            handDivider2.setMaximumHeight(5)
            handDivider3 = qt.QFrame();
            handDivider3.setFrameShape(qt.QFrame.HLine);
            handDivider3.setMaximumHeight(5)
            
            handDivider4 = qt.QFrame();
            handDivider4.setFrameShape(qt.QFrame.HLine);
            handDivider4.setMaximumHeight(30)
            handDivider5 = qt.QFrame();
            handDivider5.setFrameShape(qt.QFrame.HLine);
            handDivider5.setMaximumHeight(10)
            handDivider6 = qt.QFrame();
            handDivider6.setFrameShape(qt.QFrame.HLine);
            handDivider6.setMaximumHeight(5)
            handDivider7 = qt.QFrame();
            handDivider7.setFrameShape(qt.QFrame.HLine);
            handDivider7.setMaximumHeight(5)
            
            
            #    QUADRUPED DIVIDERS    #
            headSpacer = qt.QFrame();
            headSpacer.setFrameShape(qt.QFrame.HLine);
            headSpacer.setMaximumWidth(300)
            headSpacer1 = qt.QFrame();
            headSpacer1.setFrameShape(qt.QFrame.HLine);
            headSpacer1.setMaximumWidth(75)
            
            neck1Spacer = qt.QFrame();
            neck1Spacer.setFrameShape(qt.QFrame.HLine);
            neck1Spacer.setMaximumWidth(225)
            neck1Spacer1 = qt.QFrame();
            neck1Spacer1.setFrameShape(qt.QFrame.HLine);
            neck1Spacer1.setMaximumWidth(225)
            
            neck2Spacer = qt.QFrame();
            neck2Spacer.setFrameShape(qt.QFrame.HLine);
            neck2Spacer.setMaximumWidth(250)
            neck2Spacer1 = qt.QFrame();
            neck2Spacer1.setFrameShape(qt.QFrame.HLine);
            neck2Spacer1.setMaximumWidth(200)
            
            neck3Spacer = qt.QFrame();
            neck3Spacer.setFrameShape(qt.QFrame.HLine);
            neck3Spacer.setMaximumWidth(275)
            neck3Spacer1 = qt.QFrame();
            neck3Spacer1.setFrameShape(qt.QFrame.HLine);
            neck3Spacer1.setMaximumWidth(175)
            
            qVerticalSpacer = qt.QFrame();
            qVerticalSpacer.setFrameShape(qt.QFrame.VLine);
            qVerticalSpacer.setMaximumWidth(50)
            
            qVerticalSpacer1 = qt.QFrame();
            qVerticalSpacer1.setFrameShape(qt.QFrame.VLine);
            qVerticalSpacer1.setMaximumWidth(5)
            
            qSpineSpacer = qt.QFrame();
            qSpineSpacer.setFrameShape(qt.QFrame.HLine);
            qSpineSpacer.setMaximumWidth(75)
            qSpineSpacer1 = qt.QFrame();
            qSpineSpacer1.setFrameShape(qt.QFrame.HLine);
            qSpineSpacer1.setMaximumWidth(150)
            
            qHipShoulderSpacer = qt.QFrame();
            qHipShoulderSpacer.setFrameShape(qt.QFrame.HLine);
            qHipShoulderSpacer.setMaximumWidth(25)
            qHipShoulderSpacer1 = qt.QFrame();
            qHipShoulderSpacer1.setFrameShape(qt.QFrame.HLine);
            qHipShoulderSpacer1.setMaximumWidth(150)
            
            qHockWristSpacer = qt.QFrame();
            qHockWristSpacer.setFrameShape(qt.QFrame.HLine);
            qHockWristSpacer.setMaximumWidth(25)
            qHockWristSpacer1 = qt.QFrame();
            qHockWristSpacer1.setFrameShape(qt.QFrame.HLine);
            qHockWristSpacer1.setMaximumWidth(150)
            
            qFetlockHandSpacer = qt.QFrame();
            qFetlockHandSpacer.setFrameShape(qt.QFrame.HLine);
            qFetlockHandSpacer.setMaximumWidth(25)
            qFetlockHandSpacer1 = qt.QFrame();
            qFetlockHandSpacer1.setFrameShape(qt.QFrame.HLine);
            qFetlockHandSpacer1.setMaximumWidth(150)
            
            qCoronetHandEndSpacer = qt.QFrame();
            qCoronetHandEndSpacer.setFrameShape(qt.QFrame.HLine);
            qCoronetHandEndSpacer.setMaximumWidth(5)
            qCoronetHandEndSpacer1 = qt.QFrame();
            qCoronetHandEndSpacer1.setFrameShape(qt.QFrame.HLine);
            qCoronetHandEndSpacer1.setMaximumWidth(150)
            
            qUtilDivider = qt.QFrame()
            qUtilDivider.setFrameShape(qt.QFrame.HLine)
            
            qhnDivider = qt.QFrame()
            qhnDivider.setFrameShape(qt.QFrame.VLine)
            
            ############################################################
            #                        BUTTON COMMANDS                   #
            ############################################################
            #   BIPED BUTTONS   #
            self.generateRigButton.clicked.connect(lambda: runVisScript("first"))
            self.finishButton.clicked.connect(lambda: runVisScript("second"))
            self.headButton.clicked.connect(lambda: runButton("obj_loc_head_joint"));
            self.neckButton.clicked.connect(lambda: runButton("obj_loc_neck_joint"));
            self.chestButton.clicked.connect(lambda: runButton("obj_loc_chest_joint"));
            self.spine3Button.clicked.connect(lambda: runButton("obj_loc_spine_3_joint"));
            self.spine2Button.clicked.connect(lambda: runButton("obj_loc_spine_2_joint"));
            self.spine1Button.clicked.connect(lambda: runButton("obj_loc_spine_1_joint"));
            self.rootButton.clicked.connect(lambda: runButton("obj_loc_root_joint"));
            self.clavButton.clicked.connect(lambda: runButton("obj_loc_L_clav_joint"));
            self.shoulderButton.clicked.connect(lambda: runButton("obj_loc_L_shoulder_joint"))
            self.elbowButton.clicked.connect(lambda: runButton("obj_loc_L_elbow_joint"))
            self.wristButton.clicked.connect(lambda: runButton("obj_loc_L_hand_joint"))
            self.thighButton.clicked.connect(lambda: runButton("obj_loc_L_thigh_joint"))
            self.kneeButton.clicked.connect(lambda: runButton("obj_loc_L_knee_joint"))
            self.ankleButton.clicked.connect(lambda: runButton("obj_loc_L_ankle_joint"))
            self.ballButton.clicked.connect(lambda: runButton("obj_loc_L_ball_joint"))
            self.optionsDropdown.activated.connect(lambda: selectionChanged())
            self.qOptionsDropdown.activated.connect(lambda: qSelectionChanged())
            
            #  HAND BUTTONS  #
            self.HBIndex1Button.clicked.connect(lambda: runButton("obj_loc_L_index_joint_3"));
            self.HBIndex2Button.clicked.connect(lambda: runButton("obj_loc_L_index_joint_2"));
            self.HBIndex3Button.clicked.connect(lambda: runButton("obj_loc_L_index_joint_1"));
            self.HBMiddle1Button.clicked.connect(lambda: runButton("obj_loc_L_middle_joint_3"));
            self.HBMiddle2Button.clicked.connect(lambda: runButton("obj_loc_L_middle_joint_2"));
            self.HBMiddle3Button.clicked.connect(lambda: runButton("obj_loc_L_middle_joint_1"));
            self.HBRing1Button.clicked.connect(lambda: runButton("obj_loc_L_ring_joint_3"));
            self.HBRing2Button.clicked.connect(lambda: runButton("obj_loc_L_ring_joint_2"));
            self.HBRing3Button.clicked.connect(lambda: runButton("obj_loc_L_ring_joint_1"));
            self.HBPinky1Button.clicked.connect(lambda: runButton("obj_loc_L_pinkie_joint_3"));
            self.HBPinky2Button.clicked.connect(lambda: runButton("obj_loc_L_pinkie_joint_2"));
            self.HBPinky3Button.clicked.connect(lambda: runButton("obj_loc_L_pinkie_joint_1"));
            self.HBThumb1Button.clicked.connect(lambda: runButton("obj_loc_L_thumb_joint_3"));
            self.HBThumb2Button.clicked.connect(lambda: runButton("obj_loc_L_thumb_joint_2"));
            self.HBThumb3Button.clicked.connect(lambda: runButton("obj_loc_L_thumb_joint_1"));
            
            #   QUADRUPED BUTTONS    #
            self.qGenerateRigButton.clicked.connect(lambda: runVisScript("third"));
            self.qFinishButton.clicked.connect(lambda: runVisScript("fourth"));
            self.qHeadButton.clicked.connect(lambda: runButton("obj_loc_head_joint"));
            self.qNeckButton.clicked.connect(lambda: runButton("obj_loc_neck_joint"));
            self.qNeckButton1.clicked.connect(lambda: runButton("obj_loc_neck_1_joint"));
            self.qNeckButton2.clicked.connect(lambda: runButton("obj_loc_neck_2_joint"));
            self.qChestButton.clicked.connect(lambda: runButton("obj_loc_chest_joint"));
            self.qSpine3Button.clicked.connect(lambda: runButton("obj_loc_spine_3_joint"));
            self.qSpine2Button.clicked.connect(lambda: runButton("obj_loc_spine_2_joint"));
            self.qSpine1Button.clicked.connect(lambda: runButton("obj_loc_spine_1_joint"));
            self.qRootButton.clicked.connect(lambda: runButton("obj_loc_root_joint"));
            self.qShoulderButton.clicked.connect(lambda: runButton("obj_loc_L_shoulder_joint"));
            self.qElbowButton.clicked.connect(lambda: runButton("obj_loc_L_elbow_joint"));
            self.qWristButton.clicked.connect(lambda: runButton("obj_loc_L_knee_joint"));
            self.qHandButton.clicked.connect(lambda: runButton("obj_loc_L_frontFetlock_joint"));
            self.qHandEndButton.clicked.connect(lambda: runButton("obj_loc_L_frontCoronet_joint"));
            self.qHipButton.clicked.connect(lambda: runButton("obj_loc_L_hip_joint"));
            self.qStifleButton.clicked.connect(lambda: runButton("obj_loc_L_stifle_joint"));
            self.qHockButton.clicked.connect(lambda: runButton("obj_loc_L_hock_joint"));
            self.qFetlockButton.clicked.connect(lambda: runButton("obj_loc_L_hindFetlock_joint"));
            self.qCoronetButton.clicked.connect(lambda: runButton("obj_loc_L_hindCoronet_joint"));
            self.qTailButton.clicked.connect(lambda: runButton("obj_loc_tail_joint"));
            self.qTailButton1.clicked.connect(lambda: runButton("obj_loc_tail1_joint"));
            self.qTailButton2.clicked.connect(lambda: runButton("obj_loc_tail2_joint"));
            self.qTailButton3.clicked.connect(lambda: runButton("obj_loc_tail3_joint"));
            self.qTailButton4.clicked.connect(lambda: runButton("obj_loc_tail4_joint"));
            self.qTailButton5.clicked.connect(lambda: runButton("obj_loc_tail5_joint"));
            
            ############################################################
            #                        ADD LAYOUTS                       #
            ############################################################
            
            #    BIPED LAYOUTS    # 
            generateRigLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            generateRigLayout.addWidget(self.generateRigButton)
            generateRigLayout.addWidget(utilDivider)
            generateRigLayout.addWidget(self.optionsDropdown)
            
            finishedLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            finishedLayout.addWidget(self.finishButton)
            finishedLayout.addWidget(utilDivider)
            
            headButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            headButtonLayout.addWidget(self.headButton);
            
            neckButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            neckButtonLayout.addWidget(self.neckButton)
            
            chestButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            chestButtonLayout.addWidget(chestDivider)
            chestButtonLayout.addWidget(chestDivider)
            chestButtonLayout.addWidget(chestDivider)
            chestButtonLayout.addWidget(self.chestButton)
            chestButtonLayout.addWidget(self.clavButton)
            chestButtonLayout.addWidget(chestDivider)
            chestButtonLayout.addWidget(armDivider)
            
            spine3ButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            spine3ButtonLayout.addWidget(spine3Divider)
            spine3ButtonLayout.addWidget(spine3Divider)
            spine3ButtonLayout.addWidget(self.spine3Button)
            spine3ButtonLayout.addWidget(self.shoulderButton)
            spine3ButtonLayout.addWidget(armDivider1)
            
            spine2ButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            spine2ButtonLayout.addWidget(chestDivider)
            spine2ButtonLayout.addWidget(chestDivider)
            spine2ButtonLayout.addWidget(self.spine2Button)
            spine2ButtonLayout.addWidget(self.elbowButton)
            spine2ButtonLayout.addWidget(armDivider1)
            
            spine1ButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            spine1ButtonLayout.addWidget(spine1Divider)
            spine1ButtonLayout.addWidget(spine1Divider)
            spine1ButtonLayout.addWidget(self.spine1Button)
            spine1ButtonLayout.addWidget(self.wristButton)
            spine1ButtonLayout.addWidget(armDivider2)
            
            rootButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            rootButtonLayout.addWidget(self.rootButton)
            
            thighButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            thighButtonLayout.addWidget(legDivider)
            thighButtonLayout.addWidget(legDivider)
            thighButtonLayout.addWidget(self.thighButton)
            thighButtonLayout.addWidget(legDivider1)
            
            kneeButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            kneeButtonLayout.addWidget(legDivider)
            kneeButtonLayout.addWidget(legDivider)
            kneeButtonLayout.addWidget(self.kneeButton)
            kneeButtonLayout.addWidget(legDivider2)
            
            ankleButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            ankleButtonLayout.addWidget(legDivider)
            ankleButtonLayout.addWidget(legDivider)
            ankleButtonLayout.addWidget(self.ankleButton)
            ankleButtonLayout.addWidget(legDivider2)
            
            ballButtonLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            ballButtonLayout.addWidget(legDivider)
            ballButtonLayout.addWidget(legDivider)
            ballButtonLayout.addWidget(self.ballButton)
            ballButtonLayout.addWidget(legDivider2)
            
            #    HAND LAYOUTS    #
            '''
            HBThumbLayout = qt.QBoxLayout(qt.QBoxLayout.TopToBottom)
            HBThumbLayout.addWidget(handDivider)
            HBThumbLayout.addWidget(self.HBThumb1Button)
            HBThumbLayout.addWidget(self.HBThumb2Button)
            HBThumbLayout.addWidget(self.HBThumb3Button)
            HBIndexLayout = qt.QBoxLayout(qt.QBoxLayout.TopToBottom)
            HBIndexLayout.addWidget(self.HBIndex1Button)
            HBIndexLayout.addWidget(self.HBIndex2Button)
            HBIndexLayout.addWidget(self.HBIndex3Button)
            HBIndexLayout.addWidget(handDivider1)
            HBMiddleLayout = qt.QBoxLayout(qt.QBoxLayout.TopToBottom)
            HBMiddleLayout.addWidget(self.HBMiddle1Button)
            HBMiddleLayout.addWidget(self.HBMiddle2Button)
            HBMiddleLayout.addWidget(self.HBMiddle3Button)
            HBRingLayout = qt.QBoxLayout(qt.QBoxLayout.TopToBottom)
            HBRingLayout.addWidget(self.HBRing1Button)
            HBRingLayout.addWidget(self.HBRing2Button)
            HBRingLayout.addWidget(self.HBRing3Button)
            HBPinkyLayout = qt.QBoxLayout(qt.QBoxLayout.TopToBottom)
            HBPinkyLayout.addWidget(self.HBPinky1Button)
            HBPinkyLayout.addWidget(self.HBPinky2Button)
            HBPinkyLayout.addWidget(self.HBPinky3Button)
            '''
            
            HTopLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            HTopLayout.addWidget(handDivider)
            HTopLayout.addWidget(handDivider)
            HTopLayout.addWidget(self.HBIndex1Button)
            HTopLayout.addWidget(handDivider2)
            HTopLayout.addWidget(self.HBMiddle1Button)
            HTopLayout.addWidget(handDivider3)
            HTopLayout.addWidget(self.HBRing1Button)
            HTopLayout.addWidget(handDivider1)
            HTopLayout.addWidget(handDivider1)
            
            HTopLayout1 = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            HTopLayout1.addWidget(handDivider)
            HTopLayout1.addWidget(handDivider)
            HTopLayout1.addWidget(handDivider)
            HTopLayout1.addWidget(handDivider)
            HTopLayout1.addWidget(handDivider)
            HTopLayout1.addWidget(handDivider)
            HTopLayout1.addWidget(self.HBIndex2Button)
            HTopLayout1.addWidget(handDivider2)
            HTopLayout1.addWidget(handDivider2)
            HTopLayout1.addWidget(self.HBMiddle2Button)
            HTopLayout1.addWidget(handDivider2)
            HTopLayout1.addWidget(handDivider2)
            HTopLayout1.addWidget(self.HBRing2Button)
            HTopLayout1.addWidget(handDivider1)
            HTopLayout1.addWidget(handDivider1)
            HTopLayout1.addWidget(self.HBPinky1Button)
            HTopLayout1.addWidget(handDivider1)
            HTopLayout1.addWidget(handDivider1)

            
            
            HTopLayout2 = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            HTopLayout2.addWidget(handDivider7)
            HTopLayout2.addWidget(self.HBThumb1Button)
            HTopLayout2.addWidget(handDivider4)
            HTopLayout2.addWidget(handDivider4)
            HTopLayout2.addWidget(self.HBIndex3Button)
            HTopLayout2.addWidget(handDivider5)
            HTopLayout2.addWidget(self.HBMiddle3Button)
            HTopLayout2.addWidget(handDivider5)
            HTopLayout2.addWidget(self.HBRing3Button)
            HTopLayout2.addWidget(handDivider6)
            HTopLayout2.addWidget(self.HBPinky2Button)
            HTopLayout2.addWidget(handDivider7)
            HTopLayout2.addWidget(handDivider7)
            HTopLayout2.addWidget(handDivider7)
            
            HTopLayout3 = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            HTopLayout3.addWidget(handDivider1)
            HTopLayout3.addWidget(self.HBThumb2Button)
            HTopLayout3.addWidget(handDivider)
            HTopLayout3.addWidget(handDivider)
            HTopLayout3.addWidget(handDivider)
            HTopLayout3.addWidget(self.HBPinky3Button)
            HTopLayout3.addWidget(handDivider1)
            HTopLayout3.addWidget(handDivider1)
            
            HTopLayout4 = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            HTopLayout4.addWidget(handDivider3)
            HTopLayout4.addWidget(self.HBThumb3Button)
            HTopLayout4.addWidget(handDivider)
            HTopLayout4.addWidget(handDivider)
            HTopLayout4.addWidget(handDivider)
            
            
            #    QUADRUPED LAYOUTS    #
            qGenerateRigLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qGenerateRigLayout.addWidget(self.qGenerateRigButton)
            qGenerateRigLayout.addWidget(qUtilDivider)
            qGenerateRigLayout.addWidget(self.qOptionsDropdown)
            
            qFinishedLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qFinishedLayout.addWidget(self.qFinishButton)
            qFinishedLayout.addWidget(qUtilDivider)
            
            qSpineChainLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qSpineChainLayout.addWidget(qSpineSpacer)
            qSpineChainLayout.addWidget(self.qRootButton)
            qSpineChainLayout.addWidget(self.qSpine1Button)
            qSpineChainLayout.addWidget(self.qSpine2Button)
            qSpineChainLayout.addWidget(self.qSpine3Button)
            qSpineChainLayout.addWidget(qSpineSpacer1)
            
            qHeadLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qHeadLayout.addWidget(headSpacer)
            qHeadLayout.addWidget(headSpacer)
            qHeadLayout.addWidget(headSpacer)
            qHeadLayout.addWidget(self.qHeadButton)
            qHeadLayout.addWidget(headSpacer1)
            
            qNeck3Layout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qNeck3Layout.addWidget(neck3Spacer)
            qNeck3Layout.addWidget(neck3Spacer)
            qNeck3Layout.addWidget(neck3Spacer)
            qNeck3Layout.addWidget(self.qNeckButton2)
            qNeck3Layout.addWidget(neck3Spacer1)

            
            qNeck2Layout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qNeck2Layout.addWidget(neck2Spacer)
            qNeck2Layout.addWidget(neck2Spacer)
            qNeck2Layout.addWidget(neck2Spacer)
            qNeck2Layout.addWidget(self.qNeckButton1)
            qNeck2Layout.addWidget(neck2Spacer1)

            qNeck1Layout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qNeck1Layout.addWidget(neck1Spacer)
            qNeck1Layout.addWidget(neck1Spacer)
            qNeck1Layout.addWidget(neck1Spacer)
            qNeck1Layout.addWidget(self.qNeckButton)
            qNeck1Layout.addWidget(neck1Spacer1)
            
            qHLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qHLayout.addWidget(neck2Spacer)
            qHLayout1 = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qHLayout1.addWidget(neck2Spacer)
            qHLayout2 = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qHLayout2.addWidget(neck2Spacer)
            
            qShoulderHipLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qShoulderHipLayout.addWidget(qHipShoulderSpacer)
            qShoulderHipLayout.addWidget(self.qHipButton)
            qShoulderHipLayout.addWidget(qHipShoulderSpacer1)
            qShoulderHipLayout.addWidget(self.qShoulderButton)
            qShoulderHipLayout.addWidget(qHipShoulderSpacer)
            
            qStifleElbowLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qStifleElbowLayout.addWidget(self.qStifleButton)
            qStifleElbowLayout.addWidget(self.qElbowButton)
            
            qHockWristLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qHockWristLayout.addWidget(self.qHockButton)
            qHockWristLayout.addWidget(qHockWristSpacer1)
            qHockWristLayout.addWidget(self.qWristButton)
            qHockWristLayout.addWidget(qHockWristSpacer)
            
            qFetlockHandLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qFetlockHandLayout.addWidget(self.qFetlockButton)
            qFetlockHandLayout.addWidget(qFetlockHandSpacer1)
            qFetlockHandLayout.addWidget(self.qHandButton)
            qFetlockHandLayout.addWidget(qFetlockHandSpacer)
            
            qCoronetHandEndLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            qCoronetHandEndLayout.addWidget(qCoronetHandEndSpacer)
            qCoronetHandEndLayout.addWidget(self.qCoronetButton)
            qCoronetHandEndLayout.addWidget(qCoronetHandEndSpacer1)
            qCoronetHandEndLayout.addWidget(self.qHandEndButton)
            qCoronetHandEndLayout.addWidget(qCoronetHandEndSpacer)
            qCoronetHandEndLayout.addWidget(qCoronetHandEndSpacer)

            ############################################################
            #                        SET LAYOUTS                       #
            ############################################################
            
            #    BIPED LAYOUTS    #
            #bipedMidLayout.addWidget(verticalDivider)
            bipedMidLayout.addLayout(generateRigLayout)
            bipedMidLayout.addLayout(finishedLayout)
            bipedMidLayout.addLayout(headButtonLayout)
            bipedMidLayout.addLayout(neckButtonLayout)
            bipedMidLayout.addLayout(chestButtonLayout)
            bipedMidLayout.addLayout(spine3ButtonLayout)
            bipedMidLayout.addLayout(spine2ButtonLayout)
            bipedMidLayout.addLayout(spine1ButtonLayout)
            bipedMidLayout.addLayout(rootButtonLayout)
            bipedMidLayout.addLayout(thighButtonLayout)
            bipedMidLayout.addWidget(verticalDivider)
            bipedMidLayout.addLayout(kneeButtonLayout)
            bipedMidLayout.addWidget(verticalDivider)
            bipedMidLayout.addLayout(ankleButtonLayout)
            bipedMidLayout.addLayout(ballButtonLayout)
            
            #    HAND LAYOUTS    #
            bipedHandLayout.addWidget(handDivider)
            bipedHandLayout.addLayout(HTopLayout)
            bipedHandLayout.addLayout(HTopLayout1)
            bipedHandLayout.addLayout(HTopLayout2)
            bipedHandLayout.addLayout(HTopLayout3)
            bipedHandLayout.addLayout(HTopLayout4)
            bipedHandLayout.addWidget(handDivider)
            
            
            
            
            #    QUADRUPEED LAYOUTS    #
            quadrupedMidLayout.addLayout(qGenerateRigLayout)
            quadrupedMidLayout.addLayout(qFinishedLayout)
            quadrupedMidLayout.addWidget(qVerticalSpacer)
            quadrupedMidLayout.addLayout(qHeadLayout)
            quadrupedMidLayout.addLayout(qNeck3Layout)
            quadrupedMidLayout.addLayout(qNeck2Layout)
            quadrupedMidLayout.addLayout(qNeck1Layout)
            quadrupedMidLayout.addLayout(qHLayout)
            quadrupedMidLayout.addLayout(qSpineChainLayout)
            quadrupedMidLayout.addLayout(qHLayout1)
            quadrupedMidLayout.addLayout(qShoulderHipLayout)
            quadrupedMidLayout.addWidget(qVerticalSpacer)
            quadrupedMidLayout.addLayout(qStifleElbowLayout)
            quadrupedMidLayout.addWidget(qVerticalSpacer)
            quadrupedMidLayout.addLayout(qHockWristLayout)
            quadrupedMidLayout.addWidget(qVerticalSpacer)
            quadrupedMidLayout.addLayout(qFetlockHandLayout)
            quadrupedMidLayout.addLayout(qHLayout2)
            quadrupedMidLayout.addLayout(qCoronetHandEndLayout)
            quadrupedMidLayout.addWidget(qVerticalSpacer)
            
            ############################################################
            #                SET LAYOUTS TO MAIN LAYOUT                #
            ############################################################
            bipedTab.setLayout(bipedMidLayout);
            bipedHandTab.setLayout(bipedHandLayout);
            quadrupedTab.setLayout(quadrupedMidLayout);
            
            ############################################################
            #                        FUNCTIONS                         #
            ############################################################
            
            def checkTab():
                return tabs.currentIndex()
                
            def setImage():
                if checkTab() == 0:
                    tabs.setStyleSheet('QTabBar::tab:first {background-color: skyblue;}QTabWidget>QWidget{border-image: url("R:/Jx4/tools/dcc/maya/scripts/autoRigger/charPickerUI/pickerBackground.png");}')
                elif checkTab() == 1:
                    tabs.setStyleSheet('QTabBar::tab:middle {background-color: green;}QTabWidget>QWidget{border-image: url("R:/Jx4/tools/dcc/maya/scripts/autoRigger/charPickerUI/handImage.png");}')
                else:
                    tabs.setStyleSheet('QTabBar::tab:last {background-color: tomato;}QTabWidget>QWidget{border-image: url("R:/Jx4/tools/dcc/maya/scripts/autoRigger/charPickerUI/horseAdult1.png");}')

            def selectionChanged():
                print "Items in the list are :"
            	global scaleVar
                for count in range(self.optionsDropdown.count()):
                    print self.optionsDropdown.itemText(count)
                print "Current index",i,"selection changed ",self.optionsDropdown.currentText()
                scaleVar = self.optionsDropdown.currentText()
                print scaleVar
            def qSelectionChanged():
                print "Items in the list are :"
            	global scaleVar
                for count in range(self.optionsDropdown.count()):
                    print self.qOptionsDropdown.itemText(count)
                print "Current index",i,"selection changed ",self.qOptionsDropdown.currentText()
                scaleVar = self.qOptionsDropdown.currentText()
                print scaleVar

def runButton(nameOfButton):
    print "running button"
    print nameOfButton
    cmds.select(nameOfButton)

def runVisScript(whichScript):
    global scaleVar
    print whichScript
    #from charPicker import *
    if whichScript == "first":
        locCreate.createLoc("first")
    elif whichScript == "second":
        jointRecreate.recreateJoints()
        createControllers.scanMesh(scaleVar)
    elif whichScript == "third":
        locCreate.createLoc("third")
    elif whichScript == "fourth":
        jointRecreate.recreateJoints()
        createControllers.scanMesh(scaleVar)
        
        
ui = theWindow()
ui.show(dockable=True)