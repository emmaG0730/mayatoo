###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
############################################################################### 
import os
import json
import maya.cmds as py
import maya.mel as mel
import datetime
import logging
import sys

import glob
###############################################################################
#"""# IMPORT ADDITIONAL MODULES FOR THE MATRIX                                #
###############################################################################
path = 'R:/Jx4/tools/dcc/maya/scripts/starmanExporter/';
module = path+'sm_exportRig_maya.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import sm_exportRig_maya#sm_exportRig = reload(sm_exportRig);
module = path+'sm_generateRig.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import sm_generateRig#sm_generateRig = reload(sm_generateRig);

module = path+'sm_exportWeapon.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import sm_exportWeapon#sm_exportRig = reload(sm_exportRig);
module = path+'sm_generateWeapRig.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import sm_generateWeapRig#sm_generateRig = reload(sm_generateRig);
###############################################################################
# CHANGE THE STRING IN A FILE IF IT EXISTS                                    #
############################################################################### 
def changeStringInFile(exportedFile, oldString, newString):
    with open(exportedFile) as f:
        s = f.read();
        if oldString not in s:
            print '"{oldString}" not found in {exportedFile}.'.format(**locals());
            return
    with open(exportedFile, 'w') as f:
        print 'Changing "{oldString}" to "{newString}" in {exportedFile}'.format(**locals());
        s = s.replace(oldString, newString);
        f.write(s);
###############################################################################
# DETERMINES THE VALIDITY OF THE PREVIOUSLY SELECTED                          #
############################################################################### 
def EXPORTFILE(fileToExport,exportPath,fileName,home):
    autoKeyState = py.autoKeyframe(state=1,q=1);
    py.autoKeyframe(state=0);
    customFile = home+"CUSTOM.json" if(".json" not in home.split("/")[-1]) else home;
    customFileCheck = py.file(customFile, q=1, ex=1);
    if(customFileCheck == 1):
        with open(customFile, 'r') as f:
            line = json.load(f);
    if(fileToExport == "none"):
        fileToExport = line['BATCH FILES (FULL NAME)'].split(',')[0]; 
    pathExists = True;
    if not(os.path.exists(exportPath)):
        try:
            os.makedirs(exportPath);
        except:
            pathExists = False; 
    rigControllers = "none";
    selections = py.ls(sl=1);
    if(selections != []):
        RiGGiE = py.listAttr(selections[0], st=["RiGGiE"], r=1);
        if(isinstance(RiGGiE, list) == 1):
            rigControllers = selections[0]; 
            if(exportPath == "none"):
                exportPath = line['EXPORT FOLDER (PATH)'];
    if(rigControllers != "none" and pathExists == True):
        nameSpace = "";
        meshToExport = "none";
        name = rigControllers;
        if(":" in rigControllers):
            name = rigControllers.split(":")[-1];
            nameSpace = rigControllers[0:(len(rigControllers)-len(name))];
        masterCenter = name.replace("_L_","_M_").replace("_R_","_M_");
        masterName = masterCenter.replace(masterCenter.split("_")[2],"master");
        trajectoryName = masterCenter.replace(masterCenter.split("_")[2],"trajectory");
        masterController = nameSpace+masterName.replace(masterName.split("_")[-1],"CTRL");
        trajectoryController = nameSpace+trajectoryName.replace(trajectoryName.split("_")[-1],"CTRL");
        trajectoryConstraint = trajectoryController.replace("CTRL","CON").replace("c_","b_");
        trajectoryJoint = py.listConnections(trajectoryConstraint,d=1)[0];
###############################################################################
# XMD AND FBX PLUGIN INFO                                                     #
###############################################################################
        dialog = "";
        xmdPlugin = "MayaXMDExportPlugin2016";
        if(line['EXPORT AS .XMD'] == 1 and py.pluginInfo(xmdPlugin,l=1,q=1) == 0):
            try:
                xmdPlugin = py.pluginInfo(xmdPlugin,p=1,q=1);
                py.loadPlugin(xmdPlugin);
            except:
                py.headsUpMessage('"You need to install the XMD exporter to export XMD files." - HiGGiE', t=3);
                print "You need to install the XMD exporter to export XMD files"; 
                dialog = py.confirmDialog(t="Export Alert!",
                m="The Matrix is attempting to export an XMD file, but it is not installed.",
                b=["Cancel Export"],
                db="Cancel Export",cb="Cancel Export",ds="Cancel Export");
        fbxPlugin = "fbxmaya";
        if(line['EXPORT AS .FBX'] == 1 and py.pluginInfo(fbxPlugin,l=1,q=1) == 0):
            try:
                fbxPlugin = py.pluginInfo(fbxPlugin,p=1,q=1);
                py.loadPlugin(fbxPlugin);
            except:
                py.headsUpMessage('"You need to install the FBX exporter to export FBX files." - HiGGiE', t=3);
                print "You need to install the FBX exporter to export FBX files";
                dialog = py.confirmDialog(t="Export Alert!",
                m="The Matrix is attempting to export an FBX file, but it is not installed.",
                b=["Cancel Export"],
                db="Cancel Export",cb="Cancel Export",ds="Cancel Export");
