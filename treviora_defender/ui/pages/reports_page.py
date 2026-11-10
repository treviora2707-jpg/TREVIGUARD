"""
TREVIORA AI DEFENDER - Page 9: Security Reports & Audits
Logs historical scan sessions, threat summaries, and forensic reports.
Exports reports strictly to D: drive or user-selected destination.
"""
import csv
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from treviora_defender.database.db_manager import DatabaseManager


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # Header
        header_row = QHBoxLayout()
        header = QVBoxLayout()
        title = QLabel("Security Audit Logs & Reports")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Comprehensive forensic audit trails • Historical scan sessions • Exportable reports")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        header_row.addLayout(header)
        header_row.addStretch()

        btn_csv = QPushButton("📥 Export to CSV")
        btn_csv.setProperty("class", "SecondaryButton")
        btn_csv.clicked.connect(self.export_csv)
        header_row.addWidget(btn_csv)

        btn_json = QPushButton("📥 Export to JSON")
        btn_json.setProperty("class", "SecondaryButton")
        btn_json.clicked.connect(self.export_json)
        header_row.addWidget(btn_json)

        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setProperty("class", "SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_reports)
        header_row.addWidget(btn_refresh)

        layout.addLayout(header_row)

        # Reports table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Scan Type", "Target Scope", "Date & Time", "Files Inspected", "Threats Found", "Duration (s)", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

        self.refresh_reports()

    def refresh_reports(self):
        scans = self.db.get_scan_history(limit=50)
        self.table.setRowCount(0)

        for r, s in enumerate(scans):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(s.get("scan_type", "Scan")))
            self.table.setItem(r, 1, QTableWidgetItem(s.get("target_path", "") or "System Target"))

            dt = s.get("start_time", "").replace("T", " ")[:19]
            self.table.setItem(r, 2, QTableWidgetItem(dt))
            self.table.setItem(r, 3, QTableWidgetItem(f"{s.get('files_scanned', 0):,}"))

            threats = s.get("threats_found", 0)
            t_item = QTableWidgetItem(str(threats))
            if threats > 0:
                t_item.setForeground(Qt.red)
            else:
                t_item.setForeground(Qt.green)
            self.table.setItem(r, 4, t_item)

            dur = s.get("duration_seconds", 0.0)
            self.table.setItem(r, 5, QTableWidgetItem(f"{dur:.1f}s"))

            status_item = QTableWidgetItem(s.get("status", "Completed"))
            self.table.setItem(r, 6, status_item)

    def export_csv(self):
        scans = self.db.get_scan_history(limit=500)
        default_path = "D:/projects/antivirus/data/scan_report.csv"
        path, _ = QFileDialog.getSaveFileName(self, "Export Security Audit Log to CSV", default_path, "CSV Files (*.csv)")
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Scan Type", "Target", "Start Time", "End Time", "Files Scanned", "Threats Found", "Duration (s)", "Status"])
                for s in scans:
                    writer.writerow([
                        s.get("id"), s.get("scan_type"), s.get("target_path"),
                        s.get("start_time"), s.get("end_time"), s.get("files_scanned"),
                        s.get("threats_found"), s.get("duration_seconds"), s.get("status")
                    ])
            QMessageBox.information(self, "Export Successful", f"Audit report exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export CSV: {e}")

    def export_json(self):
        scans = self.db.get_scan_history(limit=500)
        default_path = "D:/projects/antivirus/data/scan_report.json"
        path, _ = QFileDialog.getSaveFileName(self, "Export Security Audit Log to JSON", default_path, "JSON Files (*.json)")
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(scans, f, indent=4)
            QMessageBox.information(self, "Export Successful", f"Audit report exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export JSON: {e}")
