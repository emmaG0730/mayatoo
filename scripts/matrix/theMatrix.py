###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import os
import sys
import glob
import json
import getpass
import platform
import datetime
import maya.cmds as py
import maya.mel as mel
import shiboken
import maya.OpenMayaUI as mui
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
###############################################################################
#"""# DECLARE GLOBAL VARIABLES                                                #
###############################################################################
global UI
global importPath
global exportPath
global posePath
global POSELIST
global rigPath
global scaleField
global uiIsBuildable
global timelineRange
global selectedTimelineKeys
global previouslySelectedTimelineKeys
global startKeyFrame
global endKeyFrame
global stored_pose_amount
############################################z##################################
#"""# UPDATE INFO (WHAT'S NEW)                                                #
###############################################################################
versionNumber = 3;
versionNumberBeta = 0.1;
timelineRange = "none";
previouslySelectedTimelineKeys = "none";
updateNews = """Tool name: The Matrix
Architect: Sean "HiGGiE" Higginbottom
Update Date: 05/30/2018
Download address (P4V): R:/Jx4/tools/dcc/maya/scripts/matrix
Documents(Confluence): https://seasungames.atlassian.net/wiki/display/SEAS/The+Matrix
Tutorials Video(\\172.19.64.100):


Additions:
    1. Starman Body and Weapon exports available
    2. Improved skeleton finding method; can import rigs with various items (ie: Motion Builder FBX's)

Removals:
    1. "BODY" removed from Starman Weapon json file names
    
Changes:
    1. Export based on timeline range instead of first and last key's range
    2. Starman can support dual weapons (ie: left and right fists)
    
Bugs Fixed:
    
Known Bugs:
    
"""  
###############################################################################
#"""# PATH FINDING                                                            #
###############################################################################
path = "";
state = "";
uiIsBuildable = False;
mayaVersion = py.about(v=1);
documents = os.path.expanduser("~");
documents = documents+"/";
environment = documents+"maya/"+mayaVersion+"/Maya.env";
stored_pose_amount = 0
placeHolder = 'POSE'
if(py.file(environment,q=1,ex=1) == 1):
    output = open(environment,"r");
    line = output.readlines();
    if any("nightly" in s for s in line):
        state = "(beta)";
primaryMatrixPath = 'R:/Jx4/tools/dcc/maya/scripts/matrix/subScripts/';
secondaryMatrixPath = documents+'matrix/subScripts/';
if(py.file(primaryMatrixPath,q=1,ex=1) == 1):
    path = primaryMatrixPath;
elif(py.file(secondaryMatrixPath,q=1,ex=1) == 1):
    path = secondaryMatrixPath;
if(state != ""):
    path = path.replace("maya/","maya/nightly/");
    versionNumber = str(versionNumber)+str(versionNumberBeta)[1:];
else:
    versionNumber = str(versionNumber)+str(0.0)[1:];
if(path != ""):
###############################################################################
#"""# IMPORT ADDITIONAL MODULES FOR THE MATRIX                                #
###############################################################################
    module = path+'importFile.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import importFile# = reload();
    module = path+'importField.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import importField#importField = reload(importField);
    module = path+'exportField.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import exportField#exportField = reload(exportField);
    module = path+'rigField.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import rigField#rigField = reload(rigField);
    module = path+'checkBoxes.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import checkBoxes#checkBoxes = reload(checkBoxes);
    module = path+'savePose.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import savePose#savePose = reload(savePose);
    module = path+'loadPose.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import loadPose#loadPose = reload(loadPose);
    module = path+'exportFile.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import exportFile#exportFile = reload(exportFile);
    module = path+'batchExport.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import batchExport#batchExport = reload(batchExport);
    module = path+'email.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import email#batchExport = reload(batchExport);
    #STARMAN MODULES IMPORT
    path = 'R:/Jx4/tools/dcc/maya/scripts/starmanExporter/';
    module = path+'sm_exportRig.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import sm_exportRig#sm_exportRig = reload(sm_exportRig);
    module = path+'sm_generateRig.py';
    sys.path.append(os.path.dirname(os.path.expanduser(module)));
    import sm_generateRig#sm_generateRig = reload(sm_generateRig);     
###############################################################################
#"""# FIND DOCUMENTS FOLDER                                                   #
###############################################################################
    home = "invalid";
    currentUser = getpass.getuser();
    desktop = documents.replace("/Documents/","/Desktop/");
    OS = platform.system();
    ALPHA = ["A:","B:","C:","D:","E:","F:","G:","H:","I:","J:","K:","L:","M:",
             "N:","O:","P:","Q:","R:","S:","T:","U:","V:","W:","X:","Y:","Z:"];
    lock = 1;
    if(os.path.isdir("R:/Jx4") == 1 and os.path.isdir("R:/JX4_SourceData") == 1):
        lock = 1;
    i=0;
    while(i < len(ALPHA)):
        if(os.path.isdir(documents.replace(documents[0:2],ALPHA[i])) == 1):
            home = documents.replace(documents[0:2],ALPHA[i]);
            break;
        elif(os.path.isdir(desktop.replace(desktop[0:2],ALPHA[i])) == 1):
            home = desktop.replace(desktop[0:2],ALPHA[i]);
            break;
        i+=1;    
###############################################################################
#"""# SEARCH FOR VALID RIG (FULL NAME)                                        #
###############################################################################
    if(home != "invalid"):
        initialRigPath = "R:/JX4_SourceData/Graphics/Characters/Human/MaleAdult/XieYunLiu/CHAR_xieYunLiu_v1_RIG.ma";#!
        if(py.file(initialRigPath,q=1,ex=1) == 1):
            rigPath = initialRigPath;
        else:
            rigPath = "No Rig; Please select rig before importing or map the 'R:' drive.";
