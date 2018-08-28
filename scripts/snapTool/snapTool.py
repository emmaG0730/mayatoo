import shiboken
import maya.OpenMayaUI as mui
from PySide import QtCore as qtc
from PySide import QtGui as qt
import maya.cmds as cmds




def snapFunc():
    
    selection = cmds.ls(sl=True)
    
    if len(selection) > 0:
        object1 = selection[0]
        object2 = selection[1]
        obj1_trans = cmds.xform(object1,q=1,ws=1,t=True)
        obj2_trans = cmds.xform(object2,q=1,ws=1,t=True)
        obj1_rot = cmds.xform(object1,q=1,ws=1,ro=True)
        obj2_rot = cmds.xform(object2,q=1,ws=1,ro=True)
        object2matrix = cmds.xform( object2, query=True, worldSpace=True,t=True )
        wst = cmds.xform(object2,q=True,ws=True,t=True)
        wst1 = cmds.xform(object1,q=True,ws=True,t=True)
        
        
        
    for attribute in ["Translate","Rotate","Scale"]:
        skipList = []
        goList = []
        
        for attr in ["X","Y","Z"]:
            if cmds.control(attribute + attr + "_saCheckBox", exists = True):
                pointer = mui.MQtUtil.findControl(attribute + attr + "_saCheckBox")
                checkBox = shiboken.wrapInstance(long(pointer),qt.QCheckBox)
                value = checkBox.isChecked()
                print value
                if not value:
                    skipList.append(attr.lower())

                    
                    
        if len(skipList) != 6:
            if attribute == "Translate":
                print skipList
                loc1 = cmds.spaceLocator(n="temp")
                const = cmds.pointConstraint(object1,loc1)
                cmds.delete(const)
                cmds.pointConstraint(object2,loc1, skip = skipList)
                loc1temp = cmds.xform(loc1,q=True,ws=True,t=True)
                cmds.xform(object1,t=loc1temp)
                cmds.delete(loc1)
            if attribute == "Rotate":
                print skipList
                loc2 = cmds.spaceLocator(n="temp")
                const1 = cmds.pointConstraint(object1,loc2)
                cmds.delete(const1)
                cmds.orientConstraint(object2,loc2, skip = skipList)
                loc2temp = cmds.xform(loc2,q=True,ws=True,ro=True)
                cmds.xform(object1,ro=loc2temp)
                cmds.delete(loc2)
                

def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return shiboken.wrapInstance(long(ptr),qt.QWidget)


def createSnapAlignLayout(attribute,parentLayout):
    layout = qt.QHBoxLayout()
    parentLayout.addLayout(layout)
    
    label = qt.QLabel(attribute)
    layout.addWidget(label)
    
    font = qt.QFont()
    font.setPointSize(10)
    font.setBold(True)
    label.setFont(font)
    
    for attr in ["X","Y","Z"]:
        checkbox = qt.QCheckBox(attr)
        objectName = attribute.partition(":")[0] + attr + "_saCheckBox"
        checkbox.setObjectName(objectName)
        layout.addWidget(checkbox)
        checkbox.setMinimumWidth(50)
        checkbox.setMaximumWidth(50)
        
    
    
    

def snapAlign_UI():
    objectName = "snapAlignWin"
    if cmds.window("snapAlignWin", exists=True):
        cmds.deleteUI("snapAlignWin", wnd=True)
        
    parent = getMayaWindow()
    window = qt.QMainWindow(parent)
    window.setObjectName(objectName)
    window.setWindowTitle("snapAlignWin")
    window.setMinimumSize(300,150)
    window.setMaximumSize(300,150)
    
    mainWidget = qt.QWidget()
    window.setCentralWidget(mainWidget)

    
    verticalLayout = qt.QVBoxLayout(mainWidget)
    
    labelExplain = qt.QLabel("           First object --------->>> Second Object")
    
    labelMain = qt.QLabel("        Select what attributes you would like to snap")
    
    verticalLayout.addWidget(labelExplain)
    spacer =qt.QSpacerItem(100,0)
    verticalLayout.addSpacerItem(spacer)
    verticalLayout.addWidget(labelMain)
    
    for attribute in ["Translate:","Rotate:"]:
        createSnapAlignLayout(attribute,verticalLayout)
    snapButton = qt.QPushButton("snap it")
    verticalLayout.addWidget(snapButton)
    snapButton.clicked.connect(snapFunc)
    window.show()


snapAlign_UI()