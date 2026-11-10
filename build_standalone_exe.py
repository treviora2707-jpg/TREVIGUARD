"""
PyInstaller Build Automation for TREVIORA AI DEFENDER 2.1
Compiles:
1. Treviora_AI_Defender.exe (Main Desktop Suite with --uac-admin)
2. Treviora_Setup.exe (Universal Hardware-Adaptive Installer)
Bundles all YARA rules, ONNX model, assets, and dependencies.
"""
import sys
import os
import subprocess
from pathlib import Path

BASE_DIR = Path("D:/projects/antivirus").resolve()
os.chdir(str(BASE_DIR))

def build_executables():
    print("=" * 70)
    print("  BUILDING STANDALONE WINDOWS EXECUTABLES VIA PYINSTALLER")
    print("  DEVELOPER: TREVIORA INDUSTRY")
    print("=" * 70)

    # Assets & Data to bundle
    data_separator = ";"  # Windows
    add_data_args = [
        f"--add-data={BASE_DIR / 'data'}{data_separator}data",
        f"--add-data={BASE_DIR / 'resources'}{data_separator}resources",
    ]

    # Icon path
    icon_path = BASE_DIR / "resources" / "icon.png"
    icon_args = [f"--icon={icon_path}"] if icon_path.exists() else []

    # 1. Build Main Application (Treviora_AI_Defender.exe)
    print("\n[1/2] Compiling Main Application: Treviora_AI_Defender.exe...")
    cmd_main = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--uac-admin",  # Request Administrator privileges automatically
        "--name=Treviora_AI_Defender",
        f"--distpath={BASE_DIR / 'dist'}",
        f"--workpath={BASE_DIR / 'build'}",
        *add_data_args,
        *icon_args,
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=psutil",
        "--hidden-import=cryptography",
        "--hidden-import=onnxruntime",
        str(BASE_DIR / "treviora_defender" / "main.py")
    ]
    print("Executing:", " ".join(cmd_main[:10]) + "...")
    res1 = subprocess.run(cmd_main, cwd=str(BASE_DIR))
    if res1.returncode != 0:
        print("[ERROR] Main executable compilation failed with code", res1.returncode)
        return False
    print(" -> Successfully generated dist/Treviora_AI_Defender/Treviora_AI_Defender.exe")

    # 2. Build Setup Installer (Treviora_Setup.exe)
    print("\n[2/2] Compiling Setup Installer: Treviora_Setup.exe...")
    cmd_installer = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--uac-admin",  # Request Administrator elevation for installation
        "--name=Treviora_Setup",
        f"--distpath={BASE_DIR / 'dist'}",
        f"--workpath={BASE_DIR / 'build'}",
        *add_data_args,
        *icon_args,
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PySide6.QtGui",
        str(BASE_DIR / "treviora_defender" / "installer" / "setup_wizard.py")
    ]
    print("Executing:", " ".join(cmd_installer[:10]) + "...")
    res2 = subprocess.run(cmd_installer, cwd=str(BASE_DIR))
    if res2.returncode != 0:
        print("[ERROR] Installer compilation failed with code", res2.returncode)
        return False
    print(" -> Successfully generated dist/Treviora_Setup.exe")

    print("\n" + "=" * 70)
    print("ALL WINDOWS EXECUTABLES BUILT SUCCESSFULLY!")
    print(f"Location: {BASE_DIR / 'dist'}")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = build_executables()
    sys.exit(0 if success else 1)
