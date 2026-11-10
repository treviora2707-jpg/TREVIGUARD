"""
TREVIORA AI DEFENDER - Page 3: Real-Time Protection
Manages live shields: File Protection, Process Shield, Ransomware Guard, USB Sentinel, and Persistence Monitor.
Provides live event telemetry and a safe EICAR test trigger to verify real-time protection.
"""
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt
from treviora_defender.config.settings import SettingsManager
from treviora_defender.database.db_manager import DatabaseManager


class RealtimePage(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.settings = SettingsManager()
        self.db = DatabaseManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        # Header
        header = QVBoxLayout()
        title = QLabel("Real-Time Endpoint Protection")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Continuous active background shields monitoring filesystem, processes, and memory")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        layout.addLayout(header)

        # Active Shields Cards Row
        shields_frame = QFrame()
        shields_frame.setProperty("class", "GlassCard")
        shields_layout = QVBoxLayout(shields_frame)
        shields_layout.setContentsMargins(20, 16, 20, 16)
        shields_layout.setSpacing(14)

        shields_title = QLabel("Configured Security Shields")
        shields_title.setProperty("class", "CardTitle")
        shields_layout.addWidget(shields_title)

        # Shield toggles
        self.chk_file = QCheckBox("File System Shield (Monitors Downloads, Desktop, Temp for new files)")
        self.chk_file.setChecked(self.settings.get("real_time_protection", True))
        self.chk_file.toggled.connect(lambda v: self.settings.set("real_time_protection", v))

        self.chk_proc = QCheckBox("Suspicious Process & Memory Shield (Monitors PowerShell, CertUtil, LolBins)")
        self.chk_proc.setChecked(True)

        self.chk_ransom = QCheckBox("Ransomware Guard & Canary Decoy Monitor (Detects mass encryption velocity)")
        self.chk_ransom.setChecked(self.settings.get("ransomware_protection", True))
        self.chk_ransom.toggled.connect(lambda v: self.settings.set("ransomware_protection", v))

        self.chk_usb = QCheckBox("USB Storage Guardian (Auto-scans connected USB thumb drives)")
        self.chk_usb.setChecked(self.settings.get("usb_auto_scan", True))
        self.chk_usb.toggled.connect(lambda v: self.settings.set("usb_auto_scan", v))

        self.chk_ai = QCheckBox("Machine Learning ONNX Engine (PE header & entropy inference)")
        self.chk_ai.setChecked(self.settings.get("ai_engine_enabled", True))
        self.chk_ai.toggled.connect(lambda v: self.settings.set("ai_engine_enabled", v))

        for chk in [self.chk_file, self.chk_proc, self.chk_ransom, self.chk_usb, self.chk_ai]:
            chk.setStyleSheet("color: #E2E8F0; font-size: 13px; font-weight: 500;")
            shields_layout.addWidget(chk)

        layout.addWidget(shields_frame)

        # Live telemetry table & Test trigger row
        tele_header_row = QHBoxLayout()
        tele_title = QLabel("Live Security Telemetry Feed")
        tele_title.setProperty("class", "CardTitle")
        tele_header_row.addWidget(tele_title)
        tele_header_row.addStretch()

        btn_test_eicar = QPushButton("🧪 Test EICAR Detection Live")
        btn_test_eicar.setProperty("class", "SecondaryButton")
        btn_test_eicar.clicked.connect(self.trigger_eicar_test)
        tele_header_row.addWidget(btn_test_eicar)

        btn_refresh = QPushButton("🔄 Refresh Feed")
        btn_refresh.setProperty("class", "SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_events)
        tele_header_row.addWidget(btn_refresh)

        layout.addLayout(tele_header_row)

        # Events table
        self.events_table = QTableWidget()
        self.events_table.setColumnCount(4)
        self.events_table.setHorizontalHeaderLabels(["Timestamp", "Severity", "Shield Source", "Description"])
        self.events_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.events_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.events_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.events_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.events_table.verticalHeader().setVisible(False)
        layout.addWidget(self.events_table)

        self.refresh_events()

    def refresh_events(self):
        events = self.db.get_recent_events(limit=50)
        self.events_table.setRowCount(0)
        for r, ev in enumerate(events):
            self.events_table.insertRow(r)
            ts = ev.get("timestamp", "").replace("T", " ")[:19]
            self.events_table.setItem(r, 0, QTableWidgetItem(ts))

            sev = ev.get("severity", "Info")
            sev_item = QTableWidgetItem(sev)
            if sev in ["Critical", "High"]:
                sev_item.setForeground(Qt.red)
            elif sev == "Medium":
                sev_item.setForeground(Qt.yellow)
            else:
                sev_item.setForeground(Qt.green)
            self.events_table.setItem(r, 1, sev_item)

            self.events_table.setItem(r, 2, QTableWidgetItem(ev.get("source", "RealTime")))
            self.events_table.setItem(r, 3, QTableWidgetItem(ev.get("description", "")))

    def trigger_eicar_test(self):
        """
        Creates a harmless official EICAR test string on D: drive to verify that
        hash/YARA and real-time detection intercept and quarantine it cleanly.
        """
        eicar_string = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
        test_file = Path("D:/projects/antivirus/data/test_eicar.com")

        try:
            with open(test_file, "w") as f:
                f.write(eicar_string)

            QMessageBox.information(
                self, "EICAR Test Created",
                f"Generated harmless EICAR test file at:\n'{test_file}'.\n"
                "Watch the Real-Time Telemetry or run a Quick Scan to verify interception."
            )
            self.refresh_events()
        except Exception as e:
            QMessageBox.critical(self, "Test Error", f"Could not create test file: {e}")
