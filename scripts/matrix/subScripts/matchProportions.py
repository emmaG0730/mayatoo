###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import maya.OpenMaya as om

import maya.cmds as py
import maya.mel as mel
from copy import deepcopy
import math
###############################################################################
#.............................................................................#
#.............................................................................#
#"""# LIST AND NAME SEGMENTS OF OUTPUT RIG'S SKELETON                         #
#.............................................................................#
#.............................................................................#
###############################################################################
def MATCHPROPORTIONS(transformList,nameSpace,outputNameSpace,conLayer):
    selectedElement = py.ls(sl=1)[0]; 
    keyedJointName = selectedElement.split(":")[-1][:-1] if(":" in selectedElement) else selectedElement;
    selectedRoot = py.ls(selectedElement,l=1)[0].split("|")[1];
    newOutputJoints = py.duplicate(selectedRoot,ic=1,rc=1);
    override = False;
    RiGGiE = False;
    outputChildNodes = py.listRelatives(selectedRoot,c=1,s=0);
    characterGroup = [s for s in outputChildNodes if "c_M_character_v1_GRP" in s];
    if(len(characterGroup) > 0):
        outputNameSpace = characterGroup[0].replace("c_M_character_v1_GRP","");
        outputMasterController = outputNameSpace+"c_M_master_v1_CTRL";
        if(py.objExists(outputMasterController) == 1):
            isRiGGiE = py.listAttr(outputMasterController,st=["RiGGiE"],r=1);
            if(isinstance(isRiGGiE,list) == 1):
                #OUTPUT RIG IS CREATED BY HiGGiE; DIRECT TRANSFER IS ALLOWED
                RiGGiE = True;
    if(":" in selectedElement):
        name = selectedElement.split(":")[-1];
    else:
        name = selectedElement;   
    selectedElement = [s for s in newOutputJoints if name in s][0];
###############################################################################
#"""# UNGROUP FIRST NON JOINT TRANSFORM PARENT                                #
###############################################################################
    root = py.ls(newOutputJoints[0],l=1)[0].split("|")[1];
    potentialRoot = py.ls(selectedElement,l=1)[0].split("|")[1:-1];
    rootJoint = "";
    i=0;
    while(i < len(potentialRoot)):
        type = py.nodeType(potentialRoot[i]);
        if(type == "joint"):
            rootJoint = potentialRoot[i];    
            break;        
        i+=1;
    rootJoint = selectedElement if (rootJoint == "") else rootJoint;
    potentialRoot.reverse();
    i=0;
    while(i < len(potentialRoot)):
        if("outputFileRN" not in potentialRoot[i]):
            type = py.nodeType(potentialRoot[i]);
            if(type != "joint"):
                py.parent(potentialRoot[i],w=1);    
                py.delete(root);
                root = potentialRoot[i];
                break;
        elif("outputFileRN" in potentialRoot[i] or i == len(potentialRoot)-1):
            py.parent(rootJoint,w=1);    
            py.delete(root);
            root = rootJoint;
        i+=1;
###############################################################################
#"""# PREPARE OUTPUT RIG FOR TRANSFER                                         #
###############################################################################
    log = "";
    pelvisNames = ["PELVIS","Pelvis","pelvis","HIPS","Hips","hips","cog"];
    upperSpineNames = ["spine","lumbar","thorax","Spn","spn"];
    twistNames = ["twist","roll","twst","rol"];
    footStepNames = ["footStep","footstep"];
    miscNames = ["sword","blade","shield","_bow","spear","quiver","hammer",
                 "weapon","pad","tail"];
    trajectoryNames = ["Trajectory","trajectory","TRAJ","Traj","traj"];
    spineNames = pelvisNames+upperSpineNames;
    hierarchy = py.listRelatives(rootJoint,ad=1,pa=1,s=0);
    hierarchy.insert(0,rootJoint);
###############################################################################
#"""# INPUT TRANSFORM VALUES TO OUTPUT JOINTS                                 #
############################################################################### 
    outputJoints = py.listRelatives(root,type="joint",ad=1,pa=1,s=0);
    outputJoints.reverse();
    outputJoints.insert(0,root);
    spineSegments = [s for s in outputJoints if "b_M_spine" in s];
    if(transformList == "invalid"):
        i=0;
        while(i < len(spineSegments)):
            py.setAttr(spineSegments[i]+".ty",0);py.setAttr(spineSegments[i]+".tz",0);
            i+=1;
    else:
        i=0;
        while(i < len(outputJoints) and i < len(transformList)):
            py.setAttr(outputJoints[i]+".t",transformList[i][0],transformList[i][1],transformList[i][2]);
            i+=1;
###############################################################################
#"""# REMOVE CONSTRAINTS, LOCATORS, AND TWIST JOINTS FROM OUTPUT RIG          #
###############################################################################
    expendableNodes = [];
    i=0;
    while(i < len(hierarchy)):
        #IF HIERACHY SUGGESTS A TWIST LEAF JOINT
        children = py.listRelatives(hierarchy[i],type="joint",c=1,s=0);
        if(isinstance(children,list) == 0):
            parents = py.listRelatives(hierarchy[i],type="joint",p=1,s=0);
            if(isinstance(parents,list) == 1):
                children = py.listRelatives(parents,type="joint",c=1,s=0);
                if(isinstance(children,list) == 1):
                    if(len(children) > 1 and hierarchy[i] in children):
                        ii=0;
                        while(ii < len(children)):
                            greatGrandChildren = py.listRelatives(children[ii],type="joint",c=1,s=0);
                            if(isinstance(greatGrandChildren,list) == 1):
                                children.remove(children[ii]);
                            elif any(x in children[ii] for x in expendableNodes):
                                children.remove(children[ii]);
                            ii+=1;
                        if(len(children) > 0):
                            if not any(x in hierarchy[i].lower() for x in spineNames):
                                if not any(x in hierarchy[i].lower() for x in trajectoryNames):
                                    expendableNodes.append(hierarchy[i]);
        #IF LABELED AN EXPENDABLE TWIST NAME FROM LIST THEN DELETE
        if any(x in hierarchy[i].lower() for x in twistNames):
            children = py.listRelatives(hierarchy[i],type="joint",c=1,s=0);
            if(isinstance(children,list) == 1):
                parents = py.listRelatives(hierarchy[i],type="joint",p=1,s=0);
                if(isinstance(parents,list) == 1):
                    grandChildren = py.listRelatives(children[0],type="joint",c=1,s=0);
                    if(isinstance(grandChildren,list) == 1):
                        py.parent(children[0],parents[0]);
            expendableNodes.append(hierarchy[i]);
        #IF LABELED AN EXPENDABLE MISC NAME FROM LIST THEN DELETE
        if any(x in hierarchy[i].lower() for x in miscNames):
            expendableNodes.append(hierarchy[i]);
        if any(x in hierarchy[i].lower() for x in footStepNames):
            expendableNodes.append(hierarchy[i]);
        #RENAME IF JOINT; DELETE IF CONSTRAINT
        type = py.nodeType(hierarchy[i]);
        if("Constraint" not in type):
            if not any(x in hierarchy[i] for x in expendableNodes):
                if(type == "joint"):
                    py.setAttr(hierarchy[i]+".r",0,0,0);
        else:
            expendableNodes.append(hierarchy[i]);
        i+=1;
    #REMOVE EXPENDABLE ASSETS (IE: CONSTRAINTS AND TWIST JOINTS)
    expendableNodes = list(set(expendableNodes)); 
    i=0;
    while(i < len(expendableNodes)):
        hierarchy.remove(expendableNodes[i]);
        if(py.objExists(expendableNodes[i]) == 1):
            py.delete(expendableNodes[i]);
        i+=1;
###############################################################################
#"""# LOCATE THE ROOT, TRAJECTORY, AND PELVIS JOINTS IF THEY EXIST            #
###############################################################################
    side = "M";
    version = 1;
    axis = ["x","y","z"];
    axisArray = ["0:3","4:7","8:11"];
    master = "t_"+side+"_master_v"+str(version)+"_GRP";
    origin = "t_"+side+"_origin_v"+str(version)+"_CTRL";
    pelvis = "t_"+side+"_spineMaster_v"+str(version)+"_CTRL";
    trajectory = "t_"+side+"_trajectory_v"+str(version)+"_CTRL";
    outputRoot = "none";
    outputLimbs = "none";
    outputOrigin = "none";
    outputPelvis = "none"; 
    outputLumbar = "none";
    outputThorax = "none";
    replacementRoot = "none";
    outputTrajectory = [];
    leftNames = ["left","lft","_l_"];
    rightNames = ["right","rgt","rht","_r_"];
    midNames = ["elbow","elbo","knee","kne","nee"];
    endNames = ["wrist","rist","wrst","wst","ball","bal"];
    overlap = 0;
    outputRig = [];outputSpine = [];outputCranium = [];
    outputLeftArm = [];outputRightArm = [];outputLeftLeg = [];outputRightLeg = [];
    itemList = py.listRelatives(root,type="joint",ad=1,pa=1,s=0);
    parents = py.ls(itemList[0],l=1)[0].split("|")[2:];
    shapeList = py.listRelatives(root,s=1);
    if(isinstance(shapeList,list) == 1):
        shape = shapeList[0];
    else:
        shape = root;
    type = py.nodeType(shape);
    if(type != "joint"):
        i=0;
        while(i < len(parents) and replacementRoot == "none"):
            shapeList = py.listRelatives(parents[i],s=1);
            if(isinstance(shapeList,list) == 1):
                shape = shapeList[0];
            else:
                shape = parents[i];
            type = py.nodeType(shape);
            if(type == "joint"):
                replacementRoot = parents[i];
            i+=1;  
    outputJoints = py.listRelatives(root,type="joint",ad=1,pa=1,s=0);
    outputJoints.reverse();
    outputJoints.insert(0,root);
###############################################################################
#"""# LOCATE THE ORIGIN JOINT IF IT EXISTS AND THE ROOT JOINT                 #
###############################################################################
    position = py.xform(root,q=1,t=1,ws=1);
    i=0;
    while(i < len(position)):
        position[i] = round(position[i],0);
        i+=1;
    if(position == [0.0, 0.0, 0.0]):
        outputRoot = root;
        outputOrigin = outputRoot;
        #FIND PELVIS FROM ROOT'S IMMEDIATE CHILDREN
        children = py.listRelatives(outputRoot,type="joint",c=1,s=0);
        if(isinstance(children,list) == 1):
            heighestChildrenCount = 0;
            i=0;
            while(i < len(children)):
                grandChildren = py.listRelatives(children[i],type="joint",ad=1,c=1,s=0);
                if(isinstance(grandChildren,list) == 1):
                    childrenCount = len(grandChildren);
                else:
                    childrenCount = 0;
                if(childrenCount > heighestChildrenCount):
                    heighestChildrenCount = childrenCount;
                    outputPelvis = children[i];
                i+=1;
            if(outputPelvis == "none"):#IF NO JOINTS WITH MORE CHILDREN THAN ANOTHER, PICK FIRST JOINT
                outputPelvis = children[0];
        else:
            print "rig is broken"#ROOT JOINT WITH NO JOINT CHILDREN#!
    else:
        outputRoot = root;
        if(replacementRoot == "none"):
            outputPelvis = outputRoot;
        else:
            outputPelvis = replacementRoot;
    outputJoints = py.listRelatives(outputRoot,type="joint",ad=1,pa=1,s=0);
    outputJoints.reverse();
    outputJoints.insert(0,outputRoot);
###############################################################################
#"""# SPECIAL CASE: ZERO OUT FRONT/SIDE TRANSLATIONS ON MAX RIG SPINE JOINTS  #
###############################################################################
    characterStudioSpineJoints = ["001_Pelvis","001_Spine","001_Spine1","001_Spine2"];
    i=0;
    while(i < len(characterStudioSpineJoints)):
        #LOWER CASE "BIP" NAME SCENARIO
        if(py.objExists("bip"+characterStudioSpineJoints[i]) == 1 and i == 0):
            outputPelvis = "bip"+characterStudioSpineJoints[i];
        if(py.objExists("bip"+characterStudioSpineJoints[i]) == 1 and i > 0):    
            py.setAttr("bip"+characterStudioSpineJoints[i]+".ty",0);
            py.setAttr("bip"+characterStudioSpineJoints[i]+".tz",0);
        #UPPER CASE "BIP" NAME SCENARIO
        if(py.objExists("Bip"+characterStudioSpineJoints[i]) == 1 and i == 0):
            outputPelvis = "Bip"+characterStudioSpineJoints[i];
        if(py.objExists("Bip"+characterStudioSpineJoints[i]) == 1 and i > 0):    
            py.setAttr("Bip"+characterStudioSpineJoints[i]+".ty",0);
            py.setAttr("Bip"+characterStudioSpineJoints[i]+".tz",0);
        i+=1;
