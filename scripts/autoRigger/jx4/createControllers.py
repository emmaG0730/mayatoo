###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import sys, os
import maya.cmds as py
import maya.mel as mel 
###############################################################################
#"""# IMPORT ADDITIONAL MODULES FOR THE MATRIX                                #
###############################################################################
path = "R:/Jx4/tools/dcc/maya/scripts/autoRigger/jx4/";
module = path+'createRig.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import createRig
global scaleVar
#GET MESH AND ROOT JOINT BASED ON SELECTION TO BEGIN PAIRING
def scanMesh(varScale):
    print varScale
    selection = py.ls(sl=1);
    sceneMesh = py.ls(type="mesh");
    if(len(sceneMesh) > 0):
        selection.append(sceneMesh[0]);
    destructables = []; 
    usedNames = [];
    detail = 2;#THIS VALUE CHANGES THE SUBDIVISIONS OF THE GENERATED CONTROLLERS
    targetMesh = "";
    targetJoint = "";
    slicerGroup = "";
    
    headSegments = ["head","neck"];
    headNames = ["head","neck3"];
    neckNames = ["neck","neckBase","neck1"];
    
    bodySegments = ["pelvis","spine"];
    spineNames = ["spine","body","torso"];
    pelvisNames = ["pelvis","root"];
    
    armSegments = ["clavicle","shoulder","elbow","wrist"];
    clavicleNames = ["clavicle","clavical","clav"];
    shoulderNames = ["shoulder","upperarm"];
    elbowNames = ["elbow","lowerarm"];
    wristNames = ["wrist","hand","frontFetlock","frontfetlock"];
    
    legSegments = ["hip","knee","ankle","ball","stifle","hock","hindFetlock","hindCoronet"];
    hipNames = ["hip","thigh","upperleg"];
    kneeNames = ["knee","lowerleg","stifle"];
    ankleNames = ["ankle","foot","feet","hock"];
    ballNames = ["ball","footroll","feetroll","hindFetlock","hindfetlock"];
    toeNames = ["toe","coronet","Coronet"]
    
    
    fingerSegments = ["thumb","index","middle","ring","pinky","pinkie"];
    thumbNames = ["thumb","bigfinger"];
    indexNames = ["index","pointer"];
    middleNames = ["middle","mid"];
    ringNames = ["ring"];
    babyNames = ["pinky","pinkie","baby"];
    

    py.headsUpMessage('"Starting Step 2: Create custom controllers (if possible)." - HiGGiE', t=2);
    print '"Starting Step 2: Create custom controllers (if possible)." - HiGGiE';
    
    for i in range(0,len(selection)):
        shape = py.listRelatives(selection[i],f=1,s=1);
        shape = selection[i] if(isinstance(shape,list) == 0) else shape;
        type = py.objectType(shape);
        if(type == "mesh"):
            targetMesh = selection[i];
        if(type == "joint" or type == "transform"):
            rootJoint = "";
            currentJoint = py.listRelatives(selection[i],f=1,ad=1,p=1);
            if(isinstance(currentJoint,list) == 1):
                currentJoint = currentJoint[0];
                while(rootJoint == ""):
                    potentialRoots = py.listRelatives(currentJoint,f=1,ad=1,p=1);
                    if(isinstance(potentialRoots,list) == 0):
                        currentType = py.objectType(currentJoint);
                        if(currentType == "joint"):
                            rootJoint = currentJoint;
                        else:
                            children = py.listRelatives(currentJoint,type="joint",f=1,c=1);
                            if(isinstance(children,list) == 1):
                                rootJoint = children[0];
                                destructables.append(currentJoint);
                            else:
                                break;
                    else:
                        currentType = py.objectType(potentialRoots[0]);
                        if(currentType == "joint"):
                            rootJoint = potentialRoots[0];
                        else:
                            currentJoint = potentialRoots[0];
            else:
                currentType = py.objectType(selection[i]);
                if(currentType == "joint"):
                    rootJoint = selection[i];
                else:
                    children = py.listRelatives(selection[i],type="joint",f=1,c=1);
                    if(isinstance(children,list) == 1):
                        rootJoint = children[0];
                        destructables.append(selection[i]);
                    else:
                        break; 
            targetJoint = rootJoint;
        if(targetMesh != "" and targetJoint != ""):
            break;
    posture = "biped"
    for i in py.listRelatives(targetJoint,f=1,ad=1,c=1):
        print i
        if "hock" in i:
            posture = "quadruped"
    #BEGIN ADDING SLICER PLANES TO ALL JOINT POSITIONS UNDER ROOT      
    if(targetMesh != "" and targetJoint != ""):
        allChildren = py.listRelatives(targetJoint,f=1,ad=1,c=1);
        allJoints = allChildren[:];
        allJoints.append(targetJoint);
        highestSpineID = 0;
        spineControllers = [];
        if(isinstance(allJoints,list) == 1):
            #GET SKELETON HEIGHT
            distanceNodeShape = py.distanceDimension(sp=(0, 0, 0), ep=(0, 1, 0));
            distanceLocators = py.listConnections(distanceNodeShape);
            distanceNode = py.listRelatives(distanceNodeShape, p=1);
            highestHeight = 0;
            for i in range(0,len(allJoints)):
                worldTransform = py.xform(allJoints[i],ws=1,t=1,q=1);
                if(highestHeight == 0 or worldTransform[1] > highestHeight):
                    snap = py.pointConstraint(allJoints[i],distanceLocators[-1],mo=0,w=1);
                    py.delete(snap);
                    highestHeight = worldTransform[1];
            height = py.getAttr(distanceNode[0]+".distance")/10;
            #ADD SLICER PLANES TO EACH VALID JOINT'S POSITION AND GROUP THEM
            slicerGroup = py.group(em=1);
            for i in range(0,len(allJoints)):
                skip = 0;
                children = py.listRelatives(allJoints[i],f=1,c=1);
                if(isinstance(children,list) == 1 and allJoints[i] != targetJoint):
                    if(len(children) > 1 and round(py.xform(allJoints[i],q=1,t=1,ws=1)[0],0) == 0):
                        #IF HIGHEST TORSO JOINT
                        if posture == "quadruped":
                            skip = 0
                        elif posture == "biped":
                            skip = 1;
                if(isinstance(children,list) == 1 and skip == 0):
                    slicerBox = py.polyCube(w=1,h=1,d=1,sx=detail,sy=detail,sz=detail,ax=(0,1,0),cuv=4,ch=1)[0];
                    py.move(-0.5,0,0, slicerBox+".sp", r=1);py.setAttr(slicerBox+".sptx", 0.5);
                    py.parent(slicerBox, slicerGroup);
                    #FIND SIDE
                    side = "L_" if(py.xform(allJoints[i],q=1,t=1,ws=1)[0]>0) else "R_"; 
                    side = "M_" if(round(py.xform(allJoints[i],q=1,t=1,ws=1)[0],0) == 0) else side; 
                    #GET DISTANCE BETWEEN TARGET JOINT AND TARGET'S CHILD
                    variable = -1 if(side == "R_") else 1;
                    snap = py.pointConstraint(allJoints[i],distanceLocators[0],mo=0,w=1);
                    py.delete(snap);
                    snap = py.pointConstraint(children[0],distanceLocators[-1],mo=0,w=1);
                    py.delete(snap);
                    length = py.getAttr(distanceNode[0]+".distance")*variable;
                    py.setAttr(slicerBox+".s",length,0,0);
                    #SNAP TO JOINT
                    snap = py.parentConstraint(allJoints[i],slicerBox,mo=0,w=1);
                    py.delete(snap);

                    #ADD WRAPPER TO CONTROLLERS
                    py.select(slicerBox,targetMesh,r=1);
                    py.CreateShrinkWrap();
                    shrinkWrapper = py.deformer(slicerBox,type="shrinkWrap")[0];
                    
                    #py.setAttr(shrinkWrapper+".projection",4); 
                    
                    
                    #######################################################
                    # adding a section to account for multiple shrinkWraps#
                    #######################################################
                    co=0
                    at = []
                    for numb in range(5):
                        at.append('shrinkWrap'+str(numb+1))
                    amt = []
                    wrappers = []
                    c=0
                    for items in at:
                        if py.objExists(items):
                            amt.append(py.listAttr(items))
                            
                            for var in amt[c]:
                                if var == 'projection':
                                    setThis = at[c] + '.' + var
                                    wrappers.append(setThis)
                                    c+=1
                        else:
                            pass
                    attr = wrappers     
                    for wrapper in attr:
                        py.setAttr(wrapper,4)
                    ######################################################
                    
                    
                    
                    #FIND SEGMENT NAME
                    segment = allJoints[i].split("|")[-1].lower();
                    print segment
                    if any(x in segment for x in headNames):
                        segment = "head";
                        py.rotate(45,0,-30,slicerBox,fo=1,os=1,r=1);
                    elif any(x in segment for x in neckNames):
                        segment = "neck";
                        '''
                        segmentList = segment.split("_")
                        for ii in range(0,len(segmentList)):
                            if any(x in segmentList[ii] for x in neckNames):
                                segment = segmentList[ii];
                                for iii in range(1,len(neckNames)):
                                    segment.replace(neckNames[iii],"neck");
                                    print segment
                                break;
                        
                        index = segmentList.index(segment);
                        print index
                        print ": index"
                        for ii in range(index,len(segmentList)):
                            if(segmentList[ii].isdigit() == 1):
                                segment = segment+str(segmentList[ii]);
                                break;
                        
                        if posture == "quadruped":
                            if py.objExists("a_M_neck_v1_CTRL"):
                                segment = "neckBase"
                        '''
                    elif any(x in segment for x in spineNames):
                        if ("spine_3" in segment and posture == "null"):
                            segment = "torso"
                        else:
                            segmentList = segment.split("_");
                            for ii in range(0,len(segmentList)):
                                print segmentList
                                if any(x in segmentList[ii] for x in spineNames):
                                    segment = segmentList[ii];
                                    for iii in range(1,len(spineNames)):
                                        segment.replace(spineNames[iii],"spine");
                                        print segment
                                    break;
                        
                            index = segmentList.index(segment);
                            for ii in range(index,len(segmentList)):
                                if(segmentList[ii].isdigit() == 1):
                                    segment = segment+str(segmentList[ii]);
                                    break;
                        
                    elif any(x in segment for x in pelvisNames):
                        segment = "pelvis";
                        
                    elif any(x in segment for x in clavicleNames):
                        segment = "clavicle";
                    elif any(x in segment for x in shoulderNames):
                        segment = "shoulder";
                    elif any(x in segment for x in elbowNames):
                        segment = "elbow";
                    elif any(x in segment for x in wristNames):
                        if posture == "quadruped":
                            segment = "frontFetlock"
                        else:
                            segment = "wrist";
                        
                    elif any(x in segment for x in hipNames):
                        segment = "hip";
                    elif any(x in segment for x in kneeNames):
                        if posture == "quadruped":
                            segment = "knee"
                            if py.objExists("a_L_knee_v1_CTRL") and py.objExists("a_R_knee_v1_CTRL"):
                                segment = "stifle";
                        elif posture == "biped":
                            segment = "knee"
                    elif any(x in segment for x in ankleNames):
                        if posture == "quadruped":
                            segment = "hock"
                        else:
                            segment = "ankle";
                    elif any(x in segment for x in ballNames):
                        if posture == "quadruped":
                            segment = "hindFetlock"
                        else:
                            segment = "ball"; 
                    elif any(x in segment for x in toeNames):
                        if posture == "quadruped":
                            segment = "frontCoronet"
                            if py.objExists("a_L_frontCoronet_v1_CTRL") and py.objExists("a_R_frontCoronet_v1_CTRL"):
                                segment = "hindCoronet"
                        elif posture == "biped":
                            segment = "toe"
                    elif any(x in segment for x in fingerSegments):
                        segmentList = segment.split("_");
                        for ii in range(0,len(segmentList)):
                            if any(x in segmentList[ii] for x in fingerSegments):
                                segment = segmentList[ii];
                                break;
                        index = segmentList.index(segment);
                        for ii in range(index,len(segmentList)):
                            if(segmentList[ii].isdigit() == 1):
                                #segment = segment+str(segmentList[ii]);
                                segment = segment+str(segmentList[ii][0]);#!CURRENTLY GETS DOUBLE DIGITS, BUT JUST NEEDS ONE
                                segment = segment.replace("pinkie","pinky");
                                break;
                    #DETERMINE SCALE SIZE BASED ON LENGTH AND SEGMENT
                    if varScale == '':
                        varScale = "Adult"
                    if varScale == "Adult":
                        print "Adult============================================="
                        scaleAmount = 10;  
                        if any(x in segment for x in headSegments):
                            scaleAmount = length*2 if(segment == "head") else length*1;
                        if any(x in segment for x in bodySegments):
                            scaleAmount = length*height/10 if(segment != "pelvis") else length*5;
                        if any(x in segment for x in armSegments):
                            scaleAmount = length/5 if(segment == "shoulder" or segment == "elbow") else length/2;  
                        if any(x in segment for x in legSegments):
                            scaleAmount = length/5 if(segment == "hip" or segment == "knee") else length;
                        if any(x in segment for x in fingerSegments):
                            scaleAmount = length/length;
                        
                    elif varScale == "Child":
                        print "Child=============================================="
                        scaleAmount = 10;  
                        if any(x in segment for x in headSegments):
                            scaleAmount = length*1 if(segment == "head") else length;
                        if any(x in segment for x in bodySegments):
                            scaleAmount = length*height/5 if(segment != "pelvis") else length*3;
                        if any(x in segment for x in armSegments):
                            scaleAmount = length/3 if(segment == "shoulder" or segment == "elbow") else length/2;  
                        if any(x in segment for x in legSegments):
                            scaleAmount = length/1.5 if(segment == "hip" or segment == "knee") else length/1.5;
                        if any(x in segment for x in fingerSegments):
                            scaleAmount = length/length;
                        
                    elif varScale == "Horse":
                        print "Horse============================================"
                        scaleAmount = 10;  
                        if any(x in segment for x in headSegments):
                            scaleAmount = length*2 if(segment == "head") else length*1;
                        if any(x in segment for x in bodySegments):
                            scaleAmount = length*height/10 if(segment != "pelvis") else length*2;
                        if any(x in segment for x in armSegments):
                            scaleAmount = length if(segment == "shoulder") else length/5;  
                        if any(x in segment for x in legSegments):
                            scaleAmount = length if(segment == "hip") or (segment == "hindCoronet") else length/5;
                        if any(x in segment for x in fingerSegments):
                            scaleAmount = length/length;
                    
                        
                    #DISTINGUISH END SLICER OR NOT
                    grandChildren = py.listRelatives(children[0],f=1,c=1);
                    if(isinstance(grandChildren,list) == 1):
                        version = 1;
                        newName = side+segment+"_v"+str(version)+"_seg_SP"
                        while(py.objExists(side+segment+"_v"+str(version)+"_SP")):
                            version += 1;
                        newName = side+segment+"_v"+str(version)+"_seg_SP";
                    else:
                        version = 1;
                        newName = side+segment+"_v"+str(version)+"_end_SP"
                        while(py.objExists(side+segment+"_v"+str(version)+"_end_SP")):
                            version += 1;
                        newName = side+segment+"_v"+str(version)+"_end_SP";
                    slicerBox = py.rename(slicerBox,newName);
                    py.setAttr(slicerBox+".s",length,scaleAmount,scaleAmount);
                    py.delete(slicerBox,ch=1);
                    #py.select(slicerBox,r=1);
                    #mel.eval('polyCleanupArgList 3 { "0","1","0","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","1","1" };');
                    #mel.eval('doPerformPolyReduceArgList 1 {"1","0","1","1","1","1","1","1","1","0.5","0.5","0.5","0.5","0.5","0.5","0","0.01","0","1","0","0.0","1","1","","1","1","25","0","0","1","0","0"};');
                    #GATHER THE HIGHEST SPINE JOINT INT TO CONVERT OTHERS TO "JNT"S
                    slicerBox = py.rename(slicerBox,"a_"+side+segment+"_v"+str(version)+"_CTRL");
                    print slicerBox
                    if("spine" in segment.lower()):
                        spineControllers.append(slicerBox);
                        idValue = segment.split("spine")[-1];
                        if(idValue.isdigit() == 1):
                            if(int(idValue) > highestSpineID):
                                highestSpineID = int(idValue);
            for i in range(0,len(spineControllers)):
                if("spine"+str(highestSpineID) not in spineControllers[i]):
                    slicerBox = py.rename(spineControllers[i],spineControllers[i].replace("CTRL","JNT"));
            py.delete(distanceNode,distanceLocators);
            py.headsUpMessage('"Controllers created!" - HiGGiE', t=2);
            print '"Controllers created!" - HiGGiE';
    else:
        py.headsUpMessage('"No valid mesh selected! Skipping control creation." - HiGGiE', t=2);
        print '"No valid mesh selected! Skipping control creation." - HiGGiE';
    if(targetJoint != ""):
        print targetJoint
        py.headsUpMessage('"Starting Step 3: Rigging the skeleton." - HiGGiE', t=2);
        print '"Starting Step 3: Rigging the skeleton." - HiGGiE';
        py.select(targetJoint, r=1);
        createRig.spine("generate");
        if(py.objExists(slicerGroup) == 1):
            py.delete(slicerGroup);
        if(targetMesh != ""):
            py.setAttr(targetMesh.split("Shape")[0]+".v",0);
        if(len(destructables) > 0):
            py.delete(destructables[:]);
        py.select("c_M_master_v1_CTRL",r=1);
