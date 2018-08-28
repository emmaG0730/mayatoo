###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################   
import os
import glob
import platform
import datetime
import maya.cmds as py
import maya.mel as mel
###############################################################################
#"""# IMPORT ADDITIONAL MODULES FOR THE MATRIX                                #
###############################################################################   
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/importFile.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import importFile
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/importField.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import importField
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/exportField.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import exportField
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/rigField.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import rigField
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/checkBoxes.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import checkBoxes
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/savePose.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import savePose
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/loadPose.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import loadPose
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/exportFile.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import exportFile
module = 'C:/Users/RedPanda/Documents/Scripts/MATRIX/batchExport.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import batchExport
###############################################################################
#"""# UI TO THE MATRIX                                                        #
#                                                                             #
# CUSTOM = [0-NAME, 1-COLOR1, 2-COLOR2, 3-DESKTOP, 4-FBXIMPORT, 5-EXPORT,     #
# 6-BATCH, 7-RIG, 8-HOTKEY PREFS, 9-FEET TRACKING, 10-ARM TRACKING, 11-SCALE, #
# 12-POSE PATH, 13-POSES]                                                     #
###############################################################################   
HOME = "INVALID";C = 0;
DOCUMENTS = os.path.expanduser("~");
DOCUMENTS = DOCUMENTS+"/";
DESKTOP = DOCUMENTS.replace("/Documents/", "/Desktop/");
OS = platform.system();
ALPHA = ["A:","B:","C:","D:","E:","F:","G:","H:","I:","J:","K:","L:","M:",
         "N:","O:","P:","Q:","R:","S:","T:","U:","V:","W:","X:","Y:","Z:"];
while(C < len(ALPHA)):
    if(os.path.isdir(DOCUMENTS.replace(DOCUMENTS[0:2], ALPHA[C])) == 1):
        HOME = DOCUMENTS.replace(DOCUMENTS[0:2], ALPHA[C]);
        break;
    elif(os.path.isdir(DESKTOP.replace(DESKTOP[0:2], ALPHA[C])) == 1):
        HOME = DESKTOP.replace(DESKTOP[0:2], ALPHA[C]);
        break;
    C+=1;
C = 0;
if(HOME != "INVALID"):
    CS = py.file(HOME+"CUSTOM.txt", q=1, ex=1);
    if(CS == 1):
        OUTPUT = open(HOME+"CUSTOM.txt", "r");
        LINE = OUTPUT.readlines();
        OUTPUT.close();
        if(isinstance(LINE, list) == False or len(LINE) < 14):
            os.remove(HOME+"CUSTOM.txt");
            INPUT = open(HOME+"CUSTOM.txt", "w+");
            INPUT.write("USER\r\n0.1,0.2,0.3\r\n0.05,0.1,0.15\r\n"+HOME+"\r\n"+HOME+"\r\n"+HOME+"\r\nEMPTY\r\nNO RIG\r\nRiGGiE\r\n1\r\n0\r\n1.0\r\n"+HOME+"\r\n"+HOME+"\r\n");  
            INPUT = open(HOME+"CUSTOM.txt", "r");
            LINE = INPUT.readlines();
            INPUT.close(); 
    else:
        INPUT = open(HOME+"CUSTOM.txt", "w+");
        INPUT.write("USER\r\n0.1,0.2,0.3\r\n0.05,0.1,0.15\r\n"+HOME+"\r\n"+HOME+"\r\n"+HOME+"\r\nEMPTY\r\nNO RIG\r\nRiGGiE\r\n1\r\n0\r\n1.0\r\n"+HOME+"\r\n"+HOME+"\r\n");  
        INPUT = open(HOME+"CUSTOM.txt", "r");
        LINE = INPUT.readlines();
        INPUT.close();  
