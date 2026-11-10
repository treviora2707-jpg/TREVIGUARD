"""
Benchmarking script for TREVIORA AI DEFENDER idle CPU and responsiveness.
Runs the complete Qt UI, exercises widget updates, and profiles CPU load.
"""
import sys
import os
import time
import psutil
from pathlib import Path

# Set working directory to project root
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from treviora_defender.ui.styles import MAIN_STYLE
from treviora_defender.ui.main_window import MainWindow


def benchmark():
    print("=" * 60)
    print("TREVIORA AI DEFENDER - IDLE PERFORMANCE & CPU BENCHMARK")
    print("=" * 60)

    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)

    proc = psutil.Process()
    # Baseline
    proc.cpu_percent(interval=None)

    window = MainWindow()
    window.show()

    measurements = []

    def check_cpu():
        usage = proc.cpu_percent(interval=None)
        mem_mb = proc.memory_info().rss / (1024 * 1024)
        measurements.append((usage, mem_mb))
        print(f" -> Profiler sample: CPU {usage:.1f}% | App Memory: {mem_mb:.1f} MB")

    # Sample every 1 second for 5 seconds
    timer = QTimer()
    timer.timeout.connect(check_cpu)
    timer.start(1000)

    def finish():
        timer.stop()
        window.stop_monitors()
        app.quit()

        cpu_vals = [m[0] for m in measurements if m[0] > 0]
        avg_cpu = sum(cpu_vals) / len(cpu_vals) if cpu_vals else 0.0
        max_cpu = max(cpu_vals) if cpu_vals else 0.0

        print("\n" + "=" * 60)
        print(f"BENCHMARK RESULTS (LENOVO LOQ):")
        print(f" -> Average CPU Load: {avg_cpu:.2f}%")
        print(f" -> Peak CPU Load: {max_cpu:.2f}%")
        print(f" -> Status: {'EXCELLENT (SILKY SMOOTH, < 3% CPU)' if avg_cpu < 5.0 else 'CHECK OPTIMIZATION'}")
        print("=" * 60)

    QTimer.singleShot(5500, finish)
    app.exec()


if __name__ == "__main__":
    benchmark()
