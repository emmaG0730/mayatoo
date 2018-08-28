###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################   
import os
import sys
import glob
import json
import maya.cmds as py
import maya.mel as mel
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
#"""# PATH FINDING                                                            #
###############################################################################
path = "";
state = "";
mayaVersion = py.about(v=1);
documents = os.path.expanduser("~");
documents = documents+"/";
environment = documents+"maya/"+mayaVersion+"/Maya.env";
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
###############################################################################
#"""# IMPORT ADDITIONAL MODULES FOR THE MATRIX                                #
###############################################################################   
module = path+'importFile.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import importFile#importFile = reload(importFile);
###############################################################################
#"""# UPDATES UI'S EXPORT TEXT FIELD AND UPDATES SAVED SETTINGS               #
###############################################################################   
def EXPORTFIELD(line, editExportWidget, editPoseWidget, listPoseWidget, dictionary, folder, home):
    pathContainer = "";
    customFile = py.file(home+"CUSTOM.json", q=1, ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
    if(dictionary == 'EXPORT FOLDER (PATH)' and folder == "none"):
        folder = py.fileDialog2(cap="EXPORT LOCATION", dir=line[dictionary], okc="SELECT", cc="CANCEL", ds=2, fm=3);
    if(dictionary == 'POSE (PATH)' and folder == "none"):
        folder = py.fileDialog2(cap="POSE LOCATION", dir=line[dictionary], okc="SELECT", cc="CANCEL", ds=2, fm=3);
    if(isinstance(folder, list) == 1):
        if("/" in folder[0]):
            os.remove(home+"CUSTOM.json"); 
            line[dictionary] = folder[0]+"/";
            if(dictionary == 'EXPORT FOLDER (PATH)'):
                presets = line;
                with open(home+'CUSTOM.json', 'w+') as f:
                     json.dump(presets, f, sort_keys=False, indent=4);
                editExportWidget.setText(line[dictionary]);
            else:
                textFiles = glob.glob(line[dictionary]+"*_POSE.txt");
                i=0;
                while(i < len(textFiles)):
                    pathContainer = pathContainer+textFiles[i].replace("\\","/");
                    pathContainer = pathContainer+",";
                    i+=1;
                line['POSE FILES (FULL NAME)'] = pathContainer;
                presets = line;
                with open(home+'CUSTOM.json', 'w+') as f:
                     json.dump(presets, f, sort_keys=False, indent=4);
                editPoseWidget.setText(line[dictionary]);
                #ADD ITEMS TO GRID
                thumbnailSize = [100,180];
                poseList = line['POSE FILES (FULL NAME)'].split(",");
                listPoseWidget.clear();
                i=0;
                while(i < len(poseList)):
                    if(len(poseList[i]) > 0 and py.file(poseList[i],q=1,ex=1) == 1):
                        if(py.file(poseList[i].replace(".txt",".png"),q=1,ex=1) == 1):
                            name = poseList[i].split("/")[-1].split(".")[0].split("_")[1];
                            thumbnailItem = qt.QListWidgetItem(name);
                            thumbnailImage = qt.QIcon();
                            thumbnailImage.addPixmap(qt.QPixmap(_fromUtf8(poseList[i].replace(".txt",".png"))), qt.QIcon.Normal, qt.QIcon.Off);
                            thumbnailItem.setIcon(thumbnailImage);
                            listPoseWidget.addItem(thumbnailItem);
                    i+=1; 
                    
       