###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import os
import glob
import json
import maya.cmds as py
import maya.mel as mel
from pymel.core.runtime import FrameSelected;
from pymel.core.runtime import ToggleViewAxis;
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
#"""# SAVES A POSE TO A TEXT FILE                                             #
###############################################################################   
def SAVEPOSE(listPoseWidget,home):
    poseSettings = "";
    pathContainer = "";
    customFile = py.file(home+"CUSTOM.json", q=1, ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
    primaryColor = [];
    secondaryColor = [];
    secondaryFont = "smallFixedWidthFont";
    i=0;
    while(i < 3):
        primaryColor.append(float(line['PRIMARY UI COLOR'].split(",")[i]));
        secondaryColor.append(float(line['SECONDARY UI COLOR'].split(",")[i]));
        i+=1;  
###############################################################################
# DETERMINES THE VALIDITY OF THE PREVIOUSLY SELECTED                          #
############################################################################### 
    rigControllers = [];
    selections = py.ls(sl=1);
    i=0;
    while(i < len(selections)):
        RiGGiE = py.listAttr(selections[i], st=["RiGGiE"], r=1);
        WiGGiE = py.listAttr(selections[i], st=["WiGGiE"], r=1);
        if(isinstance(RiGGiE,list) == 1 or isinstance(WiGGiE,list) == 1):
            rigControllers.append(selections[i]); 
        i+=1;
    if(rigControllers != []):
        nameSpace = "";
        if(":" in rigControllers[0]):
            name = rigControllers[0].split(":")[-1];
            nameSpace = rigControllers[0][0:(len(rigControllers[0])-len(name))];
        else:
            name = rigControllers[0];
###############################################################################
# FIND ALL CONTROLLERS IN FIRST SELECTION                                     #
###############################################################################
        outputControllers = [];
        masterCenter = name.replace("_L_","_M_").replace("_R_","_M_");
        masterName = masterCenter.replace(masterCenter.split("_")[2],"master");
        masterController = nameSpace+masterName.replace(masterName.split("_")[-1],"CTRL");
        outputItems = py.listRelatives(masterController,ad=1,pa=1);
        outputControllerShapes = [s for s in outputItems if "CTRL" in s];
        outputShapes = [s for s in outputItems if "Shape" in s];
        outputItems = list(set(outputControllerShapes) - set(outputShapes));
        i=0;
        while(i < len(outputItems)):
            RiGGiE = py.listAttr(outputItems[i], st=["RiGGiE"], r=1);
            WiGGiE = py.listAttr(outputItems[i], st=["WiGGiE"], r=1);
            if(isinstance(RiGGiE,list) == 1 or isinstance(WiGGiE,list) == 1):
                outputControllers.append(outputItems[i]);
            i+=1;
        outputControllers.insert(0,masterController);
###############################################################################
# GATHER CONTROLLERS AND THEIR ATTRIBUTES AND VALUES THEN STORE IN STRING     #
###############################################################################
        dialog = py.promptDialog(t="Pose Name",m="What kind of pose is this?",
                                 b=["OK","CANCEL"],db="OK",
                                 cb="CANCEL",ds="OK");
        poseName = py.promptDialog(text=1,q=1);
        try:
            poseName.decode('ascii');
        except:
            poseName = "?";
        if(dialog != "CANCEL" and len(poseName) > 0 and "?" not in poseName and "/" not in poseName):
            poseName = poseName.replace("_POSE","");
            i=0;
            while(i < len(outputControllers)):
                controller = outputControllers[i][len(nameSpace):];
                poseSettings = poseSettings+controller+"--";
                attribute = py.listAttr(outputControllers[i],k=1);
                rotationOrder = py.listAttr(outputControllers[i], st=["ROTATE_ORDER"], r=1);
                if(isinstance(rotationOrder,list) == 1 and isinstance(attribute,list) == 1):
                    attribute.append("ROTATE_ORDER");
                if(isinstance(attribute,list) == 1):
                    ii=0;
                    while(ii < len(attribute)):
                        poseSettings=poseSettings+attribute[ii]+"=";
                        value = py.getAttr(outputControllers[i]+"."+attribute[ii]);
                        poseSettings=poseSettings+str(value)+",";
                        ii+=1;
                    poseSettings=poseSettings+"\r\n";
                i+=1;
            #DETERMINE LOCAL OR GLOBAL PATH FOR POSE TO BE SAVED TO
            globalPosePath = "R:/Jx4/tools/dcc/maya/scripts/poseLibrary/";
            localPosePath = line['POSE (PATH)'];
            
            if(os.path.isdir(globalPosePath) == 1 and line['LOCAL POSE'] == 0 and line['GLOBAL POSE'] == 1):
                dialogPassword = py.promptDialog(t="Save Global Pose",m="What is the password?",
                                         b=["OK","CANCEL"],db="OK",
                                         cb="CANCEL",ds="OK");
                passwordAttempt = py.promptDialog(text=1,q=1);
                try:
                    passwordAttempt.decode('ascii');
                except:
                    passwordAttempt = "?";
                if(dialogPassword != "CANCEL" and passwordAttempt.lower() == "kendrick"):
                    posePath = globalPosePath;
                else:
                    posePath = localPosePath;
            else:
                posePath = localPosePath;
            
            if(line['LOCAL POSE'] == 1 or (line['GLOBAL POSE'] == 1 and posePath == globalPosePath)):
                if(localPosePath != globalPosePath):
                    input = open(posePath+"p_"+poseName+"_POSE.txt", "w+");
                    outline = input.writelines(poseSettings);
                    input.close();
            else:
                posePath = "none";
                print '"Please check the LOCAL PATH (or GLOBAL PATH) on." - HiGGiE';
                py.headsUpMessage('"Please check the LOCAL PATH (or GLOBAL PATH) on." - HiGGiE', t=2);
            if(localPosePath == globalPosePath):
                posePath = "none";
                print '"LOCAL PATH cannot be the same as the GLOBAL PATH!" - HiGGiE';
                py.headsUpMessage('"LOCAL PATH cannot be the same as the GLOBAL PATH!" - HiGGiE', t=2);  
###############################################################################
# UPDATE UI WITH NEW LIST                                                     #
###############################################################################
            if(posePath != "none"):
                globalTextFiles = [];
                localTextFiles = [];
                if(os.path.isdir(globalPosePath) == 1 and line['GLOBAL POSE'] == 1):
                    globalTextFiles = glob.glob(globalPosePath+"*_POSE.txt");
                if(os.path.isdir(localPosePath) == 1 and line['LOCAL POSE'] == 1):
                    localTextFiles = glob.glob(localPosePath+"*_POSE.txt");
                
                textFiles = globalTextFiles+localTextFiles;
                i=0;
                while(i < len(textFiles)):
                    pathContainer = pathContainer+textFiles[i].replace("\\","/");
                    pathContainer = pathContainer+",";
                    i+=1;
                os.remove(home+"CUSTOM.json");
                line['POSE FILES (FULL NAME)'] = pathContainer;
                presets = line;
                with open(home+'CUSTOM.json', 'w+') as f:
                     json.dump(presets, f, sort_keys=False, indent=4);
                #TAKE SCREEN CAP
                ToggleViewAxis();
                mel.eval("setCameraNamesVisibility(0);");
                gridStatus = 0 if(py.grid(tgl=1,q=1) == 1) else 1;py.grid(tgl=gridStatus);
                currentCamera = py.lookThru(q=1);
                translations = list(py.getAttr(currentCamera+".t")[0]);
                centerOfInterest = py.getAttr(currentCamera+".centerOfInterest");
                py.setAttr(currentCamera+"Shape.cameraScale", 1);
                FrameSelected();
                py.setAttr(currentCamera+"Shape.cameraScale", 0.25);
                thumbnailFormat = py.getAttr("defaultRenderGlobals.imageFormat");
                py.setAttr("defaultRenderGlobals.imageFormat", 32);
                currentFrame = py.currentTime(q=1);
                #START: APPLY BACKGROUND COLOR
                scaleValue = 10000;
                shader = py.shadingNode("blinn",asShader=1);
                shaderGRP = py.sets(renderable=1,noSurfaceShader=1,empty=1);
                py.connectAttr('%s.outColor'%shader,'%s.surfaceShader'%shaderGRP);
                background = py.polyCube()[0];
                
                py.hyperShade(assign=shader);
                py.polyNormal(background,normalMode=0,userNormalMode=0,ch=1);
                
                py.parentConstraint(selections,background,mo=0,w=1);
                py.setAttr(background+".s", scaleValue,scaleValue,scaleValue);
                
                if(posePath == localPosePath):
                    py.setAttr(shader+".incandescence", 0.0771, 0.2296, 0.2901, type="double3");
                else:
                    py.setAttr(shader+".incandescence", 0.4318, 0.2022, 0.2022, type="double3");
                py.setAttr(shader+".color", 0, 0, 0, type="double3");
                py.setAttr(shader+".eccentricity",0);
                py.select(selections,r=1);
                #END: APPLY BACKGROUND COLOR
                py.playblast(frame=currentFrame,format="image",cf=posePath+"p_"+poseName+"_POSE.png",wh=[100,200],p=100,v=0);
                py.delete(background,shader);
                py.setAttr("defaultRenderGlobals.imageFormat",thumbnailFormat);  
                py.setAttr(currentCamera+"Shape.cameraScale", 1);
                py.setAttr(currentCamera+"Shape.centerOfInterest", centerOfInterest);
                py.setAttr(currentCamera+".t", translations[0],translations[1],translations[2]);
                gridStatus = 0 if(py.grid(tgl=1,q=1) == 1) else 1;py.grid(tgl=gridStatus);
                ToggleViewAxis();
                #ADD ITEMS TO GRID
                thumbnailSize = [100,180];
                poseList = line['POSE FILES (FULL NAME)'].split(",");
                listPoseWidget.clear();
                i=0;
                while(i < len(poseList)):
                    if(len(poseList[i]) > 0 and py.file(poseList[i],q=1,ex=1) == 1):
                        if(py.file(poseList[i].replace(".txt",".png"),q=1,ex=1) == 1):
                            name = poseList[i].split("/")[-1].split(".")[0].split("_POSE")[0].replace("p_","",1);
                            thumbnailItem = qt.QListWidgetItem(name);
                            thumbnailImage = qt.QIcon();
                            thumbnailImage.addPixmap(qt.QPixmap(_fromUtf8(poseList[i].replace(".txt",".png"))), qt.QIcon.Normal, qt.QIcon.Off);
                            thumbnailItem.setIcon(thumbnailImage);
                            listPoseWidget.addItem(thumbnailItem);
                    i+=1;
                py.headsUpMessage('"Successfully saved your '+poseName+' pose to: '+posePath+'" - HiGGiE', t=3);
        elif(dialog != "CANCEL" and len(poseName) > 0 and ("?" in poseName or "/" in poseName)):
            print '"You must type a valid name (English only and no "_")." - HiGGiE'
            py.headsUpMessage('"You must type a valid name (English only and no "_")." - HiGGiE', t=10);
    else:
        print '"You must select a valid rig controller." - HiGGiE'
        py.headsUpMessage('"You must select a valid rig controller." - HiGGiE', t=2);