###############################################################################
#"""# SPECIAL CASE: MOVE SHOGUN CLAVICLE POSITIONS FROM CENTER                #
###############################################################################
    if(py.objExists("LeftShoulder") == 1 and py.objExists("RightShoulder") == 1):
        leftClavicleSpace = py.xform("LeftShoulder",q=1,t=1,ws=1);
        rightClavicleSpace = py.xform("RightShoulder",q=1,t=1,ws=1);
        if(leftClavicleSpace == rightClavicleSpace):
            py.setAttr("LeftShoulder.tx",1);
            py.setAttr("RightShoulder.tx",-1);
            outputRig = [["Hips","Spine","Spine2","Spine3"],["Neck","Head"],
                        [["LeftShoulder","LeftArm","LeftForeArm","LeftHand"]], 
                        [["RightShoulder","RightArm","RightForeArm","RightHand"]], 
                        [["LeftUpLeg","LeftLeg","LeftFoot","LeftToeBase","LeftToeBaseEnd"]], 
                        [["RightUpLeg","RightLeg","RightFoot","RightToeBase","RightToeBaseEnd"]], 
                        [[]], [[]], [[]], [[]]];
            aimAxisList = [["y+","y+","y+","y+"],["y+","y+"],
                        [["y+","y+","y+","y+"]], 
                        [["y+","y+","y+","y+"]], 
                        [["y-","y-","z+","z+","z+"]], 
                        [["y-","y-","z+","z+","z+"]], 
                        [[]], [[]], [[]], [[]]];
            upAxisList = [["z+","z+","z+","z+"],["x+","x+"],
                        [["z+","z+","z+","z+"]], 
                        [["z+","z+","z+","z+"]], 
                        [["z+","z+","x+","x+","x+"]], 
                        [["z+","z+","x+","x+","x+"]], 
                        [[]], [[]], [[]], [[]]];
            outputRigOverrideList = [];aimAxisOverrideList = [];upAxisOverrideList = [];
            i=0;
            while(i < len(outputRig)):
                if(isinstance(outputRig[i][0],list) == 0):
                    outputRigOverrideList = outputRigOverrideList+outputRig[i];
                    aimAxisOverrideList = aimAxisOverrideList+aimAxisList[i];
                    upAxisOverrideList = upAxisOverrideList+upAxisList[i];
                else:
                    outputRigOverrideList = outputRigOverrideList+outputRig[i][0];
                    aimAxisOverrideList = aimAxisOverrideList+aimAxisList[i][0];
                    upAxisOverrideList = upAxisOverrideList+upAxisList[i][0];
                i+=1;
            i=0;
            while(i < len(outputRigOverrideList)):
                py.addAttr(outputRigOverrideList[i],ln="aimAxis",at="enum",en=aimAxisOverrideList[i]);
                py.setAttr(outputRigOverrideList[i]+".aimAxis", k=0, cb=1, e=1);  
                py.addAttr(outputRigOverrideList[i],ln="upAxis",at="enum",en=upAxisOverrideList[i]);
                py.setAttr(outputRigOverrideList[i]+".upAxis", k=0, cb=1, e=1);  
                i+=1;
                
            limbs = [outputRig[2][0][0],outputRig[3][0][0],outputRig[4][0][0],outputRig[5][0][0]];
            outputLimbs = [outputRig[2][0],outputRig[3][0],outputRig[4][0],outputRig[5][0]];
            limbSegments = [outputRig[2][0][0],outputRig[3][0][0],outputRig[4][0][0],outputRig[5][0][0]];
            armSegments = [outputRig[2][0][0],outputRig[3][0][0]];
                
            socketJoints = ["Spine3","Hips"];
            middleJoints = ["Hips","Spine","Spine2","Spine3","Neck","Head"];
            override = True;
###############################################################################
#"""# DETERMINE IF ROOT AND PELVIS HAVE OVERLAPPING CHILDREN JOINTS           #
###############################################################################
    originChildren = py.listRelatives(outputPelvis,type="joint",c=1,s=0);
    position = py.xform(outputPelvis,q=1,t=1,ws=1);
    i=0;
    while(i < len(position)):
        position[i] = round(position[i],1);
        i+=1;
    i=0;
    if(isinstance(originChildren,list) == 0):
        originChildren = [];
    while(i < len(originChildren)):
        childPosition = py.xform(originChildren[i],q=1,t=1,ws=1);
        ii=0;
        while(ii < len(childPosition)):
            childPosition[ii] = round(childPosition[ii],1);
            ii+=1;
        if(childPosition == position):
            outputOrigin = root;
            outputRoot = outputPelvis;
            outputPelvis = originChildren[i];
        i+=1;
###############################################################################
#"""# LOCATE THE TRAJECTORY JOINT IF IT EXISTS                                #
###############################################################################
    if(outputPelvis == "none"):
        outputPelvis = outputRoot;
    if(outputOrigin != "none"):
        childrenOfChildren = [];
        originChildren = py.listRelatives(outputOrigin,type="joint",c=1,s=0);
        i=0;
        while(i < len(originChildren)):
            grandChildren = py.listRelatives(originChildren[i],type="joint",ad=1,pa=1,s=0);
            if(isinstance(grandChildren,list) == 0):
                grandChildren = [];
            childrenOfChildren.append(len(grandChildren));
            i+=1;
        lowestChildrenCount = min(childrenOfChildren);
        index = childrenOfChildren.index(lowestChildrenCount);
        outputTrajectory = [originChildren[index]];
        if(replacementRoot != "none"):
            outputJoints.remove(replacementRoot);
            outputJoints[0] = outputRoot;
        outputNodes = py.listRelatives(outputRoot,ad=1,pa=1,s=0);
        outputJoints = py.listRelatives(outputRoot,type="joint",ad=1,pa=1,s=0);
        expendableNodes = list(set(outputNodes)-set(outputJoints));
        if(len(expendableNodes) > 0):
            py.delete(expendableNodes[:]);
        outputJoints.reverse();
        outputJoints.insert(0,outputRoot);
        #FIND PELVIS AND TRAJECTORY BY NAME
        trajectory = [i for e in trajectoryNames for i in outputJoints if e in i];
        if(trajectory != []):
            outputTrajectory = [trajectory[0]];
        pelvis = [i for e in pelvisNames for i in outputJoints if e in i];
        if(pelvis != []):
            outputPelvis = pelvis[0];
        if(outputTrajectory != []):
            if(outputTrajectory[0] == outputPelvis or outputTrajectory[0] == outputRoot or outputTrajectory[0] == outputOrigin):
                outputTrajectory = [];
###############################################################################
#"""# LIST ALL MIRRORED JOINTS                                                #
###############################################################################
    if(outputPelvis != "none"):
        firstPickMirrorJoints = "";
        i=0;
        while(i < 2):#EQUALS AMOUNT OF "GET TRANSLATION" METHODS
            parents = "";
            mirrorJoints = [];
            mirroredValues = [];
            translationValues = [];
            translationValuesPair = [];
            potentialMirroredJoints = [];
            py.move(0,0,0,outputPelvis,rpr=1);
            children = py.listRelatives(outputPelvis,type="joint",c=1,s=0);
            py.select(outputPelvis,hi=1,r=1);
            outputAnimJoints = py.ls(sl=1,type="joint")[1:];
            py.select(d=1);   
            #REMOVE CHILDREN FROM OUPUT ANIM JOINTS
            if(isinstance(children,list) == 1):
                ii=0;
                while(ii < len(children)):
                    if(children[ii] in outputAnimJoints):
                        outputAnimJoints.remove(children[ii]);
                    ii+=1;
                outputAnimJoints = children+outputAnimJoints[:];
            #LIST TRANSLATION VALUES OF EACH JOINT
            ii=0;
            while(ii < len(outputAnimJoints)):
                translationsAdjusted = "";
                translationsAdjustedPair = "";
                if(i == 0):#TWO DIFFERENT METHODS FOR FINDING THE MIRROR JOINTS
                    translations = list(py.getAttr(outputAnimJoints[ii]+".t")[0]);
                elif(i == 1):
                    translations = py.xform(outputAnimJoints[ii],q=1,t=1,ws=1);
                iii=0;
                while(iii < len(translations)):
                    translationsAdjusted = translationsAdjusted+str(abs(round(translations[iii],1))).split(".")[0]+".";
                    if("0." not in (str(round(translations[iii],1)).split(".")[0]+".")):
                        translationsAdjustedPair = translationsAdjustedPair+str(round(translations[iii],1)).split(".")[0]+".";
                    else:
                        translationsAdjustedPair = translationsAdjustedPair+"0.";
                    iii+=1;
                translationValues.append(translationsAdjusted);
                translationValuesPair.append(translationsAdjustedPair);
                potentialMirroredJoints.append(outputAnimJoints[ii]);
                ii+=1;
            #LIST DUPLICATE VALUES IN LIST TO FIND MIRRORED JOINTS
            duplicateTranslationValues = translationValues[:];
            ii=0;
            while(ii < len(translationValues)):
                if(translationValues[ii] in duplicateTranslationValues):
                    index = duplicateTranslationValues.index(translationValues[ii]);
                    firstJoint = potentialMirroredJoints[index];
                    firstValue = translationValuesPair[index];
                    translationValuesPair.remove(firstValue);
                    duplicateTranslationValues.remove(translationValues[ii]);
                    potentialMirroredJoints.remove(potentialMirroredJoints[index]);
                    if(translationValues[ii] in duplicateTranslationValues):
                        index = duplicateTranslationValues.index(translationValues[ii]);
                        secondJoint = potentialMirroredJoints[index];
                        secondValue = translationValuesPair[index];
                        translationValuesPair.remove(secondValue);
                        duplicateTranslationValues.remove(translationValues[ii]);
                        potentialMirroredJoints.remove(potentialMirroredJoints[index]);
                        if(firstValue != secondValue):#IMPLIES MIRRORING    
                            mirroredValues.append(translationValues[ii]);
                            mirrorJoints.append(firstJoint);
                            mirrorJoints.append(secondJoint);
                ii+=1;
            #COLLECT LIST OF CHILDREN PAIRS
            expendableJoints = [];
            ii=0;
            while(ii < len(mirrorJoints)):
                children = py.listRelatives(mirrorJoints[ii],type="joint",ad=1,c=1,s=0);
                if(isinstance(children,list) == 1):
                    iii=0;
                    while(iii < len(children)):
                        if(children[iii] in mirrorJoints and children[iii] not in expendableJoints):
                            expendableJoints.append(children[iii]);
                        iii+=1;
                ii+=1;
            #REMOVE CHILDREN PAIRS
            ii=0;
            while(ii < len(expendableJoints)):
                mirrorJoints.remove(expendableJoints[ii]);
                ii+=1;
            #PICK BETWEEN MIRROR JOINT RESULTS
            if(firstPickMirrorJoints == ""):
                firstPickMirrorJoints = mirrorJoints;
            else:
                if(mirrorJoints != firstPickMirrorJoints):
                    firstPickMirrorJointsTemp = list(set(firstPickMirrorJoints));
                    mirrorJointsTemp = list(set(mirrorJoints));
                    if(len(firstPickMirrorJointsTemp)%2 == 0 and len(mirrorJointsTemp)%2 == 1):
                        #IF FIRST PICKS ARE EVEN AND SECOND IS ODD
                        mirrorJoints = firstPickMirrorJoints;
                    elif(len(firstPickMirrorJointsTemp)%2 == 0 and len(mirrorJointsTemp)%2 == 0):
                        #IF BOTH FIRST AND SECOND PICKS ARE EVEN
                        mirrorJoints = firstPickMirrorJoints;
            i+=1;
###############################################################################
#"""# LIST ALL SOCKET JOINTS IF THEY EXISTS AND DETERMINE POSTURE             #
###############################################################################
    if(mirrorJoints != [] and override == 0):
        posture = "biped/quadruped";
        socketJoints = [];
        i=0;
        while(i < len(mirrorJoints)):
            parents = py.listRelatives(mirrorJoints[i],type="joint",p=1,s=0);
            if(isinstance(parents,list) == 1):
                socketJoints.append(parents[0]);
            i+=1;
        socketJoints = list(set(socketJoints));
    else:
        posture = "serpant";
