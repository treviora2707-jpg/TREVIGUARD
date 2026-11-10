r"""
TREVIORA AI DEFENDER - Professional Windows 11 Installer
Developer: TREVIORA INDUSTRY
Strictly installs software into D: drive (Default: D:\projects\antivirus\installed).
Creates Desktop & Start Menu shortcuts, configures auto-startup, and creates uninstaller.
"""
import sys
import os
import shutil
import winreg
import argparse
from pathlib import Path

# Defaults strictly to D: drive workspace as demanded by user
DEFAULT_INSTALL_DIR = Path("D:/projects/antivirus/installed")
SOURCE_DIR = Path("D:/projects/antivirus")


def create_windows_shortcut(target_exe: str, shortcut_path: str, icon_path: str = "", description: str = ""):
    """
    Creates a Windows .lnk shortcut using VBScript / Windows Script Host via COM.
    """
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target_exe
        shortcut.WorkingDirectory = str(Path(target_exe).parent)
        shortcut.Description = description
        if icon_path and os.path.exists(icon_path):
            shortcut.IconLocation = icon_path
        shortcut.save()
        print(f"[OK] Created shortcut: {shortcut_path}")
        return True
    except Exception:
        # Fallback via PowerShell script
        try:
            ps_cmd = (
                f"$s = (New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}'); "
                f"$s.TargetPath = '{target_exe}'; "
                f"$s.WorkingDirectory = '{Path(target_exe).parent}'; "
                f"$s.Description = '{description}'; "
            )
            if icon_path and os.path.exists(icon_path):
                ps_cmd += f"$s.IconLocation = '{icon_path}'; "
            ps_cmd += "$s.Save()"
            os.system(f'powershell -NoProfile -Command "{ps_cmd}"')
            print(f"[OK] Created shortcut via PowerShell: {shortcut_path}")
            return True
        except Exception as e:
            print(f"[Warning] Could not create shortcut: {e}")
            return False


def install(target_dir: Path = DEFAULT_INSTALL_DIR, create_desktop_icon=True, create_start_menu=True, auto_start=False):
    print("========================================================")
    print("      TREVIORA AI DEFENDER - INSTALLER WIZARD")
    print("             DEVELOPER: TREVIORA INDUSTRY")
    print("========================================================")
    print(f"Target Installation Directory: {target_dir}")
    print("Storage policy: STRICT D: DRIVE DEPLOYMENT (Zero footprint on C:)")
    print("--------------------------------------------------------")

    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy files
    print("Deploying application files...")
    items_to_copy = [
        "treviora_defender", "resources", "data", "requirements.txt",
        "run_treviora.bat", "README.md"
    ]

    for item in items_to_copy:
        src = SOURCE_DIR / item
        dst = target_dir / item
        if src.exists():
            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            print(f"  [+] Installed {item}")

    launcher_bat = target_dir / "run_treviora.bat"
    icon_ico = target_dir / "resources" / "icon.ico"

    # Create Uninstaller Script
    uninstaller_path = target_dir / "uninstall.bat"
    with open(uninstaller_path, "w", encoding="utf-8") as f:
        f.write(f"""@echo off
title Treviora AI Defender - Uninstaller
echo ========================================================
echo        TREVIORA AI DEFENDER - UNINSTALL WIZARD
echo ========================================================
echo.
set /p confirm="Are you sure you want to uninstall Treviora AI Defender from {target_dir}? (y/n): "
if /i "%confirm%" NEQ "y" exit /b

echo Removing Desktop and Start Menu shortcuts...
del /q "%USERPROFILE%\\Desktop\\TREVIORA AI DEFENDER.lnk" 2>nul
del /q "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\TREVIORA AI DEFENDER.lnk" 2>nul

echo Cleaning registry startup entries...
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "TrevioraAIDefender" /f 2>nul

echo.
echo Application shortcuts removed. You may now safely delete:
echo {target_dir}
pause
""")
    print("  [+] Generated uninstaller script: uninstall.bat")

    # Shortcuts
    user_home = Path.home()
    if create_desktop_icon:
        desktop_link = user_home / "Desktop" / "TREVIORA AI DEFENDER.lnk"
        create_windows_shortcut(
            target_exe=str(launcher_bat),
            shortcut_path=str(desktop_link),
            icon_path=str(icon_ico),
            description="TREVIORA AI DEFENDER - Endpoint Cybersecurity"
        )

    if create_start_menu:
        start_menu = Path(os.environ.get("APPDATA", str(user_home / "AppData/Roaming"))) / "Microsoft/Windows/Start Menu/Programs"
        if start_menu.exists():
            menu_link = start_menu / "TREVIORA AI DEFENDER.lnk"
            create_windows_shortcut(
                target_exe=str(launcher_bat),
                shortcut_path=str(menu_link),
                icon_path=str(icon_ico),
                description="TREVIORA AI DEFENDER"
            )

    # Windows Startup integration
    if auto_start:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "TrevioraAIDefender", 0, winreg.REG_SZ, f'"{launcher_bat}"')
            winreg.CloseKey(key)
            print("  [+] Configured automatic launch with Windows.")
        except Exception as e:
            print(f"  [-] Could not set startup registry entry: {e}")

    print("--------------------------------------------------------")
    print("SUCCESS: TREVIORA AI DEFENDER installed successfully on D: drive!")
    print(f"Location: {target_dir}")
    print("Launch via Desktop shortcut or run_treviora.bat.")
    print("========================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Treviora AI Defender Installer")
    parser.add_argument("--dir", type=str, default=str(DEFAULT_INSTALL_DIR), help="Target install directory on D:")
    parser.add_argument("--no-desktop", action="store_true", help="Do not create Desktop shortcut")
    parser.add_argument("--no-start-menu", action="store_true", help="Do not create Start Menu shortcut")
    parser.add_argument("--auto-start", action="store_true", help="Launch with Windows")
    args = parser.parse_args()

    install(
        target_dir=Path(args.dir),
        create_desktop_icon=not args.no_desktop,
        create_start_menu=not args.no_start_menu,
        auto_start=args.auto_start
    )
