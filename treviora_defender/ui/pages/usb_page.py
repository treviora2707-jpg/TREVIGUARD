"""
TREVIORA AI DEFENDER - Page 8: USB Protection
Monitors removable media, scans root files for autorun / shortcut worms,
and generates USB security reports.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from treviora_defender.config.settings import SettingsManager
from treviora_defender.utils.win_utils import get_removable_drives
from treviora_defender.monitoring.usb_monitor import USBMonitor


class USBPage(QWidget):
    request_usb_scan = Signal(str)

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # Header
        header_row = QHBoxLayout()
        header = QVBoxLayout()
        title = QLabel("USB Storage & Removable Media Sentinel")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Automatic insertion detection • Shortcut worm prevention • Autorun.inf lockdown")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        header_row.addLayout(header)
        header_row.addStretch()

        btn_refresh = QPushButton("🔄 Scan Hardware Buses")
        btn_refresh.setProperty("class", "SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_drives)
        header_row.addWidget(btn_refresh)
        layout.addLayout(header_row)

        # Control Bar
        ctrl_frame = QFrame()
        ctrl_frame.setProperty("class", "GlassCard")
        ctrl_layout = QHBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(18, 14, 18, 14)

        self.chk_auto = QCheckBox("Automatically Initiate Scan Upon USB Insertion")
        self.chk_auto.setChecked(self.settings.get("usb_auto_scan", True))
        self.chk_auto.setStyleSheet("color: #E2E8F0; font-weight: 600;")
        self.chk_auto.toggled.connect(lambda v: self.settings.set("usb_auto_scan", v))
        ctrl_layout.addWidget(self.chk_auto)
        ctrl_layout.addStretch()

        layout.addWidget(ctrl_frame)

        # Removable Drives Table
        tbl_label = QLabel("Connected Removable Storage Volumes")
        tbl_label.setProperty("class", "CardTitle")
        layout.addWidget(tbl_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Drive Letter", "Integrity Status", "Artifacts Detected", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.refresh_drives()

    def refresh_drives(self):
        drives = get_removable_drives()
        self.table.setRowCount(0)

        if not drives:
            self.table.insertRow(0)
            self.table.setItem(0, 0, QTableWidgetItem("None"))
            self.table.setItem(0, 1, QTableWidgetItem("No USB Drives Connected"))
            self.table.setItem(0, 2, QTableWidgetItem("Connect a USB flash drive or external drive to inspect."))
            self.table.setItem(0, 3, QTableWidgetItem("-"))
            return

        for r, d in enumerate(drives):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(d))

            insp = USBMonitor.inspect_usb_drive(d)
            if insp["is_suspicious"]:
                status_item = QTableWidgetItem("⚠️ Artifacts Found")
                status_item.setForeground(Qt.yellow)
                art_item = QTableWidgetItem("; ".join(insp["artifacts"]))
                art_item.setForeground(Qt.red)
            else:
                status_item = QTableWidgetItem("🟢 Clean Root")
                status_item.setForeground(Qt.green)
                art_item = QTableWidgetItem("No suspicious autorun or hidden executables on root.")

            self.table.setItem(r, 1, status_item)
            self.table.setItem(r, 2, art_item)

            btn_scan = QPushButton("Deep Scan Drive")
            btn_scan.setProperty("class", "PrimaryButton")
            btn_scan.setFixedHeight(26)
            btn_scan.clicked.connect(lambda _, drv=d: self.request_usb_scan.emit(drv))
            self.table.setCellWidget(r, 3, btn_scan)
