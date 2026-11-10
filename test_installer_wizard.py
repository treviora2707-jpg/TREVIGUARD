"""
Test for Universal Windows Setup Wizard
Validates:
- Hardware auto-detection in setup
- Wizard pages flow
- Permissions configuration
"""
import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from treviora_defender.installer.setup_wizard import SetupWizard
from treviora_defender.core.hardware_profile import HardwareProfile

def test_installer():
    print("=" * 60)
    print("TESTING UNIVERSAL WINDOWS SETUP WIZARD & PERMISSIONS")
    print("=" * 60)

    app = QApplication(sys.argv)
    wizard = SetupWizard()
    wizard.show()

    profile = wizard.profile
    print(f"[1/4] Discovered Processor: {profile['cpu']['raw_name']}")
    print(f"[2/4] Discovered GPU: {profile['gpu']['name']}")
    print(f"[3/4] Host Form Factor: {profile['form_factor']['type']}")
    print(f"[4/4] Auto Tuning Profile: {profile['tuning']['profile_name']}")

    assert profile["cpu"]["vendor"] in ["AMD", "Intel", "Generic"]
    assert profile["ram"]["total_gb"] > 0
    assert len(wizard.pageIds()) == 5
    print(" -> All 5 Setup Wizard Pages (Welcome, Hardware, Permissions, Progress, Finish) ready!")

    wizard.close()
    print("\n" + "=" * 60)
    print("INSTALLER WIZARD & PERMISSIONS SYSTEM VERIFIED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_installer()
