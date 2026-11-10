"""
TREVIORA AI DEFENDER - Page 7: Network Security Monitoring
Monitors active TCP/UDP sockets, flags suspicious outbound connections,
and audits Windows Defender Firewall integrity.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from treviora_defender.monitoring.network_monitor import NetworkMonitor
from treviora_defender.monitoring.process_monitor import ProcessMonitor


class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        self.net_mon = NetworkMonitor()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # Header
        header_row = QHBoxLayout()
        header = QVBoxLayout()
        title = QLabel("Network Security & Socket Telemetry")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Active network socket mapping • Outbound C2 detection • Windows Firewall audit")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        header_row.addLayout(header)
        header_row.addStretch()

        self.chk_suspicious_only = QCheckBox("Filter Suspicious Only")
        self.chk_suspicious_only.setStyleSheet("color: #E2E8F0; font-weight: 600;")
        self.chk_suspicious_only.toggled.connect(self.refresh_connections)
        header_row.addWidget(self.chk_suspicious_only)

        btn_refresh = QPushButton("🔄 Refresh Sockets")
        btn_refresh.setProperty("class", "SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_connections)
        header_row.addWidget(btn_refresh)
        layout.addLayout(header_row)

        # Windows Firewall Status Bar
        fw_status = self.net_mon.get_firewall_status()
        fw_frame = QFrame()
        fw_frame.setProperty("class", "GlassCard")
        fw_layout = QHBoxLayout(fw_frame)
        fw_layout.setContentsMargins(16, 12, 16, 12)

        fw_label = QLabel("🛡️ Windows Defender Firewall:")
        fw_label.setStyleSheet("font-weight: bold; color: #94A3B8;")

        fw_val = QLabel("ACTIVE & FILTERING TRAFFIC" if fw_status.get("firewall_active") else "PROFILES MONITORED")
        fw_val.setStyleSheet("color: #10B981; font-weight: 800;" if fw_status.get("firewall_active") else "color: #38BDF8; font-weight: 700;")

        fw_layout.addWidget(fw_label)
        fw_layout.addWidget(fw_val)
        fw_layout.addStretch()

        note_label = QLabel("Safe Integration: Firewall policies respected without unconfirmed changes")
        note_label.setStyleSheet("color: #64748B; font-size: 11px;")
        fw_layout.addWidget(note_label)

        layout.addWidget(fw_frame)

        # Connections Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "PID", "Process Name", "Protocol", "Local Address", "Remote Endpoint", "State", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.refresh_connections()

    def refresh_connections(self):
        susp_only = self.chk_suspicious_only.isChecked()
        conns = self.net_mon.get_active_connections(filter_suspicious_only=susp_only)
        self.table.setRowCount(0)

        for r, c in enumerate(conns[:120]): # Display up to 120 sockets
            self.table.insertRow(r)

            # PID
            pid_item = QTableWidgetItem(str(c["pid"]))
            self.table.setItem(r, 0, pid_item)

            # Process Name
            name_item = QTableWidgetItem(c["process_name"])
            if c["is_suspicious"]:
                name_item.setForeground(Qt.red)
            self.table.setItem(r, 1, name_item)

            # Protocol
            self.table.setItem(r, 2, QTableWidgetItem(c["protocol"]))

            # Local Address
            self.table.setItem(r, 3, QTableWidgetItem(c["local_address"]))

            # Remote Address
            r_item = QTableWidgetItem(c["remote_address"])
            if c["is_suspicious"]:
                r_item.setForeground(Qt.red)
                r_item.setToolTip(c["reason"])
            self.table.setItem(r, 4, r_item)

            # State
            self.table.setItem(r, 5, QTableWidgetItem(c["status"]))

            # Action button
            btn_kill = QPushButton("End Process")
            btn_kill.setProperty("class", "SecondaryButton")
            btn_kill.setFixedHeight(24)
            btn_kill.clicked.connect(lambda _, pid=c["pid"], name=c["process_name"]: self.terminate_proc(pid, name))
            self.table.setCellWidget(r, 6, btn_kill)

    def terminate_proc(self, pid: int, name: str):
        reply = QMessageBox.question(
            self, "Confirm Process Termination",
            f"Are you sure you want to end process '{name}' (PID: {pid})?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            res = ProcessMonitor.terminate_process(pid)
            if res["success"]:
                QMessageBox.information(self, "Process Terminated", res["message"])
                self.refresh_connections()
            else:
                QMessageBox.critical(self, "Termination Error", res["message"])