###############################################################################
#"""# DECLARE PRESET SETTINGS                                                 #
###############################################################################
        presets = {
           'USER' : currentUser,#0
           'PRIMARY UI COLOR' : '0.1,0.2,0.3',#1
           'SECONDARY UI COLOR' : '0.05,0.1,0.15',#2
           'TRANSPARENCY' : 80,#3
           'DESKTOP (PATH)' : home,#4
           'IMPORT FILE (PATH)' : home,#5
           'EXPORT FOLDER (PATH)' : home,#6
           'BATCH FILES (FULL NAME)' : 'EMPTY',#7
           'RIG (FULL NAME)' : rigPath,#8
           'HOTKEY' : 'RiGGiE',#9
           'LEG IK' : 1,#10
           'ARM IK' : 0,#11
           'SCALE IK' : 1.0,#12
           'POSE (PATH)' : home,#13
           'POSE FILES (FULL NAME)' : 'EMPTY',#14
           'EXPORT AS .MA' : 1,#15
           'EXPORT AS .FBX' : 0,#16
           'EXPORT AS .XMD' : 0,#17
           'EXPORT STARMAN' : 0,#18
           'EXPORT STARMAN WEAPON' : 0,#19
           'LOCAL POSE' : 1,#20
           'GLOBAL POSE' : 0,#21
           'HORIZONTAL' : 1,#22
           'VERTICAL' : 1,#23
           'ROTATION' : 1,#24
           'TRAJECTORY' : 1,#25
           'SNAP KEYS' : 1,#26
        }
        customFile = py.file(home+"CUSTOM.json",q=1,ex=1);
        if(customFile == 1):
            with open(home+'CUSTOM.json', 'r') as f:
                line = json.load(f);
                if(len(line) != len(presets)):
                    dictionaryItems = [d for d in presets];
                    i=0;
                    while(i < len(dictionaryItems)):
                        if(dictionaryItems[i] not in line):
                            value = presets[dictionaryItems[i]]
                            line[dictionaryItems[i]] = value;
                        i+=1;
            os.remove(home+"CUSTOM.json"); 
            with open(home+'CUSTOM.json', 'w+') as f:
                 json.dump(line, f, sort_keys=True, indent=4);
        else:
            with open(home+'CUSTOM.json', 'w+') as f:
                 json.dump(presets, f, sort_keys=True, indent=4);
            with open(home+'CUSTOM.json', 'r') as f:
                line = json.load(f);
###############################################################################
#"""# BASIC SETTINGS                                                          #
###############################################################################
        primaryFont = "fixedWidthFont";
        secondaryFont = "smallFixedWidthFont";
        py.currentUnit(time="ntsc");py.playbackOptions(ps=1,e=1,min=0);#30FPS
        primaryColor = [];
        secondaryColor = [];
        i=0;
        while(i < 3):
            primaryColor.append(float(line['PRIMARY UI COLOR'].split(",")[i]));
            secondaryColor.append(float(line['SECONDARY UI COLOR'].split(",")[i]));
            i+=1; 
###############################################################################
#"""# BUILD UI                                                                #
###############################################################################
        toolTitle = "MATRIX v"+str(versionNumber)+state;
        officialTitle = toolTitle.replace(" ","_").replace(".","_");
        height = 385;
        width = 700;
        uiIsBuildable = True;
def get_maya_window():
        """Get the maya main window as a QMainWindow instance"""
        ptr = mui.MQtUtil.mainWindow()
        return shiboken.wrapInstance(long(ptr), qt.QWidget)
class theWindow(MayaQWidgetDockableMixin,qt.QWidget):    
    def __init__(self, *args, **kwargs):   
        global uiIsBuildable;
        if(uiIsBuildable == True):
            super(theWindow, self).__init__(*args, **kwargs);
            #PARENT WIDGET UNDER MAYA'S MAIN WINDOW       
            self.setParent(get_maya_window());  
            self.setWindowFlags(qtc.Qt.Window);
            #SET OPACITY 
            self.setWindowOpacity(line['TRANSPARENCY']/100.0);
            #SET NAME AND DIMENSIONS
            self.setGeometry(500, 500, width, height);   
            self.setWindowTitle(officialTitle);
            #p = self.palette();
            #p.setColor(self.backgroundRole(), qt.blue);
            #self.setPalette(p);
            mainLayout = qt.QVBoxLayout();
###############################################################################
#"""# TABS                                                                    #
###############################################################################
            tabs = qt.QTabWidget();
            importExportTab	= qt.QWidget();
            poseLibraryTab	= qt.QWidget();
            keyManagerTab	= qt.QWidget();
            settingsTab	    = qt.QWidget();
            whatsNewTab     = qt.QWidget();
            emailTab        = qt.QWidget();
            tabs.addTab(importExportTab, "IMPORT/EXPORT");
            tabs.addTab(poseLibraryTab, "POSE LIBRARY");
            tabs.addTab(keyManagerTab, "KEY MANAGER");
            tabs.addTab(settingsTab, "SETTINGS");
            tabs.addTab(whatsNewTab, "WHAT'S NEW");
            tabs.addTab(emailTab, "EMAIL");
            mainLayout.addWidget(tabs);
            importExportLayout = qt.QVBoxLayout();
            boldFont = qt.QFont("Segoe", 10, qt.QFont.Bold);
###############################################################################
#"""# IMPORT WIDGETS                                                          #
###############################################################################
            self.importLabel = qt.QLabel("IMPORT PATH:"); 
            self.importEdit = qt.QLineEdit(line['IMPORT FILE (PATH)']);
            self.importEdit.textChanged.connect(lambda: runCheckBoxes(self.importEdit,'IMPORT FILE (PATH)'));
            self.importBrowseButton = qt.QPushButton("SELECT FILES"); 
            #LEG IK
            self.legTrackingCheckBox = qt.QCheckBox("LEG IK"); 
            self.legTrackingCheckBox.setChecked(line['LEG IK']);
            self.legTrackingCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','LEG IK'));
            #ARM IK
            self.armTrackingCheckBox = qt.QCheckBox("ARM IK"); 
            self.armTrackingCheckBox.setChecked(line['ARM IK']);
            self.armTrackingCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','ARM IK'));
            #SCALE IK
            self.scaleEdit = qt.QLineEdit(str(line['SCALE IK']));
            self.scaleEdit.textChanged.connect(lambda: runCheckBoxes(self.scaleEdit,'SCALE IK'));
            self.scaleEdit.setFixedSize(25, 20);
            self.scaleLabel = qt.QLabel("SCALE IK"); 
###############################################################################
#"""# EXPORT WIDGETS                                                          #
###############################################################################
            self.exportLabel = qt.QLabel("EXPORT PATH:"); 
            self.exportEdit = qt.QLineEdit(line['EXPORT FOLDER (PATH)']);
            self.exportEdit.textChanged.connect(lambda: runCheckBoxes(self.exportEdit,'EXPORT FOLDER (PATH)'));
            self.exportBrowseButton = qt.QPushButton("SELECT FOLDER"); 
            self.rigLabel = qt.QLabel("RIG:"); 
            self.rigEdit = qt.QLineEdit(line['RIG (FULL NAME)']);
            self.rigEdit.textChanged.connect(lambda: runCheckBoxes(self.rigEdit,'RIG (FULL NAME)'));
            self.rigBrowseButton = qt.QPushButton("SELECT RIG"); 
            #MAYA
            self.mayaCheckBox = qt.QCheckBox("MAYA FILE"); 
            self.mayaCheckBox.setChecked(line['EXPORT AS .MA']);
            self.mayaCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','EXPORT AS .MA'));
            #FBX
            self.fbxCheckBox = qt.QCheckBox("FBX FILE"); 
            self.fbxCheckBox.setChecked(line['EXPORT AS .FBX']);
            self.fbxCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','EXPORT AS .FBX'));
            #XMD
            self.xmdCheckBox = qt.QCheckBox("XMD FILE");
            self.xmdCheckBox.setChecked(line['EXPORT AS .XMD']);
            self.xmdCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','EXPORT AS .XMD'));
            #STARMAN BODY
            self.starmanCheckBox = qt.QCheckBox("STARMAN BODY");
            self.starmanCheckBox.setChecked(line['EXPORT STARMAN']);
            self.starmanCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','EXPORT STARMAN'));
            #STARMAN WEAPON
            self.starmanWeaponCheckBox = qt.QCheckBox("STARMAN WEAPON");
            self.starmanWeaponCheckBox.setChecked(line['EXPORT STARMAN WEAPON']);
            self.starmanWeaponCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','EXPORT STARMAN WEAPON'));
