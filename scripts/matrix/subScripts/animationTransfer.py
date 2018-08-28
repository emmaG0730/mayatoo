###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import os
import sys
import time
import json
import maya.cmds as py
import maya.mel as mel
import pymel.core as pm
from pymel.core.runtime import FrameSelected;
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
module = path+'matchProportions.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import matchProportions#importFile = reload(matchProportions);
###############################################################################
#"""# TRANSFERS ANIMATION FROM ONE RIG TO ANOTHER                             #
###############################################################################  
def ANIMATIONTRANSFER(inputNameSpace,outputNameSpace,outputReference,home):
    translationValues = ["translateX","translateY","translateZ"];
    rotationValues = ["rotateX","rotateY","rotateZ"];
    keyableValues = translationValues+rotationValues;
    constraints = [];
    controllers = [];
    outputRoot = "none";
    outputPelvis = "none";
    outputTrajectory = "none";
    
    armElements = ["arm","armPV","armOptionsBox","clavicle","shoulder","elbow","wrist"];
    legElements = ["leg","legPV","legOptionsBox","hip","knee","ankle","ball"];
    ikElements = ["arm","armPV","leg","legPV","toe"];
    
    autoKeyState = py.autoKeyframe(state=1,q=1);
    py.autoKeyframe(state=0);
    py.playbackOptions(ps=1, e=1, min=0);#30FPS
    if(py.about(b=1,q=1) == 0):
        py.FrameSelected();py.currentUnit(time="ntsc");
        mel.eval('setUpAxis "y";  fitPanel -selected;');
    customFile = home+"CUSTOM.json" if(".json" not in home.split("/")[-1]) else home;
    customFileCheck = py.file(customFile, q=1, ex=1);
    if(customFileCheck == 1):
        with open(customFile, 'r') as f:
            line = json.load(f);
###############################################################################
#"""# CREATE A LIST OF CONTROLLERS FROM THE RIG ANIMATION WILL BE IMPORTED ON #
############################################################################### 
    selections = py.ls(sl=1)[0];
    if(inputNameSpace == "none"):
        inputNameSpace = "";
    if(":" in selections):
        name = selections.split(":")[-1];
    else:
        name = selections;
    masterCenter = name.replace("_L_","_M_").replace("_R_","_M_");
    masterName = masterCenter.replace(masterCenter.split("_")[2],"master");
    trajectoryName = masterCenter.replace(masterCenter.split("_")[2],"trajectory");
    masterController = inputNameSpace+masterName.replace(masterName.split("_")[-1],"CTRL");
    trajectoryController = inputNameSpace+trajectoryName.replace(trajectoryName.split("_")[-1],"CTRL");
    py.setAttr(masterController+".KEYALL", 0);
    inputControllers = [];
    outputControllers = [];
    inputInitialControllers = py.ls(inputNameSpace+"c_*");
    outputInitialControllers = py.ls(outputNameSpace+":c_*");
    i=0;
    while(i < len(inputInitialControllers)):
        if(inputInitialControllers[i].split("_")[-1] == "CTRL" and "Shape" not in inputInitialControllers[i]):
            inputControllers.append(inputInitialControllers[i]);
        i+=1;
    i=0;
    while(i < len(outputInitialControllers)):
        if(outputInitialControllers[i].split("_")[-1] == "CTRL" and "Shape" not in outputInitialControllers[i]):
            outputControllers.append(outputInitialControllers[i]);
        i+=1;
