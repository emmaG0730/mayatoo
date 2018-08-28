###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import os
import sys
import json
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
module = path+'undoChunk.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
from undoChunk import undo
###############################################################################
#"""# LOADS A POSE FROM A TEXT FILE AND IMPORTS ONTO THE RIG ELEMENT          #
###############################################################################
@undo
def LOADPOSE(listPoseWidget,action,home):
    try:
        thumbnailIDs = [];
        thumbnailCount = listPoseWidget.selectedItems();
        i=0;
        while(i < len(thumbnailCount)):
            thumbnailIDs.append(thumbnailCount[i]);
            i+=1;
        selectedPose = "p_"+thumbnailIDs[-1].text()+"_POSE.txt";
        poseSelection = True;
    except:
        poseSelection = False;
    customFile = py.file(home+"CUSTOM.json", q=1, ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
###############################################################################
# DETERMINES THE VALIDITY OF THE PREVIOUSLY SELECTED                          #
###############################################################################
    rigControllers = [];
    selections = py.ls(sl=1);
    i=0;
    while(i < len(selections) and poseSelection == True):
        RiGGiE = py.listAttr(selections[i], st=["RiGGiE"], r=1);
        WiGGiE = py.listAttr(selections[i], st=["WiGGiE"], r=1);
        if(isinstance(RiGGiE,list) == 1 or isinstance(WiGGiE,list) == 1):
            rigControllers.append(selections[i]); 
        i+=1;
    if(rigControllers != [] and poseSelection == True):
        nameSpace = "";
        if(":" in rigControllers[0]):
            name = rigControllers[0].split(":")[-1];
            nameSpace = rigControllers[0][0:(len(rigControllers[0])-len(name))];
        else:
            name = rigControllers[0];
###############################################################################
# FIND ALL CONTROLLERS IN FIRST SELECTION                                     #
###############################################################################
        inputControllers = [];
        fingerAssets = ["pinky", "ring", "middle", "index", "thumb"];
        toeAssets = ["pinkyToe", "ringToe", "middleToe", "indexToe", "bigToe"];
        masterCenter = name.replace("_L_","_M_").replace("_R_","_M_");
        masterName = masterCenter.replace(masterCenter.split("_")[2],"master");
        masterController = nameSpace+masterName.replace(masterName.split("_")[-1],"CTRL");
        inputItems = py.listRelatives(masterController,ad=1,pa=1);
        inputControllerShapes = [s for s in inputItems if "CTRL" in s];
        inputShapes = [s for s in inputItems if "Shape" in s];
        inputGroups = [s for s in inputItems if "GRP" in s];
        inputItems = list(set(inputControllerShapes) - set(inputShapes));
        inputItems = list(set(inputItems) - set(inputGroups));
        #ADD FINGERS OR TOES IF WRIST OR ANKLE IS IN SELECTION
        if(len(rigControllers) > 0):
            handController = rigControllers[0].replace(rigControllers[0].split("_")[2],"wrist");
            armController = rigControllers[0].replace(rigControllers[0].split("_")[2],"arm");
            footController = rigControllers[0].replace(rigControllers[0].split("_")[2],"foot");
            legController = rigControllers[0].replace(rigControllers[0].split("_")[2],"leg");
            #FINGERS IF IK/FK HAND SELECTED
            if(handController in rigControllers or armController in rigControllers):
                i=0;
                while(i < len(fingerAssets)):
                    ii=1;
                    targetDigit = rigControllers[0].replace(rigControllers[0].split("_")[2],fingerAssets[i]+str(ii));
                    while(py.objExists(targetDigit) == 1):
                        rigControllers.append(targetDigit);ii+=1;
                        targetDigit = rigControllers[0].replace(rigControllers[0].split("_")[2],fingerAssets[i]+str(ii));
                    i+=1;
            #TOES IF IK/FK FOOT SELECTED
            if(footController in rigControllers or legController in rigControllers):
                i=0;
                while(i < len(toeAssets)):
                    ii=1;
                    targetDigit = rigControllers[0].replace(rigControllers[0].split("_")[2],toeAssets[i]+str(ii));
                    while(py.objExists(targetDigit) == 1):
                        rigControllers.append(targetDigit);ii+=1;
                        targetDigit = rigControllers[0].replace(rigControllers[0].split("_")[2],toeAssets[i]+str(ii));
                    i+=1;
        i=0;
        while(i < len(inputItems)):
            RiGGiE = py.listAttr(inputItems[i], st=["RiGGiE"], r=1);
            WiGGiE = py.listAttr(inputItems[i], st=["WiGGiE"], r=1);
            if(isinstance(RiGGiE,list) == 1 or isinstance(WiGGiE,list) == 1):
                inputControllers.append(inputItems[i]);
                if(inputItems[i] in rigControllers):
                    if any(x in inputItems[i] for x in fingerAssets):
                        #ADD OPTIONS BOX IF FINGER ASSET
                        element = inputItems[i].split("_")[-3];
                        optionsBox = inputItems[i].replace(element,"armOptionsBox");
                        if(optionsBox not in rigControllers):
                            rigControllers.append(optionsBox);
                    if any(x in inputItems[i] for x in toeAssets):
                        #ADD OPTIONS BOX IF TOE ASSETS
                        element = inputItems[i].split("_")[-3];
                        optionsBox = inputItems[i].replace(element,"legOptionsBox");
                        if(optionsBox not in rigControllers):
                            rigControllers.append(optionsBox);
            i+=1;
        inputControllers.insert(0,masterController);
###############################################################################
# MATCH POSITION OF PELVIS USING THE PIVOT CONTROLLER                         #
###############################################################################
        matchPelvis = 1;
        trajectoryController = masterController.replace("master","trajectory");
        pelvisController = masterController.replace("master","spineMaster");
        pivotController = masterController.replace("master","pivot");
        masterList = [masterController,pivotController,pelvisController];
###############################################################################
# COLLECT TRANSLATION VALUES FROM MASTER LIST FOR POSSIBLE OFFSET (LATER)     #
###############################################################################
        translationArrayList = [];
        rotationArrayList = [];
        i=0;
        while(i < len(masterList)):
            translations = list(py.getAttr(masterList[i]+".t")[0]);
            translationArrayList.append(translations);
            rotations = list(py.getAttr(masterList[i]+".r")[0]);
            rotationArrayList.append(rotations);
            i+=1;
###############################################################################
# SET VALUES TO THAT OF THE POSE FILE                                         #
###############################################################################
        axis = ["X","Y","Z"];
        trajectory = "none";
        ikControllerList = [];
        pvControllerList = [];
        posePath = line['POSE (PATH)'];
        try:
            poseFile = open(posePath+selectedPose, "r");
        except:
            poseFile = open("R:/Jx4/tools/dcc/maya/scripts/poseLibrary/"+selectedPose, "r");
        poseSettings = poseFile.readlines();
        poseFile.close();
        #KILL SCRIPTJOBS
        scriptJobs = py.scriptJob(listJobs=1);
        killInstrumentHigh = False;
        if any("instrument(\'high\')" in s for s in scriptJobs):
            scriptToKill = [s for s in scriptJobs if "instrument(\'high\')" in s];
            scriptToKill = int(scriptToKill[0].split(":")[0]);
            timelinesScriptJob = py.scriptJob(k=scriptToKill, f=1);
            killInstrumentHigh = True;
        killInstrumentLow = False;
        if any("instrument(\'low\')" in s for s in scriptJobs):
            scriptToKill = [s for s in scriptJobs if "instrument(\'low\')" in s];
            scriptToKill = int(scriptToKill[0].split(":")[0]);
            timelinesScriptJob = py.scriptJob(k=scriptToKill, f=1);
            killInstrumentLow = True;
        #CREATE ROTATION ORDER OFFSET LOCATORS
        rotationOrderOld = py.spaceLocator(p=(0,0,0))[0];
        rotationOrderNew = py.spaceLocator(p=(0,0,0))[0];
        #LOOP THROUGH CONTROLLERS PASTING ATTRIBUTE VALUES
        i=0;
        while(i < len(poseSettings)):
            py.parent(rotationOrderNew,rotationOrderOld);
            outputController = poseSettings[i].split("--")[0];
            outputAttributes = poseSettings[i].split("--")[-1].split(",")[:-1];
            controllerSearch = [s for s in inputControllers if outputController in s];
            #GET PELVIS SETTINGS FOR TRAJECTORY OFFSET/MATCHING (LATER)
            if("spineMaster" in outputController):
                pelvisSettings = poseSettings[i];
                #GET POSE'S PELVIS TRANSLATIONS
                pelvisTranslations = [];
                poseTranslationValues = pelvisSettings.split("translate")[1:];  
                ii=0;
                while(ii < len(poseTranslationValues)):
                    pelvisTranslations.append(float( poseTranslationValues[ii].split(",")[0].split("=")[-1] ));
                    ii+=1;
                #GET POSE'S PELVIS ROTATIONS
                pelvisRotations = [];
                poseRotationValues = pelvisSettings.split("rotate")[1:];
                ii=0;
                while(ii < len(poseRotationValues)):
                    pelvisRotations.append(float( poseRotationValues[ii].split(",")[0].split("=")[-1] ));
                    ii+=1; 
                #GET POSE'S PELVIS ROTATION ORDER  
                if("ROTATE_ORDER" in pelvisSettings):
                    pelvisRotationOrder = int(pelvisSettings.split("ROTATE_ORDER")[-1].split(",")[0].replace("=",""));   
                else:
                    pelvisRotationOrder = 5; #ZYX;
            #GET TRAJECTORY SETTINGS FOR OFFSET/MATCHING (LATER)        
            elif("trajectory" in outputController):
                trajectorySettings = poseSettings[i];
                if("ROTATE_ORDER" in trajectorySettings):
                    trajectoryRotationOrder = int(trajectorySettings.split("ROTATE_ORDER")[-1].split(",")[0].replace("=",""));
                else:
                    trajectoryRotationOrder = 0; #XYZ
            #GET MASTER'S ROTATION ORDER FOR OFFSET/MATCHING (LATER)        
            elif("master" in outputController):
                masterSettings = poseSettings[i];
                if("ROTATE_ORDER" in masterSettings):
                    masterRotationOrder = int(masterSettings.split("ROTATE_ORDER")[-1].split(",")[0].replace("=",""));
                else:
                    masterRotationOrder = 0; #XYZ
            if(len(controllerSearch) != 0):
                #ADD IK CONTROLLERS TO LIST FOR OFFSETTING (LATER)
                targetController = controllerSearch[0];
                if(targetController.split("_")[-3] == "arm" or targetController.split("_")[-3] == "leg"):
                    ikControllerList.append(targetController);
                elif("PV" in targetController.split("_")[-3]):
                    pvControllerList.append(targetController);
                #FLIP TARGET SIDES IF MIRROR IS ACTIVATED 
                weaponStatus = py.listAttr(targetController, st=["WiGGiE"], r=1);
                if(action == "mirror"):
                    if("_L_" in targetController and isinstance(weaponStatus,list) == 0):
                        targetController = controllerSearch[0].replace("_L_","_R_");
                    elif("_R_" in targetController and isinstance(weaponStatus,list) == 0):
                        targetController = controllerSearch[0].replace("_R_","_L_");
                py.setAttr(rotationOrderOld+".rotate", 0,0,0);
                py.setAttr(rotationOrderNew+".rotate", 0,0,0);
                ii=0;
                while(ii < len(outputAttributes)):
                    skip=0;
                    match = 0;
                    reverse = 1; 
                    attr = outputAttributes[ii].split("=")[0];
                    #MIRROR VALUES IF CHOSEN BY USER
                    if(("rotateY" in attr or "rotateZ" in attr) and "_M_" in targetController and action == "mirror" and isinstance(weaponStatus,list) == 0):
                        reverse = -1;
                    elif(("rotateY" in attr or "rotateZ" in attr) and action == "mirror" and isinstance(weaponStatus,list) == 0):
                        if("arm" in targetController or "leg" in targetController):
                            reverse = -1;
                    elif("translate" in attr and "arm" in targetController and action == "mirror" and isinstance(weaponStatus,list) == 0):
                        if("OptionsBox" not in targetController and "PV" not in targetController):
                            reverse = -1;
                    elif("translateX" in attr and "leg" in targetController and action == "mirror" and isinstance(weaponStatus,list) == 0):
                        if("OptionsBox" not in targetController and "PV" not in targetController):
                            reverse = -1;
                    elif("translateX" in attr and action == "mirror" and isinstance(weaponStatus,list) == 0):
                        if("OptionsBox" not in targetController and "PV" not in targetController):
                            reverse = -1;
                    value = outputAttributes[ii].split("=")[-1];
                    value = float(value)*reverse if("." in value) else int(value);
                    #SKIP ATTRIBUTES IF THE ATTRIBUTE IS A ROTATION ORDER
                    if("ROTATE_ORDER" in attr):
                        py.setAttr(rotationOrderOld+".rotateOrder",value);
                        skip = 1;
                    #PLUG ATTRIBUTE VALUES IF NODE AND ATTRIBUTE EXISTS
                    if(py.objExists(targetController) == 1):
                        attrExists = py.listAttr(targetController, st=[attr], r=1);
                    if(ii == 0):
                        postPasteRotationValues = False;
                    if(py.objExists(targetController) == 1 and isinstance(attrExists,list) == 1 and skip == 0):
                        if any(masterController in s for s in rigControllers):
                            #IF MASTER CONTROLLER IS IN LIST, PASTE ATTRIBUTES
                            if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                                py.setAttr(targetController+"."+attr, float(value));
                            postPasteRotationValues = True;
                        elif any(targetController in s for s in rigControllers):
                            #IF NOT, PASTE ONLY IF TARGET CONTROLLER IS IN SELECTED LIST
                            if(targetController != trajectoryController):#!
                                if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                                    py.setAttr(targetController+"."+attr, float(value));
                                postPasteRotationValues = True;
                        #IF ATTRIBUTE IS A ROTATION VALUE, PLUG INTO ROTATION ORDER OFFSET LOCATORS
                        if("rotate" in attr):
                            if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                                py.setAttr(rotationOrderOld+"."+attr, float(value));
                    ii+=1;
                #PLUG ROTATION ORDER OFFSETS INTO CONTROLLER
                if(py.objExists(targetController) == 1 and postPasteRotationValues == True):
                    rotationOrder = py.xform(targetController, roo=1, q=1);
                    py.xform(rotationOrderNew,p=1,roo=rotationOrder);
                    py.parent(rotationOrderNew,w=1);
                    ii=0;
                    while(ii < len(axis)):
                        offsetValue = py.getAttr(rotationOrderNew+".rotate"+axis[ii]);
                        try:
                            if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                                py.setAttr(targetController+".rotate"+axis[ii],offsetValue);
                        except:
                            pass;
                        ii+=1;
                else:
                    py.parent(rotationOrderNew,w=1);
            else:
                py.parent(rotationOrderNew,w=1);
            i+=1;
        py.delete(rotationOrderNew,rotationOrderOld);
        #ACTIVATE SCRIPTJOBS
        if(killInstrumentHigh == True):
            try:
                weaponSpaceScriptJob = py.scriptJob(ac=[nameSpace+"c_M_evaluator_v1_LOC.rx", "instrument('high')"], kws=1, cu=1);
            except:
                print '"Failed to re-activate the instrument(high) scriptJob..." - HiGGiE';
        if(killInstrumentLow == True):
            try:
                controllerSpaceScriptJob = py.scriptJob(ac=[nameSpace+"c_M_evaluator_v1_LOC.ry", "instrument('low')"], kws=1, cu=1);
            except:
                print '"Failed to re-activate the instrument(low) scriptJob..." - HiGGiE';
###############################################################################
# CREATE OFFSET LOCATORS FOR IK CONTROLLERS                                   #
###############################################################################
        ikLocatorList = [];
        i=0;
        while(i < len(ikControllerList)):
            ikGroup = py.listRelatives(ikControllerList[i],p=1)[0];
            ikLocator = py.spaceLocator(p=(0,0,0))[0];
            rotationOrder = py.xform(ikControllerList[i], roo=1, q=1);
            py.xform(ikLocator,p=1,roo=rotationOrder);
            py.parent(ikLocator,ikGroup);
            ipNode = ikControllerList[i].replace(ikControllerList[i].split("_")[-3],ikControllerList[i].split("_")[-3]+"InitialPositionIK");
            ipNode = ipNode.replace("CTRL","LOC");
            snap = py.parentConstraint(ipNode,ikLocator,mo=0,w=1);
            py.delete(snap);
            py.makeIdentity(ikLocator, a=1, t=1, r=1, n=0);#FREEZE
            snap = py.parentConstraint(ikControllerList[i],ikLocator,mo=0,w=1);
            py.delete(snap);
            py.parentConstraint(pelvisController,ikLocator,mo=1,w=1);
            ikLocatorList.append(ikLocator);
            i+=1;
        pvLocatorList = [];
        i=0;
        while(i < len(pvControllerList)):
            pvGroup = py.listRelatives(pvControllerList[i],p=1)[0];
            pvLocator = py.spaceLocator(p=(0,0,0))[0];
            rotationOrder = py.xform(pvControllerList[i], roo=1, q=1);
            py.xform(pvLocator,p=1,roo=rotationOrder);
            py.parent(pvLocator,pvGroup);
            snap = py.parentConstraint(pvControllerList[i],pvLocator,mo=0,w=1);
            py.delete(snap);
            py.parentConstraint(pelvisController,pvLocator,mo=1,w=1);
            pvLocatorList.append(pvLocator);
            i+=1;
###############################################################################
# ADD OFFSET TO HORIZONTAL, VERTICAL AND/OR ROTATION POSITIONS                #
###############################################################################
        if(line['ROTATION'] == 0):
            i=0;
            while(i < len(masterList)):
                if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                    py.setAttr(masterList[i]+".r",rotationArrayList[i][0],rotationArrayList[i][1],rotationArrayList[i][2]);
                i+=1;
        if(line['HORIZONTAL'] == 0 and line['VERTICAL'] == 1):
            positionTracker = py.spaceLocator(p=(0,0,0))[0];
            i=0;
            while(i < len(masterList)):
                parentGroup = py.listRelatives(masterList[i],p=1)[0];
                py.parent(positionTracker,parentGroup);
                py.setAttr(positionTracker+".t",translationArrayList[i][0],translationArrayList[i][1],translationArrayList[i][2]);
                snap = py.pointConstraint(masterList[i],positionTracker,skip=["x","z"],mo=0,w=1);
                py.delete(snap);
                translations = list(py.getAttr(positionTracker+".t")[0]);
                if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                    py.setAttr(masterList[i]+".t",translations[0],translations[1],translations[2]);
                i+=1;
            py.delete(positionTracker);
        elif(line['HORIZONTAL'] == 1 and line['VERTICAL'] == 0):
            positionTracker = py.spaceLocator(p=(0,0,0))[0];
            i=0;
            while(i < len(masterList)):
                parentGroup = py.listRelatives(masterList[i],p=1)[0];
                py.parent(positionTracker,parentGroup);
                py.setAttr(positionTracker+".t",translationArrayList[i][0],translationArrayList[i][1],translationArrayList[i][2]);
                snap = py.pointConstraint(masterList[i],positionTracker,skip=["y"],mo=0,w=1);
                py.delete(snap);
                translations = list(py.getAttr(positionTracker+".t")[0]);
                if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                    py.setAttr(masterList[i]+".t",translations[0],translations[1],translations[2]);
                i+=1;
            py.delete(positionTracker);
        elif(line['HORIZONTAL'] == 0 and line['VERTICAL'] == 0):
            i=0;
            while(i < len(masterList)):
                if not("trajectory" in targetController and line['TRAJECTORY'] == 0):
                    py.setAttr(masterList[i]+".t",translationArrayList[i][0],translationArrayList[i][1],translationArrayList[i][2]);
                i+=1;
###############################################################################
# ADD OFFSET TO IK CONTROLLERS                                                #
###############################################################################
        i=0;
        while(i < len(ikLocatorList)):
            translation = list(py.getAttr(ikLocatorList[i]+".t")[0]);
            rotation = list(py.getAttr(ikLocatorList[i]+".r")[0]);
            if any(masterController in s for s in rigControllers):
                py.setAttr(ikControllerList[i]+".t",translation[0],translation[1],translation[2]);
                py.setAttr(ikControllerList[i]+".r",rotation[0],rotation[1],rotation[2]);   
            elif any(ikControllerList[i] in s for s in rigControllers):
                py.setAttr(ikControllerList[i]+".t",translation[0],translation[1],translation[2]);
                py.setAttr(ikControllerList[i]+".r",rotation[0],rotation[1],rotation[2]);
            i+=1;
        py.delete(ikLocatorList[:]);   
        i=0;
        while(i < len(pvLocatorList)):
            decoyPV = py.duplicate(pvControllerList[i],ic=0,rc=1,rr=1)[0];
            snap = py.pointConstraint(pvLocatorList[i],decoyPV,mo=0,w=1);
            translation = list(py.getAttr(decoyPV+".t")[0]);
            if any(masterController in s for s in rigControllers):
                py.setAttr(pvControllerList[i]+".t",translation[0],translation[1],translation[2]);
            elif any(pvControllerList[i] in s for s in rigControllers):
                py.setAttr(pvControllerList[i]+".t",translation[0],translation[1],translation[2]);
            py.delete(decoyPV,snap);
            i+=1;
        py.delete(pvLocatorList[:]);  
###############################################################################
# ADD OFFSET TO TRAJECTORY CONTROLLER BASED ON LOADED POSE AND NEW POSITION   #
###############################################################################
        if(py.objExists(trajectoryController) == 1 and line['TRAJECTORY'] == 1):
            if(trajectoryController in rigControllers or masterController in rigControllers):
                #SETUP DECOY PELVIS LOCATOR 
                spineMaster = masterController.replace("master","spine").replace(masterController.split("_")[-1],"GRP");
                #translation = list(py.getAttr(spineMaster+".t")[0]);
                pelvisLocator = py.spaceLocator(n="pelvis_L",p=(0,0,0))[0];
                py.setAttr(pelvisLocator+".rotateOrder",pelvisRotationOrder);
                pelvisGroup = py.group(n="pelvis",r=1);
                py.xform(pelvisGroup,p=1,roo="xyz");
                #py.setAttr(pelvisGroup+".t",translation[0],translation[1],translation[2]);
                snap = py.parentConstraint(spineMaster,pelvisGroup);
                py.delete(snap);
                py.setAttr(pelvisLocator+".t", pelvisTranslations[0],pelvisTranslations[1],pelvisTranslations[2]);
                py.setAttr(pelvisLocator+".r", pelvisRotations[0],pelvisRotations[1],pelvisRotations[2]);
                #SETUP DECOY TRAJECTORY LOCATOR 
                trajectoryGroup = py.group(n="trajectory_G",em=1);
                py.setAttr(trajectoryGroup+".rotateOrder",masterRotationOrder);
                trajectoryLocator = py.spaceLocator(n="trajectory_L",p=(0,0,0))[0];
                py.setAttr(trajectoryLocator+".rotateOrder",trajectoryRotationOrder);
                py.parent(trajectoryLocator,trajectoryGroup);
                #PASTE POSE'S TRAJECTORY VALUES ONTO DECOY TRAJECTORY (LOCATOR)
                outputAttributes = trajectorySettings.split("--")[-1].split(",")[:-1];
                i=0;
                while(i < len(outputAttributes)):
                    attr = outputAttributes[i].split("=")[0];
                    value = outputAttributes[i].split("=")[-1];
                    value = float(value) if("." in value) else int(value);
                    hasAttr = py.listAttr(trajectoryLocator, st=[attr], r=1);
                    if(isinstance(hasAttr,list) == 1):
                        py.setAttr(trajectoryLocator+"."+attr, float(value));
                    i+=1;
                #PASTE POSE'S MASTER VALUES ONTO DECOY MASTER (GROUP)
                outputAttributes = masterSettings.split("--")[-1].split(",")[:-1];
                i=0;
                while(i < len(outputAttributes)):
                    attr = outputAttributes[i].split("=")[0];
                    value = outputAttributes[i].split("=")[-1];
                    value = float(value) if("." in value) else int(value);
                    hasAttr = py.listAttr(trajectoryGroup, st=[attr], r=1);
                    if(isinstance(hasAttr,list) == 1):
                        py.setAttr(trajectoryGroup+"."+attr, float(value));
                    i+=1;
                #CONNECT DECOY TRAJECTORY AND DECOY PELVIS HIERARCHIES
                py.parent(trajectoryGroup,pelvisLocator);
                py.parent(pelvisLocator,pelvisController);
                py.setAttr(pelvisLocator+".t",0,0,0);
                py.setAttr(pelvisLocator+".r",0,0,0);
                py.parent(trajectoryLocator,masterController);
                #SET TRAJECTORY VALUES TO THAT OF THE TRAJECTORY LOCATOR
                decoyTrajectory = py.duplicate(trajectoryController,ic=0,rc=1,rr=1)[0];
                snap = py.parentConstraint(trajectoryLocator,decoyTrajectory,mo=0,w=1);
                py.delete(snap);
                translation = list(py.getAttr(decoyTrajectory+".t")[0]);
                rotation = list(py.getAttr(decoyTrajectory+".r")[0]);
                py.setAttr(trajectoryController+".t",translation[0],translation[1],translation[2]);
                py.setAttr(trajectoryController+".r",rotation[0],rotation[1],rotation[2]);
                py.delete(pelvisGroup,pelvisLocator,trajectoryGroup,trajectoryLocator,decoyTrajectory);
###############################################################################
# CONTINUED: MATCH POSITION OF PELVIS USING THE PIVOT CONTROLLER              #
###############################################################################
        poseName = selectedPose.split("_POSE")[0].replace("p_","",1);
        py.headsUpMessage('"Successfully imported the '+poseName+' pose!" - HiGGiE', t=3);
    elif(poseSelection == False):
        print '"You must select a valid pose in the library." - HiGGiE';
        py.headsUpMessage('"You must select a valid pose in the library." - HiGGiE', t=2);
    else:
        print '"You must select a valid rig controller." - HiGGiE'
        py.headsUpMessage('"You must select a valid rig controller." - HiGGiE', t=2);