###############################################################################
#"""# IMPORT LIST WIDGET                                                      #
###############################################################################
            nameList = [];
            self.importFileList = qt.QListWidget()
            fileList = line['BATCH FILES (FULL NAME)'].split(",");
            i=0;
            while(i < len(fileList)):
                if(len(fileList[i]) > 0):
                    nameList.append(fileList[i].split("/")[-1]);
                    self.importFileList.addItem(fileList[i].split("/")[-1]);
                if(i == len(fileList)-1 and len(nameList) == 0):
                    self.importFileList.addItem("EMPTY");
                i+=1;
            self.importFileList.setCurrentRow(0);
###############################################################################
#"""# IMPORT/EXPORT WIDGETS                                                   #
###############################################################################
            self.importFileButton = qt.QPushButton("IMPORT"); 
            self.exportFileButton = qt.QPushButton("EXPORT");
            self.batchFileButton = qt.QPushButton("BATCH"); 
###############################################################################
#"""# POSE WIDGETS                                                            #
###############################################################################
            poseLibraryLayout = qt.QVBoxLayout();
            #LOCAL
            self.poseLocalCheckBox = qt.QCheckBox();
            self.poseLocalCheckBox.setChecked(line['LOCAL POSE']);
            self.poseLocalCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','LOCAL POSE'));
            self.poseLocalCheckBox.stateChanged.connect(lambda: runFilterList(self.poseListWidget,self.filterEdit,"POSE"));
            self.poseLocalLabel = qt.QLabel("LOCAL PATH:"); 
            self.poseLocalEdit = qt.QLineEdit(line['POSE (PATH)']);
            self.poseLocalEdit.textChanged.connect(lambda: runCheckBoxes(self.poseLocalEdit,'POSE (PATH)'));
            self.poseLocalBrowseButton = qt.QPushButton("SELECT POSE");
            #GLOBAL
            self.poseGlobalCheckBox = qt.QCheckBox();
            self.poseGlobalCheckBox.setChecked(line['GLOBAL POSE']);
            self.poseGlobalCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','GLOBAL POSE'));
            self.poseGlobalCheckBox.stateChanged.connect(lambda: runFilterList(self.poseListWidget,self.filterEdit,"POSE"));
            self.poseGlobalLabel = qt.QLabel("GLOBAL PATH:"); 
            self.poseGlobalEdit = qt.QLineEdit("R:/Jx4/tools/dcc/maya/scripts/poseLibrary/");
            self.poseGlobalEdit.setEnabled(False);
            self.filterLabel = qt.QLabel("FILTER:"); 
            self.filterEdit = qt.QLineEdit();
            
            #self.poseGlobalCheckBox.stateChanged.connect(lambda: updatePoseLibrary(self.poseListWidget));
            #self.poseLocalCheckBox.stateChanged.connect(lambda: updatePoseLibrary(self.poseListWidget));
            
            #HORIZONTAL
            self.horizontalCheckBox = qt.QCheckBox("HORIZONTAL (X,Z)"); 
            self.horizontalCheckBox.setChecked(line['HORIZONTAL']);
            self.horizontalCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','HORIZONTAL'));
            #VERTICAL
            self.verticalCheckBox = qt.QCheckBox("VERTICAL (Y)"); 
            self.verticalCheckBox.setChecked(line['VERTICAL']);
            self.verticalCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','VERTICAL'));
            #ROTATION
            self.rotationCheckBox = qt.QCheckBox("ROTATION (X,Y,Z)");
            self.rotationCheckBox.setChecked(line['ROTATION']);
            self.rotationCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','ROTATION'));
            #TRAJECTORY
            self.trajectoryCheckBox = qt.QCheckBox("TRAJECTORY");
            self.trajectoryCheckBox.setChecked(line['TRAJECTORY']);
            self.trajectoryCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','TRAJECTORY'));
            #ACTIONS
            self.savePoseButton = qt.QPushButton("SAVE"); 
            self.loadPoseButton = qt.QPushButton("LOAD");
            self.mirrorPoseButton = qt.QPushButton("MIRROR"); 
            self.deletePoseButton = qt.QPushButton("DELETE");
            self.refreshPoseButton = qt.QPushButton("REFRESH");
            #RED#!
            palette = self.deletePoseButton.palette();
            role = self.deletePoseButton.backgroundRole();
            palette.setColor(role, qt.QColor('red'));
            self.deletePoseButton.setPalette(palette);
            self.deletePoseButton.setAutoFillBackground(True);
            self.refreshPoseButton.setStyleSheet("background-color: green")
###############################################################################
#"""# POSE LIST WIDGET                                                        #
###############################################################################
            self.poseListWidget = qt.QListWidget();
            self.poseListWidget.setViewMode(qt.QListWidget.IconMode);
            self.poseListWidget.setDragEnabled(False);
            self.poseListWidget.setResizeMode(qt.QListView.Adjust);
            self.poseListWidget.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
            self.poseListWidget.setStyleSheet("QListView::item:selected { background: palette(Highlight) }");
            #ADD ITEMS TO GRID
            thumbnailSize = [100,180];
            self.poseListWidget.setIconSize(qtc.QSize(thumbnailSize[0], thumbnailSize[1]));
            poseList = line['POSE FILES (FULL NAME)'].split(",");
            i=0;
            while(i < len(poseList)):
                if(len(poseList[i]) > 0 and py.file(poseList[i],q=1,ex=1) == 1):
                    if(py.file(poseList[i].replace(".txt",".png"),q=1,ex=1) == 1):
                        name = poseList[i].split("/")[-1].split(".")[0].split("_POSE")[0].replace("p_","",1);
                        thumbnailItem = qt.QListWidgetItem(name);
                        
                        thumbnailImage = qt.QIcon();
                        thumbnailImage.addPixmap(qt.QPixmap(_fromUtf8(poseList[i].replace(".txt",".png"))), qt.QIcon.Normal, qt.QIcon.Off);
                        thumbnailItem.setIcon(thumbnailImage);
                        
                        self.poseListWidget.addItem(thumbnailItem);
                        #SELECT FIRST ITEM
                        self.poseListWidget.item(0).setSelected(True);
                i+=1;
            self.filterEdit.textChanged.connect(lambda: runFilterList(self.poseListWidget,self.filterEdit,"POSE"));