###############################################################################
#"""# BASIC SETTINGS                                                          #
###############################################################################  
    #py.grid(sp=10, s = 140, d=1);
    py.currentUnit(time="ntsc");py.playbackOptions(ps=1, e=1, min=0);#30FPS
    #COLOR  
    COLOR1 = [];COLOR2 = [];
    COLOR1.append(float(LINE[1].split("\r\n")[0].split(",")[0]));
    COLOR1.append(float(LINE[1].split("\r\n")[0].split(",")[1]));
    COLOR1.append(float(LINE[1].split("\r\n")[0].split(",")[2]));
    COLOR2.append(float(LINE[2].split("\r\n")[0].split(",")[0]));
    COLOR2.append(float(LINE[2].split("\r\n")[0].split(",")[1]));
    COLOR2.append(float(LINE[2].split("\r\n")[0].split(",")[2]));   
###############################################################################
#"""# BUILD UI                                                                #
###############################################################################  
    TITLE = "MATRIX v0.1";
    VERSION = py.about(v=1);
    if (py.window("ANIMTRANS", exists=1)):
        py.deleteUI("ANIMTRANS"); 
    UI = py.window("ANIMTRANS", t=TITLE, w=590, h=800, bgc=COLOR1, s=0);
    if(VERSION == "2016"):
        TABS = py.tabLayout(innerMarginWidth=5, innerMarginHeight=5, bs="top");
    else:
        TABS = py.tabLayout(innerMarginWidth=5, innerMarginHeight=5);
###############################################################################
#"""# PAGE ONE (IMPORT/EXPORT)                                                #
############################################################################### 
    PAGE1 = py.rowColumnLayout(nc=3, cw=[(1,100),(2,450),(3,50)], co=[(1,"left", 5), (3,"right", 0), (3,"left", 5)]);
    py.columnLayout(w=590, h=800);
    py.rowColumnLayout(nc=3, cw=[(1,100),(2,450),(3,50)], co=[(1,"left", 5), (3,"right", 0), (3,"left", 5)]);
    py.separator(h=10, st="none");py.separator(h=10, st="none");py.separator(h=10, st="none");
    py.text(label="IMPORT PATH:", font="fixedWidthFont", rs=1);
    iPATH = py.textField(text = LINE[4], bgc=COLOR2, font="smallFixedWidthFont");
    iBROWSE = py.button("I", c="IMPORTFIELD(LINE, IMPORTPATH, IMPORTLIST, HOME, 0)", w=30);
###############################################################################
#"""# EXPORT                                                                  #
###############################################################################  
    py.separator(h=20, st="none");py.separator(h=20, st="none");py.separator(h=20, st="none");
    py.text(label="EXPORT PATH:", font="fixedWidthFont", rs=1);
    xPATH = py.textField(text = LINE[5], bgc=COLOR2, font="smallFixedWidthFont");
    xBROWSE = py.button("X", c="EXPORTFIELD(LINE, EXPORTPATH, POSEPATH, IMPORTLIST, POSELIST, HOME, 5)", w=30);
###############################################################################
#"""# RIG                                                                     #
############################################################################### 
    py.separator(h=20, st="none");py.separator(h=20, st="none");py.separator(h=20, st="none");
    py.text(label="REF RIG PATH:", font="fixedWidthFont", rs=1);
    rPATH = py.textField(text = LINE[7], bgc=COLOR2, font="smallFixedWidthFont", tcc="CHECKBOX()");
    rBROWSE = py.button("R", c="RIGFIELD(LINE, RIGPATH, HOME)", w=30);
###############################################################################
#"""# OPTIONS                                                                 #
############################################################################### 
    py.columnLayout(w=590, h=800);
    py.rowColumnLayout(nc=4, cw=[(1,140),(2,350),(3,50),(4,50)], co=[(1,"left", 0), (2,"left", 100), (3,"left", 0), (4,"right", 12)]);
    py.separator(h=60, st="none");py.separator(h=60, st="none");py.separator(h=60, st="none");py.separator(h=60, st="none");
    FEET = py.checkBox("FEET TRACKING", v=int(LINE[9]), cc="CHECKBOX(LINE)");
    HANDS = py.checkBox("HAND TRACKING", v=int(LINE[10]), cc="CHECKBOX(LINE)");
    py.text(label="SCALE x", font="fixedWidthFont",  rs=1);
    SCALE = py.textField(text=str(LINE[11][:3]), bgc=COLOR2, font="smallFixedWidthFont", tcc="CHECKBOXES(LINE)", w=34);
