#-----------------------------------------------------------------------------------#
# Scripted By: Linh Nguyen                                                          #
# Description: Allows for switching the Maya tools, Rigs, and Characters to         #
# Release or Nightly builds                                                         #
#-----------------------------------------------------------------------------------#
import os
import ctypes.wintypes
import readData as rd
import subprocess
import collections

class ReleaseStatus():

    def __init__(self,dataFile, version):
        CSIDL_PERSONAL = 5  # My Documents
        SHGFP_TYPE_CURRENT = 0  # Get current, not default value

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

        self.userPath = buf.value

        # reads in the json data file based on the maya version
        self.dataCheck = rd.rn_data(dataFile, version)

        self.mayaPref = self.dataCheck.get_maya_pref()

        self.moduleLocation = self.dataCheck.get_maya_module_location()
        self.moduleFileName = self.dataCheck.get_module_file_name()
        self.moduleDir = self.userPath + self.mayaPref + self.moduleLocation
        self.modulePath = self.moduleDir + '\\' + self.moduleFileName
        self.moduleName = self.dataCheck.get_module_name()
        self.moduleVersion = self.dataCheck.get_module_version()

        self.releasePath = self.dataCheck.get_tools(0,2)
        self.nightlyPath = self.dataCheck.get_tools(1,2)
        self.releaseData = '+ ' + self.moduleName + ' ' + self.moduleVersion + ' ' + self.releasePath
        self.nightlyData = '+ ' + self.moduleName + ' ' + self.moduleVersion + ' ' + self.nightlyPath

    # reads the maya environment file and returns a dictionary with the variables and their values
    def readMayEnv(self):
        envData = collections.OrderedDict()
        open(self.userPath + self.mayaPref + '\\maya.env', 'a')
        mayaEnv = open(self.userPath + self.mayaPref + '\\maya.env', 'r')
        for line in mayaEnv:
            if '=' in line:
                dataSplit = line.split('=')
                envData[dataSplit[0]]=dataSplit[1].strip('\n')
            else:
                pass

        return envData

    # appends the seasun custom paths to the maya paths
    # envData = Dictionary of maya env variables and their values
    # customPaths = Dictionary of custom env variables with their data
    def modifyMayaEnv(self, envData, customPaths):
        mayaVars = collections.OrderedDict()

        # extracts the maya varaible names from the custom paths
        # fills mayaVars data with the customPaths info
        for i in customPaths:
            paths = i.split('_')
            paths[0]='MAYA'
            mayaVars[('_').join(paths)] = '%' + i + '%'

        # check if custom variables exist within the maya env data
        for i in customPaths:
            if i in envData:
                print i, 'exists'
                for substring in customPaths[i]:
                    if substring in envData[i]:
                        print substring, 'exists'
                    else:
                        print substring, 'does not exist'
                        envData[i]=(',').join(customPaths[i])

            # if custom data does not exist in the maya env data, create a new collection and update the maya env data
            # with the collection's information
            else:
                print i, 'does not exist'

                # if list is not greater than 1, the key's value will be the first item within the list
                if len(customPaths[i]) > 1:
                    data = customPaths[i][0]
                # if list is greater than 1, join the list objects with a comma
                else:
                    data = (',').join(customPaths[i])

                # creates a new collection using the custom data
                customData = collections.OrderedDict()
                customData[i]=data

                # combines the collections together
                # this method is used to maintain the dictionary order
                customData.update(envData)
                envData = customData

            # check if custom vars are appended to the maya var paths
            # if not, append the custom vars to the existing maya var
            # if maya var doesn't exist, it will be generated
            for i in mayaVars:
                if i in envData:
                    print i, 'exists'
                    if mayaVars[i] in envData[i]:
                        print mayaVars[i], 'is in the path'
                    else:
                        print 'adding', mayaVars[i], 'to the path'
                        envData[i] = envData[i] + ',' + mayaVars[i]
                else:
                    print i, 'does not exist'
                    envData.update(mayaVars)
        return envData

    def writeMayaEnv(self, data):
        mayaEnv = open(self.userPath + self.mayaPref + '\\maya.env', 'w')

        for i in data:
            print i + '=' + data[i]
            mayaEnv.write(i + '=' + data[i] + '\n')

        mayaEnv.close()

    def createMayaModuleFile(self, modulePath, mode):
        print 'creating maya module file'
        open(modulePath, mode).close()

    # creates a new maya module in the user prefs
    def updateModuleData(self, moduleData, modulePath):
        print 'updating module data'
        module = open(modulePath, 'w')
        module.write(moduleData)
        module.close()

    def checkModuleData(self, modulePath):
        module = open(modulePath, 'r')

        # checks which mode the module is set to and returns an integer
        # 0 = release mode
        # 1 = nightly mode
        # 2 = missing or incorrect data
        if module.readline().strip() == self.releaseData.strip():
            print 'module is in release'
            return 0
        elif module.readline().strip() == self.nightlyData.strip():
            print 'module is in nightly'
            return 1
        else:
            print 'unsure module'
            return 2

    # checks which version of the module is being used to decifer if the tools are in release or nightly mode
    def checkToolsMode(self):
        print 'checking tools mode'

        if os.path.isdir(self.moduleDir):
            # checks if module exists
            if os.path.isfile(self.modulePath):
                print 'module exists'
                moduleData = self.checkModuleData(self.modulePath)
                return moduleData

            # if module file doesn't exist, module file is created
            else:
                print 'module file does not exist, creating module file'
                self.createMayaModuleFile(self.modulePath, 'a')
                moduleData = self.checkModuleData(self.modulePath)
                return moduleData

        # if directory doesn't exist, directory and module file will be generated
        else:
            print 'module directory does not exist, creating directory'
            os.makedirs(self.moduleDir)
            print 'creating module file'
            self.createMayaModuleFile(self.modulePath, 'a')
            moduleData = self.checkModuleData(self.modulePath)
            return moduleData

    # checks the custom environment variable for the rig mode to see if it is in release or nightly mode
    # return data
    # 0 = release mode
    # 1 = nightly mode
    # 2 = missing value for environment variable
    def checkRigMode(self, envVar):
        envExists = os.getenv(envVar)

        # if environment variable doesn't exist a new one will be made with a none value
        # environment variable is created using a subprocess
        if envExists == None:
            print 'creating', envVar
            print 'SETX ' + envVar + ' = '
            subprocess.Popen('SETX ' + envVar + ' none')

        # checks the environment variable to see if it matches the data from json file and returns a value
        # based on findings.
        else:
            print 'checking rig mode'

            if envExists == self.dataCheck.get_rig(0,1):
                return 0
            elif envExists == self.dataCheck.get_rig(1,1):
                return 1
            else:
                return 2

    # updates the custom environment variable to point to the nightly path
    def setRigNightly(self):
        print 'sets the rig mode to nightly'
        envVar = self.dataCheck.get_rig(1, 2)
        rigMode = self.checkRigMode(envVar)

        if rigMode == 1:
            print 'rig mode is already in nightly'

        # retrieves data from json data file and updates the environment variable to nightly mode
        else:
            print 'rig mode is switching to nightly'
            rig = self.dataCheck.get_rig(1,0)

            print envVar, '=',rig
            p = subprocess.Popen('SETX ' + envVar + ' ' + rig, stdout=subprocess.PIPE, bufsize = 0, shell=True)
            output, err = p.communicate()
            output = output.strip('\r\n')
            return output

    # updates the custome environment variable to point to the release path
    def setRigRelease(self):
        print 'sets the rig mode to release'
        envVar = self.dataCheck.get_rig(0, 2)
        rigMode = self.checkRigMode(envVar)

        # if the rig mode is already in nightly, do not do anything
        if rigMode == 0:
            print 'rig mode is already in release'

        # retrieves data from json data file and updates the environment variable to release mode
        else:
            print 'rig mode is switching to release'
            rig = self.dataCheck.get_rig(0, 0)
            envVar = self.dataCheck.get_rig(0, 2)
            print envVar, '=', rig
            p = subprocess.Popen('SETX ' + envVar + ' ' + rig, stdout=subprocess.PIPE, bufsize = 0, shell=True)
            output, err = p.communicate()
            output = output.strip('\r\n')
            return output

    # updates the maya module and maya environment variable to point to the nightly path
    def setToolsNightly(self):
        print 'sets the tools to nightly'
        toolsMode = self.checkToolsMode()
        print toolsMode

        if toolsMode == 1:
            print 'tools mode is already in nightly'
            shelf = self.dataCheck.get_tools(1, 0)
            scripts = self.dataCheck.get_tools(1, 1)

            # combines the dictionaries together
            shelf.update(scripts)
            self.setTools(shelf)
        else:
            print 'tools mode is switching to nightly'

            shelf = self.dataCheck.get_tools(1, 0)
            scripts = self.dataCheck.get_tools(1, 1)

            # combines the dictionaries together
            shelf.update(scripts)

            self.updateModuleData(self.nightlyData, self.modulePath)
            self.setTools(shelf)

    # updates the maya module and maya environment variable to point to the release path
    def setToolsRelease(self):
        print 'sets the tools to release'
        moduleMode = self.checkToolsMode()
        print moduleMode

        if moduleMode == 0:
            print 'tools mode is already in release'
            shelf = self.dataCheck.get_tools(0, 0)
            scripts = self.dataCheck.get_tools(0, 1)

            # combines dictionaries together
            shelf.update(scripts)
            self.setTools(shelf)
        else:
            print 'tools mode is switching to release'
            shelf = self.dataCheck.get_tools(0, 0)
            scripts = self.dataCheck.get_tools(0, 1)

            # combines dictionaries together
            shelf.update(scripts)

            self.updateModuleData(self.releaseData, self.modulePath)
            self.setTools(shelf)

    def setTools(self, customData):
        envData = self.readMayEnv()
        envData = self.modifyMayaEnv(envData, customData)
        self.writeMayaEnv(envData)


rs = ReleaseStatus('R:\\Jx4\\tools\\dcc\\maya\\scripts\\releaseNightly\\data\\releaseNightly.json', '2016') # DJM

def toolsRelease():
    print 'sets tools to release'
    rs.setToolsRelease()
    print '-----------------------------------------------------------'

def toolsNightly():
    print 'sets tools to nightly'
    rs.setToolsNightly()
    print '-----------------------------------------------------------'

def rigRelease():
    print 'sets rig to release'
    output = rs.setRigRelease()
    print '-----------------------------------------------------------'
    return output


def rigNightly():
    print 'sets rig to nightly'
    output = rs.setRigNightly()
    print '-----------------------------------------------------------'
    return output