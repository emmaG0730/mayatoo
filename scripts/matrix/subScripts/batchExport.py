###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################   
import os
import sys
import glob
import json
import platform
import datetime
import maya.cmds as py
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
module = path+'animationTransfer.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import animationTransfer#animationTransfer = reload(animationTransfer);
module = path+'exportFile.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import exportFile#exportFile = reload(exportFile);
###############################################################################
#"""# CALLS THE IMPORT AND EXPORT FUNCTION ON EACH LISTED FILE IN ORDER       #
###############################################################################   
def BATCHEXPORT(exportFiles,exportPaths,listImportWidget,home):
    dialog = "";
    customFile = home+"CUSTOM.json" if(".json" not in home.split("/")[-1]) else home;
    customFileCheck = py.file(customFile, q=1, ex=1);
    if(customFileCheck == 1):
        with open(customFile, 'r') as f:
            line = json.load(f);
    if(str(listImportWidget) != "none"):
        dialog = py.confirmDialog(t="Batch Exporter",
        m="The exporter will open a new scene. Is that okay?",
        b=["Cancel Export", "Save first", "Yes, continue"],
        db="Yes, continue",cb="Cancel Export",ds="Cancel Export");
###############################################################################
#"""# GET DATE AND TIME                                                       #
###############################################################################
    DATE = [];
    TODAY = datetime.date.today();
    DATE.append(TODAY);
    DATE = str(DATE[0]);
    TIME = datetime.datetime.now().time()
    TIME = TIME.isoformat()
###############################################################################
#"""# LOG DATA                                                                #
###############################################################################
    LOG = py.file(home+"LOG.txt", q=1, ex=1);
    if(LOG == 1):
        logFile = open(home+"LOG.txt", "r");
        logLines = logFile.readlines(); 
        logFile = open(home+"LOG.txt", "w+");
        i=0;
        while(i < len(logLines)):
            logFile.write(logLines[i]);
            i+=1;  
        logFile.write("\r\n#####################################################################################################"); 
        logFile.write("\r\n# #               EXPORT DATE: "+DATE+"         --         EXPORT TIME: "+TIME[0:8]+"                # #"); 
        logFile.write("\r\n#####################################################################################################"); 
        logFile = open(home+"LOG.txt", "r");
        logLines = logFile.readlines(); 
    else:
        logFile = open(home+"LOG.txt", "w+");
        logFile.write("\r\n#####################################################################################################"); 
        logFile.write("\r\n# #               EXPORT DATE: "+DATE+"         --         EXPORT TIME: "+TIME[0:8]+"                # #"); 
        logFile.write("\r\n#####################################################################################################"); 
        logFile = open(home+"LOG.txt", "r");
        logLines = logFile.readlines(); 
    if(dialog == "Yes, continue" or dialog == "Save first" or str(listImportWidget) == "none"):
        if(line['EXPORT AS .MA'] == 1 or line['EXPORT AS .FBX'] == 1 or line['EXPORT AS .XMD'] == 1 or line['EXPORT STARMAN'] == 1 or line['EXPORT STARMAN WEAPON'] == 1):
###############################################################################
# XMD AND FBX PLUGIN INFO                                                     #
###############################################################################
            dialog = "";
            pluginLog = "";
            xmdPlugin = "MayaXMDExportPlugin2016";
            if(line['EXPORT AS .XMD'] == 1 and py.pluginInfo(xmdPlugin,l=1,q=1) == 0):
                try:
                    xmdPlugin = py.pluginInfo(xmdPlugin,p=1,q=1);
                    py.loadPlugin(xmdPlugin);
                    pluginLog = "XMD:pass";
                except:
                    py.headsUpMessage('"You need to install the XMD exporter to export XMD files." - HiGGiE', t=3);
                    print "You need to install the XMD exporter to export XMD files"; 
                    dialog = py.confirmDialog(t="Export Alert!",
                    m="The Matrix is attempting to export an XMD file, but it is not installed.",
                    b=["Cancel Export"],
                    db="Cancel Export",cb="Cancel Export",ds="Cancel Export");
                    pluginLog = "XMD:fail";
            fbxPlugin = "fbxmaya";
            if(line['EXPORT AS .FBX'] == 1 and py.pluginInfo(fbxPlugin,l=1,q=1) == 0 and "fail" not in pluginLog):
                try:
                    fbxPlugin = py.pluginInfo(fbxPlugin,p=1,q=1);
                    py.loadPlugin(fbxPlugin);
                    pluginLog = pluginLog+";"+"FBX:pass";
                except:
                    py.headsUpMessage('"You need to install the FBX exporter to export FBX files." - HiGGiE', t=3);
                    print "You need to install the FBX exporter to export FBX files";
                    dialog = py.confirmDialog(t="Export Alert!",
                    m="The Matrix is attempting to export an FBX file, but it is not installed.",
                    b=["Cancel Export"],
                    db="Cancel Export",cb="Cancel Export",ds="Cancel Export");
                    pluginLog = pluginLog+";"+"FBX:fail";