###############################################################################
#"""# FIND THE AIM AXIS OF THE PELVIS JOINT                                   #
###############################################################################
    if(outputPelvis != "none" and override == 0):
        outputLumbar = py.listRelatives(outputPelvis,type="joint",c=1,s=0);#!MIGHT NEED A BETTER WAY TO FIND THIS JOINT
        if(isinstance(outputLumbar,list) == 1):
            outputLumbar = outputLumbar[0];
            positionAbsolute = [];
            position = list(py.getAttr(outputLumbar+".t")[0]);#!
            i=0;
            while(i < len(position)):
                positionAbsolute.append(abs(position[i]));
                i+=1;
            aimAxisValue = max(positionAbsolute);
            if(aimAxisValue in position):
                aimAxisIndex = position.index(aimAxisValue);
                sign = "+";
            else:
                aimAxisIndex = position.index(aimAxisValue*-1);
                sign = "-";
            aimAxis = axis[aimAxisIndex]+sign;
            attributeExists = py.listAttr(outputPelvis,st=["position"],r=1);
            if(isinstance(attributeExists, list) == 0):
                py.addAttr(outputPelvis,ln="position",at="enum",en="M");
                py.setAttr(outputPelvis+".position", k=0, cb=1, e=1);
            attributeExists = py.listAttr(outputPelvis,st=["aimAxis"],r=1);
            if(isinstance(attributeExists, list) == 0):
                py.addAttr(outputPelvis,ln="aimAxis",at="enum",en=aimAxis);
                py.setAttr(outputPelvis+".aimAxis", k=0, cb=1, e=1);
            aimArray = [];
            i=0;
            while(i < len(axis)):
                if(i == aimAxisIndex):
                    aimArray.append(int(aimAxis[-1]+str(1)));
                else:
                    aimArray.append(0);
                i+=1;
            remainingAxis = axis[:];
            remainingAxis.remove(axis[aimAxisIndex]);
            sideAxisIndex = axis.index(remainingAxis[0]);
            sideArray = [];
            i=0;
            while(i < len(axis)):
                if(i == sideAxisIndex):
                    sideArray.append(1);
                else:
                    sideArray.append(0);
                i+=1;
            centerAlignment = py.spaceLocator(p=(0,0,0))[0];
            py.setAttr(centerAlignment+".ty",10);
            sideTracker = py.spaceLocator(p=(0,0,0))[0];
            py.setAttr(sideTracker+".tx",10);
            base = py.spaceLocator(p=(0,0,0))[0];
            py.parent(base,outputPelvis);
            py.setAttr(base+".t",0,0,0);py.setAttr(base+".r",0,0,0);
            snap = py.aimConstraint(centerAlignment,base,aim=aimArray,u=sideArray,wut="objectrotation",wuo=sideTracker,wu=[1,0,0],mo=0,w=1);
            py.delete(snap);       
            rotations = list(py.getAttr(base+".r")[0]);
            py.setAttr(outputPelvis+".r",rotations[0],rotations[1],rotations[2]);
###############################################################################
#"""# FIND THE FIRST LEFT JOINT (AGAIN) BASED ON NAMING AND REWRITE IF FOUND  #
###############################################################################
    if(len(mirrorJoints) > 0 and override == 0):  
        leftJoint = mirrorJoints[0];
        i=0;
        while(i < len(mirrorJoints)):
            if any(x in mirrorJoints[i].lower() for x in leftNames):
                if(leftJoint != "none" and leftJoint != mirrorJoints[i]):
                    log = log+"Discrepancy: '"+leftJoint+"' was selected as the left joint, but '"+mirrorJoints[i]+"' was picked by the rigger.\n";
                leftJoint = mirrorJoints[i];
                i = len(mirrorJoints);
                break;
            i+=1;
        duplicateMirrorJoints = mirrorJoints[:];
        duplicateMirrorJoints.remove(leftJoint);
        rightJoint = duplicateMirrorJoints[0];
    else:
        leftJoint = "none";  
###############################################################################
#"""# FIND THE SIDE AXIS OF THE PELVIS                                        #
###############################################################################
    if(len(mirrorJoints) > 0 and leftJoint != "none" and override == 0):
        remainingAxis = axis[:];
        remainingAxis.remove(axis[aimAxisIndex]);
        distanceNodeShape = py.distanceDimension(sp=(0, 100, 0), ep=(0, 50, 0));
        distanceLocators = py.listConnections(distanceNodeShape);
        distanceNode = py.listRelatives(distanceNodeShape, p=1);
        snap1 = py.pointConstraint(sideTracker,distanceLocators[0], mo=0, w=1);
        snap2 = py.pointConstraint(leftJoint,distanceLocators[1], mo=0, w=1);
        distanceToLeftSide = py.getAttr(distanceNodeShape+".distance");
        py.delete(snap2);
        snap2 = py.pointConstraint(rightJoint,distanceLocators[1], mo=0, w=1);
        distanceToRightSide = py.getAttr(distanceNodeShape+".distance");
        py.delete(snap2);
        if(round(distanceToLeftSide,0) == round(distanceToRightSide,0)):
            py.setAttr(outputPelvis+".r",0,0,0);
            remainingAxis.remove(axis[sideAxisIndex]);
            sideAxisIndex = axis.index(remainingAxis[0]);
            sideArray = [];
            i=0;
            while(i < len(axis)):
                if(i == sideAxisIndex):
                    sideArray.append(1);
                else:
                    sideArray.append(0);
                i+=1;
            snap = py.aimConstraint(centerAlignment,base,aim=aimArray,u=sideArray,wut="objectrotation",wuo=sideTracker,wu=[1,0,0],mo=0,w=1);
            rotations = list(py.getAttr(base+".r")[0]);
            py.setAttr(outputPelvis+".r",rotations[0],rotations[1],rotations[2]);
            py.delete(snap);
###############################################################################
#"""# FIND THE SIDE AXIS OF THE PELVIS                                        #
###############################################################################
        skipAxis = axis[:];
        skipAxis.remove(axis[sideAxisIndex]);
        py.parent(sideTracker,outputPelvis);
        snap = py.pointConstraint(leftJoint,sideTracker,skip=skipAxis,mo=0,w=1);
        sign = "+" if(py.getAttr(sideTracker+".t"+axis[sideAxisIndex]) > 0) else "-";
        sideAxis = axis[sideAxisIndex]+sign;
        sideArray = [];
        i=0;
        while(i < len(axis)):
            if(i == sideAxisIndex):
                sideArray.append(int(sideAxis[-1]+str(1)));
            else:
                sideArray.append(0);
            i+=1;
        py.setAttr(outputPelvis+".r",0,0,0);
        py.parent(sideTracker,w=1);py.delete(snap);
        py.setAttr(sideTracker+".t",10,0,0);
        snap = py.aimConstraint(sideTracker,base,aim=sideArray,u=aimArray,wut="objectrotation",wuo=centerAlignment,wu=[0,1,0],mo=0,w=1);
        rotations = list(py.getAttr(base+".r")[0]);
        py.setAttr(outputPelvis+".r",rotations[0],rotations[1],rotations[2]);
        py.delete(distanceLocators,distanceNode,snap);
###############################################################################
#"""# BREAK TRANSLATION KEYS ON JOINTS IF THEY EXIST                          #
###############################################################################
    permissableJoints = [outputRoot,outputPelvis];
    permissableJoints = list(set(permissableJoints+outputTrajectory));
    if(outputJoints != []):
        i=0;
        while(i < len(outputJoints)):
            if not any(outputJoints[i] in s for s in permissableJoints): 
                if(py.objExists(outputJoints[i]) == 1):
                    translateKeys = py.keyframe(outputJoints[i],at="translate",n=1,s=0,q=1);
                    if(isinstance(translateKeys,list) == 1):
                        ii=0;
                        while(ii < len(translateKeys)):
                            initialAttribute = "."+translateKeys[ii].split("_")[-1];
                            attribute = "".join([x for x in initialAttribute if not x.isdigit()]);
                            try:
                                py.disconnectAttr(translateKeys[ii]+".output",outputJoints[i]+attribute);
                            except:
                                pass;
                            ii+=1;
            i+=1;
###############################################################################
#"""# ALIGN THE PELVIS TO FIND MIDDLE JOINTS                                  #
###############################################################################
    if(outputLumbar != "none" and override == 0):
        middleJoints = [outputPelvis];
        expendableNodes = [];
        i=0;
        while(i < len(outputAnimJoints)):
            worldPosition = py.xform(outputAnimJoints[i],q=1,t=1,ws=1);
            dx = 0.0-worldPosition[0];
            dy = 0.0-worldPosition[1];
            dz = 0.0-worldPosition[2];
            distance = math.sqrt(dx*dx+dy*dy+dz*dz);
            ii=0;
            while(ii < len(worldPosition)):
                worldPosition[ii] = round(worldPosition[ii],0);
                ii+=1;
            parentPosition = "?";
            parents = py.listRelatives(outputAnimJoints[i],type="joint",p=1,s=0);
            if(isinstance(parents,list) == 1):
                attributeExists = py.listAttr(parents[0],st=["position"],r=1);
                if(isinstance(attributeExists, list) == 1):
                    parentPosition = py.getAttr(parents[0]+".position", asString=1); 
###############################################################################
#"""# REORDER JOINTS IF SIDE JOINTS ARE ABOVE THE PARENT (IE:["L_ARM","NECK"])#
###############################################################################
            side = "M" if(worldPosition[0] == 0.0) else "?";
            if(side == "M" and parentPosition == "M"):
                middleJoints.append(outputAnimJoints[i]);
                attributeExists = py.listAttr(outputAnimJoints[i],st=["position"],r=1);
                if(isinstance(attributeExists, list) == 0):
                    py.addAttr(outputAnimJoints[i],ln="position",at="enum",en="M");
                    py.setAttr(outputAnimJoints[i]+".position", k=0, cb=1, e=1);
                py.setAttr(centerAlignment+".t",0,distance*2,0);
                if(i > 0):#AIMS EACH MIDDLE SEGMENT UPWARDS TO STRAIGHTEN
                    py.parent(centerAlignment,outputAnimJoints[i]);
                    absoluteTranslations = [];
                    translations = list(py.getAttr(centerAlignment+".t")[0]);
                    ii=0;
                    while(ii < len(translations)):
                        absoluteTranslations.append(abs(round(translations[ii],1)));
                        translations[ii] = round(translations[ii],1);
                        ii+=1;
                    highestValue = max(absoluteTranslations);
                    highestValueIndex = absoluteTranslations.index(highestValue);
                    sign = "+" if(absoluteTranslations[highestValueIndex] in translations) else "-";
                    pointAxis = axis[highestValueIndex]+sign;
                    pointArray = [];
                    ii=0;
                    while(ii < 3):
                        if(ii == highestValueIndex):
                            pointArray.append(int(pointAxis[-1]+str(1)));
                        else:
                            pointArray.append(0);
                        ii+=1;
                    py.parent(centerAlignment,w=1);
                    py.parent(base,outputAnimJoints[i]);
                    py.setAttr(base+".t",0,0,0);py.setAttr(base+".r",0,0,0);
                    snap = py.aimConstraint(centerAlignment,base,aim=pointArray,u=[0,0,0],wut="none",mo=0,w=1);
                    rotations = list(py.getAttr(base+".r")[0]);
                    py.delete(snap);
                    py.setAttr(outputAnimJoints[i]+".r",rotations[0],rotations[1],rotations[2]);
                if(isinstance(children,list) == 1 and i > 0):#UNPARENT SIDE SEGMENTS
                    ii=0;
                    while(ii < len(children)):
                        childPosition = py.xform(children[ii],q=1,t=1,ws=1);
                        iii=0;
                        while(iii < len(childPosition)):
                            childPosition[iii] = round(childPosition[iii],1);
                            iii+=1;
                        if not(childPosition[sideAxisIndex] == 0):
                            py.parent(children[ii],w=1);
                            py.parent(children[ii],outputAnimJoints[i]);
                        ii+=1;
