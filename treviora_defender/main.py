"""
TREVIORA AI DEFENDER - Main Application Entrypoint
Developer: TREVIORA INDUSTRY
Windows 11 Compatible Antivirus & AI Threat Defense System
Primary Architecture: D: Drive Dedicated Environment
"""
import sys
import os
from pathlib import Path

# Ensure package root is in python path
current_dir = Path(__file__).resolve().parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from treviora_defender.config.constants import APP_NAME, BASE_DIR, RESOURCES_DIR
from treviora_defender.ui.styles import MAIN_STYLE
from treviora_defender.ui.main_window import MainWindow
from treviora_defender.utils.logger import get_logger

logger = get_logger()


def main():
    logger.info(f"Starting {APP_NAME}...")
    logger.info(f"Target Working Environment: {BASE_DIR}")

    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("TREVIORA INDUSTRY")
    app.setStyleSheet(MAIN_STYLE)

    icon_path = RESOURCES_DIR / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
