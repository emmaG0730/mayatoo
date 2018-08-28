###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
import maya.cmds as py
import maya.mel as mel 
import os
from maya import cmds, OpenMaya
###############################################################################
#"""# CREATE FACIAL CONTROLLERS BASED ON SELECTED curves AND locators         #
###############################################################################
def FACE(BASE):
    C=0;
    initialSelection = py.ls(sl=1);
    nurbs = py.ls(type="nurbsCurve");
    locators = py.ls(type="locator");  
    facePoints = nurbs + locators;
    facePoints = py.listRelatives(facePoints, p=1);
    shapes = [];py.select(d=1);
    while(C < len(facePoints)):
        if(facePoints[C] in initialSelection):
            py.select(facePoints[C], add=1);
        C+=1;
    C=0;
    curves = py.ls(sl=1);
    shapes = py.listRelatives(s=1);
    original = py.rename(BASE, BASE.replace("a_", "d_"));
    GEO = py.duplicate(original, n=original.replace("d_", "a_"), rr=1, rc=1)[0];
    py.delete(GEO, ch=1);
    MAT = ["FACE_MAT"];
    ATTR = [".tx",".ty",".tz",".rx",".ry",".rz",".sx",".sy",".sz",".v"];
    while(C < len(ATTR)):
        py.setAttr(GEO+ATTR[C], l=0);C+=1; 
###############################################################################
#"""# CREATE SHADER FOR FACE MANIPULATORS                                     #
###############################################################################
    if(py.objExists(MAT[0]) == False):
        ctrlShader = py.shadingNode("shadingMap", asShader=True, n=MAT[0]);
        shadingGRP = py.sets(renderable=True,noSurfaceShader=True,empty=True);
        py.connectAttr('%s.outColor' %ctrlShader ,'%s.surfaceShader' %shadingGRP);
        py.setAttr(MAT[0]+".color", 0.032,0.48,0.814);
        py.setAttr(MAT[0]+".shadingMapColor", 0.032,0.48,0.814);
###############################################################################
#"""# CHECK REQUIREMENTS OF GEOMETRY AND shapes                               #
###############################################################################
    if(isinstance(shapes,list) == True):
        FOLLICLES = [];BINDERS = [];SUB_A = [];SUB_B = [];SCALE = 0.5;BLENDS = [];
        C = 0;py.delete(curves[:], ch=1);#CLEAN
        #FIND SCALE
        DDN = py.distanceDimension(sp = (0, 100, 0), ep = (0, 10, 0));
        DDN2 = py.pickWalk(d="up");py.select("locator1","locator2", r=1);
        DISTANCE = py.ls(sl=1);
        neckJoint = "b_M_neck_v1_JNT";
        headJoint = "b_M_head_v1_JNT";
        if(py.objExists(neckJoint) == True and py.objExists(headJoint) == True):
            SNAP1 = py.pointConstraint(neckJoint, DISTANCE[0], mo=0, w=1);
            SNAP2 = py.pointConstraint(headJoint, DISTANCE[1], mo=0, w=1);
            SCALE = py.getAttr(DDN+".distance");SCALE = SCALE/40;
            py.delete(DISTANCE[0], DISTANCE[1], DDN, DDN2);
###############################################################################
#"""# ADD LOCATORS TO curves WHERE MANIPULATORS WILL BE PLACED                #
###############################################################################
        while(C < len(shapes)):#PER CURVE SELECTED
            vNum=1;num=1;LOCATORS=[];CVLIST=[];iCVLIST=[];POS=[0];iC=0;
            S = curves[C].split("_");
            if(len(S) > 1):
                side = "L" if("l" in S[0] or "L" in S[0]) else "R";
            else:
                side = "M";
            try:
                SPANS = py.getAttr(shapes[C]+".spans");
                DEGREES = py.getAttr(shapes[C]+".degree");
                CVS = SPANS+DEGREES;
            except:
                CVS = 1;
            while(iC < CVS):
                CVLIST.append(shapes[C]+".cv"+str([iC]));
                iCVLIST.append(shapes[C]+".cv"+str([iC]));
                iC+=1;
            iC = 0;
###############################################################################
#"""# REMOVE 2ND TO LAST CVS ON BOTH ENDS OF THE CURVE                        #
###############################################################################
            try:
                CVLIST.remove(CVLIST[1]);CVLIST.remove(CVLIST[len(CVLIST)-2]);
                LIMIT = 3 if(len(CVLIST) <= 4) else len(CVLIST);
            except:
                LIMIT = 1;
            SNAP = 0.5 if(len(CVLIST) <= 4) else 1.0/(LIMIT-1);
            while(iC < LIMIT-1):
                POS.append(POS[-1]+SNAP);
                iC+=1;
            if("lowerLip" in CVLIST[0]):
                POS.remove(POS[0]);POS.remove(POS[-1]);
            iC = 0;oSide = side;
###############################################################################
#"""# CORRECT/ADJUST NAMING FOR THE FOLLOWING CONTROLLER                      #
###############################################################################
            while(iC < LIMIT):#PER CV IN CURVE
                STARTLIST = ["outer", "center", "inner", "", "inner", "center", "outer"];
                ENDLIST = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""];
                ENDLIST = ["", "", "", "", ""] if("lowerlip" in shapes[C] or "lowerLip" in shapes[C]) else ENDLIST;
                ENDLIST = ["Corner", "", "", "", "Corner"] if("upperlip" in shapes[C] or "upperLip" in shapes[C]) else ENDLIST;
                STARTLIST = ["inner", "center", "outer"] if ("pocket" in shapes[C] or "Pocket" in shapes[C] or "rim" in shapes[C] or "Rim" in shapes[C]) else STARTLIST;
                STARTLIST = ["upper", "center", "lower"] if("crease" in shapes[C] or ("cheek" in shapes[C] and "Bone" not in shapes[C] and "bone" not in shapes[C])) else STARTLIST;
                STARTLIST = ["", "", "", "", "", "", "", "", ""] if("lip" in shapes[C] or "Lip" in shapes[C]) else STARTLIST;
                END = ENDLIST[iC] if(LIMIT > 1) else "";
                START = STARTLIST[iC] if(LIMIT > 1) else "";iiC = 0;
                # NAMING ####################################################################################################################################
                S[-1] = "crease" if(S[-1] == "creese") else S[-1];S[-1] = "cheek" if(S[-1] == "cheak") else S[-1];                                        # #
                S[-1] = "eyebrow" if(S[-1] == "eyebrows" or S[-1] == "Eyebrows" or S[-1] == "eyeBrows") else S[-1];                                       # #
                S[-1] = "chin" if(S[-1] == "jaw") else S[-1];S[-1] = "forehead" if(S[-1] == "forhead") else S[-1];                                        # #
                S[-1] = S[-1][0].upper()+S[-1][1:] if(START != "") else S[-1];                                                                            # #
                LOC = py.spaceLocator(p=(0,0,0));                                                                                                         # #
                try:                                                                                                                                      # #
                    PATH = py.pathAnimation(LOC[0], shapes[C], fm=1, followAxis="x", upAxis="y");                                                         # #
                    py.setAttr(PATH+".u", POS[iC]);                                                                                                       # #
                except:                                                                                                                                   # #
                    D = py.parentConstraint(shapes[C].replace("Shape", ""), LOC[0], mo=0, w=1);py.delete(D);PATH = shapes[C];                             # #
                side = "L" if(round(py.xform(LOC[0],q=True,t=True,ws=True)[0],1) > 0.0) else "R";                                                         # #
                side = "M" if(round(py.xform(LOC[0],q=True,t=True,ws=True)[0],1) == 0.0) else side;                                                       # #
                nName = py.rename(LOC[0], "c_"+side+"_"+START+S[-1]+END+"_v"+str(num)+"_LOC");LOC[0] = nName;                                             # #
                nName = py.rename(PATH, "c_"+side+"_"+START+S[-1]+END+"_v"+str(num)+"_PATH");PATH = nName;                                                # #
                # NAMING ####################################################################################################################################
                ORIENT = 1 if(side != "R") else -1;
