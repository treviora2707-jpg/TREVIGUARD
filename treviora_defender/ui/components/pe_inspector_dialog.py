"""
TREVIORA AI DEFENDER - Deep PE Malware Forensic Inspector Dialog
Interactive visual static analysis tool inspecting:
- PE Header characteristics (x64/x86, subsystem, timestamp)
- Section entropy distribution with visual bars
- Suspicious imports mapped to MITRE ATT&CK tactics
- Authenticode signature integrity
- Cryptographic hashes (MD5, SHA1, SHA256)
- AI Threat Assessment
"""
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QScrollArea, QWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from treviora_defender.core.hash_analyzer import HashAnalyzer
from treviora_defender.core.signature_verifier import SignatureVerifier
from treviora_defender.core.ai_engine import AIEngine
from treviora_defender.utils.pe_extractor import extract_pe_features
from treviora_defender.quarantine.quarantine_manager import QuarantineManager


class PEInspectorDialog(QDialog):
    def __init__(self, file_path: str, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.quarantine_mgr = QuarantineManager()
        self.setWindowTitle(f"Treviora Threat Forensics - {Path(file_path).name}")
        self.resize(880, 720)
        self.setMinimumSize(780, 600)
        self._init_ui()
        self._analyze()

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: #0B0F19;")

        container = QWidget()
        container.setStyleSheet("background-color: #0B0F19;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(16)

        # Header Title
        title_box = QHBoxLayout()
        h_title = QLabel("PE Binary Forensic Analysis")
        h_title.setProperty("class", "PageTitle")
        title_box.addWidget(h_title)
        title_box.addStretch()

        self.btn_quarantine = QPushButton("⚠️ Quarantine File")
        self.btn_quarantine.setProperty("class", "DangerButton")
        self.btn_quarantine.clicked.connect(self._do_quarantine)
        title_box.addWidget(self.btn_quarantine)

        btn_close = QPushButton("Close")
        btn_close.setProperty("class", "SecondaryButton")
        btn_close.clicked.connect(self.accept)
        title_box.addWidget(btn_close)

        self.layout.addLayout(title_box)

        # File Overview Card
        self.overview_frame = QFrame()
        self.overview_frame.setProperty("class", "GlassCard")
        self.ov_layout = QVBoxLayout(self.overview_frame)
        self.ov_layout.setContentsMargins(18, 14, 18, 14)
        self.ov_layout.setSpacing(6)
        self.layout.addWidget(self.overview_frame)

        # AI Threat Score Frame
        self.ai_frame = QFrame()
        self.ai_frame.setProperty("class", "GlassCardHighlight")
        self.ai_layout = QVBoxLayout(self.ai_frame)
        self.ai_layout.setContentsMargins(18, 14, 18, 14)
        self.layout.addWidget(self.ai_frame)

        # Sections Table
        sec_label = QLabel("PE Sections & Shannon Entropy Distribution")
        sec_label.setProperty("class", "CardTitle")
        self.layout.addWidget(sec_label)

        self.sections_table = QTableWidget()
        self.sections_table.setColumnCount(5)
        self.sections_table.setHorizontalHeaderLabels([
            "Section Name", "Virtual Size", "Raw Size", "Entropy (0-8)", "Characteristics"
        ])
        self.sections_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.sections_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.sections_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.sections_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.sections_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.sections_table.verticalHeader().setVisible(False)
        self.sections_table.setFixedHeight(180)
        self.layout.addWidget(self.sections_table)

        # Suspicious APIs Table
        api_label = QLabel("Suspicious API Imports (Mapped to Threat Tactics)")
        api_label.setProperty("class", "CardTitle")
        self.layout.addWidget(api_label)

        self.api_table = QTableWidget()
        self.api_table.setColumnCount(3)
        self.api_table.setHorizontalHeaderLabels(["MITRE Threat Tactic", "API Function Name", "Threat Severity"])
        self.api_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.api_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.api_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.api_table.verticalHeader().setVisible(False)
        self.api_table.setFixedHeight(180)
        self.layout.addWidget(self.api_table)

        scroll.setWidget(container)
        root_layout.addWidget(scroll)

    def _analyze(self):
        p = Path(self.file_path)
        if not p.exists():
            return

        # 1. Hashes
        hashes = HashAnalyzer.compute_hashes(self.file_path)
        sig = SignatureVerifier.verify(self.file_path)
        pe = extract_pe_features(self.file_path)
        ai_res = AIEngine().analyze_file(self.file_path)

        # Populate Overview
        f_name = QLabel(f"<b>File:</b> {p.name} ({p.stat().st_size:,} bytes)")
        f_path = QLabel(f"<b>Path:</b> <span style='font-family: monospace;'>{p}</span>")
        f_hash = QLabel(f"<b>SHA-256:</b> <span style='font-family: monospace; color: #00D2FF;'>{hashes.get('sha256', 'N/A')}</span>")
        f_sig = QLabel(f"<b>Digital Signature:</b> <span style='color: {'#10B981' if sig['signed'] else '#EF4444'}; font-weight: bold;'>{sig['status']}</span> - {sig['summary']}")

        for w in [f_name, f_path, f_hash, f_sig]:
            w.setTextFormat(Qt.RichText)
            w.setStyleSheet("color: #E2E8F0; font-size: 12px;")
            self.ov_layout.addWidget(w)

        # Populate AI Score
        score = ai_res.get("risk_score", 0.0)
        cls_name = ai_res.get("classification", "Safe")
        color = "#10B981" if score < 30 else ("#F59E0B" if score < 70 else "#EF4444")

        ai_header = QLabel(f"AI Risk Assessment: <span style='color: {color}; font-size: 18px; font-weight: bold;'>{score:.1f}% ({cls_name})</span>")
        ai_header.setTextFormat(Qt.RichText)
        self.ai_layout.addWidget(ai_header)

        ai_desc = QLabel(ai_res.get("ai_summary", "") + "\n\n" + "\n".join([f"• {r}" for r in ai_res.get("reasons", [])]))
        ai_desc.setStyleSheet("color: #94A3B8; font-size: 12px; line-height: 1.4;")
        self.ai_layout.addWidget(ai_desc)

        # Populate Sections
        sections = pe.get("sections", [])
        self.sections_table.setRowCount(0)
        for r, s in enumerate(sections):
            self.sections_table.insertRow(r)
            self.sections_table.setItem(r, 0, QTableWidgetItem(s["name"]))
            self.sections_table.setItem(r, 1, QTableWidgetItem(f"{s['virtual_size']:,}"))
            self.sections_table.setItem(r, 2, QTableWidgetItem(f"{s['raw_size']:,}"))

            # Entropy bar widget
            ent = s["entropy"]
            bar_container = QWidget()
            bar_layout = QHBoxLayout(bar_container)
            bar_layout.setContentsMargins(4, 2, 4, 2)
            p_bar = QProgressBar()
            p_bar.setRange(0, 800)
            p_bar.setValue(int(ent * 100))
            p_bar.setFormat(f"{ent:.2f} / 8.0")
            if ent >= 7.2:
                p_bar.setStyleSheet("QProgressBar::chunk { background-color: #EF4444; }")
            elif ent >= 6.0:
                p_bar.setStyleSheet("QProgressBar::chunk { background-color: #00D2FF; }")
            else:
                p_bar.setStyleSheet("QProgressBar::chunk { background-color: #10B981; }")
            bar_layout.addWidget(p_bar)
            self.sections_table.setCellWidget(r, 3, bar_container)

            chars = "W+X (Suspicious)" if s.get("is_wx") else "Normal"
            c_item = QTableWidgetItem(chars)
            if s.get("is_wx"):
                c_item.setForeground(Qt.red)
            self.sections_table.setItem(r, 4, c_item)

        # Populate Suspicious APIs
        apis = pe.get("suspicious_apis_found", {})
        row = 0
        self.api_table.setRowCount(0)
        for tactic, func_list in apis.items():
            for func in func_list:
                self.api_table.insertRow(row)
                self.api_table.setItem(row, 0, QTableWidgetItem(tactic))
                self.api_table.setItem(row, 1, QTableWidgetItem(func))

                sev = "High" if "Injection" in tactic or "Crypto" in tactic else "Medium"
                s_item = QTableWidgetItem(sev)
                s_item.setForeground(Qt.red if sev == "High" else Qt.yellow)
                self.api_table.setItem(row, 2, s_item)
                row += 1

        if row == 0:
            self.api_table.insertRow(0)
            self.api_table.setItem(0, 0, QTableWidgetItem("None"))
            self.api_table.setItem(0, 1, QTableWidgetItem("No suspicious Windows APIs detected."))
            self.api_table.setItem(0, 2, QTableWidgetItem("Clean"))

    def _do_quarantine(self):
        reply = QMessageBox.question(
            self, "Confirm Quarantine",
            f"Are you sure you want to securely isolate this file to Quarantine:\n'{self.file_path}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            res = self.quarantine_mgr.quarantine_file(self.file_path, "Manual.Forensics.Isolation")
            if res["success"]:
                QMessageBox.information(self, "Quarantined", "File has been encrypted and moved to the Quarantine Vault.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", res.get("error", "Failed"))