###############################################################################
#"""# KEY MANAGERS WIDGETS                                                    #
###############################################################################
            keyManagerLayout = qt.QVBoxLayout();
            #SHIFT
            self.shiftLabel = qt.QLabel("SHIFT KEYS"); 
            self.shiftLabel.setFont(boldFont);
            self.shiftStartButton = qt.QPushButton("SET START FRAME");
            self.shiftBackwardButton = qt.QPushButton("   -   ");
            self.shiftIncrementEdit = qt.QLineEdit("10");
            self.shiftForwardButton = qt.QPushButton("   +   "); 
            self.shiftEndButton = qt.QPushButton("SET END FRAME");
            #SCALE
            self.scaleLabel = qt.QLabel("SCALE KEYS"); 
            self.scaleLabel.setFont(boldFont);
            self.scaleFromLabel = qt.QLabel("FROM FRAME:"); 
            self.scaleFromEdit = qt.QLineEdit();
            self.scaleToLabel = qt.QLabel("TO FRAME:"); 
            self.scaleToEdit = qt.QLineEdit();
            self.scaleButton = qt.QPushButton("SCALE FRAMES"); 
            self.scaleSnapCheckBox = qt.QCheckBox("AUTO SNAP KEYS");
            self.scaleSnapCheckBox.setChecked(line['SNAP KEYS']);
            self.scaleSnapCheckBox.stateChanged.connect(lambda: runCheckBoxes('none','SNAP KEYS'));
            #MAIN
            self.snapFramesButton = qt.QPushButton("SNAP FRAMES"); 
            self.deleteFramesButton = qt.QPushButton("DELETE FRAMES"); 
            
            
###############################################################################
#"""# SETTINGS                                                   #
###############################################################################
            settingsLayout = qt.QHBoxLayout();
            #TRANSPARENCY
            self.transparencyLabel = qt.QLabel("UI TRANSPARANCY:"); 
            self.transparancySlider = qt.QSlider();

            self.transparancySlider.setRange(35, 100);
            self.transparancySlider.setOrientation(qtc.Qt.Horizontal);
            self.transparancySlider.setInvertedAppearance(False);
            self.transparancySlider.setInvertedControls(False);
            self.transparancySlider.setValue(line['TRANSPARENCY']);
            
            

###############################################################################
#"""# WHAT'S NEW WIDGET                                                       #
###############################################################################   
            whatsNewLayout = qt.QVBoxLayout();
            self.whatsNew = qt.QTextEdit();
            self.whatsNew.setReadOnly(True);
            self.whatsNew.setText(updateNews);
            self.whatsNew.setLineWrapMode(qt.QTextEdit.NoWrap);
            
            font = self.whatsNew.font();
            font.setFamily("Courier");
            font.setPointSize(10);

            whatsNewLayout.addWidget(self.whatsNew); 
###############################################################################
#"""# CONNECTED COMMANDS (GLOBAL)                                             #
###############################################################################
            self.importFileButton.clicked.connect(lambda: runImport(self.importFileList));
            self.exportFileButton.clicked.connect(lambda: runExport());
            self.batchFileButton.clicked.connect(lambda: runBatch(self.importFileList));
            self.importBrowseButton.clicked.connect(lambda: runImportBrowse(self.importEdit,self.importFileList));
            self.exportBrowseButton.clicked.connect(lambda: runExportBrowse(self.exportEdit,"none","none",'EXPORT FOLDER (PATH)',"none"));
            self.rigBrowseButton.clicked.connect(lambda: runRigBrowse(self.rigEdit));
            
            self.savePoseButton.clicked.connect(lambda: runSave(self.poseListWidget));

            self.loadPoseButton.clicked.connect(lambda: runLoad(self.poseListWidget,"load"));

            self.mirrorPoseButton.clicked.connect(lambda: runLoad(self.poseListWidget,"mirror"));

            self.deletePoseButton.clicked.connect(lambda: runDelete(self.poseLocalEdit,self.poseListWidget,self.filterEdit,"POSE"));

            self.refreshPoseButton.clicked.connect(lambda: runFilterList(self.poseListWidget,self.filterEdit,"POSE"));
            self.poseLocalBrowseButton.clicked.connect(lambda: runExportBrowse("none",self.poseLocalEdit,self.poseListWidget,'POSE (PATH)',"none"));

            self.shiftStartButton.clicked.connect(lambda: runShiftKeys(self.shiftIncrementEdit,"startKey"));
            self.shiftBackwardButton.clicked.connect(lambda: runShiftKeys(self.shiftIncrementEdit,"minusKey"));
            self.shiftForwardButton.clicked.connect(lambda: runShiftKeys(self.shiftIncrementEdit,"plusKey"));
            self.shiftEndButton.clicked.connect(lambda: runShiftKeys(self.shiftIncrementEdit,"endKey"));
            self.scaleButton.clicked.connect(lambda: storeVals(self.scaleFromEdit,self.scaleToEdit));
            self.scaleButton.clicked.connect(lambda: runScaleKeys(self.scaleFromEdit,self.scaleToEdit));
            
            self.snapFramesButton.clicked.connect(lambda: runSnapKeys());
            self.deleteFramesButton.clicked.connect(lambda: runDeleteKeys());
            
            
            self.transparancySlider.valueChanged.connect(lambda: uiTransparency(self.transparancySlider.value(),self.setWindowOpacity));
