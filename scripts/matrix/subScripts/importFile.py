###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################   
import os
import sys
import json
import maya.cmds as py
import maya.mel as mel
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
module = path+'animationTransfer.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import animationTransfer# = reload();
###############################################################################
#"""# IMPORTS THE FILE INTO THE SCENE AND THEN CALLS FOR AN ANIMATION TRANSFER#
###############################################################################
def IMPORTFILE(outputReference,listImportWidget,batchMode,home):
    py.scriptEditorInfo(suppressWarnings=1, e=1);
    validSelection = 0;
    animationSelection = True;
    if(str(listImportWidget) != "none" and ("." not in str(listImportWidget) or "<" in str(listImportWidget))):
        #IF FILE NAME ISN'T PROVIDED BY OUTSIDE SOURCES, GET IT FROM LIBRARY
        try:
            selectedAnimation = listImportWidget.currentItem().text();
        except:
            animationSelection = False;
    customFile = home+"CUSTOM.json" if(".json" not in home.split("/")[-1]) else home;
    customFileCheck = py.file(customFile, q=1, ex=1);
    if(customFileCheck == 1):
        with open(customFile, 'r') as f:
            line = json.load(f);
    if(outputReference == "none" and animationSelection == True):
        outputReference = line['IMPORT FILE (PATH)']+selectedAnimation;
    #GET RIG PATH FROM CUSTOM (USE "LITE" PATH IF IN BATCH MODE) 
    rigPath = line['RIG (FULL NAME)'];   
    rigLitePath = rigPath.replace("CHAR_","LITE_");
    if(py.file(rigLitePath, q=1, ex=1) == 1 and line['EXPORT AS .MA'] == 0 and batchMode == 1 and animationSelection == True):
        rigPath = rigLitePath;
    inputNameSpace = "inputFile";
    outputNameSpace = "outputFile";
    i=1;
    while(py.namespace(exists=outputNameSpace) == 1):
        outputNameSpace = outputNameSpace+str(i);
        i+=1;
    i=1;
    while(py.namespace(exists=inputNameSpace) == 1):
        inputNameSpace = inputNameSpace+str(i);
        i+=1;
    #IF SELECTED, CHECK NAMESPACE IF CONTROLLER IS VALID
    selections = py.ls(sl=1);
    if(selections != [] and animationSelection == True):
        i=0;
        while(i < len(selections)):
            RiGGiE = py.listAttr(selections[i], st=["RiGGiE"], r=1);
            if(isinstance(RiGGiE, list) == 1):
                selections = selections[i];
                try:
                    filePath = py.referenceQuery(selections,filename=1);
                    if(":" in selections):
                        name = selections.split(":")[-1];
                    else:
                        name = selections;
                    if(len(selections) > len(name)):
                        nameSpace = selections[0:(len(selections)-len(name))];
                    else:
                        nameSpace = "";
                    if("_" in nameSpace):
                        correctedName = nameSpace.replace("_", "");
                        py.file(filePath, referenceNode="nameSpace",namespace=correctedName,e=1);
                        inputNameSpace = correctedName;
                    else:
                        inputNameSpace = nameSpace;
                except:
                    inputNameSpace = "none";
                validSelection = 1;
                break;
            if(i == len(selections)-1):
                selections = [];
                py.headsUpMessage('"No valid controllers selected..." - HiGGiE', t=2);
                print '"No valid controllers selected..." - HiGGiE';
            i+=1;
    #REFERENCE IN THE INPUT RIG (TARGET) AND output RIG (ANIMATED)
    if((py.file(rigPath, q=1, ex=1) == 1 or inputNameSpace == "none") and py.file(outputReference,q=1,ex=1) == 1 and animationSelection == True):
        #try:#IF FAILS, THEN USER IS IMPORTING THE SAME FILE INTO ITSELF
        py.file(outputReference, namespace=outputNameSpace, prompt=0, mnp=1, iv=1, gr=1, r=1);
        referenceGroup = py.ls(sl=1)[0];
        py.setAttr(referenceGroup+".v", 0);
        try:
            firstItem = py.listRelatives(referenceGroup,type="joint",c=1,s=0)[-1];
        except:
            firstItem = py.listRelatives(referenceGroup,type="joint",ad=1,s=0)[-1];
        nameSpaceBreakdown = firstItem.split(":")[:-1];
        officialOutputNameSpace = "";
        i=0;
        while(i < len(nameSpaceBreakdown)):
            officialOutputNameSpace = officialOutputNameSpace+nameSpaceBreakdown[i]+":";
            i+=1;
        outputNameSpace = officialOutputNameSpace[:-1];
        #IMPORT INPUT RIG IF NO RIG IS SELECTED
        if(inputNameSpace != "none" and validSelection == 0):
            initialObjects = py.ls(type="transform",o=1);
            py.file(rigPath, namespace=inputNameSpace, prompt=0, mnp=1, iv=1, r=1);
        #FIND OFFICIAL NAMESPACE OF INPUT RIG
        if(selections == []):
            allObjects = py.ls(type="transform",o=1);
            allTransforms = list(set(allObjects) - set(initialObjects));
            i=0;
            while(i < len(allTransforms)):
                if("_" in allTransforms[i]):
                    if(allTransforms[i].split("_")[-1] == "CTRL"):
                        rigController = allTransforms[i];
                        break;
                i+=1;
            if(":" in rigController):
                name = rigController.split(":")[-1];
                inputNameSpace = rigController[0:(len(rigController)-len(name))];
            else:
                inputNameSpace = "none";
            selections = rigController;
        joints = py.ls(outputNameSpace+":*", type="joint");
        if(joints != []):
            py.select(selections,r=1);
            animationTransfer.ANIMATIONTRANSFER(inputNameSpace,outputNameSpace,outputReference,home);
        else:
            py.headsUpMessage('"No joints found in animated file..." - HiGGiE', t=2);
            print '"No joints found in animated file..." - HiGGiE';
        #except:
        #    py.headsUpMessage('"Can not reference the same file into itself." - HiGGiE', t=2);
        #    print '"Can not reference the same file into itself." - HiGGiE';
    elif(animationSelection == False):
        py.headsUpMessage('"You must select a valid animation in the library." - HiGGiE', t=2);
        print '"You must select a valid animation in the library." - HiGGiE';
    else:
        py.headsUpMessage('"Import file(s) do not exist..." - HiGGiE', t=2);
        print '"Import file(s) do not exist..." - HiGGiE';
        
        