###############################################################################
#"""# FIND THE AIM AXIS OF THE REMAINING JOINTS                               #
###############################################################################
            parentPosition = "?";
            parents = py.listRelatives(outputAnimJoints[i],type="joint",p=1);
            children = py.listRelatives(outputAnimJoints[i],type="joint",c=1);
            if(isinstance(parents,list) == 1):
                attributeExists = py.listAttr(parents[0],st=["position"],r=1);
                if(isinstance(attributeExists, list) == 1):
                    parentPosition = py.getAttr(parents[0]+".position", asString=1); 
            mirrored = [s for s in mirrorJoints if outputAnimJoints[i] in s];
            if not(isinstance(children,list) == 0 and parentPosition == "M" and side != "M" and mirrored == []):
                absoluteTranslations = [];
                if not any(x in outputAnimJoints[i] for x in socketJoints):
                    if(isinstance(children,list) == 1 and mirrored == []):
                        invalidChildren = [];
                        ii=0;
                        while(ii < len(children)):
                            subPosition = py.xform(children[ii],q=1,t=1,ws=1);
                            iii=0;
                            while(iii < len(subPosition)):
                                subPosition[iii] = round(subPosition[iii],0);
                                iii+=1;
                            subSide = "M" if(subPosition[0] == 0.0) else "?";
                            if not any(x in children[ii] for x in mirrorJoints):
                                if(side == "M" and subSide != "M"):
                                    invalidChildren.append(children[ii]);
                            ii+=1;
                        children = list(set(children)-set(invalidChildren));
                        if(len(children) == 0):
                            children = "";
                if(isinstance(children,list) == 0):#!
                    if(isinstance(parents,list) == 1):
                        attributeExists = py.listAttr(parents[0],st=["aimAxis"],r=1);
                        if(isinstance(attributeExists, list) == 1):
                            tipLocator = py.spaceLocator(p=(0,0,0))[0];
                            expendableNodes.append(tipLocator);
                            py.parent(tipLocator,parents[0]);
                            py.setAttr(tipLocator+".t",0,0,0);
                            py.setAttr(tipLocator+".r",0,0,0);
                            dx = 0-worldPosition[0];
                            dy = 0-worldPosition[1];
                            dz = 0-worldPosition[2];
                            distance = math.sqrt(dx*dx+dy*dy+dz*dz);
                            py.setAttr(tipLocator+".t"+aimAxis[0],float(aimAxis[-1]+str(distance*2)));
                            originPosition = py.xform(parents[0],q=1,t=1,ws=1);
                            worldPosition = py.xform(outputAnimJoints[i],q=1,t=1,ws=1);
                            py.parent(tipLocator,outputAnimJoints[i]);
                            checkJoint = tipLocator;
                        else:    
                            checkJoint = parents[0];
                    else:   
                        checkJoint = outputAnimJoints[i];  
                else:
                    checkJoint = children[0];
                    children = children[0];
                translations = list(py.getAttr(checkJoint+".t")[0]);
                ii=0;
                while(ii < len(translations)):
                    absoluteTranslations.append(abs(round(translations[ii],1)));
                    translations[ii] = round(translations[ii],1);
                    ii+=1;
                highestValue = max(absoluteTranslations);
                highestValueIndex = absoluteTranslations.index(highestValue);
                sign = "+" if(absoluteTranslations[highestValueIndex] in translations) else "-";
                aimAxis = axis[highestValueIndex]+sign;
                if(checkJoint != children):
                    child = py.spaceLocator(p=(0,0,0))[0];
                    py.parent(child,outputAnimJoints[i]);
                    py.setAttr(child+".t",0,0,0);py.setAttr(child+".r",0,0,0);
                    py.setAttr(child+".t"+aimAxis[0],int(aimAxis[-1]+str(1)));
                attributeExists = py.listAttr(outputAnimJoints[i],st=["aimAxis"],r=1);
                if(isinstance(attributeExists, list) == 0):
                    py.addAttr(outputAnimJoints[i],ln="aimAxis",at="enum",en=aimAxis);
                    py.setAttr(outputAnimJoints[i]+".aimAxis", k=0, cb=1, e=1);
            else:
                py.delete(outputAnimJoints[i]);
            i+=1;
        if(isinstance(expendableNodes,list) == 1 and len(expendableNodes) > 0):#!
            py.delete(expendableNodes[:]);
###############################################################################
#"""# FIND THE AXIS FOR THE LEFT SIDE OF THE RIG                              #
###############################################################################   
    if(leftJoint != "none" and middleJoints != []):
        positionAbsolute = [];
        leftLocator = py.spaceLocator(p=(0,0,0))[0];
        snap = py.pointConstraint(leftJoint,leftLocator,mo=0,w=1);
        py.delete(snap);py.setAttr(leftLocator+".ty",0);
        position = py.xform(leftLocator,q=1,t=1,ws=1);
        i=0;
        while(i < len(position)):
            positionAbsolute.append(abs(position[i]));
            i+=1;
        leftAxisValue = max(positionAbsolute);
        if(leftAxisValue in position):
            leftAxisIndex = position.index(leftAxisValue);
            sign="+";
        else:
            leftAxisIndex = position.index(leftAxisValue*-1);
            sign="-";
        leftAxis = axis[leftAxisIndex]+sign;
        nonSideAxis = axis[:];
        nonSideAxis.remove(leftAxis[0]);
        py.setAttr(leftLocator+".t",0,0,0);
        py.setAttr(leftLocator+".t"+leftAxis[0],int(leftAxis[-1]+str(1)));
        i=0;
        while(i < len(middleJoints)):
            positionAbsolute = [];
            snap = py.pointConstraint(middleJoints[i],leftLocator,skip=[leftAxis[0]],mo=0,w=1);
            py.delete(snap);
            py.parent(leftLocator,middleJoints[i]);
            position = list(py.getAttr(leftLocator+".t")[0]);
            ii=0;
            while(ii < len(position)):
                positionAbsolute.append(abs(position[ii]));
                ii+=1;
            tempAxisValue = max(positionAbsolute);
            if(tempAxisValue in position):
                tempAxisIndex = position.index(tempAxisValue);
                sign="+";
            else:
                tempAxisIndex = position.index(tempAxisValue*-1);
                sign="-";
            tempLeftAxis = axis[tempAxisIndex]+sign;
            tempSideAxis = axis[tempAxisIndex]+"+";
            attributeExists = py.listAttr(middleJoints[i],st=["leftAxis"],r=1);
            if(isinstance(attributeExists, list) == 0):
                py.addAttr(middleJoints[i],ln="leftAxis",at="enum",en=tempLeftAxis);
                py.setAttr(middleJoints[i]+".leftAxis", k=0, cb=1, e=1);    
            attributeExists = py.listAttr(middleJoints[i],st=["rightAxis"],r=1);
            if(isinstance(attributeExists, list) == 0):
                sign = "-" if("+" in tempLeftAxis[-1]) else "+";
                rightAxis = tempLeftAxis[0]+sign;
                py.addAttr(middleJoints[i],ln="rightAxis",at="enum",en=rightAxis);
                py.setAttr(middleJoints[i]+".rightAxis", k=0, cb=1, e=1);    
            attributeExists = py.listAttr(middleJoints[i],st=["sideAxis"],r=1);
            if(isinstance(attributeExists, list) == 0):
                py.addAttr(middleJoints[i],ln="sideAxis",at="enum",en=tempSideAxis);
                py.setAttr(middleJoints[i]+".sideAxis", k=0, cb=1, e=1);
            py.parent(leftLocator,w=1);
            i+=1;
        py.delete(leftLocator);      
###############################################################################
#"""# ADD FORWARD AXIS TO ALL MIDDLE JOINTS                                   #
###############################################################################
        i=0;
        while(i < len(middleJoints)):
            aim = py.getAttr(middleJoints[i]+".aimAxis",asString=1);
            side = py.getAttr(middleJoints[i]+".leftAxis",asString=1);
            frontAxis = axis[:];
            try:
                frontAxis.remove(aim[0]);
                frontAxis.remove(side[0]);
            except:
                middleJoints.remove(middleJoints[i]);
            if(("x" in aim and "z" in side) or ("y" in aim and "x" in side) or ("z" in aim and "y" in side)):
                sign = "+" if(aim[-1] == side[-1]) else "-";
            else:
                sign = "-" if(aim[-1] == side[-1]) else "+";
            frontAxis = frontAxis[0]+sign;
            attributeExists = py.listAttr(middleJoints[i],st=["frontAxis"],r=1);
            if(isinstance(attributeExists, list) == 0):
                py.addAttr(middleJoints[i],ln="frontAxis",at="enum",en=frontAxis);
                py.setAttr(middleJoints[i]+".frontAxis", k=0, cb=1, e=1);
            i+=1;
###############################################################################
#"""# LIST MIDDLE JOINTS AND REARANGE THEM FROM BOTTOM TO TOP BY HEIGHT       #
###############################################################################
    potentialSpineJoints = [];
    if(len(middleJoints) > 0 and override == 0):
        potentialSpineJointsHeights = [];
        i=0;
        while(i < len(middleJoints)):
            position = py.xform(middleJoints[i],q=1,t=1,ws=1,r=1);
            potentialSpineJoints.append(middleJoints[i]);
            potentialSpineJointsHeights.append(round(position[1],1));
            i+=1;
        #REORGANIZE LIST BASED ON SORTED NUMBERS FROM ANOTHER LIST
        heightElevation = sorted(potentialSpineJointsHeights);
        i=0;
        while(i < len(heightElevation)):
            index = potentialSpineJointsHeights.index(heightElevation[i]);
            potentialSpineJointsHeights.insert(i,potentialSpineJointsHeights.pop(index));
            potentialSpineJoints.insert(i,potentialSpineJoints.pop(index));
            i+=1; 
###############################################################################
#"""# LIST SPINE, NECK, AND HEAD JOINTS FROM SEGMENT                          #
###############################################################################
    if(socketJoints != [] and potentialSpineJoints != [] and override == 0):
        maxHipIndex = int(round(float(len(middleJoints))/4,0));
        hipIndex = potentialSpineJoints.index(socketJoints[0]);
        value = 0 if(hipIndex >= maxHipIndex) else -1;
        if(len(socketJoints) > 1 or hipIndex >= maxHipIndex):
            index = potentialSpineJoints.index(socketJoints[value]);
            outputThorax = potentialSpineJoints[index];
            outputCranium = potentialSpineJoints[index+1:];
            outputSpine = potentialSpineJoints[:index+1];
        else:#WHEN ONLY ONE SOCKET JOINT EXISTS AND ITS A HIP SOCKET
            index = len(middleJoints);
            if(len(middleJoints) <= 4):
                outputThorax = potentialSpineJoints[index];
                outputSpine = potentialSpineJoints[:index+1];
            else:
                outputThorax = potentialSpineJoints[index-3];
                outputCranium = potentialSpineJoints[index-2:];
                outputSpine = potentialSpineJoints[:index-2];
        neckNames = ["NECK","Neck","neck","NEK","Nek","nek","NEC","Nec","nec","nck"];
        neck = [i for e in neckNames for i in potentialSpineJoints if e in i];
        if(neck != []):
            index = potentialSpineJoints.index(neck[0]);
            currentThorax = outputThorax;
            outputThorax = potentialSpineJoints[index-1];
            outputCranium = potentialSpineJoints[index:];
            outputSpine = potentialSpineJoints[:index];
            if(outputThorax != "none" and outputThorax != currentThorax):
                log = log+"Discrepancy: '"+currentThorax+"' was selected as the thorax, but '"+outputThorax+"' was picked by the rigger.\n";
###############################################################################
#"""# FIND AND LIST THE NECK/HEAD SEGMENTS                                    #
###############################################################################
    if(outputCranium != [] and override == 0):
        initialCraniumList = outputCranium[:];
        if(len(outputCranium) > 3):
            index = len(outputCranium);
            outputCranium = outputCranium[index-2:];
        elif(len(outputCranium) == 2 or len(outputCranium) == 3):
            outputCranium = outputCranium[:2];
        else:
            outputCranium = [];
        newCraniumList = outputCranium;
        headNames = ["HEAD","Head","head","HED","Hed","hed"];
        head = [i for e in headNames for i in outputCranium if e in i];
        if(head != []):
            outputCranium = [];
            outputCranium.append(initialCraniumList[0]);
            outputCranium.append(head[0]); 
        if(outputCranium != newCraniumList):
            log = log+"Discrepancy: The 'neck' and 'head' selected were different that chosen by the rigger.\n";    
###############################################################################
#"""# FIND AND LIST THE SPINE SEGMENTS                                        #
###############################################################################
    if(outputSpine != [] and override == 0):
        if(len(outputSpine) < 4):
            while(len(outputSpine) < 4):
                outputSpine.insert(1,"none");
        elif(len(outputSpine) > 4):
            spineBox = outputSpine[:];
            index = len(outputSpine)-1;
            spineDivider = int(round(float(len(outputSpine))/4,0));
            outputSpine = [spineBox[0],spineBox[spineDivider],spineBox[index-spineDivider],spineBox[-1]];
        outputRig.append(outputSpine); 
        outputRig.append(outputCranium); 
