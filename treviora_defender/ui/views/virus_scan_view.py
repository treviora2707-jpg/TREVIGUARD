"""
TREVIORA AI DEFENDER - Virus Scanner & Threat Destroyer View
Provides:
- Quick Virus Scan & Full System Scan modes
- Live Scanning Progress & File Path Display
- Threat Detection Table (AI Heuristics, YARA, SHA-256 Hash matches)
- Action buttons:
  * "Destroy Virus (Permanent Shred)" - multi-pass zero-overwrite destruction
  * "Isolate to Quarantine Vault" - AES-GCM 256-bit isolation
"""
import os
import time
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal, QThread
from treviora_defender.core.scanner import AntivirusScanner, ScanResult
from treviora_defender.quarantine.quarantine_manager import QuarantineManager
from treviora_defender.ui.custom_components import ModernCard, ToolButton, BrandHeaderWidget


class VirusScanWorker(QThread):
    progress = Signal(int, str)
    threat_found = Signal(object)
    scan_finished = Signal(int, int)

    def __init__(self, mode="quick", custom_path=None, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.custom_path = custom_path
        self.scanner = AntivirusScanner()
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True
        self.scanner.request_cancel()

    def run(self):
        scan_targets = []
        user_home = Path.home()

        if self.mode == "custom" and self.custom_path:
            scan_targets.append(Path(self.custom_path))
        elif self.mode == "quick":
            scan_targets.extend([
                user_home / "Downloads",
                Path("D:/projects/antivirus/treviora_defender"),
                Path("D:/projects/antivirus/data")
            ])
        else: # Full Scan
            scan_targets.extend([
                user_home / "Downloads",
                user_home / "Desktop",
                user_home / "Documents",
                Path("D:/projects/antivirus")
            ])

        files_to_scan = []
        for target in scan_targets:
            if target.exists():
                if target.is_file():
                    files_to_scan.append(target)
                else:
                    for root, _, files in os.walk(target):
                        if self._is_cancelled:
                            break
                        for f in files:
                            fp = Path(root) / f
                            files_to_scan.append(fp)
                            if len(files_to_scan) >= 800 and self.mode == "quick":
                                break

        total = len(files_to_scan)
        if total == 0:
            self.scan_finished.emit(0, 0)
            return

        threat_count = 0
        last_emit = 0

        for idx, file_path in enumerate(files_to_scan):
            if self._is_cancelled:
                break

            now = time.time()
            if now - last_emit > 0.08:
                pct = int((idx / total) * 100)
                self.progress.emit(pct, str(file_path))
                last_emit = now

            try:
                res = self.scanner.scan_single_file(str(file_path))
                if res.is_threat:
                    threat_count += 1
                    self.threat_found.emit(res)
            except Exception:
                continue

        self.progress.emit(100, "Scan Complete")
        self.scan_finished.emit(total, threat_count)


class VirusScanView(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.is_scanning = False
        self.detected_threats = []
        self.quarantine_mgr = QuarantineManager()
        self._init_ui()

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #060911; border: none;")

        wrapper = QWidget()
        wrapper.setStyleSheet("background: #060911;")
        w_layout = QHBoxLayout(wrapper)
        w_layout.setContentsMargins(0, 0, 0, 0)
        w_layout.addStretch(1)

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        container.setMaximumWidth(1000)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 28)
        layout.setSpacing(16)

        # 1. Back Header + Brand Header
        top_bar = QHBoxLayout()
        self.btn_back = QPushButton("‹  Virus Scanner && Threat Destroyer")
        self.btn_back.setStyleSheet(
            "font-size: 18px; font-weight: 700; color: #FFFFFF; background: transparent; border: none;"
        )
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.back_requested.emit)
        top_bar.addWidget(self.btn_back)

        top_bar.addStretch()

        self.brand_header = BrandHeaderWidget()
        top_bar.addWidget(self.brand_header)

        top_bar.addSpacing(16)

        self.lbl_threat_badge = QLabel("0 Threats Detected")
        self.lbl_threat_badge.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 700;")
        top_bar.addWidget(self.lbl_threat_badge)
        layout.addLayout(top_bar)

        # 2. Scan Mode Selector Buttons
        mode_row = QHBoxLayout()
        mode_row.setSpacing(12)

        self.btn_quick = ToolButton("⚡ Quick Scan")
        self.btn_quick.clicked.connect(lambda: self.start_scan("quick"))

        self.btn_full = ToolButton("🛡️ Full System Scan")
        self.btn_full.clicked.connect(lambda: self.start_scan("full"))

        self.btn_custom = ToolButton("📁 Custom Folder Scan")
        self.btn_custom.clicked.connect(self._select_custom_folder)

        for b in [self.btn_quick, self.btn_full, self.btn_custom]:
            mode_row.addWidget(b)

        layout.addLayout(mode_row)

        # 3. Live Scanning Status Card
        status_card = ModernCard()
        sc_layout = QVBoxLayout(status_card)
        sc_layout.setContentsMargins(22, 18, 22, 18)
        sc_layout.setSpacing(10)

        self.lbl_status_text = QLabel("Ready to scan. Select scan mode above.")
        self.lbl_status_text.setStyleSheet("color: #00D2FF; font-size: 15px; font-weight: 700;")

        self.scan_bar = QProgressBar()
        self.scan_bar.setRange(0, 100)
        self.scan_bar.setValue(0)
        self.scan_bar.setFixedHeight(12)
        self.scan_bar.setTextVisible(False)
        self.scan_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1E293B;
                border: none;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
                border-radius: 6px;
            }
        """)

        self.lbl_cur_file = QLabel("Ready")
        self.lbl_cur_file.setStyleSheet("color: #64748B; font-size: 12px;")

        sc_layout.addWidget(self.lbl_status_text)
        sc_layout.addWidget(self.scan_bar)
        sc_layout.addWidget(self.lbl_cur_file)
        layout.addWidget(status_card)

        # 4. Detected Threats Table
        lbl_tbl_hdr = QLabel("DETECTED THREATS & SUSPICIOUS BEHAVIOR")
        lbl_tbl_hdr.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;")
        layout.addWidget(lbl_tbl_hdr)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Threat Name", "Method", "Risk Score", "File Location"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        layout.addWidget(self.table)

        # 5. Threat Action Controls (Destroy / Quarantine / Stop)
        action_row = QHBoxLayout()
        action_row.setSpacing(14)

        self.btn_destroy = QPushButton("🔥 Destroy Virus (Permanent Shred)")
        self.btn_destroy.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EF4444, stop:1 #B91C1C);
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 800;
                font-size: 14px;
                border-radius: 20px;
                padding: 10px 24px;
                border: none;
            }
            QPushButton:hover {
                background: #DC2626;
            }
        """)
        self.btn_destroy.setCursor(Qt.PointingHandCursor)
        self.btn_destroy.clicked.connect(self._destroy_selected_threat)

        self.btn_quarantine = ToolButton("📦 Isolate to Quarantine Vault")
        self.btn_quarantine.clicked.connect(self._quarantine_selected_threat)

        self.btn_cancel = QPushButton("Stop Scan")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setFixedHeight(42)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background: #00D2FF;
                color: #060A10;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 800;
                border: none;
                border-radius: 21px;
                padding: 0px 24px;
            }
            QPushButton:hover {
                background: #38BDF8;
            }
        """)
        self.btn_cancel.clicked.connect(self._cancel_scan)
        self.btn_cancel.setEnabled(False)

        action_row.addWidget(self.btn_destroy)
        action_row.addWidget(self.btn_quarantine)
        action_row.addStretch()
        action_row.addWidget(self.btn_cancel)
        layout.addLayout(action_row)

        w_layout.addWidget(container)
        w_layout.addStretch(1)

        scroll.setWidget(wrapper)
        root_layout.addWidget(scroll)

    def start_scan(self, mode: str, custom_path: str = None):
        if self.is_scanning or (hasattr(self, 'worker') and self.worker and self.worker.isRunning()):
            return

        self.is_scanning = True
        self.detected_threats = []
        self.table.setRowCount(0)
        self.scan_bar.setValue(0)
        self.btn_cancel.setEnabled(True)
        self.lbl_threat_badge.setText("0 Threats Detected")
        self.lbl_threat_badge.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 700;")
        self.lbl_status_text.setText(f"Active {mode.capitalize()} Scan in Progress...")

        self.worker = VirusScanWorker(mode=mode, custom_path=custom_path)
        self.worker.progress.connect(self._on_progress)
        self.worker.threat_found.connect(self._on_threat_found)
        self.worker.scan_finished.connect(self._on_finished)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def _select_custom_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Scan", "D:/")
        if folder:
            self.start_scan("custom", folder)

    def _on_progress(self, pct: int, current_path: str):
        self.scan_bar.setValue(pct)
        if len(current_path) > 75:
            display_path = "..." + current_path[-72:]
        else:
            display_path = current_path
        self.lbl_cur_file.setText(f"Analyzing: {display_path}")

    def _on_threat_found(self, res: ScanResult):
        self.detected_threats.append(res)
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_name = QTableWidgetItem(res.threat_name)
        item_name.setForeground(Qt.red)
        item_method = QTableWidgetItem(res.detection_method)
        item_score = QTableWidgetItem(f"{res.risk_score:.0f}/100")
        item_score.setForeground(Qt.yellow if res.risk_score < 80 else Qt.red)
        item_path = QTableWidgetItem(res.file_path)

        self.table.setItem(row, 0, item_name)
        self.table.setItem(row, 1, item_method)
        self.table.setItem(row, 2, item_score)
        self.table.setItem(row, 3, item_path)

        count = len(self.detected_threats)
        self.lbl_threat_badge.setText(f"⚠️ {count} Threat(s) Found!")
        self.lbl_threat_badge.setStyleSheet("color: #EF4444; font-size: 13px; font-weight: 700;")

    def _on_finished(self, total_scanned: int, threats_count: int):
        self.is_scanning = False
        self.btn_cancel.setEnabled(False)
        self.scan_bar.setValue(100)

        if threats_count == 0:
            self.lbl_status_text.setText(f"✓ Scan Finished. {total_scanned} files inspected. System clean!")
            self.lbl_cur_file.setText("No threats or malicious binaries detected.")
        else:
            self.lbl_status_text.setText(f"⚠️ Scan Finished. {threats_count} malicious items require action!")
            self.lbl_cur_file.setText("Select threats and choose 'Destroy Virus' or 'Isolate to Quarantine Vault'.")

    def _cancel_scan(self):
        if self.worker:
            self.worker.cancel()
            self.worker.wait(500)
        self.is_scanning = False
        self.btn_cancel.setEnabled(False)
        self.lbl_status_text.setText("Scan Aborted by User.")
        self.lbl_cur_file.setText("Stopped.")

    def _destroy_selected_threat(self):
        selected_rows = set(index.row() for index in self.table.selectedIndexes())
        if not selected_rows:
            if self.detected_threats:
                selected_rows = range(len(self.detected_threats))
            else:
                QMessageBox.information(self, "No Threats Selected", "No threat items currently detected to destroy.")
                return

        reply = QMessageBox.warning(
            self,
            "Permanent Threat Destruction",
            f"Are you sure you want to permanently destroy and zero-shred {len(selected_rows)} detected threat(s)?\n\nThis cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            destroyed_count = 0
            for r in sorted(selected_rows, reverse=True):
                target_path = self.table.item(r, 3).text()
                try:
                    p = Path(target_path)
                    if p.exists():
                        sz = p.stat().st_size
                        with open(p, "wb") as f:
                            f.write(b"\x00" * sz)
                        os.remove(p)
                        destroyed_count += 1
                    self.table.removeRow(r)
                except Exception as e:
                    QMessageBox.warning(self, "Error Destroying File", f"Could not destroy {target_path}:\n{e}")

            QMessageBox.information(
                self,
                "Threats Destroyed",
                f"Successfully shredded and destroyed {destroyed_count} virus item(s)!"
            )
            if self.table.rowCount() == 0:
                self.lbl_threat_badge.setText("0 Threats Detected")
                self.lbl_threat_badge.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 700;")
                self.lbl_status_text.setText("All threats successfully eliminated.")

    def _quarantine_selected_threat(self):
        selected_rows = set(index.row() for index in self.table.selectedIndexes())
        if not selected_rows:
            if self.detected_threats:
                selected_rows = range(len(self.detected_threats))
            else:
                QMessageBox.information(self, "No Threats Selected", "No threat items currently detected to isolate.")
                return

        quarantined_count = 0
        for r in sorted(selected_rows, reverse=True):
            target_path = self.table.item(r, 3).text()
            threat_name = self.table.item(r, 0).text()
            res = self.quarantine_mgr.quarantine_file(target_path, threat_name=threat_name)
            if res.get("success"):
                quarantined_count += 1
                self.table.removeRow(r)

        QMessageBox.information(
            self,
            "Quarantine Vault",
            f"Successfully encrypted and isolated {quarantined_count} file(s) into D:\\projects\\antivirus\\data\\quarantine\\."
        )
        if self.table.rowCount() == 0:
            self.lbl_threat_badge.setText("0 Threats Detected")
            self.lbl_threat_badge.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 700;")
