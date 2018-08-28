#!/usr/bin/python
#  -*- coding: iso-8859-15 -*

# Python hooks for SVN

import os, subprocess, _winreg
from base64 import b64encode, b64decode


SCRIPTPATH = 'D:/SeasunProjects/ToolBox/DCC/Maya/scripts/VersionControl/'
USERDIR = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
USERDOCUMENTS = _winreg.QueryValueEx(USERDIR, 'Personal')[0]
USERLOCALAPPDATA = _winreg.QueryValueEx(USERDIR, 'Local AppData')[0]

# sets the file to add state
def add(filePath):

    print 'svn add "' + filePath + '"'
    p = subprocess.Popen('svn add "' + filePath + '"', stdout=subprocess.PIPE, shell=True)
    output = p.communicate()

    if output[0] == '':
        return False
    else:
        return True


# checks if the file has been set to add
def checkAdd(filePath):
    p = subprocess.Popen('svn add "' + filePath + '"', stdout=subprocess.PIPE, shell=True)
    b_add = p.communicate()

    return b_add


# reverts or undoes add
def revert(filePath):
    print "reverting", filePath
    subprocess.Popen('svn revert "' + filePath + '"')


# checks out a file
def checkoutFile(file):
    print "checking out", file
    subprocess.Popen('svn checkout file:')


# deletes a file from the depot
def delete(file):
    print "deleting", file
    subprocess.Popen('svn delete "' + file + '"', shell = True)


# moves file to a new location
def moveFile(file, newLocation):
    print "moving ", file, "to", newLocation


# locks the file
def lockFile(file):
    print "locking", file


# unlocks the file
def unlockFile(file):
    print "unlocking", file


# commits the file to the depot
def commit(filePath, message):

    subprocess.Popen('svn commit "' + filePath + '" -m "' + message + '"', shell = True)


# checks if the file exists in the depot
def checkExists(filePath):
    p = subprocess.Popen('svn info "' + filePath + '"', stdout=subprocess.PIPE, shell=True)
    (output) = p.communicate()
    print output
    for line in output:
        if line == "":
            return False
        else:
            return True


# gets specified data from the file path if it exists in the depot
def getInfo(filePath, data):

    b_exists = checkExists(filePath)
    if not b_exists:
        error = False
        return error
    else:
        p = subprocess.Popen('svn info "' + filePath + '"', stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()

        info = output.split('\n')

        fileInfo = {'path': (info[0].split(':'))[1] + ":" +  (info[0].split(':'))[2],
                    'name': (info[1].split(':'))[1],
                    'workingCopyRootPath': (info[2].split(':'))[1] + ':' + (info[2].split(':'))[2],
                    'url': (info[3].split(':'))[1] + ':' + (info[3].split(':'))[2],
                    'relativeUrl': (info[4].split(':'))[1],
                    'repoRoot': (info[5].split(':'))[1] + ':' + (info[5].split(':'))[2],
                    'repoUUID': (info[6].split(':'))[1],
                    'revision': (info[7].split(':'))[1],
                    'nodeKind': (info[8].split(':'))[1],
                    'schedule': (info[9].split(':'))[1],
                    'lastChangedAuthor': (info[10].split(':'))[1],
                    'lastChangedRev': (info[11].split(':'))[1],
                    'lastChangedDate': (info[12].split(':'))[1] + ':' + (info[12].split(':'))[2] + ':' + (info[12].split(':'))[3],
                    'textLastUpdated': (info[13].split(':'))[1] + ':' + (info[13].split(':'))[2] + ':' + (info[13].split(':'))[3],
                    'checkSum': (info[14].split(':'))[1]
                    }
        return fileInfo[data]


# -------------------------- User Login ----------------------------
def writeUserData(userData):
    global SCRIPTPATH
    global USERDOCUMENTS

    print "Writing user data"

    encriptedData = encryptData(userData)

    file = open(SCRIPTPATH + 'userInfo.txt','wb')
    file.write(encriptedData[0] + ',')
    file.write(encriptedData[1])
    file.close()

# encrypts the data being passed in
def encryptData(userData):
    global USERLOCALAPPDATA

    print "Encrypting Data"

    if os.path.isfile(USERLOCALAPPDATA + '\\svnpy\\userInfo.txt') == False:
        genSalt()
        salt = readSalt()
    else:
        salt = readSalt()

    encryptedData = [b64encode(b64decode(salt[0])+b64encode(userData[0])),
                     b64encode(b64decode(salt[1])+b64encode(userData[1]))]

    return encryptedData

# decrypts the user info data coming from the text file
def decryptData(encryptedData):
    print"decript data"

    salt = readSalt()

    username = b64decode(b64decode(encryptedData[0]).replace(b64decode(salt[0]), ''))
    password = b64decode(b64decode(encryptedData[1]).replace(b64decode(salt[1]), ''))

    return username, password

# reads the user data from the userInfo.txt
def readUserData():
    global SCRIPTPATH

    print "Reading user data"

    if not os.path.isfile(SCRIPTPATH + 'userInfo.txt'):

        userData = ['username', 'password']

        writeUserData(userData)
        print "user data has been written"

        return None
    else:
        argsfile = open(SCRIPTPATH + 'userInfo.txt', 'r')
        for line in argsfile:
            paths = line.split(',')
            username = paths[0]
            password = paths[1]
            print "line", line
            userData = [username, password]

            return userData

# Generates a random salt value
def genSalt():
    global USERLOCALAPPDATA

    if not os.path.isdir(USERLOCALAPPDATA + '\\svnpy'):
        os.mkdir(USERLOCALAPPDATA + '\\svnpy')

    saltFile = open(USERLOCALAPPDATA + '\\svnpy\\userInfo.txt', 'a')
    userSalt = b64encode(os.urandom(24))
    pwSalt = b64encode(os.urandom(24))

    encryptUserSalt = b64encode(userSalt)
    encryptPwSalt = b64encode(pwSalt)
    saltFile.write(str(encryptUserSalt) + ',' + str(encryptPwSalt))
    saltFile.close()

# Reads from the file to get the salt value
def readSalt():
    global USERDOCUMENTS

    saltFile = open(USERLOCALAPPDATA + '\\svnpy\\userInfo.txt', 'r')
    for line in saltFile:
        salt = line.split(',')
        return salt