###############################################################################
#"""# GETS THE CONTROLLERS OF THE RIG TO BE EXPORTED                          #
###############################################################################
        if(dialog == ""):
            controlWithMostKeys = [];
            outputControllers = [];
            outputItems = py.listRelatives(masterController,ad=1,pa=1);
            outputControllerShapes = [s for s in outputItems if "CTRL" in s];
            outputShapes = [s for s in outputItems if "Shape" in s];
            outputItems = list(set(outputControllerShapes) - set(outputShapes));
            i=0;
            while(i < len(outputItems)):
                if(outputItems[i].split("_")[-1] == "CTRL"):
                    outputControllers.append(outputItems[i]);
                i+=1;
            outputControllers.insert(0,masterController);
            outputJoint = trajectoryJoint;
            outputRoot = py.ls(outputJoint,l=1)[0].split("|")[1];
###############################################################################
#"""# FIND THE SOONEST AND LATEST KEYS OF ALL OUTPUT ITEMS                    #
###############################################################################
            translationValues = ["translateX","translateY","translateZ"];
            rotationValues = ["rotateX","rotateY","rotateZ"];
            keyableValues = translationValues+rotationValues;
            firstFrame = 0;
            lastFrame = 0;
            i=0;
            while(i < len(outputControllers)):
                currentFirstKey = 0;
                currentLastKey = 0;
                if not any(s in outputControllers[i] for s in keyableValues):#IN CASE ITEM IS KEY
                    isKeyed = py.keyframe(outputControllers[i],q=1);
                    if(isinstance(isKeyed,list) == 1):
                        currentFirstKey = round(py.findKeyframe(outputControllers[i],w="first"),0);
                        currentLastKey = round(py.findKeyframe(outputControllers[i],w="last"),0);
                        if(currentFirstKey < firstFrame):
                            firstFrame = currentFirstKey
                        if(currentLastKey > lastFrame):
                            lastFrame = currentLastKey
                i+=1;
            #OVERRIDE KEYFRAME RANGE WITH TIMELINE RANGE
            firstFrame = py.playbackOptions(min=1,q=1);
            lastFrame = py.playbackOptions(max=1,q=1);
            if(firstFrame != lastFrame):
                exportType = "animation";
                difference = 0-firstFrame;
                py.playbackOptions(minTime=0, maxTime=lastFrame+difference);
###############################################################################
#"""# CREATES SKELETON FROM ANIMATED RIG                                      #
###############################################################################
                outputJoints = py.listRelatives(outputRoot,type="joint",ad=1,pa=1,s=0);
                outputJoints.reverse();
                outputJoints.insert(0,outputRoot);
                visibility = outputRoot+".v";    
                mel.eval("source channelBoxCommand; CBdeleteConnection \"%s\""%visibility);
                py.setAttr(outputRoot+".v", 1);py.select(masterController,r=1);
                exportRoot = py.duplicate(outputRoot, ic=0, rr=1);
                if(nameSpace == ""):
                    py.rename(outputRoot,"b_M_temporary_v1_JNT");
                    correctedName = exportRoot.replace("T1","T");
                    exportRoot = py.rename(exportRoot,correctedName);
                exportSkeleton = py.listRelatives(exportRoot[0],type="joint",ad=1,pa=1,s=0);
                exportSkeleton.reverse();
                exportSkeleton.insert(0,exportRoot[0]);
                i=0;
                while(i < len(outputJoints)):
                    py.xform(exportSkeleton[i], p=1, roo="xyz");
                    py.parentConstraint(outputJoints[i],exportSkeleton[i],mo=1,w=1);
                    i+=1;