###############################################################################
#"""# FIND AND LIST THE ARM AND LEG SOCKET JOINTS                             #
###############################################################################
    if(socketJoints != [] and posture != "serpant" and override == 0):
        leftLegSockets = [];
        rightLegSockets = [];
        leftArmSockets = [];
        rightArmSockets = [];
        worldSideAxis = "x+";#BECAUSE RIGS SHOULD BE FACING Z FORWARD (Y UP)
        maxHipIndex = int(round(float(len(outputSpine))/4,0));
        i=0;
        while(i < len(socketJoints)):
            children = py.listRelatives(socketJoints[i],type="joint",c=1,s=0);
            if(isinstance(children,list) == 0):
                children = [];
            ii=0;
            while(ii < len(children)):
                attributeExists = py.listAttr(children[ii],st=["position"],r=1);
                if(isinstance(attributeExists, list) == 1):
                    side = py.getAttr(children[ii]+".position", asString=1); 
                else:
                    side = "?";
                grandChildren = py.listRelatives(children[ii],type="joint",c=1,s=0);
                if(isinstance(grandChildren,list) == 1 and side != "M"):
                    positionAbsolute = [];
                    sideLocator = py.spaceLocator(p=(0,0,0))[0];
                    snap = py.pointConstraint(children[ii],sideLocator,mo=0,w=1);
                    py.delete(snap);
                    nonSideAxis = axis[:];
                    nonSideAxis.remove(worldSideAxis[0]);
                    py.setAttr(sideLocator+".t"+nonSideAxis[0],0);
                    py.setAttr(sideLocator+".t"+nonSideAxis[1],0);
                    position = py.xform(sideLocator,q=1,t=1,ws=1);
                    iii=0;
                    while(iii < len(position)):
                        positionAbsolute.append(abs(position[iii]));
                        iii+=1;
                    tempAxisValue = max(positionAbsolute);
                    if(tempAxisValue in position):
                        tempAxisIndex = position.index(tempAxisValue);
                        sign="+";
                    else:
                        tempAxisIndex = position.index(tempAxisValue*-1);
                        sign="-";
                    tempAxis = axis[tempAxisIndex]+sign;
                    py.delete(sideLocator);
                    index = outputSpine.index(socketJoints[i]);
                    if(index < maxHipIndex):
                        if(tempAxis == leftAxis):
                            leftLegSockets.append(children[ii]);
                        else:
                            rightLegSockets.append(children[ii]);
                    else:
                        if(tempAxis == leftAxis):
                            leftArmSockets.append(children[ii]);
                        else:
                            rightArmSockets.append(children[ii]);
                ii+=1;
            i+=1;
###############################################################################
#"""# FIND AND LIST THE ARM AND LEG JOINTS SEGMENTS                           #
###############################################################################
    if(override == 0):
        if(leftArmSockets != [] or rightArmSockets != [] or leftLegSockets != [] or rightLegSockets != []):
            limbs = [leftArmSockets,rightArmSockets,leftLegSockets,rightLegSockets];
            outputLimbs = [outputLeftArm,outputRightArm,outputLeftLeg,outputRightLeg];
            limbSegments = leftArmSockets+rightArmSockets+leftLegSockets+rightLegSockets;
            armSegments = leftArmSockets+rightArmSockets;
            i=0;
            while(i < len(limbs)):
                ii=0;
                try:
                    limbContainer = [limbs[i][ii]];
                except:
                    limbContainer = [limbs[i]];
                while(ii < len(limbContainer)):
                    children = py.listRelatives(limbContainer[ii],type="joint",c=1);
                    if(isinstance(children,list) == 1):
                        if(len(children) > 1):
                            invalidJointChains = [];
                            iii=0;
                            while(iii < len(children)):
                                grandChildren = py.listRelatives(children[iii],type="joint",ad=1,c=1);
                                if(isinstance(grandChildren,list) == 0 or len(grandChildren) == 1):
                                    invalidJointChains.append(children[iii]);
                                iii+=1;
                            children = [x for x in children if x not in invalidJointChains];
                        if(len(children) > 0 and len(children) < 2):
                            limbContainer.append(children[0]);
                            limbs[i].append(children[0]);  
                    ii+=1;
                outputLimbs[i].append(limbContainer[:]);
                i+=1;
            i=0;
            while(i < len(outputLimbs)):
                outputRig.append(outputLimbs[i]); 
                i+=1;  
###############################################################################
#"""# FIND AND LIST THE FINGER/TOES PARENT JOINTS                             #
###############################################################################
    if(outputLimbs != "none" and override == 0):
        metaDigits = deepcopy(outputLimbs[:]);
        metaDigitsClock = deepcopy(metaDigits[:]);
        i=0;
        while(i < len(metaDigitsClock)):
            ii=0;
            while(ii < len(metaDigitsClock[i])):
                digits = py.listRelatives(metaDigitsClock[i][ii][-1],type="joint",c=1);
                if(isinstance(digits,list) == 1):
                    cycleCount = len(digits);
                    iii=0;
                    while(iii < cycleCount):
                        subDigits = py.listRelatives(digits[iii],type="joint",c=1);
                        if(isinstance(subDigits,list) == 0):
                            py.delete(digits[iii]);
                        iii+=1;
                    digits = py.listRelatives(metaDigitsClock[i][ii][-1],type="joint",c=1);
                    if(isinstance(digits,list) == 0):
                        digits = [];
                    if(len(digits) > 0):#!USED TO EQUAL 5
                        digitList = [];
                        iii=0;
                        while(iii < len(digits)):
                            digitList.append([digits[iii]]);
                            iii+=1;
                        metaDigits[i][ii] = digitList[:];
                else:
                    metaDigits[i][ii] = [];
                ii+=1;
            i+=1;
        i=0;
        while(i < len(metaDigits)):
            outputRig.append(metaDigits[i]); 
            i+=1;  
###############################################################################
#"""# FIND AND LIST THE INDIVIDUAL FINGER SEGMENTS                            #
###############################################################################
    if(len(outputRig) >= 6):
        thumbNames = ["THUMB","Thumb","thumb","THUM","Thum","thum","finger0"];
        indexNames = ["INDEX","Index","index","POINT","Point","point","finger1"];
        middleNames = ["MIDDLE","Middle","middle","MID","Mid","mid","finger2"];
        ringNames = ["RING","Ring","ring","THIRD","Third","third","finger3"];
        pinkyNames = ["PINKY","Pinky","pinky","BABY","Baby","baby","finger4"];
        digitNames = [thumbNames,indexNames,middleNames,ringNames,pinkyNames];
        digitAppendedNames = thumbNames+indexNames+middleNames+ringNames+pinkyNames;
        i=6;
        while(i < len(outputRig)):
            digits = [];
            ii=0;
            while(ii < len(outputRig[i])):
                thumb = [];
                potentialThumbList = [];
                shortestDistanceToWrist = "none";
                wristAim = py.getAttr(outputRig[i-4][ii][-1]+".aimAxis",asString=1);
                iii=0;#FIND THE THUMB BY USING WRIST'S AIM AXIS
                while(iii < len(outputRig[i][ii])):
                    distanceToWrist = py.getAttr(outputRig[i][ii][iii][0]+".t"+wristAim[0]);
                    if(shortestDistanceToWrist == "none"):
                        shortestDistanceToWrist = abs(distanceToWrist);
                        potentialThumbList = outputRig[i][ii][iii]; 
                    if(abs(distanceToWrist) < shortestDistanceToWrist):
                        potentialThumbList = outputRig[i][ii][iii]; 
                    iii+=1;
                thumb = potentialThumbList;
                #FIND THE SIDE AXIS BY FINDING THE LARGEST RANGED AXIS
                if(thumb != []):
                    wristSide = "none";
                    remainingAxis = axis[:];
                    remainingAxis.remove(wristAim[0]);
                    firstAxisRange = "none";
                    secondAxisRange = "none";
                    iii=0;  
                    while(iii < len(outputRig[i][ii])):
                        firstAxis = py.getAttr(outputRig[i][ii][iii][0]+".t"+remainingAxis[0]);
                        secondAxis = py.getAttr(outputRig[i][ii][iii][0]+".t"+remainingAxis[1]);
                        if(firstAxisRange == "none"):firstAxisRange = [firstAxis,firstAxis];
                        if(secondAxisRange == "none"):secondAxisRange = [secondAxis,secondAxis];
                        if(firstAxis < firstAxisRange[0]):firstAxisRange[0] = firstAxis;
                        if(firstAxis > firstAxisRange[1]):firstAxisRange[1] = firstAxis; 
                        if(secondAxis < secondAxisRange[0]):secondAxisRange[0] = secondAxis;
                        if(secondAxis > secondAxisRange[1]):secondAxisRange[1] = secondAxis;
                        iii+=1;
                    firstAxisRange = firstAxisRange[1]-firstAxisRange[0];
                    secondAxisRange = secondAxisRange[1]-secondAxisRange[0];
                    if(firstAxisRange > secondAxisRange):
                        wristSide = remainingAxis[0];
                    elif(firstAxisRange < secondAxisRange):
                        wristSide = remainingAxis[1];
                    value = py.getAttr(thumb[0]+".t"+wristSide[0]);
                    wristSide = wristSide+"-" if(value < 0) else wristSide+"+";
                    #FIND THE FINGERS BY USING THE SIDE AXIS TO MAKE IN ORDER LIST
                    if(wristSide != "none"):
                        digitList = [];
                        digitListPosition = [];
                        iii=0;
                        while(iii < len(outputRig[i][ii])):
                            position = py.getAttr(outputRig[i][ii][iii][0]+".t"+wristSide[0]);
                            digitList.append(outputRig[i][ii][iii]);
                            digitListPosition.append(position);
                            iii+=1;
                        thumbIndex = digitList.index(thumb);
                        digitList.remove(digitList[thumbIndex]);
                        digitListPosition.remove(digitListPosition[thumbIndex]);
                        #REORGANIZE LIST BASED ON SORTED NUMBERS FROM ANOTHER LIST
                        positionElevation = sorted(digitListPosition);
                        if(wristSide[-1] == "-"):
                            positionElevation.reverse();
                        iii=0;
                        while(iii < len(positionElevation)):
                            index = digitListPosition.index(positionElevation[iii]);
                            digitListPosition.insert(iii,digitListPosition.pop(index));
                            digitList.insert(iii,digitList.pop(index));
                            iii+=1;
                        digitList.append(thumb);
                        digitList.reverse();
                        digits = digitList;
                outputRig[i][ii] = digits;
                #REORGANIZE LIST IF NAMES ARE PROVIDED
                if(len(digits) == len(digitNames)):
                    newDigitList = [];
                    iii=0;
                    while(iii < len(digitNames)):
                        iiii=0;
                        while(iiii < len(outputRig[i][ii])):
                            existing = [s for e in digitNames[iii] for s in outputRig[i][ii][iiii] if e in s];
                            if(existing != []):
                                newDigitList.append([existing[0]]);
                            iiii+=1;
                        iii+=1;
                    if(len(newDigitList) == len(digitNames)):
                        outputRig[i][ii] = newDigitList;  
                #FIND THE CHAINING FINGER JOINTS
                iii=0;
                while(iii < len(outputRig[i][ii])):
                    iiii=0;
                    while(iiii < len(outputRig[i][ii][iii])):
                        children = py.listRelatives(outputRig[i][ii][iii][iiii],type="joint",c=1);
                        if(isinstance(children,list) == 1):
                            if(len(children) > 1):
                                invalidJointChains = [];
                                iiiii=0;
                                while(iiiii < len(children)):
                                    grandChildren = py.listRelatives(children[iiiii],type="joint",ad=1,c=1);
                                    if(isinstance(grandChildren,list) == 0 or len(grandChildren) == 1):
                                        invalidJointChains.append(children[iiii]);
                                    iiiii+=1;
                                children = [x for x in children if x not in invalidJointChains];
                            if(len(children) > 0 and len(children) < 2):
                                outputRig[i][ii][iii].append(children[0]);
                        iiii+=1;     
                    iii+=1;
                ii+=1;
            i+=1;
