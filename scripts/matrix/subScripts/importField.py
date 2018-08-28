###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
##############################a################################################   
import os
import sys
import json
import maya.cmds as py
import maya.mel as mel
###############################################################################
#"""# UPDATES UI'S IMPORT TEXT FIELD AND UPDATES SAVED SETTINGS               #
###############################################################################   
def IMPORTFIELD(line, editImportWidget, listImportWidget, home):
    itemList = [];
    paths = "";
    customFile = py.file(home+"CUSTOM.json", q=1, ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
        folder = py.fileDialog2(cap="FILE TO IMPORT", dir=line['IMPORT FILE (PATH)'], okc="SELECT", cc="CANCEL", ds=2, fm=4);
        if(isinstance(folder,list) == 1):
            if("/" in folder[0]):
                os.remove(home+"CUSTOM.json");
                i=0;
                while(i < len(folder)):
                    paths = paths+folder[i];
                    paths = paths+",";
                    i+=1;
                sections = folder[0].split("/"); 
                directory = folder[0].replace(sections[len(sections)-1], "");
                line['IMPORT FILE (PATH)'] = directory;
                line['BATCH FILES (FULL NAME)'] = paths;
                presets = line;
                with open(home+'CUSTOM.json', 'w+') as f:
                     json.dump(presets, f, sort_keys=False, indent=4);
                editImportWidget.setText(line['IMPORT FILE (PATH)'])
                itemListItem = line['BATCH FILES (FULL NAME)'].split(",");
                listImportWidget.clear();
                i=0;
                while(i < len(itemListItem)):
                    if(len(itemListItem[i]) > 0):
                        listImportWidget.addItem(itemListItem[i].split("/")[-1]);
                    i+=1;
                listImportWidget.setCurrentRow(0);