###############################################################################
#"""#CREATE A LIST OF CONTROLLERS FROM THE RIG ANIMATION WILL BE EXPORTED FROM#
###############################################################################
    #outputControllers = [];#!
    outputItems = py.ls(outputNameSpace+":*",type="transform",o=1);
    outputJoint = py.ls(outputNameSpace+":*", type="joint")[0];
    #SPECIAL CASE: IF OLD SKELETON (E JOINTS) EXISTS, REPLACE
    if(len(outputJoint) > 2):
        if(outputJoint[:2] == "e_"):
            if(py.objExists(outputJoint.replace("e_","b_",1)) == 1):
                outputJoint = outputJoint.replace("e_","b_",1);
        elif(":e_" in outputJoint):
            if(py.objExists(outputJoint.replace(":e_",":b_")) == 1):
                outputJoint = outputJoint.replace(":e_",":b_");
    #GET RELATED JOINTS FROM INITIAL SELECTION
    outputRootInitial = py.ls(outputJoint,l=1)[0].split("|")[2];
    outputRootGroup = py.ls(outputJoint,l=1)[0].split("|")[1];
    outputJoints = py.listRelatives(outputRootInitial,type="joint",ad=1,pa=1,s=0);
    outputJoints.reverse();
    outputJoints.insert(0,outputRootInitial);
    referenceFile = outputReference.split("/")[-1];
###############################################################################
#"""# CREATE A CAMERA TO TRACK/FOLLOW THE ANIMATION                           #
###############################################################################
    if(py.about(b=1,q=1) == 0):
        characterCamera = py.camera()[0];
        characterCameraGroup = py.group();
        py.setAttr(characterCamera+".t",220,220,400);
        py.setAttr(characterCamera+".r",-15,30,0);
        initialCamera = py.lookThru(q=1);
        py.lookThru(characterCamera);
        py.setAttr(initialCamera+".t",220,220,400);
        py.setAttr(initialCamera+".r",-15,30,0);
        py.pointConstraint(trajectoryController, characterCameraGroup, mo=0, w=1);
###############################################################################
#"""# SETS RIGS TO T POSE                                                     #
###############################################################################
    skipAttributes = ["attachment","visibility"];
    #INPUT
    i=0;
    while(i < len(inputControllers)):
        keyableAttributes = py.listAttr(inputControllers[i],u=1,k=1,v=1);
        if(isinstance(keyableAttributes,list) == 1):
            ii=0;
            while(ii < len(keyableAttributes)):
                if not any(x in keyableAttributes[ii].lower() for x in skipAttributes):
                    if("SPACE" not in keyableAttributes[ii]):
                        py.setAttr(inputControllers[i]+"."+keyableAttributes[ii],0);
                    else:
                        py.setAttr(inputControllers[i]+"."+keyableAttributes[ii],1);
                ii+=1;
        i+=1;
    #OUTPUT
    i=0;
    while(i < len(outputControllers)):
        keyableAttributes = py.listAttr(outputControllers[i],u=1,k=1,v=1);
        if(isinstance(keyableAttributes,list) == 1):
            ii=0;
            while(ii < len(keyableAttributes)):
                if("translate" in keyableAttributes[ii] or "rotate" in keyableAttributes[ii]):
                    py.setAttr(outputControllers[i]+"."+keyableAttributes[ii],0);
                ii+=1;
        i+=1;
###############################################################################
#"""# COLLECT TRANSFORM VALUES OF OUTPUT JOINTS AFTER TPOSE                   #
###############################################################################
    if(outputControllers != []):
        transformList = [];    
        i=0;
        while(i < len(outputJoints)):
            translations = list(py.getAttr(outputJoints[i]+".t")[0]);
            transformList.append(translations);
            i+=1;
    else:
        transformList = "invalid";
        py.headsUpMessage('"No valid controllers found. Will attempt to use joints instead." - HiGGiE', t=2);
        print '"No valid controllers found. Will attempt to use joints instead." - HiGGiE'
###############################################################################
#"""# TURN OFF SOLO MODE FOR EACH LAYER                                       #
###############################################################################  
    animationLayers = py.ls(type="animLayer");
    if(outputInitialControllers != []):
        isRiGGiE = py.listAttr(outputInitialControllers[0], st=["RiGGiE"], r=1);
        if(isinstance(isRiGGiE, list) == 1 and animationLayers != []):
            i=0;
            while(i < len(animationLayers)):
                py.animLayer(animationLayers[i],solo=0,lock=0,e=1);
                i+=1;
