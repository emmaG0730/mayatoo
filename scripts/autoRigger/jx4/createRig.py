###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import os
import maya.cmds as py
import maya.mel as mel 
import maya.OpenMaya as om
import pymel.core as pm
from pymel.core.runtime import FrameSelected;
###############################################################################
#.............................................................................#
#.............................................................................#
#"""# CREATES A LIMB RIG                                                      #
#.............................................................................#
#.............................................................................#
###############################################################################
def limb(style,posture):
    axis = ["x","y","z"];
    armRotationOrder = "zyx"
    legRotationOrder = "zyx"
    clavicleRotationOrder="xzy";
    initialJointSelection = py.ls(sl=1, type="joint");
    if(isinstance(initialJointSelection, list) == 1):
        py.select(hi=1, r=1);
        initialSelectionHierarchy = py.ls(sl=1, type="joint");
    if(len(initialSelectionHierarchy) >= 4):
        switchSpaceCalculator = "c_M_spaceSwitchCalculator_v1_PMA";
###############################################################################
#"""# CHECKS THE LIMB TYPE, POSITION AND VERSION OF THE JOIN CHAIN            #
###############################################################################
        limbJoints = [];
        fingerJoints = [];
        wristJoint = "none";
        clavicle = "none";
        toeName = "none";
        clavicleName = "clavicle";
        armPose = "A";
        newJoints = py.duplicate(initialSelectionHierarchy, rc=1, rr=1);
        firstPosition = py.xform(newJoints[0],q=1,t=1,ws=1);
        secondPosition = py.xform(newJoints[1],q=1,t=1,ws=1);
        thirdPosition = py.xform(newJoints[2],q=1,t=1,ws=1);
        distance = [];
        i=0;
        while(i < len(firstPosition)):
            distance.append(abs(abs(firstPosition[i]) - abs(secondPosition[i])));
            i+=1;
        if(distance[0] > distance[1]/5 and posture == "biped"):
            section = ["shoulder", "elbow", "wrist", "palm", "arm"];
        elif(posture == "biped"):
            section = ["hip", "knee", "ankle", "ball", "toe", "leg"];  
        elif(firstPosition[2] > 0 and posture == "quadruped"):
            section = ["elbow", "knee", "frontFetlock", "frontCoronet", "frontHoof", "frontLeg"];
        elif(posture == "quadruped"):
            section = ["stifle", "hock", "hindFetlock", "hindCoronet", "hindHoof", "hindLeg"];  
        side = "L" if(py.xform(newJoints[0],q=1,t=1,ws=1)[0]>0) else "R"; 
        reverse = -1 if(side == "R") else 1;
        counterReverse = -1 if(side == "R" and section[-1] != "leg") else 1;
        version = 1;
        while(py.objExists("c_"+side+"_"+section[0]+"_v"+str(version)+"_CTRL")):
            version += 1;   
        parentJoint = py.listRelatives(newJoints[0], p=1);
        if(isinstance(parentJoint, list) == 1):
            py.parent(newJoints[0], w=1);
        i=0;    
        while(i < len(newJoints)):
            py.makeIdentity(newJoints[i], apply=1, r=1, n=0);
            i+=1;     
        if(section[-1] == "arm" and round(secondPosition[1],0) == round(thirdPosition[1],0)):
            armPose = "T";
        if(posture == "biped"):
            wristIndex = 2;ankleIndex = 2;ballIndex = 3;endIndex = wristIndex;
        elif(posture == "quadruped"):
            wristIndex = 2;ankleIndex = 2;ballIndex = 3;endIndex = wristIndex;
###############################################################################
#"""# ORIENTS THE ANKLE TO AIM FORWARD                                        #
############################################################################### 
        if(section[-1] != "arm" and posture == "biped"):
            footAimLocator = py.spaceLocator(p=(0,0,0))[0];
            snap = py.pointConstraint(newJoints[ballIndex], footAimLocator, mo=0, w=1);
            py.delete(snap);
            snap = py.pointConstraint(newJoints[ankleIndex], footAimLocator, skip=["x","z"], mo=0, w=1);
            py.delete(snap);
            ankleGroup = py.group(em=1); 
            snap1 = py.pointConstraint(newJoints[ankleIndex], ankleGroup, mo=0, w=1);
            snap2 = py.aimConstraint(footAimLocator,ankleGroup,aim=(0,0,1),u=(0,1,0),wut="scene",mo=0,w=1);
            py.delete(snap1,snap2);
            py.parent(newJoints[ankleIndex],ankleGroup);
            py.setAttr(ankleGroup+".r",0,0,0);
            py.parent(newJoints[ankleIndex],newJoints[ankleIndex-1]);
            py.delete(ankleGroup,footAimLocator);
###############################################################################
#"""# FINDS CLAVICLE, SHOULDER, ELBOW, WRIST AND FINGERS IF LIMB IS AN ARM    #
############################################################################### 
        i=0;
        while(i < len(newJoints) and section[-1] == "arm"):
            children = py.listRelatives(newJoints[i], c=1);
            if(isinstance(children,list) == 1 and len(children) > 1):
                wristJoint = newJoints[i];
                limbJoints.append(newJoints[i]);
            if(isinstance(children,list) == 1 and len(children) == 1):
                parents = py.ls(newJoints[i], long=1)[0].split("|")[1:-1];
                if(isinstance(parents,list) == 1):
                    if any(i in wristJoint for i in parents):
                        subParents = py.ls(newJoints[i], long=1)[0].split("|")[1:-1];
                        if not any(i in subParents for i in fingerJoints):
                            fingerJoints.append(newJoints[i]);
                    else:
                        limbJoints.append(newJoints[i]);  
            if(i == len(newJoints)-1):
                limbJoints.append(py.listRelatives(limbJoints[-1], c=1)[0]);
            i+=1; 
        if(section[-1] == "arm"):
            if(len(fingerJoints) > 0):
                py.select(fingerJoints[:], hi=1, r=1);
                allFingerJoints = py.ls(sl=1, type="joint");
                allFingerJoints.remove(limbJoints[-1]);
                newJoints = [x for x in newJoints if x not in allFingerJoints];
                py.parent(fingerJoints, w=1);
            if(len(limbJoints) >= 5):
                newJoints.remove(newJoints[0]);
                clavicle = limbJoints[0];
                limbJoints = newJoints;#ADDED TO ENSURE ELBOW OFFSET IS FIXED!
        elif(posture == "quadruped"):
            clavicle = newJoints[0];
            newJoints.remove(newJoints[0]);
            limbJoints = newJoints;  
        else:
            limbJoints = newJoints;   
###############################################################################
#"""# INDEPENDENTLY ZEROES OUT EACH JOINT TO AVOID FUTURE OFFSET ISSUES	      #
###############################################################################
        if(posture == "biped"):
            targetLocator = py.spaceLocator(p=(0,0,0))[0];
            upLocator = py.spaceLocator(p=(0,0,0))[0];
            py.setAttr(upLocator+".ty", 10);
            py.parent(upLocator, targetLocator);
            snap = py.pointConstraint(limbJoints[1], targetLocator, mo=0, w=1);
            py.delete(snap);
            py.parent(targetLocator, limbJoints[0]);
            py.setAttr(targetLocator+".r", 0,0,0);
            py.parent(targetLocator, w=1);
            py.setAttr(limbJoints[0]+".r", 0,0,0);
            py.setAttr(limbJoints[0]+".jo", 0,0,0);
            aimValue = 1 if(py.getAttr(limbJoints[1]+".tx") > 0) else -1; 
            upValue = 1 if(py.getAttr(limbJoints[1]+".tx") > 0 and section[-1] == "arm") else -1;
            if(section[-1] == "arm"):
                snap = py.aimConstraint(targetLocator,limbJoints[0],aim=(aimValue,0,0),u=(0,upValue,0),wut="scene",mo=0,w=1);
            else:
                snap = py.aimConstraint(targetLocator,limbJoints[0],aim=(aimValue,0,0),u=(0,1,0),wu=(0,1,0),wut="objectrotation",wuo=upLocator,mo=0,w=1);
            py.delete(snap, targetLocator);
            i=0;
            while(i < len(limbJoints)):
                py.makeIdentity(limbJoints[i], apply=1, r=1, n=0);
                i+=1; 
###############################################################################
#"""# MEASURE JOINT LENGTHS                                                   #
###############################################################################
        distanceNodeShape = py.distanceDimension(sp=(0, 100, 0), ep=(0, 10, 0));
        distanceLocators = py.listConnections(distanceNodeShape);
        distanceNode = py.listRelatives(distanceNodeShape, p=1);
        jointLengths = [];
        i=0;
        while(i < len(limbJoints)-1):
            snap = py.pointConstraint(limbJoints[i],distanceLocators[0], mo=0, w=1);
            py.delete(snap);
            snap = py.pointConstraint(limbJoints[i+1],distanceLocators[1],mo=0,w=1);
            py.delete(snap);
            currentMeasurement = py.getAttr(distanceNodeShape+".distance");
            jointLengths.append(currentMeasurement);
            i+=1;        
        py.delete(distanceNode, distanceLocators);
        controllerSize = jointLengths[0]/2.5 if(section[-1] == "arm") else jointLengths[0]/3;
###############################################################################
#"""# REORIENT JOINTS                                                         #
###############################################################################
        if(section[-1] == "arm"):
            jointRadius = py.getAttr(newJoints[-1]+".radius");
            tipJoint = py.joint(radius=jointRadius);
            snap = py.parentConstraint(newJoints[-2],tipJoint,mo=0,w=1);
            py.delete(snap);
            if(fingerJoints == []):
                py.delete(newJoints[-1]);
            py.parent(tipJoint,newJoints[-2]);
            if(clavicle == "none" and posture != "quadruped"):
                py.setAttr(tipJoint+".tx", jointLengths[-1]*reverse);
            else:
                py.setAttr(tipJoint+".tx", jointLengths[-2]*reverse);
            newJoints.remove(newJoints[-1]);py.makeIdentity(tipJoint,apply=1,r=1,n=0);
            newJoints.append(tipJoint); 
        if(side == "L"):
            if(clavicle == "none" or posture == "quadruped"):
                if(section[-1] == "arm"):
                    py.joint(newJoints[0],e=1,oj="xyz",secondaryAxisOrient="yup",ch=1,zso=1);
                else:
                    py.joint(newJoints[0],e=1,oj="xzy",secondaryAxisOrient="zup",ch=1,zso=1);
                    py.joint(newJoints[3],e=1, oj="xyz", secondaryAxisOrient="xup", ch=1, zso=1);
            else:
                py.joint(clavicle,e=1,oj="xyz",secondaryAxisOrient="yup",ch=1,zso=1);
        elif(side == "R"):
            if(clavicle == "none" or posture == "quadruped"):
                newJointsMirrored = py.mirrorJoint(newJoints[0], mirrorYZ=1, mirrorBehavior=1);
                py.delete(newJoints);
                if(section[-1] == "arm"):
                    py.joint(newJointsMirrored[0],e=1,oj="xyz",secondaryAxisOrient="yup",ch=1,zso=1);
                else:
                    py.joint(newJointsMirrored[0],e=1,oj="xzy",secondaryAxisOrient="zup",ch=1,zso=1);
                    py.joint(newJointsMirrored[3],e=1, oj="xyz", secondaryAxisOrient="xup", ch=1, zso=1);
                newJoints = py.mirrorJoint(newJointsMirrored[0], mirrorYZ=1, mirrorBehavior=1);
                py.delete(newJointsMirrored);
            else:
                newJointsMirrored = py.mirrorJoint(clavicle, mirrorYZ=1, mirrorBehavior=1);
                py.delete(clavicle);
                if(section[-1] == "arm"):
                    py.joint(newJointsMirrored[0],e=1,oj="xyz",secondaryAxisOrient="yup",ch=1,zso=1);
                else:
                    py.joint(newJointsMirrored[0],e=1,oj="xzy",secondaryAxisOrient="zup",ch=1,zso=1);
                    py.joint(newJointsMirrored[3],e=1, oj="xyz", secondaryAxisOrient="xup", ch=1, zso=1);
                newJoints = py.mirrorJoint(newJointsMirrored[0], mirrorYZ=1, mirrorBehavior=1);
                clavicle = newJoints[0];py.delete(newJointsMirrored);
                newJoints = newJoints[1:];
        py.setAttr(newJoints[1]+".jointOrientX", 0);       
###############################################################################
#"""# RENAME JOINT CHAINS                                                     #
###############################################################################
        bindJointChain = [];
        i = len(newJoints);
        while(i > 0):
            name = "b_"+side+"_"+section[i-1]+"_v"+str(version)+"_JNT";
            newName = py.rename(newJoints[i-1], name);
            bindJointChain.append(newName);
            i-=1;
        bindJointChain.reverse();
        newJoints = py.duplicate(bindJointChain, rc=1, rr=1);
        jointChain = [];
        i = len(newJoints);
        while(i > 0):
            name = "c_"+side+"_"+section[i-1]+"_v"+str(version)+"_JNT";
            newName = py.rename(newJoints[i-1], name);
            #py.setAttr(newName+".radius",0);
            py.setAttr(newName+".drawStyle",2);
            jointChain.append(newName);
            i-=1;
        jointChain.reverse();
        #TWIST JOINTS ADDED WITH SUB JOINTS
        twistJoints = py.duplicate(bindJointChain, rc=1, rr=1);
        twistJointChain = [];
        i = len(twistJoints);
        while(i > 0):
            name = "c_"+side+"_"+section[i-1]+"Twist_v"+str(version)+"_JNT";
            newName = py.rename(twistJoints[i-1], name);
            py.setAttr(newName+".radius",3);#py.setAttr(newName+".drawStyle",2);
            twistJointChain.append(newName);
            i-=1;
        twistJointChain.reverse();
        i=0;
        while(i < len(twistJointChain)):
            children = py.listRelatives(twistJointChain[i],type="joint",c=1,s=0);
            if(isinstance(children,list) == 1):
                py.parent(children[:],w=1);
            if(isinstance(children,list) == 1):
                py.parent(children[:],twistJointChain[i]);
            i+=1;
        py.delete(initialJointSelection);
###############################################################################
#"""# CREATE MATERIAL                                                         #
###############################################################################
        MAT = [side+str(section[len(section)-1]).upper()+str(version)+"_MAT"];
        i=0;
        while(i < len(MAT)):
            if(py.objExists(MAT[i]) == 0):
                ctrlShader = py.shadingNode("blinn", asShader=1, n=MAT[i]);
                shadingGRP = py.sets(renderable=1,noSurfaceShader=1,empty=1);
                py.connectAttr('%s.outColor'%ctrlShader,'%s.surfaceShader'%shadingGRP);
                py.setAttr(MAT[i]+".incandescence", 0,0,0);
                py.setAttr(MAT[i]+".color", 0,0.1777/3,0.4421/3);
                py.setAttr(MAT[i]+".ambientColor", 0,0.1777,0.4421);
                py.setAttr(MAT[i]+".diffuse", 1.0);
                py.setAttr(MAT[i]+".transparency", 0,0,0);
                py.setAttr(MAT[i]+".translucenceDepth",0);
                py.setAttr(MAT[i]+".translucenceFocus",0);
                py.setAttr(MAT[i]+".reflectivity",0);
                py.setAttr(MAT[i]+".eccentricity",0);
                py.setAttr(MAT[i]+".specularRollOff",0);
                py.setAttr(MAT[i]+".specularColor",0,0,0);
                py.setAttr(MAT[i]+".ihi", 0);
                py.disconnectAttr(MAT[i]+".msg", "defaultShaderList1.s", na=1);
            i+=1;
###############################################################################
#"""# CREATE CONTROLLERS                                                      #
###############################################################################
        controllers = [];
        shapes = [];
        counterGroups = [];
        groups = [];
        i=0;
        while(i < len(jointChain)-1):
            name = "c_"+side+"_"+section[i]+"_v"+str(version)+"_CTRL";
            controller = py.polyCube(n=name, h=abs(controllerSize), d=abs(controllerSize), ax=(0,1,0), cuv=4, ch=1)[0];
            shapes.append(py.listConnections(controller+"Shape")[-1]);
            py.setAttr(controller+"Shape.ihi",0);
            name = "c_"+side+"_"+section[i]+"Counter_v"+str(version)+"_GRP";
            counterGroup = py.group(n=name, r=1);
            name = "c_"+side+"_"+section[i]+"_v"+str(version)+"_GRP";
            controllerGroup = py.group(n=name, r=1);
            py.move(-0.5,0,0, controller+".sp", r=1);
            py.setAttr(controller+".sptx", 0.5);
            attributes = [".primaryVisibility",".castsShadows",".receiveShadows",
                          ".visibleInReflections",".holdOut",".smoothShading",
                          ".motionBlur",".visibleInRefractions",".doubleSided",
                          ".opposite"];
            ii=0;              
            while(ii < len(attributes)):
                py.setAttr(controller+"Shape"+attributes[ii], 0);
                ii+=1;
            #CREATE CLAVICLE CONTROLLER
            clavicleController = "none";
            if(i == len(jointChain)-2 and clavicle != "none"):
                if(section[-1] == "arm"):
                    clavicleName = "clavicle"
                else:
                    clavicleName = "hip" if(section[-1] == "hindLeg") else "shoulder";
                duplicateControllerGroup = py.duplicate(controllerGroup,rc=1,rr=1)[0];
                py.select(duplicateControllerGroup, hi=1, r=1);
                clavicleSet = py.ls(sl=1);
                name = "c_"+side+"_"+clavicleName+"_v"+str(version)+"_GRP";
                clavicleGroup = py.rename(clavicleSet[0], name);
                name = "c_"+side+"_"+clavicleName+"Counter_v"+str(version)+"_GRP";
                clavicleCounterGroup = py.rename(clavicleSet[1], name);
                name = "c_"+side+"_"+clavicleName+"_v"+str(version)+"_CTRL";
                clavicleController = py.rename(clavicleSet[2], name);
                py.setAttr(clavicleController+".overrideEnabled", 1);
                py.setAttr(clavicleGroup+".sx", jointLengths[-1]*reverse);
                py.makeIdentity(clavicleGroup, pn=1, a=1, s=1, n=0);
                snap = py.parentConstraint(clavicle,clavicleGroup,mo=0,w=1);
                py.delete(snap);py.xform(clavicleController, p=1, roo=clavicleRotationOrder);
                name = "b_"+side+"_"+clavicleName+"_v"+str(version)+"_JNT";
                clavicleJoint = py.rename(clavicle, name);
                name = clavicleJoint.replace(clavicleJoint.split("_")[-1], "ONT");
                clavicleConstraint = py.orientConstraint(clavicleController,clavicleJoint,n=name,mo=1,w=1)[0];
                py.setAttr(clavicleConstraint+".ihi", 0);
            py.setAttr(controllerGroup+".sx",jointLengths[i]*reverse);
            py.makeIdentity(controllerGroup, pn=1, a=1, s=1, n=0);#FREEZE
            py.setAttr(controller+".overrideEnabled", 1);
            #FLATTEN FK ANKLE ORIENTATION
            if not(section[-1] != "arm" and i == ankleIndex):
                #IF NOT A LEG'S ANKLE CONTROLLER...
                snap = py.parentConstraint(jointChain[i],controllerGroup,mo=0,w=1);
                py.delete(snap);
            else:
                #IF A LEG'S ANKLE CONTROLLER CREATE AN ANKLE OFFSET
                snap1 = py.pointConstraint(jointChain[i],controllerGroup,mo=0,w=1);
                name = "c_"+side+"_"+section[i]+"OffsetFK_v"+str(version)+"_LOC";
                ankleOffsetFK = py.spaceLocator(p=(0,0,0),n=name)[0];
                aim = py.spaceLocator(p=(0,0,0))[0];
                snap2 = py.pointConstraint(controllerGroup,ankleOffsetFK,mo=0,w=1);
                snap3 = py.pointConstraint(controllerGroup,aim,mo=0,w=1);
                py.setAttr(aim+".ty", (py.getAttr(aim+".ty")*10));
                snap4 = py.aimConstraint(aim,controllerGroup,aim=(0,0,1*reverse),u=(0,1,0),wu=(1,0,0),wut="objectrotation",wuo=ankleOffsetFK,mo=0,w=1);
                py.delete(aim,snap1,snap2,snap3,snap4);
                py.parent(ankleOffsetFK,jointChain[i]);
                py.setAttr(ankleOffsetFK+".r",0,0,0);
                py.parent(ankleOffsetFK,controller);
                py.setAttr(ankleOffsetFK+".v",0);
                #IK LOCATOR (FOR MATCHING)
                name = "c_"+side+"_"+section[i]+"OffsetIK_v"+str(version)+"_LOC";
                ankleOffsetIK = py.spaceLocator(p=(0,0,0),n=name)[0];
                py.parent(ankleOffsetIK,controller);
                py.setAttr(ankleOffsetIK+".t",0,0,0);py.setAttr(ankleOffsetIK+".r",0,0,0);
                py.parent(ankleOffsetIK,jointChain[i]);
                py.setAttr(ankleOffsetIK+".v",0);
                if(side == "L"):
                    py.setAttr(controller+".sptx", jointLengths[i]/-3);#!
                    py.setAttr(controller+".sptz", jointLengths[i]/-6);#!
                else:
                    py.setAttr(controller+".sptx", jointLengths[i]/3);#!
                    py.setAttr(controller+".sptz", jointLengths[i]/6);#!
                py.makeIdentity(controller, a=1, pn=1, n=0);#FREEZE
            #ROTATE FK BALL BOX CONTROLLER
            if(section[-1] == "leg" and i == ballIndex and posture == "biped"):
                py.setAttr(controller+".ray",-90);
                if(side == "L"):
                    py.setAttr(controller+".sptz", jointLengths[i]/-2);
                else:
                    py.setAttr(controller+".sptz", jointLengths[i]/2);
                py.makeIdentity(controller, a=1, pn=1, n=0);#FREEZE
            #ADD TO HIERARCHY AND LISTS
            if(i > 0):
                py.parent(controllerGroup, controllers[-1]);
            controllers.append(controller);
            counterGroups.append(counterGroup);
            groups.append(controllerGroup);
            i+=1;
###############################################################################
#"""# LOCK SETTINGS WITH ATTRIBUTE VALUES                                     #
###############################################################################
        py.addAttr(controllers[endIndex], ln="ON", at="long", min=1, max=1, dv=1);
        py.setAttr(controllers[endIndex]+".ON", l=1);
        py.addAttr(controllers[endIndex], ln="OFF", at="long", min=0, max=0, dv=0);
        py.setAttr(controllers[endIndex]+".OFF", l=1);
        i=0;
        while(i < len(controllers)):
            ii=0;                    
            while(ii < len(attributes)):
                py.connectAttr(controllers[endIndex]+".OFF", controllers[i]+attributes[ii]);
                ii+=1;
            i+=1;  