###############################################################################
#"""# DELETE NODE CREATING CYCLES THAT WERE GENERATED THROUGH PATHS           #
###############################################################################
                try:
                    CYCLE = py.listConnections(PATH,type="addDoubleLinear",s=1)
                    py.delete(CYCLE[:], PATH);
                except:
                    pass;
                py.setAttr(LOC[0]+".r", 0,0,0);
                JNT = py.joint(p=(0,0,0), radius=0, n=PATH.replace("PATH", "JNT").replace("upperLipCorner", "mouthCorner"));
                py.setAttr(JNT+".t", 0,0,0);py.setAttr(JNT+".sx", ORIENT);
                GRP1 = py.group(n=(PATH.replace("PATH", "GRP")).replace("_v","Sub_v"), em=1);
                GRP2 = py.group(n=PATH.replace("PATH", "GRP"), r=1);
                D = py.pointConstraint(LOC[0], GRP2, mo=0, w=1);py.delete(D);
                py.parent(JNT,GRP1);py.parent(GRP2,LOC[0]);#PARENT
                BALL  = py.polySphere(sx=7, sy=7, r=SCALE/2);
                nName = py.rename(BALL[0], PATH.replace("PATH", "CTRL").replace("upperLipCorner", "mouthCorner"));BALL = nName;
                cSHAPE = py.listRelatives(s=1);
                py.parent(cSHAPE, JNT, s=1, r=1);
                py.delete(nName);py.select(d=1);
                nName = py.rename(JNT, JNT.replace("JNT", "CTRL"));JNT = nName;
                py.select(JNT, r=1);py.hyperShade(assign=MAT[0]);py.select(d=1);
###############################################################################
#"""# ATTACH POINT TO SURFACE                                                 #
###############################################################################
                closest=py.createNode("closestPointOnMesh", n=JNT.replace("CTRL", "CPN"));                                                                
                py.connectAttr(GEO+".outMesh", closest+".inMesh");                                                                                       
                tVAL = py.xform(LOC[0], t=1, q=1);                                                                                                        
                py.setAttr(closest+".inPositionX", tVAL[0]);
                py.setAttr(closest+".inPositionY", tVAL[1]);
                py.setAttr(closest+".inPositionZ", tVAL[2]);      
                follicle = py.createNode("follicle",n=JNT.replace("CTRL","FOLShape"));
                py.pickWalk(d="Up");                                              
                FOL = py.ls(sl=1);py.rename(FOL[0], JNT.replace("CTRL", "FOL"));
                FOL[0] = JNT.replace("CTRL", "FOL");                                      
                follicleTrans = py.listRelatives(follicle, type="transform", p=1);                                                                        
                py.connectAttr(follicle+".outRotate", follicleTrans[0]+".rotate");                                                                        
                py.connectAttr(follicle+".outTranslate", follicleTrans[0]+".translate");                                                                  
                py.connectAttr(GEO+".worldMatrix", follicle+".inputWorldMatrix");                                                                         
                py.connectAttr(GEO+".outMesh", follicle+".inputMesh");                                                                                    
                py.setAttr(follicle+".simulationMethod", 0);                                                                                              
                U = py.getAttr(closest+".result.parameterU");                                                                                             
                V = py.getAttr(closest+".result.parameterV");                                                                                             
                py.setAttr(follicle+".parameterU", U);                                                                                                    
                py.setAttr(follicle+".parameterV", V);                                                                                                    
                H1 = py.pointConstraint(follicleTrans[0], LOC[0], n=LOC[0].replace(LOC[0][len(LOC[0])-3:],"CON"), mo=1, w=1);                             
                py.delete(closest);py.setAttr(H1[0]+".ihi",0);                                                                                            
###############################################################################
#"""# HIDE CONNECTION NODES                                                   #
###############################################################################
                py.setAttr(H1[0]+".ihi",0);
                py.select(d=1);py.delete(JNT, ch=1);#CLEAN
                ATTR = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"];
                while(iiC < len(ATTR)):
                    py.setAttr(JNT+ATTR[iiC], k=0, l=1, cb=0);iiC+=1; 
                FOLLICLES.append(FOL[0]);LOCATORS.append(LOC[0]);
                iC+=1;
                if("lowerLip" in CVLIST[0] and iC == 3):
                    iC=LIMIT;
            iC = 0;
            subGRP = py.group(n="c_"+side+"_"+S[-1]+"_v"+str(num)+"_GRP", em=1);
            SUB_A.append(subGRP);
            py.parent(LOCATORS[:], subGRP);
            py.select(subGRP, hi=1, r=1);
            A_LIST = py.ls(sl=1)
            DUP = py.duplicate(subGRP, rr=1, rc=1);py.select(DUP, hi=1, r=1);
            B_LIST = py.ls(sl=1);iC = len(B_LIST)-1;
            while(iC > -1):
                B_ITEM = py.rename(B_LIST[iC], B_LIST[iC].replace("_v", "B_v")[:len(B_LIST[iC])]);iC-=1;
            iC = 0;SUB_B.append(B_ITEM);
            py.select(B_ITEM, hi=1, r=1);
            B_LIST = py.ls(sl=1);
            while(iC < len(A_LIST)):
                if("CTRL" in A_LIST[iC] and "Shape" not in A_LIST[iC]):
                    py.connectAttr(A_LIST[iC]+".t", B_LIST[iC]+".t");
                    py.connectAttr(A_LIST[iC]+".s", B_LIST[iC]+".s");
                    MDN = py.createNode("multiplyDivide", n=A_LIST[iC].replace("CTRL", "MDN").replace("_v", "Translate_v"));
                    py.setAttr(MDN+".input2", -1,-1,-1);
                    py.connectAttr(A_LIST[iC]+".t", MDN+".input1");
                    py.connectAttr(MDN+".output", A_LIST[iC]+".rpt");
                    py.setAttr(MDN+".ihi",0);BINDERS.append(B_LIST[iC]);
                if("LOC" in A_LIST[iC] and "Shape" in A_LIST[iC]):
                    py.setAttr(A_LIST[iC]+".overrideEnabled", 1);
                    py.setAttr(A_LIST[iC]+".overrideDisplayType", 2);
                    py.setAttr(A_LIST[iC]+".overrideVisibility", 0);
                    py.setAttr(B_LIST[iC]+".overrideEnabled", 1);
                    py.setAttr(B_LIST[iC]+".overrideDisplayType", 2);
                    py.setAttr(B_LIST[iC]+".overrideVisibility", 0);
                iC+=1; 
            iC = 0;C+=1;
###############################################################################
#"""# ORGANIZE NODES IN GROUPS                                                #
###############################################################################
        py.delete(curves[:]);C = 0;
        if(py.objExists("c_M_face_v1_GRP") == True):#PARENTING
            py.parent(SUB_A[:],"c_M_manipulatorsA_v1_GRP");py.select(d=1);
            py.parent(SUB_B[:],"c_M_manipulatorsB_v1_GRP");py.select(d=1);
            py.parent(FOLLICLES[:],"c_M_follicle_v1_GRP");
        else:
            py.select(d=1);
            if(py.objExists("b_M_origin_v1_JNT") == True):
                BASE = py.duplicate("b_M_origin_v1_JNT", rr=1)[0];#BASE  = "b_root";
                py.select(BASE, hi=1);
                ITEMS = py.ls(sl=1, typ="joint");
                iC = len(ITEMS)-1;
                while(iC > -1):
                    py.rename(ITEMS[iC], ITEMS[iC].split("|")[-1].replace("b_", "c_").replace("1", ""));iC-=1;
                iC+=1;BASE = ITEMS[iC].split("|")[-1].replace("b_", "c_").replace("1", "");iC = 0;
            else:
                BASE = py.joint(p=(0,0,0), radius=0, n="c_root");
                D = py.parentConstraint(headJoint, BASE, mo=0, w=1);py.delete(D);
            py.select(BASE, r=1);
            eGRP = py.group(n="c_M_face_v1_GRP");
            aGRP = py.group(n="c_M_manipulatorsA_v1_GRP", em=1);
            bGRP = py.group(n="c_M_manipulatorsB_v1_GRP", em=1);
            cGRP = py.group(n="c_M_manipulatorsC_v1_GRP", em=1);
            dGRP = py.group(n="c_M_follicle_v1_GRP", em=1);
            py.parent(aGRP, bGRP, cGRP, dGRP, eGRP);
            BINDERS.append(BASE);
            py.setAttr(bGRP+".v", 0);py.setAttr(dGRP+".v", 0);
            py.parent(SUB_A[:],"c_M_manipulatorsA_v1_GRP");py.select(d=1);
            py.parent(SUB_B[:],"c_M_manipulatorsB_v1_GRP");py.select(d=1);
            py.parent(FOLLICLES[:],"c_M_follicle_v1_GRP");
        if(py.objExists("a_M_faceManipulators_v1_SHP") == False):#BLENDSHAPE
            BLEND = py.duplicate(GEO, n="a_M_faceCreator_v1_SHP", rr=1, rc=1)[0];#FACE CTREATOR
            BS = py.blendShape(BLEND, GEO, n="a_M_face_v1_BS")[0];
            py.setAttr(BS+"."+BLEND, 1);py.setAttr(BLEND+".v", 0);
            BLEND = py.duplicate(GEO, n="a_M_faceManipulators_v1_SHP", rr=1, rc=1)[0];#FACE CTRLS
            py.blendShape("a_M_face_v1_BS", e=1, t=(GEO,1,BLEND,1));
            py.setAttr(BLEND+".v", 0);py.setAttr(BS+"."+BLEND, 1);
            MASTERBLEND = BLEND;
