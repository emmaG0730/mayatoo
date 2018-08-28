import sys
import os
import csv

try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass
try:
    import maya.cmds as cmds
except:
    pass


class updateRef():

    def __init__(self):
        # dirPath, refRigPath, namespace
        print "Initiating"

    # Updates the rig reference path
    def updateRefPath(self, refPath, refNode):
        cmds.file(refPath, loadReference=refNode, type='mayaAscii', options='v=0')

    # Returns a list of .ma files within a directory
    def getFileList(self, directory, ext):
        return [file for root, dirs, files in os.walk(directory) for file in files if file.endswith(ext)]

    # Opens the passed in file and keeps the prompt off
    def openFile(self, fileName):
        cmds.file(fileName, force=True, open=True, prompt=False)

    def readCSV(self, fileName):
        fileData = []

        with open(fileName, 'rb') as csvfile:
            linereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in linereader:
                data = row[0].split(',')
                fileData.append(data)
        return fileData

    def standAloneBatch(self, fileName):
        fileData = self.readCSV(fileName)

        for i in fileData:
            fileList = self.getFileList(i[0], '.ma')
            self.batchProcess(i[0], i[1], i[2], fileList, i[3])

    def batchProcess(self, dirPath, refRigPath, namespace, files, tempLoc):
        newpath = (dirPath.split('/'))[4:]
        subPath = '/'.join(newpath)
        for i in files:
            if not os.path.exists(tempLoc + '/' + subPath):
                os.makedirs(tempLoc + '/' + subPath)
            self.openFile(dirPath + '/' + i)
            self.updateRefPath(refRigPath, namespace)
            print "Saving"
            print tempLoc + '/' + subPath + '/' + i
            cmds.file(rename=tempLoc + '/' + subPath + '/' + i)
            cmds.file(save=True, force=True, type="mayaAscii")
            print i + ' has been saved'

    def main(self):
        self.args = sys.argv
        self.dirPath = self.args[1]
        self.refRigPath = self.args[2]
        self.namespace = self.args[3]

        files = self.getFileList(self.dirPath, '.ma')
        self.batchProcess(self.dirPath, self.refRigPath, self.namespace, files, )

def main():
    batchRef = updateRef()
    batchRef.standAloneBatch('R:/Jx4/tools/dcc/maya/scripts/UpdateRigRefShftKeys/UpdateReferences/updateRefPaths.csv')

main()