###############################################################################
#"""# IK SETUP                                                                #
###############################################################################
        controllerListIK = [];
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_IK";
        primaryIK = py.ikHandle(n=name, sj=jointChain[0], ee=jointChain[endIndex], sol="ikRPsolver", shf=1, s="sticky")[0];
        solverIK = py.listConnections(primaryIK, type="ikSolver")[0];
        py.setAttr(solverIK+".ihi", 0);
        name = "c_"+side+"_"+section[-1]+"PivotHandleV3_v"+str(version)+"_GRP";
        handlePivotV3 = py.group(n=name, em=1);
        name = "c_"+side+"_"+section[-1]+"PivotHandleV2_v"+str(version)+"_GRP";
        handlePivotV2 = py.group(n=name, r=1);
        name = "c_"+side+"_"+section[-1]+"PivotHandleV1_v"+str(version)+"_GRP";
        handlePivotV1 = py.group(n=name, r=1);
        name = "c_"+side+"_"+section[-1]+"Handle_v"+str(version)+"_GRP";
        handleGroup = py.group(n=name, r=1);
        py.select(jointChain[0], hi=1, r=1);
        effectors = py.ls(type="ikEffector");
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_EF";
        primaryEffector = py.rename(effectors[0], name);
        if(section[-1] == "arm"):
            #ORIENT BIPED ARM IK CONTROLLER
            snap1 = py.pointConstraint(jointChain[wristIndex], handleGroup, mo=0, w=1);
            up = py.spaceLocator(p=(0,0,0))[0];
            aim = py.spaceLocator(p=(0,0,0))[0];
            aimGroup = py.group(em=1);py.parent(up,aim,aimGroup);
            snap2 = py.parentConstraint(jointChain[wristIndex], aimGroup, mo=0, w=1);
            if(armPose == "A"):
                py.setAttr(aim+".tx", -10*reverse);
                py.setAttr(up+".ty", 10);
                snap3 = py.aimConstraint(aim,handleGroup,aim=(0,1,0),u=(1,0,0),wu=(1,0,0),wut="object",wuo=up,mo=0,w=1);
            else:#TPOSE
                py.setAttr(aim+".tx", 10);
                py.setAttr(up+".ty", 10*reverse);
                snap3 = py.aimConstraint(aim,handleGroup,aim=(1,0,0),u=(0,1,0),wu=(0,1,0),wut="object",wuo=up,mo=0,w=1);
            py.delete(aimGroup,snap1,snap2,snap3);
        elif(posture == "quadruped"):
            #ORIENT QUADRUPED LEG IK CONTROLLER
            snap1 = py.pointConstraint(jointChain[endIndex], handleGroup, mo=0, w=1);
            up = py.spaceLocator(p=(0,0,0))[0];
            aim = py.spaceLocator(p=(0,0,0))[0];
            aimGroup = py.group(em=1);py.parent(up,aim,aimGroup);
            snap2 = py.pointConstraint(jointChain[endIndex], aimGroup, mo=0, w=1);
            snap3 = py.pointConstraint(jointChain[ballIndex], aim, mo=0, w=1);
            py.delete(snap3);
            snap3 = py.pointConstraint(jointChain[endIndex], aim, skip=["x","z"],mo=0, w=1);
            py.setAttr(up+".ty", 10);
            snap4 = py.aimConstraint(aim,handleGroup,aim=(0,0,1),u=(0,1,0),wu=(0,1,0),wut="object",wuo=up,mo=0,w=1);
            py.delete(aimGroup,snap1,snap2,snap3,snap4);
        else:
            #ORIENT BIPED LEG IK CONTROLLER (OR ANYTHING ELSE)
            snap1 = py.pointConstraint(jointChain[ballIndex], handleGroup, mo=0, w=1);
            up = py.spaceLocator(p=(0,0,0))[0];
            aim = py.spaceLocator(p=(0,0,0))[0];
            aimGroup = py.group(em=1);py.parent(up,aim,aimGroup);
            snap2 = py.pointConstraint(jointChain[ballIndex], aimGroup, mo=0, w=1);
            snap3 = py.pointConstraint(jointChain[-1], aim, mo=0, w=1);
            py.setAttr(up+".ty", 10);
            snap4 = py.aimConstraint(aim,handleGroup,aim=(0,0,1),u=(0,1,0),wu=(0,1,0),wut="object",wuo=up,mo=0,w=1);
            py.delete(aimGroup,snap1,snap2,snap3,snap4);
        py.parent(primaryIK,handleGroup);
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_CTRL";
        controllerIK = py.group(n=name, em=1);
        if(section[-1] == "arm" or posture == "quadruped"):
            snap = py.pointConstraint(bindJointChain[endIndex], controllerIK, mo=0, w=1);
        else:
            snap = py.pointConstraint(bindJointChain[ballIndex], controllerIK, mo=0, w=1);
        py.delete(snap);py.parent(controllerIK, handlePivotV3);
        py.setAttr(controllerIK+".r", 0,0,0);
        if(section[-1] == "arm"):
            name = primaryIK.replace(primaryIK.split("_")[-1], "PNT");
            constraint = py.pointConstraint(controllerIK,primaryIK,n=name,mo=1,w=1);
            py.setAttr(constraint[0]+".ihi", 0);
        py.setAttr(controllerIK+".r", 0,0,0);
        py.setAttr(primaryIK+".r", 0,0,0);
        py.setAttr(primaryEffector+".hiddenInOutliner", 1);
        #py.setAttr(primaryIK+".hiddenInOutliner", 1);
        py.setAttr(primaryIK+".overrideEnabled", 1);
        py.setAttr(primaryIK+".overrideLevelOfDetail", 1);
        py.connectAttr(controllerIK+".rotateOrder",primaryIK+".rotateOrder");
        py.connectAttr(controllerIK+".rotateOrder",groups[endIndex]+".rotateOrder");
        py.setAttr(primaryIK+".v", 0);
        #CONSTRAIN IK TO END JOINT
        if(section[-1] == "arm"):#!
            #CREATE IK WRIST OFFSET (IN IK WRIST JOINT'S POSITION)
            name = "c_"+side+"_"+section[-1]+"MatchIK_v"+str(version)+"_LOC";
            matchIK = py.spaceLocator(p=(0,0,0),n=name)[0];
            py.setAttr(matchIK+".v",0);
            name = "c_"+side+"_"+section[-1]+"MatchIK_v"+str(version)+"_GRP";
            matchGroupIK = py.group(n=name);
            snap = py.parentConstraint(jointChain[endIndex],matchGroupIK,mo=0,w=1);
            py.delete(snap);
            py.parent(matchGroupIK,controllerIK);
            name = jointChain[endIndex].replace(jointChain[endIndex].split("_")[-1], "ONT");
            constraint = py.orientConstraint(matchIK,jointChain[endIndex],n=name,mo=1,w=1);
        else:#!
            name = jointChain[endIndex].replace(jointChain[endIndex].split("_")[-1], "ONT");
            constraint = py.orientConstraint(controllerIK,jointChain[endIndex],n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        attributes = py.listAttr(controllerIK, k=1);
        controllerListIK.append(controllerIK);
###############################################################################
#"""# COLOR OPTIONS                                                           #
###############################################################################
        colorOptions = "RED:BLUE:GREEN:YELLOW:PURPLE:ORANGE:TEAL:BLACK:WHITE:"
        primaryColors = [4,15,23,25,8,12,28,1,3];#0-31
        secondaryColors = [13,29,19,17,30,24,19,2,16];#0-31
        colorValues = [[0.7971,0,0],[0,0.1777,0.4421],[0.0506,1,0.0506],
                       [1,0.9988,0],[0.1949,0.0123,0.1478],[0.9567,0.4601,0],
                       [0,1,0.6006],[0.01,0.01,0.01],[1,1,1]];         
        colorOptionsAmount = colorOptions.split(":")[:-1];
        py.addAttr(primaryIK, ln="RIG", at="enum", en="TRADITIONAL:HYBRID:", dv=1);
        py.addAttr(primaryIK, ln="GIR", at="enum", en="HYBRID:TRADITIONAL:", dv=0);
        py.addAttr(primaryIK, ln="GUIDE", at="enum", en="OFF:ON:", dv=0);
        py.addAttr(primaryIK, ln="COLOR", at="enum", en=colorOptions, dv=1);
        py.addAttr(primaryIK, ln="firstCOLOR", at="long", min=0, max=31, dv=1);
        py.addAttr(primaryIK, ln="secondCOLOR",at="long", min=0, max=31, dv=1);
        py.setAttr(primaryIK+".COLOR", k=1, e=1);
        py.setAttr(primaryIK+".firstCOLOR", k=1, e=1);
        py.setAttr(primaryIK+".secondCOLOR", k=1, e=1);
        py.setAttr(primaryIK+".COLOR", k=1, e=1);
        py.setDrivenKeyframe(primaryIK+".GIR",   cd=primaryIK+".RIG");
        py.setAttr(primaryIK+".RIG",0);py.setAttr(primaryIK+".GIR",1);
        py.setDrivenKeyframe(primaryIK+".GIR",   cd=primaryIK+".RIG");
        i=0;
        while(i < len(colorOptionsAmount)):
            index = ["R","G","B"];
            py.setAttr(primaryIK+".COLOR",i);
            py.setAttr(primaryIK+".firstCOLOR",primaryColors[i]);
            py.setDrivenKeyframe(primaryIK+".firstCOLOR",cd=primaryIK+".COLOR");
            py.setAttr(primaryIK+".secondCOLOR",secondaryColors[i]);
            py.setDrivenKeyframe(primaryIK+".secondCOLOR",cd=primaryIK+".COLOR");
            ii=0;
            while(ii < len(colorValues[i])):
                targetColor = MAT[0]+".color"+index[ii];
                targetIncandescence = MAT[0]+".ambientColor"+index[ii];
                py.setAttr(targetColor,colorValues[i][ii]);
                py.setAttr(targetIncandescence,colorValues[i][ii]/3);
                py.setDrivenKeyframe(targetColor,cd=primaryIK+".COLOR");
                py.setDrivenKeyframe(targetIncandescence,cd=primaryIK+".COLOR");
                ii+=1;
            i+=1;
###############################################################################
#"""# CREATE OPTIONS BOX                                                      #
###############################################################################
        name = "c_"+side+"_"+section[-1]+"OptionsBox_v"+str(version)+"_CTRL";
        optionsBox = py.polyCube(n=name, w=abs(controllerSize/5), h=abs(controllerSize/5), d=abs(controllerSize/5), ax=(0,1,0), cuv=4, ch=1)[0];
        name = "c_"+side+"_"+section[-1]+"OptionsBox_v"+str(version)+"_GRP";
        optionsBoxGroup = py.group(n=name, r=1);
        py.setAttr(optionsBox+"Shape.ihi",0);
        py.setAttr(optionsBox+"Shape.overrideEnabled", 1);
        py.setAttr(optionsBox+"Shape.overrideShading", 0);
        py.setAttr(optionsBox+"Shape.overrideTexturing", 0);
        py.connectAttr(primaryIK+".secondCOLOR",optionsBox+"Shape.overrideColor");
        py.setAttr(optionsBox+"Shape.overrideDisplayType", 0);
        py.connectAttr(optionsBox+".overrideDisplayType",optionsBox+"Shape.overrideDisplayType");
        poleVectorShape = py.duplicate(optionsBox);
        py.setAttr(optionsBox+"Shape.hideOnPlayback", 1);
        py.setAttr(optionsBox+".ty", controllerSize/1.25*reverse);
        py.makeIdentity(optionsBox, a=1, t=1, n=0);#FREEZE
        if(section[-1] == "arm"):
            name = optionsBox.replace("CTRL","GRID");
            optionsGrid = py.duplicate(optionsBox, n=name)[0];
            py.setAttr(optionsGrid+".template", 1);
            py.setAttr(optionsGrid+".ty", controllerSize/-10*reverse);
            py.setAttr(optionsGrid+".s", controllerSize/2.05,0,controllerSize/2.05);
        py.setAttr(optionsBox+".ty",l=1,k=0);py.setAttr(optionsBox+".ty",cb=0);
        if(section[-1] == "arm"): 
            py.transformLimits(optionsBox,tx=(controllerSize/-2.25,controllerSize/2.25),etx=(1,1));
            py.transformLimits(optionsBox,tz=(controllerSize/-2.25,controllerSize/2.25),etz=(1,1));
        else:
            py.transformLimits(optionsBox,tx=(0,0),etx=(1,1));
            py.transformLimits(optionsBox,tz=(0,0),etz=(1,1));
        py.connectAttr(primaryIK+".GIR",optionsBoxGroup+".v");
###############################################################################
#"""# ADD OPTIONS BOX ATTRIBUTES                                              #
###############################################################################
        py.addAttr(optionsBox, ln="MODE", at="double", min=0, max=1, dv=0);
        py.setAttr(optionsBox+".MODE", k=1, e=1);
        py.addAttr(optionsBox+"Shape", ln="FLIP", at="double", min=0, max=1, dv=1);
        py.setDrivenKeyframe(optionsBox+"Shape.FLIP", cd=optionsBox+".MODE");
        py.setAttr(optionsBox+".MODE",1);py.setAttr(optionsBox+"Shape.FLIP",0);  
        py.setDrivenKeyframe(optionsBox+"Shape.FLIP", cd=optionsBox+".MODE");
        py.addAttr(optionsBox+"Shape", ln="FK", at="enum", en="OFF:ON:", dv=1);
        py.setAttr(optionsBox+"Shape.FK", k=1, e=1);
        py.addAttr(optionsBox+"Shape", ln="IK", at="enum", en="OFF:ON:", dv=0);
        py.setAttr(optionsBox+"Shape.IK", k=1, e=1);
        py.setAttr(optionsBox+".MODE",0);
        py.setDrivenKeyframe(optionsBox+"Shape.FK", cd=optionsBox+".MODE");
        py.setDrivenKeyframe(optionsBox+"Shape.IK", cd=optionsBox+".MODE");
        py.setAttr(optionsBox+".MODE",0.01);
        py.setAttr(optionsBox+"Shape.FK",0);py.setAttr(optionsBox+"Shape.IK",0);
        py.setDrivenKeyframe(optionsBox+"Shape.FK", cd=optionsBox+".MODE");
        py.setDrivenKeyframe(optionsBox+"Shape.IK", cd=optionsBox+".MODE");
        py.setAttr(optionsBox+".MODE",0.99);
        py.setDrivenKeyframe(optionsBox+"Shape.FK", cd=optionsBox+".MODE");
        py.setDrivenKeyframe(optionsBox+"Shape.IK", cd=optionsBox+".MODE");
        py.setAttr(optionsBox+".MODE",1);
        py.setAttr(optionsBox+"Shape.FK",0);py.setAttr(optionsBox+"Shape.IK",1);
        py.setDrivenKeyframe(optionsBox+"Shape.FK", cd=optionsBox+".MODE");
        py.setDrivenKeyframe(optionsBox+"Shape.IK", cd=optionsBox+".MODE");
        py.keyTangent(optionsBox+"Shape.FLIP",itt="linear",ott="linear",e=1);
        py.setAttr(optionsBox+"Shape.hiddenInOutliner",1);
        py.setAttr(optionsBox+"Shape.IK", l=1);
        py.setAttr(optionsBox+"Shape.FK", l=1);
        py.setAttr(optionsBox+"Shape.FLIP", l=1);
        py.setAttr(optionsBox+".MODE", k=1, e=1);
        py.addAttr(optionsBox, ln="RESTRICTED", at="enum", en="OFF:ON:", dv=0);
        py.setAttr(optionsBox+".RESTRICTED", k=0, cb=1, e=1);
        py.setAttr(optionsBox+"Shape.FK", k=0, cb=0, e=1);
        py.setAttr(optionsBox+"Shape.IK", k=0, cb=0, e=1);
        py.transformLimits(controllers[1],rx=(0,0),erx=(1,1));
        py.transformLimits(controllers[1],rz=(0,0),erz=(1,1));
###############################################################################
#"""# ADD ATTRIBUTE RESTRICTIONS FEATURE (FOR REALISM)                        #
###############################################################################
        limbList = [clavicleController]+controllers if(clavicle != "none") else controllers;
        i=0;
        while(i < len(limbList)):
            #SET LOCK VALUES PER AXIS
            lockAxisMin = [-360,-360,-360];
            lockAxisMax = [360,360,360];
            if(limbList[i] == clavicleController):
                lockAxisMin = [-90,-90,-90];
                lockAxisMax = [90,90,90];
            if(limbList[i] == controllers[1]):#ELBOW INDEX (?)
                lockValue = py.getAttr(bindJointChain[1]+".jointOrientY")*-1;
                lockAxisMin = [0,-145,0];
                lockAxisMax = [0,lockValue,0];
            if(limbList[i] == controllers[endIndex]):
                lockAxisMin = [-180,-180,-180];
                lockAxisMax = [180,180,180];
            if(section[-1] != "arm" and limbList[i] == controllers[ballIndex]):
                lockAxisMin = [0,-90,0];
                lockAxisMax = [0,90,0];
            #PLUG IN LOCK LIMITATIONS TO TARGET'S MIN AND MAX ROTATION LIMITS
            ii=0;
            while(ii < len(axis)):
                py.connectAttr(optionsBox+".RESTRICTED",limbList[i]+".minRot"+axis[ii].upper()+"LimitEnable");
                py.connectAttr(optionsBox+".RESTRICTED",limbList[i]+".maxRot"+axis[ii].upper()+"LimitEnable");
                if(ii == 0):
                    py.transformLimits(limbList[i],rx=(lockAxisMin[ii],lockAxisMax[ii]),erx=(0,1));
                if(ii == 1):
                    if(lockAxisMax[ii] >= 0):
                        py.transformLimits(limbList[i],ry=(lockAxisMin[ii],lockAxisMax[ii]),ery=(0,1));
                    else:
                        py.transformLimits(limbList[i],ry=(lockAxisMax[ii],lockAxisMin[ii]*-1),ery=(1,0));
                if(ii == 2):
                    py.transformLimits(limbList[i],rz=(lockAxisMin[ii],lockAxisMax[ii]),erz=(0,1));
                ii+=1;
            i+=1;
###############################################################################
#"""# CONNECT BLEND TO TWIST JOINTS                                           #
###############################################################################
        i=0;
        while(i < len(controllers)):
            name = twistJointChain[i].replace(twistJointChain[i].split("_")[-1], "ONT");
            if(section[-1] == "arm" and i == endIndex):
                name = "c_"+side+"_"+section[-1]+"MatchFK_v"+str(version)+"_LOC";
                matchFK = py.spaceLocator(p=(0,0,0),n=name)[0];
                py.setAttr(matchFK+".v",0);
                name = "c_"+side+"_"+section[-1]+"MatchFK_v"+str(version)+"_GRP";
                matchGroupFK = py.group(n=name);
                snap = py.parentConstraint(controllers[endIndex],matchGroupFK,mo=0,w=1);
                py.delete(snap);
                py.parent(matchGroupFK,controllerIK);
                constraint = py.orientConstraint(matchFK,controllers[i],twistJointChain[i],n=name,mo=1,w=1);#!
            elif(section[-1] != "arm" and i == endIndex):
                constraint = py.orientConstraint(jointChain[i],ankleOffsetFK,twistJointChain[i],n=name,mo=1,w=1);#!
            else:
                constraint = py.orientConstraint(jointChain[i],controllers[i],twistJointChain[i],n=name,mo=1,w=1);#!
            subName = controllers[i].split("_")[2];
            name = "c_"+side+"_"+subName+"HyrbidToggle_v"+str(version)+"_MDN";
            hybridToggle = py.createNode("multiplyDivide", n=name);
            py.connectAttr(primaryIK+".GIR",hybridToggle+".input2X");
            py.connectAttr(primaryIK+".GIR",hybridToggle+".input2Y");
            py.setAttr(hybridToggle+".ihi",0);
            py.setAttr(constraint[0]+".offset", 0,0,0);
            py.setAttr(constraint[0]+".restRotate", 0,0,0);
            py.setAttr(constraint[0]+".interpType", 2);
            py.setAttr(constraint[0]+".ihi", 0);
            if(section[-1] == "arm" and i == endIndex):
                plug = constraint[0]+"."+matchFK+"W0";
            else:
                plug = constraint[0]+"."+jointChain[i]+"W0";
            py.connectAttr(optionsBox+".MODE", hybridToggle+".input1X");
            py.connectAttr(hybridToggle+".outputX",plug);
            if(section[-1] != "arm" and i == endIndex):
                plug = constraint[0]+"."+ankleOffsetFK+"W1";
            else:
                plug = constraint[0]+"."+controllers[i]+"W1"; 
            py.connectAttr(optionsBox+"Shape.FLIP", hybridToggle+".input1Y");
            py.connectAttr(hybridToggle+".outputY",plug);
            i+=1;
###############################################################################
#"""# POSITION OPTIONS BOX                                                    #
###############################################################################
        snap1 = py.pointConstraint(bindJointChain[endIndex],bindJointChain[-1],optionsBoxGroup,mo=0,w=1);
        snap2 = py.orientConstraint(bindJointChain[endIndex],optionsBoxGroup,mo=0,w=1);
        py.delete(snap1, snap2);py.delete(optionsBox, ch=1);
        name = optionsBoxGroup.replace(optionsBoxGroup.split("_")[-1], "CON");
        constraint = py.parentConstraint(bindJointChain[endIndex],optionsBoxGroup,n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi", 0);
###############################################################################
#"""# PV SETUP                                                                #
###############################################################################
        name = "c_"+side+"_"+section[-1]+"PV_v"+str(version)+"_CTRL";
        poleVector = py.rename(poleVectorShape, name);
        py.connectAttr(primaryIK+".firstCOLOR",poleVector+"Shape.overrideColor");
        py.setAttr(poleVector+".s", 2, 2, 2);
        name = "c_"+side+"_"+section[-1]+"PV_v"+str(version)+"_LOC";
        poleVectorBlend = py.spaceLocator(p=(0,0,0), n=name)[0];
        py.select(poleVector, poleVectorBlend, r=1);
        name = "c_"+side+"_"+section[-1]+"PV_v"+str(version)+"_GRP";
        poleVectorGroup = py.group(n=name, r=1);
        name = "c_"+side+"_"+section[-1]+"MasterPV_v"+str(version)+"_GRP";
        poleVectorMasterGroup = py.group(n=name, r=1);
        startJoint = py.xform(jointChain[0], ws=1, t=1, q=1);
        midJoint = py.xform(jointChain[1], ws=1, t=1, q=1);
        endJoint = py.xform(jointChain[endIndex], ws=1, t=1, q=1);
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
        bendJointLength = jointLengths[0]+jointLengths[1];
        if(posture == "quadruped"):
            aimValue *= bendJointLength/15 if(section[-1] == "hindLeg") else bendJointLength/2;
        else:
            aimValue *= bendJointLength/2;
        finalPosition = midJointV+aimValue;
        py.xform(poleVectorMasterGroup,ws=1,t=(finalPosition.x,finalPosition.y,finalPosition.z));
        py.makeIdentity(poleVectorMasterGroup, apply=1, t=1, r=1, s=1, n=0); 
        name = "c_"+side+"_"+section[0]+"_v"+str(version)+"_LOC";
        startLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
        name = startLocator.replace(startLocator.split("_")[-1], "PNT");
        constraint = py.pointConstraint(jointChain[0], startLocator, n=name, mo=0, w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        name = startLocator.replace(startLocator.split("_")[-1], "AIM");
        constraint = py.aimConstraint(controllerIK, startLocator, n=name, aim=(0,-1,0), u=(0,1,0), wu=(0,1,0), wut="vector", mo=1, w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        name = primaryIK.replace(primaryIK.split("_")[-1], "PVC");
        constraint = py.poleVectorConstraint(poleVector, primaryIK, n=name);
        py.parent(poleVectorBlend,startLocator);
        py.makeIdentity(poleVectorBlend, apply=1, t=1, r=1, s=1, n=0); 
        py.makeIdentity(poleVectorGroup, a=1, t=1, n=0);#FREEZE    
        py.setAttr(constraint[0]+".ihi", 0); 
        name = poleVectorGroup.replace(poleVectorGroup.split("_")[-1], "PNT");
        constraint = py.pointConstraint(poleVectorBlend, poleVectorGroup, n=name, mo=1, w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        py.addAttr(poleVector, ln="LOCK", at="enum", en="ON:OFF:", dv=1);
        py.setAttr(poleVector+".LOCK", k=1, e=1);
        py.connectAttr(poleVector+".LOCK",constraint[0]+"."+poleVectorBlend+"W0");
        py.setAttr(startLocator+".v", 0);py.setAttr(poleVectorBlend+".v", 0);
        controllerListIK.append(poleVector);
        #CREATE VISUAL LINE CONNECTING PV TO JOINT
        name = "c_"+side+"_"+section[-1]+"PV_v"+str(version)+"_CRV";
        poleVectorCurve = py.curve(n=name,p=[(0,0,0),(0,100,0)],d=1);
        poleVectorCurveShape = py.listRelatives(poleVectorCurve,c=1,f=1,s=1)[0];
        poleVectorCurveShape = py.rename(poleVectorCurveShape,name+"Shape");
        py.setAttr(poleVectorCurve+".template",1);
        py.parent(poleVectorCurve,poleVectorGroup);
        py.setAttr(poleVectorCurve+".inheritsTransform",0);
        py.setAttr(poleVectorCurveShape+".hideOnPlayback",1);
        py.connectAttr(poleVector+".v",poleVectorCurve+".v");
        py.select(poleVectorCurve+".cv[0]",r=1);
        name = "c_"+side+"_"+section[-1]+"PV_v"+str(version)+"_CLUSTER";
        poleVectorStartCluster = py.cluster(n=name)[-1];
        name = "c_"+side+"_"+section[-1]+"PV_v"+str(version)+"_CLUSTERHANDLE";
        poleVectorStartCluster = py.rename(poleVectorStartCluster,name);
        py.setAttr(poleVectorStartCluster+".v",0);
        py.parent(poleVectorStartCluster,poleVectorGroup);
        name = poleVectorStartCluster.replace(poleVectorStartCluster.split("_")[-1], "PNT");
        constraint = py.pointConstraint(poleVector,poleVectorStartCluster,n=name,mo=0,w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        py.select(poleVectorCurve+".cv[1]",r=1);
        name = "c_"+side+"_"+section[-1]+"JNT_v"+str(version)+"_CLUSTER";
        poleVectorEndCluster = py.cluster(n=name)[-1];
        name = "c_"+side+"_"+section[-1]+"JNT_v"+str(version)+"_CLUSTERHANDLE";
        poleVectorEndCluster = py.rename(poleVectorEndCluster,name);
        py.setAttr(poleVectorEndCluster+".v",0);
        py.parent(poleVectorEndCluster,poleVectorGroup);
        name = poleVectorStartCluster.replace(poleVectorEndCluster.split("_")[-1], "PNT");
        constraint = py.pointConstraint(bindJointChain[1],poleVectorEndCluster,n=name,mo=0,w=1);
        py.setAttr(constraint[0]+".ihi", 0);
###############################################################################
#"""# CREATE AND CONNECT WIREFRAME SHAPE NODES TO JOINTS THEN SHAPE THEM      #
###############################################################################
        nodes = controllers[:];
        if(clavicle != "none"):
            py.connectAttr(primaryIK+".GIR",clavicleConstraint+"."+clavicleController+"W0");
            nodes.append(clavicleController);
        i=0;
        while(i < len(nodes)):
            decoy = py.duplicate(nodes[i], rc=1, rr=1)[0];
            if(clavicleName not in nodes[i]):
                py.setDrivenKeyframe(controllers[i]+"Shape.v", cd=optionsBox+"Shape.FLIP");
                py.setAttr(optionsBox+".MODE",0.95);py.setAttr(controllers[i]+"Shape.v",1);
                py.setDrivenKeyframe(controllers[i]+"Shape.v", cd=optionsBox+"Shape.FLIP");
                py.setAttr(optionsBox+".MODE",1);py.setAttr(controllers[i]+"Shape.v",0);
                py.setDrivenKeyframe(controllers[i]+"Shape.v", cd=optionsBox+"Shape.FLIP");
                py.delete(shapes[i], ch=1);
            wireShape = py.rename(decoy, decoy.replace("CTRL1", "WIRE"));
            py.setAttr(wireShape+".s", 1, 1.1, 1.1);
            py.makeIdentity(wireShape, pn=1, a=1, s=1, n=0);#FREEZE
            py.setAttr(wireShape+"Shape.overrideEnabled", 1);
            py.setAttr(wireShape+"Shape.overrideShading", 0);
            py.setAttr(wireShape+"Shape.overrideTexturing", 0);
            py.setAttr(wireShape+"Shape.hiddenInOutliner", 1);
            py.connectAttr(primaryIK+".firstCOLOR",wireShape+"Shape.overrideColor");
            py.connectAttr(primaryIK+".firstCOLOR",nodes[i]+".overrideColor");
            py.setAttr(nodes[i]+".overrideColor",k=0);
            py.setAttr(wireShape+"Shape.template", 1);
            py.setAttr(wireShape+"Shape.hideOnPlayback", 1);
            if(nodes[i] == controllers[endIndex]):
                ikWire = py.duplicate(wireShape, rc=1, rr=1)[0];
                if(posture == "biped"):
                    if(armPose == "A"):
                        py.setAttr(ikWire+".s", 0.15, 1, 1);#!
                    else:
                        py.setAttr(ikWire+".s", 1, 0.15, 1);#!
                py.makeIdentity(ikWire, pn=1, a=1, s=1, n=0);#FREEZE
                shape = py.listRelatives(ikWire, s=1)[0];
                name = nodes[i].replace(nodes[i].split("_")[2], section[-1]);
                name = name.replace("CTRL", "IK");
                ikWireShape = py.rename(shape, name+"Shape");
                py.connectAttr(primaryIK+".firstCOLOR",ikWireShape+".overrideColor");
                py.setAttr(ikWireShape+".template", 0);
                if(armPose == "A"):#!
                    py.move(0,controllerSize/-2,0,ikWireShape+".vtx[0:7]",r=1,os=1);#!
                py.parent(ikWireShape, controllerIK, r=1, s=1);
                py.setAttr(ikWireShape+".hideOnPlayback", 0);
                ikWireShape = py.rename(ikWireShape,ikWireShape.replace("IK","CTRL"));
                py.delete(ikWire);
            if(i < len(controllers)):
                duplicateWireShape = py.duplicate(wireShape, rc=1, rr=1)[0];  
                shape = py.listRelatives(duplicateWireShape, s=1)[0];  
                name = jointChain[i].replace("JNT", "JointWireframe");
                jointWireShape = py.rename(shape, name);
                py.connectAttr(optionsBox+"Shape.FK", jointWireShape+".v");
                py.parent(jointWireShape, jointChain[i], r=1, s=1);
                py.setAttr(jointWireShape+".ihi",0);
                py.delete(duplicateWireShape);
            if(clavicleName not in nodes[i]):
                py.connectAttr(optionsBox+"Shape.IK", wireShape+"Shape.v");
                py.connectAttr(primaryIK+".GUIDE", wireShape+"Shape.overrideVisibility");
                py.connectAttr(primaryIK+".GUIDE", jointWireShape+".overrideVisibility");
            else:
                py.setAttr(wireShape+"Shape.template", 0);
            py.parent(wireShape+"Shape", nodes[i], r=1, s=1);
            py.setAttr(wireShape+"Shape.ihi",0);
            py.delete(wireShape);
            bodyShape = nodes[i].replace(nodes[i][0:2], "a_");
            if(py.objExists(bodyShape) == 0):
                name = bodyShape;
                bodyShape = py.duplicate(nodes[i],n=name,rr=1)[0];
            if(py.objExists(bodyShape) == 1):
                if(clavicleName not in nodes[i]):
                    jointShape = bodyShape.replace("CTRL","JNT");
                    decoy = py.duplicate(bodyShape, n=jointShape, rc=1, rr=1)[0];
                else:
                    try:
                        py.setAttr(wireShape+"Shape.visibility", 0);
                    except:
                        pass;
                py.parent(bodyShape,nodes[i]);
                py.makeIdentity(bodyShape, pn=1, a=1, t=1, r=1, s=1, n=0);#FREEZE
                py.parent(bodyShape,w=1);
                shapeNode = py.listRelatives(bodyShape, type="shape");
                shapeNode = shapeNode[0] if(len(shapeNode) > 0) else shapeNode;
                py.parent(shapeNode, nodes[i], r=1, s=1);
                py.rename(shapeNode, bodyShape+"Shape");
                py.setAttr(bodyShape+"Shape.ihi", 0);
                py.setAttr(nodes[i]+"Shape.lodVisibility", 0);
                if(clavicleName in nodes[i]):
                    py.connectAttr(nodes[i]+"Shape.v",bodyShape+"Shape.v");
                else:
                    py.connectAttr(optionsBox+"Shape.FK",bodyShape+"Shape.v");
                py.delete(bodyShape);
            py.select(nodes[i], r=1);    
            py.hyperShade(assign=MAT[0]);
            i+=1;
        nodes = jointChain;
        i=0;
        while(i < len(nodes)):
            bodyShape = nodes[i].replace(nodes[i][0:2], "a_");
            if(py.objExists(bodyShape) == 1):
                py.parent(bodyShape,nodes[i]);
                py.makeIdentity(bodyShape, pn=1, a=1, t=1, r=1, s=1, n=0);#FREEZE
                py.parent(bodyShape,w=1);
                shapeNode = py.listRelatives(bodyShape, type="shape");
                shapeNode = shapeNode[0] if(len(shapeNode) > 0) else shapeNode;
                py.parent(shapeNode, nodes[i], r=1, s=1);
                py.rename(shapeNode, bodyShape+"Shape");
                py.setAttr(bodyShape+"Shape.template", 1);
                py.connectAttr(optionsBox+"Shape.IK",bodyShape+"Shape.v");
                py.delete(bodyShape);
            i+=1;
###############################################################################
#"""# IK FOOT CONTROLLER RESHAPE AND IK TOE CONTROLLER                        #
###############################################################################
        if(section[-1] != "arm"):
            #ADD IK TOE CONTROLLER
            if(section[-1] == "leg"):
                toeName = "toe"
            else:
                toeName = "hindToe" if(section[-1] == "hindLeg") else "frontToe";
            name = "c_"+side+"_"+toeName+"_v"+str(version)+"_CTRL";
            toeControllerIK = py.duplicate(controllerIK, n=name, rc=1, rr=1)[0];  
            name = "c_"+side+"_"+toeName+"_v"+str(version)+"_GRP";
            toePivotV1 = py.group(em=1, n=name);
            name = "c_"+side+"_"+toeName+"Master_v"+str(version)+"_GRP";
            toeHandleGroup = py.group(r=1, n=name);  
            snap1 = py.pointConstraint(jointChain[ballIndex], toeHandleGroup, mo=0, w=1);
            snap2 = py.pointConstraint(jointChain[ballIndex], toeControllerIK, mo=0, w=1);
            py.delete(snap1,snap2);
            py.parent(toeControllerIK,toePivotV1);
            py.setAttr(controllerIK+".r",0,0,0);
            py.setAttr(toeControllerIK+".r",0,0,0);
            py.setAttr(handleGroup+".r",0,0,0);
            py.setAttr(handlePivotV3+".r",0,0,0);
            py.connectAttr(primaryIK+".firstCOLOR",toeControllerIK+"Shape.overrideColor");
            py.connectAttr(controllerIK+".v",toeControllerIK+".v");
            #SHAPE CONTROLLERS
            if(posture == "biped"):
                heelDist = controllerSize*-1.2;
                x1 = [controllerSize/-2,controllerSize/-2,controllerSize/2,controllerSize/2,
                      controllerSize/2,controllerSize/2,controllerSize/-2,controllerSize/-2];
                x2 = [controllerSize/-2,controllerSize/-2,controllerSize/2,controllerSize/2,
                      controllerSize/2,controllerSize/2,controllerSize/-2,controllerSize/-2];
                y1 = [controllerSize/10,controllerSize/10,controllerSize/10,controllerSize/10,
                      0,0,0,0];
                y2 = [controllerSize/10,controllerSize/10,controllerSize/10,controllerSize/10,
                      0,0,0,0];
                z1 = [heelDist,0,heelDist,0,heelDist,0,heelDist,0];
                z2 = [0,jointLengths[-1],0,jointLengths[-1],0,jointLengths[-1],0,jointLengths[-1]];
            elif(posture == "quadruped"):
                heelDist = controllerSize*-0.5;
                x1 = [controllerSize/-2,controllerSize/-2,controllerSize/2,controllerSize/2,
                      controllerSize/2,controllerSize/2,controllerSize/-2,controllerSize/-2];
                x2 = [controllerSize/-2,controllerSize/-2,controllerSize/2,controllerSize/2,
                      controllerSize/2,controllerSize/2,controllerSize/-2,controllerSize/-2];
                y1 = [0,0,0,0,
                      controllerSize*-1,controllerSize*-1,controllerSize*-1,controllerSize*-1];
                y2 = [controllerSize*-1,controllerSize*-1,controllerSize*-1,controllerSize*-1,#!
                      0,0,0,0];
                z1 = [heelDist,jointLengths[-1]*2,heelDist,jointLengths[-1]*2,heelDist,jointLengths[-1]*3,heelDist,jointLengths[-1]*3];
                z2 = [heelDist,jointLengths[-1]*3,heelDist,jointLengths[-1]*3,heelDist,jointLengths[-1]*3,heelDist,jointLengths[-1]*3];
            tracer = py.spaceLocator(p=(0,0,0))[0];
            tracerGrid = py.spaceLocator(p=(0,0,0))[0];
            if(posture == "biped"):
                snap1 = py.pointConstraint(jointChain[ballIndex], tracer, mo=0, w=1);
                snap2 = py.pointConstraint(jointChain[ballIndex], tracerGrid, skip=["y"], mo=0, w=1);
            elif(posture == "quadruped"):
                snap1 = py.pointConstraint(jointChain[endIndex], tracer, mo=0, w=1);
                snap2 = py.pointConstraint(jointChain[endIndex], tracerGrid, skip=["y"], mo=0, w=1);
            py.delete(snap1,snap2);
            ballPosition = list(py.getAttr(tracer+".t")[0]);
            ballGridPosition = list(py.getAttr(tracerGrid+".t")[0]);
            i=0;
            while(i < len(x1)):
                #LEG IK
                if(i < 4 or posture == "quadruped"):
                    py.setAttr(tracer+".t",ballPosition[0]+x1[i],ballPosition[1]+y1[i],ballPosition[2]+z1[i]);
                    tracerPosition = py.xform(tracer,q=1,t=1,ws=1);
                else:
                    py.setAttr(tracerGrid+".t",ballGridPosition[0]+x1[i],ballGridPosition[1]+y1[i],ballGridPosition[2]+z1[i]);
                    tracerPosition = py.xform(tracerGrid,q=1,t=1,ws=1);
                vertexPosition = py.pointPosition(controllerIK+".vtx["+str(i)+"]",w=1);
                position = [t - v for t, v in zip(tracerPosition,vertexPosition)];
                py.move(position[0],position[1],position[2],controllerIK+".vtx["+str(i)+"]",r=1,ws=1); 
                #TOE IK
                if(i < 4):
                    py.setAttr(tracer+".t",ballPosition[0]+x2[i],ballPosition[1]+y2[i],ballPosition[2]+z2[i]);
                    tracerPosition = py.xform(tracer,q=1,t=1,ws=1);
                else:
                    py.setAttr(tracerGrid+".t",ballGridPosition[0]+x2[i],ballGridPosition[1]+y2[i],ballGridPosition[2]+z2[i]);
                    tracerPosition = py.xform(tracerGrid,q=1,t=1,ws=1);
                vertexPosition = py.pointPosition(toeControllerIK+".vtx["+str(i)+"]",w=1);
                position = [t - v for t, v in zip(tracerPosition,vertexPosition)];
                py.move(position[0],position[1],position[2],toeControllerIK+".vtx["+str(i)+"]",r=1,ws=1); 
                i+=1;
            controllerListIK.append(toeControllerIK);
            py.delete(tracer,tracerGrid);
###############################################################################
#"""# IK AND FK LOCATORS SETUP                                                #
###############################################################################
        endJoint = jointChain[endIndex];
        name = "c_"+side+"_"+section[endIndex]+"IK_v"+str(version)+"_LOC";
        endLocatorIK = py.spaceLocator(p=(0,0,0), n=name)[0];
        endLocatorIKGRP = py.group(r=1, n=name.replace("LOC", "GRP"));
        py.connectAttr(controllers[endIndex]+".rotateOrder",endLocatorIK+".rotateOrder");
        py.connectAttr(controllers[endIndex]+".rotateOrder",endLocatorIKGRP+".rotateOrder");
        snap = py.parentConstraint(endJoint, endLocatorIKGRP, mo=0, w=1);
        py.delete(snap);
        name = "c_"+side+"_"+section[endIndex]+"FK_v"+str(version)+"_LOC";
        newLocator = py.duplicate(endLocatorIK, rr=1);py.select(newLocator, r=1);
        endLocatorFKGRP = py.group(r=1, n=name.replace("LOC", "GRP"));
        endLocatorFK = py.rename(newLocator, name);
        py.connectAttr(controllers[endIndex]+".rotateOrder",endLocatorFK+".rotateOrder");
        py.connectAttr(controllers[endIndex]+".rotateOrder",endLocatorFKGRP+".rotateOrder");
        name = endLocatorIK.replace(endLocatorIK.split("_")[-1], "CON");
        constraint = py.parentConstraint(jointChain[endIndex],endLocatorIK,n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        py.parent(endLocatorFKGRP, jointChain[1]);
        name = endLocatorFK.replace(endLocatorFK.split("_")[-1], "ONT");
        constraint = py.orientConstraint(jointChain[endIndex],endLocatorFK,n=name,mo=1,w=1);#!
        #constraint = py.orientConstraint(controllers[endIndex],endLocatorFK,n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        py.setAttr(endLocatorIK+".v",0);py.setAttr(endLocatorFK+".v",0);
###############################################################################
#"""# CREATE LOCATOR FOR INITIAL LOCATION FOR FK CONTROLLERS                  #
###############################################################################
        name = "c_"+side+"_"+section[-1]+"InitialPositionFK_v"+str(version)+"_LOC";
        intialLocationFK = py.spaceLocator(p=(0,0,0), n=name)[0];
        snap = py.parentConstraint(controllers[-1], intialLocationFK, mo=0, w=1);
        py.delete(snap);py.parent(intialLocationFK,controllers[endIndex]);
        py.setAttr(intialLocationFK+".v",0);
###############################################################################
#"""# ADD FOOT ROLL AND BANK FUNCTIONS TO BIPED FOOT                          #
###############################################################################
        footAttributes = ["ROLL","BANK","HEEL","TOE","TOEFLOP","HEELROLL","TOEROLL"]; 
        if(section[-1] != "arm" and posture == "biped"): 
            FFV1 = "";FFV6 = bindJointChain;
            FFV2 = side;FFV7 = ankleIndex;
            FFV3 = section;FFV8 = ballIndex;
            FFV4 = version;FFV9 = controllerSize;
            FFV5 = jointChain;FFV10 = primaryIK;
            
            FFV11 = controllerIK;FFV16 = toePivotV1;
            FFV12 = toeControllerIK;FFV17 = toeHandleGroup;
            FFV13 = heelDist;FFV18 = handlePivotV1;
            FFV14 = handleGroup;FFV19 = handlePivotV2;
            FFV15 = legRotationOrder;FFV20 = handlePivotV3;
            
            footFunctionCollection = footFunctions(FFV1,FFV2,FFV3,FFV4,FFV5,FFV6,FFV7,FFV8,FFV9,FFV10,FFV11,FFV12,FFV13,FFV14,FFV15,FFV16,FFV17,FFV18,FFV19,FFV20);
            masterFootGroup = footFunctionCollection[0];
            footAttributes = footFunctionCollection[1];
###############################################################################
#"""# SETUP QUADRUPED FOOT                                                    #
###############################################################################
        elif(section[-1] != "leg" and posture == "quadruped"): 
            name = "c_"+side+"_footMaster_v"+str(version)+"_GRP"
            masterFootGroup = py.group(n=name, em=1);
            snap = py.pointConstraint(bindJointChain[ankleIndex], masterFootGroup, mo=0, w=1);
            py.delete(snap);
            py.parent(handleGroup,masterFootGroup);
            #CREATE LOCATOR FOR INITIAL LOCATION FOR IK LEG CONTROLLER
            name = "c_"+side+"_"+section[-1]+"InitialPositionIK_v"+str(version)+"_LOC";
            intialLocationIK = py.spaceLocator(p=(0,0,0), n=name)[0];
            snap = py.pointConstraint(controllerIK, intialLocationIK, mo=0, w=1);
            py.delete(snap);
            py.parent(intialLocationIK,masterFootGroup);
            py.makeIdentity(intialLocationIK, a=1, t=1, n=0);#FREEZE
            py.addAttr(intialLocationIK,ln="aimAxis",at="enum",en="0,0,1");
            py.addAttr(intialLocationIK,ln="upAxis",at="enum",en="0,1,0");
            py.setAttr(intialLocationIK+".v",0);
            #SETUP HIERARCHY
            py.parent(primaryIK,controllerIK);
            py.parent(toeHandleGroup,controllerIK);
            name = jointChain[ballIndex].replace(jointChain[ballIndex].split("_")[-1], "ONT");
            constraint = py.orientConstraint(toeControllerIK,jointChain[ballIndex],n=name,mo=1,w=1);
###############################################################################
#"""# CREATE LOCATOR FOR INITIAL LOCATION FOR IK ARM CONTROLLER               #
###############################################################################
        else:
            name = "c_"+side+"_"+section[-1]+"InitialPositionIK_v"+str(version)+"_LOC";
            intialLocationIK = py.spaceLocator(p=(0,0,0), n=name)[0];
            snap = py.pointConstraint(controllerIK, intialLocationIK, mo=0, w=1);
            py.delete(snap);py.parent(intialLocationIK,handleGroup);
            py.makeIdentity(intialLocationIK, a=1, t=1, n=0);#FREEZE
            if(armPose == "A"):
                py.addAttr(intialLocationIK,ln="aimAxis",at="enum",en="0,"+str(-1)+",0");
                py.addAttr(intialLocationIK,ln="upAxis",at="enum",en=str(1*reverse)+",0,0");
            else:
                py.addAttr(intialLocationIK,ln="aimAxis",at="enum",en=str(1*reverse)+",0,0");
                py.addAttr(intialLocationIK,ln="upAxis",at="enum",en="0,1,0");
            py.setAttr(intialLocationIK+".v",0);
###############################################################################
#"""# GROUP AND ORGANIZE                                                      #
###############################################################################
        name = "c_"+side+"_"+section[-1]+"Misc_v"+str(version)+"_GRP";
        subGroup = py.group(em=1, n=name);
        snap = py.pointConstraint(jointChain[0],subGroup, mo=0, w=1);
        py.delete(snap);
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_GRP";
        mainGroup = py.group(em=1, n=name);
        snap = py.pointConstraint(jointChain[0],mainGroup, mo=0, w=1);
        py.delete(snap);
        if(section[-1] != "arm"):
            py.parent(masterFootGroup,subGroup);
        else:
            py.parent(handleGroup,subGroup);
        py.parent(startLocator,endLocatorIKGRP,subGroup);
        py.parent(jointChain[0],mainGroup);
        if(clavicle != "none"):
            py.parent(clavicleGroup,mainGroup);
        py.parent(groups[0],poleVectorMasterGroup,optionsBoxGroup,subGroup,mainGroup);
        #py.makeIdentity(controllerIK, apply=1, t=1, r=1, n=0);#FREEZE
        if(section[-1] == "arm" and side == "R"):
            py.setAttr(optionsBoxGroup+".s", -1,1,-1);
###############################################################################
#"""# SET ROTATION ORDERS AND ADDING AN INDENTIFIER TAG                       #
###############################################################################
        if(posture == "biped"):
            rotationOrders = ["xzy","zxy","zyx"] if(section[-1] == "arm") else ["xzy","zxy","xzy","xzy"];
        elif(posture == "quadruped"):
            rotationOrders = ["zxy","zxy","zxy","zxy","zxy"] if(section[-1] == "frontLeg") else ["zxy","zxy","zxy","zxy","zxy"];
        i=0;
        while(i < len(controllers)):
            py.xform(controllers[i], p=1, roo=rotationOrders[i]);
            i+=1;
        nodes = controllers[:];
        nodes.extend((controllerIK, poleVector, optionsBox));
        if(clavicle != "none"):
            nodes.append(clavicleController);
        if(section[-1] != "arm"):
            nodes.append(toeControllerIK);
        i=0;
        while(i < len(nodes)):
            py.addAttr(nodes[i], ln="RiGGiE", dt="string");
            rotationOrder = py.getAttr(nodes[i]+".rotateOrder");
            py.addAttr(nodes[i], ln="ROTATE_ORDER", at="enum", en="XYZ:YZX:ZXY:XZY:YXZ:ZYX:", dv=0);
            py.setAttr(nodes[i]+".ROTATE_ORDER", k=0, cb=1, e=1);
            py.setAttr(nodes[i]+".ROTATE_ORDER", rotationOrder);
            py.connectAttr(nodes[i]+".ROTATE_ORDER",nodes[i]+".rotateOrder");
            try:
                py.connectAttr(nodes[i]+".overrideDisplayType",nodes[i]+"Shape.overrideDisplayType");
            except:
                pass;
            i+=1;
        animatorNodes = nodes[:];
###############################################################################
#"""# LOCK AND HIDE ATTRIBUTES                                                #
############################################################################### 
        attributes = [".sx", ".sy", ".sz", ".v"];
        nodes = controllers[:];
        if(section[-1] != "arm"):
            nodes.append(toeControllerIK);
        if(clavicle != "none"):
            nodes.append(clavicleController);
        specialCaseNodes = [optionsBox, poleVector, controllerIK]
        nodes.extend(specialCaseNodes);
        py.connectAttr(optionsBox+"Shape.IK", controllerIK+".v");
        py.connectAttr(optionsBox+"Shape.IK", poleVector+".v");
        i=0;
        while(i < len(nodes)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(nodes[i]+attributes[ii], k=0, l=1);
                py.setAttr(nodes[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
        attributes = [".tx", ".ty", ".tz"];
        nodes = controllers[:];
        if(section[-1] != "arm"):
            nodes.append(toeControllerIK);
        if(clavicle != "none"):
            nodes.append(clavicleController);
        i=0;
        while(i < len(nodes)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(nodes[i]+attributes[ii], k=0, l=1);
                py.setAttr(nodes[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
        attributes = [".rx", ".ry", ".rz"];
        nodes = [optionsBox, poleVector];
        i=0;
        while(i < len(nodes)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(nodes[i]+attributes[ii], k=0, l=1);
                py.setAttr(nodes[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
        #ADD OPTIONS BOX ATTRIBUTES (CONTINUED)
        py.addAttr(optionsBox, ln="tranX", at="double", dv=0);
        #py.setAttr(optionsBox+".tranX", k=1, e=1);
        py.addAttr(optionsBox, ln="tranZ", at="double", dv=0);
        #py.setAttr(optionsBox+".tranZ", k=1, e=1);
        #CREATE CONDITION NODE FOR OPTIONS BOX
        name = "c_"+side+"_"+section[-1]+"OptionsBox_v"+str(version)+"_CDN";
        optionsBoxCDN = py.createNode("condition", n=name);
        py.setAttr(optionsBoxCDN+".firstTerm", 0);
        py.setAttr(optionsBoxCDN+".secondTerm", 0);
        py.setAttr(optionsBoxCDN+".operation", 0);
        py.connectAttr(optionsBox+".tx", optionsBoxCDN+".colorIfTrueR");
        py.connectAttr(optionsBox+".tz", optionsBoxCDN+".colorIfTrueG");
        py.connectAttr(optionsBoxCDN+".outColorR", optionsBox+".tranX");
        py.connectAttr(optionsBoxCDN+".outColorG", optionsBox+".tranZ");
        py.setAttr(optionsBoxCDN+".ihi",0); 
###############################################################################
#"""# CREATE SPACE LOCATOR                                                    #
############################################################################### 
        spineIK = "c_M_spine_v1_IK";
        pelvis = "c_M_pelvis_v1_CTRL";
        thorax = "c_M_spine3_v1_CTRL";
        name = "c_"+side+"_"+section[-1]+"Space_v"+str(version)+"_LOC";
        spacePivotLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
        snap = py.parentConstraint(controllers[0],spacePivotLocator,mo=0,w=1);
        py.delete(snap);py.parent(spacePivotLocator, subGroup);
        py.addAttr(optionsBox, ln="SPACE", at="enum", en="WORLD:LOCAL:", dv=0);
        py.setAttr(optionsBox+".SPACE", k=1, e=1);
        name = jointChain[0].replace(jointChain[0].split("_")[-1], "PNT");
        constraint = py.pointConstraint(spacePivotLocator,jointChain[0],n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi",0);
        name = groups[0].replace(groups[0].split("_")[-1], "PNT");
        constraint = py.pointConstraint(spacePivotLocator,groups[0],n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi",0);
        name = groups[0].replace(groups[0].split("_")[-1], "ONT");
        constraint = py.orientConstraint(spacePivotLocator,groups[0],n=name,mo=1,w=1);
        py.connectAttr(optionsBox+".SPACE",constraint[0]+"."+spacePivotLocator+"W0");
        py.setAttr(constraint[0]+".ihi",0);py.setAttr(spacePivotLocator+".v",0);
        name = spacePivotLocator.replace(spacePivotLocator.split("_")[-1], "CON");
        if(clavicle != "none" and (section[-1] == "arm" or posture == "quadruped")):
            #IF ARM WITH CLAVICLE OR QUADRUPED LIMB
            if(py.objExists(thorax) == 1):
                spineMAT = "MSPINE1_MAT";
                clavicleForm = clavicleController.replace(clavicleController[0:2],"a_");
                if(py.objExists(clavicleForm) == 1):
                    py.setAttr(clavicleForm+"Shape.overrideEnabled", 1);
                    py.connectAttr(spineIK+".firstCOLOR",clavicleForm+"Shape.overrideColor");
                if(section[-1] == "frontLeg" and py.objExists(thorax) == 1):
                    #IF QUADRUPED FRONT LEG
                    bodyAttachmentPoint = thorax;
                elif(section[-1] == "hindLeg" and py.objExists(pelvis) == 1):
                    #IF QUADRUPED HIND LEG
                    bodyAttachmentPoint = pelvis;
                else:
                    #IF BIPED ARM
                    bodyAttachmentPoint = thorax;
                constraint = py.parentConstraint(bodyAttachmentPoint,clavicleGroup,n=name,mo=1,w=1);
                py.select(clavicleController,r=1);py.hyperShade(assign=spineMAT);
                py.setAttr(constraint[0]+".ihi",0);
            constraint = py.parentConstraint(clavicleController,spacePivotLocator,n=name,mo=1,w=1);
        elif(clavicle == "none" and section[-1] == "arm" and py.objExists(thorax) == 1):
            #IF ARM WITHOUT A CLAVICLE
            bodyAttachmentPoint = thorax;
            constraint = py.parentConstraint(bodyAttachmentPoint,spacePivotLocator,n=name,mo=1,w=1);
        elif(py.objExists(pelvis) == 1):
            #IF ANYTHING ELSE AND PELVIS EXISTS
            bodyAttachmentPoint = pelvis;
            constraint = py.parentConstraint(bodyAttachmentPoint,spacePivotLocator,n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi",0);
        py.addAttr(optionsBox, ln="SWITCH_SPACE", at="enum", en="----------:WORLD:LOCAL:", dv=0);
        py.setAttr(optionsBox+".SWITCH_SPACE", k=0, cb=1, e=1);
###############################################################################
#"""# CREATE LIMB CONNECTION ATTRIBUTES TO SHAPE NODES                        #
############################################################################### 
        attributes = ["translate", "rotate", "MODE", "SPACE"];
        attributes.extend(footAttributes);
        i=0;
        while(i < len(animatorNodes)):
            otherNodes = animatorNodes[:];
            index = [l for l, s in enumerate(otherNodes) if animatorNodes[i].split("_")[2] in s][0];
            otherNodes.remove(otherNodes[index]);
            ii=0;
            while(ii < len(otherNodes)):
                iii=0;
                while(iii < len(attributes)):
                    if(py.attributeQuery(attributes[iii],node=otherNodes[ii],ex=1) == 1):#EXISTS?
                        if(py.getAttr(otherNodes[ii]+"."+attributes[iii], l=1) == 0):#UNLOCKED?
                            name = otherNodes[ii].split("_")[2]+"_"+attributes[iii];
                            vectorCheck = py.attributeQuery(attributes[iii],node=otherNodes[ii],lc=1);
                            if(isinstance(vectorCheck,list) == 1):
                                #IF VECTOR
                                py.addAttr(animatorNodes[i]+"Shape",ln=name,at="double3");
                                iiii=0;
                                while(iiii < len(axis)):
                                    py.addAttr(animatorNodes[i]+"Shape",ln=name+axis[iiii].upper(),p=name,at="double");
                                    iiii+=1;
                                iiii=0;
                                while(iiii < len(vectorCheck)):
                                    if(py.getAttr(otherNodes[ii]+"."+vectorCheck[iiii], k=1) == 1):
                                        py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), k=1, e=1);
                                    else:
                                        py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), k=0, e=1);
                                        py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), cb=0, e=1);
                                    iiii+=1;
                            elif(py.attributeQuery(attributes[iii],node=otherNodes[ii],e=1) == 1):
                                #IF ENUM
                                options = py.addAttr(otherNodes[ii]+"."+attributes[iii],en=1,q=1);
                                py.addAttr(animatorNodes[i]+"Shape",ln=name,at="enum",en=options,dv=0);
                            else:
                                #IF FLOAT
                                py.addAttr(animatorNodes[i]+"Shape",ln=name,at="double");
                            py.setAttr(animatorNodes[i]+"Shape."+name, k=1, e=1);
                    iii+=1;
                ii+=1;
            py.setAttr(animatorNodes[i]+"Shape.hiddenInOutliner", 1);
            i+=1;
###############################################################################
#"""# CONNECT CHILDREN TO ARM                                                 #
###############################################################################
        fingers = ["pinky", "ring", "middle", "index", "thumb"];
        confirmedFingers = [];
        if(len(fingerJoints) > 0):
            fingerPositions = [];
            py.parent(fingerJoints,bindJointChain[wristIndex]);
            i=0;
            while(i < len(fingerJoints)):
                py.select(fingerJoints[i], hi=1, r=1);
                fingerTip = py.ls(sl=1, type="joint");
                fingerPositions.append(py.xform(fingerTip[-1],q=1,t=1,ws=1)[-1]);
                i+=1;
            fingerPositions.sort();
            i=0;
            while(i < len(fingerPositions)):
                ii=0;
                while(ii < len(fingerJoints)):
                    py.select(fingerJoints[ii], hi=1, r=1);
                    fingerTip = py.ls(sl=1, type="joint");
                    position = py.xform(fingerTip[-1],q=1,t=1,ws=1)[-1];
                    if(fingerPositions[i] == position):
                        fingerPositions[i] = fingerJoints[ii];
                        fingerJoints.remove(fingerJoints[ii]);
                        py.select(fingerPositions[i], r=1);
                        segment(fingers[i],bindJointChain[wristIndex],subGroup,MAT[0],primaryIK);
                        confirmedFingers.append(fingers[i]);
                    ii+=1;
                i+=1;
        if(section[-1] == "arm"):
            py.delete(bindJointChain[-1]);
            bindJointChain.remove(bindJointChain[-1]);
            jointChain.remove(jointChain[-1]);
            py.setAttr(optionsBox+".MODE", 0);
        else:
            py.setAttr(optionsBox+".MODE", 1);
###############################################################################
#"""# CREATE TWIST JOINTS                                                     #
###############################################################################
        outputChain = [];
        inputChain = [bindJointChain[0]];
        limbPosition = ["Upper","Lower"];
        name = "c_"+side+"_"+section[-1]+"Twist_v"+str(version)+"_GRP";
        twistGroup = py.group(n=name,em=1);
        snap = py.parentConstraint(twistJointChain[0],twistGroup,mo=0,w=1);
        py.delete(snap);py.parent(twistJointChain[0],twistGroup);
        py.setAttr(twistGroup+".v",0);
        #TWIST
        if(section[-1] == "arm"):
            name = "c_"+side+"_shoulderSocketTwist_v"+str(version)+"_JNT";
        else:
            name = "c_"+side+"_hipSocketTwist_v"+str(version)+"_JNT";
        socketJoint = py.duplicate(twistJointChain[0], n=name, po=1)[0];
        outputChain.append(socketJoint);
        divideLocator = py.spaceLocator(p=(0,0,0))[0];
        snap = py.pointConstraint(twistJointChain[0],twistJointChain[1],divideLocator,mo=0,w=1);
        py.delete(snap);py.parent(socketJoint,twistJointChain[0]);
        i=0;
        while(i < len(limbPosition) and posture != "quadruped"):
            #INPUT
            part = section[-1][0].upper()+section[-1][1:];
            name = "b_"+side+"_"+"upper"+part+limbPosition[i]+"Twist_v"+str(version)+"_JNT";
            bindTwist = py.duplicate(bindJointChain[0], n=name, po=1)[0];
            snap = py.pointConstraint(bindJointChain[i],divideLocator,bindTwist,mo=0,w=1);
            py.setAttr(snap[0]+"."+divideLocator+"W1",2);
            py.delete(snap);py.parent(bindTwist,bindJointChain[0]);
            inputChain.append(bindTwist);
            #OUTPUT
            part = section[-1][0].upper()+section[-1][1:];
            name = "c_"+side+"_"+"upper"+part+limbPosition[i]+"Twist_v"+str(version)+"_JNT";
            jointTwist = py.duplicate(twistJointChain[0], n=name, po=1)[0];
            snap = py.pointConstraint(twistJointChain[i],divideLocator,jointTwist,mo=0,w=1);
            py.setAttr(snap[0]+"."+divideLocator+"W1",2);
            py.delete(snap);py.parent(jointTwist,twistJointChain[0]);
            outputChain.append(jointTwist);
            i+=1;
        inputChain.append(bindJointChain[1]);#!
        outputChain.append(twistJointChain[1]);
        py.delete(divideLocator);
        if(section[-1] == "arm"):  
            divideLocator = py.spaceLocator(p=(0,0,0))[0];
            snap = py.pointConstraint(twistJointChain[1],twistJointChain[endIndex],divideLocator,mo=0,w=1);
            py.delete(snap);
            i=0;
            while(i < len(limbPosition)):
                #INPUT
                part = section[-1][0].upper()+section[-1][1:];
                name = "b_"+side+"_"+"lower"+part+limbPosition[i]+"Twist_v"+str(version)+"_JNT";
                bindTwist = py.duplicate(bindJointChain[1], n=name, po=1)[0];
                snap = py.pointConstraint(bindJointChain[i+1],divideLocator,bindTwist,mo=0,w=1);
                py.setAttr(snap[0]+"."+divideLocator+"W1",2);
                py.delete(snap);py.parent(bindTwist,bindJointChain[1]);
                inputChain.append(bindTwist);
                #OUTPUT
                part = section[-1][0].upper()+section[-1][1:];
                name = "c_"+side+"_"+"lower"+part+limbPosition[i]+"Twist_v"+str(version)+"_JNT";
                jointTwist = py.duplicate(twistJointChain[1], n=name, po=1)[0];
                snap = py.pointConstraint(twistJointChain[i+1],divideLocator,jointTwist,mo=0,w=1);
                py.setAttr(snap[0]+"."+divideLocator+"W1",2);
                py.delete(snap);py.parent(jointTwist,twistJointChain[1]);
                outputChain.append(jointTwist);
                i+=1;
            py.delete(divideLocator);
        i=2;
        while(i < len(bindJointChain)):
            inputChain.append(bindJointChain[i]);
            outputChain.append(twistJointChain[i]);
            i+=1;
        ballJoints = [twistJointChain[0],twistJointChain[-2]];
        if(section[-1] == "arm"): 
            wristTwist = [s for s in twistJointChain if "wrist" in s];
            index = twistJointChain.index(wristTwist[0]);
            name = "c_"+side+"_wristSocketTwist_v"+str(version)+"_JNT";
            socketJoint = py.duplicate(twistJointChain[index], n=name, po=1)[0];
            outputChain[-1] = socketJoint;
            py.parent(socketJoint,twistJointChain[index]);
###############################################################################
#"""# CREATE UPPER LIMB TWIST FUNCTIONALITY                                   #
###############################################################################
        limbPosition = ["upper","lower"];
        bindJoints = [bindJointChain[0],bindJointChain[-2]];
        driverJoints = [twistJointChain[0],twistJointChain[-2]];
        targetJoints = [twistJointChain[1],twistJointChain[-2]];
        counterJoints = [outputChain[0],outputChain[-1]];
        rooTargets = [bindJointChain[0],bindJointChain[-1]];
        i=0;
        while(i < len(driverJoints) and section[-1] == "arm"):#!
            part = section[-1][0].upper()+section[-1][1:];
            name = "c_"+side+"_"+limbPosition[i]+part+"Divider_v"+str(version)+"_MDN";
            divider = py.createNode("multiplyDivide", n=name);
            py.setAttr(divider+".input2",1.0,0.66,0.33);
            if(i == 0):
                twistJoints = [outputChain[1],outputChain[2]];
            else:
                twistJoints = [outputChain[5],outputChain[4]];#!
            #ADD AIM JOINT
            part = ballJoints[i].split("_")[2];
            name = "c_"+side+"_"+part+"Start_v"+str(version)+"_JNT";
            startJoint = py.duplicate(driverJoints[i], n=name, po=1)[0];     
            aimJoint = startJoint;
            part = ballJoints[i].split("_")[2];
            name = "c_"+side+"_"+part+"End_v"+str(version)+"_JNT";
            endJoint = py.duplicate(driverJoints[i], n=name, po=1)[0];
            if(i != len(driverJoints)-1):
                snap1 = py.pointConstraint(ballJoints[i],startJoint,mo=0,w=1);
                snap2 = py.pointConstraint(targetJoints[i],endJoint,mo=0,w=1);
            else:
                snap1 = py.pointConstraint(targetJoints[i],startJoint,mo=0,w=1);
                snap2 = py.pointConstraint(twistJointChain[-3],endJoint,mo=0,w=1);
            py.delete(snap1,snap2);
            py.parent(endJoint,startJoint);py.parent(aimJoint,w=1);
            plug = -1 if((side == "R" and section[-1] == "arm") or section[-1] == "leg") else 1;
            name = aimJoint.replace(aimJoint.split("_")[-1],"PNT");
            constraint = py.pointConstraint(ballJoints[i],aimJoint,n=name,mo=0, w=1);
            #ADD AIM LOCATORS AND GROUPS
            rotationOrder = py.xform(rooTargets[i],roo=1, q=1);
            part = section[-1][0].upper()+section[-1][1:];
            name = "c_"+side+"_"+limbPosition[i]+part+"HalfTwist_v"+str(version)+"_LOC";
            half = py.spaceLocator(p=(0,0,0),n=name)[0];
            name = "c_"+side+"_"+limbPosition[i]+part+"FullTwist_v"+str(version)+"_LOC";
            full = py.spaceLocator(p=(0,0,0),n=name)[0];
            py.xform(half,full, p=1, roo=rotationOrder);
            py.parent(half,full,ballJoints[i]);
            py.setAttr(half+".t",0,0,0);py.setAttr(half+".r",0,0,0);
            py.setAttr(full+".t",0,0,0);py.setAttr(full+".r",0,0,0);
            #ADD IK TO AIM (START/END) JOINTS
            name = "c_"+side+"_"+limbPosition[i]+part+"Twist_v"+str(version)+"_IK";
            twistIK = py.ikHandle(n=name, sj=startJoint, ee=endJoint, sol="ikRPsolver")[0];
            py.setAttr(twistIK+".poleVector",0,0,0);
            solverIK = py.listConnections(twistIK, type="ikSolver")[0];
            py.setAttr(solverIK+".ihi", 0);
            effectors = py.ls(type="ikEffector");
            name = "c_"+side+"_"+limbPosition[i]+part+"Twist_v"+str(version)+"_EF";
            primaryEffector = py.rename(effectors[-1],name);
            py.xform(counterJoints[i], twistIK, p=1, roo=rotationOrder);
            #ADD TWIST FUNCTION TO JOINTS
            name = half.replace(half.split("_")[-1],"ONT");
            constraint = py.orientConstraint(aimJoint,half,n=name,mo=0, w=1);
            name = full.replace(full.split("_")[-1],"ONT");
            constraint = py.orientConstraint(aimJoint,ballJoints[i],full,n=name,mo=0, w=1);#!
            py.addAttr(counterJoints[i],ln="twist180",at="double");
            py.setAttr(counterJoints[i]+".twist180",k=0,cb=1,e=1);
            py.addAttr(counterJoints[i],ln="twist360",at="double");
            py.setAttr(counterJoints[i]+".twist360",k=0,cb=1,e=1);
            py.connectAttr(half+".rx",counterJoints[i]+".twist180");
            part = section[-1][0].upper()+section[-1][1:];
            name = "c_"+side+"_"+limbPosition[i]+part+"TwistDoubler_v"+str(version)+"_MDL";
            doubler = py.createNode("multDoubleLinear", n=name);
            py.connectAttr(full+".rx",doubler+".input1");
            variation = 1 if not(i == len(driverJoints)-1) else -1;
            py.setAttr(doubler+".input2",2*variation);
            py.connectAttr(doubler+".output",counterJoints[i]+".twist360");
            py.connectAttr(doubler+".output",divider+".input1X");
            py.connectAttr(doubler+".output",divider+".input1Y");
            py.connectAttr(doubler+".output",divider+".input1Z");
            #CONNECT VALUES TO TWIST JOINTS
            if not(i == len(driverJoints)-1):
                py.connectAttr(divider+".outputX",counterJoints[i]+".rx");
            py.connectAttr(divider+".outputY",      twistJoints[0]+".rx");
            py.connectAttr(divider+".outputZ",      twistJoints[1]+".rx");
            radius = py.getAttr(counterJoints[i]+".radius");
            py.setAttr(counterJoints[i]+".radius",radius*2);
            py.parent(aimJoint,twistGroup);py.parent(twistIK,driverJoints[i]);
            if(i == len(driverJoints)-1):
                py.parent(twistIK,twistJointChain[-3]);
                py.parent(startJoint,twistJointChain[-3]);
            if(section[-1] == "arm"): 
                i+=1;
            else:
                break
        #PARENT TWIST GROUP UNDER BEST NODE TO AVOID SPIN ROTATION'S FLIPPING
        topSpineValue = 1;
        while(py.objExists("c_M_spine"+str(topSpineValue)+"_v1_CTRL") == 1):
            topSpineValue += 1; 
        topSpineController = "c_M_spine"+str(topSpineValue-1)+"_v1_CTRL";
        bottomSpineController = "c_M_pelvis_v1_CTRL" if(py.objExists("c_M_pelvis_v1_CTRL") == 1) else "";
        py.parent(twistGroup,subGroup);
        if(section[-1] == "arm" or section[-1] == "frontLeg"):
            if(clavicle != "none"):
                name = twistGroup.replace(twistGroup.split("_")[-1],"CON");
                constraint = py.parentConstraint(clavicleController,twistGroup,n=name,mo=1, w=1);#!
                py.setAttr(constraint[0]+".ihi", 0);
                py.connectAttr(primaryIK+".GIR",constraint[0]+"."+clavicleController+"W0");
            elif(py.objExists(topSpineController) == 1):
                name = twistGroup.replace(twistGroup.split("_")[-1],"CON");
                constraint = py.parentConstraint(topSpineController,twistGroup,n=name,mo=1, w=1);#!
                py.setAttr(constraint[0]+".ihi", 0);
        else:
            if(bottomSpineController != ""):
                name = twistGroup.replace(twistGroup.split("_")[-1],"CON");
                constraint = py.parentConstraint(bottomSpineController,twistGroup,n=name,mo=1, w=1);#!
                py.setAttr(constraint[0]+".ihi", 0);
###############################################################################
#"""# CONNECT BLEND TO TWIST JOINTS                                           #
###############################################################################
        i=0;
        while(i < len(outputChain)):
            name = inputChain[i].replace(inputChain[i].split("_")[-1],"ONT");
            constraint = py.orientConstraint(outputChain[i],inputChain[i],n=name,mo=1, w=1);#!
            py.setAttr(constraint[0]+".ihi", 0);
            i+=1;
###############################################################################
#"""# ADD PICKWALK ATTRIBUTES TO SHAPE NODES                                  #
###############################################################################
        #FK MODE
        animatorNodes = controllers[:];
        if(clavicle != "none"):
            animatorNodes.insert(0,clavicleController);
        animatorNodes.insert(len(animatorNodes),animatorNodes[0]);
        animatorNodes.insert(0,animatorNodes[-2]);   
        i=1;
        while(i < len(animatorNodes)-1):
            shapeNode = animatorNodes[i]+"Shape";
            py.addAttr(shapeNode,ln="UP"+animatorNodes[i-1], at="long");
            py.setAttr(shapeNode+".UP"+animatorNodes[i-1],l=1,cb=1,e=1);
            if not("wrist" in shapeNode and confirmedFingers != []):
                py.addAttr(shapeNode,ln="DOWN"+animatorNodes[i+1], at="long");
                py.setAttr(shapeNode+".DOWN"+animatorNodes[i+1],l=1,cb=1,e=1);
            else:
                ii=0;
                while(ii < len(confirmedFingers)):
                    finger = animatorNodes[i].replace(animatorNodes[i].split("_")[2],confirmedFingers[ii]+"1");
                    py.addAttr(shapeNode,ln="DOWN"+finger, at="long");
                    py.setAttr(shapeNode+".DOWN"+finger,l=1,cb=1,e=1);
                    ii+=1; 
            i+=1;  
        #IK MODE
        animatorNodes = controllerListIK[:];
        animatorNodes.insert(len(animatorNodes),animatorNodes[0]);
        animatorNodes.insert(0,animatorNodes[-2]);
        animatorNodes.reverse();
        i=1;
        while(i < len(animatorNodes)-1):
            shapeNode = animatorNodes[i]+"Shape";
            py.addAttr(shapeNode,ln="UP"+animatorNodes[i-1], at="long");
            py.setAttr(shapeNode+".UP"+animatorNodes[i-1],l=1,cb=1,e=1);
            py.addAttr(shapeNode,ln="DOWN"+animatorNodes[i+1], at="long");
            py.setAttr(shapeNode+".DOWN"+animatorNodes[i+1],l=1,cb=1,e=1);
            i+=1;
###############################################################################
#"""# CONNECT LIMB TO SPINE                                                   #
###############################################################################
        if(clavicle == "none" and isinstance(parentJoint,list) == 1):
            py.parent(bindJointChain[0], parentJoint);
        elif(isinstance(parentJoint,list) == 1):
            py.parent(clavicleJoint, parentJoint);
###############################################################################
#"""# CONNECT MASTER CONTROLLER'S TRANSPARENCY ATTRIBUTE TO MATERIAL          #
###############################################################################
        masterVariation = controllers[0].replace(controllers[0].split("_")[2],"master");
        masterController = masterVariation.replace(controllers[0].split("_")[1],"M",1);
        if(py.objExists(masterController) == 1):
            transparent = py.listAttr(masterController, st=["TRANSPARENCY"], r=1);
            if(isinstance(transparent, list) == True):
                py.setAttr(masterController+".TRANSPARENCY",0);
                py.setDrivenKeyframe(MAT[0]+".transparency",cd=masterController+".TRANSPARENCY");
                py.setAttr(masterController+".TRANSPARENCY",100);py.setAttr(MAT[0]+".transparency",1,1,1);
                py.setDrivenKeyframe(MAT[0]+".transparency",cd=masterController+".TRANSPARENCY");
                py.setAttr(masterController+".TRANSPARENCY",0);
###############################################################################
#"""# CREATE AND FINALIZE SPINE/CHARACTER ASSETS                              #
###############################################################################
        master = "c_M_master_v1_CTRL";
        subMaster = "c_M_pivot_v1_CTRL";
        if(py.objExists(master) == 1 and py.objExists(subMaster) == 1):
            py.parent(mainGroup, subMaster);
            py.connectAttr(master+".GUIDE", primaryIK+".GUIDE");
            if(side == "L"):
                py.connectAttr(master+".LEFT_COLOR", primaryIK+".COLOR");
            else:
                py.connectAttr(master+".RIGHT_COLOR", primaryIK+".COLOR");
            py.connectAttr(master+".RIG", primaryIK+".RIG");
        py.displayPref(displayAffected=0);
        i=0;
        while(i < 100 and py.objExists(switchSpaceCalculator) == 1):
            try:
                py.connectAttr(optionsBox+".SWITCH_SPACE",switchSpaceCalculator+".input1D["+str(i)+"]");
                break
            except:
                pass;
            i+=1;
        print '"'+section[-1][0].upper()+section[-1][1:]+' successfully created!" - HiGGiE';
        py.headsUpMessage('"'+section[-1][0].upper()+section[-1][1:]+' successfully created!" - HiGGiE', t=3);
    py.select(d=1);
###############################################################################
#.............................................................................#
#.............................................................................#
#"""# CREATES A SPINE RIG                                                     #
#.............................................................................#
#.............................................................................#
###############################################################################
def spine(style):
    VERSION = 3;
    axis = ["X","Y","Z"];
    initialJointSelection = py.ls(sl=1, type="joint");
    if(isinstance(initialJointSelection, list) == 1):
        #DUPLICATE SKELETON AND GIVE JOINTS A UNIQUE NAME
        py.duplicate(initialJointSelection, rc=1, rr=1);
        py.delete(initialJointSelection);
        initialJointSelection = py.ls(sl=1, type="joint");
        #FIND FIRST SPINE JOINT (TO BEGIN CATEGORIZATION OF LIMBS)
        py.pickWalk(d="down");
        nextSpineSegment = py.ls(sl=1, type="joint");
        py.select(initialJointSelection[0],hi=1, r=1);
        initialSelectionHierarchy = py.ls(sl=1, type="joint");
    if(len(initialSelectionHierarchy) >= 5 and nextSpineSegment[0] != initialJointSelection[0]):
###############################################################################
#"""# FINDS THE CHILDREN OF THE SPINE SEGMENTS                                #
###############################################################################
        masterPosition  = py.xform(initialSelectionHierarchy[0],q=1,t=1,ws=1);
        firstPosition = py.xform(initialSelectionHierarchy[0],q=1,t=1,ws=1);
        lastPosition = py.xform(nextSpineSegment,q=1,t=1,ws=1);
        posture = "quadruped" if not(round(firstPosition[1],0) < round(lastPosition[1],0)) else "biped";
        children = [];
        joints = initialSelectionHierarchy[:];
        requiredJointCount = 5;
        i=0;
        while(i < requiredJointCount):
            allChildren = py.listRelatives(joints[i], c=1);
            if(isinstance(allChildren,list) == 1):
                limbChildren = [];
                ii=0;
                while(ii < len(allChildren)):
                    position = py.xform(allChildren[ii],q=1,t=1,ws=1);
                    if(round(position[0],0) != round(masterPosition[0],0)):
                        #LIMBS
                        limbChildren.append(allChildren[ii]);
                        py.parent(allChildren[ii], w=1);
                        py.select(allChildren[ii], hi=1, r=1);
                        limbs = py.ls(sl=1, type="joint");
                        joints = [x for x in joints if x not in limbs];
                    elif(round(position[0],0) == round(masterPosition[0],0) and i == requiredJointCount-1):
                        #HEAD
                        neck = py.listRelatives(joints[i], c=1);
                        if(isinstance(neck,list) == 1):
                            py.parent(neck[0], w=1);
                            py.select(neck[0], hi=1, r=1);
                            limbs = py.ls(sl=1, type="joint");
                            joints = [x for x in joints if x not in limbs];
                            py.joint(neck[0],e=1,oj="xyz",secondaryAxisOrient="xdown",ch=1,zso=1);
                            limbChildren.append(neck[0]); 
                    elif(posture == "quadruped" and round(position[0],0) == round(masterPosition[0],0) and round(position[2],0) < round(masterPosition[2],0)):
                        #QUADRUUPED TAIL
                        limbChildren.append(allChildren[ii]);
                        py.parent(allChildren[ii], w=1);
                        py.select(allChildren[ii], hi=1, r=1);
                        limbs = py.ls(sl=1, type="joint");
                        joints = [x for x in joints if x not in limbs];
                    ii+=1;  
            children.append(limbChildren);
            i+=1;    
        initialSelectionHierarchy = joints[:];
###############################################################################
#"""# CHECKS THE SPINE TYPE, POSITION AND VERSION OF THE JOIN CHAIN           #
############################################################################### 
        newJoints = py.duplicate(initialSelectionHierarchy, rc=1, rr=1);
        firstPosition = py.xform(newJoints[0],q=1,t=1,ws=1);
        #lastPosition = py.xform(newJoints[-1],q=1,t=1,ws=1);
        #posture = "quadruped" if not(firstPosition[1] < lastPosition[1]) else "biped";
        section = ["pelvis", "spine1", "spine2", "spine3", "spine4", "spine"];
        side = "M";
        reverse = 1;
        version = 1;
        while(py.objExists("c_"+side+"_"+section[0]+"_v"+str(version)+"_CTRL")):
            version += 1;   
        i=0;
        while(i < len(newJoints)):
            py.makeIdentity(newJoints[i], apply=1, r=1, n=0);
            i+=1;
        if(posture == "biped"):
            py.joint(newJoints[0],e=1,oj="xzy",secondaryAxisOrient="zup",ch=1,zso=1);
        else:
            py.joint(newJoints[0],e=1,oj="xzy",secondaryAxisOrient="ydown",ch=1,zso=1);
        #CREATE EVALUATION LOCATOR
        name = "c_"+side+"_evaluator_v"+str(version)+"_LOC";
        evaluationLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
        name = "c_"+side+"_spaceSwitchCalculator_v1_PMA";
        switchSpaceCalculator = py.createNode("plusMinusAverage",n=name);
        py.setAttr(switchSpaceCalculator+".ihi",0);
###############################################################################
#"""# RENAME JOINT CHAINS                                                     #
###############################################################################
        bindJointChain = [];
        i = len(newJoints);
        while(i > 0):
            name = "b_"+side+"_"+section[i-1]+"_v"+str(version)+"_JNT";
            newName = py.rename(newJoints[i-1], name);
            bindJointChain.append(newName);
            i-=1;
        bindJointChain.reverse()
        newJoints = py.duplicate(bindJointChain, rc=1, rr=1);
        jointChain = [];
        positions = [];
        i = len(newJoints);ii=7;
        while(i > 0):
            if(i == 1 or ii == 7):
                tag = section[i-1] if(i == 1) else section[i-1][:-1]+str(ii);
                name = "c_"+side+"_"+tag+"_v"+str(version)+"_JNT";
                newName = py.rename(newJoints[i-1], name);
                jointPosition = py.xform(newName, t=1, ws=1, q=1);
                positions.append(jointPosition);
                jointChain.append(newName);
            else:
                py.select(d=1);
                name = "c_"+side+"_"+section[i-1][:-1]+str(ii)+"_v"+str(version)+"_JNT";
                midJoint = py.joint(p=(0,0,0), n=name);
                snap1 = py.pointConstraint(newJoints[i-1],newJoints[i-2],midJoint,mo=0,w=1);
                snap2 = py.orientConstraint(newJoints[i-1],midJoint,mo=0,w=1);
                py.delete(snap1, snap2);
                name = "c_"+side+"_"+section[i-1][:-1]+str(ii+1)+"_v"+str(version)+"_JNT";
                newName = py.rename(newJoints[i-1], name);
                py.parent(newName, midJoint);py.parent(midJoint, newJoints[i-2]);
                #py.setAttr(newName+".radius", 0);py.setAttr(newName+".drawStyle", 2);
                jointPosition1 = py.xform(newName, t=1, ws=1, q=1);
                jointPosition2 = py.xform(midJoint, t=1, ws=1, q=1);
                positions.extend((jointPosition1, jointPosition2));
                jointChain.extend((newName, midJoint));
            i-=1;ii-=2;
        jointChain.reverse();positions.reverse();
        py.delete(initialJointSelection);
        py.makeIdentity(jointChain[:], a=1, r=1, n=0);#FREEZE
        if(posture == "biped"):
            py.joint(jointChain[0],e=1,oj="yzx",secondaryAxisOrient="zup",ch=1,zso=1);
        else:
            py.joint(jointChain[0],e=1,oj="yzx",secondaryAxisOrient="ydown",ch=1,zso=1);
###############################################################################
#"""# CREATE SPINE CURVE                                                      #
###############################################################################
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_CRV";
        spineCurve = py.curve(d=1, p=positions[:], ws=1, n=name);
        name = "c_"+side+"_"+section[-1]+"Info_v"+str(version)+"_CRV";
        py.arclen(ch=1);
        curveInfo = py.rename("curveInfo1", name);
        arcLength = py.getAttr(curveInfo+".arcLength");
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_IK";
        primaryIK = py.ikHandle(sol="ikSplineSolver", c=spineCurve, sj=jointChain[0], ee=jointChain[-1], ccv=0, pcv=0, n=name)[0];
        py.setAttr(spineCurve+".inheritsTransform", 0);
        py.select(jointChain[0], hi=1, r=1);
        effectors = py.ls(type="ikEffector");
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_EF";
        primaryEffector = py.rename(effectors[0], name);
        name = "c_"+side+"_upper"+section[-1][0].upper()+section[-1][1:]+"_v"+str(version)+"_JNT";
        upperSpine = py.duplicate(jointChain[-1], rr=1, po=1, rc=1, n=name)[0];
        py.parent(upperSpine,w=1);
        name = "c_"+side+"_lower"+section[-1][0].upper()+section[-1][1:]+"_v"+str(version)+"_JNT";
        lowerSpine = py.duplicate(jointChain[0], rr=1, po=1, rc=1, n=name)[0];
        py.skinCluster(spineCurve, lowerSpine, upperSpine, mi=3, nw=1, bm=0, sm=0, dr=4.0);
        curveShape = py.listRelatives(spineCurve, s=1);
        skin = py.listConnections(curveShape[0], t="skinCluster")[0];
        i=0;
        while(i < len(jointChain)):
            py.setAttr(jointChain[i]+".drawStyle", 2);
            i+=1;
        py.setAttr(spineCurve+".v", 0);py.setAttr(primaryIK+".v", 0);
        py.setAttr(upperSpine+".v", 0);py.setAttr(lowerSpine+".v", 0);
        py.skinPercent(skin, spineCurve+".cv[7]", tv=[(lowerSpine, 0.000), (upperSpine, 1.000)]);
        py.skinPercent(skin, spineCurve+".cv[6]", tv=[(lowerSpine, 0.142), (upperSpine, 0.858)]);
        py.skinPercent(skin, spineCurve+".cv[5]", tv=[(lowerSpine, 0.285), (upperSpine, 0.715)]);
        py.skinPercent(skin, spineCurve+".cv[4]", tv=[(lowerSpine, 0.428), (upperSpine, 0.572)]);
        py.skinPercent(skin, spineCurve+".cv[3]", tv=[(lowerSpine, 0.572), (upperSpine, 0.428)]);
        py.skinPercent(skin, spineCurve+".cv[2]", tv=[(lowerSpine, 0.715), (upperSpine, 0.285)]);
        py.skinPercent(skin, spineCurve+".cv[1]", tv=[(lowerSpine, 0.858), (upperSpine, 0.142)]);
        py.skinPercent(skin, spineCurve+".cv[0]", tv=[(lowerSpine, 1.000), (upperSpine, 0.000)]);  
###############################################################################
#"""# MEASURE JOINT LENGTHS                                                   #
###############################################################################
        distanceNodeShape = py.distanceDimension(sp=(0, 100, 0), ep=(0, 10, 0));
        distanceLocators = py.listConnections(distanceNodeShape);
        distanceNode = py.listRelatives(distanceNodeShape, p=1);
        jointLengths = [];
        i = 0;
        while(i < len(bindJointChain)-1):
            snap = py.pointConstraint(bindJointChain[i],distanceLocators[0], mo=0, w=1);
            py.delete(snap);
            snap = py.pointConstraint(bindJointChain[i+1],distanceLocators[1],mo=0,w=1);
            py.delete(snap);
            currentMeasurement = py.getAttr(distanceNodeShape+".distance");
            jointLengths.append(currentMeasurement);
            i+=1;        
        py.delete(distanceNode, distanceLocators);
        spineLength = jointLengths[-1];
        controllerSize = spineLength/2.5 if(posture == "biped") else jointLengths[0]/1.5;
###############################################################################
#"""# CREATE MATERIAL                                                         #
###############################################################################
        MAT = [side+str(section[len(section)-1]).upper()+str(version)+"_MAT"];
        i=0;
        while(i < len(MAT)):
            if(py.objExists(MAT[i]) == 0):
                ctrlShader = py.shadingNode("blinn", asShader=1, n=MAT[i]);
                shadingGRP = py.sets(renderable=1,noSurfaceShader=1,empty=1);
                py.connectAttr('%s.outColor'%ctrlShader,'%s.surfaceShader'%shadingGRP);
                py.setAttr(MAT[i]+".incandescence", 0,0,0);
                py.setAttr(MAT[i]+".color", 0,0.1777/3,0.4421/3);
                py.setAttr(MAT[i]+".ambientColor", 0,0.1777,0.4421);
                py.setAttr(MAT[i]+".diffuse", 1.0);
                py.setAttr(MAT[i]+".transparency", 0,0,0);
                py.setAttr(MAT[i]+".translucenceDepth",0);
                py.setAttr(MAT[i]+".translucenceFocus",0);
                py.setAttr(MAT[i]+".reflectivity",0);
                py.setAttr(MAT[i]+".eccentricity",0);
                py.setAttr(MAT[i]+".specularRollOff",0);
                py.setAttr(MAT[i]+".specularColor",0,0,0);
                py.setAttr(MAT[i]+".ihi", 0);
                py.disconnectAttr(MAT[i]+".msg", "defaultShaderList1.s", na=1);
            i+=1;
###############################################################################
#"""# COLOR OPTIONS                                                           #
###############################################################################
        colorOptions = "RED:BLUE:GREEN:YELLOW:PURPLE:ORANGE:TEAL:BLACK:WHITE:"
        primaryColors = [4,15,23,25,8,12,28,1,3];#0-31
        secondaryColors = [13,29,19,17,30,24,19,2,16];#0-31
        colorValues = [[0.7971,0,0],[0,0.1777,0.4421],[0.0506,1,0.0506],
                       [1,0.9988,0],[0.1949,0.0123,0.1478],[0.9567,0.4601,0],
                       [0,1,0.6006],[0.01,0.01,0.01],[1,1,1]];     
        colorOptionsAmount = colorOptions.split(":")[:-1];
        py.addAttr(primaryIK, ln="COLOR", at="enum", en=colorOptions, dv=1);
        py.addAttr(primaryIK, ln="firstCOLOR", at="long", min=0, max=31, dv=1);
        py.addAttr(primaryIK, ln="secondCOLOR",at="long", min=0, max=31, dv=1);
        py.setAttr(primaryIK+".COLOR", k=1, e=1);
        py.setAttr(primaryIK+".firstCOLOR", k=1, e=1);
        py.setAttr(primaryIK+".secondCOLOR", k=1, e=1);
        py.setAttr(primaryIK+".COLOR", k=1, e=1);
        i=0;
        while(i < len(colorOptionsAmount)):
            index = ["R","G","B"];
            py.setAttr(primaryIK+".COLOR",i);
            py.setAttr(primaryIK+".firstCOLOR",primaryColors[i]);
            py.setDrivenKeyframe(primaryIK+".firstCOLOR",cd=primaryIK+".COLOR");
            py.setAttr(primaryIK+".secondCOLOR",secondaryColors[i]);
            py.setDrivenKeyframe(primaryIK+".secondCOLOR",cd=primaryIK+".COLOR");
            ii=0;
            while(ii < len(colorValues[i])):
                targetColor = MAT[0]+".color"+index[ii];
                targetIncandescence = MAT[0]+".ambientColor"+index[ii];
                py.setAttr(targetColor,colorValues[i][ii]);
                py.setAttr(targetIncandescence,colorValues[i][ii]/3);
                py.setDrivenKeyframe(targetColor,cd=primaryIK+".COLOR");
                py.setDrivenKeyframe(targetIncandescence,cd=primaryIK+".COLOR");
                ii+=1;
            i+=1;
###############################################################################
#"""# CREATE CONTROLLERS                                                      #
###############################################################################
        controllers = [];
        shapes = [];
        counterGroups = [];
        groups = [];
        value = controllerSize*5;
        i=0;
        while(i < len(bindJointChain)-1):
            name = "c_"+side+"_"+section[i]+"_v"+str(version)+"_CTRL";
            if(i == 0 or i == len(bindJointChain)-2):
                if(posture == "biped"):
                    controller = py.polyCube(n=name,w=abs(value),d=abs(value),ax=(0,1,0),cuv=4,ch=1)[0];
                elif(posture == "quadruped"):
                    controller = py.polyCube(n=name,w=abs(value),d=abs(value),ax=(0,0,1),cuv=4,ch=1)[0];
            else:
                if(posture == "biped"):
                    controller = py.circle(ch=1, o=1, nr=(0, 1, 0), r=(controllerSize*3), n=name)[0];
                elif(posture == "quadruped"):
                    controller = py.circle(ch=1, o=1, nr=(0, 0, 1), r=(controllerSize*3), n=name)[0];
                py.setAttr(controller+"Shape.overrideEnabled", 1);
                py.connectAttr(primaryIK+".secondCOLOR",controller+"Shape.overrideColor");
            shapes.append(py.listConnections(controller+"Shape")[-1]);
            py.setAttr(controller+"Shape.ihi",0);
            name = "c_"+side+"_"+section[i]+"Counter_v"+str(version)+"_GRP";
            counterGroup = py.group(n=name, r=1);
            name = "c_"+side+"_"+section[i]+"_v"+str(version)+"_GRP";
            controllerGroup = py.group(n=name, r=1);
            py.move(0,-0.5,0, controller+".sp", r=1);
            py.setAttr(controller+".spty", 0.5);
            if(posture == "biped"):
                py.setAttr(controllerGroup+".sy", jointLengths[i]);
            else:
                py.setAttr(controllerGroup+".sz", jointLengths[i]);
            py.makeIdentity(controllerGroup, apply=1, s=1, n=0);
            py.setAttr(controller+".overrideEnabled", 1);
            snap1 = py.pointConstraint(bindJointChain[i],controllerGroup,mo=0,w=1);
            py.delete(snap1);
            attributes = [".primaryVisibility",".castsShadows",".receiveShadows",
                          ".visibleInReflections",".holdOut",".smoothShading",
                          ".motionBlur",".visibleInRefractions",".doubleSided",
                          ".opposite"];
            ii=0;              
            while(ii < len(attributes)):
                try:
                    py.setAttr(controller+"Shape"+attributes[ii], 0);
                except:
                    pass;
                ii+=1;
            if(i > 1 and style != "RiGGiE"):
                py.parent(controllerGroup, controllers[-1]);
            controllers.append(controller);
            counterGroups.append(counterGroup);
            groups.append(controllerGroup);
            i+=1; 
###############################################################################
#"""# CREATE HIP CONTROLLERS                                                  #
###############################################################################
        name = "c_"+side+"_"+section[-1]+"Master_v"+str(version)+"_CTRL";
        masterHipController = py.circle(ch=1,o=1,nr=(0,1,0),r=(controllerSize*5),n=name,s=20)[0];
        py.xform(masterHipController, p=1, roo="zyx");
        py.select(masterHipController, r=1);
        py.setAttr(masterHipController+"Shape.overrideEnabled", 1);
        py.connectAttr(primaryIK+".secondCOLOR",masterHipController+"Shape.overrideColor");
        py.setAttr(masterHipController+"Shape.ihi",0);
        name = "c_"+side+"_"+section[-1]+"MasterCounter_v"+str(version)+"_GRP";
        counterGroup = py.group(n=name, r=1);
        name = "c_"+side+"_"+section[-1]+"Master_v"+str(version)+"_GRP";
        controllerGroup = py.group(n=name, r=1);
        snap1 = py.pointConstraint(bindJointChain[0],controllerGroup,mo=0,w=1);
        py.delete(snap1);
        py.parent(groups[0], groups[1], masterHipController);
        py.move(controllerSize,0,controllerSize,masterHipController+"Shape.cv[10]",os=1,wd=1,r=1);
        py.move(0,0,controllerSize*2,masterHipController+"Shape.cv[11]",os=1,wd=1,r=1);
        py.move(controllerSize*-1,0,controllerSize,masterHipController+"Shape.cv[12]",os=1,wd=1,r=1);
###############################################################################
#"""# LOCK SETTINGS WITH ATTRIBUTE VALUES                                     #
###############################################################################
        py.addAttr(controllers[2], ln="ON", at="long", min=1, max=1, dv=1);
        py.setAttr(controllers[2]+".ON", l=1);
        py.addAttr(controllers[2], ln="OFF", at="long", min=0, max=0, dv=0);
        py.setAttr(controllers[2]+".OFF", l=1);
        i=0;
        while(i < len(controllers)):
            ii=0;                    
            while(ii < len(attributes)):
                try:
                    py.connectAttr(controllers[2]+".OFF", controllers[i]+attributes[ii]);
                except:
                    pass;
                ii+=1;
            i+=1;  
###############################################################################
#"""# CONNECT BIND JOINTS                                                     #
###############################################################################
        py.parent(bindJointChain[-2],bindJointChain[0]);
        i=0;ii=0;
        while(i < len(bindJointChain)-1):
            name = bindJointChain[i].replace(bindJointChain[i].split("_")[-1],"CON");
            if(i == 0):
                name = bindJointChain[i].replace(bindJointChain[i].split("_")[-1],"CON");
                constraint = py.parentConstraint(lowerSpine,bindJointChain[i],n=name,mo=1,w=1);
            elif(i == len(bindJointChain)-2):
                name = bindJointChain[i].replace(bindJointChain[i].split("_")[-1],"ONT");
                constraint = py.orientConstraint(upperSpine,bindJointChain[i],n=name,mo=1,w=1);
                name = bindJointChain[i].replace(bindJointChain[i].split("_")[-1],"PNT");
                pointConstraint = py.pointConstraint(controllers[-1],bindJointChain[i],n=name,mo=1,w=1);
                py.setAttr(pointConstraint[0]+".ihi",0);
            else:
                constraint = py.parentConstraint(jointChain[ii],bindJointChain[i],n=name,mo=1,w=1);
                py.connectAttr(jointChain[ii]+".sx",bindJointChain[i]+".sz");
                py.connectAttr(jointChain[ii]+".sy",bindJointChain[i]+".sx");
                py.connectAttr(jointChain[ii]+".sz",bindJointChain[i]+".sy");
            py.setAttr(constraint[0]+".ihi",0);
            i+=1;ii+=2;
###############################################################################
#"""# CONNECT SHAPES TO JOINTS AND DELETE EMPTY TRANSFORM NODES               #
###############################################################################
        i=0;
        while(i < len(jointChain)-1 and style == "RiGGiE"):
            py.setAttr(jointChain[i]+".radius", k=0, l=1);
            py.setAttr(jointChain[i]+".radius", cb=0);
            decoyShape = py.spaceLocator(p=(0,0,0),n=decoyJointChain[i][1:])[0];
            py.parent(decoyShape+"Shape", decoyJointChain[i], r=1, s=1);
            py.delete(decoyShape);
            if(section[2] not in jointChain[i]):
                py.parent(controllers[i]+"Shape", jointChain[i], r=1, s=1);
                py.setAttr(controllers[i]+"Shape.ihi",0);
                py.delete(groups[i]);
                py.rename(jointChain[i], jointChain[i].replace("JNT", "CTRL"));
            name = decoyJointChain[i].replace("Decoy", "");
            py.rename(decoyShape+"Shape", name.replace("JNT","DECOY"));
            i+=1;
###############################################################################
#"""# CREATE AND CONNECT WIREFRAME SHAPE NODES TO JOINTS THEN SHAPE THEM      #
###############################################################################
        nodes = controllers[:];
        if(style != "RiGGiE"):
            nodes.remove(nodes[1]);nodes.remove(nodes[1]);
            shapes.remove(shapes[1]);shapes.remove(shapes[1]);
        i=0;
        while(i < len(nodes)):
            decoy = py.duplicate(nodes[i], rc=1, rr=1)[0];
            py.delete(shapes[i], ch=1);
            wireShape = py.rename(decoy, decoy.replace("CTRL1", "WIRE"));
            py.setAttr(wireShape+".s", 1, 1.1, 1.1);
            py.makeIdentity(wireShape, pn=1, a=1, s=1, n=0);#FREEZE
            py.setAttr(wireShape+"Shape.overrideEnabled", 1);
            py.setAttr(wireShape+"Shape.overrideShading", 0);
            py.setAttr(wireShape+"Shape.overrideTexturing", 0);
            py.setAttr(wireShape+"Shape.hiddenInOutliner", 1);
            py.connectAttr(primaryIK+".firstCOLOR",wireShape+"Shape.overrideColor");
            py.connectAttr(nodes[i]+".overrideDisplayType",wireShape+"Shape.overrideDisplayType");
            py.connectAttr(primaryIK+".firstCOLOR",nodes[i]+".overrideColor");
            py.setAttr(nodes[i]+".overrideColor",k=0);
            py.parent(wireShape+"Shape", nodes[i], r=1, s=1);
            py.setAttr(wireShape+"Shape.ihi",0);
            py.delete(wireShape);
            bodyShape = nodes[i].replace(nodes[i][0:2], "a_");
            if(py.objExists(bodyShape) == 1):
                py.parent(bodyShape,nodes[i]);
                py.makeIdentity(bodyShape, pn=1, a=1, t=1, r=1, s=1, n=0);#FREEZE
                py.parent(bodyShape,w=1);
                shapeNode = py.listRelatives(bodyShape, type="shape");
                shapeNode = shapeNode[0] if(len(shapeNode) > 0) else shapeNode;
                py.parent(shapeNode, nodes[i], r=1, s=1);
                if("pelvis" in nodes[i]):
                    py.setAttr(shapeNode+".template", 1);
                py.rename(shapeNode, bodyShape+"Shape");
                py.setAttr(bodyShape+"Shape.ihi", 0);
                py.setAttr(nodes[i]+"Shape.visibility", 0);
                py.delete(bodyShape);
            py.select(nodes[i], r=1);    
            py.hyperShade(assign=MAT[0]);
            i+=1;
        nodes = jointChain;
        i=0;
        while(i < len(nodes)):
            bodyShape = nodes[i].replace(nodes[i][0:2], "a_");
            if(py.objExists(bodyShape) == 1):
                py.parent(bodyShape,nodes[i]);
                py.makeIdentity(bodyShape, pn=1, a=1, t=1, r=1, s=1, n=0);#FREEZE
                py.parent(bodyShape,w=1);
                shapeNode = py.listRelatives(bodyShape, type="shape");
                shapeNode = shapeNode[0] if(len(shapeNode) > 0) else shapeNode;
                py.parent(shapeNode, nodes[i], s=1);
                py.setAttr(shapeNode+".template", 1);
                py.rename(shapeNode, bodyShape+"Shape");
                py.delete(bodyShape);
            i+=1;
###############################################################################
#"""# ADD TWIST FUNCTION                                                      #
###############################################################################
        py.setAttr(primaryIK+".dTwistControlEnable", 1);
        py.setAttr(primaryIK+".dWorldUpType", 4);
        py.setAttr(primaryIK+".dForwardAxis", 2);
        py.setAttr(primaryIK+".dWorldUpAxis", 4);
        py.setAttr(primaryIK+".dWorldUpVector", 0,0,0);
        py.setAttr(primaryIK+".dWorldUpVectorEnd", 0,0,0);
        if(posture == "biped"):
            py.setAttr(primaryIK+".dWorldUpVectorZ", -1);
            py.setAttr(primaryIK+".dWorldUpVectorEndZ", -1);
        else:
            py.setAttr(primaryIK+".dWorldUpVectorY", 1);
            py.setAttr(primaryIK+".dWorldUpVectorEndY", 1);
        py.connectAttr(controllers[0]+".worldMatrix[0]", primaryIK+".dWorldUpMatrix", f=True);
        py.connectAttr(controllers[-1]+".worldMatrix[0]", primaryIK+".dWorldUpMatrixEnd", f=True);
###############################################################################
#"""# ADD STRETCH FUNCTION                                                    #
###############################################################################
        curveShape= py.listRelatives(spineCurve, type="shape");
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_CRVShape"
        py.rename(curveShape[0], name);
        name = "c_"+side+"_"+section[-1]+"Stretch_v"+str(version)+"_CDN";
        stretch = py.createNode("multiplyDivide", n=name);
        py.setAttr(stretch+".operation", 2);
        py.setAttr(stretch+".input2X", arcLength);
        py.connectAttr(curveInfo+".arcLength", stretch+".input1X");
        py.setAttr(stretch+".ihi",0);
        name = "c_"+side+"_"+section[-1]+"Power_v"+str(version)+"_CDN";
        power = py.createNode("multiplyDivide", n=name);
        py.setAttr(power+".operation", 3);py.setAttr(power+".input2X", 0.5);
        py.connectAttr(stretch+".outputX", power+".input1X");
        py.setAttr(power+".ihi",0);
        name = "c_"+side+"_"+section[-1]+"Squash_v"+str(version)+"_CDN";
        squash = py.createNode("multiplyDivide", n=name);
        py.setAttr(squash+".operation", 2);py.setAttr(squash+".input1X", 1);
        py.connectAttr(power+".outputX", squash+".input2X");
        py.setAttr(squash+".ihi",0);
        i=0;
        while(i < len(jointChain)-1):
            name = "c_"+side+"_"+section[-1]+"Zero_v"+str(version)+"_CDN";
            zeroCondition = py.createNode("condition", n=name);
            py.connectAttr(curveInfo+".arcLength", zeroCondition+".firstTerm");
            py.setAttr(zeroCondition+".secondTerm",0);
            py.setAttr(zeroCondition+".operation", 1);
            py.connectAttr(squash+".outputX", zeroCondition+".colorIfTrueR");
            py.connectAttr(stretch+".outputX",zeroCondition+".colorIfTrueG");
            py.connectAttr(squash+".outputX", zeroCondition+".colorIfTrueB");
            py.setAttr(zeroCondition+".ihi",0);
            py.connectAttr(zeroCondition+".outColorR",jointChain[i]+".sx");
            py.connectAttr(zeroCondition+".outColorG",jointChain[i]+".sy");
            py.connectAttr(zeroCondition+".outColorB",jointChain[i]+".sz");
            i+=1;
###############################################################################
#"""# GROUP AND ORGANIZE                                                      #
###############################################################################
        name = "c_"+side+"_"+section[-1]+"Misc_v"+str(version)+"_GRP";
        subGroup = py.group(em=1, n=name);
        snap = py.pointConstraint(bindJointChain[0],subGroup, mo=0, w=1);
        py.delete(snap);
        name = "c_"+side+"_"+section[-1]+"_v"+str(version)+"_GRP";
        mainGroup = py.group(em=1, n=name);
        snap = py.pointConstraint(bindJointChain[0],mainGroup, mo=0, w=1);
        py.delete(snap);
        py.delete(bindJointChain[-1]);bindJointChain.remove(bindJointChain[-1]);
        if(style == "RiGGiE"):
            py.parent(lowerSpine,controllers[0]);
            py.parent(upperSpine,controllers[-1]);
            py.parent(spineCurve,primaryIK,subGroup);
            py.parent(jointChain,groups,subGroup,mainGroup);
        else:
            py.parent(lowerSpine,controllers[0]);
            py.parent(upperSpine,controllers[-1]);
            py.parent(spineCurve,primaryIK,subGroup);
            py.parent(jointChain[0],controllerGroup,subGroup,mainGroup);
###############################################################################
#"""# SET ROTATION ORDERS AND ADDING AN INDENTIFIER TAG                       #
###############################################################################
        i=0;
        while(i < len(controllers)):
            rotationOrders = "zyx" if(i > 0 or posture == "quadruped") else "yzx";
            py.xform(controllers[i], p=1, roo=rotationOrders);
            py.addAttr(controllers[i], ln="RiGGiE", dt="string");
            rotationOrder = py.getAttr(controllers[i]+".rotateOrder");
            py.addAttr(controllers[i], ln="ROTATE_ORDER", at="enum", en="XYZ:YZX:ZXY:XZY:YXZ:ZYX:", dv=0);
            py.setAttr(controllers[i]+".ROTATE_ORDER", k=0, cb=1, e=1);
            py.setAttr(controllers[i]+".ROTATE_ORDER", rotationOrder);
            py.connectAttr(controllers[i]+".ROTATE_ORDER",controllers[i]+".rotateOrder");
            try:
                py.connectAttr(controllers[i]+".overrideDisplayType",controllers[i]+"Shape.overrideDisplayType");
            except:
                pass;
            i+=1;
###############################################################################
#"""# CREATE BREATHING FUNCTION                                               #
###############################################################################
        name = "b_"+side+"_breath_v"+str(version)+"_JNT";
        breathJoint = py.duplicate(bindJointChain[-1], n=name, po=1)[0];
        radius = py.getAttr(breathJoint+".radius");
        py.setAttr(breathJoint+".tz", controllerSize*0.5);
        py.setAttr(breathJoint+".radius", radius*2);
        py.parent(breathJoint,bindJointChain[-1]);
        name = "c_"+side+"_breath_v"+str(version)+"_CTRL";
        breathController = py.circle(ch=1, o=1, nr=(0, 0, 1), r=(controllerSize), n=name)[0];
        py.setAttr(breathController+"Shape.ihi", 0);
        py.setAttr(breathController+"Shape.overrideEnabled", 1);
        py.connectAttr(breathController+".overrideDisplayType",breathController+"Shape.overrideDisplayType");
        py.connectAttr(primaryIK+".secondCOLOR",breathController+"Shape.overrideColor");
        name = "c_"+side+"_breath_v"+str(version)+"_GRP";
        breathGroup = py.group(n=name, r=1);
        snap = py.pointConstraint(jointChain[-2],jointChain[-1],breathGroup,mo=0,w=1);
        py.delete(snap);
        name = breathGroup.replace(breathGroup.split("_")[-1], "CON");
        constraint = py.parentConstraint(bindJointChain[-1],breathGroup,n=name, mo=1, w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        if(posture == "biped"):
            py.setAttr(breathController+".tz", jointLengths[-1]);
        elif(posture == "quadruped"):
            py.setAttr(breathGroup+".scalePivotTranslateY", jointLengths[-1]*-1.5);
            py.setAttr(breathController+".tz", jointLengths[-1]*2);
        py.transformLimits(breathController,ty=(controllerSize/-2,controllerSize/2),ety=(1,1));
        py.setDrivenKeyframe(breathJoint+".s", cd=breathController+".ty");
        py.setDrivenKeyframe(breathController+".s", cd=breathController+".ty");
        py.setAttr(breathController+".ty",controllerSize/2);
        py.setAttr(breathJoint+".s", 1.5,1.25,2);
        py.setAttr(breathController+".s", 1.5,1.25,2);
        py.setDrivenKeyframe(breathJoint+".s", cd=breathController+".ty");
        py.setDrivenKeyframe(breathController+".s", cd=breathController+".ty");
        py.setAttr(breathController+".ty",controllerSize/-2);
        py.setAttr(breathJoint+".s", 0.6,0.75,0.5);
        py.setAttr(breathController+".s", 0.6,0.75,0.5);
        py.setDrivenKeyframe(breathJoint+".s", cd=breathController+".ty");
        py.setDrivenKeyframe(breathController+".s", cd=breathController+".ty");
        py.keyTangent(breathJoint+".s",itt="linear",ott="linear",e=1);
        py.keyTangent(breathController+".s",itt="linear",ott="linear",e=1);
        py.setAttr(breathController+".ty",0);
        py.parent(breathGroup,subGroup);
###############################################################################
#"""# LOCK AND HIDE ATTRIBUTES                                                #
############################################################################### 
        name = "c_"+side+"_pivot_v"+str(version)+"_CTRL";
        pivotController = py.circle(ch=1,o=1,s=20,nr=(0,1,0),r=(controllerSize*7),n=name)[0];
        py.setAttr(pivotController+"Shape.overrideEnabled", 1);
        py.connectAttr(primaryIK+".firstCOLOR",pivotController+"Shape.overrideColor");
        py.move(controllerSize*2,0,controllerSize,pivotController+"Shape.cv[10]",os=1,wd=1,r=1);
        py.move(0,0,controllerSize*2,pivotController+"Shape.cv[11]",os=1,wd=1,r=1);
        py.move(controllerSize*-2,0,controllerSize,pivotController+"Shape.cv[12]",os=1,wd=1,r=1);
        py.setAttr(pivotController+"Shape.ihi", 0);
        name = "c_"+side+"_master_v"+str(version)+"_CTRL";
        masterController = py.duplicate(pivotController, rr=1, n=name)[0];
        py.connectAttr(primaryIK+".secondCOLOR",masterController+"Shape.overrideColor");
        py.setAttr(masterController+".s",1.5,1.5,1.5);
        py.makeIdentity(masterController, pn=1, a=1, s=1, n=0);#FREEZE
        name = "c_"+side+"_trajectory_v"+str(version)+"_CTRL";
        trajectoryController = py.polyPyramid(w=1, n=name)[0];
        py.setAttr(trajectoryController+"Shape.overrideEnabled", 1);
        py.connectAttr(primaryIK+".secondCOLOR",trajectoryController+"Shape.overrideColor");
        py.hyperShade(assign=MAT[0]);py.setAttr(trajectoryController+"Shape.ihi",0);
        py.move(0.353553,0,trajectoryController+".vtx[0:4]",yz=1,r=1);
        py.move(0,0.707107,trajectoryController+".vtx[0]",yz=1,r=1);
        py.move(0,0.707107,trajectoryController+".vtx[2]",yz=1,r=1);
        py.setAttr(trajectoryController+".s",controllerSize,controllerSize,controllerSize);
        py.addAttr(trajectoryController, ln="CAPSULE_HEIGHT", at="double", min=1, dv=1);
        py.setAttr(trajectoryController+".CAPSULE_HEIGHT", k=0, cb=1, e=1);
        py.addAttr(trajectoryController, ln="CAPSULE_DIAMETER", at="double", min=1, dv=1);
        py.setAttr(trajectoryController+".CAPSULE_DIAMETER", k=0, cb=1, e=1);
        #SET ROTATION ORDER FOR MASTER HIP CONTROLLER
        nodes = [masterController,pivotController,masterHipController,trajectoryController];
        i=0;
        while(i < len(nodes)):
            rotationOrders = "zxy";
            py.xform(nodes[i], p=1, roo=rotationOrders);
            py.addAttr(nodes[i], ln="RiGGiE", dt="string");
            rotationOrder = py.getAttr(nodes[i]+".rotateOrder");
            py.addAttr(nodes[i], ln="ROTATE_ORDER", at="enum", en="XYZ:YZX:ZXY:XZY:YXZ:ZYX:", dv=0);
            py.setAttr(nodes[i]+".ROTATE_ORDER", k=0, cb=1, e=1);
            py.setAttr(nodes[i]+".ROTATE_ORDER", rotationOrder);
            py.connectAttr(nodes[i]+".ROTATE_ORDER",nodes[i]+".rotateOrder");
            try:
                py.connectAttr(nodes[i]+".overrideDisplayType",nodes[i]+"Shape.overrideDisplayType");
            except:
                pass;
            i+=1;
        #HIDE ATTRIBUTES
        attributes = [".sx", ".sy", ".sz", ".v"];
        node = controllers[:];
        node.extend((masterHipController,trajectoryController));
        node.extend((pivotController,masterController));
        i=0;
        while(i < len(node)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(node[i]+attributes[ii], k=0, l=1);
                py.setAttr(node[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
        attributes = [".tx", ".ty", ".tz"];
        node = controllers[1:3];
        i=0;
        while(i < len(node)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(node[i]+attributes[ii], k=0, l=1);
                py.setAttr(node[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
        attributes = [".tx",".tz",".rx",".ry",".rz",".sx",".sy",".sz",".v"];
        node = [breathController];
        i=0;
        while(i < len(node)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(node[i]+attributes[ii], k=0, l=1);
                py.setAttr(node[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
        py.addAttr(masterController, ln="MAIN_COLOR", at="enum", en=colorOptions, dv=1);
        py.setAttr(masterController+".MAIN_COLOR", k=0, cb=1, e=1);
        py.connectAttr(masterController+".MAIN_COLOR", primaryIK+".COLOR");
        py.addAttr(masterController, ln="LEFT_COLOR", at="enum", en=colorOptions, dv=1);
        py.setAttr(masterController+".LEFT_COLOR", k=0, cb=1, e=1);
        py.addAttr(masterController, ln="RIGHT_COLOR", at="enum", en=colorOptions, dv=1);
        py.setAttr(masterController+".RIGHT_COLOR", k=0, cb=1, e=1);
        py.addAttr(masterController,ln="TRANSPARENCY",at="double",min=0,max=100,dv=0);
        py.setAttr(masterController+"."+"TRANSPARENCY", k=0, cb=1, e=1);                   
        py.addAttr(masterController, ln="RIG_TYPE", at="enum", en="BODY:FACE:BOTH:", dv=0);
        py.setAttr(masterController+".RIG_TYPE", k=0, cb=1, e=1);
        py.addAttr(masterController, ln="CAPSULE", at="enum", en="OFF:ON:", dv=0);
        py.setAttr(masterController+".CAPSULE", k=0, cb=1, e=1);
        py.addAttr(masterController, ln="GUIDE", at="enum", en="OFF:ON:", dv=0);
        py.setAttr(masterController+".GUIDE", k=0, cb=1, e=1);
        py.addAttr(masterController, ln="LOOP", at="enum", en="False:True:", dv=0);
        py.setAttr(masterController+".LOOP", k=0, cb=0, e=1);
        py.addAttr(masterController, ln="RIG", at="enum", en="TRADITIONAL:HYBRID:", dv=0);
        #py.setAttr(masterController+".RIG", k=0, cb=1, e=1);
###############################################################################
#"""# CREATE SPINE CONNECTION ATTRIBUTES TO SHAPE NODES                       #
############################################################################### 
        attributes = ["translate", "rotate", "MODE", "SPACE"];
        animatorNodes = controllers[:];
        animatorNodes.append(masterHipController);
        i=0;
        while(i < len(animatorNodes)):
            otherNodes = animatorNodes[:];
            index = [l for l, s in enumerate(otherNodes) if animatorNodes[i].split("_")[2] in s][0];
            otherNodes.remove(otherNodes[index]);
            ii=0;
            while(ii < len(otherNodes)):
                iii=0;
                while(iii < len(attributes)):
                    if(py.attributeQuery(attributes[iii],node=otherNodes[ii],ex=1) == 1):#EXISTS?
                        if(py.getAttr(otherNodes[ii]+"."+attributes[iii], l=1) == 0):#UNLOCKED?
                            name = otherNodes[ii].split("_")[2]+"_"+attributes[iii];
                            vectorCheck = py.attributeQuery(attributes[iii],node=otherNodes[ii],lc=1);
                            if(isinstance(vectorCheck,list) == 1):
                                #IF VECTOR
                                py.addAttr(animatorNodes[i]+"Shape",ln=name,at="double3");
                                iiii=0;
                                while(iiii < len(axis)):
                                    py.addAttr(animatorNodes[i]+"Shape",ln=name+axis[iiii].upper(),p=name,at="double");
                                    iiii+=1;
                                iiii=0;
                                while(iiii < len(vectorCheck)):
                                    if(py.getAttr(otherNodes[ii]+"."+vectorCheck[iiii], k=1) == 1):
                                        py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), k=1, e=1);
                                    else:
                                        py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), k=0, e=1);
                                        py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), cb=0, e=1);
                                    iiii+=1;
                            elif(py.attributeQuery(attributes[iii],node=otherNodes[ii],e=1) == 1):
                                #IF ENUM
                                options = py.addAttr(otherNodes[ii]+"."+attributes[iii],en=1,q=1);
                                py.addAttr(animatorNodes[i]+"Shape",ln=name,at="enum",en=options,dv=0);
                            else:
                                #IF FLOAT
                                py.addAttr(animatorNodes[i]+"Shape",ln=name,at="double");
                            py.setAttr(animatorNodes[i]+"Shape."+name, k=1, e=1);
                    iii+=1;
                ii+=1;
            py.setAttr(animatorNodes[i]+"Shape.hiddenInOutliner", 1);
            i+=1;
###############################################################################
#"""# CONNECT CHILDREN TO SPINE                                               #
###############################################################################
        headExists = False;
        i=0;
        while(i < len(bindJointChain)):
            if(len(children[i]) > 0):
                py.parent(children[i], bindJointChain[i]);
            if(i == len(bindJointChain)-1 and len(children[i+1]) > 0):
                py.parent(children[i+1], bindJointChain[i]);
            i+=1;
        if(len(children) > 0):#!
            i=0;
            while(i < len(children)):
                ii=0;
                while(ii < len(children[i])):
                    py.select(children[i][ii], hi=1, r=1);
                    #joints = py.ls(sl=1,type="joint");
                    sidePosition = py.xform(children[i][ii],q=1,t=1,ws=1)[0];
                    upPosition = py.xform(children[i][ii],q=1,t=1,ws=1)[1];
                    forwardPosition = py.xform(children[i][ii],q=1,t=1,ws=1)[2];
                    if(posture == "biped" and round(sidePosition,0) == 0.0 and round(upPosition,0) > round(masterPosition[1],0)):
                        #BIPED HEAD
                        segment("head", bindJointChain[-1],subGroup,"none",primaryIK);
                        headExists = True;
                    elif(posture == "quadruped" and round(sidePosition,0) == 0.0 and round(forwardPosition,0) > round(masterPosition[2],0)):
                        #QUADRUPED HEAD
                        segment("head", bindJointChain[-1],subGroup,"none",primaryIK);
                        headExists = True;
                    elif(posture == "quadruped" and round(sidePosition,0) == 0.0 and round(forwardPosition,0) <= round(masterPosition[2],0)):
                        #QUADRUPED TAIL
                        segment("tail", bindJointChain[0],subGroup,"none",primaryIK);
                    else:
                        #LIMB
                        limb(style,posture);    
                    ii+=1;
                i+=1;
###############################################################################
#"""# ADD PICKWALK ATTRIBUTES TO SHAPE NODES                                  #
###############################################################################
        animatorNodes = controllers[:];
        animatorNodes.insert(0,masterHipController);
        if(headExists == True):
            neck = controllers[0].replace(controllers[0].split("_")[2],"neck");
            if(py.objExists(neck) == 1):
                animatorNodes.append(neck);
            head = controllers[0].replace(controllers[0].split("_")[2],"head");
            if(py.objExists(head) == 1):
                animatorNodes.append(head);
            if(py.objExists(head.replace("head","headOptionsBox")) == 1):
                animatorNodes.append(head.replace("head","headOptionsBox"));
        animatorNodes.insert(len(animatorNodes),animatorNodes[0]);
        animatorNodes.insert(0,animatorNodes[-2]);
        i=1;
        while(i < len(animatorNodes)-1):
            shapeNode = animatorNodes[i]+"Shape";
            py.addAttr(shapeNode,ln="UP"+animatorNodes[i-1], at="long");
            py.setAttr(shapeNode+".UP"+animatorNodes[i-1],l=1,cb=1,e=1);
            py.addAttr(shapeNode,ln="DOWN"+animatorNodes[i+1], at="long");
            py.setAttr(shapeNode+".DOWN"+animatorNodes[i+1],l=1,cb=1,e=1);
            i+=1;
###############################################################################
#"""# CREATE DEGREE WHEEL                                                     #
###############################################################################
        mel.eval("cycleCheck -e off");
        degrees = ["0","330","315","300","270","240","225","210",
                   "180","150","135","120","90","60","45","30"];
        pathPos = [0.0, 0.083, 0.125, 0.167, 0.25, 0.333, 0.375, 0.417, 
                   0.5, 0.583, 0.625, 0.667, 0.75, 0.833, 0.875, 0.917];
        name = "c_"+side+"_degreeWheel_v"+str(version)+"_DECOY";
        degreeGraph = py.circle(ch=1,o=1,s=16,nr=(0,-1,0),r=(controllerSize*9.5),n=name)[0];
        degreeList = [];
        i=0;iii=1;
        while(i < len(degrees)):
            angle = py.textCurves(f="Tahoma",t=degrees[i])[0];
            name = "c_"+side+"_degree"+degrees[i][:-1]+"_v"+str(version)+"_GRP";
            angle = py.rename(angle,name);
            allItems = py.listRelatives(angle,type="transform",ad=1,c=1);
            #RENAME SUB CURVE PARTS
            ii=0;
            while(ii < len(allItems)):
                num = allItems[ii][-1];
                if("curve" in allItems[ii]):
                    name = "c_"+side+"_degree"+degrees[i][:-1]+"Part"+str(num)+"_v"+str(version)+"_CURVE";
                else:
                    name = "c_"+side+"_degree"+degrees[i][:-1]+"Part"+str(num)+"_v"+str(version)+"_GRP";
                py.rename(allItems[ii],name);
                ii+=1;iii+=1;
            fontSize = controllerSize/1.5 if(i!=0 and i!=4 and i!=8 and i!=12) else controllerSize;
            py.xform(angle,cp=1);py.setAttr(angle+".template",1);
            py.setAttr(angle+".s",fontSize,fontSize,fontSize);
            path = py.pathAnimation(angle,degreeGraph,wut="vector",wu=[0,1,0],ua="z",fa="x",fm=1,f=1);
            py.setAttr(path+".uValue",pathPos[i]);
            translations = list(py.getAttr(angle+".t")[0]);
            rotations = list(py.getAttr(angle+".r")[0]);py.delete(path);
            py.setAttr(angle+".t",translations[0],translations[1],translations[2]);
            py.setAttr(angle+".r",rotations[0],rotations[1],rotations[2]);
            degreeList.append(angle);
            i+=1;
        py.select("makeText*");
        makeTextNodes = py.ls(sl=1);
        py.delete(makeTextNodes);
        py.parent(degreeList[:],degreeGraph);
        py.setAttr(degreeGraph+"Shape.v",0);
        py.setAttr(degreeGraph+".hiddenInOutliner", 1);
        py.setAttr(degreeGraph+".hideOnPlayback",1);
        name = "c_"+side+"_degreeWheel_v"+str(version+1)+"_DECOY";
        degreeGraphV2 = py.duplicate(degreeGraph, n=name)[0];
        py.setAttr(degreeGraphV2+".s",0.75,0.75,0.75);
        py.setAttr(degreeGraphV2+".v",0);
        i=0;
        while(i < len(axis)):
            #LOCK FIRST DEGREE WHEEL'S ATTRIBUTES
            py.setAttr(degreeGraph+".t"+axis[i].lower(),cb=0,k=0);
            py.setAttr(degreeGraph+".r"+axis[i].lower(),cb=0,k=0);
            py.setAttr(degreeGraph+".s"+axis[i].lower(),l=1);
            py.setAttr(degreeGraph+".v",cb=1,k=0);
            #LOCK SECOND DEGREE WHEEL'S ATTRIBUTES
            py.setAttr(degreeGraphV2+".t"+axis[i].lower(),cb=0,k=0);
            py.setAttr(degreeGraphV2+".r"+axis[i].lower(),cb=0,k=0);
            py.setAttr(degreeGraphV2+".s"+axis[i].lower(),l=1);
            py.setAttr(degreeGraphV2+".v",cb=0,k=0);
            i+=1;
        py.setAttr(degreeGraph+".overrideEnabled",1);
        py.setAttr(degreeGraphV2+".overrideEnabled",1);
        py.setAttr(degreeGraphV2+".hideOnPlayback", 1);
        py.connectAttr(masterController+".overrideVisibility",degreeGraph+".overrideVisibility");
        py.connectAttr(masterController+".overrideVisibility",degreeGraphV2+".overrideVisibility");
        distanceNodeShape = py.distanceDimension(sp=(0, 100, 0), ep=(0, 10, 0));
        distanceLocators = py.listConnections(distanceNodeShape);
        distanceNode = py.listRelatives(distanceNodeShape, p=1);
        distanceNode = py.rename(distanceNode,"c_"+side+"_distance_v"+str(version+1)+"_DDN");
        start = py.rename(distanceLocators[0],"c_"+side+"_startDistance_v"+str(version+1)+"_LOC");
        end = py.rename(distanceLocators[1],"c_"+side+"_endDistance_v"+str(version+1)+"_LOC");
        py.setAttr(start+".v",0);py.setAttr(end+".v",0);
        name = start.replace(start.split("_")[-1], "PNT");
        constraint = py.pointConstraint(degreeGraph,start,n=name,mo=0,w=1);
        name = end.replace(end.split("_")[-1], "PNT");
        constraint = py.pointConstraint(degreeGraphV2,end,n=name,mo=0,w=1);
        py.parent(distanceNode,start,end,subGroup); 
        name = degreeGraph.replace(degreeGraph.split("_")[-1],"PNT");
        constraint = py.pointConstraint(pivotController,degreeGraph,n=name,mo=0,w=1);
        name = degreeGraphV2.replace(degreeGraphV2.split("_")[-1],"PNT");
        constraint = py.pointConstraint(masterHipController,degreeGraphV2,n=name,mo=0,w=1);
        py.setAttr(distanceNode+".v",0);
        initialDistance = py.getAttr(distanceNode+"Shape.distance");
        name = "c_"+side+"_visibilityState_v"+str(version)+"_CDN";
        VS = py.createNode("condition", n=name);
        py.connectAttr(distanceNode+"Shape.distance",VS+".firstTerm");
        py.setAttr(VS+".secondTerm", initialDistance*1.25);
        py.setAttr(VS+".operation", 4);py.setAttr(VS+".ihi",0);
        py.setAttr(VS+".colorIfTrue", 1,0,1);
        py.setAttr(VS+".colorIfFalse",0,1,0); 
        py.connectAttr(VS+".outColorR", degreeGraph+".v"); 
        py.connectAttr(VS+".outColorG", degreeGraphV2+".v"); 
        mel.eval("cycleCheck -e on");
###############################################################################
#"""# CREATE AND SPINE/CHARACTER TRAJECTORY AND GROUP NODES                   #
###############################################################################
        name = "b_"+side+"_origin_v"+str(version)+"_JNT";py.select(d=1);
        root = py.joint(n=name);
        name = "b_"+side+"_trajectory_v"+str(version)+"_JNT";py.select(d=1);
        trajectory = py.joint(p=(0,0,0),n=name);
        py.parent(bindJointChain[0], trajectory, root);
        name = trajectory.replace(trajectory.split("_")[-1], "CON");
        constraint = py.parentConstraint(trajectoryController,trajectory,n=name,mo=1,w=1);
        py.setAttr(constraint[0]+".ihi", 0);
        name = "c_"+side+"_character_v"+str(version)+"_GRP";
        characterGroup = py.group(n=name, em=1);
        name = "c_"+side+"_weapon_v"+str(version)+"_GRP";
        weaponGroup = py.group(n=name, em=1);
###############################################################################
#"""# CREATE CAPSULE                                                          #
###############################################################################
        currentMeasurmentType = py.currentUnit(l=1,q=1);
        py.currentUnit(l="cm");
        #CREATE TOP OF CAPSULE
        name = "a_"+side+"_capsuleTop_v"+str(version)+"_GEO";
        capsuleTop = py.polySphere(n=name,sx=20,sy=20,ax=[0,1,0],r=0.5)[0];
        py.select(capsuleTop+".f[0:179]",capsuleTop+".f[360:379]",r=1);
        py.delete();py.delete(capsuleTop,ch=1);
        py.move(0,0.5,0, capsuleTop+".sp", r=1);
        capsuleTopLocator = py.spaceLocator(p=(0,0,0))[0];
        py.parent(capsuleTopLocator,capsuleTop);
        py.setAttr(capsuleTopLocator+".v",0);
        py.setAttr(capsuleTop+".ty",0.5);
        py.setAttr(capsuleTop+".hideOnPlayback", 0);
        py.setAttr(capsuleTop+".overrideEnabled", 1);
        py.setAttr(capsuleTop+".overrideDisplayType", 1);
        #CREATE MIDDLE OF CAPSULE
        name = "a_"+side+"_capsuleMiddle_v"+str(version)+"_GEO";
        capsuleMiddle = py.polyCylinder(n=name,sx=20,sy=1,sz=1,ax=[0,1,0],r=0.5)[0];
        py.select(capsuleMiddle+".f[20:59]",r=1);
        py.delete();py.delete(capsuleMiddle,ch=1);
        py.setAttr(capsuleMiddle+".ty",0.5);
        py.setAttr(capsuleMiddle+".sy",0);
        py.select(capsuleMiddle+".vtx[20:39]",r=1);
        name = "c_"+side+"_capsuleTop_v"+str(version)+"_CLST";
        capsuleTopCluster = py.cluster(n=name)[-1];
        py.setAttr(capsuleTopCluster+".v",0);
        py.setAttr(capsuleTopCluster+".hiddenInOutliner",1);
        py.select(capsuleMiddle+".vtx[0:19]",r=1);
        name = "c_"+side+"_capsuleBottom_v"+str(version)+"_CLST";
        capsuleBottomCluster = py.cluster(n=name)[-1];
        py.setAttr(capsuleBottomCluster+".v",0);
        py.setAttr(capsuleBottomCluster+".hiddenInOutliner",1);
        py.setAttr(capsuleMiddle+".inheritsTransform", 0);
        py.setAttr(capsuleMiddle+".hideOnPlayback", 0);
        py.setAttr(capsuleMiddle+".overrideEnabled", 1);
        py.setAttr(capsuleMiddle+".overrideDisplayType", 1);
        #CREATE BOTTOM OF CAPSULE
        name = "a_"+side+"_capsuleBottom_v"+str(version)+"_GEO";
        capsuleBottom = py.polySphere(n=name,sx=20,sy=20,ax=[0,1,0],r=0.5)[0];
        py.select(capsuleBottom+".f[180:359]",capsuleBottom+".f[380:399]",r=1);
        py.delete();py.delete(capsuleBottom,ch=1);
        py.move(0,-0.5,0, capsuleBottom+".sp", r=1);
        capsuleBottomLocator = py.spaceLocator(p=(0,0,0))[0];
        py.parent(capsuleBottomLocator,capsuleBottom);
        py.setAttr(capsuleBottomLocator+".v",0);
        py.setAttr(capsuleBottom+".ty",0.5);
        py.setAttr(capsuleBottom+".hideOnPlayback", 0);
        py.setAttr(capsuleBottom+".overrideEnabled", 1);
        py.setAttr(capsuleBottom+".overrideDisplayType", 1);
        #CREATE CAPSULE HIERARCHY
        name = "c_"+side+"_capsule_v"+str(version)+"_GRP";
        capsuleGroup = py.group(n=name,em=1);
        py.parent(capsuleTopCluster,capsuleTop);
        py.parent(capsuleBottomCluster,capsuleBottom);
        py.parent(capsuleTop,capsuleMiddle,capsuleBottom,capsuleGroup);
        py.parent(capsuleGroup,trajectoryController);
        #CONNECT ATTRIBUTES TO CONTROLLERS
        py.setAttr(capsuleTop+".ty",-0.5);
        py.makeIdentity(capsuleTop, a=1, t=1, n=0);#FREEZE
        py.connectAttr(trajectoryController+".CAPSULE_HEIGHT",capsuleTop+".ty");
        py.connectAttr(trajectoryController+".CAPSULE_DIAMETER",capsuleTop+".sx");
        py.connectAttr(trajectoryController+".CAPSULE_DIAMETER",capsuleTop+".sy");
        py.connectAttr(trajectoryController+".CAPSULE_DIAMETER",capsuleTop+".sz");      
        py.connectAttr(trajectoryController+".CAPSULE_DIAMETER",capsuleBottom+".sx");
        py.connectAttr(trajectoryController+".CAPSULE_DIAMETER",capsuleBottom+".sy");
        py.connectAttr(trajectoryController+".CAPSULE_DIAMETER",capsuleBottom+".sz");
        py.connectAttr(masterController+".CAPSULE",capsuleGroup+".v");
        #FINALIZE
        py.setAttr(trajectoryController+".CAPSULE_HEIGHT", 180);
        py.setAttr(trajectoryController+".CAPSULE_DIAMETER", 75);
        py.currentUnit(l=currentMeasurmentType);
###############################################################################
#"""# CONNECT MASTER CONTROLLER'S TRANSPARENCY ATTRIBUTE TO MATERIAL          #
###############################################################################
        py.setAttr(masterController+".TRANSPARENCY",0);
        py.setDrivenKeyframe(MAT[0]+".transparency",cd=masterController+".TRANSPARENCY");
        py.setAttr(masterController+".TRANSPARENCY",100);py.setAttr(MAT[0]+".transparency",1,1,1);
        py.setDrivenKeyframe(MAT[0]+".transparency",cd=masterController+".TRANSPARENCY");
        py.setAttr(masterController+".TRANSPARENCY",0);
###############################################################################
#"""# CREATE CHARACTER CAMERA                                                 #
###############################################################################
        name = "c_"+side+"_character_v"+str(version)+"_CAM";
        characterCamera = py.camera()[0];
        characterCamera = py.rename(characterCamera,name);
        snap = py.pointConstraint(controllers[-1],characterCamera,skip=["x","z"],mo=0,w=1);
        py.delete(snap);
        zValue = py.getAttr(characterCamera+".ty")*-1;
        py.setAttr(characterCamera+".tz",zValue);
        py.setAttr(characterCamera+".ry",180);py.setAttr(characterCamera+".v",0);
        py.setAttr(characterCamera+".sx",k=0);py.setAttr(characterCamera+".sy",k=0);
        py.setAttr(characterCamera+".sz",k=0);py.setAttr(characterCamera+".s",cb=0);
        py.parent(characterCamera,trajectoryController);
        initialCamera = py.lookThru(q=1);py.lookThru(characterCamera);
###############################################################################
#"""# FINALIZE SPINE/CHARACTER ATTRIBUTES AND HIERARCHY                       #
###############################################################################
        py.parent(mainGroup, weaponGroup, pivotController);
        py.parent(pivotController,trajectoryController,masterController);
        py.parent(masterController,degreeGraph,degreeGraphV2,characterGroup);
        py.select(controllers[-1],r=1);
        FrameSelected();
        py.setAttr(characterCamera+".tz",zValue);
        zValue = py.getAttr(characterCamera+".tz")*-1;
        py.setAttr(characterCamera+".centerOfInterest",zValue);
        py.lookThru(initialCamera);
        #py.setAttr(root+".drawStyle",2);py.setAttr(trajectory+".drawStyle",2);
        #py.setAttr(root+".template", 1);
        py.addAttr(masterController, ln="KEYALL", at="enum", en="OFF:ON:", dv=0);
        py.setAttr(masterController+".KEYALL", k=0, cb=1, e=1);
        py.addAttr(masterController, ln="VERSION", at="double", dv=VERSION);
        py.setAttr(masterController+".VERSION", k=0, l=1, cb=1, e=1);
        py.setAttr(root+".template",1);
        py.setAttr(root+".v",0);
###############################################################################
#"""# MAKE ALL GROUP NODES NOT KEYABLE                                        #
###############################################################################
        allAttributes = ["rotateX","rotateY","rotateZ",
                         "translateX","translateY","translateZ",
                         "scaleX","scaleY","scaleZ","visibility"];            
        py.select(characterGroup,hi=1);
        allGroupNodes = py.ls("*GRP",sl=1);
        i=0;
        while(i < len(allGroupNodes)):
            mayaAttributes = py.listAttr(allGroupNodes[i],st=allAttributes,k=1);
            mayaAttributes = [] if(isinstance(mayaAttributes,list) == 0) else mayaAttributes;
            userAttributes = py.listAttr(allGroupNodes[i],ud=1);
            userAttributes = [] if(isinstance(userAttributes,list) == 0) else userAttributes;
            keyableAttributes = mayaAttributes+userAttributes;
            ii=0;
            while(ii < len(keyableAttributes)):
                py.setAttr(allGroupNodes[i]+"."+keyableAttributes[ii],k=0);
                ii+=1;
            i+=1;
        #GROUP EVALUATION LOCATOR
        py.parent(evaluationLocator, characterGroup);
        py.setAttr(evaluationLocator+".s",0.01,0.01,0.01);
        py.setAttr(evaluationLocator+".template",1);
        py.setAttr(evaluationLocator+".hiddenInOutliner",1);
        if(py.objExists(evaluationLocator) == 1):
            py.connectAttr(switchSpaceCalculator+".output1D",evaluationLocator+".ry");
        if(py.objExists("a_M_adultMaleControllers_v1_GRP") == 1):
            py.delete("a_M_adultMaleControllers_v1_GRP");
        if(py.objExists("BaseAnimation") == 1):
            py.delete("BaseAnimation");
        py.displayPref(displayAffected=0);
        if(len(children) > 0):#!
            print '"Character successfully created!" - HiGGiE';
            py.headsUpMessage('"Character successfully created!" - HiGGiE', t=3);
        else:
            print '"Spine successfully created!" - HiGGiE';
            py.headsUpMessage('"Spine successfully created!" - HiGGiE', t=3);
    py.select(d=1);
###############################################################################
#.............................................................................#
#.............................................................................#
#"""# CREATES A SEGMENT                                                       #
#.............................................................................#
#.............................................................................#
###############################################################################
def segment(segmentName,owner,mainGroup,material,IK):
    axis = ["x","y","z"];
    initialJointSelection = py.ls(sl=1, type="joint");
    if(isinstance(initialJointSelection, list) == True):
        py.select(hi=1, r=1);
        initialSelectionHierarchy = py.ls(sl=1, type="joint");
    if(len(initialSelectionHierarchy) > 1):
        switchSpaceCalculator = "c_M_spaceSwitchCalculator_v1_PMA";
###############################################################################
#"""# CHECKS THE SEGMENT TYPE, POSITION AND VERSION OF THE JOIN CHAIN         #
###############################################################################
        section = [];
        middleSegmentNames = ["neck","head","tail","segment"];
        newJoints = py.duplicate(initialSelectionHierarchy, rc=1, rr=1);
        if(segmentName == "neck" or segmentName == "head"):
            section = ["neck", "head", "cranium"];
        else:
            i=0;
            while(i < len(newJoints)):
                section.append(segmentName+str(i+1));
                i+=1;
        if any(s in segmentName for s in middleSegmentNames):
            side = "M";
        else:
            side = "L" if(py.xform(newJoints[0],q=1,t=1,ws=1)[0]>0) else "R"; 
        reverse = -1 if(side == "R") else 1;
        version = 1;
        while(py.objExists("c_"+side+"_"+section[0]+"_v"+str(version)+"_CTRL")):
            version += 1;   
        i=0;
        while(i < len(newJoints)):
            py.makeIdentity(newJoints[i], apply=1, r=1, n=0);
            i+=1;
###############################################################################
#"""# MEASURE JOINT LENGTHS                                                   #
###############################################################################
        distanceNodeShape = py.distanceDimension(sp=(0, 100, 0), ep=(0, 10, 0));
        distanceLocators = py.listConnections(distanceNodeShape);
        distanceNode = py.listRelatives(distanceNodeShape, p=1);
        jointLengths = [];
        i = 0;
        while(i < len(newJoints)-1):
            snap = py.pointConstraint(newJoints[i],distanceLocators[0], mo=0, w=1);
            py.delete(snap);
            snap = py.pointConstraint(newJoints[i+1],distanceLocators[1],mo=0,w=1);
            py.delete(snap);
            currentMeasurement = py.getAttr(distanceNodeShape+".distance");
            jointLengths.append(currentMeasurement);
            i+=1;        
        py.delete(distanceNode, distanceLocators);
        controllerSize = jointLengths[0]/2.5;
###############################################################################
#"""# RENAME JOINT CHAINS                                                     #
###############################################################################
        bindJointChain = [];
        i = len(newJoints);
        newSection = [];
        while(i > 0):
            if(i == len(newJoints)-1 and section[-1] == "cranium"):
                name = "b_"+side+"_"+section[-2]+"_v"+str(version)+"_JNT";
            elif(len(newJoints) != 3 and section[-1] == "cranium"):
                name = "b_"+side+"_"+section[0]+str(i)+"_v"+str(version)+"_JNT";
            else:
                name = "b_"+side+"_"+section[i-1]+"_v"+str(version)+"_JNT";
            newSection.append(name.split("_")[-3]);
            newName = py.rename(newJoints[i-1], name);
            bindJointChain.append(newName);
            i-=1;
        section = newSection;
        section.reverse();
        bindJointChain.reverse();
        py.delete(initialJointSelection);
###############################################################################
#"""# CREATE CONTROLLERS                                                      #
###############################################################################
        jointChain = bindJointChain[:];
        controllers = [];
        shapes = [];
        counterGroups = [];
        groups = [];
        i=0;
        while(i < len(jointChain)-1):
            scaleMultiplier = 1 if("head" not in section[i]) else 2;
            value = controllerSize*scaleMultiplier;
            name = "c_"+side+"_"+section[i]+"_v"+str(version)+"_CTRL";
            if(side == "M"):
                controller = py.polyCube(n=name, w=abs(value), d=abs(value), ax=(0,1,0), cuv=4, ch=1)[0];
            else:
                controller = py.polyCube(n=name, h=abs(value), d=abs(value), ax=(0,1,0), cuv=4, ch=1)[0];
            shapes.append(py.listConnections(controller+"Shape")[-1]);
            py.setAttr(controller+"Shape.ihi",0);
            name = "c_"+side+"_"+section[i]+"Counter_v"+str(version)+"_GRP";
            counterGroup = py.group(n=name, r=1);
            name = "c_"+side+"_"+section[i]+"_v"+str(version)+"_GRP";
            controllerGroup = py.group(n=name, r=1);
            if(side == "M"):
                py.move(0,-0.5,0, controller+".sp", r=1);
                py.setAttr(controller+".spty", 0.5);
            else:
                py.move(-0.5,0,0, controller+".sp", r=1);
                py.setAttr(controller+".sptx", 0.5);
            attributes = [".primaryVisibility",".castsShadows",".receiveShadows",
                          ".visibleInReflections",".holdOut",".smoothShading",
                          ".motionBlur",".visibleInRefractions",".doubleSided",
                          ".opposite"];
            ii=0;              
            while(ii < len(attributes)):
                py.setAttr(controller+"Shape"+attributes[ii], 0);
                ii+=1;
            if(side == "M"):
                py.setAttr(controllerGroup+".sy", jointLengths[i]);
            else:
                py.setAttr(controllerGroup+".sx", jointLengths[i]*reverse);
            py.makeIdentity(controllerGroup, pn=1, a=1, s=1, n=0);
            
            py.setAttr(controller+".overrideEnabled", 1);
            if("head" not in section):
                snap = py.parentConstraint(jointChain[i],controllerGroup,mo=0,w=1);
                py.delete(snap);
            else:
                snap1 = py.aimConstraint(jointChain[i+1],controllerGroup,aim=(0,1,0),u=(0,0,1),wu=(0,0,1),wut="objectrotation",wuo=jointChain[i],mo=0,w=1);
                snap2 = py.pointConstraint(jointChain[i],controllerGroup,mo=0,w=1);
                py.delete(snap1,snap2);
            name = jointChain[i].replace(jointChain[i].split("_")[-1], "ONT");
            constraint = py.orientConstraint(controller,jointChain[i],n=name,mo=1,w=1);
            py.setAttr(constraint[0]+".ihi", 0);
            py.addAttr(controller, ln="RiGGiE", dt="string");
            controllers.append(controller);
            counterGroups.append(counterGroup);
            groups.append(controllerGroup);
            i+=1; 
###############################################################################
#"""# CREATE AND CONNECT WIRERAME SHAPE NODES TO JOINTS THEN SHAPE THEM       #
###############################################################################
        if(material == "none" and py.objExists("MSPINE1_MAT") == 1):
            MAT = "MSPINE1_MAT";
        else:
            MAT = material;
        nodes = controllers[:];
        i=0;
        while(i < len(nodes)):
            decoy = py.duplicate(nodes[i], rc=1, rr=1)[0];
            py.delete(shapes[i], ch=1);
            wireShape = py.rename(decoy, decoy.replace("CTRL1", "WIRE"));
            py.setAttr(wireShape+".s", 1, 1.1, 1.1);
            py.makeIdentity(wireShape, pn=1, a=1, s=1, n=0);#FREEZE
            py.setAttr(wireShape+"Shape.overrideEnabled", 1);
            py.setAttr(wireShape+"Shape.overrideShading", 0);
            py.setAttr(wireShape+"Shape.overrideTexturing", 0);
            py.setAttr(wireShape+"Shape.hiddenInOutliner", 1);
            if(py.objExists(IK) == 1):
                py.connectAttr(IK+".secondCOLOR",wireShape+"Shape.overrideColor");
                py.connectAttr(IK+".secondCOLOR",nodes[i]+".overrideColor");
            py.parent(wireShape+"Shape", nodes[i], r=1, s=1);
            py.setAttr(wireShape+"Shape.ihi",0);
            py.delete(wireShape);
            py.select(controllers[i], r=1);
            bodyShape = nodes[i].replace(nodes[i][0:2], "a_");
            if(py.objExists(bodyShape) == 1):
                py.parent(bodyShape,nodes[i]);
                py.makeIdentity(bodyShape, pn=1, a=1, t=1, r=1, s=1, n=0);#FREEZE
                py.parent(bodyShape,w=1);
                shapeNode = py.listRelatives(bodyShape, type="shape");
                shapeNode = shapeNode[0] if(len(shapeNode) > 0) else shapeNode;
                py.parent(shapeNode, nodes[i], r=1, s=1);
                py.rename(shapeNode, bodyShape+"Shape");
                py.setAttr(bodyShape+"Shape.ihi", 0);
                py.setAttr(nodes[i]+"Shape.visibility", 0);
                py.setAttr(wireShape+"Shape.visibility", 0);
                py.delete(bodyShape);
            py.select(nodes[i], r=1);    
            if(MAT != "none"):
                py.hyperShade(assign=MAT);
            i+=1;
###############################################################################
#"""# GROUP AND ORGANIZE                                                      #
###############################################################################
        type = "".join([x for x in section[-1] if not x.isdigit()]);
        name = "c_"+side+"_"+type+"_v"+str(version)+"_GRP";
        subGroup = py.group(em=1, n=name);
        snap = py.pointConstraint(jointChain[0],subGroup, mo=0, w=1);
        py.delete(snap);
        py.parent(groups[:], subGroup);
###############################################################################
#"""# CREATE SPACE LOCATOR                                                    #
############################################################################### 
        i=0;
        while(i < len(controllers)):
            name = "c_"+side+"_"+section[i]+"Space_v"+str(version)+"_LOC";
            spacePivotLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
            snap = py.parentConstraint(controllers[i],spacePivotLocator,mo=0,w=1);
            py.delete(snap);py.parent(spacePivotLocator, subGroup);
            py.addAttr(controllers[i], ln="SPACE", at="enum", en="WORLD:LOCAL:", dv=1);
            py.setAttr(controllers[i]+".SPACE", k=1, e=1);
            name = jointChain[i].replace(jointChain[i].split("_")[-1], "PNT");
            constraint = py.pointConstraint(spacePivotLocator,jointChain[i],n=name,mo=1,w=1);
            py.setAttr(constraint[0]+".ihi",0);
            name = groups[i].replace(groups[i].split("_")[-1], "PNT");
            constraint = py.pointConstraint(spacePivotLocator,groups[i],n=name,mo=1,w=1);
            py.setAttr(constraint[0]+".ihi",0);
            name = groups[i].replace(groups[i].split("_")[-1], "ONT");
            constraint = py.orientConstraint(spacePivotLocator,groups[i],n=name,mo=1,w=1);
            py.connectAttr(controllers[i]+".SPACE",constraint[0]+"."+spacePivotLocator+"W0");
            py.setAttr(constraint[0]+".ihi",0);py.setAttr(spacePivotLocator+".v",0);
            name = spacePivotLocator.replace(spacePivotLocator.split("_")[-1],"CON");
            if(owner != "none" and i == 0):
                if(py.objExists(owner) == 1 and py.objExists(mainGroup) == 1):
                    constraint = py.parentConstraint(owner,spacePivotLocator,n=name,mo=1,w=1);
                    py.setAttr(constraint[0]+".ihi",0);
                    py.parent(subGroup, mainGroup);
            py.setAttr(constraint[0]+".ihi",0);
            if(i > 0):
                constraint = py.parentConstraint(controllers[i-1],spacePivotLocator,n=name,mo=1,w=1);
                py.setAttr(constraint[0]+".ihi",0);
            i+=1;
###############################################################################
#"""# ADD OPTION BOX ANIMATION TO FINGER CONTROLLERS                          #
############################################################################### 
        fingers = ["pinky", "ring", "middle", "index", "thumb"]; 
        openValues = [20, 7, -15, -30, -25];
        closeValues = [-45, -17, 3, 20, 25];
        if any(section[0][:-1] in i for i in fingers):
            value = fingers.index(section[0][:-1])
            name = "c_"+side+"_"+section[-1]+"Misc_v"+str(version)+"_GRP";
            optionsBoxGroup = subGroup.replace(subGroup.split("_")[2],"armOptionsBox");
            optionsBox = optionsBoxGroup.replace(subGroup.split("_")[-1],"CTRL");
            if(py.objExists(optionsBox) == 1):
                limitX = py.getAttr(optionsBox+".maxTransXLimit");
                limitZ = py.getAttr(optionsBox+".maxTransZLimit");
                i=0;
                while(i < len(counterGroups)):
                    rotValue = -70 if("thumb" not in counterGroups[i]) else -15*(i+1);
                    py.setDrivenKeyframe(counterGroups[i]+".rz", cd=optionsBox+".tranX");
                    if("thumb1" in counterGroups[i]):
                        py.setDrivenKeyframe(counterGroups[i]+".rx", cd=optionsBox+".tranX");
                    py.setAttr(optionsBox+".tx",limitX);py.setAttr(counterGroups[i]+".rz",rotValue);  
                    py.setDrivenKeyframe(counterGroups[i]+".rz", cd=optionsBox+".tranX");
                    if("thumb1" in counterGroups[i]):
                        py.setAttr(counterGroups[i]+".rx",rotValue);  
                        py.setDrivenKeyframe(counterGroups[i]+".rx", cd=optionsBox+".tranX");
                    py.setAttr(optionsBox+".tx",limitX*-1);py.setAttr(counterGroups[i]+".rz",30);  
                    py.setDrivenKeyframe(counterGroups[i]+".rz", cd=optionsBox+".tranX");
                    py.setAttr(optionsBox+".tx",0);
                    if(i == 0):
                        py.setDrivenKeyframe(counterGroups[i]+".ry", cd=optionsBox+".tranZ");
                        py.setAttr(optionsBox+".tz",limitZ*-1);py.setAttr(counterGroups[i]+".ry",openValues[value]); 
                        py.setDrivenKeyframe(counterGroups[i]+".ry", cd=optionsBox+".tranZ");
                        py.setAttr(optionsBox+".tz",limitZ);py.setAttr(counterGroups[i]+".ry",closeValues[value]); 
                        py.setDrivenKeyframe(counterGroups[i]+".ry", cd=optionsBox+".tranZ");
                        py.setAttr(optionsBox+".tz",0);
                        py.keyTangent(counterGroups[i]+".ry",itt="linear",ott="linear",e=1);
                    py.keyTangent(counterGroups[i]+".rz",itt="linear",ott="linear",e=1);
                    i+=1;
###############################################################################
#"""# CREATE OPTIONS BOX                                                      #
###############################################################################
        if(section[-1] == "cranium"):
            name = "c_"+side+"_"+section[1]+"OptionsBox_v"+str(version)+"_CTRL";
            optionsBox = py.polyCube(n=name, w=abs(controllerSize/2.5), h=abs(controllerSize/2.5), d=abs(controllerSize/2.5), ax=(0,1,0), cuv=4, ch=1)[0];
            name = "c_"+side+"_"+section[1]+"OptionsBox_v"+str(version)+"_GRP";
            optionsBoxGroup = py.group(n=name, r=1);
            py.setAttr(optionsBox+"Shape.ihi",0);
            py.setAttr(optionsBox+"Shape.overrideEnabled", 1);
            py.setAttr(optionsBox+"Shape.overrideShading", 0);
            py.setAttr(optionsBox+"Shape.overrideTexturing", 0);
            py.connectAttr(IK+".secondCOLOR",optionsBox+"Shape.overrideColor");
            py.setAttr(optionsBox+"Shape.overrideDisplayType", 0);
            py.connectAttr(optionsBox+".overrideDisplayType",optionsBox+"Shape.overrideDisplayType");
            py.setAttr(optionsBox+"Shape.hideOnPlayback", 1);
            py.setAttr(optionsBox+".tz", controllerSize*-1.5);
            py.makeIdentity(optionsBox, a=1, t=1, n=0);#FREEZE
            py.setAttr(optionsBox+".tz",l=1,k=0);py.setAttr(optionsBox+".tz",cb=0);
            py.transformLimits(optionsBox,tx=(0,0),etx=(1,1));
            py.transformLimits(optionsBox,tz=(0,0),etz=(1,1));
            py.addAttr(optionsBox, ln="RiGGiE", dt="string");
###############################################################################
#"""# ADD OPTIONS BOX ATTRIBUTES                                              #
###############################################################################
            py.addAttr(optionsBox, ln="RESTRICTED", at="enum", en="OFF:ON:", dv=0);
            py.setAttr(optionsBox+".RESTRICTED", k=0, cb=1, e=1);
            rotationOrders = "xyz";
            py.xform(optionsBox, p=1, roo=rotationOrders);
            rotationOrder = py.getAttr(optionsBox+".rotateOrder");
            py.addAttr(optionsBox, ln="ROTATE_ORDER", at="enum", en="XYZ:YZX:ZXY:XZY:YXZ:ZYX:", dv=0);
            py.setAttr(optionsBox+".ROTATE_ORDER", k=0, cb=1, e=1);
            py.setAttr(optionsBox+".ROTATE_ORDER", rotationOrder);
            py.connectAttr(optionsBox+".ROTATE_ORDER",optionsBox+".rotateOrder");
###############################################################################
#"""# CONNECT SPACE ATTRIBUTES FROM OPTIONS BOX TO SEGMENT ATTRIBUTES         #
###############################################################################
            py.addAttr(optionsBox, ln="NECK_SPACE", at="enum", en="WORLD:LOCAL:", dv=0);
            py.setAttr(optionsBox+".NECK_SPACE", k=1, e=1);
            py.addAttr(optionsBox, ln="HEAD_SPACE", at="enum", en="WORLD:LOCAL:", dv=0);
            py.setAttr(optionsBox+".HEAD_SPACE", k=1, e=1);
            i=0;
            while(i < len(controllers)-1):
                py.connectAttr(optionsBox+".NECK_SPACE",controllers[i]+".SPACE");
                py.setAttr(controllers[i]+".SPACE", k=0, l=1);
                py.setAttr(controllers[i]+".SPACE", cb=0);
                i+=1;
            py.connectAttr(optionsBox+".HEAD_SPACE",controllers[-1]+".SPACE");
            py.setAttr(controllers[-1]+".SPACE",k=0,cb=0);
            py.addAttr(optionsBox, ln="SWITCH_NECK_SPACE", at="enum", en="----------:WORLD:LOCAL:", dv=0);
            py.setAttr(optionsBox+".SWITCH_NECK_SPACE", k=0, cb=1, e=1);
            py.addAttr(optionsBox, ln="SWITCH_HEAD_SPACE", at="enum", en="----------:WORLD:LOCAL:", dv=0);
            py.setAttr(optionsBox+".SWITCH_HEAD_SPACE", k=0, cb=1, e=1);
###############################################################################
#"""# POSITION OPTIONS BOX                                                    #
###############################################################################
            snap1 = py.pointConstraint(bindJointChain[0],optionsBoxGroup,mo=0,w=1);
            snap2 = py.orientConstraint(bindJointChain[0],optionsBoxGroup,mo=0,w=1);
            py.delete(snap1, snap2);py.delete(optionsBox, ch=1);
            name = optionsBoxGroup.replace(optionsBoxGroup.split("_")[-1], "CON");
            constraint = py.parentConstraint(bindJointChain[0],optionsBoxGroup,n=name,mo=1,w=1);
            py.setAttr(constraint[0]+".ihi", 0);
            py.parent(optionsBoxGroup,mainGroup);
###############################################################################
#"""# ADD PICKWALK ATTRIBUTES TO SHAPE NODES                                  #
###############################################################################
        animatorNodes = controllers[:];
        topController = controllers[-1];
        resetController = controllers[0];
        if any(section[0][:-1] in i for i in fingers):
            clavicle = controllers[0].replace(controllers[0].split("_")[2],"clavicle");
            shoulder = controllers[0].replace(controllers[0].split("_")[2],"shoulder");
            wrist = controllers[0].replace(controllers[0].split("_")[2],"wrist");
            if(py.objExists(clavicle) == 1):
                resetController = clavicle;
            elif(py.objExists(shoulder) == 1):
                resetController = shoulder;
            if(py.objExists(wrist) == 1):
                topController = wrist;
            animatorNodes.insert(len(animatorNodes),resetController);
            animatorNodes.insert(0,topController);
            i=1;
            while(i < len(animatorNodes)-1):
                py.addAttr(animatorNodes[i]+"Shape",ln="UP"+animatorNodes[i-1], at="long");
                py.setAttr(animatorNodes[i]+"Shape."+"UP"+animatorNodes[i-1],l=1,cb=1,e=1);
                py.addAttr(animatorNodes[i]+"Shape",ln="DOWN"+animatorNodes[i+1], at="long");
                py.setAttr(animatorNodes[i]+"Shape."+"DOWN"+animatorNodes[i+1],l=1,cb=1,e=1);
                i+=1; 
###############################################################################
#"""# ADD ATTRIBUTE RESTRICTIONS FEATURE (FOR REALISM)                        #
###############################################################################
            limbList = controllers[:];
            i=0;
            while(i < len(limbList)):
                #SET LOCK VALUES PER AXIS
                lockAxisMin = [-90,-90,-90];
                lockAxisMax = [90,90,90];
                #PLUG IN LOCK LIMITATIONS TO TARGET'S MIN AND MAX ROTATION LIMITS
                ii=0;
                while(ii < len(axis)):
                    py.connectAttr(optionsBox+".RESTRICTED",limbList[i]+".minRot"+axis[ii].upper()+"LimitEnable");
                    py.connectAttr(optionsBox+".RESTRICTED",limbList[i]+".maxRot"+axis[ii].upper()+"LimitEnable");
                    if(ii == 0):
                        py.transformLimits(limbList[i],rx=(lockAxisMin[ii],lockAxisMax[ii]),erx=(0,1));
                    if(ii == 1):
                        py.transformLimits(limbList[i],ry=(lockAxisMin[ii],lockAxisMax[ii]),ery=(0,1));
                    if(ii == 2):
                        py.transformLimits(limbList[i],rz=(lockAxisMin[ii],lockAxisMax[ii]),erz=(0,1));
                    ii+=1;
                i+=1;
###############################################################################
#"""# SET ROTATION ORDERS                                                     #
###############################################################################  
        i=0;
        while(i < len(controllers) and section[-1] == "cranium"):
            rotationOrders = "zxy";
            py.xform(controllers[i], p=1, roo=rotationOrders);
            rotationOrder = py.getAttr(controllers[i]+".rotateOrder");
            py.addAttr(controllers[i], ln="ROTATE_ORDER", at="enum", en="XYZ:YZX:ZXY:XZY:YXZ:ZYX:", dv=0);
            py.setAttr(controllers[i]+".ROTATE_ORDER", k=0, cb=1, e=1);
            py.setAttr(controllers[i]+".ROTATE_ORDER", rotationOrder);
            py.connectAttr(controllers[i]+".ROTATE_ORDER",controllers[i]+".rotateOrder");
            try:
                py.connectAttr(controllers[i]+".overrideDisplayType",controllers[i]+"Shape.overrideDisplayType");
            except:
                pass;
            i+=1;
###############################################################################
#"""# LOCK AND HIDE ATTRIBUTES                                                #
############################################################################### 
        attributes = [".tx", ".ty", ".tz",".sx", ".sy", ".sz", ".v", ".ro"];
        nodes = controllers[:];
        i=0;
        while(i < len(nodes)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(nodes[i]+attributes[ii], k=0, l=1);
                py.setAttr(nodes[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
        attributes = [".tx",".ty",".tz",".rx",".ry",".rz",".sx",".sy",".sz",".v"];
        nodes = counterGroups[:];
        if(section[-1] == "cranium"):
            nodes.append(optionsBox);
        i=0;
        while(i < len(nodes)):
            ii=0;
            while(ii < len(attributes)):
                py.setAttr(nodes[i]+attributes[ii], k=0, l=1);
                py.setAttr(nodes[i]+attributes[ii], cb=0);
                ii+=1;
            i+=1;
###############################################################################
#"""# CREATE HEAD CONNECTION ATTRIBUTES TO SHAPE NODES                        #
###############################################################################
        if(section[-1] == "cranium"):
            attributes = ["translate","rotate","MODE","NECK_SPACE","HEAD_SPACE"];
            animatorNodes = controllers[:]+[optionsBox];
            i=0;
            while(i < len(animatorNodes)):
                otherNodes = animatorNodes[:];
                index = [l for l, s in enumerate(otherNodes) if animatorNodes[i].split("_")[2] in s][0];
                otherNodes.remove(otherNodes[index]);
                ii=0;
                while(ii < len(otherNodes)):
                    iii=0;
                    while(iii < len(attributes)):
                        if(py.attributeQuery(attributes[iii],node=otherNodes[ii],ex=1) == 1):#EXISTS?
                            if(py.getAttr(otherNodes[ii]+"."+attributes[iii], l=1) == 0):#UNLOCKED?
                                name = otherNodes[ii].split("_")[2]+"_"+attributes[iii];
                                vectorCheck = py.attributeQuery(attributes[iii],node=otherNodes[ii],lc=1);
                                if(isinstance(vectorCheck,list) == 1):
                                    #IF VECTOR
                                    py.addAttr(animatorNodes[i]+"Shape",ln=name,at="double3");
                                    iiii=0;
                                    while(iiii < len(axis)):
                                        py.addAttr(animatorNodes[i]+"Shape",ln=name+axis[iiii].upper(),p=name,at="double");
                                        iiii+=1;
                                    iiii=0;
                                    while(iiii < len(vectorCheck)):
                                        if(py.getAttr(otherNodes[ii]+"."+vectorCheck[iiii], k=1) == 1):
                                            py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), k=1, e=1);
                                        else:
                                            py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), k=0, e=1);
                                            py.setAttr(animatorNodes[i]+"Shape."+name+axis[iiii].upper(), cb=0, e=1);
                                        iiii+=1;
                                elif(py.attributeQuery(attributes[iii],node=otherNodes[ii],e=1) == 1):
                                    #IF ENUM
                                    options = py.addAttr(otherNodes[ii]+"."+attributes[iii],en=1,q=1);
                                    py.addAttr(animatorNodes[i]+"Shape",ln=name,at="enum",en=options,dv=0);
                                else:
                                    #IF FLOAT
                                    py.addAttr(animatorNodes[i]+"Shape",ln=name,at="double");
                                py.setAttr(animatorNodes[i]+"Shape."+name, k=1, e=1);
                        iii+=1;
                    ii+=1;
                py.setAttr(animatorNodes[i]+"Shape.hiddenInOutliner", 1);
                i+=1;
###############################################################################
#"""# CREATE AND FINALIZE SEGMENT ASSETS                                      #
############################################################################### 
        i=0;
        while(i < 100 and py.objExists(switchSpaceCalculator) == 1):
            try:
                py.connectAttr(optionsBox+".SWITCH_NECK_SPACE",switchSpaceCalculator+".input1D["+str(i)+"]");
                py.connectAttr(optionsBox+".SWITCH_HEAD_SPACE",switchSpaceCalculator+".input1D["+str(i+1)+"]");
                break
            except:
                pass;
            i+=1;
        py.delete(bindJointChain[-1]);
        py.displayPref(displayAffected=0);
        if(segmentName == "neck" or segmentName == "head"):
            print '"The neck and head segment was successfully created!" - HiGGiE';
            py.headsUpMessage('"The neck and head segment was successfully created!" - HiGGiE', t=3);
        else:    
            print '"The '+str(section[0][:-1])+' segment was successfully created!" - HiGGiE';
            py.headsUpMessage('"The '+str(section[0][:-1])+' segment was successfully created!" - HiGGiE', t=3);
    py.select(d=1);






















###############################################################################
#.............................................................................#
#.............................................................................#
#"""# CREATES IK FOOT FUNCTIONS: ROLL, BANK, PIVOT, ETC                       #
#.............................................................................#
#.............................................................................#
###############################################################################
def footFunctions(FFV1,FFV2,FFV3,FFV4,FFV5,FFV6,FFV7,FFV8,FFV9,FFV10,FFV11,FFV12,FFV13,FFV14,FFV15,FFV16,FFV17,FFV18,FFV19,FFV20):
    variableName = FFV1;
    side = FFV2;
    section = FFV3;
    version = FFV4;
    jointChain = FFV5;
    bindJointChain = FFV6;
    ankleIndex = FFV7;
    ballIndex = FFV8;
    controllerSize = FFV9;
    primaryIK = FFV10;
    
    controllerIK = FFV11;
    toeControllerIK = FFV12;
    heelDist = FFV13;
    handleGroup = FFV14;
    legRotationOrder = FFV15;
    toePivotV1 = FFV16;
    toeHandleGroup = FFV17;
    handlePivotV1 = FFV18;
    handlePivotV2 = FFV19;
    handlePivotV3 = FFV20;    
    
    footAttributes = ["ROLL","BANK","HEEL","TOE","TOEFLOP","HEELROLL","TOEROLL"];  
    axis = ["x","y","z"];
    footElements = [];
    #CREATE AND ORGANIZE PIVOT POINT GROUPS AND LOCATORS
    name = "c_"+side+"_footMaster"+variableName+"_v"+str(version)+"_GRP";
    masterFootGroup = py.group(n=name, em=1);
    snap = py.pointConstraint(bindJointChain[ankleIndex], masterFootGroup, mo=0, w=1);
    py.delete(snap);
    name = "c_"+side+"_"+section[-1]+"PivotMaster"+variableName+"_v"+str(version)+"_LOC";
    pivotLocatorMaster = py.spaceLocator(p=(0,0,0), n=name)[0];
    name = "c_"+side+"_"+section[-1]+"PivotMaster"+variableName+"_v"+str(version)+"_GRP";
    pivotLocatorMasterGroup = py.group(n=name,r=1);
    #BANK RIGHT
    name = "c_"+side+"_bankRightMaster"+variableName+"_v"+str(version)+"_LOC";
    bankRightLocatorMaster = py.spaceLocator(p=(0,0,0), n=name)[0];
    name = "c_"+side+"_bankRight"+variableName+"_v"+str(version)+"_LOC";
    bankRightLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
    py.parent(bankRightLocator,bankRightLocatorMaster);
    py.parent(bankRightLocatorMaster,pivotLocatorMaster);
    if(side == "L"):
        py.setAttr(bankRightLocatorMaster+".tx", controllerSize/-4);#!WAS "2"
    else:
        py.setAttr(bankRightLocatorMaster+".tx", controllerSize/-2.25);#!WAS "2"
    #BANK LEFT
    name = "c_"+side+"_bankLeftMaster"+variableName+"_v"+str(version)+"_LOC";
    bankLeftLocatorMaster = py.spaceLocator(p=(0,0,0), n=name)[0];
    name = "c_"+side+"_bankLeft"+variableName+"_v"+str(version)+"_LOC";
    bankLeftLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
    py.parent(bankLeftLocator,bankLeftLocatorMaster);
    py.parent(bankLeftLocatorMaster,bankRightLocator);
    if(side == "L"):
        py.setAttr(bankLeftLocatorMaster+".tx", controllerSize/1.5);#!WAS "1"
    else:
        py.setAttr(bankLeftLocatorMaster+".tx", controllerSize/1.45);#!WAS "1"
    #HEEL PIVOT
    name = "c_"+side+"_heelPivotMaster"+variableName+"_v"+str(version)+"_LOC";
    heelLocatorMaster = py.spaceLocator(p=(0,0,0), n=name)[0];
    name = "c_"+side+"_heelPivot"+variableName+"_v"+str(version)+"_LOC";
    heelLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
    py.parent(heelLocator,heelLocatorMaster);
    py.parent(heelLocatorMaster,bankLeftLocator);
    py.setAttr(heelLocatorMaster+".tz", heelDist);
    snap = py.pointConstraint(bindJointChain[ballIndex],pivotLocatorMasterGroup,mo=0,w=1);
    py.delete(snap);
    #TOE PIVOT
    name = "c_"+side+"_toePivotMaster"+variableName+"_v"+str(version)+"_LOC";
    toeLocatorMaster = py.spaceLocator(p=(0,0,0), n=name)[0];
    name = "c_"+side+"_toePivot"+variableName+"_v"+str(version)+"_LOC";
    toeLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
    py.parent(toeLocator,toeLocatorMaster);
    py.parent(toeLocatorMaster,heelLocator);
    snap = py.pointConstraint(bindJointChain[-1],toeLocatorMaster,mo=0,w=1);
    py.delete(snap);
    #BALL PIVOT
    name = "c_"+side+"_ballPivotMaster"+variableName+"_v"+str(version)+"_LOC";
    ballLocatorMaster = py.spaceLocator(p=(0,0,0), n=name)[0];
    name = "c_"+side+"_ballPivot"+variableName+"_v"+str(version)+"_LOC";
    ballLocator = py.spaceLocator(p=(0,0,0), n=name)[0];
    py.parent(ballLocator,ballLocatorMaster);
    py.parent(ballLocatorMaster,toeLocator);
    snap = py.pointConstraint(bindJointChain[ballIndex],ballLocatorMaster,mo=0,w=1);
    py.delete(snap);
    #CREATE LOCATOR FOR INITIAL LOCATION FOR IK LEG CONTROLLER
    name = "c_"+side+"_"+section[-1]+"InitialPositionIK"+variableName+"_v"+str(version)+"_LOC";
    intialLocationIK = py.spaceLocator(p=(0,0,0), n=name)[0];
    snap = py.pointConstraint(controllerIK, intialLocationIK, mo=0, w=1);
    py.delete(snap);
    py.parent(intialLocationIK,masterFootGroup);
    py.makeIdentity(intialLocationIK, a=1, t=1, n=0);#FREEZE
    py.addAttr(intialLocationIK,ln="aimAxis",at="enum",en="0,0,1");
    py.addAttr(intialLocationIK,ln="upAxis",at="enum",en="0,1,0");
    py.setAttr(intialLocationIK+".v",0);
    #SET HIERARCHY FOR GROUPS AND LOCATORS
    name = "c_"+side+"_"+section[-1]+"Mesh"+variableName+"_v"+str(version)+"_DECOY";
    shapeIK = py.duplicate(controllerIK,n=name,rc=1)[0];
    name = "c_"+side+"_"+section[-1]+variableName+"_v"+str(version)+"_JNT";
    jointIK = py.joint(n=name);
    children = py.listRelatives(shapeIK, c=1, type="transform", s=0);
    if(isinstance(children,list) == 1):
        py.delete(children);
    py.setAttr(shapeIK+".hiddenInOutliner",1);
    py.parent(jointIK,masterFootGroup);
    py.parent(shapeIK,masterFootGroup);
    pivotPoints = [masterFootGroup,handleGroup,handlePivotV1,handlePivotV2,handlePivotV3,
                   pivotLocatorMasterGroup,pivotLocatorMaster,
                   bankRightLocatorMaster,bankRightLocator,
                   bankLeftLocatorMaster,bankLeftLocator,
                   heelLocatorMaster,heelLocator,
                   toeLocatorMaster,toeLocator,
                   ballLocatorMaster,ballLocator,shapeIK];         
    if(variableName == "Hybrid"):          
        snap1 = py.pointConstraint(bindJointChain[ankleIndex],shapeIK, mo=0, w=1);
    else:
        snap1 = py.pointConstraint(bindJointChain[ballIndex],shapeIK, mo=0, w=1);
    snap2 = py.pointConstraint(bindJointChain[ballIndex],jointIK, mo=0, w=1);
    py.delete(snap1,snap2);
    py.parent(handleGroup,masterFootGroup);
    py.parent(pivotLocatorMasterGroup,controllerIK);
    #ASSIGN AND SETUP SHAPES AND BLENDSHAPES
    try:
        py.makeIdentity(shapeIK, a=1, t=1, n=0);#FREEZE
    except:
        pass;
    decoyShape = py.listRelatives(shapeIK, s=1);
    decoyShape = py.rename(decoyShape, shapeIK+"Shape");
    controllerCurve = py.curve(d=1,p=[(-0.5,0,0),(-0.5,0,2),(-2,0,2),(0,0,4),(2,0,2),(0.5,0,2),(0.5,0,0),(0,0,0),(-0.5,0,0)]);
    py.setAttr(controllerCurve+".s", controllerSize*0.25,controllerSize*0.15,controllerSize*0.15);
    py.makeIdentity(controllerCurve, a=1, s=1, n=0);#FREEZE
    controllerShape = py.listRelatives(controllerCurve, s=1)[0];
    py.setAttr(controllerShape+".overrideEnabled", 1);
    py.setAttr(controllerShape+".overrideDisplayType",1);
    py.connectAttr(controllerCurve+".overrideDisplayType",controllerShape+".overrideDisplayType");
    py.connectAttr(primaryIK+".secondCOLOR",controllerShape+".overrideColor");
    py.parent(controllerShape,handleGroup,s=1,r=1);
    controllerShape = py.listRelatives(handleGroup, s=1)[0];
    controllerShape = py.rename(controllerShape,handleGroup+"Shape");
    try:
        py.makeIdentity(handleGroup, a=1, t=1, n=0);#FREEZE
    except:
        pass;
    py.delete(controllerCurve);
    name = "c_"+side+"_"+section[-1]+variableName+"_v"+str(version)+"_BRIDGE";
    bridge = py.blendShape(shapeIK,controllerIK+"Shape",n=name)[0];
    py.setAttr(bridge+"."+shapeIK,1);
    py.setAttr(shapeIK+".v",l=0);py.setAttr(jointIK+".v",l=0);
    py.setAttr(shapeIK+".v",0);py.setAttr(jointIK+".v",0);
    py.skinCluster(jointIK,shapeIK,mi=1,nw=1,bm=0,sm=0,dr=1.0);
    #CREATE SAFE MODE FOR WHEN CONSTRAINTS NEED TO BE CONNECTED TO CONTROLLER
    counterGroup = handlePivotV3;
    complexGroup = handlePivotV2;
    py.addAttr(counterGroup, ln="SAFE", at="enum", en="OFF:ON:", dv=0);
    #TRANSLATION CONDITION
    name = "c_"+side+"_"+section[-1]+"SafeModeTranslations"+variableName+"_v"+str(version)+"_CDN";
    safePlugTranslations = py.createNode("condition", n=name);
    py.setAttr(safePlugTranslations+".operation", 0);
    py.connectAttr(counterGroup+".SAFE",safePlugTranslations+".firstTerm");
    py.connectAttr(controllerIK+".t",safePlugTranslations+".colorIfTrue");
    py.setAttr(safePlugTranslations+".secondTerm", 0);
    py.setAttr(safePlugTranslations+".colorIfFalse", 0,0,0);
    py.setAttr(safePlugTranslations+".ihi",0);
    #ROTATION CONDITION
    name = "c_"+side+"_"+section[-1]+"SafeModeRotations"+variableName+"_v"+str(version)+"_CDN";
    safePlugRotations = py.createNode("condition", n=name);
    py.setAttr(safePlugRotations+".operation", 0);
    py.connectAttr(counterGroup+".SAFE",safePlugRotations+".firstTerm");
    py.connectAttr(controllerIK+".r",safePlugRotations+".colorIfTrue");
    py.setAttr(safePlugRotations+".secondTerm", 0);
    py.setAttr(safePlugRotations+".colorIfFalse", 0,0,0);
    py.setAttr(safePlugRotations+".ihi",0);
    #CREATE COUNTER NODE AND ADDITION NODES
    name = "c_"+side+"_"+section[-1]+"CounterTranslate"+variableName+"_v"+str(version)+"_MDN";
    counterTranslate = py.createNode("multiplyDivide", n=name);
    py.connectAttr(safePlugTranslations+".outColor",counterTranslate+".input1");
    py.setAttr(counterTranslate+".input2",-1,-1,-1);
    py.connectAttr(counterTranslate+".output",counterGroup+".t");
    py.setAttr(counterTranslate+".ihi",0);
    name = "c_"+side+"_"+section[-1]+"CounterRotate"+variableName+"_v"+str(version)+"_MDN";
    counterRotate = py.createNode("multiplyDivide", n=name);
    py.connectAttr(safePlugRotations+".outColor",counterRotate+".input1");
    py.setAttr(counterRotate+".input2",-1,-1,-1);
    py.connectAttr(counterRotate+".output",complexGroup+".r");
    #MIRROR ROTATION ORDER OF IK CONTROLLER TO THE COUNTER GROUP
    pivotPoints.remove(complexGroup);
    rotationOrderList = mel.eval('attributeQuery -le -n "'+controllerIK+'" "rotateOrder"');
    rotationOrderValue = rotationOrderList[0].split(":").index(legRotationOrder);
    rotationOrderCount = len(rotationOrderList[0].split(":"));
    i=0;
    while(i < rotationOrderCount):
        try:
            py.setAttr(controllerIK+".ROTATE_ORDER",i);
            currentRotationOrder = py.getAttr(controllerIK+".ROTATE_ORDER",asString=1);
        except:
            py.setAttr(controllerIK+".rotateOrder",i);
            currentRotationOrder = py.getAttr(controllerIK+".rotateOrder",asString=1);
        mirroredRotationOrder = currentRotationOrder[2]+currentRotationOrder[1]+currentRotationOrder[0];
        py.xform(complexGroup,p=1,roo=mirroredRotationOrder);
        try:
            py.setDrivenKeyframe(complexGroup+".rotateOrder", cd=controllerIK+".ROTATE_ORDER");
        except:
            py.setDrivenKeyframe(complexGroup+".rotateOrder", cd=controllerIK+".rotateOrder");
        i+=1;
    py.xform(controllerIK,p=1,roo="xyz");#!
    py.setAttr(counterRotate+".ihi",0);
    #ADD SLIDER FUNCTIONS
    name = "c_"+side+"_"+section[3]+variableName+"_v"+str(version)+"_IK";
    ballIK = py.ikHandle(n=name, sj=jointChain[ankleIndex], ee=jointChain[ballIndex], sol="ikSCsolver", shf=0, s=0)[0];
    name = "c_"+side+"_"+section[4]+variableName+"_v"+str(version)+"_IK";
    toeIK = py.ikHandle(n=name, sj=jointChain[ballIndex], ee=jointChain[-1], sol="ikSCsolver", shf=0, s=0)[0];
    py.setAttr(ballIK+".v",0);py.setAttr(toeIK+".v",0);
    footElements.extend((toeLocator,toeLocatorMaster));
    footElements.extend((ballLocator,ballLocatorMaster));
    footElements.extend((heelLocator,heelLocatorMaster));
    rollMin = -45;rollMax = 90;ballRollValue = 45;toeRollValue = 70;
    py.addAttr(controllerIK, ln="ROLL", at="double", min=rollMin, max=rollMax, dv=0);
    py.setAttr(controllerIK+".ROLL", e=1, k=1);
    py.addAttr(controllerIK, ln="BANK", at="double", dv=0);
    py.setAttr(controllerIK+".BANK", e=1, k=1);
    py.addAttr(controllerIK, ln="HEEL", at="double", dv=0);
    py.setAttr(controllerIK+".HEEL", e=1, k=1);
    py.addAttr(controllerIK, ln="TOE", at="double", dv=0);
    py.setAttr(controllerIK+".TOE", e=1, k=1);
    py.addAttr(controllerIK, ln="TOEFLOP", at="double", dv=0);
    py.setAttr(controllerIK+".TOEFLOP", e=1, k=1);
    py.addAttr(controllerIK, ln="HEELROLL", at="double",min=rollMin, max=0, dv=0);
    py.setAttr(controllerIK+".HEELROLL", e=1, k=1);
    py.addAttr(controllerIK, ln="TOEROLL", at="double",min=0, max=rollMax, dv=0);
    py.setAttr(controllerIK+".TOEROLL", e=1, k=1);
    py.addAttr(controllerIK, ln="BALL_PIVOT_ANGLE",at="double",min=1,dv=ballRollValue);
    py.setAttr(controllerIK+".BALL_PIVOT_ANGLE", e=1, k=0, cb=1);
    py.addAttr(controllerIK, ln="TOE_PIVOT_ANGLE", at="double",min=1,dv=toeRollValue);
    py.setAttr(controllerIK+".TOE_PIVOT_ANGLE", e=1, k=0, cb=1);
    rotations = list(py.getAttr(ballLocatorMaster+".r")[0]);
    py.setAttr(toeLocatorMaster+".r",rotations[0],rotations[1],rotations[2])
    name = "c_"+side+"_toe"+variableName+"_v"+str(version)+"_CMP";
    toeClamp = py.createNode("clamp", n=name);
    py.setAttr(toeClamp+".ihi",0);
    name = "c_"+side+"_ball"+variableName+"_v"+str(version)+"_CMP";
    ballClamp = py.createNode("clamp", n=name);
    py.setAttr(ballClamp+".ihi",0);
    name = "c_"+side+"_ball"+variableName+"_v"+str(version)+"_SR";
    ballSetRange = py.createNode("setRange", n=name);
    py.setAttr(ballSetRange+".ihi",0);
    name = "c_"+side+"_heel"+variableName+"_v"+str(version)+"_CMP";
    heelClamp = py.createNode("clamp", n=name);
    py.setAttr(heelClamp+".ihi",0);
    name = "c_"+side+"_heel"+variableName+"_v"+str(version)+"_CMP";
    py.setAttr(heelClamp+".minR", -1080);
    py.setAttr(heelClamp+".maxR", 0);
    name = "c_"+side+"_bend"+variableName+"_v"+str(version)+"_CMP";
    bendClamp = py.createNode("clamp", n=name);
    py.setAttr(bendClamp+".ihi",0);
    name = "c_"+side+"_bend"+variableName+"_v"+str(version)+"_SR";
    bendSetRange = py.createNode("setRange", n=name);
    py.setAttr(bendSetRange+".ihi",0);
    name = "c_"+side+"_"+section[1]+"roll"+variableName+"_v"+str(version)+"_MDN";
    rollClamp = py.createNode("multiplyDivide", n=name);
    py.setAttr(rollClamp+".ihi",0);
    py.connectAttr(controllerIK+".BALL_PIVOT_ANGLE", bendClamp+".minR");
    py.connectAttr(controllerIK+".TOE_PIVOT_ANGLE", bendClamp+".maxR");
    py.connectAttr(bendClamp+".minR", bendSetRange+".oldMinX");
    py.connectAttr(bendClamp+".maxR", bendSetRange+".oldMaxX");
    py.connectAttr(bendClamp+".inputR", bendSetRange+".valueX");
    py.connectAttr(ballClamp+".minR", ballSetRange+".oldMinX");
    py.connectAttr(ballClamp+".maxR", ballSetRange+".oldMaxX");
    py.connectAttr(ballClamp+".inputR", ballSetRange+".valueX");
    py.setAttr(bendSetRange+".maxX", 1);
    py.setAttr(ballSetRange+".maxX", 1);
    py.connectAttr(bendSetRange+".outValueX", rollClamp+".input1X");
    py.connectAttr(bendClamp+".inputR", rollClamp+".input2X");
    py.connectAttr(controllerIK+".BALL_PIVOT_ANGLE", ballClamp+".maxR");#!
    name = "c_"+side+"_toeRoll"+variableName+"_v"+str(version)+"_ADL";
    toeRoll = py.createNode("addDoubleLinear", n=name);
    py.connectAttr(rollClamp+".outputX", toeRoll+".input1");
    py.connectAttr(controllerIK+".TOEROLL", toeRoll+".input2");
    py.setAttr(toeRoll+".ihi",0);
    py.connectAttr(toeRoll+".output", toeLocator+".rx");
    py.connectAttr(heelClamp+".outputR", heelLocator+".rx");
    py.connectAttr(controllerIK+".ROLL", heelClamp+".inputR");
    py.connectAttr(controllerIK+".ROLL", ballClamp+".inputR");
    py.connectAttr(controllerIK+".ROLL", toeClamp+".inputR");
    py.connectAttr(controllerIK+".ROLL", bendClamp+".inputR");
    py.connectAttr(controllerIK+".HEELROLL", heelLocatorMaster+".rx");
    name = "c_"+side+"_foot"+variableName+"_v"+str(version)+"_PMA";
    footClamp = py.createNode("plusMinusAverage", n=name);
    py.setAttr(footClamp+".ihi",0);
    name = "c_"+side+"_footMult1"+variableName+"_v"+str(version)+"_MDN";
    footMultiplier1 = py.createNode("multiplyDivide", n=name);
    py.setAttr(footMultiplier1+".ihi",0);
    name = "c_"+side+"_footMult2"+variableName+"_v"+str(version)+"_MDN";
    footMultiplier2 = py.createNode("multiplyDivide", n=name);
    py.setAttr(footMultiplier2+".ihi",0);
    py.setAttr(footClamp+".operation", 2);
    py.setAttr(footClamp+".input1D[0]", 1);
    py.setAttr(footClamp+".input1D[1]", 1);
    py.connectAttr(bendSetRange+".outValueX", footClamp+".input1D[1]");
    py.connectAttr(ballSetRange+".outValueX", footMultiplier1+".input1X");
    py.connectAttr(footClamp+".output1D", footMultiplier1+".input2X");
    py.connectAttr(footMultiplier1+".outputX", footMultiplier2+".input1X");
    py.connectAttr(controllerIK+".ROLL", footMultiplier2+".input2X");
    py.connectAttr(footMultiplier2+".outputX", ballLocator+".rx");
    name = "c_"+side+"_"+section[3]+"Flip"+variableName+"_v"+str(version)+"_MDN";
    ballFlip = py.createNode("multiplyDivide", n=name);
    py.setAttr(ballFlip+".ihi",0);
    py.connectAttr(footMultiplier2+".outputX", ballFlip+".input1X");
    py.setAttr(ballFlip+".input2", -1, -1, -1);
    py.xform(footElements,ballIK,toeIK,p=1,roo=legRotationOrder);
    name = "c_"+side+"_"+section[-1]+"Bank"+variableName+"_v"+str(version)+"_MDN";
    bankReverse = py.createNode("multiplyDivide", n=name);
    py.connectAttr(controllerIK+".BANK", bankReverse+".input1X");
    py.setAttr(bankReverse+".input2",-1,-1,-1);
    name = "c_"+side+"_"+section[-1]+"Bank"+variableName+"_v"+str(version)+"_CMP";
    clamp = py.createNode("clamp", n=name);
    py.connectAttr(bankReverse+".outputX", clamp+".inputR");
    py.connectAttr(bankReverse+".outputX", clamp+".inputG");
    py.setAttr(clamp+".minR", 0);py.setAttr(clamp+".maxR", 1000);
    py.setAttr(clamp+".minG", -1000);py.setAttr(clamp+".maxG",0);
    py.connectAttr(clamp+".outputR", bankRightLocator+".rz");
    py.connectAttr(clamp+".outputG", bankLeftLocator+".rz");
    py.setAttr(clamp+".ihi",0);py.setAttr(bankReverse+".ihi",0);
    py.connectAttr(controllerIK+".TOEFLOP",toePivotV1+".rx");
    #DUPLICATE PIVOT LOCATORS AND CONNECTIONS FOR CYCLE PREVENTION
    expendableList = [];
    connectionHierarchy = [];
    duplicatedPivotHierarchy = py.duplicate(pivotLocatorMaster,ic=1,rc=1);
    py.parent(duplicatedPivotHierarchy[0],masterFootGroup);
    i=0;
    while(i < len(duplicatedPivotHierarchy)):
        if("LOC" in duplicatedPivotHierarchy[i]):
            newName = duplicatedPivotHierarchy[i].replace("_v","Rotation"+variableName+"_v").replace("LOC1","LOC");
            item = py.rename(duplicatedPivotHierarchy[i],newName);
            py.setAttr(item+".v",0);
            connectionHierarchy.append(item);
        else:
            expendableList.append(duplicatedPivotHierarchy[i]);
        i+=1;
    py.delete(expendableList);
    py.setAttr(connectionHierarchy[0]+".inheritsTransform",0);
    snap = py.pointConstraint(pivotLocatorMaster,connectionHierarchy[0],mo=0,w=1);
    py.delete(snap);
    name = jointIK.replace(jointIK.split("_")[-1], "CON");
    constraint = py.parentConstraint(connectionHierarchy[-1], jointIK, n=name, mo=1,w=1);
    #CONNECT ATTRIBUTES TO CORRESPONDING NODE
    name = "c_"+side+"_rotationCollection"+variableName+"_v"+str(version)+"_ADL";
    rotationHeelToeNode = py.createNode("addDoubleLinear", n=name);
    py.connectAttr(controllerIK+".HEEL", rotationHeelToeNode+".input1");
    py.connectAttr(controllerIK+".TOE", rotationHeelToeNode+".input2");
    py.setAttr(rotationHeelToeNode+".ihi",0);
    py.connectAttr(controllerIK+".HEEL", connectionHierarchy[6]+".ry");
    py.connectAttr(controllerIK+".TOE", connectionHierarchy[8]+".ry");
    py.connectAttr(rotationHeelToeNode+".output",controllerIK+".ray");
    py.connectAttr(safePlugTranslations+".outColor", handleGroup+".t");
    py.connectAttr(safePlugRotations+".outColor", handleGroup+".r");
    #CREATE LOCATORS TO TRACK POSITIONS
    ballTranslationLocator = py.spaceLocator(p=(0,0,0))[0];
    snap = py.pointConstraint(connectionHierarchy[-1],ballTranslationLocator,mo=0,w=1);
    py.delete(snap);
    py.parent(ballTranslationLocator,handleGroup);
    py.makeIdentity(ballTranslationLocator,a=1,t=1,n=0);#FREEZE
    snap = py.pointConstraint(connectionHierarchy[-1],ballTranslationLocator,mo=1,w=1);
    #SET DRIVEN KEY FOR HEEL PIVOT (Y AXIS)
    i=-360;
    while(i <= 360):
        py.setAttr(controllerIK+".HEEL",i);
        translations = list(py.getAttr(ballTranslationLocator+".t")[0]);
        py.setAttr(complexGroup+".t",translations[0],translations[1],translations[2]);
        py.setDrivenKeyframe(complexGroup+".t", cd=controllerIK+".HEEL");
        i+=1;
    py.setAttr(controllerIK+".HEEL",0);
    py.disconnectAttr(controllerIK+".HEEL", connectionHierarchy[6]+".ry");
    #SET DRIVEN KEY FOR TOE PIVOT (Y AXIS)
    i=-360;
    while(i <= 360):
        py.setAttr(controllerIK+".TOE",i);
        translations = list(py.getAttr(ballTranslationLocator+".t")[0]);
        py.setAttr(complexGroup+".rpt",translations[0],translations[1],translations[2]);
        py.setDrivenKeyframe(complexGroup+".rpt", cd=controllerIK+".TOE");
        i+=1;
    py.setAttr(controllerIK+".TOE",0);
    py.disconnectAttr(controllerIK+".TOE", connectionHierarchy[8]+".ry");
    py.delete(ballTranslationLocator,snap);
    #MAKE DISTANCE BASED PIVOT VISIBILITY
    distanceNodeShape = py.distanceDimension(sp=(0, 100, 0), ep=(0, 10, 0));
    distanceLocators = py.listConnections(distanceNodeShape);
    distanceNode = py.listRelatives(distanceNodeShape, p=1);
    distanceNode = py.rename(distanceNode,"c_"+side+"_footDistance"+variableName+"_v"+str(version)+"_DDN");
    start = py.rename(distanceLocators[0],"c_"+side+"_footStartDistance"+variableName+"_v"+str(version)+"_LOC");
    end = py.rename(distanceLocators[1],"c_"+side+"_footEndDistance"+variableName+"_v"+str(version)+"_LOC");
    py.setAttr(start+".v",0);py.setAttr(end+".v",0);py.setAttr(distanceNode+".v",0);
    name = start.replace(start.split("_")[-1], "PNT");
    constraint = py.pointConstraint(handleGroup,start,n=name,mo=0,w=1);
    name = end.replace(end.split("_")[-1], "PNT");
    constraint = py.pointConstraint(ballLocator,end,n=name,mo=0,w=1);
    py.parent(distanceNode,start,end,masterFootGroup); 
    name = "c_"+side+"_footPivotVisibilityState"+variableName+"_v"+str(version)+"_CDN";
    VS = py.createNode("condition", n=name);
    py.connectAttr(distanceNode+"Shape.distance",VS+".firstTerm");
    py.setAttr(VS+".operation", 2);
    py.setAttr(VS+".secondTerm", 0.1);
    py.setAttr(VS+".colorIfTrue", 1,0,1);
    py.setAttr(VS+".colorIfFalse",0,1,0);
    py.connectAttr(VS+".outColorR", controllerShape+".v"); 
    py.setAttr(distanceNode+".hiddenInOutliner",1);
    py.setAttr(start+".hiddenInOutliner",1);
    py.setAttr(end+".hiddenInOutliner",1);
    py.setAttr(VS+".ihi",0);
    #MAKE LOCATORS INVISIBLE AND ORGANIZE
    py.parent(ballIK,ballLocator);py.parent(toeIK,toeControllerIK);
    py.parent(toeHandleGroup,ballLocatorMaster);
    py.parent(primaryIK,ballLocator);
    i=0;
    while(i < len(pivotPoints)):
        if("GRP" not in pivotPoints[i]): 
            py.setAttr(pivotPoints[i]+"Shape.v",0);
        try:
            py.connectAttr(controllerIK+".ROTATE_ORDER",pivotPoints[i]+".rotateOrder");
        except:
            py.connectAttr(controllerIK+".rotateOrder",pivotPoints[i]+".rotateOrder");
        i+=1;
    return [masterFootGroup,footAttributes];