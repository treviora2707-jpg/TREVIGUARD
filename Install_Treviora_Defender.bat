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
if exist "%~dp0Treviora_Setup.exe" (
    echo [OK] Launching Standalone Windows Setup Executable: Treviora_Setup.exe...
    start "" "%~dp0Treviora_Setup.exe"
    exit /b 0
)

echo Launching Treviora Hardware-Adaptive Setup Wizard...
set PYTHONPATH=%~dp0

:: Check if source code is armored
if exist "%~dp0treviora_defender\installer\setup_wizard.py" (
    findstr /C:"__TREVIORA_ARMORED__ = True" "%~dp0treviora_defender\installer\setup_wizard.py" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        if exist "%~dp0key.txt" (
            echo [VAULT] Armored source detected. Unlocking with local master key...
            python "%~dp0unlock_vault.py"
        ) else (
            echo ======================================================================
            echo [!] TREVIORA SECURITY VAULT IS LOCKED ^& ENCRYPTED (AES-256)
            echo ======================================================================
            echo The source code is encrypted to protect firewall architecture and loopholes.
            echo Please run Treviora_Setup.exe to install the application.
            echo ======================================================================
            pause
            exit /b 1
        )
    )
)

python "%~dp0treviora_defender\installer\setup_wizard.py"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installation exited with code %ERRORLEVEL%.
    pause
)