###############################################################################
#"""# FIND THE SOONEST AND LATEST KEYS OF ALL OUTPUT ITEMS                    #
###############################################################################
    firstFrame = 0;
    lastFrame = 0;
    i=0;
    while(i < len(outputItems)):
        currentFirstKey = 0;
        currentLastKey = 0;
        if not any(s in outputItems[i] for s in keyableValues):#IN CASE ITEM IS KEY
            currentFirstKey = round(py.findKeyframe(outputItems[i],w="first"),0);
            currentLastKey = round(py.findKeyframe(outputItems[i],w="last"),0);
            if(currentFirstKey < firstFrame):
                firstFrame = currentFirstKey
            if(currentLastKey > lastFrame):
                lastFrame = currentLastKey
            if(currentLastKey > 1000):
                print '"Warning: "'+outputItems[i]+'" has over 1000 keys. Transfer may take a while..." - HiGGiE';
        i+=1;
    difference = 0-firstFrame;
###############################################################################
#"""# IF RIG IS FROM HiGGiE: DO A DIRECT TRANSFER THROUGH CONTROLLERS         #
###############################################################################
    RiGGiE = False;
    outputMasterController = outputNameSpace+":"+"c_M_master_v1_CTRL";
    if(py.objExists(outputMasterController) == 1):
        isRiGGiE = py.listAttr(outputMasterController,st=["RiGGiE"],r=1);
        if(isinstance(isRiGGiE,list) == 1):
            #OUTPUT RIG IS CREATED BY HiGGiE; DIRECT TRANSFER IS ALLOWED
            RiGGiE = True;
            py.headsUpMessage('"This rig is RiGGiE status (made by HiGGiE)!" - HiGGiE', t=2);
            print '"This rig is RiGGiE status (made by HiGGiE)!" - HiGGiE';
    RiGGiE = False;#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
###############################################################################
#"""# SETS THE RIG TO FK MODE                                                 #
###############################################################################
    optionsBoxList = [];
    i=0;
    while(i < len(inputControllers)):
        if("OptionsBox_" in inputControllers[i] and inputControllers[i].split("_")[-1] == "CTRL"):
            MODE = py.listAttr(inputControllers[i], st=["MODE"], r=1);
            if(isinstance(MODE, list) == True):
                py.setAttr(inputControllers[i]+".MODE", 0);
                optionsBoxList.append(inputControllers[i]);
            inputControllers.remove(inputControllers[i]);
        i+=1;   
###############################################################################
#"""# BAKE THE SKELETON IN CASE IT IS ANIMATED BY CONTROLLERS (CONSTRAINTS)   #
###############################################################################
    if(RiGGiE == False):
        py.playbackOptions(minTime=0, maxTime=lastFrame+difference);
        py.currentTime(round(py.currentTime(q=1),0));
        py.headsUpMessage('"Baking imported skeleton." - HiGGiE', t=2);
        print '"Baking imported skeleton." - HiGGiE';
        py.bakeResults(outputJoints[:],t=(firstFrame,lastFrame),at=keyableValues,sm=1,s=0); 
###############################################################################
#"""# MAKE CONSTRAINT LAYER                                                   #
###############################################################################
    version=1;
    while(py.objExists("a_M_importedConstraints_v"+str(version)+"_LYR")):
        version+=1;
    conLayer = "a_M_importedConstraints_v"+str(version)+"_LYR";  
###############################################################################
#"""# CONNECT RIGS                                                            #
###############################################################################
    nameSpace = inputNameSpace;
    py.select(outputJoint,r=1);
    py.headsUpMessage('"Starting animation transfer..." - HiGGiE', t=2);
    print '"Starting animation transfer..." - HiGGiE';
    if(RiGGiE == False):
        out = matchProportions.MATCHPROPORTIONS(transformList,nameSpace,outputNameSpace,conLayer);