###############################################################################
#"""# GENERATE TARGET LISTS                                                   #
############################################################################### 
    if(outputRig != []):
        outputRig.append(outputTrajectory);
        inputRig = [[nameSpace+"c_M_spineMaster_v1_CTRL",nameSpace+"c_M_spine1_v1_CTRL",nameSpace+"c_M_spine2_v1_CTRL",nameSpace+"c_M_spine3_v1_CTRL"],
                    [nameSpace+"c_M_neck_v1_CTRL",nameSpace+"c_M_head_v1_CTRL"],
                    [[nameSpace+"c_L_clavicle_v1_CTRL",nameSpace+"c_L_shoulder_v1_CTRL",nameSpace+"c_L_elbow_v1_CTRL",nameSpace+"c_L_wrist_v1_CTRL"]],
                    [[nameSpace+"c_R_clavicle_v1_CTRL",nameSpace+"c_R_shoulder_v1_CTRL",nameSpace+"c_R_elbow_v1_CTRL",nameSpace+"c_R_wrist_v1_CTRL"]],
                    [[nameSpace+"c_L_hip_v1_CTRL",nameSpace+"c_L_knee_v1_CTRL",nameSpace+"c_L_ankle_v1_CTRL",nameSpace+"c_L_ball_v1_CTRL"]],
                    [[nameSpace+"c_R_hip_v1_CTRL",nameSpace+"c_R_knee_v1_CTRL",nameSpace+"c_R_ankle_v1_CTRL",nameSpace+"c_R_ball_v1_CTRL"]],
                    [[[nameSpace+"c_L_thumb1_v1_CTRL",nameSpace+"c_L_thumb2_v1_CTRL",nameSpace+"c_L_thumb3_v1_CTRL"],
                      [nameSpace+"c_L_index1_v1_CTRL",nameSpace+"c_L_index2_v1_CTRL",nameSpace+"c_L_index3_v1_CTRL"],
                      [nameSpace+"c_L_middle1_v1_CTRL",nameSpace+"c_L_middle2_v1_CTRL",nameSpace+"c_L_middle3_v1_CTRL"],
                      [nameSpace+"c_L_ring1_v1_CTRL",nameSpace+"c_L_ring2_v1_CTRL",nameSpace+"c_L_ring3_v1_CTRL"],
                      [nameSpace+"c_L_pinky1_v1_CTRL",nameSpace+"c_L_pinky2_v1_CTRL",nameSpace+"c_L_pinky3_v1_CTRL"]]],
                    [[[nameSpace+"c_R_thumb1_v1_CTRL",nameSpace+"c_R_thumb2_v1_CTRL",nameSpace+"c_R_thumb3_v1_CTRL"],
                      [nameSpace+"c_R_index1_v1_CTRL",nameSpace+"c_R_index2_v1_CTRL",nameSpace+"c_R_index3_v1_CTRL"],
                      [nameSpace+"c_R_middle1_v1_CTRL",nameSpace+"c_R_middle2_v1_CTRL",nameSpace+"c_R_middle3_v1_CTRL"],
                      [nameSpace+"c_R_ring1_v1_CTRL",nameSpace+"c_R_ring2_v1_CTRL",nameSpace+"c_R_ring3_v1_CTRL"],
                      [nameSpace+"c_R_pinky1_v1_CTRL",nameSpace+"c_R_pinky2_v1_CTRL",nameSpace+"c_R_pinky3_v1_CTRL"]]],
                    [[]],
                    [[]],
                    [nameSpace+"c_M_trajectory_v1_CTRL"]]; 
        inputTargets = [[inputRig[0][0]]+inputRig[0],[inputRig[0][-1]]+inputRig[1]];
        outputTargets = [[outputRig[0][0]]+outputRig[0],[outputRig[0][-1]]+outputRig[1]];
        #ADD LOCATOR TO THE TOP OF SPINE AND HEAD 
        i=0;
        while(i < len(inputTargets)):
            endLocator = py.spaceLocator(p=(0,0,0))[0];
            py.parent(endLocator,outputTargets[i][-1]);
            py.setAttr(endLocator+".t",0,0,0);
            py.setAttr(endLocator+".r",0,0,0);
            aim = py.getAttr(outputTargets[i][-1]+".aimAxis",asString=1);
            py.setAttr(endLocator+".t"+aim[0],int(aim[-1]+str(1)));
            outputTargets[i].append(endLocator);
            i+=1;
        i=2;
        while(i < 10):
            ii=0;
            while(ii < len(outputRig[i]) and ii < len(inputRig[i])):
                if(i < 6):#LIMBS
                    index = 0 if(i >= 4) else -1;
                    inputParents = [inputRig[0][index]];
                    outputParents = py.listRelatives(outputRig[i][ii][0],type="joint",p=1);
                    inputTargets.append(inputParents+inputRig[i][ii]);
                    outputTargets.append(outputParents+outputRig[i][ii]);
                    #ADD LOCATOR TO THE END OF EACH SEGMENT 
                    if not(ii < len(outputRig[i])-1 and ii < len(inputRig[i])-1):
                        endLocator = py.spaceLocator(p=(0,0,0))[0];
                        py.parent(endLocator,outputRig[i][ii][-1]);
                        py.setAttr(endLocator+".t",0,0,0);
                        py.setAttr(endLocator+".r",0,0,0);
                        aim = py.getAttr(outputRig[i][ii][-1]+".aimAxis",asString=1);
                        py.setAttr(endLocator+".t"+aim[0],int(aim[-1]+str(1)));
                        outputTargets[-1].append(endLocator);
                if(i >=6 and i < 10):#DIGITS
                    iii=0;
                    while(iii < len(outputRig[i][ii]) and iii < len(inputRig[i][ii])):
                        inputParents = [inputRig[i-4][ii][-1]];
                        outputParents = py.listRelatives(outputRig[i][ii][iii][0],type="joint",p=1);
                        inputTargets.append(inputParents+inputRig[i][ii][iii]);
                        outputTargets.append(outputParents+outputRig[i][ii][iii]);
                        #ADD LOCATOR TO THE END OF EACH SEGMENT 
                        endLocatorShape = py.listRelatives(outputRig[i][ii][iii],type="locator",ad=1,c=1);
                        endLocator = endLocatorShape[0].replace("Shape","");
                        outputTargets[-1].append(endLocator);
                        iii+=1;
                ii+=1;
            i+=1;
        inputTargets.append(inputRig[-1]);
        outputTargets.append(outputRig[-1]);
###############################################################################
#"""# SPECIAL CASE: SET CS ("BIP") RIG'S SPINE TO SPECIFIC ROTATIONS          #
###############################################################################
        MAX = False;
        #pelvisOffset = [0,0,96.831]; translations
        characterStudioCentralValues = [[0,0,-2.7],[0,0,-6.029],[0,0,0.192],
                                        [0,0,21.855],[0,0,0]];
                                        #[0,0,21.855],[0,0,-4.776]];
                                        
        characterStudioLeftArmValues = [[7.117,-80.883,-178.67],[4.615,54.007,6.916],
                                        #[[-1.401,-80.883,-178.662],[17.695,52.958,18.55],
                                        [0,0,-13.227],[-82.562,5.218,4.998]];
                                        #[0,0,-13.227],[-82.562,5.218,4.998]];
        characterStudioRightArmValues = [[7.117,80.883,-178.67],[-27.164,-50.037,24.723],
                                        #[[1.401,80.883,-178.662],[-17.695,-52.958,18.55],
                                         [0,0,-13.183],[82.562,-5.218,4.998]];
                                         #[0,0,-13.227],[82.562,-5.218,4.998]];
        characterStudioLeftLegValues = [[0.003,184.66,1.288],[0,0,-6.291],#[0,0,-3.196]
                                        #[[179.046,-4.472,-177.146],[0,0,0],#[0,0,-3.196]
                                        [-0.136,-4.749,7.122],[0,0,90],[0,0,180]];
                                        #[-2.186,-4.514,5.984],[0,0,90],[0,0,180]];
        characterStudioRightLegValues = [[-0.003,-184.66,1.288],[0,0,-6.291],#[0,0,-3.196]
                                        #[[-179.046,4.472,-177.146],[0,0,0],#[0,0,-3.196]
                                         [0.136,4.749,7.122],[0,0,90],[0,0,180]];
                                         #[2.186,4.514,5.984],[0,0,90],[0,0,180]];                                 
        characterStudioLeftFingersValues = [[81.56,28.089,28.311],[0,0,5.398],
                                            [0,0,-9.153],[8.231,10.696,7.97],
                                            [0,0,19.737],[0,0,6.224],[9.42,-5.295,6.806],
                                            [0,0,22.206],[0,0,8.17],[2.47,-18.779,19.416],
                                            [0,0,13.905],[0,0,5.929],[-5.787,-33.208,21.809],
                                            [0,0,18.031],[0,0,1.517]];
        characterStudioRightFingersValues = [[-81.56,-28.089,28.311],[0,0,5.398],
                                             [0,0,-9.153],[-8.231,-10.696,7.97],
                                             [0,0,19.737],[0,0,6.224],[-9.42,5.295,6.806],
                                             [0,0,22.206],[0,0,8.17],[-2.47,18.779,19.416],
                                             [0,0,13.905],[0,0,5.929],[5.787,33.208,21.809],
                                             [0,0,18.031],[0,0,1.517]];                            
        if(len(outputTargets)-1 == 16):#3DS MAX BIPEDS ONLY HAVE 16 PARTS
            characterStudioJoints = [outputTargets[0][2:-1]+outputTargets[1][1:-1],
                                     outputTargets[2][1:-1],outputTargets[3][1:-1],
                                     outputTargets[4][1:-1],outputTargets[5][1:-1],
                                     outputTargets[6][1:-2]+outputTargets[7][1:-2]+outputTargets[8][1:-2]+outputTargets[9][1:-2]+outputTargets[10][1:-2],#!
                                     outputTargets[11][1:-2]+outputTargets[12][1:-2]+outputTargets[13][1:-2]+outputTargets[14][1:-2]+outputTargets[15][1:-2]];#!
        characterStudioValues = [characterStudioCentralValues,characterStudioLeftArmValues,
                                 characterStudioRightArmValues,characterStudioLeftLegValues,
                                 characterStudioRightLegValues,characterStudioLeftFingersValues,
                                 characterStudioRightFingersValues];
        if(len(outputPelvis) >= 3):
            #CHECK IF FROM 3DS MAX
            MAX = True if("bip" in outputPelvis[:3].lower() and len(outputTargets)-1 == 16) else False;
        i=0;
        if(MAX == True):
            log = log+"Transfered from a compatible Character Studio rig.\n";
            while(i < len(characterStudioJoints) and i < len(characterStudioValues)):
                ii=0;
                while(ii < len(characterStudioJoints[i]) and ii < len(characterStudioValues[i])):
                    py.setAttr(characterStudioJoints[i][ii]+".r",characterStudioValues[i][ii][0],characterStudioValues[i][ii][1],characterStudioValues[i][ii][2]);
                    ii+=1;
                i+=1;
        else:
            while(i < len(outputAnimJoints)):
                if(outputAnimJoints[i] == "LeftShoulder" and override == 1):
                    py.setAttr(outputAnimJoints[i]+".r",-30,0,16);
                elif(outputAnimJoints[i] == "RightShoulder" and override == 1):
                    py.setAttr(outputAnimJoints[i]+".r",-30,0,-16);
                elif(outputAnimJoints[i] == "LeftArm" and override == 1):
                    py.setAttr(outputAnimJoints[i]+".r",13.182,21.435,-73.344);
                elif(outputAnimJoints[i] == "RightArm" and override == 1):
                    py.setAttr(outputAnimJoints[i]+".r",13.182,-21.435,73.344);
                elif(outputAnimJoints[i] == "LeftForeArm" and override == 1):
                    py.setAttr(outputAnimJoints[i]+".r",15,0,0);
                elif(outputAnimJoints[i] == "RightForeArm" and override == 1):
                    py.setAttr(outputAnimJoints[i]+".r",15,0,0); 
                else:
                    py.setAttr(outputAnimJoints[i]+".r",0,0,0);
                i+=1;
###############################################################################
#"""# COLLECT TRANSFORM VALUES OF OUTPUT JOINTS AFTER TPOSE                   #
###############################################################################
        outputItems = [outputPelvis]+outputAnimJoints;
        outputOrigin = py.listRelatives(outputPelvis,type="joint",p=1,s=0);
        outputItems = outputOrigin+outputItems if(isinstance(outputOrigin,list) == 1) else outputItems;
        translationList = [];
        rotationList = [];
        i=0;
        while(i < len(outputItems)):
            translations = list(py.getAttr(outputItems[i]+".t")[0]);
            rotations = list(py.getAttr(outputItems[i]+".r")[0]);
            translationList.append(translations);
            rotationList.append(rotations);
            i+=1;
###############################################################################
#"""# MAKE ANIMATION LAYER                                                    #
###############################################################################
        inputControllers = [];
        i=0;
        while(i < len(inputTargets)):
            ii=0;
            while(ii < len(inputTargets[i])):
                inputControllers.append(inputTargets[i][ii]);
                ii+=1;
            i+=1;
        py.select(inputControllers[:],r=1); 
        #CREATE NEW CONSTRAINT LAYER
        version=1;
        while(py.objExists("a_M_importedConstraints_v"+str(version)+"_LYR")):
            version+=1;
        conLayer = py.animLayer("a_M_importedConstraints_v"+str(version)+"_LYR");
        py.setAttr(conLayer+".rotationAccumulationMode", 1);
        py.setAttr(conLayer+".scaleAccumulationMode", 0);
        py.animLayer(conLayer,solo=1,e=1);
        #MUTE LAYERS CONNECTED TO THE INPUT RIG
        py.select(inputControllers[:],r=1); 
        relevantLayers = py.animLayer(affectedLayers=1,q=1);
        if(isinstance(relevantLayers,list) == 1):
            i=0;
            while(i < len(relevantLayers)):
                py.animLayer(relevantLayers[i],solo=0,mute=1,e=1);
                py.setAttr(relevantLayers[i]+".override",0);
                i+=1;
        py.animLayer(conLayer,aso=1,e=1);
