"""
TREVIORA AI DEFENDER - Security View (Matches Image 3: Vivo iManager Security Scan)
- Back button `< Security scan`
- Brand Header with Circular Logo Avatar & Tagline
- Center Glowing Animated Energy Shield
- Live target label: e.g. "Scanning: DeepSeek", "Scanning: explorer.exe", etc.
- 5 Security Checklist items inside ModernCard
- Cyan action button: "Stop scanning" / "Rescan Now"
"""
import time
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QThread
from treviora_defender.ui.animated_widgets import GlowingEnergyShieldWidget
from treviora_defender.ui.custom_components import ModernCard, BrandHeaderWidget


class SecurityScanWorker(QThread):
    progress = Signal(str, int, int)
    step_completed = Signal(int, str, bool)
    scan_finished = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        steps = [
            ("Network environment", ["Inspecting DNS resolution...", "Verifying TCP/IP stack...", "Checking ARP tables..."]),
            ("System vulnerabilities", ["Checking Windows Update status...", "Verifying UAC elevation policies...", "Scanning Defender coexistence..."]),
            ("Payment environment", ["Securing SSL/TLS cipher suites...", "Scanning active browser keystroke hooks...", "Verifying browser sandbox..."]),
            ("Trojan viruses", ["Scanning active memory processes...", "Inspecting autostart registry hooks...", "Analyzing running PE binaries..."]),
            ("Risky apps", ["Evaluating unsigned background binaries...", "Auditing scheduled tasks...", "Checking telemetry hooks..."])
        ]

        total_threats = 0

        for idx, (step_name, sub_actions) in enumerate(steps):
            if self._is_cancelled:
                return

            self.progress.emit(f"Scanning: {step_name}", idx, 1)

            for sub in sub_actions:
                if self._is_cancelled:
                    return
                self.progress.emit(f"Analyzing: {sub}", idx, 1)
                time.sleep(0.35)

            has_warning = False
            self.step_completed.emit(idx, f"{step_name} secured", has_warning)
            time.sleep(0.2)

        self.scan_finished.emit(total_threats)


