import maya.cmds as cmds
import subprocess
import VersionControl.svnPy as svnPy


def runSVN():
    filePath = cmds.file(query = True, sceneName = True)
    if filePath == "":
        errorWin('File not in Depot.\nPlease save the file first')
    else:
        b_exists = svnPy.getInfo(filePath, 'path')
        if b_exists:
            filePath = cmds.file(query = True, sceneName = True)
            fileUrl = svnPy.getInfo(filePath, 'url')
            repoRoot = svnPy.getInfo(filePath, 'repoRoot')
            subprocess.Popen('python "D:\SeasunProjects\ToolBox\DCC\Maya\scripts\VersionControl\svnCheckoutMaya.py" ' + fileUrl + ' ' + repoRoot, shell = True)
        else:
            b_add = addWin('File not in Depot.\nWould you like to add this to SVN?')

            if b_add == "No":
                print "Not adding file"
            else:
                b_inrepoPath = svnPy.add(filePath)
                print b_inrepoPath

def errorWin(message):
    cmds.confirmDialog( title='Error', message=message, button=['OK'], cancelButton='OK', dismissString='No' )

def addWin(message):
    response = cmds.confirmDialog( title='Add File', message=message, button=['Yes', 'No'], cancelButton='OK', dismissString='No' )
    return response

runSVN()