###############################################################################
#"""# ADD TRANSFORM VALUES OF OUTPUT JOINTS AFTER LAYERING                    #
###############################################################################
        i=0;
        while(i < len(outputItems)):
            py.setAttr(outputItems[i]+".t",translationList[i][0],translationList[i][1],translationList[i][2]);
            py.setAttr(outputItems[i]+".r",rotationList[i][0],rotationList[i][1],rotationList[i][2]);
            i+=1;
###############################################################################
#"""# MATCH PELVIS POSITIONS FOR THE INPUT AND OUTPUT RIGS TO BEGIN MATCHING  #
###############################################################################
        ikControllerList=[];ikPoleVectorList=[];aimArrayList=[];upArrayList=[];
        endJointList=[];endLocatorList=[];midJointList=[];ikChainList=[];
        optionsBoxList=[];
        cogLocator = py.spaceLocator(p=(0,0,0))[0];
        py.pointConstraint(inputTargets[0][0],cogLocator,mo=0,w=1);
        cogParent = py.listRelatives(outputTargets[0][0],p=1);
        if(isinstance(cogParent,list) == 1):
            py.parent(cogLocator,cogParent);
        translations = list(py.getAttr(cogLocator+".t")[0]);
        py.setAttr(outputTargets[0][0]+".t",translations[0],translations[1],translations[2]);
        py.delete(cogLocator);
        py.pointConstraint(outputTargets[0][0],inputTargets[0][0],l=conLayer,mo=0,w=1);
        outputTargets[0].remove(outputTargets[0][0]);
        inputTargets[0].remove(inputTargets[0][0]);
        distanceNodeShape = py.distanceDimension(sp=(0, 100, 0), ep=(0, 10, 0));
        distanceLocators = py.listConnections(distanceNodeShape);
        distanceNode = py.listRelatives(distanceNodeShape, p=1);
        startPoint = py.spaceLocator(p=(0,0,0))[0];
        endPoint = py.spaceLocator(p=(0,0,0))[0];
        py.parent(endPoint,startPoint);
###############################################################################
#"""# CONNECT FK CONTROLLERS BASED ON GERATED LISTS AND COLLECT IK CONTROLLERS#
###############################################################################
        override = override if(RiGGiE == False) else True;
        distance = 100;
        i=0;
        while(i < len(outputTargets) and i < len(inputTargets)):
            ii=0;
            if(outputTargets[i] == outputTrajectory and outputTrajectory != []):
                py.move(0,0,0,outputTrajectory[0],rpr=1);
                py.setAttr(outputTrajectory[0]+".r",0,0,0);
                py.pointConstraint(outputTargets[i][ii],inputTargets[i][ii],l=conLayer,mo=0,w=1);  
                py.orientConstraint(outputTargets[i][ii],inputTargets[i][ii],l=conLayer,mo=1,w=1);  
            while(ii < len(outputTargets[i])-1 and ii < len(inputTargets[i])):
                #CREATE IK CHAINS AND GENERATE A LIST OF CONTROLLERS FOR LATER PAIRING
                baseJoint = outputTargets[i][ii+1];
                if(baseJoint != []):
                    if any(x in baseJoint for x in limbSegments):
                        duplicatedJointChainIK = py.duplicate(baseJoint,ic=1,rc=1);
                        jointChainIK = py.listRelatives(duplicatedJointChainIK[0],type="joint",ad=1,c=1);
                        jointChainIK.append(duplicatedJointChainIK[0]);
                        jointChainIK.reverse();
                        ikChainList.append(jointChainIK)
                        segmentName = "arm" if any(x in baseJoint for x in armSegments) else "leg";
                        jointCount = len(outputTargets[i][1:-1]);
                        if(segmentName == "leg"):
                            midPosition = 1;
                            endPosition = -1 if(jointCount <= 4) else -2;
                        else:
                            midPosition = 2 if(jointCount > 3) else 1;
                            endPosition = -1;
                        endJoint = [s for s in jointChainIK if outputTargets[i][1:-1][endPosition][:-1] in s][0];#END JOINT
                        namedEndJoint = [s for e in endNames for s in jointChainIK if e in s];
                        if(namedEndJoint != []):
                            endJoint = namedEndJoint[0];
                        midJoint = [s for s in jointChainIK if outputTargets[i][1:-1][midPosition][:-1] in s][0];#HINGE JOINT
                        namedMidJoint = [s for e in midNames for s in jointChainIK if e in s];
                        if(namedMidJoint != []):
                            midJoint = namedMidJoint[0]; 
                        type = inputTargets[i][ii+1].split("_")[-3];
                        controllerIK = inputTargets[i][ii+1].replace(type,segmentName);
                        initialPosition = controllerIK.replace(segmentName,segmentName+"InitialPositionIK").replace("CTRL","LOC");
                        #GET IK CONTROLLER'S AIM AND UP AXIS
                        aimArrayIK = py.getAttr(initialPosition+".aimAxis", asString=1); 
                        aimArrayIK = aimArrayIK.split(",");
                        aimArrayIK = [int(aimArrayIK[0]),int(aimArrayIK[1]),int(aimArrayIK[2])];
                        upArrayIK = py.getAttr(initialPosition+".upAxis", asString=1); 
                        upArrayIK = upArrayIK.split(",");
                        upArrayIK = [int(upArrayIK[0]),int(upArrayIK[1]),int(upArrayIK[2])];
                        #CREATE AIM LOCATOR AT END JOINT (TO AIM CONSTRAIN IK CONTROLLER)  
                        attributeExists = py.listAttr(endJoint,st=["aimAxis"],r=1);
                        if(isinstance(attributeExists,list) == 1):
                            aimTempAxis = py.getAttr(endJoint+".aimAxis", asString=1);
                            aimAxisIndex = axis.index(aimTempAxis[0]); 
                            aimTempArray = [];
                            iii=0;
                            while(iii < len(axis)):
                                if(iii == aimAxisIndex):
                                    aimTempArray.append(int(aimTempAxis[-1]+str(1)));
                                else:
                                    aimTempArray.append(0);
                                iii+=1;
                            endLocator = py.spaceLocator(p=(0,0,0))[0];
                            py.parent(endLocator,endJoint);
                            py.setAttr(endLocator+".t",aimTempArray[0],aimTempArray[1],aimTempArray[2]);
                            py.setAttr(endLocator+".r",0,0,0);
                            if(segmentName == "leg"):
                                potentialAnkle = py.listRelatives(endJoint,type="joint",p=1);
                                if(isinstance(potentialAnkle,list) == 1):
                                    py.parent(endLocator,potentialAnkle[0]);
                        else:
                            endLocator = py.listRelatives(endJoint,type='locator',fullPath=1,ad=1,c=1)[-1].split("|")[-2];
                        #GET OPTIONS BOX
                        optionsBox = controllerIK.replace(controllerIK.split("_")[2],controllerIK.split("_")[2]+"OptionsBox");
                        optionsBoxList.append(optionsBox);
                        #GENERATE PAIRING LISTS
                        poleVectorName = controllerIK.replace("_"+segmentName+"_","_"+segmentName+"PV_");
                        ikPoleVectorList.append(poleVectorName);
                        ikControllerList.append(controllerIK);
                        midJointList.append(midJoint);
                        endJointList.append(endJoint);
                        endLocatorList.append(endLocator);
                        aimArrayList.append(aimArrayIK);
                        upArrayList.append(upArrayIK);
                #CONVERT OUTPUT PROPORTIONS TO INPUT
                if(ii < len(inputTargets[i])-1):
                    parentJoint = py.listRelatives(outputTargets[i][ii+1],type="joint",p=1,s=0)[0];
                    snap1 = py.pointConstraint(inputTargets[i][ii],distanceLocators[0], mo=0, w=1);
                    snap2 = py.pointConstraint(inputTargets[i][ii+1],distanceLocators[1], mo=0, w=1);
                    py.delete(snap1,snap2);
                    distance = py.getAttr(distanceNodeShape+".distance");
                    py.setAttr(endPoint+".tx",distance);
                    snap1 = py.pointConstraint(outputTargets[i][ii],startPoint,mo=0,w=1);
                    snap2 = py.aimConstraint(outputTargets[i][ii+1],startPoint,aim=[1,0,0],u=[0,0,0],wut="none",mo=0,w=1);
                    py.delete(snap1,snap2);
                    offset = py.group(em=1,r=1);
                    snap = py.parentConstraint(outputTargets[i][ii+1],offset,mo=0,w=1);
                    py.delete(snap);
                    py.parent(outputTargets[i][ii+1],offset);
                    py.parent(offset,parentJoint);
                    snap = py.pointConstraint(endPoint,offset,mo=0,w=1);
                    py.delete(snap);
                #ADD CONSTRAINTS
                if not(i > 0 and ii == 0):
                    if("_M_" in inputTargets[i][ii]):
                        aimArray = [0,1,0];
                        upArray = [0,0,1];
                    else:
                        aimArray = [1,0,0] if("_L_" in inputTargets[i][ii]) else [-1,0,0];
                        upArray = [0,0,1] if("_L_" in inputTargets[i][ii]) else [0,0,-1];
                    attributeExists = py.listAttr(outputTargets[i][ii],st=["frontAxis"],r=1);
                    if(override == 1):#(outputTargets[i][ii] == "LeftShoulder" or outputTargets[i][ii] == "RightShoulder") and 
                        if(RiGGiE == False):
                            py.orientConstraint(outputTargets[i][ii],inputTargets[i][ii],l=conLayer,mo=1,w=1);
                        else:
                            py.orientConstraint(outputTargets[i][ii],inputTargets[i][ii],l=conLayer,mo=1,w=1);

                            #newOutputController = outputNameSpace+inputTargets[i][ii].split(":")[-1];
                            #py.orientConstraint(newOutputController,inputTargets[i][ii],l=conLayer,mo=0,w=1);
                    elif(isinstance(attributeExists, list) == 1):
                        #IF MIDDLE JOINT ORIENT INSTEAD OF AIM
                        py.orientConstraint(outputTargets[i][ii],inputTargets[i][ii],l=conLayer,mo=1,w=1);

                    
                    
                    #if(isinstance(attributeExists, list) == 1):
                    #    #IF MIDDLE JOINT ORIENT INSTEAD OF AIM
                    #    py.orientConstraint(outputTargets[i][ii],inputTargets[i][ii],l=conLayer,mo=1,w=1);
                    #elif(override == 1):#(outputTargets[i][ii] == "LeftShoulder" or outputTargets[i][ii] == "RightShoulder") and 
                    #    snapValue = 1 if(RiGGiE == False) else 0;
                    #    py.orientConstraint(outputTargets[i][ii],inputTargets[i][ii],l=conLayer,mo=snapValue,w=1);
                    else:#IF SIDE JOINT
                        axisArrayList = [];
                        aim = py.getAttr(outputTargets[i][ii]+".aimAxis",asString=1);
                        potentialUpAxis = axis[:];
                        potentialUpAxis.remove(aim[0]);
                        iii=0;
                        while(iii < len(potentialUpAxis)):
                            objectUpAIndex = axis.index(potentialUpAxis[iii]);
                            objectUpArray = [];
                            iiii=0;
                            while(iiii < 3):
                                if(iiii == objectUpAIndex):
                                    objectUpArray.append(int(aim[-1]+str(1)));
                                else:
                                    objectUpArray.append(0);
                                iiii+=1;
                            objectUpFlipArray = objectUpArray[:];
                            if(-1 in objectUpFlipArray):
                                index = objectUpFlipArray.index(-1);
                                objectUpFlipArray[index] = 1;
                            else:
                                index = objectUpFlipArray.index(1);
                                objectUpFlipArray[index] = -1;
                            axisArrayList.append(objectUpArray);
                            axisArrayList.append(objectUpFlipArray);
                            iii+=1;
                        iii=0;
                        while(iii < len(axisArrayList) and ii != 0 and (MAX == False or i >= 6)):
                            #FIND AIM AXIS BY CYCLING THROUGH AXIS (TO FIND ONE WITH THE SMALLEST EFFECT ON THE CTRL)
                            snap = py.aimConstraint(outputTargets[i][ii+1],inputTargets[i][ii],aim=aimArray,u=upArray,wu=axisArrayList[iii],wut="objectrotation",wuo=outputTargets[i][ii],l=conLayer,mo=0,w=1);
                            rotations = list(py.getAttr(inputTargets[i][ii]+".r")[0]);
                            total = abs(rotations[0])+abs(rotations[1])+abs(rotations[2]);
                            py.delete(snap);
                            if(iii == 0):
                                smallestRotaions = total;
                                objectUpArray = axisArrayList[iii];
                            if(total < smallestRotaions):
                                smallestRotaions = total;
                                objectUpArray = axisArrayList[iii];
                            iii+=1;
                        #GET OFFSET VALUES IF THEY EXISTS
                        offsetLocator = inputTargets[i][ii].replace(inputTargets[i][ii].split("_")[-3],inputTargets[i][ii].split("_")[-3]+"OffsetFK").replace(inputTargets[i][ii].split("_")[-1],"LOC");
                        if(py.objExists(offsetLocator) == 1):
                            offsetArray = list(py.getAttr(offsetLocator+".r")[0]);
                            iii=0;
                            while(iii < len(offsetArray)):
                                offsetArray[iii] = offsetArray[iii]*-1;
                                iii+=1;
                        else:
                            offsetArray = [0,0,0];
                        if(MAX == False):
                            #IF NOT A MAX RIG
                            py.aimConstraint(outputTargets[i][ii+1],inputTargets[i][ii],aim=aimArray,u=upArray,wu=objectUpArray,wut="objectrotation",wuo=outputTargets[i][ii],offset=offsetArray,l=conLayer,mo=0,w=1);
                        elif any(x in inputTargets[i][ii] for x in digitAppendedNames):
                            #IF A DIGIT (FINGER/TOE) JOINT
                            py.aimConstraint(outputTargets[i][ii+1],inputTargets[i][ii],aim=aimArray,u=upArray,wu=objectUpArray,wut="objectrotation",wuo=outputTargets[i][ii],offset=offsetArray,l=conLayer,mo=0,w=1);
                        else:
                            antiFlipLocator = py.spaceLocator(p=(0,0,0))[0];
                            antiFlipGroup = py.group(r=1);
                            py.parent(antiFlipGroup,inputTargets[i][ii]);
                            py.setAttr(antiFlipGroup+".t",0,0,0);
                            py.setAttr(antiFlipGroup+".r",0,0,0);
                            py.parent(antiFlipGroup,outputTargets[i][ii]);
                            py.orientConstraint(antiFlipLocator,inputTargets[i][ii],l=conLayer,mo=1,w=1);
                ii+=1;
            i+=1;
