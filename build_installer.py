"""
TREVIORA AI DEFENDER - PyInstaller Executable Builder
Compiles the application into a standalone Windows executable.
Build artifacts are placed strictly on D: drive (D:\projects\antivirus\dist\).
"""
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path("D:/projects/antivirus")
ENTRY_POINT = BASE_DIR / "treviora_defender" / "main.py"
ICON_PATH = BASE_DIR / "resources" / "icon.ico"
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"


def build():
    print("========================================================")
    print("      TREVIORA AI DEFENDER - EXECUTABLE BUILDER")
    print("             DEVELOPER: TREVIORA INDUSTRY")
    print("========================================================")
    print(f"Source: {ENTRY_POINT}")
    print(f"Target Distribution: {DIST_DIR}")
    print("--------------------------------------------------------")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=TrevioraAIDefender",
        "--noconsole",
        "--onedir",
        f"--icon={ICON_PATH}",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--specpath={BASE_DIR}",
        f"--add-data={BASE_DIR / 'resources'};resources",
        f"--add-data={BASE_DIR / 'data' / 'rules'};data/rules",
        f"--add-data={BASE_DIR / 'data' / 'models'};data/models",
        "--paths=d:/projects/antivirus",
        "--clean",
        "--noconfirm",
        str(ENTRY_POINT)
    ]

    print("Running PyInstaller compiler...")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n========================================================")
        print(f"BUILD SUCCESSFUL! Binary available at:\n{DIST_DIR / 'TrevioraAIDefender' / 'TrevioraAIDefender.exe'}")
        print("========================================================")
    else:
        print(f"\n[ERROR] Build failed with return code {result.returncode}")


if __name__ == "__main__":
    build()
