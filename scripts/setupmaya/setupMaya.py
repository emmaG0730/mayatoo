import _winreg
import os
import shutil

USERDIR = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
USERDOCUMENTS = _winreg.QueryValueEx(USERDIR, 'Personal')[0]
MAYAPREFS = USERDOCUMENTS + '\\maya\\2016'
SCRIPTPATH = 'R:\\JX4\\tools\\dcc\\maya\\scripts'

def setupModule():
    global MAYAPREFS
    global SCRIPTPATH

    if not os.path.isdir(MAYAPREFS + '\\modules'):
        os.mkdir(MAYAPREFS + '\\modules')

    shutil.copy(SCRIPTPATH + '\\setupmaya\\data\\seasun.module',MAYAPREFS + '\\modules\\')
    print "Seasun module has been created"

def setupMayaEnv():
    global MAYAPREFS
    global SCRIPTPATH

    if os.path.isfile(MAYAPREFS + '\\Maya.env'):
        os.rename(MAYAPREFS + '\\Maya.env', MAYAPREFS + '\\Maya.env.bak')
        shutil.copy(SCRIPTPATH + '\\setupmaya\\data\\Maya.env',MAYAPREFS + '\\')
        print "Maya environment has been updated"
    else:
        shutil.copy(SCRIPTPATH + '\\setupmaya\\data\\Maya.env',MAYAPREFS + '\\')
        print "Maya environment has been updated"

def setMayaLanguage():
    os.system('SETX MAYA_UI_LANGUAGE "en_US"')
    print "Maya language has been set to English"

def setupMaya():
    setupModule()
    setupMayaEnv()
    setMayaLanguage()

setupMaya()