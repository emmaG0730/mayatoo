import _winreg

HKLM_MAYA_PATH = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Autodesk\\Maya\\2016\\Setup\\InstallPath')
MAYAPATH = _winreg.QueryValueEx(HKLM_MAYA_PATH,'MAYA_INSTALL_LOCATION')[0]
HKLM_MAX_PATH = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Autodesk\\3dsMax\\18.0')
MAXPATH = _winreg.QueryValueEx(HKLM_MAX_PATH, 'Installdir')[0]
P4PROJPATH = 'D:\\SeasunProjects'
EXTERNALSCRIPTS = P4PROJPATH + "\\ToolBox\\External"
EXTERNALMAYA = EXTERNALSCRIPTS + "\\DCC\\Maya"
MAYASCRIPTS = P4PROJPATH + "\\ToolBox\\DCC\\Maya\\scripts"
MAXSCRIPTS = P4PROJPATH + "\\ToolBox\\DCC\\Max"
MOBUSCRIPTS = P4PROJPATH + "\\ToolBox\\DCC\\Mobu"
USERDIR = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
USERDOCUMENTS = _winreg.QueryValueEx(USERDIR, 'Personal')[0]