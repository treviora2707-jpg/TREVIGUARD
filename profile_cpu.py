"""
Profile function CPU time in TREVIORA AI DEFENDER to find exact hotspots.
"""
import sys
import os
import cProfile
import pstats
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from treviora_defender.ui.styles import MAIN_STYLE
from treviora_defender.ui.main_window import MainWindow


def profile_run():
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)

    window = MainWindow()
    window.show()

    def finish():
        window.stop_monitors()
        app.quit()

    QTimer.singleShot(3000, finish)
    app.exec()


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    profile_run()
    pr.disable()

    ps = pstats.Stats(pr).sort_stats('cumtime')
    print("=" * 60)
    print("TOP 30 CPU CONSUMING FUNCTIONS:")
    print("=" * 60)
    ps.print_stats(30)
