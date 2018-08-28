@echo off

FOR /F "usebackq tokens=3*" %%A IN (`REG QUERY "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Personal`) DO (
    set appdir=%%A%%B
    )

:: setting environment variables

setx MAYA_UI_LANGUAGE "en_US"
echo Maya language set to English

xcopy /s r:\jx4\tools\dcc\maya\scripts\setupmaya\data\Maya.env "%appdir%\maya\2016\"
echo Finished setting up Maya Environment

xcopy /s r:\jx4\tools\dcc\maya\scripts\setupmaya\data\seasun.module %appdir%\maya\2016\modules\
echo Finished setting up Maya Module
PAUSE