###############################################################################
#"""# LAYOUT                                                                  #
###############################################################################
            #HORIZONTAL LAYOUT: IMPORT PATH
            importLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            importLayout.addWidget(self.importLabel);
            importLayout.addWidget(self.importEdit);
            importLayout.addWidget(self.importBrowseButton);
            #HORIZONTAL LAYOUT: IK CHECKBOXES AND INPUT
            ikLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            ikLayout.addWidget(self.legTrackingCheckBox);
            ikLayout.addWidget(self.armTrackingCheckBox);
            ikLayout.addWidget(self.scaleEdit);
            ikLayout.addWidget(self.scaleLabel);
            #HORIZONTAL LAYOUT: EXPORT PATH
            exportLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            exportLayout.addWidget(self.exportLabel);
            exportLayout.addWidget(self.exportEdit);
            exportLayout.addWidget(self.exportBrowseButton);
            #HORIZONTAL LAYOUT: RIG PATH
            rigLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            rigLayout.addWidget(self.rigLabel);
            rigLayout.addWidget(self.rigEdit);
            rigLayout.addWidget(self.rigBrowseButton);
            #HORIZONTAL LAYOUT: FILE TYPE CHECKBOXES
            fileLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            fileLayout.addWidget(self.mayaCheckBox);
            fileLayout.addWidget(self.fbxCheckBox);
            fileLayout.addWidget(self.xmdCheckBox);
            fileLayout.addWidget(self.starmanCheckBox);
            fileLayout.addWidget(self.starmanWeaponCheckBox);
            #HORIZONTAL LAYOUT: IMPORT, EXPORT, AND BATCH
            runLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight)
            runLayout.addWidget(self.importFileButton);
            runLayout.addWidget(self.exportFileButton);
            runLayout.addWidget(self.batchFileButton);
            #HORIZONTAL LAYOUT: POSE LOCAL PATH
            poseLocalLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            poseLocalLayout.addWidget(self.poseLocalCheckBox);
            poseLocalLayout.addWidget(self.poseLocalLabel);
            poseLocalLayout.addWidget(self.poseLocalEdit);
            poseLocalLayout.addWidget(self.poseLocalBrowseButton);
            #HORIZONTAL LAYOUT: POSE GLOBAL PATH
            poseGlobalLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            poseGlobalLayout.addWidget(self.poseGlobalCheckBox);
            poseGlobalLayout.addWidget(self.poseGlobalLabel);
            poseGlobalLayout.addWidget(self.poseGlobalEdit);
            #HORIZONTAL LAYOUT: POSE FILTER
            filterLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            filterLayout.addWidget(self.filterLabel);
            filterLayout.addWidget(self.filterEdit);
            #HORIZONTAL LAYOUT: POSITION CHECKBOXES
            positionLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            positionLayout.addWidget(self.horizontalCheckBox);
            positionLayout.addWidget(self.verticalCheckBox);
            positionLayout.addWidget(self.rotationCheckBox);
            positionLayout.addWidget(self.trajectoryCheckBox);
            #HORIZONTAL LAYOUT: POSE BUTTONS
            poseActionLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            poseActionLayout.addWidget(self.savePoseButton);
            poseActionLayout.addWidget(self.loadPoseButton);
            poseActionLayout.addWidget(self.mirrorPoseButton);
            poseActionLayout.addWidget(self.deletePoseButton);
            poseActionLayout.addWidget(self.refreshPoseButton);

            
            
            
            #HORIZONTAL LAYOUT: SHIFT KEYS
            #shiftFramesLayout = qt.QWidget();
            shiftFramesLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            
            
            
            
            shiftFramesLayout.addWidget(self.shiftStartButton);
            shiftFramesLayout.addWidget(self.shiftBackwardButton);
            shiftFramesLayout.addWidget(self.shiftIncrementEdit);
            shiftFramesLayout.addWidget(self.shiftForwardButton);
            shiftFramesLayout.addWidget(self.shiftEndButton);
            
            
            
            #shiftIncFramesWidget.setFixedWidth(width/3);






            
            
            #HORIZONTAL LAYOUT: SCALE KEYS
            scaleFramesLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            scaleFramesLayout.addWidget(self.scaleFromLabel);
            scaleFramesLayout.addWidget(self.scaleFromEdit);
            scaleFramesLayout.addWidget(self.scaleToLabel);
            scaleFramesLayout.addWidget(self.scaleToEdit);
            scaleFramesLayout.addWidget(self.scaleButton);
            
            #HORIZONTAL LAYOUT: ACTION KEYS
            actionKeysLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            actionKeysLayout.addWidget(self.snapFramesButton);
            actionKeysLayout.addWidget(self.deleteFramesButton);
###############################################################################
#"""# ADD HORIZONTAL LAYOUTS TO IMPORT/EXPORT TAB'S LAYOUT                    #
###############################################################################
            importExportDivider = qt.QFrame();
            importExportDivider.setFrameShape(qt.QFrame.HLine);
            importExportDivider.setFrameShadow(qt.QFrame.Sunken);
            
            importExportLayout.addLayout(importLayout);
            importExportLayout.addLayout(ikLayout);
            importExportLayout.addWidget(importExportDivider);
            importExportLayout.addLayout(exportLayout);
            importExportLayout.addLayout(rigLayout);
            importExportLayout.addLayout(fileLayout);
            importExportLayout.addWidget(self.importFileList);
            importExportLayout.addLayout(runLayout);
###############################################################################
#"""# ADD HORIZONTAL LAYOUTS TO POSE LIBRARY TAB'S LAYOUT                     #
###############################################################################
            poseLibraryDivider = qt.QFrame();
            poseLibraryDivider.setFrameShape(qt.QFrame.HLine);
            poseLibraryDivider.setFrameShadow(qt.QFrame.Sunken);
            
            poseLibraryLayout.addLayout(poseLocalLayout);
            poseLibraryLayout.addLayout(poseGlobalLayout);
            poseLibraryLayout.addWidget(poseLibraryDivider);
            poseLibraryLayout.addLayout(filterLayout);
            poseLibraryLayout.addLayout(positionLayout);
            poseLibraryLayout.addWidget(self.poseListWidget);
            poseLibraryLayout.addLayout(poseActionLayout);