###############################################################################
#"""#                                                #
###############################################################################
        MAIN = ["c_L_mouthCorner_v1_FOL", "c_R_mouthCorner_v1_FOL", "c_M_upperLip_v1_FOL", 
                "c_M_lowerLip_v1_FOL", "c_L_upperLid_v1_FOL", "c_R_upperLid_v1_FOL", 
                "c_L_centerCheek_v1_FOL", "c_R_centerCheek_v1_FOL", "c_M_noseBridge_v1_FOL", "c_M_nose_v1_FOL",
                "c_L_neck_v1_FOL", "c_M_neck_v1_FOL", "c_R_neck_v1_FOL",
                "c_L_centerEyebrow_v1_FOL", "c_R_centerEyebrow_v1_FOL", "c_M_chin_v1_FOL"];
        while(C < len(MAIN)):#MAIN CTRL SETUP
            iC = 0;LIMIT = 1 if("_M_" in MAIN[C]) else 1;ORIENT = 0;
            nNAME = MAIN[C].replace("_v","Main_v").replace("FOL","CTRL").replace("chin", "jaw").replace("upperLid", "eyelid").replace("noseMain", "nostrilMain");
            nNAME = nNAME.replace("centerEyebrow", "eyebrow").replace("centerCheek", "cheek").replace("Bridge", "");
            if(py.objExists(MAIN[C]) == True and py.objExists(nNAME) == False):
                num = 6 if("Eyebrow" in MAIN[C] or "nose_" in MAIN[C]) else 4;
                CTRL = py.circle(ch=1, o=1, nr=(0, 0, 1), s=num, r=SCALE*2, n=nNAME);
                GRP = py.group(n=MAIN[C].replace("_v","Main_v").replace("FOL","GRP"), r=1);
                py.setAttr(CTRL[0]+".overrideEnabled", 1);
                py.setAttr(CTRL[0]+".overrideColor", 13);
                if("centerEyebrow" not in MAIN[C]):
                    ATTR = [".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"] 
                else:
                    ATTR = [".tz",".rx", ".ry", ".sx", ".sy", ".sz", ".v"];
                while(iC < len(ATTR)):
                    py.setAttr(CTRL[0]+ATTR[iC], k=0, l=1, cb=0);iC+=1; 
                iC = 0;
                if("jaw" in CTRL[0]):
                    py.setAttr(CTRL[0]+".tz", l=0, cb=1);
                    py.setAttr(CTRL[0]+".tz", k=1);
                if("jaw" not in CTRL[0]):
                    py.transformLimits(CTRL[0], tx=(LIMIT*-1, LIMIT), ty=(LIMIT*-1, LIMIT), tz=(LIMIT*-1, LIMIT), etx=(1, 1), ety=(1, 1), etz=(1, 1));
                if("eyebrowMain" in CTRL[0]):
                    py.transformLimits(CTRL[0], rz=(15*-1, 15), erz=(1, 1));
                    py.setAttr(CTRL[0]+".tz", k=0, l=1, cb=0);
                if("noseMain" in CTRL[0]):
                    py.setAttr(CTRL[0]+".tx", k=0, l=1, cb=0);
                    py.setAttr(CTRL[0]+".tz", k=0, l=1, cb=0);
                if("cheekMain" in CTRL[0] or "L_neckMain" in CTRL[0] or "R_neckMain" in CTRL[0]):
                    py.setAttr(CTRL[0]+".ty", k=0, l=1, cb=0);
                    py.setAttr(CTRL[0]+".tz", k=0, l=1, cb=0);
                if("LipMain" in CTRL[0]):
                    py.setAttr(CTRL[0]+".tx", k=0, l=1, cb=0);
                    py.setAttr(CTRL[0]+".tz", l=0, cb=1);py.setAttr(CTRL[0]+".tz", k=1);
                    py.setAttr(CTRL[0]+".rx", l=0, cb=1);py.setAttr(CTRL[0]+".rx", k=1);
                    py.setAttr(CTRL[0]+".sy", l=0, cb=1);py.setAttr(CTRL[0]+".sy", k=1);
                    py.transformLimits(CTRL[0], rx=(-15, 0), erx=(1, 1));
                D = py.pointConstraint(MAIN[C], GRP, mo=0, w=1);py.delete(D);
                py.setAttr(GRP+".tz", py.getAttr(GRP+".tz")+SCALE*1.5);#CTRL DISPLACEMENT
                H1 = py.pointConstraint(MAIN[C], GRP, n=GRP.replace(GRP[len(GRP)-3:],"CON"), mo=1, w=1);
                py.parent(GRP, "c_M_manipulatorsC_v1_GRP");py.setAttr(H1[0]+".ihi",0);  
                MDN = py.createNode("multiplyDivide", n=CTRL[0].replace("CTRL", "MDN"));
                py.setAttr(MDN+".input2", -1,-1,-1);py.connectAttr(CTRL[0]+".t", MDN+".input1");
                py.connectAttr(MDN+".output", CTRL[0]+".rpt");py.setAttr(MDN+".ihi",0);
                if(py.objExists("b_M_jaw_v1_JNT") == True and "jaw" in CTRL[0]):
                    MDN = py.createNode("multiplyDivide", n="c_M_jaw_v1_MDN");
                    SKIN = mel.eval('findRelatedSkinCluster("a_M_face_v1_GEO")');
                    py.setAttr(MDN+".input2", 7,7,-1);
                    py.connectAttr(CTRL[0]+".ty", MDN+".input1X");
                    py.connectAttr(CTRL[0]+".tx", MDN+".input1Y");
                    ADL = py.createNode("addDoubleLinear", n="c_M_jaw_v1_ADL");
                    py.setAttr(ADL+".input1", (py.getAttr("b_M_jaw_v1_JNT.ty")));
                    py.connectAttr(CTRL[0]+".tz", MDN+".input1Z");
                    py.connectAttr(MDN+".outputZ", ADL+".input2");
                    py.connectAttr(MDN+".outputX", "b_M_jaw_v1_JNT.rz");
                    py.connectAttr(MDN+".outputY", "b_M_jaw_v1_JNT.ry");
                    py.connectAttr(ADL+".output", "b_M_jaw_v1_JNT.ty");
                    py.setAttr(MDN+".ihi",0);py.setAttr(ADL+".ihi",0);