###############################################################################
#"""# BEGIN BATCH ITEM CHECK IF PLUGIN STATUS PASSES                          #
###############################################################################
            if("fail" not in pluginLog):
                if(str(listImportWidget) != "none"):
                    #SELECT 1ST ITEM IN LIST
                    listImportWidget.item(0).setSelected(True);
                if(dialog == "Save first"):
                    py.file(f=1, type='mayaAscii', save=1);
                py.file(f=1, newFile=1);
                batchFiles = line['BATCH FILES (FULL NAME)'].split(",");
                if(len(batchFiles) > 1 and py.file(batchFiles[-1],q=1,ex=1) == 0):
                    batchFiles.remove(batchFiles[-1]);
                listImportWidget.setCurrentRow(0);
###############################################################################
#"""# START OF IMPORT/EXPORT LOOP                                             #
###############################################################################
    	        i=0;
    	        while(i < len(batchFiles)):
    	            index = batchFiles[i].split("/")[-1];
    	            if(listImportWidget != "none"):
    	                #MOVE DOWN THE LIST IF UI EXISTS
    	                listImportWidget.item(i).setSelected(True);
    	            fileToImport = batchFiles[i];
    	            fileToExport = fileToImport;
    	            logFile = open(home+"LOG.txt", "r");
    	            logLines = logFile.readlines();
    	            logFile = open(home+"LOG.txt", "w+");
    	            try:
    	                pathSections = fileToExport.split("/");
    	                importFile.IMPORTFILE(fileToImport,listImportWidget,1,home);
    	                py.headsUpMessage('"Imported '+batchFiles[i].split("/")[-1] + '!" - HiGGiE', t=3);
    	                if("," in line['EXPORT FOLDER (PATH)']):
    	                    fileName = line['EXPORT FOLDER (PATH)'].split(",")[i].split("/")[-1].split(".")[0];
    	                    exportPath = line['EXPORT FOLDER (PATH)'].split(",")[i].split(fileName)[0];
    	                else:
    	                    fileName = pathSections[len(pathSections)-1].split(".")[0];
    	                    exportPath = line['EXPORT FOLDER (PATH)'];
    	                exportFile.EXPORTFILE(fileToExport,exportPath,fileName,home);
    	                py.headsUpMessage('"Exported '+batchFiles[i].split("/")[-1] + '!" - HiGGiE', t=3);
    	                fileSections = batchFiles[i].split("/");
    	                ii=0;
    	                while(ii < len(logLines)):
    	                    logFile.write(logLines[ii]);
    	                    ii+=1;
    	                logFile.write("\r\nSuccessfully exported "+str(line['EXPORT FOLDER (PATH)']+fileSections[len(fileSections)-1].split(".")[0]).split("/")[-1]+" to: "+line['EXPORT FOLDER (PATH)']);
    	                logFile.close();
    	            except:
    	                fileSections = batchFiles[i].split("/");
    	                ii=0;
    	                while(ii < len(logLines)):
    	                    logFile.write(logLines[ii]);
    	                    ii+=1;
    	                logFile.write("\r\nFailed to export "+str(line['EXPORT FOLDER (PATH)']+fileSections[len(fileSections)-1].split(".")[0]).split("/")[-1]+" to: "+line['EXPORT FOLDER (PATH)']);
    	                logFile.close();
    	            #if("1" in line['EXPORT AS .MA']):
    	            #    py.file(newFile=1, f=1);
    	            py.file(newFile=1, f=1);
    	            i+=1;
    	        py.headsUpMessage('"Batch complete!" - HiGGiE', t=7);
	    else:
	        py.headsUpMessage('"Please select at least one file type to export." - HiGGiE', t=7);
###############################################################################
#"""# END OF IMPORT/EXPORT; NOW OPENS NEW FILE AND CONTINUES LOOP             #
###############################################################################
    else:
        py.headsUpMessage('"Batch cancelled." - HiGGiE', t=7);