###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################   
import os 
import json
import maya.cmds as py
###############################################################################
#"""# UPDATES UI'S CHECKBOXES                                                 #
###############################################################################   
def CHECKBOXES(value, dictionary, home):
    customFile = py.file(home+"CUSTOM.json", q=1, ex=1);
    if(customFile == 1):
        with open(home+'CUSTOM.json', 'r') as f:
            line = json.load(f);
        os.remove(home+"CUSTOM.json"); 
        if(value != 'none'):
            if(dictionary == "SCALE IK"):
                line[dictionary] = value if(value.replace(".","").isdigit() == 1) else "1.0";
            else:
                line[dictionary] = value;
        else:#BOOLEAN VALUES
            if(line[dictionary] == 0):
                line[dictionary] = 1;
            else:
                line[dictionary] = 0;
        presets = line;
        with open(home+'CUSTOM.json', 'w+') as f:
             json.dump(presets, f, sort_keys=False, indent=4);
def LAYER(log=None):
    if not log:
        import logging
        log = logging.getLogger();
    disLayers = py.ls(type = "displayLayer");
    disLayers.remove("defaultLayer");
    if disLayers :
        for x in disLayers:
            try:
                py.delete(x);
            except:
                import traceback
                
