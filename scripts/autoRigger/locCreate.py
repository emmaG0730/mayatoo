import maya.cmds as cmds
def createLoc(type):
    print type
    if cmds.objExists("loc_Grp_1"):
        print "it exists already"
    else:
        if type == "first":
            filePath = "R:/Jx4/tools/dcc/maya/scripts/autoRigger/importFiles/biped/"
        elif type == "third":
            filePath = "R:/Jx4/tools/dcc/maya/scripts/autoRigger/importFiles/quadruped/"
        fileType = "ma"
        fileObj = "obj"
        masterObj = ''
        files = cmds.getFileList(folder=filePath, filespec='*.%s' % fileType)
        filesObj = cmds.getFileList(folder=filePath, filespec='*.%s' % fileObj)
        print files
        if len(files) == 0:
            cmds.warning("no files found")
        else:
            for f in files:
                masterObj = cmds.file(filePath + f, i=True)
        
        
        allJoints = []
        jointList = []
        locList = []
        objList = []
        allJoints = cmds.listRelatives('root_joint',ad=True)
        allJoints.append('root_joint')
        print allJoints
        cmds.select('root_joint')
    
        
        
        cmds.select( cmds.listRelatives( type='joint', fullPath=True, allDescendents=True ), add=True )
        cmds.select( cmds.listRelatives( parent=True, fullPath=True ), add=True )
        sel = cmds.ls ( selection = True, type = 'joint' )
        if not sel :
            cmds.warning( "Please select a joint / No joints in selection " )
            return
    
        locGrp = cmds.group(n="loc_Grp_#", em=True)
        cmds.addAttr ( locGrp, attributeType='double' , longName='locScale' , defaultValue=1.0 , keyable=1 )
        masterLoc = cmds.spaceLocator(n="loc_0")[0]
        cmds.parent( masterLoc, locGrp )
        print " u are here"
        for attr in ["scaleZ", "scaleY", "scaleX"]:
            cmds.connectAttr ( locGrp + ".locScale" , "%s.%s" % ( masterLoc, attr ) )
    
        is_root_loop = True
        loc_to_rename = masterLoc
        
        for jnt in sel:
            #print jnt 
            jointList.append(jnt)
            coordsT = cmds.xform ( jnt, query=True, worldSpace=True, t=True )
            coordsR = cmds.xform ( jnt, query=True, worldSpace=True, ro=True)
            cmds.select( masterLoc, replace=True )        
    
            if not is_root_loop:
                loc_to_rename = cmds.duplicate( returnRootsOnly=True , inputConnections=True )[0]
    
            # No more errors!
            renamed_loc = cmds.rename(str(loc_to_rename), ("loc_" + str(jnt)))
            locList.append(renamed_loc)
            #renamed_locs = renamed_loc.split("loc_",1)[1]
            #_parent = cmds.listRelatives(jnt,p=True)
            #proper_parent = "loc_" + _parent[-1]
            if is_root_loop:
                masterLoc = renamed_loc
    
            cmds.xform(t=coordsT )
            cmds.xform(ro=coordsR)
            
            #cmds.parent(renamed_loc,proper_parent)
            is_root_loop = False 
        counter = 0
        for joints in jointList:
            getParent = cmds.listRelatives(joints,p=True)
            if not getParent:
                print "no parent"
            else:
                properParent = "loc_" + getParent[-1]
                print properParent
                properChild =  locList[counter]
                print properChild
                print counter
                cmds.parent(properChild,properParent,a=True)
                counter += 1
        count = 0
        for o in filesObj:
            newFile = cmds.file(filePath + o, i=True)
            grabFile = 'joint_visualizer_joint_visualizer'
            
        
        objGroup = cmds.group(n='obj_group_#',em=True)
        deleteList = []
        for i in locList:
            dupFile = cmds.duplicate(grabFile)
            cmds.parent(dupFile,objGroup)
            renameFile = cmds.rename(dupFile,'obj_' + str(i))
            count +=1
            print renameFile
            objList.append(renameFile)
            print i
            cmds.parentConstraint(i,renameFile,mo=False)
            const = cmds.listRelatives(renameFile,c=True, type = 'constraint')
            cmds.delete(const)
            cmds.parentConstraint(renameFile,i)
            
        counterObj=0
        for joints in jointList:
            getObjParent = cmds.listRelatives(joints,p=True)
            if not getObjParent:
                print "no parent"
            else:
                properObjParent = "obj_loc_" + getObjParent[-1]
                print properObjParent
                properObjChild =  objList[counterObj]
                print properObjChild
                print counterObj
                cmds.parent(properObjChild,properObjParent,a=True)
                counterObj += 1
        objGroupList = cmds.listRelatives("obj_group_1",ad=True)
        for obj in objGroupList:
            print obj
            if "end" in obj:
                deleteList.append(obj)
                print "goodbye"
            elif "R_" in obj:
                deleteList.append(obj)
            else:
                print "you get to live to see another day"
        for locator in locList:
            print locator
            if "R_" in locator:
                deleteList.append(locator)
        for item in deleteList:
            #print item
            cmds.delete(item)
        cmds.delete('joint_visualizer_joint_visualizer')
        for j in jointList:
            cmds.delete(j)
            

