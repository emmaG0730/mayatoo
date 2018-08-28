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
###############################################################################
#"""# FIND DOCUMENTS FOLDER                                                   #
###############################################################################
home = "R:/Jx4/tools/dcc/maya/scripts/library/";#!
versionNumber = 1;
state = "";
###############################################################################
#"""# SEARCH FOR VALID RIG (FULL NAME)                                        #
###############################################################################
if(home != "invalid"):
###############################################################################
#"""# BUILD UI                                                                #
###############################################################################
    toolTitle = "JX4 LIBRARY v"+str(versionNumber)+state;
    officialTitle = toolTitle.replace(" ","_").replace(".","_");
    height = 650;
    width = 470;
    uiIsBuildable = True;
def get_maya_window():
    """Get the maya main window as a QMainWindow instance"""
    ptr = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), qt.QWidget)
class theWindow(qt.QWidget):    
    def __init__(self, *args, **kwargs):   
        global uiIsBuildable;
        if(uiIsBuildable == True):
            super(theWindow, self).__init__(*args, **kwargs);
            #PARENT WIDGET UNDER MAYA'S MAIN WINDOW       
            self.setParent(get_maya_window());  
            self.setWindowFlags(qtc.Qt.Window);
            #SET OPACITY 
            self.setWindowOpacity(0.8);
            #SET NAME AND DIMENSIONS
            self.setGeometry(500, 300, width, height);   
            self.setWindowTitle(officialTitle);
            #p = self.palette();
            #p.setColor(self.backgroundRole(), qt.blue);
            #self.setPalette(p);
            mainLayout = qt.QVBoxLayout();
###############################################################################
#"""# TABS                                                                    #
###############################################################################
            tabs = qt.QTabWidget();
            characterTab	= qt.QWidget();
            weaponTab	= qt.QWidget();
            tabs.addTab(characterTab, "CHARACTER LIBRARY");
            tabs.addTab(weaponTab, "WEAPON LIBRARY");
            mainLayout.addWidget(tabs);
            importExportLayout = qt.QVBoxLayout();
###############################################################################
#"""# CHARACTER WIDGETS                                                       #
###############################################################################
            self.characterLabel = qt.QLabel("FILTER:"); 
            self.characterEdit = qt.QLineEdit();
###############################################################################
#"""# WEAPON WIDGETS                                                          #
###############################################################################
            self.weaponLabel = qt.QLabel("FILTER:"); 
            self.weaponEdit = qt.QLineEdit();
###############################################################################
#"""# CHARACTER LIST WIDGETS                                                  #
###############################################################################
            tabName = "characters/";
            characterLibraryLayout = qt.QVBoxLayout();
            self.characterListWidget = qt.QListWidget();
            self.characterListWidget.setViewMode(qt.QListWidget.IconMode);
            self.characterListWidget.setDragEnabled(False);
            self.characterListWidget.setResizeMode(qt.QListView.Adjust);
            #ADD ITEMS TO GRID
            thumbnailSize = [130,240];
            self.characterListWidget.setIconSize(qtc.QSize(thumbnailSize[0], thumbnailSize[1]));
            characterList = glob.glob(home+tabName+"*_CHAR.txt");
            i=0;
            while(i < len(characterList)):
                if(len(characterList[i]) > 0 and py.file(characterList[i],q=1,ex=1) == 1):
                    if(py.file(characterList[i].replace(".txt",".png"),q=1,ex=1) == 1):
                        name = characterList[i].split("/")[-1].split(".")[0].split("_")[1];
                        thumbnailItem = qt.QListWidgetItem(name);
                        
                        thumbnailItem.setSizeHint(qtc.QSize(width/3.45,height/2.45));
                        
                        thumbnailImage = qt.QIcon();
                        thumbnailImage.addPixmap(qt.QPixmap(_fromUtf8(characterList[i].replace(".txt",".png"))), qt.QIcon.Normal, qt.QIcon.Off);
                        thumbnailItem.setIcon(thumbnailImage)
                        self.characterListWidget.addItem(thumbnailItem)
                i+=1;
            self.characterLoadButton = qt.QPushButton("LOAD");
            self.characterLoadButton.clicked.connect(lambda: runLoadItem(self.characterListWidget,tabName,"CHAR"));
            self.characterEdit.textChanged.connect(lambda: runFilterList(self.characterListWidget,self.characterEdit,tabName,"CHAR"));
###############################################################################
#"""# LAYOUT                                                                  #
###############################################################################
            divider = qt.QFrame();
            divider.setFrameShape(qt.QFrame.HLine);
            divider.setFrameShadow(qt.QFrame.Sunken);
            #HORIZONTAL LAYOUT: CHARACTER FILTER
            characterLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            characterLayout.addWidget(self.characterLabel);
            characterLayout.addWidget(self.characterEdit);
            #HORIZONTAL LAYOUT: WEAPON FILTER
            weaponLayout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight);
            weaponLayout.addWidget(self.weaponLabel);
            weaponLayout.addWidget(self.weaponEdit);
