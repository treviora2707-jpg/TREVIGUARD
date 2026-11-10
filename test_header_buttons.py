"""
Test for Top Header Controls:
1. 🔔 Security Notifications Dialog
2. 🔅 / 🌙 Theme & Brightness Toggle
3. 👤 User Profile & Dynamic Hardware Dialog
"""
import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from treviora_defender.ui.styles import MAIN_STYLE
from treviora_defender.ui.main_window import MainWindow
from treviora_defender.core.hardware_profile import HardwareProfile


def test_buttons():
    print("=" * 60)
    print("TESTING HEADER CONTROLS: BELL (🔔), THEME (🔅), USER (👤)")
    print("=" * 60)

    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)

    window = MainWindow()
    window.show()

    # 1. Test Theme Toggle
    print("\n[1/3] Testing Theme / Brightness Toggle (🔅 / 🌙)...")
    assert window.btn_theme.text() == "🔅"
    assert window.is_stealth_mode is False
    window._toggle_theme_brightness()
    assert window.is_stealth_mode is True
    assert window.btn_theme.text() == "🌙"
    print(" -> Switched to Stealth Obsidian Night Mode (🌙) - Verified!")
    window._toggle_theme_brightness()
    assert window.is_stealth_mode is False
    assert window.btn_theme.text() == "🔅"
    print(" -> Switched back to Cyber Neon Mode (🔅) - Verified!")

    # 2. Test Notification Bell
    print("\n[2/3] Testing Notification Bell Dialog (🔔)...")
    window._open_notifications_dialog()
    assert hasattr(window, "notif_dialog")
    assert window.notif_dialog.isVisible()
    print(" -> Security Notifications Dialog successfully instantiated & rendered!")
    window.notif_dialog.close()

    # 3. Test User Profile & Hardware Intel
    print("\n[3/3] Testing User Profile & Dynamic Hardware Dialog (👤)...")
    window._open_user_profile_dialog()
    assert hasattr(window, "user_dialog")
    assert window.user_dialog.isVisible()
    profile = HardwareProfile.get_profile()
    print(f" -> Discovered Host: {profile['os']['hostname']}")
    print(f" -> Discovered CPU: {profile['cpu']['raw_name']}")
    print(f" -> Discovered GPU: {profile['gpu']['name']}")
    print(f" -> Discovered RAM: {profile['ram']['formatted']}")
    print(f" -> Dynamic Spec: {profile['display_spec']}")
    window.user_dialog.close()

    window.stop_monitors()
    print("\n" + "=" * 60)
    print("ALL 3 HEADER BUTTONS OPERATIONAL WITH ZERO BUGS!")
    print("=" * 60)


if __name__ == "__main__":
    test_buttons()