###############################################################################
#"""# SPECIAL CASE: TRANSFER ANIMATION DIRECTLY FROM CONTROLLERS              #
###############################################################################
    else:
        #CREATE NEW CONSTRAINT LAYER
        conLayer = py.animLayer("a_M_importedConstraints_v"+str(version)+"_LYR");
        py.setAttr(conLayer+".rotationAccumulationMode", 1);
        py.setAttr(conLayer+".scaleAccumulationMode", 0);
        #py.animLayer(conLayer,solo=1,e=1);
        #MUTE LAYERS CONNECTED TO THE INPUT RIG
        
        py.select(outputControllers[:],r=1); 
        relevantOutputLayers = py.animLayer(affectedLayers=1,q=1);
        
        
        
        py.select(inputControllers[:],r=1); 
        relevantLayers = py.animLayer(affectedLayers=1,q=1);
        if(isinstance(relevantLayers,list) == 1):
            i=0;
            while(i < len(relevantLayers)):
                py.animLayer(relevantLayers[i],solo=0,mute=1,e=1);
                py.setAttr(relevantLayers[i]+".override",0);
                i+=1;
        #py.animLayer(conLayer,aso=1,e=1);
        #SET OUTPUT RIG TO T POSE (AGAIN)
        for i in range(0, len(inputControllers)):
            outputController = outputNameSpace+":"+inputControllers[i].split(":")[-1];
            if(py.objExists(outputController) == 1):
                keyableAttributes = py.listAttr(outputController,u=1,k=1,v=1);
                if(isinstance(keyableAttributes,list) == 1):
                    for ii in range(0, len(keyableAttributes)):
                        if("translate" in keyableAttributes[ii] or "rotate" in keyableAttributes[ii]):
                            py.setAttr(outputController+"."+keyableAttributes[ii],0);
                            py.animLayer(conLayer,at=outputController+"."+keyableAttributes[ii],e=1);
        #BEGIN TRANSFER...
        ikControllerList = [];
        for i in range(0, len(inputControllers)):
            #CHANGE OUTPUT CONTROLLER TARGET BASED ON THE IK/FK STATUS
            typeName = inputControllers[i].split("_")[-3];
            if(typeName in armElements):
                inputOptionsBox = inputControllers[i].replace(typeName,"armOptionsBox",-1);
            elif(typeName in legElements):
                inputOptionsBox = inputControllers[i].replace(typeName,"legOptionsBox",-1);
            else:
                inputOptionsBox = "invalid";
            if(inputOptionsBox != "invalid"):
                inputMode = 0 if(typeName not in ikElements) else 1;
                outputOptionsBox = outputNameSpace+":"+inputOptionsBox.split(":")[-1];
                outputMode = int(py.getAttr(outputOptionsBox+".MODE"));
                if(inputMode != outputMode):
                    if(inputMode == 0):
                        #PAIR INPUT FK CONTROLLER TO OUTPUT IK JNT
                        outputController = outputNameSpace+":"+inputControllers[i].split(":")[-1];
                        outputController = outputController.replace("CTRL","JNT",-1);
                        if(typeName == armElements[-1]):
                            outputController = outputController.replace(typeName,"armInitialPositionFK",-1);
                            outputController = outputController.replace("JNT","LOC",-1);
                        if(typeName == legElements[-2]):
                            outputController = outputController.replace(typeName,"legInitialPositionFK",-1);
                            outputController = outputController.replace("JNT","LOC",-1);
                    else:
                        #PAIR INPUT IK CONTROLLER TO OUTPUT FK LOCATORS
                        outputController = outputNameSpace+":"+inputControllers[i].split(":")[-1];
                        if(typeName == "arm"):
                            outputController = outputController.replace(typeName,"wristIK",-1);
                            outputController = outputController.replace("CTRL","LOC",-1);
                        elif(typeName == "leg"):
                            outputController = outputController.replace(typeName,"ankleIK",-1);
                            outputController = outputController.replace("CTRL","LOC",-1);
                        elif(typeName == "armPV" or typeName == "legPV"):
                            outputController = outputController.replace("CTRL","LOC",-1);
                        elif(typeName == "toe"):
                            outputController = outputController.replace(typeName,"ball",-1);
                else:
                    #PAIR INPUT CONTROLLER TO OUTPUT CONTROLLER 1-To-1
                    outputController = outputNameSpace+":"+inputControllers[i].split(":")[-1];
            else:
                #PAIR INPUT CONTROLLER TO OUTPUT CONTROLLER 1-To-1
                outputController = outputNameSpace+":"+inputControllers[i].split(":")[-1];
            isWeapon = py.listAttr(inputControllers[i],st=["WiGGiE"],r=1);
            if(isinstance(isWeapon,list) == 0):
                if("_arm_" in inputControllers[i] or "_leg_" in inputControllers[i]):
                    ikControllerList.append(inputControllers[i]);
                    parents = py.listRelatives(inputControllers[i],p=1,s=0)[0];
                    SAFE = py.listAttr(parents, st=["SAFE"], r=1);
                    if(isinstance(SAFE, list) == 1):
                        py.setAttr(parents+".SAFE",1);
                if(py.objExists(outputController) == 1):
                    try:
                        #py.parentConstraint(outputController,inputControllers[i],l=conLayer,mo=1,w=1);
                        py.pointConstraint(outputController,inputControllers[i],mo=0,w=1);
                        py.orientConstraint(outputController,inputControllers[i],l=conLayer,mo=0,w=1);
                    except:
                        try:
                            py.orientConstraint(outputController,inputControllers[i],l=conLayer,mo=0,w=1);
                        except:
                            try:
                                py.pointConstraint(outputController,inputControllers[i],l=conLayer,mo=1,w=1);
                            except:
                                #FOR CONTROLLERS WHERE 3 AXIS AREN'T AVAILABLE (IE: BREATH)
                                pass;
