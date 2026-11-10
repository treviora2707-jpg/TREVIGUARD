@echo off
title TREVIORA AI DEFENDER 2.1 - Launcher
echo ========================================================
echo         TREVIORA AI DEFENDER - WINDOWS 11
echo           Developed by TREVIORA INDUSTRY
echo       Primary Target: Lenovo LOQ (Ryzen 5 / RTX 3050)
echo ========================================================
echo.
echo Launching Treviora AI Defender from D:\projects\antivirus...
echo.

:: Check if source code is armored
if exist "%~dp0treviora_defender\main.py" (
    findstr /C:"__TREVIORA_ARMORED__ = True" "%~dp0treviora_defender\main.py" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        if exist "%~dp0key.txt" (
            echo [VAULT] Armored source detected. Auto-unlocking with local master key...
            python "%~dp0unlock_vault.py"
        ) else (
            echo ======================================================================
            echo [!] TREVIORA SECURITY VAULT IS LOCKED ^& ENCRYPTED (AES-256)
            echo ======================================================================
            echo The source code is encrypted to protect firewall architecture and loopholes.
            echo.
            echo To install and run the production application without source code:
            echo   Launch: Treviora_Setup.exe
            echo.
            echo To unlock source code for developer editing:
            echo   python unlock_vault.py
            echo ======================================================================
            pause
            exit /b 1
        )
    )
)

set PYTHONPATH=D:\projects\antivirus
if exist "C:\Users\Thiruvel\AppData\Local\Programs\Python\Python312\python.exe" (
    "C:\Users\Thiruvel\AppData\Local\Programs\Python\Python312\python.exe" "D:\projects\antivirus\treviora_defender\main.py" %*
) else (
    python "D:\projects\antivirus\treviora_defender\main.py" %*
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with code %ERRORLEVEL%.
    pause
)
