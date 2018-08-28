###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import os
import json
import maya.cmds as py
###############################################################################
#"""# UPDATES UI'S IMPORT TEXT FIELD AND UPDATES SAVED SETTINGS               #
###############################################################################   
def RIGFIELD(editRigWidget, home):
    correct = ["HULK","Hulk","hulk","SPIDERMAN","Spiderman","spiderman",
               "IRONMAN","Ironman","ironman","CAPTAIN AMERICA","Captain America",
               "captain america"];
    almostCorrect = ["Batman","Aqua Man","War Machine","Wonder Woman","Flash",
                     "Superman","Joker","Hawkeye","Black Widow","Daredevil",
                     "Hawk Girl","Marvel","DC","comics"];
    customFile = py.file(home+"CUSTOM.json", q=1, ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
        #dialog = py.promptDialog(t="Password",m="What is the password?",
        #b=["ANSWER","CANCEL"],db="ANSWER",cb="CANCEL",ds="CANCEL");
        #answer = py.promptDialog(text=1,q=1);
        answer = "Hulk";#!
        if(answer != ""):
            if any(answer in s for s in correct):
                print '"Correct! You may now select a rig to reference." - HiGGiE';
                py.headsUpMessage('"Correct! You may now select a rig to reference." - HiGGiE', t=3);
                selectedFile = py.fileDialog2(cap = "RIG FILE TO IMPORT", ff="*.ma", dir=line['RIG (FULL NAME)'], okc="SELECT", cc="CANCEL", ds=2, fm=1);
                if(isinstance(selectedFile, list)):
                    if("/" in selectedFile[0]):
                        os.remove(home+"CUSTOM.json");
                        paths = selectedFile[-1];
                        sections = selectedFile[-1].split("/"); 
                        DIR = selectedFile[-1].replace(sections[len(sections)-1],"");
                        line['RIG (FULL NAME)'] = paths+"\r\n";
                        presets = line;
                        with open(home+'CUSTOM.json', 'w+') as f:
                             json.dump(presets, f, sort_keys=False, indent=4);
                        editRigWidget.setText(line['RIG (FULL NAME)']);
            elif any(answer in s for s in almostCorrect):
                print '"You got the right idea! But still wrong answer!" - HiGGiE';
                py.headsUpMessage('"You got the right idea! But still wrong answer!" - HiGGiE', t=3);
            else:
                print '"Wrong Answer!" - HiGGiE';
                py.headsUpMessage('"Wrong answer!" - HiGGiE', t=3);
            