###############################################################################
#"""# CONNECT WEAPON TO ATTACHMENT POINT                                      #
###############################################################################
    weaponID = ["00","01","02","03","04","05","06","07","08","09","10"];
    weapons = ["none","sword","R_blade","R_hammer","spear","longBow","wand",
               "heavySword","L_sword.R_sword","harp","shield.R_blade"];
    secondaryWeapons = ["shield"];
    py.currentTime((py.currentTime(q=1)+1));#STEP ANIMATION FORWARD 1 FRAME
    i=0;
    while(i < len(weaponID)):
        if(weaponID[i] in referenceFile.split("_")[-1] and "_" in referenceFile):#!
            weaponsSet = weapons[i].split(".");
            ii=0;
            while(ii < len(weaponsSet)):
                position = "primary";
                if any(s in weaponsSet[ii] for s in secondaryWeapons):
                    position = "secondary";
                if(weaponsSet[ii] != "none"):
                    properWeaponController = 0;
                    weaponController = [s for s in inputControllers if weaponsSet[ii]+"_" in s];
                    if(weaponController != []):
                        #CHECK MAX WEAPON BEFORE MAYA
                        weaponController = weaponController[0];
                        side = "_R_" if("_R_" in weaponController) else "_L_";
                        weaponPosition = position+"Weapon";
                        name = side+position+"Weapon";
                        weaponPosition = [s for s in outputJoints if name in s];
                        if(len(weaponPosition) == 0):
                            #SECOND MAX WEAPON CHECK
                            name = "RightWeapon" if(side == "_R_") else "LeftWeapon";
                            weaponPosition = [s for s in outputJoints if name in s];
                            properWeaponController = 0;
                        if(len(weaponPosition) == 0):
                            #FIND OLD RIG WEAPON
                            name = side+"weapon";
                            weaponPosition = [s for s in outputJoints if name in s];
                            properWeaponController = 0;
                        if(len(weaponPosition) == 0):
                            #FIND NEW RIG WEAPON
                            name = side+weaponsSet[ii]+"_";
                            weaponPosition = [s for s in outputJoints if name in s];
                            properWeaponController = 1;
                        #HOLSTER ATTACHMENT
                        holster = 1;
                        if(side == "_L_" and position == "primary"):
                            holster = 2;
                        elif(side == "_L_" and position == "secondary"):
                            holster = 3;
                        try:
                            py.setAttr(weaponController+".ATTACHMENT",holster);
                            target = masterController+"."+weaponsSet[ii].upper();
                            py.setAttr(target,1);
                        except:
                            pass;
                        if(len(weaponPosition) != 0):
                            controllerAP = weaponPosition[0].replace("t_","c_").replace("JNT","CTRL");
                            if(py.objExists(outputNameSpace+":"+controllerAP) == 1):
                                weaponPosition = outputNameSpace+":"+controllerAP;
                            else:
                                weaponPosition = weaponPosition[0];
                            if(holster == 1 or holster == 2):
                                weaponJoint = weaponPosition.split(":")[-1].replace("c_","t_").replace("CTRL","JNT");
                                weaponJoint = outputNameSpace+":"+weaponJoint;
                                if(properWeaponController == 0):                                 
                                    py.orientConstraint(weaponPosition,weaponController,l=conLayer,mo=0,w=1);
                                elif(py.objExists(weaponJoint) == 1):
                                    py.parentConstraint(weaponJoint,weaponController,l=conLayer,mo=0,w=1);
                ii+=1;
        i+=1;