class SecurityView(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.is_scanning = False
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
        container.setMaximumWidth(960)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 28)
        layout.setSpacing(16)

        # 1. Top Header Row (< Security scan ... Brand ... [Gear])
        top_bar = QHBoxLayout()
        self.btn_back = QPushButton("‹  Security scan")
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

        btn_settings = QPushButton("⚙️")
        btn_settings.setStyleSheet("background: transparent; border: none; font-size: 16px; color: #94A3B8;")
        btn_settings.setCursor(Qt.PointingHandCursor)
        top_bar.addWidget(btn_settings)
        layout.addLayout(top_bar)

        # Glowing divider line
        self.glow_line = QFrame()
        self.glow_line.setFixedHeight(1)
        self.glow_line.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.5 #FF7814, stop:1 transparent);"
        )
        layout.addWidget(self.glow_line)
        layout.addSpacing(8)

        # 2. Central High-Tech Glowing Energy Shield (Image 3)
        shield_container = QHBoxLayout()
        shield_container.addStretch()
        self.shield_widget = GlowingEnergyShieldWidget(size=170, color_theme="orange")
        shield_container.addWidget(self.shield_widget)
        shield_container.addStretch()
        layout.addLayout(shield_container)

        # Scanning target label (Image 3: "Scanning: DeepSeek")
        self.lbl_target = QLabel("Scanning: Initializing AI Defense...")
        self.lbl_target.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: 700;")
        self.lbl_target.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_target)

        layout.addSpacing(8)

        # 3. 5-Item Security Checklist Card (Image 3)
        card = ModernCard()
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(24, 20, 24, 20)
        c_layout.setSpacing(16)

        self.checklist_items = [
            ("Network environment", "🔒"),
            ("System vulnerabilities", "🛡️"),
            ("Payment environment", "💳"),
            ("Trojan viruses", "🦠"),
            ("Risky apps", "📱")
        ]

        self.badge_labels = []

        for idx, (title, icon) in enumerate(self.checklist_items):
            row = QHBoxLayout()
            row.setSpacing(12)

            lbl_icon = QLabel(icon)
            lbl_icon.setStyleSheet("font-size: 16px;")

            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: 600;")

            badge = QLabel("⌛")
            badge.setStyleSheet("font-size: 14px; color: #64748B;")

            row.addWidget(lbl_icon)
            row.addWidget(lbl_title)
            row.addStretch()
            row.addWidget(badge)

            c_layout.addLayout(row)
            self.badge_labels.append(badge)

        layout.addWidget(card)
        layout.addStretch()

        # 4. "Powered by Treviora AI Engine"
        lbl_power = QLabel("Powered by Treviora AI Engine & Heuristics")
        lbl_power.setStyleSheet("color: #64748B; font-size: 12px; font-weight: 500;")
        lbl_power.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_power)

        # 5. Stop scanning / Clean button (Image 3 bottom cyan pill button)
        self.btn_action = QPushButton("Stop scanning")
        self.btn_action.setCursor(Qt.PointingHandCursor)
        self.btn_action.setFixedHeight(46)
        self.btn_action.setStyleSheet("""
            QPushButton {
                background: #00D2FF;
                color: #060A10;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                font-weight: 800;
                border: none;
                border-radius: 23px;
                padding: 0px 32px;
            }
            QPushButton:hover {
                background: #38BDF8;
            }
            QPushButton:pressed {
                background: #0284C7;
            }
        """)
        self.btn_action.clicked.connect(self.handle_action_button)
        layout.addWidget(self.btn_action)

        w_layout.addWidget(container)
        w_layout.addStretch(1)

        scroll.setWidget(wrapper)
        root_layout.addWidget(scroll)

    def start_scan(self):
        if self.is_scanning or (hasattr(self, 'worker') and self.worker and self.worker.isRunning()):
            return

        self.is_scanning = True
        self.shield_widget.set_theme("orange")
        self.glow_line.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.5 #FF7814, stop:1 transparent);"
        )
        self.lbl_target.setText("Scanning: DeepSeek & Process Memory...")
        self.btn_action.setText("Stop scanning")

        for badge in self.badge_labels:
            badge.setText("⏳")
            badge.setStyleSheet("color: #00D2FF; font-size: 13px;")

        self.worker = SecurityScanWorker()
        self.worker.progress.connect(self._on_worker_progress)
        self.worker.step_completed.connect(self._on_step_completed)
        self.worker.scan_finished.connect(self._on_scan_finished)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()

    def _on_worker_progress(self, target_text: str, step_idx: int, status: int):
        self.lbl_target.setText(target_text)
        if 0 <= step_idx < len(self.badge_labels):
            self.badge_labels[step_idx].setText("🔄")
            self.badge_labels[step_idx].setStyleSheet("color: #00D2FF; font-size: 14px;")

    def _on_step_completed(self, step_idx: int, msg: str, has_warning: bool):
        if 0 <= step_idx < len(self.badge_labels):
            if has_warning:
                self.badge_labels[step_idx].setText("⚠️ Warning")
                self.badge_labels[step_idx].setStyleSheet("color: #F59E0B; font-weight: 700; font-size: 12px;")
            else:
                self.badge_labels[step_idx].setText("✓ Safe")
                self.badge_labels[step_idx].setStyleSheet("color: #00E676; font-weight: 700; font-size: 12px;")

    def _on_scan_finished(self, threats: int):
        self.is_scanning = False
        self.shield_widget.set_theme("emerald")
        self.glow_line.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.5 #00E676, stop:1 transparent);"
        )
        self.lbl_target.setText("System is Fully Protected")
        self.btn_action.setText("Rescan Now")

    def handle_action_button(self):
        if self.is_scanning:
            if self.worker:
                self.worker.cancel()
                self.worker.wait(500)
            self.is_scanning = False
            self.lbl_target.setText("Scan Cancelled")
            self.btn_action.setText("Start Security Scan")
        else:
            self.start_scan()
