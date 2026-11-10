"""
TREVIORA AI DEFENDER - Page 4: Threat Detection Center
Lists active and resolved threats, provides threat severity metrics,
and allows instant quarantine or XAI threat inspection.
"""
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QDialog, QTextEdit
)
from PySide6.QtCore import Qt
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.quarantine.quarantine_manager import QuarantineManager
from treviora_defender.ui.components.threat_table import ThreatTableWidget


class ThreatPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.quarantine_mgr = QuarantineManager()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # Header
        header_row = QHBoxLayout()
        header = QVBoxLayout()
        title = QLabel("Threat Intelligence & Incident Management")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Review active security detections, AI feature explanations, and containment status")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        header_row.addLayout(header)
        header_row.addStretch()

        btn_refresh = QPushButton("🔄 Refresh Threats")
        btn_refresh.setProperty("class", "SecondaryButton")
        btn_refresh.clicked.connect(self.refresh_threats)
        header_row.addWidget(btn_refresh)
        layout.addLayout(header_row)

        # Threat table
        self.table = ThreatTableWidget(action_callback=self.handle_action)
        layout.addWidget(self.table)

        self.refresh_threats()

    def refresh_threats(self):
        threats = self.db.get_active_threats()
        self.table.populate_threats(threats)

    def handle_action(self, action: str, threat: dict):
        if action == "quarantine":
            reply = QMessageBox.question(
                self, "Quarantine Threat",
                f"Quarantine infected file:\n'{threat['file_path']}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                res = self.quarantine_mgr.quarantine_file(threat["file_path"], threat["threat_name"])
                if res["success"]:
                    self.db.update_threat_status(threat["id"], "Quarantined")
                    QMessageBox.information(self, "Success", "File isolated into encrypted quarantine storage.")
                    self.refresh_threats()
                else:
                    QMessageBox.critical(self, "Quarantine Error", res.get("error", "Failed"))

        elif action == "explain":
            f_path = threat.get("file_path", "")
            if os.path.exists(f_path):
                from treviora_defender.ui.components.pe_inspector_dialog import PEInspectorDialog
                diag = PEInspectorDialog(f_path, parent=self)
                diag.exec()
            else:
                diag = QDialog(self)
                diag.setWindowTitle("AI Threat Forensic Explanation")
                diag.resize(600, 420)
                d_layout = QVBoxLayout(diag)

                lbl = QLabel(f"Threat: {threat['threat_name']} | Risk: {threat.get('risk_score', 0)}%")
                lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #00D2FF;")
                d_layout.addWidget(lbl)

                txt = QTextEdit()
                txt.setReadOnly(True)
                exp = threat.get("ai_explanation", "No detailed breakdown available.")
                txt.setText(f"Detection Method: {threat.get('detection_method', 'Unknown')}\n\n{exp}")
                d_layout.addWidget(txt)

                btn = QPushButton("Close")
                btn.setProperty("class", "SecondaryButton")
                btn.clicked.connect(diag.accept)
                d_layout.addWidget(btn)
                diag.exec()