###############################################################################
#"""# BAKE ANIMATION FROM CONSTRAINT LAYER TO ANIMATION LAYER                 #
###############################################################################
    if(masterController in inputControllers and RiGGiE == 0):
        inputControllers.remove(masterController);
    py.select(inputControllers[:],r=1); 
    py.animLayer(conLayer,solo=1,mute=0,e=1);
    py.setAttr(conLayer+".override",1);
    version=1;
    while(py.objExists("a_M_importedAnimation_v"+str(version)+"_LYR")):
        version+=1;
    bakeLayer = py.animLayer("a_M_importedAnimation_v"+str(version)+"_LYR");
    py.setAttr(bakeLayer+".rotationAccumulationMode", 1);
    py.setAttr(bakeLayer+".scaleAccumulationMode", 0);
    py.animLayer(bakeLayer,solo=1,e=1);#!
    py.bakeResults(t=(firstFrame,lastFrame),dl=bakeLayer,at=keyableValues,sm=1,s=0);
    py.animLayer(conLayer,solo=0,mute=0,e=1);
    py.delete(out[-1],conLayer);
    py.animLayer(bakeLayer,solo=0,e=1);
    if(py.about(b=1,q=1) == 0):
        py.lookThru(initialCamera);
        py.delete(characterCameraGroup);
    py.autoKeyframe(state=autoKeyState);
    py.select(masterController,r=1);
    py.setAttr(bakeLayer+".rotationAccumulationMode", 0);
    py.setAttr(bakeLayer+".scaleAccumulationMode", 1);
    #SET IKFK MODE FROM OPTIONS BOX LIST
    i=0;
    while(i < len(out[1])):
        if py.objExists(out[1][i]) == False:
            print "the object doesnt exist"
        else:
            if(("leg" in out[1][i] and line['LEG IK'] == 1) or ("arm" in out[1][i] and line['ARM IK'] == 1)):
                py.setAttr(out[1][i]+".MODE",1);
        i+=1;   
    #FINALIZE
    if(py.about(b=1,q=1) == 0):
        py.FrameSelected();
    i=0;
    while(i < len(out[0])):
        parents = py.listRelatives(out[0][i],p=1,s=0)[0];
        SAFE = py.listAttr(parents, st=["SAFE"], r=1);
        if(isinstance(SAFE, list) == 1):
            py.setAttr(parents+".SAFE",0);
        i+=1;
    py.headsUpMessage('"Animation successfully converted!" - HiGGiE', t=2);
    py.file(outputReference, rr=1);
    py.select(masterController,r=1);