import _winreg
import subprocess

HKLM_MAYA_PATH = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Autodesk\\Maya\\2016\\Setup\\InstallPath')
MAYAPATH = _winreg.QueryValueEx(HKLM_MAYA_PATH,'MAYA_INSTALL_LOCATION')[0]

def main():
    global MAYAPATH
    subprocess.Popen([MAYAPATH + 'bin/mayapy.exe', 'exportXYL.py'],stdout=subprocess.PIPE)
main()