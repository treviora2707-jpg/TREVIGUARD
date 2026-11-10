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