###############################################################################
#"""# BAKE SIMULATION                                                         #
###############################################################################
                bakeAttributes = ["tx","ty","tz","rx","ry","rz"];
                py.headsUpMessage('"Baking skeleton for export..." - HiGGiE', t=2);
                py.bakeResults(exportSkeleton[:],t=(firstFrame,lastFrame),at=bakeAttributes,bol=0,sm=1,s=1);
                py.select(exportSkeleton[:],r=1);
                py.keyframe(tc=difference,time=(firstFrame,lastFrame),r=1,e=1);
                #REMOVE FROM LAYER
                assestsToExport = exportSkeleton[:];
                i=0;
                while(i < len(assestsToExport)):
                    checkAxis = ["x","y","z"];
                    ii=0;
                    while(ii < len(checkAxis)):
                        target = assestsToExport[i]+".s"+checkAxis[ii];
                        scalePlug = py.listConnections(target,p=1);
                        if(isinstance(scalePlug,list) == 1):
                            py.disconnectAttr(scalePlug[0],target);
                        ii+=1;
                    py.setAttr(assestsToExport[i]+".s", 1, 1, 1); 
                    displayLayer = py.listConnections(assestsToExport[i], t="displayLayer", s=1);
                    if(isinstance(displayLayer, list) == True):
                        py.disconnectAttr(displayLayer[0]+".drawInfo", assestsToExport[i]+".drawOverride");
                    i+=1;
###############################################################################
#"""# CREATES SKELETON FROM BASE RIG                                          #
###############################################################################
            else:
                exportType = "base rig";
                exportRoot = py.duplicate(outputRoot, ic=0, rr=1);
                if(nameSpace == ""):
                    #IF NOT REFERENCED, REMOVE "1" FROM END OF NAME
                    py.rename(outputRoot,"b_M_temporary_v1_JNT");
                    correctedName = exportRoot.replace("T1","T");
                    exportRoot = py.rename(exportRoot,correctedName);
                exportSkeleton = py.listRelatives(exportRoot[0],type="joint",ad=1,pa=1,s=0);
                exportSkeleton.reverse();
                exportSkeleton.insert(0,exportRoot[0]);
                i=0;
                while(i < len(exportSkeleton)):
                    py.xform(exportSkeleton[i], p=1, roo="xyz");
                    i+=1;
                #IF SKIN CLUSTER ON ORIGINAL SKELETON, GET GEOMETRY
                isCluster = py.listConnections(outputRoot,type="skinCluster");
                if(isinstance(isCluster,list) == 1):
                    skinClusters = list(set(isCluster));
                    i=0;
                    while(i < len(skinClusters)):
                        deformdedGeometry = py.skinCluster(skinClusters[i],g=1,q=1);
                        if(isinstance(deformdedGeometry,list) == 1):
                            
                            tweaks = py.listConnections(deformdedGeometry[i],type="tweak");
                            if(isinstance(tweaks,list) == 1):
                                mesh = py.listConnections(tweaks[0],type="mesh");
                                if(isinstance(mesh,list) == 1):
                                    meshToExport = py.duplicate(mesh[0], ic=0, rr=1)[0];
                                    if(nameSpace == ""):
                                        #IF NOT REFERENCED, REMOVE "1" FROM END OF NAME
                                        py.rename(mesh[0],"a_M_temporary_v1_GEO");
                                        correctedName = meshToExport.replace("O1","O");
                                        exportRoot = py.rename(meshToExport,correctedName); 
                                    exportCluster = py.skinCluster(meshToExport, exportRoot[0], mi=5, nw=1, bm=0, sm=0, dr=4.0);
                                    py.copySkinWeights(ss=skinClusters[0],ds=exportCluster[0],ia="closestJoint",sa="closestPoint",nm=1);
                                    break;
                        i+=1;
###############################################################################
#"""# DETERMINE FILE NAME                                                     #
###############################################################################
            if(fileName == "none"):
                weaponID = "00";
                nameCheck = "pass";
                fileName = py.file(sn=1,q=1);
                fileName = fileName.split("/")[-1].split(".")[0] if(len(fileName) != 0) else "noName";
                if(fileName != "noName"):
                    potentialID = fileName.split("_")[-1].split(".")[0];
                    weaponID = potentialID if(potentialID.isdigit() == 1) else "00";
            else:
                potentialID = fileName.split("_")[-1].split(".")[0];
                weaponID = potentialID if(potentialID.isdigit() == 1) else "00";
            if(py.about(batch=1) == 0):     
                mel.eval('FBXExportInAscii -v true;FBXExportGenerateLog -v false;');
                mel.eval('FBXExportFileVersion "FBX201000"');
                mel.eval('FBXExportInputConnections -v 0');
