"""
Capture high-res screenshots of the new dialogs:
- Security Notifications Dialog (🔔)
- User Profile & Dynamic Hardware Dialog (👤)
"""
import sys
import os
import time
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from treviora_defender.ui.styles import MAIN_STYLE
from treviora_defender.ui.header_dialogs import SecurityNotificationsDialog, UserProfileDialog

ARTIFACT_DIR = Path(r"C:\Users\Thiruvel\.gemini\antigravity\brain\a84d44c0-3f89-4e98-ae62-15a899da9949")

def capture_dialogs():
    app = QApplication(sys.argv)
    for font_file in ["segoeui.ttf", "segoeuib.ttf", "seguisb.ttf", "seguiemj.ttf"]:
        fp = Path("C:/Windows/Fonts") / font_file
        if fp.exists():
            QFontDatabase.addApplicationFont(str(fp))
    app.setStyleSheet(MAIN_STYLE)

    # 1. Capture Notifications Dialog
    dlg_notif = SecurityNotificationsDialog()
    dlg_notif.show()
    app.processEvents()
    time.sleep(0.1)
    app.processEvents()
    pix1 = dlg_notif.grab()
    pix1.save(str(ARTIFACT_DIR / "imanager_notifications_dialog.png"))
    print("Captured: imanager_notifications_dialog.png")
    dlg_notif.close()

    # 2. Capture User Profile Dialog
    dlg_user = UserProfileDialog()
    dlg_user.show()
    app.processEvents()
    time.sleep(0.1)
    app.processEvents()
    pix2 = dlg_user.grab()
    pix2.save(str(ARTIFACT_DIR / "imanager_user_profile_dialog.png"))
    print("Captured: imanager_user_profile_dialog.png")
    dlg_user.close()

if __name__ == "__main__":
    capture_dialogs()
