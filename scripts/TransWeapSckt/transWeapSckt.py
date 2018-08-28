import maya.cmds as cmds
import maya.mel as mel
import csv

class transWeapSock():

    def __init__(self, filemap):
        self.jntNames = {'b_M_weaponWaist_v1_JNT': 'Bone_Swrod_Waist',
                         'b_M_weaponBack_v1_JNT': 'Bone_Swrod_Back',
                         'b_L_weapon_v1_JNT': 'Bone_LeftWeapon',
                         'b_R_weapon_v1_JNT': 'Bone_RightWeapon'
                         }

        self.attachParent = {'b_M_weaponWaist_v1_JNT': 'b_M_spine1_v1_JNT',
                             'b_M_weaponBack_v1_JNT': 'b_M_spine3_v1_JNT',
                             'b_L_weapon_v1_JNT': 'b_L_wrist_v1_JNT',
                             'b_R_weapon_v1_JNT': 'b_R_wrist_v1_JNT'
                             }

        self.contParent = {'c_M_weaponWaist_v1_GRP': 'c_M_spine1_v1_CTRL',
                           'c_M_weaponBack_v1_GRP': 'c_M_spine3_v1_CTRL',
                           'c_L_weapon_v1_GRP': 'c_L_wrist_v1_CTRL',
                           'c_R_weapon_v1_GRP': 'c_R_wrist_v1_CTRL'}

        self.socketData = {'s_M_waistSheath_v1_SKT': 'S_Shell_Waist',
                           's_M_waistWeapon_v1_SKT': 'S_Sword_Waist',
                           's_M_backSheath_v1_SKT': 'S_Shell_Back',
                           's_M_backWeapon_v1_SKT': 'S_Sword_Back',
                           's_L_weapon_v1_SKT': 'S_Bone_LeftWeapon',
                           's_R_weapon_v1_SKT': 'S_Bone_RightWeapon'
                           }

        self.socketParent = {'s_M_waistSheath_v1_SKT': 'b_M_weaponWaist_v1_JNT',
                             's_M_waistWeapon_v1_SKT': 'b_M_weaponWaist_v1_JNT',
                             's_M_backSheath_v1_SKT': 'b_M_weaponBack_v1_JNT',
                             's_M_backWeapon_v1_SKT': 'b_M_weaponBack_v1_JNT',
                             's_L_weapon_v1_SKT': 'b_L_weapon_v1_JNT',
                             's_R_weapon_v1_SKT': 'b_R_weapon_v1_JNT'}

        self.filemap = filemap
        self.fileData = self.readFile(self.filemap + '/filemap.csv')

    # Joint Naming Convention - b_side_unique_v1_JNT
    def createJointCont(self, jntName, matName):
        cntName = jntName.replace('b_', 'c_')
        cntName = cntName.replace('JNT', 'CTRL')
        cntNullName = cntName.replace('CTRL', 'GRP')

        # creating parts - joint, controller, and null
        cmds.select(deselect=True)
        attachJnt = cmds.joint(p=(0, 0, 0), name=jntName)
        cmds.joint(attachJnt, edit=True, orientJoint='xyz', secondaryAxisOrient='zup', ch=1, zso=1)
        attachCont = cmds.polyCube(w=10, h=10, d=10, sx=1, sy=1, sz=1, ax=(0, 1, 0), cuv=4, ch=1, name=cntName)
        cmds.makeIdentity(attachCont[0])
        cmds.hyperShade(assign=matName)
        attachNull = cmds.group(attachCont[0], name=cntNullName)

        # attaches joint to controller
        attachPrntConst = cmds.parentConstraint(attachCont[0], attachJnt, maintainOffset=False)

        return attachCont[0], attachNull, attachPrntConst

    # Attaches the old rig to the new rig
    def attachOldToNewJnt(self,oldJoint, newJoint):
        pntConst = cmds.pointConstraint(newJoint, oldJoint, maintainOffset=False)
        orientConst = cmds.orientConstraint(newJoint, oldJoint, maintainOffset=True)

        return pntConst, orientConst

    # Reads csv file and returns data
    def readFile(self, filepath):
        fileData = {}
        with open (filepath, 'rb') as csvfile:
            linereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in linereader:
                data = row[0].split(',')
                fileData [data[0]] = data[1]
        return fileData

    # Opens the maya file and imports the old rig file
    def openAndImportFile(self, fileName, fbxFile, namespace):
        cmds.file(fileName, force=True, open=True, prompt=False)
        self.fbxFileContents = cmds.file(fbxFile, i=True, type="FBX", ignoreVersion=True, ra=True, prompt=False,
                                          mergeNamespacesOnClash=False, namespace=namespace, options="mo-0", pr=True)

    # Gets the tagging data for the skeleton
    def matchSkeleton(self):
        rigTags = self.readFile('W:/JX4/Animation/MaleAdult/AnimationSource/Rigs/rigTag.csv')
        for i in rigTags:
            self.attachOldToNewJnt(i, rigTags[i])

    # Attaches controller to main rig
    def attachControllers(self):
        for i in self.jntNames:
            attachCont, attachNull, attachPrntConst = self.createJointCont(i, 'T_MAT')
            cmds.parent(i, self.attachParent[i])
            PC = cmds.parentConstraint(self.jntNames[i], attachNull, mo=False)

            cmds.delete(PC)

            cmds.parent(attachNull, self.contParent[attachNull])

    # Creates the sockets and attaches them to the proper parent joint
    def createSocket(self):
        for i in self.socketData:
            socket = cmds.spaceLocator(p=(0, 0, 0), name=i)
            cmds.parent(i, self.socketParent[i])
            PC = cmds.parentConstraint(self.socketData[i], socket)
            cmds.delete(PC)

    # Cleans up the imported files
    def cleanup(self):
        objectList = ['Character', 'xyl_002_body', 'xyl_002_gloves', 'xyl_002_cheat']
        for i in objectList:
            cmds.delete(i)
            mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
            self.deleteEmptyLayers()

    # Finds all empty layers and deletes them
    def deleteEmptyLayers(self):
        dispLayers = cmds.ls(type='displayLayer')

        for i in dispLayers:
            layerItems = cmds.editDisplayLayerMembers(i, query=True)
            if layerItems == None:
                cmds.delete(i)
            else:
                print layerItems

    def main(self):
        self.openAndImportFile('W:/JX4/Animation/MaleAdult/AnimationSource/Rigs/RIG_MA_NEW.ma',
                            'W:/JX4/Animation/MaleAdult/AnimationSource/Rigs/refRig.FBX',
                            'refRig')

        self.matchSkeleton()
        self.attachControllers()
        self.createSocket()
        self.cleanup()

transWeap = transWeapSock('W:/JX4/Animation/MaleAdult/AnimationSource/Movement')
transWeap.main()