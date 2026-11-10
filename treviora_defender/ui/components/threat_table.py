"""
TREVIORA AI DEFENDER - Threat Table Component
Interactive Dark Cyber Table with severity badges and action buttons.
"""
from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QWidget,
    QHBoxLayout, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


class ThreatTableWidget(QTableWidget):
    def __init__(self, action_callback=None):
        super().__init__()
        self.action_callback = action_callback
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels([
            "Threat Name", "Category", "Severity", "Risk Score", "File Path", "Actions"
        ])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)

    def populate_threats(self, threats: list):
        self.setRowCount(0)
        for row_idx, threat in enumerate(threats):
            self.insertRow(row_idx)

            # Name
            name_item = QTableWidgetItem(threat.get("threat_name", "Unknown"))
            name_item.setForeground(QColor("#FFFFFF"))
            self.setItem(row_idx, 0, name_item)

            # Category
            cat_item = QTableWidgetItem(threat.get("category", "General"))
            cat_item.setForeground(QColor("#94A3B8"))
            self.setItem(row_idx, 1, cat_item)

            # Severity badge
            sev = threat.get("severity", "Medium")
            sev_item = QTableWidgetItem(sev)
            if sev in ["Critical", "High"]:
                sev_item.setForeground(QColor("#EF4444"))
            elif sev == "Medium":
                sev_item.setForeground(QColor("#F59E0B"))
            else:
                sev_item.setForeground(QColor("#10B981"))
            self.setItem(row_idx, 2, sev_item)

            # Risk Score
            score = threat.get("risk_score", 0)
            score_item = QTableWidgetItem(f"{score}%")
            score_item.setTextAlignment(Qt.AlignCenter)
            score_item.setForeground(QColor("#00D2FF"))
            self.setItem(row_idx, 3, score_item)

            # File Path
            path_item = QTableWidgetItem(threat.get("file_path", ""))
            path_item.setToolTip(threat.get("file_path", ""))
            self.setItem(row_idx, 4, path_item)

            # Action Buttons
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(4, 2, 4, 2)
            btn_layout.setSpacing(6)

            quar_btn = QPushButton("Quarantine")
            quar_btn.setProperty("class", "DangerButton")
            quar_btn.setFixedHeight(26)
            quar_btn.clicked.connect(lambda _, t=threat: self._on_action("quarantine", t))

            info_btn = QPushButton("Explain AI")
            info_btn.setProperty("class", "SecondaryButton")
            info_btn.setFixedHeight(26)
            info_btn.clicked.connect(lambda _, t=threat: self._on_action("explain", t))

            btn_layout.addWidget(quar_btn)
            btn_layout.addWidget(info_btn)
            self.setCellWidget(row_idx, 5, btn_container)

    def _on_action(self, action_type: str, threat: dict):
        if self.action_callback:
            self.action_callback(action_type, threat)
