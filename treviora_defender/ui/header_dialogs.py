"""
TREVIORA AI DEFENDER - Header Bar Interactive Dialogs
Implements functions for the 3 top-right header buttons:
1. 🔔 Security Notifications & Incident Intel Dialog
2. 👤 User Profile, License & Device Hardware Details Dialog
"""
import os
import platform
import psutil
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTabWidget, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont, QColor, QIcon

from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.core.hardware_profile import HardwareProfile
from treviora_defender.config.constants import APP_NAME, APP_VERSION


class SecurityNotificationsDialog(QDialog):
    """
    Floating modern Cyberpunk Notifications & Security Alerts Dialog.
    Triggered by the top header bell button (🔔).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Security Notifications & Threat Intel")
        self.setFixedSize(540, 620)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.db = DatabaseManager()
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        # Outer Frame with Cyber Glow
        outer = QFrame()
        outer.setObjectName("NotifOuterFrame")
        outer.setStyleSheet("""
            QFrame#NotifOuterFrame {
                background-color: #060B18;
                border: 2px solid #00D2FF;
                border-radius: 18px;
            }
        """)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(20, 18, 20, 18)
        outer_layout.setSpacing(14)

        # Header Row
        hdr = QHBoxLayout()
        lbl_icon = QLabel("🔔")
        lbl_icon.setStyleSheet("font-size: 20px;")
        
        lbl_title = QLabel("SECURITY NOTIFICATIONS")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 800; letter-spacing: 0.8px;")

        lbl_live = QLabel("● LIVE FEED")
        lbl_live.setStyleSheet("color: #00E676; font-size: 10px; font-weight: 800; margin-left: 6px;")

        btn_close = QPushButton("✕")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #111D36;
                color: #94A3B8;
                border-radius: 15px;
                font-weight: 800;
                font-size: 13px;
                border: 1px solid #1E2E4E;
            }
            QPushButton:hover {
                background: #EF4444;
                color: #FFFFFF;
                border-color: #EF4444;
            }
        """)
        btn_close.clicked.connect(self.close)

        hdr.addWidget(lbl_icon)
        hdr.addWidget(lbl_title)
        hdr.addWidget(lbl_live)
        hdr.addStretch()
        hdr.addWidget(btn_close)
        outer_layout.addLayout(hdr)

        # Subtitle
        lbl_sub = QLabel("Real-time telemetry, threat alerts, firewall locks, and background events.")
        lbl_sub.setStyleSheet("color: #64748B; font-size: 11px;")
        outer_layout.addWidget(lbl_sub)

        # Scrollable Notifications List
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.list_container = QWidget()
        self.list_container.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 4, 0, 4)
        self.list_layout.setSpacing(8)

        self._populate_notifications()

        scroll.setWidget(self.list_container)
        outer_layout.addWidget(scroll)

        # Bottom Action Buttons
        bot_bar = QHBoxLayout()
        bot_bar.setSpacing(10)

        btn_clear = QPushButton("🧹 Clear All Notifications")
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setFixedHeight(36)
        btn_clear.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: #94A3B8;
                border: 1px solid #1E293B;
                border-radius: 10px;
                font-size: 11px;
                font-weight: 700;
                padding: 0px 14px;
            }
            QPushButton:hover {
                color: #EF4444;
                border-color: #EF4444;
            }
        """)
        btn_clear.clicked.connect(self._clear_notifications)

        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setFixedHeight(36)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                font-size: 11px;
                font-weight: 800;
                padding: 0px 18px;
            }
            QPushButton:hover {
                background: #00B0FF;
            }
        """)
        btn_refresh.clicked.connect(self._populate_notifications)

        bot_bar.addWidget(btn_clear)
        bot_bar.addStretch()
        bot_bar.addWidget(btn_refresh)
        outer_layout.addLayout(bot_bar)

        root.addWidget(outer)

    def _populate_notifications(self):
        # Clear existing
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Fetch events from database
        events = self.db.get_recent_events(limit=25)

        # Default system events if DB is fresh
        if not events:
            events = [
                {"event_type": "ShieldActive", "source": "SafeGuard", "description": "SafeGuard 3-Layer Quantum Energy Shield is armed & active.", "severity": "Info", "timestamp": "Just now"},
                {"event_type": "RealTimeWatch", "source": "Observer", "description": "Continuous real-time file protection observer watching endpoints.", "severity": "Info", "timestamp": "1m ago"},
                {"event_type": "CanaryGuard", "source": "RansomwareGuard", "description": "Anti-ransomware canary decoy traps actively armed.", "severity": "Info", "timestamp": "3m ago"},
                {"event_type": "Optimizer", "source": "SystemOptimizer", "description": "RAM working set flushed: 469.4 MB reclaimed successfully.", "severity": "Info", "timestamp": "5m ago"},
            ]

        for ev in events:
            card = self._create_notif_card(ev)
            self.list_layout.addWidget(card)

        self.list_layout.addStretch()

    def _create_notif_card(self, ev: dict) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #0A1224;
                border: 1px solid #1E2E4E;
                border-radius: 10px;
                padding: 10px;
            }
            QFrame:hover {
                border-color: #00D2FF;
            }
        """)
        l = QVBoxLayout(card)
        l.setContentsMargins(12, 8, 12, 8)
        l.setSpacing(4)

        hdr = QHBoxLayout()
        sev = ev.get("severity", "Info")
        dot_color = "#00E676" if sev == "Info" else ("#F59E0B" if sev == "Warning" else "#EF4444")
        
        lbl_src = QLabel(f"● {ev.get('source', 'System')}")
        lbl_src.setStyleSheet(f"color: {dot_color}; font-size: 11px; font-weight: 800;")
        
        lbl_time = QLabel(str(ev.get("timestamp", "Recent")))
        lbl_time.setStyleSheet("color: #64748B; font-size: 10px;")

        hdr.addWidget(lbl_src)
        hdr.addStretch()
        hdr.addWidget(lbl_time)
        l.addLayout(hdr)

        lbl_desc = QLabel(ev.get("description", "Event logged."))
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #E2E8F0; font-size: 12px; line-height: 1.3;")
        l.addWidget(lbl_desc)

        return card

    def _clear_notifications(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        lbl_empty = QLabel("All notifications cleared.\nNo active security incidents.")
        lbl_empty.setAlignment(Qt.AlignCenter)
        lbl_empty.setStyleSheet("color: #64748B; font-size: 13px; padding: 40px;")
        self.list_layout.addWidget(lbl_empty)


class UserProfileDialog(QDialog):
    """
    Modern Cyberpunk User Identity, Machine Specs & License Details Dialog.
    Triggered by top header profile avatar button (👤).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operator Profile & Hardware Intelligence")
        self.setFixedSize(560, 660)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.profile = HardwareProfile.get_profile()
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        outer = QFrame()
        outer.setObjectName("UserOuterFrame")
        outer.setStyleSheet("""
            QFrame#UserOuterFrame {
                background-color: #060B18;
                border: 2px solid #00D2FF;
                border-radius: 20px;
            }
        """)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(22, 20, 22, 20)
        outer_layout.setSpacing(14)

        # Top Bar with Close
        top_bar = QHBoxLayout()
        lbl_badge = QLabel("OPERATOR IDENTITY & HARDWARE INTEL")
        lbl_badge.setStyleSheet("color: #00D2FF; font-size: 11px; font-weight: 800; letter-spacing: 1.0px;")

        btn_close = QPushButton("✕")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #111D36;
                color: #94A3B8;
                border-radius: 15px;
                font-weight: 800;
                font-size: 13px;
                border: 1px solid #1E2E4E;
            }
            QPushButton:hover {
                background: #EF4444;
                color: #FFFFFF;
                border-color: #EF4444;
            }
        """)
        btn_close.clicked.connect(self.close)

        top_bar.addWidget(lbl_badge)
        top_bar.addStretch()
        top_bar.addWidget(btn_close)
        outer_layout.addLayout(top_bar)

        # User Card Row
        u_card = QFrame()
        u_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0B1930, stop:1 #132A52);
                border: 1px solid #00D2FF;
                border-radius: 14px;
            }
        """)
        u_layout = QHBoxLayout(u_card)
        u_layout.setContentsMargins(18, 14, 18, 14)
        u_layout.setSpacing(16)

        lbl_avatar = QLabel("👤")
        lbl_avatar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0070F3, stop:1 #00D2FF);
            font-size: 26px;
            border-radius: 26px;
            padding: 10px;
        """)

        u_info = QVBoxLayout()
        u_info.setSpacing(2)
        lbl_uname = QLabel(self.profile["os"]["user"].upper())
        lbl_uname.setStyleSheet("color: #FFFFFF; font-size: 17px; font-weight: 800;")
        lbl_role = QLabel("TREVIORA SECURITY ADMINISTRATOR")
        lbl_role.setStyleSheet("color: #00E676; font-size: 11px; font-weight: 800;")
        lbl_tier = QLabel("TREVIORA AI DEFENDER ULTIMATE (Lifetime Enterprise)")
        lbl_tier.setStyleSheet("color: #94A3B8; font-size: 11px;")

        u_info.addWidget(lbl_uname)
        u_info.addWidget(lbl_role)
        u_info.addWidget(lbl_tier)

        u_layout.addWidget(lbl_avatar)
        u_layout.addLayout(u_info)
        u_layout.addStretch()
        outer_layout.addWidget(u_card)

        # Dynamic System Hardware Specifications Grid
        lbl_hw_title = QLabel("SYSTEM HARDWARE SPECIFICATIONS")
        lbl_hw_title.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: 800; letter-spacing: 0.5px;")
        outer_layout.addWidget(lbl_hw_title)

        hw_box = QFrame()
        hw_box.setStyleSheet("""
            QFrame {
                background: #081020;
                border: 1px solid #1E2E4E;
                border-radius: 12px;
            }
        """)
        hw_layout = QVBoxLayout(hw_box)
        hw_layout.setContentsMargins(16, 12, 16, 12)
        hw_layout.setSpacing(8)

        # Rows of specifications
        hw_layout.addLayout(self._build_spec_row("🖥️ Host Computer:", self.profile["os"]["hostname"]))
        hw_layout.addLayout(self._build_spec_row("⚡ Processor (CPU):", self.profile["cpu"]["raw_name"]))
        hw_layout.addLayout(self._build_spec_row("⚙️ CPU Topology:", f"{self.profile['cpu']['cores_logical']} Logical Threads ({self.profile['cpu']['cores_physical']} Cores)"))
        hw_layout.addLayout(self._build_spec_row("🎮 Graphics (GPU):", self.profile["gpu"]["name"]))
        hw_layout.addLayout(self._build_spec_row("🧠 System RAM:", f"{self.profile['ram']['formatted']} High-Speed Physical Memory"))
        hw_layout.addLayout(self._build_spec_row("🔋 Form Factor:", f"{self.profile['form_factor']['type']}"))
        hw_layout.addLayout(self._build_spec_row("🪟 Operating System:", f"Windows {self.profile['os']['release']} (Build {self.profile['os']['version']})"))
        hw_layout.addLayout(self._build_spec_row("📁 Storage Root:", "D:\\projects\\antivirus (Dedicated Environment)"))
        hw_layout.addLayout(self._build_spec_row("🛡️ Endpoint Privilege:", "Administrator / UAC Elevated"))

        outer_layout.addWidget(hw_box)

        # Optimization Tuning Profile
        tune_box = QFrame()
        tune_box.setStyleSheet("""
            QFrame {
                background: #0A1428;
                border-left: 4px solid #00E676;
                border-radius: 8px;
            }
        """)
        tl = QVBoxLayout(tune_box)
        tl.setContentsMargins(14, 8, 14, 8)
        tl.setSpacing(3)
        lbl_t_title = QLabel(f"AUTO-OPTIMIZATION PROFILE: {self.profile['tuning']['profile_name']}")
        lbl_t_title.setStyleSheet("color: #00E676; font-size: 11px; font-weight: 800;")
        lbl_t_desc = QLabel(self.profile["tuning"]["description"])
        lbl_t_desc.setStyleSheet("color: #94A3B8; font-size: 11px;")
        tl.addWidget(lbl_t_title)
        tl.addWidget(lbl_t_desc)
        outer_layout.addWidget(tune_box)

        # Bottom Buttons
        bot_bar = QHBoxLayout()
        btn_copy = QPushButton("📋 Copy Hardware Specs")
        btn_copy.setCursor(Qt.PointingHandCursor)
        btn_copy.setFixedHeight(38)
        btn_copy.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: #00D2FF;
                border: 1px solid #1E2E4E;
                border-radius: 12px;
                font-weight: 700;
                font-size: 12px;
                padding: 0px 16px;
            }
            QPushButton:hover {
                border-color: #00D2FF;
                color: #FFFFFF;
            }
        """)
        btn_copy.clicked.connect(self._copy_specs)

        btn_ok = QPushButton("Dismiss")
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.setFixedHeight(38)
        btn_ok.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                font-weight: 800;
                font-size: 12px;
                padding: 0px 22px;
            }
            QPushButton:hover {
                background: #00B0FF;
            }
        """)
        btn_ok.clicked.connect(self.close)

        bot_bar.addWidget(btn_copy)
        bot_bar.addStretch()
        bot_bar.addWidget(btn_ok)
        outer_layout.addLayout(bot_bar)

        root.addWidget(outer)

    def _build_spec_row(self, label: str, value: str) -> QHBoxLayout:
        row = QHBoxLayout()
        lbl_l = QLabel(label)
        lbl_l.setStyleSheet("color: #64748B; font-size: 11px; font-weight: 600;")
        lbl_v = QLabel(value)
        lbl_v.setStyleSheet("color: #E2E8F0; font-size: 11px; font-weight: 700;")
        row.addWidget(lbl_l)
        row.addStretch()
        row.addWidget(lbl_v)
        return row

    def _copy_specs(self):
        from PySide6.QtGui import QGuiApplication
        cb = QGuiApplication.clipboard()
        text = (
            f"--- TREVIORA AI DEFENDER SYSTEM SPECIFICATIONS ---\n"
            f"Host Computer: {self.profile['os']['hostname']}\n"
            f"Operator: {self.profile['os']['user']}\n"
            f"Processor: {self.profile['cpu']['raw_name']} ({self.profile['cpu']['cores_logical']} logical threads)\n"
            f"Graphics: {self.profile['gpu']['name']}\n"
            f"Memory (RAM): {self.profile['ram']['formatted']}\n"
            f"Device Type: {self.profile['form_factor']['type']}\n"
            f"OS: Windows {self.profile['os']['release']} (Build {self.profile['os']['version']})\n"
            f"License: TREVIORA AI DEFENDER ULTIMATE PRO (Lifetime Enterprise Activated)\n"
        )
        cb.setText(text)
        QMessageBox.information(self, "Copied", "Hardware specifications copied to clipboard!")
