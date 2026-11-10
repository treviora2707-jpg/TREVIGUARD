"""
Screenshots generator for TREVIORA AI DEFENDER (Vivo iManager Style)
Captures high-resolution renders of all views into the artifact directory.
Loads native TrueType fonts for crystal-clear typography.
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
from PySide6.QtCore import QTimer
from treviora_defender.ui.styles import MAIN_STYLE
from treviora_defender.ui.main_window import MainWindow
from treviora_defender.ui.cyber_shield_matrix import DesktopEnergyShieldOverlay

ARTIFACT_DIR = Path(r"C:\Users\Thiruvel\.gemini\antigravity\brain\a84d44c0-3f89-4e98-ae62-15a899da9949")


def capture_all():
    app = QApplication(sys.argv)
    
    # Load fonts for offscreen renderer
    for font_file in ["segoeui.ttf", "segoeuib.ttf", "seguisb.ttf", "seguiemj.ttf", "arial.ttf", "arialbd.ttf"]:
        fp = Path("C:/Windows/Fonts") / font_file
        if fp.exists():
            QFontDatabase.addApplicationFont(str(fp))

    default_font = QFont("Segoe UI", 10)
    app.setFont(default_font)
    app.setStyleSheet(MAIN_STYLE)

    window = MainWindow()
    window.resize(1400, 860)
    window.show()

    def grab(idx: int, filename: str):
        window.switch_view(idx)
        app.processEvents()
        time.sleep(0.12)
        app.processEvents()
        pix = window.grab()
        target = ARTIFACT_DIR / filename
        pix.save(str(target))
        print(f"Captured: {filename} -> {target}")

    # Capture main views
    grab(0, "imanager_dashboard.png")
    grab(1, "imanager_security.png")
    grab(2, "imanager_performance.png")
    grab(3, "imanager_space.png")
    grab(4, "imanager_utilities.png")
    grab(5, "imanager_optimize.png")
    grab(6, "imanager_battery.png")
    grab(7, "imanager_safeguard.png")
    grab(8, "imanager_virus_destroyer.png")

    # Capture Deactivated SafeGuard state
    window.view_safeguard.set_shield_active(False)
    grab(7, "imanager_safeguard_deactivated.png")
    window.view_safeguard.set_shield_active(True)

    # Capture Desktop Energy Shield Screen HUD
    overlay = DesktopEnergyShieldOverlay(is_active=True)
    overlay.resize(1280, 800)
    overlay.show()
    app.processEvents()
    time.sleep(0.12)
    app.processEvents()
    pix_overlay = overlay.grab()
    pix_overlay.save(str(ARTIFACT_DIR / "imanager_desktop_energy_shield.png"))
    print("Captured: imanager_desktop_energy_shield.png")
    overlay.close()

    window.stop_monitors()
    print("All screenshots successfully captured with crystal-clear fonts!")


if __name__ == "__main__":
    capture_all()
