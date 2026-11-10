"""
TREVIORA AI DEFENDER - Space Cleanup & Storage Management View
Matches Vivo iManager / Clean Master aesthetic:
- Free up more space header & available storage gauge
- One-Click Junk Clean button
- Storage breakdown by drive (C: & D:)
- Tabs/Panels for:
  * Temporary & Junk Files
  * Large Files (>50MB)
  * Duplicate Files
"""
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QScrollArea, QTabWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QThread
from treviora_defender.core.space_cleaner import SpaceCleaner
from treviora_defender.ui.custom_components import ModernCard, PillOptimizeButton, BrandHeaderWidget


class JunkScanWorker(QThread):
    finished_signal = Signal(dict)

    def run(self):
        data = SpaceCleaner.scan_junk_files()
        self.finished_signal.emit(data)


class DeepScanWorker(QThread):
    finished_signal = Signal(list, list)

    def run(self):
        large = SpaceCleaner.scan_large_files(target_dir="D:/projects/antivirus", min_size_mb=50)
        duplicates = SpaceCleaner.scan_duplicate_files(target_dir="D:/projects/antivirus")
        self.finished_signal.emit(large, duplicates)


class SpaceView(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.junk_data = {}
        self._init_ui()
        self.refresh_storage()

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
        self.btn_back = QPushButton("‹  Space cleanup")
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

        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.setProperty("class", "ModernSecondary")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_storage)
        top_bar.addWidget(self.btn_refresh)
        layout.addLayout(top_bar)

        # 2. Main Storage Hero Card (Image 1 Space Card Style)
        hero_card = ModernCard()
        h_layout = QVBoxLayout(hero_card)
        h_layout.setContentsMargins(24, 22, 24, 22)
        h_layout.setSpacing(14)

        lbl_hdr = QLabel("STORAGE MANAGEMENT")
        lbl_hdr.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;")

        self.lbl_available_main = QLabel("Calculating available space...")
        self.lbl_available_main.setStyleSheet("color: #FFFFFF; font-size: 28px; font-weight: 800;")

        self.storage_progress = QProgressBar()
        self.storage_progress.setFixedHeight(12)
        self.storage_progress.setTextVisible(False)
        self.storage_progress.setStyleSheet("""
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

        # Action row inside Hero
        act_row = QHBoxLayout()
        self.lbl_junk_status = QLabel("Scanning for junk & temporary files...")
        self.lbl_junk_status.setStyleSheet("color: #00D2FF; font-size: 14px; font-weight: 600;")
        act_row.addWidget(self.lbl_junk_status)
        act_row.addStretch()

        self.btn_clean_junk = PillOptimizeButton("🧹 Clean Junk Files")
        self.btn_clean_junk.clicked.connect(self._execute_clean_junk)
        act_row.addWidget(self.btn_clean_junk)

        h_layout.addWidget(lbl_hdr)
        h_layout.addWidget(self.lbl_available_main)
        h_layout.addWidget(self.storage_progress)
        h_layout.addLayout(act_row)
        layout.addWidget(hero_card)

        # 3. Drive Breakdown (C: & D:)
        drives_card = ModernCard()
        d_layout = QVBoxLayout(drives_card)
        d_layout.setContentsMargins(24, 20, 24, 20)
        d_layout.setSpacing(14)

        lbl_drives_title = QLabel("System Drive Breakdown")
        lbl_drives_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 700;")
        d_layout.addWidget(lbl_drives_title)

        self.drive_c_box = self._create_drive_row("C: Windows System Drive")
        self.drive_d_box = self._create_drive_row("D: Treviora & Project Drive")
        d_layout.addLayout(self.drive_c_box["layout"])
        d_layout.addLayout(self.drive_d_box["layout"])
        layout.addWidget(drives_card)

        # 4. Deep Cleanup Tabs (Junk / Large Files / Duplicates)
        tabs_card = ModernCard()
        t_layout = QVBoxLayout(tabs_card)
        t_layout.setContentsMargins(18, 18, 18, 18)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #0B111E;
                color: #94A3B8;
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #1E293B;
                color: #00D2FF;
            }
        """)

        # Tab 1: Junk Files List
        self.junk_table = QTableWidget(0, 3)
        self.junk_table.setHorizontalHeaderLabels(["File Name", "Size (MB)", "Path"])
        self.junk_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabs.addTab(self.junk_table, "📁 Temporary Junk Files")

        # Tab 2: Large Files
        self.large_table = QTableWidget(0, 3)
        self.large_table.setHorizontalHeaderLabels(["File Name", "Size (MB)", "Path"])
        self.large_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabs.addTab(self.large_table, "📦 Large Files (>50MB)")

        # Tab 3: Duplicates
        self.dup_table = QTableWidget(0, 3)
        self.dup_table.setHorizontalHeaderLabels(["Original File", "Duplicate File", "Size (MB)"])
        self.dup_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabs.addTab(self.dup_table, "👥 Duplicate Files")

        t_layout.addWidget(self.tabs)
        layout.addWidget(tabs_card)

        w_layout.addWidget(container)
        w_layout.addStretch(1)

        scroll.setWidget(wrapper)
        root_layout.addWidget(scroll)

    def _create_drive_row(self, label_text: str) -> dict:
        row_layout = QVBoxLayout()
        row_layout.setSpacing(6)

        header_row = QHBoxLayout()
        lbl_name = QLabel(label_text)
        lbl_name.setStyleSheet("color: #E2E8F0; font-size: 13px; font-weight: 600;")
        lbl_stats = QLabel("0 GB / 0 GB (0%)")
        lbl_stats.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")

        header_row.addWidget(lbl_name)
        header_row.addStretch()
        header_row.addWidget(lbl_stats)

        bar = QProgressBar()
        bar.setFixedHeight(10)
        bar.setTextVisible(False)
        bar.setStyleSheet("""
            QProgressBar {
                background-color: #1E293B;
                border: none;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
                border-radius: 5px;
            }
        """)

        row_layout.addLayout(header_row)
        row_layout.addWidget(bar)

        return {
            "layout": row_layout,
            "label_stats": lbl_stats,
            "bar": bar
        }

    def refresh_storage(self):
        drives = SpaceCleaner.get_drive_storage()
        for d in drives:
            if "C:" in d["drive"].upper():
                self.drive_c_box["label_stats"].setText(f"{d['used_gb']} GB used of {d['total_gb']} GB ({d['percent']}%)")
                self.drive_c_box["bar"].setValue(int(d["percent"]))
            elif "D:" in d["drive"].upper():
                self.drive_d_box["label_stats"].setText(f"{d['used_gb']} GB used of {d['total_gb']} GB ({d['percent']}%)")
                self.drive_d_box["bar"].setValue(int(d["percent"]))

        free_gb = SpaceCleaner.get_primary_available_gb()
        self.lbl_available_main.setText(f"{free_gb:.2f} GB available")
        self.storage_progress.setValue(min(100, int((free_gb / 512.0) * 100)))

        # Prevent concurrent worker collisions (prevents PySide segfault)
        if hasattr(self, 'junk_worker') and self.junk_worker and self.junk_worker.isRunning():
            return
        if hasattr(self, 'deep_worker') and self.deep_worker and self.deep_worker.isRunning():
            return

        self.lbl_junk_status.setText("Scanning junk files...")
        self.junk_worker = JunkScanWorker()
        self.junk_worker.finished_signal.connect(self._on_junk_scanned)
        self.junk_worker.finished.connect(self.junk_worker.deleteLater)
        self.junk_worker.start()

        self.deep_worker = DeepScanWorker()
        self.deep_worker.finished_signal.connect(self._on_deep_scanned)
        self.deep_worker.finished.connect(self.deep_worker.deleteLater)
        self.deep_worker.start()

    def _on_junk_scanned(self, data: dict):
        self.junk_data = data
        self.lbl_junk_status.setText(f"Found {data['count']} junk items ({data['total_mb']} MB cleanable)")

        self.junk_table.setRowCount(0)
        for f in data.get("files", [])[:100]:
            row = self.junk_table.rowCount()
            self.junk_table.insertRow(row)
            self.junk_table.setItem(row, 0, QTableWidgetItem(f["name"]))
            self.junk_table.setItem(row, 1, QTableWidgetItem(str(f["size_mb"])))
            self.junk_table.setItem(row, 2, QTableWidgetItem(f["path"]))

    def _on_deep_scanned(self, large_files: list, duplicates: list):
        self.large_table.setRowCount(0)
        for f in large_files:
            row = self.large_table.rowCount()
            self.large_table.insertRow(row)
            self.large_table.setItem(row, 0, QTableWidgetItem(f["name"]))
            self.large_table.setItem(row, 1, QTableWidgetItem(str(f["size_mb"])))
            self.large_table.setItem(row, 2, QTableWidgetItem(f["path"]))

        self.dup_table.setRowCount(0)
        for d in duplicates:
            row = self.dup_table.rowCount()
            self.dup_table.insertRow(row)
            self.dup_table.setItem(row, 0, QTableWidgetItem(Path(d["original"]).name))
            self.dup_table.setItem(row, 1, QTableWidgetItem(Path(d["duplicate"]).name))
            self.dup_table.setItem(row, 2, QTableWidgetItem(str(d["size_mb"])))

    def _execute_clean_junk(self):
        result = SpaceCleaner.clean_junk_files()
        QMessageBox.information(
            self,
            "Cleanup Complete",
            f"Successfully cleaned {result['deleted_count']} temporary junk files.\nFreed {result['freed_mb']} MB of space!"
        )
        self.refresh_storage()