###############################################################################
#"""# RESET IK LIMB POSITIONS FOR POLEVECTORS                                 #
###############################################################################
        characterStudioJoints = [outputTargets[0][2:-1]+outputTargets[1][1:-1],
                                 ikChainList[0],ikChainList[1],
                                 ikChainList[2],ikChainList[3]];
        i=0;
        if(MAX == True):
            while(i < len(characterStudioJoints) and i < len(characterStudioValues)):
                ii=0;
                while(ii < len(characterStudioJoints[i]) and ii < len(characterStudioValues[i])):
                    py.setAttr(characterStudioJoints[i][ii]+".r",characterStudioValues[i][ii][0],characterStudioValues[i][ii][1],characterStudioValues[i][ii][2]);
                    ii+=1;
                i+=1;
        else:
            while(i < len(ikChainList)):
                ii=0;
                while(ii < len(ikChainList[i])):
                    py.setAttr(ikChainList[i][ii]+".r",0,0,0);
                    ii+=1;
                i+=1;  
###############################################################################
#"""# CONNECT IK CONTROLLERS BASED ON GERATED LISTS                           #
###############################################################################
        py.select(ikControllerList,ikPoleVectorList,r=1);
        py.animLayer(conLayer,aso=1,e=1);
        ikGroupList = [];
        i=0;
        while(i < len(ikControllerList)):
            segmentName = "arm" if ("arm" in ikControllerList[i]) else "leg";
            parentGroup = py.listRelatives(ikControllerList[i],p=1,s=0)[0];
            SAFE = py.listAttr(parentGroup, st=["SAFE"], r=1);
            if(isinstance(SAFE, list) == 1):
                py.setAttr(parentGroup+".SAFE",1);
            py.pointConstraint(endJointList[i],ikControllerList[i],mo=0,w=1);
            #REMOVE AIM AXIS AND ITS REVERSE FROM POSSIBLE UP AXIS LIST
            axisArrayList = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
            reverseAimArrayIK = aimArrayIK[:];
            if(-1 in reverseAimArrayIK):
                index = reverseAimArrayIK.index(-1);
                reverseAimArrayIK[index] = 1;
            elif(1 in reverseAimArrayIK):
                index = reverseAimArrayIK.index(1);
                reverseAimArrayIK[index] = -1;
            axisArrayList.remove(aimArrayIK);
            axisArrayList.remove(reverseAimArrayIK);
            ii=0;
            while(ii < len(axisArrayList)):
                #FIND AIM AXIS BY CYCLING THROUGH AXIS (TO FIND ONE WITH THE SMALLEST EFFECT ON THE CTRL)
                snap = py.aimConstraint(endLocatorList[i],ikControllerList[i],aim=aimArrayList[i],u=upArrayList[i],wut="objectrotation",wuo=endJointList[i],wu=axisArrayList[ii],l=conLayer,mo=0,w=1);
                rotations = list(py.getAttr(ikControllerList[i]+".r")[0]);
                total = abs(rotations[0])+abs(rotations[1])+abs(rotations[2]);
                py.delete(snap);
                if(ii == 0):
                    smallestRotaions = total;
                    objectUpArray = axisArrayList[ii];
                if(total < smallestRotaions):
                    smallestRotaions = total;
                    objectUpArray = axisArrayList[ii];
                ii+=1;
            #SPECIAL CASE: IF MAX RIG, OVERIDE OBJECT UP ARRAY TO BE Z(+/-) BEFORE CONSTRAINING
            if(MAX == True and "L_arm" in ikControllerList[i]):#!
                objectUpArray = [0,-1,0];
            elif(MAX == True and "R_arm" in ikControllerList[i]):#!
                objectUpArray = [0,-1,0];
            if(MAX == True and "L_leg" in ikControllerList[i]):#!
                objectUpArray = [0,1,0];
            elif(MAX == True and "R_leg" in ikControllerList[i]):#!
                objectUpArray = [0,1,0];
                
                
                
            if(MAX == False and "b_L_wrist_v" in endJointList[i]):#!
                objectUpArray = [0,1,0];
            elif(MAX == False and "b_R_wrist_v" in endJointList[i]):#!
                objectUpArray = [0,-1,0];

                
                
            #initialPositionIK = ikControllerList[i].replace(segmentName,segmentName+"InitialPositionIK");
            #upArrayIK = py.getAttr(initialPositionIK+".upAxis", asString=1); 
            #upArrayIK = upArrayIK.split(",");
            #upArrayIK = [int(upArrayIK[0]),int(upArrayIK[1]),int(upArrayIK[2])];
            
            #if(MAX == False):
            #    py.aimConstraint(endLocatorList[i],ikControllerList[i],aim=aimArrayList[i],u=upArrayList[i],wut="objectrotation",wuo=endJointList[i],wu=objectUpArray,l=conLayer,mo=0,w=1);
            #else:
            #    py.aimConstraint(endLocatorList[i],ikControllerList[i],aim=aimArrayList[i],u=upArrayList[i],wut="objectrotation",wuo=endJointList[i],wu=objectUpArray,l=conLayer,mo=0,w=1);
            

            #if(MAX == False):
            #    #IF NOT A MAX RIG
            #    py.aimConstraint(endLocatorList[i],ikControllerList[i],aim=aimArrayList[i],u=upArrayList[i],wut="objectrotation",wuo=endJointList[i],wu=objectUpArray,l=conLayer,mo=0,w=1);
            #if(segmentName == "arm"):
            #    #IF MAX ARM RIG
            #    antiFlipLocator = py.spaceLocator(p=(0,0,0))[0];
            #    antiFlipGroup = py.group(r=1);
            #    py.parent(antiFlipGroup,ikControllerList[i]);
            #    py.setAttr(antiFlipGroup+".t",0,0,0);
            #    py.setAttr(antiFlipGroup+".r",0,0,0);
            #    py.parent(antiFlipGroup,endJointList[i]);
            #    py.orientConstraint(antiFlipLocator,ikControllerList[i],l=conLayer,mo=1,w=1);
                
                

            if(MAX == False and segmentName == "arm"):
                #IF NOT A MAX RIG
                py.aimConstraint(endLocatorList[i],ikControllerList[i],aim=aimArrayList[i],u=upArrayList[i],wut="objectrotation",wuo=endJointList[i],wu=objectUpArray,l=conLayer,mo=0,w=1);
            elif(segmentName == "leg"):
                #IF MAX LEG RIG
                orientationPin = py.spaceLocator(p=(0,0,0))[0];
                snap = py.parentConstraint(ikControllerList[i],orientationPin,mo=1,w=1);
                py.delete(snap);
                potentialHingeEnd = py.listRelatives(endJointList[i],type="joint",p=1);
                if(isinstance(potentialHingeEnd,list) == 1):
                    py.parent(orientationPin,potentialHingeEnd[0]);
                else:
                    py.parent(orientationPin,endJointList[i]);            
                py.setAttr(orientationPin+".t",0,0,0);
                py.orientConstraint(orientationPin,ikControllerList[i],l=conLayer,mo=0,w=1);
            #CONNECT TOES
            if(segmentName == "leg"):
                toeController = ikControllerList[i].replace("leg","toe");
                ballController = ikControllerList[i].replace("leg","ball");
                if(py.objExists(toeController) == 1):
                    potentialToe = py.listRelatives(endJointList[i],type="joint",c=1,s=0)[0];
                    antiFlipLocator = py.spaceLocator(p=(0,0,0))[0];
                    antiFlipGroup = py.group(r=1);
                    py.parent(antiFlipGroup,toeController);
                    py.setAttr(antiFlipGroup+".t",0,0,0);
                    py.setAttr(antiFlipGroup+".r",0,0,0);
                    if(isinstance(potentialToe,list) == 1):
                        py.parent(antiFlipGroup,potentialToe[0]);
                    else:    
                        py.parent(antiFlipGroup,endJointList[i]);
                    py.select(toeController,r=1);
                    py.animLayer(conLayer,aso=1,e=1);
                    py.orientConstraint(antiFlipLocator,toeController,l=conLayer,mo=1,w=1);
            #CONNECT POLEVECTOR
            poleVectorLocator = py.spaceLocator(p=(0,0,0))[0];
            socketIK = py.listRelatives(midJointList[i],p=1,s=0)[0];
            endIK = py.listRelatives(midJointList[i],c=1,s=0);
            endIK = socketIK if(isinstance(endIK,list) == 0) else endIK[0];
            startJoint = py.xform(socketIK, ws=1, t=1, q=1);
            midJoint = py.xform(midJointList[i], ws=1, t=1, q=1);
            endJoint = py.xform(endIK, ws=1, t=1, q=1);
            startJointV = om.MVector(startJoint[0],startJoint[1],startJoint[2]);
            midJointV = om.MVector(midJoint[0] ,midJoint[1], midJoint[2]);
            endJointV = om.MVector(endJoint[0] ,endJoint[1], endJoint[2]);
            startToEndJoints = endJointV - startJointV;
            startJoint2midJoint = midJointV - startJointV;
            dot = startJoint2midJoint * startToEndJoints;
            point = float(dot)/float(startToEndJoints.length());
            startToEndJoints2 = startToEndJoints.normal();
            pointV = startToEndJoints2 * point;
            aimValue = startJoint2midJoint - pointV;
            aimValue *= (50)/10;#!
            finalPosition = midJointV+aimValue;
            py.xform(poleVectorLocator,ws=1,t=(finalPosition.x,finalPosition.y,finalPosition.z));
            #py.parent(poleVectorLocator,socketIK);
            py.parent(poleVectorLocator,midJointList[i]);
            snap = py.pointConstraint(ikPoleVectorList[i],poleVectorLocator, mo=0, w=1);
            py.delete(snap);
            py.pointConstraint(poleVectorLocator,ikPoleVectorList[i],l=conLayer,mo=1,w=1);
            #py.pointConstraint(poleVectorLocator,ikPoleVectorList[i],l=conLayer,mo=0,w=1);
            i+=1;
        py.delete(distanceNode,distanceLocators,startPoint);
###############################################################################
#"""# FINALIZE                                                                #
###############################################################################
        if(override == 0 or RiGGiE == True):
            py.delete(centerAlignment, sideTracker, base);
        print log
        return [ikControllerList,optionsBoxList,root];