###############################################################################
#"""# CREATE CONTROLLER shapes BY ALTERING THEIR CV POSITIONS                 #
###############################################################################
                if(C == 0 or C == 1 or C == 6 or C == 7 or C == 10 or C == 12):
                    #LEFT AND RIGHT (MOUTH & CHEEKS)
                    py.move(1.5,0,0, CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
                    py.move(-0.5,0,0, CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                    py.move(0.5,0,0,CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
                    py.move(-0.5,0,CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                    ORIENT = -1 if("_R_" in CTRL[0]) else 1;
                    py.setAttr(GRP+".sx", ORIENT);   
                    if(C == 10 or C == 12):
                         py.setAttr(CTRL[0].replace("CTRL", "GRP")+".s", 2*ORIENT,2,2);
                         py.transformLimits(CTRL[0], tx=(0, LIMIT), etx=(1, 1));
                if(C == 9):
                    #NOSTRILS
                    py.move(0,-1,-1.8, CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                    py.move(0,1,-1.8, CTRL[0]+"Shape.cv[4]",r=1,os=1,wd=1);
                    py.move(0.9,0.8,-1.8, CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
                    py.move(0.9,-0.8,-1.8, CTRL[0]+"Shape.cv[5]",r=1,os=1,wd=1);
                    py.move(-0.9,0.8,-1.8, CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
                    py.move(-0.9,-0.8,-1.8, CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                    py.setAttr(CTRL[0]+".sx",k=1,l=0,cb=1);py.setAttr(CTRL[0]+".sx",k=1);
                    py.setAttr(CTRL[0]+".sy",k=1,l=0,cb=1);py.setAttr(CTRL[0]+".sy",k=1);
                    py.setAttr(CTRL[0]+".sz",k=1,l=0,cb=1);py.setAttr(CTRL[0]+".sz",k=1);
                    py.setAttr(CTRL[0]+".tx",k=0,l=1,cb=0);py.setAttr(CTRL[0]+".ty",k=0,l=1,cb=0);
                    py.xform(CTRL[0], cpc=1);
                    nADL = py.createNode("plusMinusAverage", n=CTRL[0].replace("CTRL", "PMA"));
                    py.connectAttr(CTRL[0]+".sx", nADL+".input3D[0].input3Dx");
                    py.connectAttr(CTRL[0]+".sy", nADL+".input3D[1].input3Dx");
                    py.connectAttr(CTRL[0]+".sz", nADL+".input3D[2].input3Dx");
                if(C == 2 or C == 3 or C == 11):
                    #UP AND DOWN (MOUTH)
                    py.move(0,1.5,0, CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                    py.move(0,-0.5,0, CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
                    py.move(0,0.5,0,CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                    py.move(0,-0.5,0,CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
                    ORIENT = 180 if("_M_" in CTRL[0] and "lower" in CTRL[0]) else 0;
                    py.setAttr(GRP+".raz", ORIENT); 
                    if(C == 11):#ADAM'S APPLE
                         py.move(0,0,0.725, CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                         py.move(0,0,1, CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                         py.setAttr(CTRL[0]+".tx", l=1, k=0, cb=0);
                         py.setAttr(CTRL[0].replace("CTRL", "GRP")+".s", 2,2,2);
                         py.transformLimits(CTRL[0], ty=(0, LIMIT), ety=(1, 1));
                if(C == 4 or C == 5):
                    #UP AND DOWN (EYELID)
                    FLIP = 1 if(C == 4) else -1;
                    py.move(0,0.7,0, CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                    py.move(0,-0.5,0,CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                    py.move(-0.7,-0.4,-0.5*FLIP, CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
                    py.move(0.7,-0.4,-0.5*FLIP,CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
                    ORIENT = 180 if("_R_" in CTRL[0]) else 0;
                    py.setAttr(GRP+".ray", ORIENT);  
                if(C == 8):
                    #UP AND DOWN (NOSE)
                    py.move(0,1,0.3, CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                    py.move(-0.5,-1,-1, CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
                    py.move(0,0.5,-0.2,CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                    py.move(0.5,-1,-1,CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
                    ORIENT = 180 if("_M_" in CTRL[0] and "lower" in CTRL[0]) else 0;
                    py.setAttr(GRP+".rax", ORIENT);  
                if(C > 12 and C < len(MAIN)-1):
                    #EYEBROWS
                    if("_L_" in CTRL[0]):
                        py.move(-1.4,0,0.5, CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
                        py.move(0,-0.5,0.4, CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                        py.move(1.5,-0.3,-1.5, CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
                        py.move(-2.2,-1,0.5,CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                        py.move(0,0.5,0.4,CTRL[0]+"Shape.cv[4]",r=1,os=1,wd=1);
                        py.move(1.5,0.1,-1.5, CTRL[0]+"Shape.cv[5]",r=1,os=1,wd=1);
                        py.setAttr(GRP+".ray", 0);   
                    else:
                        py.move(-1.4,0,-0.5, CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
                        py.move(0,-0.5,-0.4, CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
                        py.move(1.5,-0.3,1.5, CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
                        py.move(-2.2,-1,-0.5,CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
                        py.move(0,0.5,-0.4,CTRL[0]+"Shape.cv[4]",r=1,os=1,wd=1);
                        py.move(1.5,0.1,1.5, CTRL[0]+"Shape.cv[5]",r=1,os=1,wd=1);
                        py.setAttr(GRP+".ray", 180); 
###############################################################################
#"""# DELETE UNNECESSARY NODES                                                #
###############################################################################
            if("noseMain" in CTRL[0]):
                py.delete("c_M_manipulatorsA_v1_GRP|c_M_noseBridge_v1_GRP");
            if("L_neckMain" in CTRL[0]):
                py.delete("c_M_manipulatorsA_v1_GRP|c_L_neck_v1_GRP");
            if("M_neckMain" in CTRL[0]):
                py.delete("c_M_manipulatorsA_v1_GRP|c_M_neck_v1_GRP");
            if("R_neckMain" in CTRL[0]):
                py.delete("c_M_manipulatorsA_v1_GRP|c_R_neck_v1_GRP");
###############################################################################
#"""# CONNECT EXISTSING BLENDshapes TO THEIR CORRESPONDING CONTROLLERS        #
###############################################################################
            py.transformLimits(CTRL[0], sx=(0.5, 1.5), sy=(0.5, 1.5), sz=(0.5, 1.5), esx=(1, 1), esy=(1, 1), esz=(1, 1));C+=1;
        side = "L";C =0;num = 2;
        BSHAPE = ["a_X_mouthUp_v1_SHP", "a_X_mouthDown_v1_SHP", "a_X_mouthWide_v1_SHP", "a_X_mouthNarrow_v1_SHP",#1
                  "a_X_eyebrowUp_v1_SHP", "a_X_eyebrowDown_v1_SHP", "a_X_eyebrowWide_v1_SHP", "a_X_eyebrowNarrow_v1_SHP", "a_X_eyebrowAngry_v1_SHP", "a_X_eyebrowConcerned_v1_SHP",#2
                  "a_X_neck_v1_SHP", "a_X_eyelidSquint_v1_SHP",#3
                  "a_X_cheekIn_v1_SHP", "a_X_cheekOut_v1_SHP",#4
                  "a_M_mouthUpperUp_v1_SHP", "a_M_mouthUpperDown_v1_SHP", "a_M_mouthUpperOut_v1_SHP", "a_M_mouthUpperIn_v1_SHP", "a_M_mouthUpperFlat_v1_SHP", "a_M_mouthUpperRot_v1_SHP",#5
                  "a_M_mouthLowerDown_v1_SHP", "a_M_mouthLowerUp_v1_SHP", "a_M_mouthLowerOut_v1_SHP", "a_M_mouthLowerIn_v1_SHP", "a_M_mouthLowerFlat_v1_SHP", "a_M_mouthLowerRot_v1_SHP",#6
                  "a_M_noseUp_v1_SHP", "a_M_noseDown_v1_SHP", "a_M_cheekOut_v1_SHP", "a_M_neck_v1_SHP", "a_M_nostrilFlare_v1_SHP", "a_M_mouthOpen_v1_SHP"];#7
        ATTR = [".ty",".ty",".tx",".tx",#1   
                ".ty",".ty",".tx",".tx",".rz",".rz",#2
                ".tx",".tx",#3
                ".tx",".tx",#4
                ".ty",".ty",".tz",".tz",".sy",".rx",#5
                ".ty",".ty",".tz",".tz",".sy",".rx",#6
                ".ty",".ty",".ty",".ty",".sx",".ty"];#7
        while(C < len(BSHAPE)):#PER BLENDSHAPE
            VAL = 1 if (C % 2 == 0 or "a_M_neck_v1_SHP" in BSHAPE[C]) else -1;#1=ODD;if C is EVEN
            if(py.objExists(BSHAPE[C].replace("X", side)) == False):
                BLEND = py.duplicate(GEO, n=BSHAPE[C].replace("X", side), rr=1, rc=1)[0];
            else:
                BLEND = BSHAPE[C].replace("X", side);
            py.blendShape("a_M_face_v1_BS", e=1, t=(GEO,num,BLEND,1));
            CTRL = "c_M_upperLipMain_v1_CTRL" if(py.objExists("c_M_upperLipMain_v1_CTRL") == True and "_M_" in BLEND and "Upper" in BLEND) else "";
            CTRL = "c_M_jawMain_v1_CTRL" if(py.objExists("c_M_jawMain_v1_CTRL") == True and "_M_" in BLEND and "mouthOpen" in BLEND) else CTRL;
            CTRL = "c_M_lowerLipMain_v1_CTRL" if(py.objExists("c_M_lowerLipMain_v1_CTRL") == True and "_M_" in BLEND and "Lower" in BLEND) else CTRL;
            CTRL = "c_L_mouthCornerMain_v1_CTRL" if(py.objExists("c_L_mouthCornerMain_v1_CTRL") == True and "_L_" in BLEND and "mouth" in BLEND) else CTRL;
            CTRL = "c_R_mouthCornerMain_v1_CTRL" if(py.objExists("c_R_mouthCornerMain_v1_CTRL") == True and "_R_" in BLEND and "mouth" in BLEND) else CTRL;
            CTRL = "c_L_eyelidMain_v1_CTRL" if(py.objExists("c_L_eyelidMain_v1_CTRL") == True and "_L_" in BLEND and "eyelid" in BLEND) else CTRL;
            CTRL = "c_R_eyelidMain_v1_CTRL" if(py.objExists("c_R_eyelidMain_v1_CTRL") == True and "_R_" in BLEND and "eyelid" in BLEND) else CTRL;
            CTRL = "c_L_eyebrowMain_v1_CTRL" if(py.objExists("c_L_eyebrowMain_v1_CTRL") == True and "_L_" in BLEND and "eyebrow" in BLEND) else CTRL;
            CTRL = "c_R_eyebrowMain_v1_CTRL" if(py.objExists("c_R_eyebrowMain_v1_CTRL") == True and "_R_" in BLEND and "eyebrow" in BLEND) else CTRL;
            CTRL = "c_M_noseMain_v1_CTRL" if(py.objExists("c_M_noseMain_v1_CTRL") == True and "_M_" in BLEND and "nose" in BLEND) else CTRL;
            CTRL = "c_M_nostrilMain_v1_CTRL" if(py.objExists("c_M_nostrilMain_v1_CTRL") == True and "_M_" in BLEND and "nostril" in BLEND) else CTRL;
            CTRL = "c_L_neckMain_v1_CTRL" if(py.objExists("c_L_neckMain_v1_CTRL") == True and "_L_" in BLEND and "neck" in BLEND) else CTRL;
            CTRL = "c_M_neckMain_v1_CTRL" if(py.objExists("c_M_neckMain_v1_CTRL") == True and "_M_" in BLEND and "neck" in BLEND) else CTRL;
            CTRL = "c_R_neckMain_v1_CTRL" if(py.objExists("c_R_neckMain_v1_CTRL") == True and "_R_" in BLEND and "neck" in BLEND) else CTRL;
            MAX = 1 if(ATTR[C] != ".rz" and ATTR[C] != ".rx") else 15;#VAL = VAL*-1 if("lowerLip" in CTRL and (ATTR[C] == ".tz" or ATTR[C] == ".rx")) else VAL;
            MAX = 5 if(CTRL == "c_M_jawMain_v1_CTRL") else MAX;
            MAX = 0.5 if(ATTR[C] == ".sy") else MAX;
            if(CTRL != ""):
                BS = "a_M_face_v1_BS";
                default = py.getAttr(CTRL+ATTR[C]);
                #try:
                if(CTRL != "c_M_nostrilMain_v1_CTRL"):     
                    py.setDrivenKeyframe(BS+"."+BSHAPE[C].replace("X", side), cd=CTRL+ATTR[C]);
                    py.setAttr(CTRL+ATTR[C], VAL*MAX);py.setAttr(BS+"."+BSHAPE[C].replace("X", side), 1);
                    py.setDrivenKeyframe(BS+"."+BSHAPE[C].replace("X", side), cd=CTRL+ATTR[C]);
                    py.setAttr(CTRL+ATTR[C], default);
                else:    
                    py.setDrivenKeyframe(BS+"."+BSHAPE[C].replace("X", side), cd=nADL+".output3D.output3Dx");
                    py.setAttr(CTRL+".s", 1.5,1.5,1.5);py.setAttr(BS+"."+BSHAPE[C].replace("X", side), 1);
                    py.setDrivenKeyframe(BS+"."+BSHAPE[C].replace("X", side), cd=nADL+".output3D.output3Dx");
                    py.setAttr(CTRL+".s", 1,1,1);
                if(CTRL == "c_M_noseMain_v1_CTRL"):
                    py.setDrivenKeyframe(CTRL+".spty", CTRL+".sptz", cd=CTRL+".ty");
                    py.setAttr(CTRL+".ty", 1);py.setAttr(CTRL+".spt", 0,1,-0.5);
                    py.setDrivenKeyframe(CTRL+".spty", CTRL+".sptz", cd=CTRL+".ty");
                    py.setAttr(CTRL+".ty", -1);py.setAttr(CTRL+".spt", 0,-1,0.5);
                    py.setDrivenKeyframe(CTRL+".spty", CTRL+".sptz", cd=CTRL+".ty");
                    py.setAttr(CTRL+".ty", 0);
                #except:
                #    pass;
            C+=1;num+=1;py.setAttr(BLEND+".v", 0);BLENDS.append(BLEND);
            if(C == 14 and side == "L"):#END L/R BLENDshapes
                side = "R";C = 0;
        C = 0;py.keyTangent("a_M_face_v1_BS", itt="linear", ott="linear", e=1);
###############################################################################
#"""# CONNECT CHEEK BLENDshapes AND THEIR OVERLAPPING FUNCTIONALITY           #
###############################################################################
        if(py.objExists("a_L_cheekOut_v1_SHP") == 1 and py.objExists("a_L_cheekIn_v1_SHP") == 1 and py.objExists("a_R_cheekOut_v1_SHP") == 1 and py.objExists("a_R_cheekIn_v1_SHP") == 1 and py.objExists("a_M_cheekOut_v1_SHP") == 1):
            plug = ["R", "G", "B"];
            iCMP = py.createNode("clamp", n="c_M_cheekCap_v1_CMP");
            py.setAttr(iCMP+".min", 0, 0, 0);py.setAttr(iCMP+".max", 1, 1, 1);
            py.connectAttr("c_L_cheekMain_v1_CTRL.tx", iCMP+".inputR");
            py.connectAttr("c_R_cheekMain_v1_CTRL.tx", iCMP+".inputG");
            while(C < 2):
                S = "L" if(C == 0) else "R";S2 = "R" if(C == 0) else "G";
                F = "R" if(C == 0) else "L";F2 = "G" if(C == 0) else "R";
                py.setDrivenKeyframe(BS+"."+"a_"+S+"_cheekIn_v1_SHP", cd="c_"+S+"_cheekMain_v1_CTRL.tx");
                py.setAttr("c_"+S+"_cheekMain_v1_CTRL.tx", -1);
                py.setAttr(BS+"."+"a_"+S+"_cheekIn_v1_SHP", 1);
                py.setDrivenKeyframe(BS+"."+"a_"+S+"_cheekIn_v1_SHP", cd="c_"+S+"_cheekMain_v1_CTRL.tx");
                py.setAttr("c_"+S+"_cheekMain_v1_CTRL.tx", 0);
                PMA = py.createNode("plusMinusAverage", n="c_"+S+"_cheek_v1_PMA");
                py.setAttr(PMA+".operation", 2);
                py.connectAttr(iCMP+".output"+S2, PMA+".input2D[0].input2Dx");
                py.connectAttr(iCMP+".output"+F2, PMA+".input2D[1].input2Dx");
                if(C == 0):
                    CMP = py.createNode("clamp", n="c_M_cheek_v1_CMP");
                    py.setAttr(CMP+".min", 0, 0, 0);py.setAttr(CMP+".max", 1, 1, 1);
                    PMA2 = py.createNode("plusMinusAverage", n="c_M_cheekCap_v1_PMA");
                    py.setAttr(PMA2+".operation", 2);
                    py.connectAttr(iCMP+".outputR", PMA2+".input2D[0].input2Dx");
                    py.connectAttr(iCMP+".outputG", PMA2+".input2D[0].input2Dy");
                py.connectAttr(PMA+".output2Dx", CMP+".input"+plug[C]);
                CMP2 = py.createNode("clamp", n="c_"+S+"_cheek_v1_CMP");
                py.setAttr(CMP2+".min", 0, 0, 0);py.setAttr(CMP2+".max", 1, 1, 1);
                py.connectAttr("c_"+S+"_cheekMain_v1_CTRL.tx", CMP2+".input"+plug[C]);
                CDN = py.createNode("condition", n="c_"+S+"_cheek_v1_CDN");
                py.setAttr(CDN+".operation", 2);
                py.connectAttr(CMP2+".output"+plug[C], CDN+".firstTerm");
                py.connectAttr(CMP2+".output"+plug[C], CDN+".secondTerm");
                py.connectAttr(CMP2+".output"+plug[C], CDN+".colorIfTrueR");
                py.connectAttr(CMP+".output"+plug[C], CDN+".colorIfFalseR");
                py.connectAttr(CDN+".outColorR", BS+"."+"a_"+S+"_cheekOut_v1_SHP");
                C+=1;
            C = 0;#MIDDLE BLENDSHAPE
            py.connectAttr("c_L_cheek_v1_CDN"+".outColorR", PMA2+".input2D[1].input2Dx");
            py.connectAttr("c_R_cheek_v1_CDN"+".outColorR", PMA2+".input2D[1].input2Dy");
            PMA3 = py.createNode("plusMinusAverage", n="c_M_cheek_v1_PMA");
            py.setAttr(PMA3+".operation", 1);
            py.connectAttr(PMA2+".output2Dx", PMA3+".input2D[0].input2Dx");
            py.connectAttr(PMA2+".output2Dy", PMA3+".input2D[1].input2Dx");
            MDN = py.createNode("multiplyDivide", n="c_M_cheek_v1_MDN");
            py.connectAttr(PMA3+".output2Dx", MDN+".input1X");
            py.setAttr(MDN+".input2", 0.5, 0.5, 0.5); 
            py.connectAttr(MDN+".outputX", BS+"."+"a_M_cheekOut_v1_SHP");
###############################################################################
#"""# CREATE INDIVIDUAL EYE CONTROLLERS                                       #
###############################################################################
        if(py.objExists("b_L_eyeBall_v1_JNT") == True and py.objExists("c_L_eyeBall_v1_CTRL") == False):   
            CTRL = py.circle(ch=1, o=1, nr=(0, 0, 1), s=4, r=SCALE*10, n="c_L_eyeBall_v1_CTRL");
            GRP = py.group(n="c_L_eyeBall_v1_GRP", r=1);
            D = py.pointConstraint("b_L_eyeBall_v1_JNT", "c_L_eyeBall_v1_GRP", mo=0, w=1);
            py.delete(D);
            py.setAttr("c_L_eyeBall_v1_CTRL.overrideEnabled", 1);
            py.setAttr("c_L_eyeBall_v1_CTRL.overrideColor", 13);
            ATTR = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"];
            while(C < len(ATTR)):
                py.setAttr("c_L_eyeBall_v1_CTRL"+ATTR[C], k=0, l=1, cb=0);C+=1; 
            C = 0;
        if(py.objExists("b_R_eyeBall_v1_JNT") == True and py.objExists("c_R_eyeBall_v1_CTRL") == False):   
            CTRL = py.circle(ch=1, o=1, nr=(0, 0, 1), s=4, r=SCALE*10, n="c_R_eyeBall_v1_CTRL");
            GRP = py.group(n="c_R_eyeBall_v1_GRP", r=1);
            D = py.pointConstraint("b_R_eyeBall_v1_JNT", "c_R_eyeBall_v1_GRP", mo=0, w=1);
            py.delete(D);
            py.setAttr("c_R_eyeBall_v1_CTRL.overrideEnabled", 1);
            py.setAttr("c_R_eyeBall_v1_CTRL.overrideColor", 13);
            ATTR = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"];
            while(C < len(ATTR)):
                py.setAttr("c_R_eyeBall_v1_CTRL"+ATTR[C], k=0, l=1, cb=0);C+=1; 
            C = 0;
        eyeAssets = [];
###############################################################################
#"""# CREATE MASTER EYE CONTROLLER AND ITS BINOCULAR SHAPE                    #
###############################################################################
        if(py.objExists("b_L_eyeBall_v1_JNT") == True and py.objExists("b_R_eyeBall_v1_JNT") == True and py.objExists("c_M_eyeBalls_v1_CTRL") == False):   
            CTRL = py.circle(ch=1, o=1, nr=(0, 0, 1), s=8, r=SCALE*10, n="c_M_eyeBalls_v1_CTRL");
            GRP = py.group(n="c_M_eyeBalls_v1_GRP", r=1);
            D = py.pointConstraint("b_L_eyeBall_v1_JNT", "b_R_eyeBall_v1_JNT", GRP, mo=0, w=1);
            py.delete(D);
            py.parent("c_L_eyeBall_v1_GRP", "c_R_eyeBall_v1_GRP", CTRL[0]);
            py.setAttr(GRP+".tz", SCALE*200);
            py.setAttr("c_M_eyeBalls_v1_CTRL.overrideEnabled", 1);
            py.setAttr("c_M_eyeBalls_v1_CTRL.overrideColor", 4);
            while(C < 2):
                S = "L" if(C == 0) else "R";
                if(C == 0):
                    GRP = py.group(n="c_M_eyeBallsTracker_v1_GRP", em=1);
                    D = py.pointConstraint("b_L_eyeBall_v1_JNT", "b_R_eyeBall_v1_JNT", GRP, mo=0, w=1);
                    py.delete(D);
                    eyeAssets.append(GRP);
                TRK = py.spaceLocator(p=(0,0,0), n="c_"+S+"_eyeBallsTracker_v1_LOC")[0];
                py.parent(TRK, GRP);
                D = py.pointConstraint("b_"+S+"_eyeBall_v1_JNT", TRK, mo=0, w=1);
                py.delete(D);
                H1 = py.aimConstraint("c_"+S+"_eyeBall_v1_CTRL", TRK, n="c_"+S+"_eyeBall_v1_AIM", aim=(0,0,1), u=(0,1,0), skip="z", wut="scene", mo=0, w=1);
                py.setAttr(H1[0]+".ihi",0);
                CMP = py.createNode("clamp", n="c_"+S+"_eyeBall_v1_CMP");
                py.setAttr(CMP+".min", -50, -50, 0);
                py.setAttr(CMP+".max", 50, 70, 0);
                
                CDN = py.createNode("condition", n="c_"+S+"_eyeBallV_v1_CDN");
                py.connectAttr(TRK+".ry", CDN+".firstTerm");
                py.setAttr(CDN+".secondTerm", 180);
                py.setAttr(CDN+".operation", 2);
                py.setAttr(CDN+".colorIfTrueG", -90);
                py.connectAttr(TRK+".ry", CDN+".colorIfFalseG");
                
                py.connectAttr(TRK+".rx", CMP+".inputR");
                py.connectAttr(CDN+".outColorG", CMP+".inputG");

                py.connectAttr(CMP+".outputR", "b_"+S+"_eyeBall_v1_JNT.rx");
                py.connectAttr(CMP+".outputG", "b_"+S+"_eyeBall_v1_JNT.ry");
                C+=1;
            C = 0;
            ATTR = [".rx", ".ry", ".rz", ".sx", ".sy", ".sz", ".v"];
            while(C < len(ATTR)):
                py.setAttr("c_M_eyeBalls_v1_CTRL"+ATTR[C], k=0, l=1, cb=0);
                C+=1; 
            C = 0;
            py.move(SCALE*20,0,0, CTRL[0]+"Shape.cv[7]",r=1,os=1,wd=1);
            py.move(SCALE*-20,0,0, CTRL[0]+"Shape.cv[3]",r=1,os=1,wd=1);
            py.move(0,SCALE*-10,0, CTRL[0]+"Shape.cv[1]",r=1,os=1,wd=1);
            py.move(0,SCALE*10,0, CTRL[0]+"Shape.cv[5]",r=1,os=1,wd=1);
            py.move(SCALE*5,SCALE*10,0, CTRL[0]+"Shape.cv[0]",r=1,os=1,wd=1);
            py.move(SCALE*5,SCALE*-10,0, CTRL[0]+"Shape.cv[6]",r=1,os=1,wd=1);
            py.move(SCALE*-5,SCALE*-10,0,CTRL[0]+"Shape.cv[4]",r=1,os=1,wd=1);
            py.move(SCALE*-5,SCALE*10,0,CTRL[0]+"Shape.cv[2]",r=1,os=1,wd=1);
            py.parent(GRP, "c_M_manipulatorsC_v1_GRP");
###############################################################################
#"""# EYE LID TRACKING ATTRIBUTES                                             #
###############################################################################
        while(C < 2):
            S = "L" if(C == 0) else "R";FLIP = 1 if(C == 0) else -1;
            if(py.objExists("c_"+S+"_upperLid_v1_CTRL") == True and py.objExists("c_"+S+"_lowerLid_v1_CTRL") == True and py.objExists(headJoint) == True and py.objExists("c_M_eyeBalls_v1_CTRL") == True):
                if(C == 0):
                    py.addAttr("c_M_eyeBalls_v1_CTRL", ln="VERTICAL", at='double', min=0, max=100, dv=50);
                    py.setAttr("c_M_eyeBalls_v1_CTRL"+".VERTICAL", e=1, k=0, cb=1);
                    py.addAttr("c_M_eyeBalls_v1_CTRL", ln="HORIZONTAL", at='double', min=0, max=100, dv=25);
                    py.setAttr("c_M_eyeBalls_v1_CTRL"+".HORIZONTAL", e=1, k=0, cb=1);
                MULT = py.createNode("multiplyDivide", n="c_"+S+"_lidTracker_v1_MDN");
                py.connectAttr("c_M_eyeBalls_v1_CTRL.VERTICAL", MULT+".input1X");
                py.connectAttr("c_M_eyeBalls_v1_CTRL.HORIZONTAL", MULT+".input1Y");
                py.setAttr(MULT+".input2", 0.01, 0.01, 0);   
                py.select(d=1);
                if(py.objExists("b_"+S+"_upperLid_v1_JNT") == False and py.objExists("b_"+S+"_lowerLid_v1_JNT") == False):
                    UP = py.joint(p=(0,0,0), radius=0, n="b_"+S+"_upperLid_v1_JNT");
                    py.select(d=1);
                    DOWN = py.joint(p=(0,0,0), radius=0, n="b_"+S+"_lowerLid_v1_JNT");
                    D = py.pointConstraint("b_"+S+"_eyeBall_v1_JNT","b_"+S+"_upperLid_v1_JNT",mo=0,w=1);
                    py.delete(D);
                    D = py.pointConstraint("b_"+S+"_eyeBall_v1_JNT","b_"+S+"_lowerLid_v1_JNT",mo=0,w=1);
                    py.delete(D);
                    py.parent(UP, DOWN, headJoint);
                else:
                    UP = "b_"+S+"_upperLid_v1_JNT";
                    DOWN = "b_"+S+"_lowerLid_v1_JNT";
###############################################################################
#"""# CREATE EYE FUNCTIONALITY                                                #
###############################################################################
                DDN = py.distanceDimension(sp = (0, 100, 0), ep = (0, 10, 0));
                DDN2 = py.pickWalk(d="up");py.select("locator1","locator2", r=1);
                DISTANCE = py.ls(sl=1);
                D = py.pointConstraint("b_"+S+"_eyeBall_v1_JNT", DISTANCE[1], mo=0, w=1);
                py.delete(D);
                D = py.pointConstraint("c_"+S+"_lowerLid_v1_CTRL", DISTANCE[0], mo=0, w=1);
                py.delete(D);
                DIST = py.getAttr(DDN+".distance");
                CTRL = py.circle(ch=1, o=1, nr=(1, 0, 0), s=8, r=DIST, n="c_"+S+"_eyeBall_v1_CRV");
                SUB = py.group(n="c_"+S+"_eyeBallSub_v1_GRP", r=1);
                GRP = py.group(n="c_"+S+"_eyeBall_v1_GRP", r=1);
                eyeAssets.append(GRP);
                D = py.pointConstraint("b_"+S+"_eyeBall_v1_JNT", GRP, mo=0, w=1);
                py.delete(D);
                D = py.aimConstraint("c_"+S+"_lowerLid_v1_CTRL", SUB, aim=(0,1,0), u=(0,1,0), wut="scene", mo=0, w=1);
                py.delete(D); 
                uLOC = py.spaceLocator(p=(0,0,0), n="c_"+S+"_upperLidTracker_v1_LOC");
                eyeAssets.append(uLOC[0]);
                dLOC = py.spaceLocator(p=(0,0,0), n="c_"+S+"_lowerLidTracker_v1_LOC");
                eyeAssets.append(dLOC[0]);   
                py.cycleCheck(e=0);
                PATH1 = py.pathAnimation(dLOC[0], CTRL, fm=1, followAxis="x", upAxis="y");
                py.setAttr(PATH1+".u", 0);  
                PATH2 = py.pathAnimation(uLOC[0], CTRL, fm=1, followAxis="x", upAxis="y");
                py.setAttr(PATH2+".u", 1);  
                D = py.pointConstraint("c_"+S+"_upperLid_v1_CTRL", DISTANCE[0], mo=0, w=1);
                py.delete(D);   
                D = py.pointConstraint("c_"+S+"_upperLidTracker_v1_LOC", DISTANCE[1], mo=0, w=1);
                #py.delete(D);
                while(round(py.getAttr(DDN+".distance"), 2) > 0.1):
                    py.setAttr(PATH2+".u", (py.getAttr(PATH2+".u")-0.005) );  
                py.cutKey(PATH1, PATH2, s=1);#py.cycleCheck(e=1);
                LIDROLL = py.createNode("multiplyDivide", n="c_"+S+"_lowerLid_v1_MDN");
                py.connectAttr("b_"+S+"_eyeBall_v1_JNT.rx", LIDROLL+".input1X");
                py.connectAttr("b_"+S+"_eyeBall_v1_JNT.ry", LIDROLL+".input1Y");
                py.connectAttr(MULT+".outputX", LIDROLL+".input2X");
                py.connectAttr(MULT+".outputY", LIDROLL+".input2Y");
                py.connectAttr(LIDROLL+".outputX", GRP+".rx");
                py.connectAttr(LIDROLL+".outputY", GRP+".ry");
                D1 = py.aimConstraint("c_"+S+"_upperLidTracker_v1_LOC", "b_"+S+"_upperLid_v1_JNT", aim=(0,0,1), u=(0,1,0), wut="scene", mo=0, w=1);
                py.delete(D1);
                D2 = py.aimConstraint("c_"+S+"_lowerLidTracker_v1_LOC", "b_"+S+"_lowerLid_v1_JNT", aim=(0,0,1), u=(0,1,0), wut="scene", mo=0, w=1);
                py.delete(D2); 
                try:
                    py.makeIdentity(UP,DOWN, apply=1, r=1, n=0);#FREEZE 
                except:
                    pass;
                H1 = py.aimConstraint(uLOC[0], UP, n="b_"+S+"_upperLid_v1_AIM", aim=(0,0,1), u=(0,1,0), wut="scene", skip="z", mo=0, w=1);
                py.setAttr(H1[0]+".ihi",0); 
                H1 = py.aimConstraint(dLOC[0], DOWN, n="b_"+S+"_lowerLid_v1_AIM", aim=(0,0,1), u=(0,1,0), wut="scene", skip="z", mo=0, w=1);
                py.setAttr(H1[0]+".ihi",0);  
                if(py.objExists("c_"+S+"_upperLid_v1_CTRL") == True):
                    py.setDrivenKeyframe(PATH1+".u", cd="c_"+S+"_eyelidMain_v1_CTRL.ty");
                    py.setDrivenKeyframe(PATH2+".u", cd="c_"+S+"_eyelidMain_v1_CTRL.ty");
                    py.setAttr("c_"+S+"_eyelidMain_v1_CTRL.ty", -1);
                    py.setAttr(PATH2+".u", 1);  
                    py.setDrivenKeyframe(PATH1+".u", cd="c_"+S+"_eyelidMain_v1_CTRL.ty");
                    py.setDrivenKeyframe(PATH2+".u", cd="c_"+S+"_eyelidMain_v1_CTRL.ty");
                    py.setAttr("c_"+S+"_eyelidMain_v1_CTRL.ty", 1);
                    py.setAttr(PATH1+".u", (py.getAttr(PATH1+".u")+0.05));
                    py.setAttr(PATH2+".u", (py.getAttr(PATH2+".u")-0.05));  
                    py.setDrivenKeyframe(PATH1+".u", cd="c_"+S+"_eyelidMain_v1_CTRL.ty");
                    py.setDrivenKeyframe(PATH2+".u", cd="c_"+S+"_eyelidMain_v1_CTRL.ty");
                    py.setAttr("c_"+S+"_eyelidMain_v1_CTRL.ty", 0);
                    py.keyTangent(PATH1, PATH2, itt="linear", ott="linear", e=1);
                py.delete(D, "c_M_manipulatorsA_v1_GRP|c_"+S+"_upperLid_v1_GRP", "c_M_manipulatorsA_v1_GRP|c_"+S+"_lowerLid_v1_GRP");
                if(C == 0):
                    py.delete(DISTANCE[0], DISTANCE[1], DDN, DDN2);
            C+=1;
        C = 0;   
        GRP = py.group(n="c_M_eyeTracker_v1_GRP", em=1);
        py.group(n="c_M_blendshapes_v1_GRP", em=1);
        py.parent(eyeAssets[:], "c_M_eyeTracker_v1_GRP");
        py.parent("a_M_faceCreator_v1_SHP", "a_M_faceManipulators_v1_SHP", BLENDS[:], "c_M_blendshapes_v1_GRP");
        py.parent("c_M_eyeTracker_v1_GRP", "c_M_blendshapes_v1_GRP", "c_M_face_v1_GRP");
        py.setAttr("c_M_eyeTracker_v1_GRP.v", 0);
###############################################################################
#"""# TONGUE RIG                                                              #
###############################################################################
        if(py.objExists("b_M_tongueStart_v1_JNT") == True and py.objExists("b_M_tongueEnd_v1_JNT") == True):
            D = py.pointConstraint("b_M_tongueStart_v1_JNT", DISTANCE[1], mo=0, w=1);
            py.delete(D);
            D = py.pointConstraint("b_M_tongueEnd_v1_JNT", DISTANCE[0], mo=0, w=1);
            py.delete(D);
            DIST = py.getAttr(DDN+".distance");
            CTRL = py.circle(ch=1, o=1, nr=(1, 0, 0), s=8, r=DIST/3, n="c_M_tongue_v1_CTRL");
            subGRP = py.group(n="c_M_tongue_v1_GRP", r=1);
            GRP = py.group(n="c_M_tongueMain_v1_GRP", r=1);
            D = py.parentConstraint("b_M_tongueEnd_v1_JNT", GRP, mo=0, w=1);
            py.delete(D);
            py.setAttr(subGRP+".tx", DIST*1.25);
            H1 = py.aimConstraint(CTRL[0], "b_M_tongueStart_v1_JNT", n="b_M_tongueStart_v1_AIM", aim=(1,0,0), u=(0,1,0), wut="scene", mo=1, w=1);
            py.setAttr(H1[0]+".ihi",0);    
            py.delete(DISTANCE[0], DISTANCE[1], DDN, DDN2);
            py.parent(GRP, "c_M_jawMain_v1_CTRL");
            H1 = py.parentConstraint("b_M_jaw_v1_JNT", GRP, n=GRP.replace("GRP", "CON"), mo=1, w=1);
            py.setAttr(H1[0]+".ihi",0);   

            MDN = py.createNode("multiplyDivide", n="c_M_tongue_v1_MDN");
            py.connectAttr(CTRL[0]+".tx", MDN+".input1X");
            py.setAttr(MDN+".input2", 0.5, 0.5, 0.5);
            
            ADL = py.createNode("addDoubleLinear", n="c_M_tongueMid_v1_ADL");
            py.setAttr(ADL+".input1", py.getAttr("b_M_tongueMid_v1_JNT.tx"));
            py.connectAttr(MDN+".outputX", ADL+".input2");
            py.connectAttr(ADL+".output", "b_M_tongueMid_v1_JNT.tx");
            
            ADL = py.createNode("addDoubleLinear", n="c_M_tongueEnd_v1_ADL");
            py.setAttr(ADL+".input1", py.getAttr("b_M_tongueEnd_v1_JNT.tx"));
            py.connectAttr(MDN+".outputX", ADL+".input2");
            py.connectAttr(ADL+".output", "b_M_tongueEnd_v1_JNT.tx");
            
            MDN = py.createNode("multiplyDivide", n="c_M_tongueMid_v1_MDN");
            py.connectAttr(CTRL[0]+".r", MDN+".input1");
            py.setAttr(MDN+".input2", 0.1, 0.5, 0.5);
            py.connectAttr(MDN+".output", "b_M_tongueMid_v1_JNT.r");
            py.connectAttr(CTRL[0]+".r", "b_M_tongueEnd_v1_JNT.r");
            
            jaw = "c_M_jawMain_v1_CTRL";
            py.addAttr(jaw, ln="TONGUE", at="enum", en="OFF:ON:", dv=1);
            py.setAttr(jaw+".TONGUE", k=1, e=1);
            py.connectAttr(jaw+".TONGUE", CTRL[0]+".v");
            py.setAttr("c_M_tongue_v1_CTRL.v", k=0, cb=0);

            mel.eval("select -r -sym c_M_tongue_v1_CTRL.cv[3] c_M_tongue_v1_CTRL.cv[7];");
            mel.eval("select -tgl -sym c_M_tongue_v1_CTRL.cv[1] ;");
            mel.eval("select -tgl -sym c_M_tongue_v1_CTRL.cv[5] ;");
            mel.eval("scale -r -smn -p 0cm 159.036439cm 11.988379cm -1.13332 -1.13332 -1.13332 ;");
            mel.eval("scale -r -smn -p 0cm 159.036439cm 11.988379cm 0.883365 0.883365 0.883365 ;");
###############################################################################
#"""# COPY SKIN WEIGHTS                                                       #
###############################################################################
        if(py.objExists(headJoint) == True):
            #py.parentConstraint(headJoint, GRP, n=GRP.replace("GRP", "CON"), mo=1, w=1);
            py.parentConstraint(headJoint, cGRP, n=cGRP.replace("GRP", "CON"), mo=1, w=1);
        try:
            if(py.objExists("b_M_origin_v1_JNT") == True):
                ROOT = "b_M_origin_v1_JNT";
            else:
                ROOT = "b_root";
            bindPose = py.dagPose(ROOT, bp=1, q=1);
            py.delete(bindPose);
            py.dagPose(ROOT, bp=1, save=1, n="b_M_bindPose_v1_BIND");
            py.skinCluster(ROOT, GEO, mi=3, nw=1, bm=0, sm=0, dr=4.0, n="b_M_face_v1_SKIN");
            py.copySkinWeights(original, GEO, noMirror=1, surfaceAssociation="closestPoint", influenceAssociation="closestJoint", normalize=1);
            py.skinCluster(BINDERS[:], MASTERBLEND, mi=3, nw=1, bm=0, sm=0, dr=4.0, n="c_M_face_v1_SKIN");
            py.copySkinWeights(original, MASTERBLEND, noMirror=1, surfaceAssociation="closestPoint", influenceAssociation="closestJoint", normalize=1);
            py.delete(original);
        except:
            pass;
        py.headsUpMessage('"Facial Setup successfully created!" - HiGGiE', t=2);
        py.select(d=1);
###############################################################################
#"""# MIRROR BLENDshapes                                                      #
###############################################################################
def MIRROR(BASE):
    BLENDSHAPE = py.ls(sl=1);C = 0;
    if(py.objExists(BASE) == True and isinstance(BLENDSHAPE, list) == True):
        while(C < len(BLENDSHAPE)):
            MAIN = BASE;
            SCALE = py.duplicate(MAIN, rr=1, rc=1)[0];
            WRAP = py.duplicate(MAIN, rr=1, rc=1)[0];
            py.setAttr(SCALE+".sx", l=0);py.setAttr(SCALE+".sx", -1);
            BS = py.blendShape(BLENDSHAPE[C], SCALE)[0];
            py.select(WRAP, SCALE, r=1);
            py.CreateWrap();
            py.setAttr(BS+"."+BLENDSHAPE[C], 1);
            if("R_" in BLENDSHAPE[C] or "r_" in BLENDSHAPE[C]):
                MIRROR = py.duplicate(WRAP, n=BLENDSHAPE[C].replace("R_", "L_").replace("r_", "L_"), rr=1, rc=1)[0];
            elif("L_" in BLENDSHAPE[C] or "l_" in BLENDSHAPE[C]):
                MIRROR = py.duplicate(WRAP, n=BLENDSHAPE[C].replace("L_", "R_").replace("l_", "R_"), rr=1, rc=1)[0];
            else:
                MIRROR = py.duplicate(WRAP, n=BLENDSHAPE[C], rr=1, rc=1)[0];
            VAL = py.getAttr(BLENDSHAPE[C]+".tx");py.setAttr(MIRROR+".tx", l=0);
            py.setAttr(MIRROR+".tx", VAL*-1);py.delete(SCALE, WRAP);
            C+=1;
        py.headsUpMessage('"Blendshape(s) successfully mirrored!" - HiGGiE', t=2);
    else:
        py.headsUpMessage('"Please select atleast one blendshape to mirror and check your base head name." - HiGGiE', t=5);
###############################################################################
#"""# PROMPT UI                                                               #
###############################################################################
TYPE = py.promptDialog(
        title='FACE RIG CREATOR v1.0',
        message="WHAT IS THE NAME OF THE BASE HEAD?",
        text="a_M_face_v1_GEO",
        button=['CREATE FACE', 'MIRROR BLENDSHAPE', 'CANCEL'],
        defaultButton='OK',
        cancelButton='CANCEL',
        dismissString='CANCEL'); 
BASE = py.promptDialog(query=1, text=1);
if(TYPE == "CREATE FACE"):
    FACE(BASE);
if(TYPE == "MIRROR BLENDSHAPE"):
    MIRROR(BASE);
    

    
#selectKey -add -k -f -0.5 -f 0 a_M_face_v1_BS_a_M_mouthLowerRight_v1_SHP ;
#keyTangent -itt linear -ott linear;
#py.createNode("clamp");