###############################################################################
#"""# ADD HORIZONTAL LAYOUTS TO CHARACTER LIBRARY TAB'S LAYOUT                #
###############################################################################
            characterLibraryLayout.addLayout(characterLayout);
            characterLibraryLayout.addWidget(self.characterListWidget);
            characterLibraryLayout.addWidget(self.characterLoadButton);
###############################################################################
#"""# ADD HORIZONTAL LAYOUTS TO CHARACTER LIBRARY TAB'S LAYOUT                #
###############################################################################
            #weaponLibraryLayout.addLayout(weaponLayout);
            #weaponLibraryLayout.addWidget(self.weaponListWidget);
            #weaponLibraryLayout.addWidget(self.weaponLoadButton);
###############################################################################
#"""# ADD TAB LAYOUTS TO THEIR CORRESPONDING TABS                             #
###############################################################################

            characterTab.setLayout(characterLibraryLayout);
            #weaponTab.setLayout(weaponLibraryLayout);


            self.setLayout(mainLayout);
###############################################################################
#"""# COMMANDS: GLOBAL                                                        #
###############################################################################
def runFilterList(listWidget,filterString,category,suffix):
    thumbnailSize = [130,240];
    filterString = filterString.text();
    listWidget.setIconSize(qtc.QSize(thumbnailSize[0], thumbnailSize[1]));
    characterList = glob.glob(home+category+"*_"+suffix+".txt");
    listWidget.clear();
    i=0;
    while(i < len(characterList)):
        if(len(characterList[i]) > 0 and py.file(characterList[i],q=1,ex=1) == 1):
            if(py.file(characterList[i].replace(".txt",".png"),q=1,ex=1) == 1 and "p_"+filterString.lower() in characterList[i].lower()):
                name = characterList[i].split("/")[-1].split(".")[0].split("_")[1];
                thumbnailItem = qt.QListWidgetItem(name);
                
                thumbnailItem.setSizeHint(qtc.QSize(width/3.45,height/2.45));#!
                
                thumbnailImage = qt.QIcon();
                thumbnailImage.addPixmap(qt.QPixmap(_fromUtf8(characterList[i].replace(".txt",".png"))), qt.QIcon.Normal, qt.QIcon.Off);
                thumbnailItem.setIcon(thumbnailImage)
                listWidget.addItem(thumbnailItem)
        i+=1;
def runLoadItem(listWidget,category,suffix):
    rigControllers = [];
    selections = py.ls(sl=1);
    try:
        thumbnailIDs = [];
        thumbnailCount = listWidget.selectedItems();
        i=0;
        while(i < len(thumbnailCount)):
            thumbnailIDs.append(thumbnailCount[i]);
            i+=1;
        selectedItem = "p_"+thumbnailIDs[-1].text()+"_"+suffix+".txt";
        itemSelection = True;
    except:
        itemSelection = False;
    if(itemSelection == True):
        textFile = open(home+category+selectedItem, "r");
        fileFullPath = textFile.readlines();
        textFile.close();
###############################################################################
# DETERMINES THE VALIDITY OF THE SELECTED                                     #
############################################################################### 
        i=0;
        while(i < len(selections)):
            RiGGiE = py.listAttr(selections[i], st=["RiGGiE"], r=1);
            if(isinstance(RiGGiE, list) == True):
                rigControllers.append(selections[i]);
            i+=1;
###############################################################################
# IF VALID RIG CONTROLLERS ARE SELECTED THEN SWAP RIG WITH NEW REFERENCE      #
############################################################################### 
        if(len(rigControllers) > 0):
            try:
                referencePath = py.referenceQuery(rigControllers[-1],rfn=1,p=1);
                py.file(fileFullPath,loadReference=referencePath,type="mayaAscii",options="v=0");
                py.headsUpMessage('"Rig successfully swapped with the '+thumbnailIDs[-1].text()+' rig!" - HiGGiE', t=1);
                print '"Rig successfully swapped with the '+thumbnailIDs[-1].text()+' rig!" - HiGGiE';  
            except:
                pass;
###############################################################################
# IF NO VALID RIG CONTROLLERS ARE SELECTED THEN ADD REFERENCE TO SCENE        #
############################################################################### 
        elif(len(rigControllers) == 0):
            py.file(fileFullPath, namespace=thumbnailIDs[-1].text(), mnp=1, iv=1, r=1);
            py.headsUpMessage('"Successfully added the '+thumbnailIDs[-1].text()+' rig to the scene!" - HiGGiE', t=1);
            print '"Successfully added the '+thumbnailIDs[-1].text()+' rig to the scene!" - HiGGiE';  

               
ui = theWindow()
ui.show()