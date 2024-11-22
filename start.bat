@echo off

REM  Check for permissions
 >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

REM If error flag set, we do not have admin.
 if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
 ) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

REM Check virtual environment exists
IF EXIST ".venv" (
    goto :RUN
)

:VENV
echo Creating python virtual environment...
python -m venv .venv
echo Virtual environment created.

:RUN
echo Activating virtual environment...
call .venv\Scripts\activate.bat

python noone_pause.py

deactivate
pause