###############################################################################
#"""# EXPORT RIG BODY AS AN FBX FILE                                          #
###############################################################################
            newFileName = fileName+"_BODY" if(exportType == "animation") else fileName;
            if(line['EXPORT AS .FBX'] == 1):
                py.select(exportSkeleton[0], r=1);
                if(meshToExport != "none"):
                    py.select(meshToExport, add=1);
                if(os.path.isdir(exportPath+newFileName) == 1 and path != "fail"):
                    p.open_for_edit(exportPath+newFileName+".fbx".replace("R:", userDrive))
                mel.eval('FBXExport -f "'+exportPath+newFileName+'" -s');
###############################################################################
#"""# EXPORT RIG BODY AS AN XMD FILE (IF THE PLUGIN IS ACTIVE)                #
###############################################################################
            if(line['EXPORT AS .XMD'] == 1):
                try:#EXPORT BODY AS XMD
                    py.select(exportSkeleton[:], r=1);
                    if(meshToExport != "none"):
                        py.select(meshToExport, add=1);
                    if(os.path.isdir(exportPath+newFileName) == 1 and path != "fail"):
                        p.open_for_edit(exportPath+newFileName+".xmd".replace("R:", userDrive))                  
                    i=0;
                    while(i < len(exportSkeleton)):
                        py.xform(exportSkeleton[i], p=1, roo="xyz");
                        i+=1;
                    xmdoptions = "-xmd_version=5;-anim=1;-ascii=1;-constraints=0;-timeline=1;"; 
                    py.file(exportPath+newFileName+".xmd",type="XMD Export",options=xmdoptions,es=1,f=1);
                    #CHANGE ANIMATION TAKE STRING TO UNTITLED
                    sceneName = py.file(sn=1,q=1);
                    sceneName = sceneName.split("/")[-1].split(".")[0] if(sceneName != "") else "untitled";
                    changeStringInFile(exportPath+newFileName+".xmd", 'ANIMATION_TAKE "'+sceneName+'"', 'ANIMATION_TAKE "untitled"');
                except:
                    pass;
###############################################################################
#"""# EXPORT RIG HEAD AS AN FBX FILE                                          #
###############################################################################
            if(py.objExists(nameSpace+"c_M_face_v1_GRP") == True):
                newFileName = fileName+"_FACE" if(exportType == "animation") else fileName;
                if(line['EXPORT AS .FBX'] == 1):
                    py.select(exportSkeleton[:], r=1);py.cutKey();
                    py.select(exportSkeleton[0], baseFaceExport[0], blendShapesExport[:], hi=1, r=1);
                    if(os.path.isdir(exportPath+newFileName) == 1 and path != "fail"):
                        p.open_for_edit(exportPath+newFileName+".fbx".replace("R:", userDrive));
                    mel.eval('FBXExport -f "'+exportPath+newFileName+'" -s');
                    py.rename(outputRoot,"b_M_temporary_v1_JNT");
                    correctedName = exportRoot.replace("T1","T");
                    exportRoot = py.rename(exportRoot,correctedName);\
###############################################################################
#"""# EXPORT RIG HEAD AS AN XMD FILE (IF THE PLUGIN IS ACTIVE)                #
###############################################################################
                if(line['EXPORT AS .XMD'] == 1):
                    try:#EXPORT HEAD AS XMD 
                        py.select(exportSkeleton[:], baseFaceExport[0], blendShapesExport[:], hi=1, r=1);
                        if(os.path.isdir(exportPath+newFileName) == 1 and path != "fail"):
                            p.open_for_edit(exportPath+newFileName+".xmd".replace("R:", userDrive))
                        py.file(exportPath+newFileName+".xmd", type="XMD Export", options="xmdoptions", es=1, f=1);
                        #CHANGE ANIMATION TAKE STRING TO UNTITLED
                        sceneName = py.file(sn=1,q=1);
                        sceneName = sceneName.split("/")[-1].split(".")[0] if(sceneName != "") else "untitled";
                        changeStringInFile(exportPath+newFileName+".xmd", 'ANIMATION_TAKE "'+sceneName+'"', 'ANIMATION_TAKE "untitled"');
                    except:
                        pass;
