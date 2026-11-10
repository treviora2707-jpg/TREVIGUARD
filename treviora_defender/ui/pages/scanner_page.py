"""
TREVIORA AI DEFENDER - Page 2: Antivirus Scanner
Executes Quick Scan, Full System Scan, Custom Folder Scan, USB Drive Scan, and Download Folder Scan.
Runs real file-by-file scanning in background QThread with live progress reporting.
"""
import os
import time
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFileDialog, QMessageBox, QDialog, QTextEdit
)
from PySide6.QtCore import Qt, QThread, Signal
from treviora_defender.core.scanner import AntivirusScanner, ScanResult
from treviora_defender.quarantine.quarantine_manager import QuarantineManager
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.ui.components.scan_progress import ScanProgressWidget
from treviora_defender.ui.components.threat_table import ThreatTableWidget


class ScanWorker(QThread):
    progress_signal = Signal(str, int, int, int) # (file_path, scanned, threats, speed)
    threat_found_signal = Signal(dict)
    finished_signal = Signal(int, int, float) # (scanned, threats, duration)

    def __init__(self, scanner: AntivirusScanner, targets: list, scan_type: str):
        super().__init__()
        self.scanner = scanner
        self.targets = targets
        self.scan_type = scan_type
        self.db = DatabaseManager()

    def run(self):
        scan_id = self.db.log_scan_start(self.scan_type, ", ".join(self.targets[:2]))
        start_time = time.time()
        last_emit_time = 0
        scanned = 0
        threats = 0

        for res in self.scanner.scan_path_generator(self.targets):
            scanned += 1
            now = time.time()
            if res.is_threat:
                threats += 1
                threat_dict = {
                    "threat_name": res.threat_name,
                    "category": res.category,
                    "severity": res.severity,
                    "risk_score": int(res.risk_score),
                    "file_path": res.file_path,
                    "detection_method": res.detection_method,
                    "ai_explanation": res.ai_explanation
                }
                self.threat_found_signal.emit(threat_dict)

            elapsed = max(now - start_time, 0.001)
            speed = int(scanned / elapsed)

            # Throttle UI signals to every 80ms (avoids flooding Qt event loop and eliminates GUI lag)
            if (now - last_emit_time) >= 0.08 or res.is_threat:
                self.progress_signal.emit(res.file_path, scanned, threats, speed)
                last_emit_time = now

        duration = time.time() - start_time
        status = "Cancelled" if self.scanner.is_cancelled() else "Completed"
        self.db.log_scan_end(scan_id, scanned, threats, duration, status)
        self.finished_signal.emit(scanned, threats, duration)


class ScannerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.scanner = AntivirusScanner()
        self.quarantine_mgr = QuarantineManager()
        self.db = DatabaseManager()
        self.worker = None
        self.found_threats = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # Title
        title_row = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Antivirus Threat Scanner")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Multi-engine detection: Hash DB • YARA Signatures • ONNX AI Model • PE Analysis")
        sub.setProperty("class", "PageSubtitle")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        title_row.addLayout(title_box)
        title_row.addStretch()

        self.btn_cancel = QPushButton("⏹ Cancel Scan")
        self.btn_cancel.setProperty("class", "DangerButton")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self.cancel_scan)
        title_row.addWidget(self.btn_cancel)
        layout.addLayout(title_row)

        # Scan Type Selector Buttons
        btn_bar = QFrame()
        btn_bar.setProperty("class", "GlassCard")
        btn_layout = QHBoxLayout(btn_bar)
        btn_layout.setContentsMargins(14, 12, 14, 12)
        btn_layout.setSpacing(12)

        self.b_quick = QPushButton("⚡ Quick Scan")
        self.b_quick.setProperty("class", "PrimaryButton")
        self.b_quick.clicked.connect(self.start_quick_scan)

        self.b_full = QPushButton("🛡️ Full System")
        self.b_full.setProperty("class", "SecondaryButton")
        self.b_full.clicked.connect(self.start_full_scan)

        self.b_custom = QPushButton("📁 Custom Folder...")
        self.b_custom.setProperty("class", "SecondaryButton")
        self.b_custom.clicked.connect(self.start_custom_scan)

        self.b_usb = QPushButton("💾 USB Drive")
        self.b_usb.setProperty("class", "SecondaryButton")
        self.b_usb.clicked.connect(self.start_usb_scan)

        self.b_downloads = QPushButton("📥 Downloads")
        self.b_downloads.setProperty("class", "SecondaryButton")
        self.b_downloads.clicked.connect(self.start_downloads_scan)

        self.b_forensics = QPushButton("🔬 Inspect File Forensics...")
        self.b_forensics.setProperty("class", "SecondaryButton")
        self.b_forensics.clicked.connect(self.start_forensics_inspect)

        for b in [self.b_quick, self.b_full, self.b_custom, self.b_usb, self.b_downloads, self.b_forensics]:
            btn_layout.addWidget(b)
        layout.addWidget(btn_bar)

        # Animated Progress Widget
        self.progress_widget = ScanProgressWidget()
        layout.addWidget(self.progress_widget)

        # Threat Results Section
        results_header = QLabel("Detected Threat Analysis")
        results_header.setProperty("class", "CardTitle")
        layout.addWidget(results_header)

        self.table = ThreatTableWidget(action_callback=self.handle_table_action)
        layout.addWidget(self.table)

    def start_quick_scan(self):
        targets = self.scanner.get_quick_scan_targets()
        self._launch_scan("Quick Scan", targets)

    def start_full_scan(self):
        targets = self.scanner.get_full_scan_targets()
        self._launch_scan("Full System Scan", targets)

    def start_custom_scan(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan", "D:\\")
        if folder:
            self._launch_scan("Custom Scan", [folder])

    def start_usb_scan(self):
        drives = self.scanner.get_usb_scan_targets()
        if not drives:
            QMessageBox.information(self, "USB Scan", "No removable USB storage devices currently detected.")
            return
        self._launch_scan("USB Scan", drives)

    def start_downloads_scan(self):
        targets = self.scanner.get_download_scan_targets()
        if not targets:
            QMessageBox.warning(self, "Scan Error", "Downloads folder not found.")
            return
        self._launch_scan("Downloads Scan", targets)

    def start_forensics_inspect(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Binary or Executable to Inspect Forensics", "D:\\",
            "Executables & Binaries (*.exe *.dll *.sys *.bin *.scr);;All Files (*.*)"
        )
        if file_path:
            from treviora_defender.ui.components.pe_inspector_dialog import PEInspectorDialog
            diag = PEInspectorDialog(file_path, parent=self)
            diag.exec()

    def _launch_scan(self, scan_type: str, targets: list):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Scan Active", "A scan is already in progress. Please cancel it first.")
            return

        self.found_threats.clear()
        self.table.populate_threats([])
        self.btn_cancel.setEnabled(True)
        self.progress_widget.status_title.setText(f"{scan_type} in Progress...")
        self.progress_widget.progress_bar.setRange(0, 0)

        self.worker = ScanWorker(self.scanner, targets, scan_type)
        self.worker.progress_signal.connect(self.progress_widget.update_progress)
        self.worker.threat_found_signal.connect(self._on_threat_found)
        self.worker.finished_signal.connect(self._on_scan_finished)
        self.worker.start()

    def _on_threat_found(self, threat_dict: dict):
        self.found_threats.append(threat_dict)
        self.table.populate_threats(self.found_threats)

    def _on_scan_finished(self, scanned: int, threats: int, duration: float):
        self.btn_cancel.setEnabled(False)
        self.progress_widget.set_completed(scanned, threats, duration)
        if threats > 0:
            QMessageBox.warning(
                self, "Threats Detected",
                f"Scan finished with {threats} detected threat(s).\nReview and isolate them in the table below."
            )
        else:
            QMessageBox.information(
                self, "Scan Clean",
                f"Scan finished! All {scanned:,} files inspected are clean."
            )

    def cancel_scan(self):
        if self.worker and self.worker.isRunning():
            self.scanner.request_cancel()
            self.btn_cancel.setEnabled(False)

    def handle_table_action(self, action: str, threat: dict):
        if action == "quarantine":
            reply = QMessageBox.question(
                self, "Confirm Quarantine",
                f"Are you sure you want to securely isolate:\n'{threat['file_path']}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                res = self.quarantine_mgr.quarantine_file(threat["file_path"], threat["threat_name"])
                if res["success"]:
                    QMessageBox.information(self, "Quarantine Success", "File was encrypted and isolated safely in Quarantine.")
                    # Remove from list
                    self.found_threats = [t for t in self.found_threats if t["file_path"] != threat["file_path"]]
                    self.table.populate_threats(self.found_threats)
                else:
                    QMessageBox.critical(self, "Quarantine Failed", res.get("error", "Unknown error"))

        elif action == "explain":
            f_path = threat.get("file_path", "")
            if os.path.exists(f_path):
                from treviora_defender.ui.components.pe_inspector_dialog import PEInspectorDialog
                diag = PEInspectorDialog(f_path, parent=self)
                diag.exec()
            else:
                diag = QDialog(self)
                diag.setWindowTitle("AI Threat Explanation")
                diag.resize(550, 400)
                d_layout = QVBoxLayout(diag)

                lbl = QLabel(f"Threat: {threat['threat_name']} (Risk Score: {threat.get('risk_score', 0)}%)")
                lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #00D2FF;")
                d_layout.addWidget(lbl)

                txt = QTextEdit()
                txt.setReadOnly(True)
                txt.setText(threat.get("ai_explanation", "No detailed breakdown available."))
                d_layout.addWidget(txt)

                close_btn = QPushButton("Close")
                close_btn.setProperty("class", "SecondaryButton")
                close_btn.clicked.connect(diag.accept)
                d_layout.addWidget(close_btn)
                diag.exec()