###############################################################################
#"""# ADD HORIZONTAL LAYOUTS TO KEY MANAGER TAB'S LAYOUT                      #
###############################################################################
            keyManagerDivider1 = qt.QFrame();
            keyManagerDivider1.setFrameShape(qt.QFrame.HLine);
            keyManagerDivider1.setFrameShadow(qt.QFrame.Sunken);
            keyManagerDivider2 = qt.QFrame();
            keyManagerDivider2.setFrameShape(qt.QFrame.HLine);
            keyManagerDivider2.setFrameShadow(qt.QFrame.Sunken);

            keyManagerLayout.addWidget(self.shiftLabel);
            keyManagerLayout.addLayout(shiftFramesLayout);
            verticalSpacer1 = qt.QSpacerItem(0, 0, qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
            keyManagerLayout.addItem(verticalSpacer1);
            keyManagerLayout.addWidget(keyManagerDivider1);
            
            keyManagerLayout.addWidget(self.scaleLabel);
            keyManagerLayout.addLayout(scaleFramesLayout);
            
            #checkBoxes scaleKeys layout
            keyManagerLayout.addWidget(self.scaleSnapCheckBox);
            
            verticalSpacer2 = qt.QSpacerItem(0, 0, qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
            keyManagerLayout.addItem(verticalSpacer2);
            keyManagerLayout.addWidget(keyManagerDivider2);
            
            keyManagerLayout.addLayout(actionKeysLayout);
###############################################################################
#"""# ADD HORIZONTAL LAYOUTS TO SETTINGS TAB'S LAYOUT                         #
###############################################################################
            settingsDivider1 = qt.QFrame();
            settingsDivider1.setFrameShape(qt.QFrame.HLine);
            settingsDivider1.setFrameShadow(qt.QFrame.Sunken);
            settingsDivider2 = qt.QFrame();
            settingsDivider2.setFrameShape(qt.QFrame.HLine);
            settingsDivider2.setFrameShadow(qt.QFrame.Sunken);

            settingsLayout.addWidget(self.transparencyLabel);
            settingsLayout.addWidget(self.transparancySlider);
###############################################################################
#"""# ADD TAB LAYOUTS TO THEIR CORRESPONDING TABS                             #
###############################################################################
            importExportTab.setLayout(importExportLayout);
            poseLibraryTab.setLayout(poseLibraryLayout);
            keyManagerTab.setLayout(keyManagerLayout);
            settingsTab.setLayout(settingsLayout);
            whatsNewTab.setLayout(whatsNewLayout);

            self.setLayout(mainLayout);
###############################################################################
#"""# COMMANDS: NESTED                                                        #
###############################################################################
        def runCheckBoxes(widget,dictionary):
            widgetString = repr(widget);
            if(widget != "none"):
                value = widget.text();
            else:
                value = "none";
            checkBoxes.CHECKBOXES(value,dictionary,home)
###############################################################################
#"""# COMMANDS: GLOBAL                                                        #
###############################################################################
def runImport(listImportWidget):
    importFile.IMPORTFILE('none',listImportWidget,0,home);
def runExport():
    exportFile.EXPORTFILE('none',line['EXPORT FOLDER (PATH)'],'none',home);
def runBatch(listImportWidget):
    batchExport.BATCHEXPORT('none','none',listImportWidget,home)
def runImportBrowse(editImportWidget,listImportWidget):
    importField.IMPORTFIELD(line,editImportWidget,listImportWidget,home);
def runExportBrowse(editExportWidget,editPoseWidget,listPoseWidget,dictionary,folder):
    exportField.EXPORTFIELD(line,editExportWidget,editPoseWidget,listPoseWidget,dictionary,folder,home);
def runRigBrowse(editRigWidget):
    rigField.RIGFIELD(editRigWidget,home);
def runSave(listPoseWidget):  
    savePose.SAVEPOSE(listPoseWidget,home);
def runLoad(listPoseWidget,action):  
    loadPose.LOADPOSE(listPoseWidget,action,home);
def runShiftKeys(increment,mode):
    global previouslySelectedTimelineKeys
    global selectedTimelineKeys
    global timelineRange
    increment = increment.text();
    #CHECK TO DETERMINE WHETHER TIMELINE RANGE SHOULD BE UPDATED OR RESET
    timelineRangeCheck = mel.eval("global string $gPlayBackSlider;float $rangeArray[2];$rangeArray = `timeControl -q -rangeArray $gPlayBackSlider`;");
    timelineRangeCheckLength = abs(timelineRangeCheck[0]-timelineRangeCheck[-1]);
    timelineRangeLength = abs(timelineRange[0]-timelineRange[-1]) if(timelineRange != "none") else 0;
    if(timelineRangeCheckLength != 1.0 and timelineRangeCheckLength != timelineRangeLength):
        #IF KEY RANGE IS NOT THE SAME THEN RESET
        timelineRange = mel.eval("global string $gPlayBackSlider;float $rangeArray[2];$rangeArray = `timeControl -q -rangeArray $gPlayBackSlider`;");
    else:
        try:
            #IF SELECTED KEYS ARE NOT THE SAME THEN RESET
            py.selectKey(t=(timelineRange[0],timelineRange[-1]));
            currentlySelectedTimelineKeys = py.keyframe(sl=1,n=1,q=1);
            if(currentlySelectedTimelineKeys != previouslySelectedTimelineKeys):
                timelineRange = mel.eval("global string $gPlayBackSlider;float $rangeArray[2];$rangeArray = `timeControl -q -rangeArray $gPlayBackSlider`;");
        except:
            pass;
    py.selectKey(clear=1);
    #IF USER INPUT IS VALID THEN SHIFT KEYS      
    if(increment.replace(".","").replace("-","").isdigit() == 1):
        py.selectKey(t=(timelineRange[0],timelineRange[-1]));
        currentlySelectedTimelineKeys = py.keyframe(sl=1,n=1,q=1);
        previouslySelectedTimelineKeys = currentlySelectedTimelineKeys;
        py.selectKey(clear=1);
        if(isinstance(currentlySelectedTimelineKeys,list) == 1):
            selectedTimelineKeys = currentlySelectedTimelineKeys;
        if(isinstance(selectedTimelineKeys,list) == 1):
            if(mode == "minusKey"):
                increment = float("-"+increment) if("-" not in increment) else increment;
                py.keyframe(selectedTimelineKeys,tc=increment,o="over",t=(timelineRange[0],timelineRange[-1]),r=1,e=1);
                timelineRange[0] = timelineRange[0]+increment;
                timelineRange[-1] = timelineRange[-1]+increment;
            elif(mode == "startKey"):
                increment = float(increment)-float(timelineRange[0]);
                py.keyframe(selectedTimelineKeys,tc=increment,o="over",t=(timelineRange[0],timelineRange[-1]),r=1,e=1);
                timelineRange[0] = float(timelineRange[0])+float(increment);
                timelineRange[-1] = float(timelineRange[-1])+float(increment);
            elif(mode == "endKey"):
                increment = float(increment)-float(timelineRange[-1]);
                py.keyframe(selectedTimelineKeys,tc=increment,o="over",t=(timelineRange[0],timelineRange[-1]),r=1,e=1);
                timelineRange[0] = float(timelineRange[0])+float(increment);
                timelineRange[-1] = float(timelineRange[-1])+float(increment);
            else:
                py.keyframe(selectedTimelineKeys,tc=increment,o="over",t=(timelineRange[0],timelineRange[-1]),r=1,e=1);
                timelineRange[0] = float(timelineRange[0])+float(increment);
                timelineRange[-1] = float(timelineRange[-1])+float(increment);
        else:
            py.headsUpMessage('"No keys selected on timeline." - HiGGiE', t=1);
            print '"No keys selected on timeline." - HiGGiE';  
    else:
        py.headsUpMessage('"Please input a valid frame number." - HiGGiE', t=1);
        print '"Please input a valid frame number." - HiGGiE';
###############################################################################
#"""# SCALE KEY FRAMES                                                        #
############################################################################### 
def runScaleKeys(scaleStart,scaleEnd):  
    global previouslySelectedTimelineKeys
    global selectedTimelineKeys
    global timelineRange
    global startKeyFrame
    global endKeyFrame
    scaleStart = scaleStart.text();
    scaleEnd = scaleEnd.text();
    #CHECK TO DETERMINE WHETHER TIMELINE RANGE SHOULD BE UPDATED OR RESET
    timelineRangeCheck = mel.eval("global string $gPlayBackSlider;float $rangeArray[2];$rangeArray = `timeControl -q -rangeArray $gPlayBackSlider`;");
    timelineRangeCheckLength = abs(timelineRangeCheck[0]-timelineRangeCheck[-1]);
    timelineRangeLength = abs(timelineRange[0]-timelineRange[-1]) if(timelineRange != "none") else 0;

    if(timelineRangeCheckLength != 1.0 and timelineRangeCheckLength != timelineRangeLength):
        #IF KEY RANGE IS NOT THE SAME THEN RESET
        timelineRange = mel.eval("global string $gPlayBackSlider;float $rangeArray[2];$rangeArray = `timeControl -q -rangeArray $gPlayBackSlider`;");
    else:
        try:
            #IF SELECTED KEYS ARE NOT THE SAME THEN RESET
            py.selectKey(t=(timelineRange[0],timelineRange[-1]));
            currentlySelectedTimelineKeys = py.keyframe(sl=1,n=1,q=1);
            if(currentlySelectedTimelineKeys != previouslySelectedTimelineKeys):
                timelineRange = mel.eval("global string $gPlayBackSlider;float $rangeArray[2];$rangeArray = `timeControl -q -rangeArray $gPlayBackSlider`;");
        except:
            pass;
    py.selectKey(clear=1);
    timelineRangeLength = abs(timelineRange[0]-timelineRange[-1]) if(timelineRange != "none") else 0;
    py.selectKey(t=(timelineRange[0],timelineRange[-1]));
    firstSelectedKey = sorted(list(set(py.keyframe(q=1))))[0];
    lastSelectedKey = sorted(list(set(py.keyframe(q=1))))[-1];
    #print firstSelectedKey
    #print lastSelectedKey
    currentlySelectedTimelineKeys = py.keyframe(sl=1,n=1,q=1);
    py.selectKey(clear=1);
    if(isinstance(currentlySelectedTimelineKeys,list) == 1):
        selectedTimelineKeys = currentlySelectedTimelineKeys;
    customFile = py.file(home+"CUSTOM.json",q=1,ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
    if line['SNAP KEYS'] ==1:
        if(isinstance(selectedTimelineKeys,list) == 1):
            if(scaleStart.replace(".","").replace("-","").isdigit() == 1):
                #STRETCH TO START
                pivotFrame = timelineRange[-1];
                pivotScale = abs((float(scaleStart)-float(timelineRange[-1]))/timelineRangeLength);
                py.scaleKey(selectedTimelineKeys,t=(timelineRange[0],timelineRange[-1]),ts=pivotScale,tp=pivotFrame,fs=pivotScale,fp=pivotFrame,vs=1,vp=0,iub=0);
                timelineRange[0] = float(scaleStart);
                timelineRangeLength = abs(timelineRange[0]-timelineRange[-1]);
                
            if(scaleEnd.replace(".","").replace("-","").isdigit() == 1):
                #STRETCH TO END
                pivotFrame = timelineRange[0];
                pivotScale = abs((float(timelineRange[0])-float(scaleEnd))/timelineRangeLength);
                py.scaleKey(selectedTimelineKeys,t=(timelineRange[0],timelineRange[-1]),ts=pivotScale,tp=pivotFrame,fs=pivotScale,fp=pivotFrame,vs=1,vp=0,iub=0);
                timelineRange[-1] = float(scaleEnd);
                timelineRangeLength = abs(timelineRange[0]-timelineRange[-1]);
        runSnapKeys()
    elif line['SNAP KEYS'] == 0:
        if(isinstance(selectedTimelineKeys,list) == 1):
            if(scaleStart.replace(".","").replace("-","").isdigit() == 1):
                #STRETCH TO START
                pivotFrame = timelineRange[-1];
                pivotScale = abs((float(scaleStart)-float(timelineRange[-1]))/timelineRangeLength);
                py.scaleKey(selectedTimelineKeys,t=(timelineRange[0],timelineRange[-1]),ts=pivotScale,tp=pivotFrame,fs=pivotScale,fp=pivotFrame,vs=1,vp=0,iub=0);
                timelineRange[0] = float(scaleStart);
                timelineRangeLength = abs(timelineRange[0]-timelineRange[-1]);
                
            if(scaleEnd.replace(".","").replace("-","").isdigit() == 1):
                #STRETCH TO END
                pivotFrame = timelineRange[0];
                pivotScale = abs((float(timelineRange[0])-float(scaleEnd))/timelineRangeLength);
                py.scaleKey(selectedTimelineKeys,t=(timelineRange[0],timelineRange[-1]),ts=pivotScale,tp=pivotFrame,fs=pivotScale,fp=pivotFrame,vs=1,vp=0,iub=0);
                timelineRange[-1] = float(scaleEnd);
                timelineRangeLength = abs(timelineRange[0]-timelineRange[-1]);
    else:
        py.headsUpMessage('"No keys selected on timeline." - HiGGiE', t=1);
        print '"No keys selected on timeline." - HiGGiE';
###############################################################################
#"""# SNAP KEY FRAME(S)                                                       #
############################################################################### 
def storeVals(startTime,endTime):
    global startKeyFrame
    global endKeyFrame
    startKeyFrame = startTime.text()
    endKeyFrame = endTime.text()

def runSnapKeys():
    keyframes = py.keyframe(time=(startKeyFrame,endKeyFrame), query=True) #find keyframes in time range
    keyframeSet = set(keyframes) #remove duplicates
    keyframeList = list(keyframeSet)
    keyframeList = sorted(keyframeList,key=float)
    print keyframeList
    if keyframeList:
        for number in keyframeList:
            if number != int(number): # non int numbers
                py.cutKey(time=(number, number))
                roundDown = float(int(number))
                roundUp = int(number)+1.0
                if roundDown in keyframeList:
                    if roundUp in keyframeList:
                        # delete key if the previous and next int frames already have keys
                        print("deleted key on frame " + str(number)) 
                    else:
                        # move key to next int frame if previous int frame already has key
                        py.pasteKey(time=(roundUp, roundUp))
                        keyframeList.append(roundUp)
                        print ("moved key on frame "+ str(number)+" to frame "+ str(roundUp))
                else:
                    # move key to previous int frame if previous int doesn't have key
                    py.pasteKey(time=(roundDown, roundDown))
                    keyframeList.append(roundDown)
                    print ("moved key on frame "+ str(number)+" to frame "+str(roundDown))

    #mel.eval("timeSliderSnapKey;;");
    
###############################################################################
#"""# DELETE KEY FRAME(S)                                                     #
############################################################################### 
def runDeleteKeys():
    mel.eval("timeSliderClearKey;");
###############################################################################
#"""# FILTER POSE(S)                                                          #
############################################################################### 
def runFilterList(listWidget,filterString,suffix):
    customFile = py.file(home+"CUSTOM.json",q=1,ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
            if(len(line) != len(presets)):
                dictionaryItems = [d for d in presets];
                i=0;
                while(i < len(dictionaryItems)):
                    if(dictionaryItems[i] not in line):
                        value = presets[dictionaryItems[i]]
                        line[dictionaryItems[i]] = value;
                    i+=1;
        os.remove(home+"CUSTOM.json"); 
        with open(home+'CUSTOM.json', 'w+') as f:
            json.dump(line, f, sort_keys=True, indent=4);
    #ADD ITEMS TO GRID
    globalPosePath = "R:/Jx4/tools/dcc/maya/scripts/poseLibrary/";
    localPosePath = line['POSE (PATH)'];
    thumbnailSize = [100,180];
    filterString = filterString.text();
    listWidget.setIconSize(qtc.QSize(thumbnailSize[0], thumbnailSize[1]));
    poseLocalList = glob.glob(localPosePath+"*_"+suffix+".txt") if(line['LOCAL POSE'] == 1) else [];
    poseGlobalList = glob.glob(globalPosePath+"*_"+suffix+".txt") if(line['GLOBAL POSE'] == 1) else [];
    poseList = poseLocalList+poseGlobalList;
    listWidget.clear();
    i=0;
    if filterString == "":
        while(i < len(poseList)):
            if(len(poseList[i]) > 0 and py.file(poseList[i],q=1,ex=1) == 1):
                if(py.file(poseList[i].replace(".txt",".png"),q=1,ex=1) == 1 and "p_"+filterString.lower() in poseList[i].lower()):
                    name = poseList[i].split("\\")[-1].split(".")[0].split("_POSE")[0].replace("p_","",1);
                    thumbnailItem = qt.QListWidgetItem(name);
                    
                    
                    thumbnailImage = qt.QIcon();
                    thumbnailImage.addPixmap(qt.QPixmap(_fromUtf8(poseList[i].replace(".txt",".png"))), qt.QIcon.Normal, qt.QIcon.Off);
                    thumbnailItem.setIcon(thumbnailImage)
                    listWidget.addItem(thumbnailItem)
            i+=1;  
        #WRITE NEW FILES TO HOME (JSON)    
        pathContainer = "";    
        i=0;
        while(i < len(poseList)):
            pathContainer = pathContainer+poseList[i].replace("\\","/");
            pathContainer = pathContainer+",";
            i+=1;
        os.remove(home+"CUSTOM.json");
        line['POSE FILES (FULL NAME)'] = pathContainer;
        with open(home+'CUSTOM.json', 'w+') as f:
             json.dump(line, f, sort_keys=False, indent=4);  
    else:
        print filterString
        while(i < len(poseList)):
            if(len(poseList[i]) > 0 and py.file(poseList[i],q=1,ex=1) == 1):
                if(py.file(poseList[i].replace(".txt",".png"),q=1,ex=1) == 1 and "p_"+filterString.lower() in poseList[i].lower()):
                    name = poseList[i].split("\\")[-1].split(".")[0].split("_POSE")[0].replace("p_","",1);
                    thumbnailItem = qt.QListWidgetItem(name);
                    
                    
                    thumbnailImage = qt.QIcon();
                    thumbnailImage.addPixmap(qt.QPixmap(_fromUtf8(poseList[i].replace(".txt",".png"))), qt.QIcon.Normal, qt.QIcon.Off);
                    thumbnailItem.setIcon(thumbnailImage)
                    listWidget.addItem(thumbnailItem)
            i+=1;  
        #WRITE NEW FILES TO HOME (JSON)    
        pathContainer = "";    
        i=0;
        while(i < len(poseList)):
            pathContainer = pathContainer+poseList[i].replace("\\","/");
            pathContainer = pathContainer+",";
            i+=1;
        os.remove(home+"CUSTOM.json");
        line['POSE FILES (FULL NAME)'] = pathContainer;
        with open(home+'CUSTOM.json', 'w+') as f:
            json.dump(line, f, sort_keys=False, indent=4);     
###############################################################################
#"""# DELETE POSE(S)                                                          #
############################################################################### 
def runDelete(editPoseWidget,listPoseWidget,filterString,suffix):
    thumbnailIDs = [];
    thumbnailCount = listPoseWidget.selectedItems();
    i=0;
    print thumbnailCount
    while(i < len(thumbnailCount)):
        thumbnailIDs.append(thumbnailCount[i]);
        i+=1;
    print thumbnailIDs
    if(len(thumbnailIDs) == 1):
        dialog = py.confirmDialog(t="Delete Pose",
        m="Are you sure you want to delete this pose?",
        b=["Yes", "No"],db="No",cb="No",ds="No");
    elif(len(thumbnailIDs) > 1):
        dialog = py.confirmDialog(t="Delete Poses",
        m="Are you sure you want to delete these poses?",
        b=["Yes", "No"],db="No",cb="No",ds="No");
    else:
        py.headsUpMessage('"Please select at least one (1) pose." - HiGGiE', t=1);
        print '"Please select at least one (1) pose." - HiGGiE';  
        dialog == "No";
    homeExists = py.file(home+"CUSTOM.json", q=1, ex=1);
    if(homeExists == 1 and dialog == "Yes"):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f); 
        #DELETE SELECTED FILES
        globalPosePath = "R:/Jx4/tools/dcc/maya/scripts/poseLibrary/";
        localPosePath = line['POSE (PATH)'];
        i=0;
        print thumbnailIDs
        while(i < len(thumbnailIDs)):
            print thumbnailIDs[i].text()
            poseFile = localPosePath+"p_"+thumbnailIDs[i].text()+"_POSE.txt";
            print poseFile
            if(py.file(poseFile,q=1,ex=1) == 1):
                os.remove(poseFile);
                os.remove(poseFile.replace(".txt",".png"));
            #poseFile = globalPosePath+"p_"+thumbnailIDs[i].text()+"_POSE.txt";
            #if(py.file(poseFile,q=1,ex=1) == 1):
            #    os.remove(poseFile);
            #    os.remove(poseFile.replace(".txt",".png"));
            i+=1;
        runExportBrowse("none",editPoseWidget,listPoseWidget,'POSE (PATH)',[line['POSE (PATH)'][:-1]])
        runFilterList(listPoseWidget,filterString,suffix)
###############################################################################
#"""# SETTINGS                                                                #
############################################################################### 
def uiTransparency(value,target):
    target(value/100.0);
    
    
    with open(home+'CUSTOM.json', 'r') as f:
        line = json.load(f);
    os.remove(home+"CUSTOM.json"); 
    line["TRANSPARENCY"] = value;
    presets = line;
    with open(home+'CUSTOM.json', 'w+') as f:
        json.dump(presets, f, sort_keys=False, indent=4);

ui = theWindow()
ui.show(dockable=True)