###############################################################################
#"""# EXPORT STARMAN RIG                                                      #
###############################################################################
            if(line['EXPORT STARMAN'] == 1 or line['EXPORT STARMAN WEAPON'] == 1):
                smDataPath = "R:/Jx4/tools/dcc/maya/scripts/starmanExporter/starman_settings/sm_data.json";
                smNameSpace = "";#nameSpace
                smFileName = fileName;
                numType = "integer";
                weapon = "weapon_"+weaponID;
                
                smLogPath = "R:/Jx4/tools/dcc/maya/scripts/starmanExporter/logs/";
                smCurrentTime = datetime.datetime.now()
                smLogStatus = logging.getLogger(__name__);
                hdlr = logging.FileHandler(smLogPath + 'starman_'
                                           + str(smCurrentTime.year) + '_'
                                           + str(smCurrentTime.month) + '_'
                                           + str(smCurrentTime.day) + '_'
                                           + str(smCurrentTime.hour) + '_'
                                           + str(smCurrentTime.minute) + '_'
                                           + str(smCurrentTime.second) + '_' + '.log');
                formatter = logging.Formatter('%(asctime)s %(message)s');
                hdlr.setFormatter(formatter);
                smLogStatus.addHandler(hdlr);
                smLogStatus.setLevel(logging.INFO);
                    
                if(fileName == "noName"):
                    if(exportType == "base rig" and len(nameSpace.split(":")) > 2):
                        smFileName="CHAR_starmanExport";
                    elif(exportType == "base rig" and len(nameSpace.split(":")) <= 2):
                        smFileName="RIG_starmanExport";
                    else:
                        smFileName="ANIM_starmanExport";

                sm_generateRig.main(weapon);
                if(line['EXPORT STARMAN'] == 1):
                    sm_export = sm_exportRig_maya.sm_export_rig(smDataPath, smFileName, smNameSpace, numType,
                                                           masterController, exportPath);
                if(line['EXPORT STARMAN WEAPON'] == 1):
                    smDataPath = "R:/Jx4/tools/dcc/maya/scripts/starmanExporter/starman_settings/sm_weapon_data.json";
                    sm_export = sm_exportWeapon.sm_export_rig(smDataPath, smFileName, smNameSpace, numType,
                                                           masterController, exportPath, smLogStatus, weapon);
                                                               
                sm_export.check_scene();
                sm_export.get_animation_data();
                
                smNodes = py.ls("*_SMN");
                if(len(smNodes) > 0):
                    py.delete(smNodes);
                
                print '"Successfully exported Starman to: ' +  exportPath + '" - HiGGiE';
                py.headsUpMessage('"Successfully exported Starman to: ' +  exportPath + '" - HiGGiE', t=3);
###############################################################################
#"""# FINALIZE/CLEANUP SCENE                                                  #
###############################################################################
            py.delete(exportSkeleton[0]); 
            if(nameSpace == ""):
                py.rename("b_M_temporary_v1_JNT", "b_M_origin_v1_JNT");
            py.setAttr(outputRoot+".v", 0);
            mel.eval("delete `ls -type unknown -type unknownDag -type unknownTransform`");
            if(line['EXPORT AS .MA'] == 1):
                fileName = fileName.replace("_BODY","");#!
                py.file(rename=exportPath+fileName+".ma");
                py.file(save=1, type="mayaAscii");
            py.select(masterController,r=1);
            print '"Successfully exported '+exportType+' to: ' +  exportPath + '" - HiGGiE';
            py.headsUpMessage('"Successfully exported '+exportType+' to: ' +  exportPath + '" - HiGGiE', t=3);
        else:
            print '"Relevant plugin to user settings is not installed." - HiGGiE';
            py.headsUpMessage('"Relevant plugin to user settings is not installed." - HiGGiE', t=3);
    elif(rigControllers != "none" and pathExists == False):
        print '"Must select a valid path before exporting!" - HiGGiE';
        py.headsUpMessage('"Must select a valid path before exporting!" - HiGGiE', t=4);
    else:
        print '"Must select a valid controller before exporting!" - HiGGiE';
        py.headsUpMessage('"Must select a valid controller before exporting!" - HiGGiE', t=4);
    py.autoKeyframe(state=autoKeyState);     
