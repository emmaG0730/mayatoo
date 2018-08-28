@ECHO OFF
FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKLM\Software\Autodesk\Maya\2016\Setup\InstallPath" /v MAYA_INSTALL_LOCATION`) DO (
    set appdir=%%A %%B
    )

"%appdir%bin/mayapy.exe" R:/Jx4/tools/dcc/maya/nightly/scripts/starmanExporter/starman_weapon_batch_export.py
PAUSE