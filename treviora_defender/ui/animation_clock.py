"""
TREVIORA AI DEFENDER - Unified Animation Clock
Replaces multiple independent 60 FPS QTimers with ONE single centralized clock.
Fires at a calm 30 FPS (33ms).
Cuts Python GIL contention and idle CPU usage to near 0%.
"""
from PySide6.QtCore import QObject, QTimer, Signal


class SharedAnimationClock(QObject):
    _instance = None
    tick = Signal()

    @classmethod
    def get_clock(cls):
        if cls._instance is None:
            cls._instance = SharedAnimationClock()
        return cls._instance

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick.emit)
        # 40ms = 25 FPS, completely fluid cyber UI animations with near-zero CPU footprint
        self.timer.start(40)

    def pause(self):
        if self.timer.isActive():
            self.timer.stop()

    def resume(self):
        if not self.timer.isActive():
            self.timer.start(40)