###############################################################################
#"""# IMPORT LIST                                                             #
############################################################################### 
    py.columnLayout(w=590, h=800);
    py.rowColumnLayout(nc=1, cw=[(1,570)], co=[(10,"both", 50)]);
    py.separator(h=20, st="none");
    py.button("importListOrderBar", en=0, l="BATCH FILES", h=30);
    topLIST = LINE[6].split(",");
    C = 0;LIST = [];
    while(C < len(topLIST)):
        LIST.append(topLIST[C].split("/")[-1]);C+=1;
    iLIST = py.iconTextScrollList("importList1", bgc=COLOR2, append=LIST, ams=1, h=450);
###############################################################################
#"""# EXECUTE                                                                 #
############################################################################### 
    py.columnLayout(w=590, h=800);
    py.rowColumnLayout(nc=3, cw=[(1,215),(2,155),(3,190)], co=[(1,"left", 5), (2,"left", 25), (3,"right", 5)]);
    py.separator(h=50, st="none");py.separator(h=50, st="none");py.separator(h=50, st="none");
    IN = py.button("IMPORT", c="IMPORTFILE()", w=90);
    OUT = py.button("EXPORT", c="EXPORTFILE()", w=90);############################################################################################################################
    INOUT = py.button("BATCH", c="BATCHEXPORT()", w=90);
    py.setParent("..");py.setParent("..");py.setParent("..");
    py.setParent("..");py.setParent("..");py.setParent("..");
    py.setParent("..");py.setParent("..");py.setParent("..");
###############################################################################
#"""# PAGE TWO (POSE LIBRARY)                                                 #
############################################################################### 
    PAGE2 = py.rowColumnLayout(nc=3, cw=[(1,100),(2,450),(3,50)], co=[(1,"left", 5), (3,"right", 0), (3,"left", 5)]);
    py.columnLayout(w=590, h=800);
    py.rowColumnLayout(nc=3, cw=[(1,100),(2,450),(3,50)], co=[(1,"left", 5), (3,"right", 0), (3,"left", 5)]);

    py.separator(h=10, st="none");py.separator(h=10, st="none");py.separator(h=10, st="none");
    py.text(label="POSE PATH:", font="fixedWidthFont", rs=1);
    pPATH = py.textField(text = LINE[12], bgc=COLOR2, font="smallFixedWidthFont");
    pBROWSE = py.button("S", c="EXPORTFIELD(LINE, EXPORTPATH, POSEPATH, IMPORTLIST, POSELIST, HOME, 12)", w=30);

    py.columnLayout(w=590, h=800);
    py.rowColumnLayout(nc=3, cw=[(1,215),(2,155),(3,190)], co=[(1,"left", 5), (2,"left", 25), (3,"right", 5)]);
    py.separator(h=20, st="none");py.separator(h=20, st="none");py.separator(h=20, st="none");
    IN = py.button("SAVE", c="SAVEPOSE(LINE, POSEPATH, POSELIST, HOME)", w=90);
    OUT = py.button("LOAD", c="LOADPOSE(LINE, POSEPATH, POSELIST)", w=90);
    INOUT = py.button("MIRROR", c="", en=0, w=90);
###############################################################################
#"""# POSE LIST                                                               #
############################################################################### 
    py.columnLayout(w=590, h=800);
    py.rowColumnLayout(nc=1, cw=[(1,570)], co=[(10,"both", 50)]);
    py.separator(h=20, st="none");
    py.button("importListOrderBar", en=0, l="POSE FILES", h=30);
    topLIST = LINE[13].split(",");
    C = 0;LIST = [];
    while(C < len(topLIST)):
        LIST.append(topLIST[C].split("/")[-1]);C+=1;
    pLIST = py.iconTextScrollList("importList2", bgc=COLOR2, append=LIST, ams=0, h=450);
    
    py.setParent("..");py.setParent("..");py.setParent("..");py.setParent("..");py.setParent("..");py.setParent("..");
    

###############################################################################
#"""# GENERATE UI                                                             #
############################################################################### 
    py.tabLayout(TABS, edit=1, tabLabel=( (PAGE1, "IMPORT/EXPORT"), (PAGE2, "POSE LIBRARY")) );   
    py.showWindow(UI);
    
    
    


    

