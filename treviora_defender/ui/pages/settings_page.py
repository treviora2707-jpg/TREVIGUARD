r"""
TREVIORA AI DEFENDER - Page 10: Configuration & System Settings
Manages exclusions, AI parameters, quarantine behavior, and hardware integration.
All configuration is strictly saved to D:\projects\antivirus\data\config.json.
"""
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QCheckBox, QSpinBox, QListWidget, QFileDialog, QMessageBox,
    QScrollArea
)
from PySide6.QtCore import Qt
from treviora_defender.config.settings import SettingsManager
from treviora_defender.config.constants import DATA_DIR, BASE_DIR


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self._init_ui()

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(18)

        # Header
        header = QVBoxLayout()
        title = QLabel("System Settings & Customization")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Device Optimization • Exclusion Rules • AI Inference Settings • Storage Policy")
        sub.setProperty("class", "PageSubtitle")
        header.addWidget(title)
        header.addWidget(sub)
        layout.addLayout(header)

        # Storage & Device Specs Frame
        specs_frame = QFrame()
        specs_frame.setProperty("class", "GlassCard")
        specs_layout = QVBoxLayout(specs_frame)
        specs_layout.setContentsMargins(18, 14, 18, 14)
        specs_layout.setSpacing(6)

        specs_title = QLabel("Storage Policy & Hardware Profile")
        specs_title.setProperty("class", "CardTitle")
        specs_layout.addWidget(specs_title)

        loc_label = QLabel(f"📁 Designated Storage Partition: {BASE_DIR} (STRICT D: DRIVE ONLY)")
        loc_label.setStyleSheet("color: #00D2FF; font-weight: 700; font-size: 13px;")
        specs_layout.addWidget(loc_label)

        hw_label = QLabel("💻 Primary Device: Lenovo LOQ | AMD Ryzen 5 | NVIDIA RTX 3050 6GB | 24GB RAM | Windows 11")
        hw_label.setStyleSheet("color: #94A3B8; font-size: 12px;")
        specs_layout.addWidget(hw_label)

        layout.addWidget(specs_frame)

        # Exclusion Manager
        excl_frame = QFrame()
        excl_frame.setProperty("class", "GlassCard")
        excl_layout = QVBoxLayout(excl_frame)
        excl_layout.setContentsMargins(18, 14, 18, 14)
        excl_layout.setSpacing(10)

        excl_title = QLabel("Scan Exclusions & Whitelist Paths")
        excl_title.setProperty("class", "CardTitle")
        excl_layout.addWidget(excl_title)

        self.list_exclusions = QListWidget()
        self.list_exclusions.setFixedHeight(90)
        excl_layout.addWidget(self.list_exclusions)

        btn_row = QHBoxLayout()
        btn_add_folder = QPushButton("Add Folder...")
        btn_add_folder.setProperty("class", "SecondaryButton")
        btn_add_folder.clicked.connect(self.add_folder_exclusion)

        btn_add_file = QPushButton("Add File...")
        btn_add_file.setProperty("class", "SecondaryButton")
        btn_add_file.clicked.connect(self.add_file_exclusion)

        btn_remove = QPushButton("Remove Selected")
        btn_remove.setProperty("class", "DangerButton")
        btn_remove.clicked.connect(self.remove_exclusion)

        btn_row.addWidget(btn_add_folder)
        btn_row.addWidget(btn_add_file)
        btn_row.addWidget(btn_remove)
        btn_row.addStretch()
        excl_layout.addLayout(btn_row)

        layout.addWidget(excl_frame)

        # AI Configuration Frame
        ai_frame = QFrame()
        ai_frame.setProperty("class", "GlassCard")
        ai_layout = QVBoxLayout(ai_frame)
        ai_layout.setContentsMargins(18, 14, 18, 14)
        ai_layout.setSpacing(10)

        ai_title = QLabel("AI Security Assistant & External LLM Configuration")
        ai_title.setProperty("class", "CardTitle")
        ai_layout.addWidget(ai_title)

        self.chk_cloud_ai = QCheckBox("Enable Optional External AI (Ollama localhost / OpenAI compatible)")
        self.chk_cloud_ai.setChecked(self.settings.get("cloud_ai_enabled", False))
        self.chk_cloud_ai.setStyleSheet("color: #E2E8F0; font-weight: 500;")
        ai_layout.addWidget(self.chk_cloud_ai)

        endpoint_row = QHBoxLayout()
        ep_lbl = QLabel("Endpoint URL:")
        ep_lbl.setStyleSheet("color: #94A3B8;")
        self.txt_endpoint = QLineEdit(self.settings.get("cloud_ai_endpoint", "http://localhost:11434"))
        endpoint_row.addWidget(ep_lbl)
        endpoint_row.addWidget(self.txt_endpoint, 1)
        ai_layout.addLayout(endpoint_row)

        key_row = QHBoxLayout()
        key_lbl = QLabel("API Key (if required):")
        key_lbl.setStyleSheet("color: #94A3B8;")
        self.txt_api_key = QLineEdit(self.settings.get("cloud_ai_api_key", ""))
        self.txt_api_key.setEchoMode(QLineEdit.Password)
        key_row.addWidget(key_lbl)
        key_row.addWidget(self.txt_api_key, 1)
        ai_layout.addLayout(key_row)

        layout.addWidget(ai_frame)

        # Save Settings Button
        save_btn = QPushButton("💾 Save All Settings")
        save_btn.setProperty("class", "PrimaryButton")
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)

        scroll.setWidget(container)
        root_layout.addWidget(scroll)

        self.refresh_exclusions()

    def refresh_exclusions(self):
        self.list_exclusions.clear()
        for excl in self.settings.get("exclusions", []):
            self.list_exclusions.addItem(excl)

    def add_folder_exclusion(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Exclusion Folder", "D:\\")
        if folder:
            self.settings.add_exclusion(folder)
            self.refresh_exclusions()

    def add_file_exclusion(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Exclusion File", "D:\\")
        if file_path:
            self.settings.add_exclusion(file_path)
            self.refresh_exclusions()

    def remove_exclusion(self):
        sel = self.list_exclusions.currentItem()
        if sel:
            self.settings.remove_exclusion(sel.text())
            self.refresh_exclusions()

    def save_settings(self):
        self.settings.set("cloud_ai_enabled", self.chk_cloud_ai.isChecked())
        self.settings.set("cloud_ai_endpoint", self.txt_endpoint.text().strip())
        self.settings.set("cloud_ai_api_key", self.txt_api_key.text().strip())
        QMessageBox.information(self, "Settings Saved", "Configuration updated and saved successfully to D: drive.")
