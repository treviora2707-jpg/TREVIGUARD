@echo off
title TREVIORA AI DEFENDER 2.1 - Universal Windows Installer
echo ======================================================================
echo             TREVIORA AI DEFENDER - WINDOWS 11 INSTALLER
echo                 Developed by TREVIORA INDUSTRY
echo            "ENGINEERING TOMORROW, EMPOWERING HUMANITY"
echo ======================================================================
echo.

:: Check for Administrator Privileges
net session >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Running with Administrator Privileges.
) else (
    echo [NOTICE] Requesting Administrator Elevation (UAC)...
    powershell -Command "Start-Process '%~dp0Install_Treviora_Defender.bat' -Verb RunAs"
    exit /b
)

echo.
echo Launching Treviora Hardware-Adaptive Setup Wizard...
set PYTHONPATH=%~dp0
python "%~dp0treviora_defender\installer\setup_wizard.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installation exited with code %ERRORLEVEL%.
    pause
)
