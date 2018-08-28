import maya.cmds as cmds
import pymel.core as pm

def recreateJoints():
    if not cmds.objExists("loc_Grp_1"):
        print "You must generate a skeleton first!"
    else:
        
        
        locList=[]
        cmds.duplicate("loc_Grp_1",rc=True)
        locsDup=[]
        cmds.group(n="loc_Grp_dup",em=True)
        
        for pc in cmds.listRelatives("loc_Grp_2",ad=True):
            if "parentConstraint2" in pc:
                cmds.delete(pc)
            else:
                print "didnt find pc"
                if "Shape" in pc:
                    print "this is shape"
                else:
                    locsDup.append(pc)
                    cmds.parent(pc,"loc_Grp_dup")
        for loc in cmds.listRelatives("loc_Grp_dup"):
            cmds.select(loc)
            for item in pm.selected():
                if "tail" in loc:
                    print "skippy"
                elif "4"in item:
                    item.rename(item.name().replace('4', '11'))
                elif "5" in loc:
                    item.rename(item.name().replace('5', '21'))
                elif "6" in loc:
                    item.rename(item.name().replace('6', '31'))
                else:
                    print "nope"
                '''
                if item == "loc_spine11":
                    item.rename(item.name().replace('11','21'))
                    
                if item == "loc_spine3":
                    item.rename(item.name().replace('spine3','spine11'))
                '''

        cmds.delete("loc_Grp_2")
        cmds.group(n="new_dup_Grp",em=True)
        for i in cmds.listRelatives("loc_Grp_dup"):
            #aimLocs = cmds.listRelatives(i,p=1)
            #aimLocsPar = cmds.listRelatives(i,p=1)
            if "L_" in i:
                print i
                new_dup = cmds.duplicate(i,n= i + "moved")
                cmds.parent(new_dup,'new_dup_Grp')
                cmds.xform(os=True,r=True, t=(0,1,0))
        
        for obj in cmds.listRelatives("loc_Grp_1",ad=True,type="locator"):
            #print obj
            locs=cmds.listRelatives(obj,p=1)
            locsPar = cmds.listRelatives(locs,p=True)
            #print locs[0] + " is the child"
            #print locsPar[0] + " is the parent"
            if locs[0] == "loc_root_joint":
                locList.append(locs[0])
            elif locs[0] == "loc_Grp_1":
                print locs[0]
            elif locsPar[0] == "loc_Grp_1":
                print locsPar[0]
            else:
                if "11" in locs[0] or "11" in locsPar[0]:
                    print "no par"
                elif not cmds.objExists(locs[0] + "1") or not cmds.objExists(locsPar[0] + "1"):
                    print "no exists"
                else:
                    if "L_" not in locs[0] or "L_" not in locsPar[0]:
                        print "THIS IS THE FLAG YOURE LOOKING FOR       :         " + locs[0] + " ----->" + locsPar[0]
                        #aimToDel = cmds.aimConstraint(locs[0] + "1",locsPar[0] + "1",wuo=locs[0] + "1" + "moved")
                        #cmds.delete(aimToDel)
                        cmds.parent(locs[0] + "1",locsPar[0] + "1")
                        locList.append(locs[0])
                    elif "hand" in locsPar[0]:
                        print "THIS IS THE HAND : " + locsPar[0]
                        cmds.parent(locs[0] + "1",locsPar[0] + "1")
                        locList.append(locs[0])
                    else:
                        print "THIS IS THE FLAG SAYING NOT L        :      " + locs[0] + "=====>" + locsPar[0]
                        aimToDel = cmds.aimConstraint(locs[0] + "1",locsPar[0] + "1",wuo=locsPar[0] + "1" + "moved",u=(0,1,0),aim=(1,0,0),wut="object")
                        cmds.delete(aimToDel)
                        cmds.parent(locs[0] + "1",locsPar[0] + "1")
                        locList.append(locs[0])
        cmds.delete('new_dup_Grp')
        jointGroup = []
        newLocList = []
        newJointList = []
        counterJoint = 1
        newJointGroup = cmds.group(n="joint_group", em=True)
        '''
        for locator in locList:
            print locator
            if "_R_" in locator:
                print "bad loc"
            else:
                if locator not in newLocList:
                    print locator
                    newLocList.append(locator)
                else:
                    print " its in list"
        '''
        posture = ''
        for fix in cmds.listRelatives("loc_Grp_dup",ad=True,type="locator"):
            fixNew=cmds.listRelatives(fix,p=True)
            newLocList.append(fixNew)

        if "hock" in str(newLocList):
            posture = "quadruped"
        elif "hock" not in str(newLocList):
            print "asd"
            posture = "biped"
            
        print locList
        print newLocList
        for l in newLocList:
            print "JUST STARTESDFSJDGSDFJG"
            print l
            
            cmds.select(cl=True)
            locPos = []
            locRot = []
            locPos.append(cmds.xform(l,q=True,ws=True,t=True))
            locRot.append(cmds.xform(l,q=True,ws=True,ro=True))
            newJoint = cmds.joint(n="joint_" + l[0], p = locPos[0],o=locRot[0])
            jointGroup.append(newJoint)
            print "just made " + newJoint
            newJointList.append(newJoint)
            cmds.parent(newJoint,newJointGroup)
            print "just parented " + newJoint + " to : " + newJointGroup
        for jtl in newLocList:
            getJointParent = cmds.listRelatives(jtl,p=True)
            print getJointParent[0] + " THIS IS THE PARENT"
            print jtl[0] + " THIS IS THE CHILD"
            if not getJointParent:
                print "no parent"
            else:
                properJointParent = "joint_" + getJointParent[-1]
                properJointChild = newJointList[counterJoint]
                
                if "joint_loc_Grp_dup" in properJointParent or "joint_loc_Grp_dup" in properJointChild:
                    print "top of chain"
                else:
                    print "it dont work"
                    print properJointChild + "      ch"
                    print properJointParent + "     par"
                    cmds.parent(properJointChild,properJointParent,a=True)
                    counterJoint += 1
        print posture
        if posture == "biped":
            shoulderNames = ["clav"]
        else:         
            shoulderNames = ["clav","shoulder"]
            
        thighNames = ["thigh","hip"]
        for jx in newLocList:
            print jx[0]
            jxPar = cmds.listRelatives(jx[0],p=True)
            if ("_L_" in jx[0] or "L_" in jx[0]) and ("_L_" not in jxPar or "L_" not in jxPar):
                for name in shoulderNames:
                    if name in jx[0]:
                        clav_mirror = cmds.select("joint_" + jx[0])
                        sel = cmds.ls(sl=True)
                        cmds.mirrorJoint(clav_mirror,mb=True, myz=True, sr = ("L_","R_"))
                for oName in thighNames:
                    if oName in jx[0]:
                        thigh_mirror = cmds.select("joint_" + jx[0])
                        sel = cmds.ls(sl=True)
                        cmds.mirrorJoint(thigh_mirror,mb=True, myz=True, sr = ("L_","R_"))
                else:
                    print "not right"
            
        #cmds.mirrorJoint(clav_mirror,mb=True, myz=True, sr = ("L_","R_"))
        #thigh_mirror = cmds.select("joint_loc_L_thigh_joint1")
        #cmds.mirrorJoint(thigh_mirror,mb=True, myz=True, sr = ("L_","R_"))
        
        cmds.delete("loc_Grp_1")
        cmds.delete("obj_group_1")
        cmds.delete("loc_Grp_dup")
    cmds.select('joint_loc_root_joint1')
    print "THIS IS THE NEW SCRIPT!!!!!!!"
