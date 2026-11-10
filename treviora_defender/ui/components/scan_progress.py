"""
TREVIORA AI DEFENDER - Scan Progress Widget
Displays live animated scan progress, file ticker, throughput speed, and threat tally.
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt


class ScanProgressWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "GlassCardHighlight")
        self.setMinimumHeight(150)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # Header: Scan status and Speed
        top_row = QHBoxLayout()
        self.status_title = QLabel("System Scan Active")
        self.status_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #00D2FF;")

        self.speed_label = QLabel("0 files/sec")
        self.speed_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")

        top_row.addWidget(self.status_title)
        top_row.addStretch()
        top_row.addWidget(self.speed_label)
        layout.addLayout(top_row)

        # Current File path ticker
        self.file_label = QLabel("Initializing scanning engine...")
        self.file_label.setStyleSheet("color: #E2E8F0; font-size: 12px; font-family: 'Consolas', monospace;")
        self.file_label.setWordWrap(False)
        layout.addWidget(self.file_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # Indeterminate initially
        layout.addWidget(self.progress_bar)

        # Metrics Footer
        bot_row = QHBoxLayout()
        self.scanned_counter = QLabel("Files Scanned: 0")
        self.scanned_counter.setStyleSheet("color: #94A3B8; font-weight: 600;")

        self.threats_counter = QLabel("Threats Detected: 0")
        self.threats_counter.setStyleSheet("color: #10B981; font-weight: 700;")

        bot_row.addWidget(self.scanned_counter)
        bot_row.addStretch()
        bot_row.addWidget(self.threats_counter)
        layout.addLayout(bot_row)

    def update_progress(self, file_path: str, scanned: int, threats: int, speed: int):
        # Truncate file path display if too long
        display_path = file_path
        if len(display_path) > 75:
            display_path = display_path[:35] + "..." + display_path[-35:]
        self.file_label.setText(display_path)

        self.scanned_counter.setText(f"Files Scanned: {scanned:,}")
        self.speed_label.setText(f"{speed:,} files/sec")

        if threats > 0:
            self.threats_counter.setText(f"Threats Detected: {threats}")
            self.threats_counter.setStyleSheet("color: #EF4444; font-weight: 800;")
        else:
            self.threats_counter.setText("Threats Detected: 0")
            self.threats_counter.setStyleSheet("color: #10B981; font-weight: 700;")

    def set_completed(self, scanned: int, threats: int, duration: float):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.status_title.setText("Scan Completed Successfully")
        self.status_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #10B981;")
        self.file_label.setText(f"Finished inspecting {scanned:,} files in {duration:.1f} seconds.")
        self.speed_label.setText("Idle")
