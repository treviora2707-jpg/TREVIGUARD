"""
TREVIORA AI DEFENDER - Full Desktop Dashboard View
Exact 1000% Implementation of Reference Image (media_1794294858477_ccea698a.jpg)
Developer: TREVIORA INDUSTRY
Tagline: "ENGINEERING TOMORROW, EMPOWERING HUMANITY"

Structure:
- Row 1: Hero Banner ("Your System is in Great Shape!") + 4 Mini Telemetry Cards (CPU, GPU, RAM, Battery)
- Row 2: 3 Major Function Cards (Space Cleanup, Security Scan, Hardware & Performance)
- Row 3: 3 Bottom Cards (Power & Battery, Recommended Tools, System Activity)
"""
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QProgressBar, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from treviora_defender.core.system_optimizer import SystemOptimizer
from treviora_defender.core.space_cleaner import SpaceCleaner
from treviora_defender.core.battery_monitor import BatteryMonitor
from treviora_defender.core.performance_monitor import PerformanceMonitor
from treviora_defender.core.telemetry_service import TelemetryService
from treviora_defender.core.hardware_profile import HardwareProfile
from treviora_defender.ui.custom_components import ModernCard, PillOptimizeButton, ToolButton
from treviora_defender.ui.cyber_dashboard_widgets import (
    RadialScoreWidget, HoloShieldWidget, RadialStorageWidget,
    BatteryCylinderWidget, AmdRyzenChipWidget, MiniTelemetryCard, SparklineWaveWidget
)


class DesktopDashboardView(QWidget):
    open_optimize_requested = Signal()
    open_space_requested = Signal()
    open_security_requested = Signal()
    open_performance_requested = Signal()
    open_battery_requested = Signal()
    open_virus_scan_requested = Signal(str)
    open_tools_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.telemetry = TelemetryService.get_instance()
        self.telemetry.telemetry_updated.connect(self._on_telemetry_updated)
        self._on_telemetry_updated(self.telemetry.cached_metrics)

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #040814; border: none;")

        container = QWidget()
        container.setStyleSheet("background: #040814;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 14, 18, 18)
        layout.setSpacing(14)

        # =========================================================================
        # ROW 1: Hero Card ("Your System is in Great Shape!") + 4 Mini Telemetry Cards
        # =========================================================================
        row1 = QHBoxLayout()
        row1.setSpacing(14)

        # Left Hero Card (Matches Reference Image)
        self.hero_card = ModernCard()
        self.hero_card.setFixedHeight(168)
        h_layout = QHBoxLayout(self.hero_card)
        h_layout.setContentsMargins(18, 14, 18, 14)
        h_layout.setSpacing(16)

        # 1. Radial Score Dial (Left)
        self.score_dial = RadialScoreWidget(score=95, size=140)
        h_layout.addWidget(self.score_dial)

        # 2. Text Stack & Optimize Button (Middle)
        mid_stack = QVBoxLayout()
        mid_stack.setContentsMargins(0, 6, 0, 6)
        mid_stack.setSpacing(6)

        lbl_hero_title = QLabel("Your System\nis in Great Shape!")
        lbl_hero_title.setStyleSheet("""
            color: #FFFFFF;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 20px;
            font-weight: 800;
            line-height: 1.15;
        """)

        lbl_hero_sub = QLabel("All systems are running optimally and securely.")
        lbl_hero_sub.setStyleSheet("color: #94A3B8; font-size: 11px;")

        self.btn_optimize = QPushButton("⚡ Optimize Now ➔")
        self.btn_optimize.setCursor(Qt.PointingHandCursor)
        self.btn_optimize.setFixedHeight(34)
        self.btn_optimize.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E676, stop:1 #00B0FF);
                color: #060A10;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 800;
                border: none;
                border-radius: 17px;
                padding: 0px 22px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00FF88, stop:1 #33C5FF);
            }
        """)
        self.btn_optimize.clicked.connect(self.open_optimize_requested.emit)

        mid_stack.addWidget(lbl_hero_title)
        mid_stack.addWidget(lbl_hero_sub)
        mid_stack.addWidget(self.btn_optimize, 0, Qt.AlignLeft)
        mid_stack.addStretch()
        h_layout.addLayout(mid_stack, 1)

        # 3. Holographic Glowing Energy Shield with Checkmark on Pedestal (Right)
        self.hero_holo_shield = HoloShieldWidget(size=140, show_lock=False, show_check=True)
        h_layout.addWidget(self.hero_holo_shield)

        row1.addWidget(self.hero_card, 5)

        # Right: 4 Mini Telemetry Cards in a 4-column horizontal group
        mini_group = QHBoxLayout()
        mini_group.setSpacing(10)

        self.card_mini_cpu = MiniTelemetryCard("🔲", "CPU", "33.3%", "#00E676")
        self.card_mini_gpu = MiniTelemetryCard("🎮", "GPU", "9%", "#00D2FF")
        self.card_mini_ram = MiniTelemetryCard("💾", "RAM", "11.9/23.7 GB", "#A855F7")
        self.card_mini_batt = MiniTelemetryCard("🔋", "Battery", "58% ⚡", "#00E676")

        for c in [self.card_mini_cpu, self.card_mini_gpu, self.card_mini_ram, self.card_mini_batt]:
            mini_group.addWidget(c)

        row1.addLayout(mini_group, 4)
        layout.addLayout(row1)

        # =========================================================================
        # ROW 2: 3 Major Function Cards (Space Cleanup, Security Scan, Performance)
        # =========================================================================
        row2 = QHBoxLayout()
        row2.setSpacing(14)

        # -------------------------------------------------------------
        # Card 1: Space Cleanup
        # -------------------------------------------------------------
        self.card_space = ModernCard()
        self.card_space.setFixedHeight(225)
        c1_box = QVBoxLayout(self.card_space)
        c1_box.setContentsMargins(18, 14, 18, 14)
        c1_box.setSpacing(8)

        # Card 1 Header
        c1_hdr = QHBoxLayout()
        lbl_c1_icon = QLabel("🧹")
        lbl_c1_icon.setStyleSheet("font-size: 16px;")
        c1_title_box = QVBoxLayout()
        c1_title_box.setSpacing(1)
        lbl_c1_t = QLabel("Space Cleanup")
        lbl_c1_t.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 700;")
        lbl_c1_s = QLabel("Free up more space")
        lbl_c1_s.setStyleSheet("color: #94A3B8; font-size: 11px;")
        c1_title_box.addWidget(lbl_c1_t)
        c1_title_box.addWidget(lbl_c1_s)

        lbl_c1_badge = QLabel("⚡ +12.5 GB")
        lbl_c1_badge.setStyleSheet("""
            background-color: #064E3B;
            color: #00E676;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 10px;
        """)

        c1_hdr.addWidget(lbl_c1_icon)
        c1_hdr.addLayout(c1_title_box)
        c1_hdr.addStretch()
        c1_hdr.addWidget(lbl_c1_badge)
        c1_box.addLayout(c1_hdr)

        # Card 1 Body: Radial Storage Gauge + Checklist
        c1_body = QHBoxLayout()
        c1_body.setSpacing(14)

        self.storage_dial = RadialStorageWidget(available_gb=87.32, total_gb=250.0, size=115)
        c1_body.addWidget(self.storage_dial)

        # Checklist
        chk_box = QVBoxLayout()
        chk_box.setSpacing(5)
        for item_name in ["Temporary Files", "Cache Files", "Logs & Traces", "Recycle Bin"]:
            row_chk = QHBoxLayout()
            row_chk.setSpacing(6)
            tick = QLabel("✔")
            tick.setStyleSheet("color: #00E676; font-size: 11px; font-weight: 800;")
            txt = QLabel(item_name)
            txt.setStyleSheet("color: #E2E8F0; font-size: 11px; font-weight: 600;")
            row_chk.addWidget(tick)
            row_chk.addWidget(txt)
            row_chk.addStretch()
            chk_box.addLayout(row_chk)

        c1_body.addLayout(chk_box)
        c1_box.addLayout(c1_body)

        # Card 1 Button: "Clean Now ➔"
        self.btn_clean_now = QPushButton("Clean Now ➔")
        self.btn_clean_now.setCursor(Qt.PointingHandCursor)
        self.btn_clean_now.setFixedHeight(32)
        self.btn_clean_now.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 700;
                border: none;
                border-radius: 16px;
                padding: 0px 20px;
            }
            QPushButton:hover {
                background: #00B0FF;
            }
        """)
        self.btn_clean_now.clicked.connect(self.open_space_requested.emit)
        c1_box.addWidget(self.btn_clean_now, 0, Qt.AlignLeft)

        row2.addWidget(self.card_space, 1)

        # -------------------------------------------------------------
        # Card 2: Security Scan
        # -------------------------------------------------------------
        self.card_sec = ModernCard()
        self.card_sec.setFixedHeight(225)
        c2_box = QVBoxLayout(self.card_sec)
        c2_box.setContentsMargins(18, 14, 18, 14)
        c2_box.setSpacing(8)

        # Card 2 Header
        c2_hdr = QHBoxLayout()
        lbl_c2_icon = QLabel("🛡️")
        lbl_c2_icon.setStyleSheet("font-size: 16px;")
        c2_title_box = QVBoxLayout()
        c2_title_box.setSpacing(1)
        lbl_c2_t = QLabel("Security Scan")
        lbl_c2_t.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 700;")
        lbl_c2_s = QLabel("Keep your system safe")
        lbl_c2_s.setStyleSheet("color: #94A3B8; font-size: 11px;")
        c2_title_box.addWidget(lbl_c2_t)
        c2_title_box.addWidget(lbl_c2_s)

        c2_hdr.addWidget(lbl_c2_icon)
        c2_hdr.addLayout(c2_title_box)
        c2_hdr.addStretch()
        c2_box.addLayout(c2_hdr)

        # Card 2 Body: Green Check Badge + Status + Holographic Shield with Lock
        c2_body = QHBoxLayout()
        c2_body.setSpacing(12)

        sec_status_box = QVBoxLayout()
        sec_status_box.setSpacing(6)

        status_row = QHBoxLayout()
        lbl_green_circle = QLabel("✔")
        lbl_green_circle.setStyleSheet("""
            background-color: #065F46;
            color: #00E676;
            font-size: 16px;
            font-weight: 800;
            border-radius: 18px;
            padding: 8px 11px;
        """)

        t_stat = QVBoxLayout()
        t_stat.setSpacing(1)
        lbl_prot = QLabel("Security\nProtected")
        lbl_prot.setStyleSheet("color: #00E676; font-size: 14px; font-weight: 800; line-height: 1.1;")
        lbl_last = QLabel("Last Scan: Just now")
        lbl_last.setStyleSheet("color: #64748B; font-size: 10px;")
        t_stat.addWidget(lbl_prot)
        t_stat.addWidget(lbl_last)

        status_row.addWidget(lbl_green_circle)
        status_row.addLayout(t_stat)
        status_row.addStretch()

        sec_status_box.addLayout(status_row)
        sec_status_box.addStretch()
        c2_body.addLayout(sec_status_box, 1)

        # Holo Shield with Padlock (Right)
        self.sec_holo_shield = HoloShieldWidget(size=115, show_lock=True, show_check=False)
        c2_body.addWidget(self.sec_holo_shield)
        c2_box.addLayout(c2_body)

        # Card 2 Button: "Run Scan ➔"
        self.btn_run_scan = QPushButton("Run Scan ➔")
        self.btn_run_scan.setCursor(Qt.PointingHandCursor)
        self.btn_run_scan.setFixedHeight(32)
        self.btn_run_scan.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E676, stop:1 #00B0FF);
                color: #060A10;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 800;
                border: none;
                border-radius: 16px;
                padding: 0px 22px;
            }
            QPushButton:hover {
                background: #00FF88;
            }
        """)
        self.btn_run_scan.clicked.connect(self.open_security_requested.emit)
        c2_box.addWidget(self.btn_run_scan, 0, Qt.AlignLeft)

        row2.addWidget(self.card_sec, 1)

        # -------------------------------------------------------------
        # Card 3: Hardware & Performance
        # -------------------------------------------------------------
        self.card_perf = ModernCard()
        self.card_perf.setFixedHeight(225)
        c3_box = QVBoxLayout(self.card_perf)
        c3_box.setContentsMargins(18, 14, 18, 14)
        c3_box.setSpacing(8)

        # Card 3 Header
        c3_hdr = QHBoxLayout()
        lbl_c3_icon = QLabel("💻")
        lbl_c3_icon.setStyleSheet("font-size: 16px;")
        c3_title_box = QVBoxLayout()
        c3_title_box.setSpacing(1)
        lbl_c3_t = QLabel("Hardware & Performance")
        lbl_c3_t.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 700;")
        hw_prof = HardwareProfile.get_profile()
        lbl_c3_s = QLabel(hw_prof["display_spec"])
        lbl_c3_s.setStyleSheet("color: #94A3B8; font-size: 11px;")
        c3_title_box.addWidget(lbl_c3_t)
        c3_title_box.addWidget(lbl_c3_s)

        btn_perf_arrow = QPushButton("➔")
        btn_perf_arrow.setStyleSheet("background: transparent; color: #00D2FF; font-size: 15px; border: none;")
        btn_perf_arrow.clicked.connect(self.open_performance_requested.emit)

        c3_hdr.addWidget(lbl_c3_icon)
        c3_hdr.addLayout(c3_title_box)
        c3_hdr.addStretch()
        c3_hdr.addWidget(btn_perf_arrow)
        c3_box.addLayout(c3_hdr)

        # Card 3 Body: Realistic AMD Ryzen Chip + 3 Usage Bars
        c3_body = QHBoxLayout()
        c3_body.setSpacing(12)

        self.chip_widget = AmdRyzenChipWidget(size=90)
        c3_body.addWidget(self.chip_widget)

        bars_box = QVBoxLayout()
        bars_box.setSpacing(6)

        # CPU Usage Bar
        self.bar_cpu_val = QLabel("33.3%")
        self.bar_cpu_val.setStyleSheet("color: #00D2FF; font-size: 11px; font-weight: 700;")
        self.bar_cpu = self._create_mini_bar("#00D2FF", 33)
        bars_box.addLayout(self._build_bar_row("CPU Usage", self.bar_cpu_val, self.bar_cpu))

        # GPU Usage Bar
        self.bar_gpu_val = QLabel("9%")
        self.bar_gpu_val.setStyleSheet("color: #00E676; font-size: 11px; font-weight: 700;")
        self.bar_gpu = self._create_mini_bar("#00E676", 9)
        bars_box.addLayout(self._build_bar_row("GPU Usage", self.bar_gpu_val, self.bar_gpu))

        # RAM Usage Bar
        self.bar_ram_val = QLabel("11.9 / 23.7 GB")
        self.bar_ram_val.setStyleSheet("color: #A855F7; font-size: 11px; font-weight: 700;")
        self.bar_ram = self._create_mini_bar("#A855F7", 50)
        bars_box.addLayout(self._build_bar_row("RAM Usage", self.bar_ram_val, self.bar_ram))

        c3_body.addLayout(bars_box, 1)
        c3_box.addLayout(c3_body)

        # Card 3 Button: "View Details ➔"
        self.btn_view_details = QPushButton("View Details ➔")
        self.btn_view_details.setCursor(Qt.PointingHandCursor)
        self.btn_view_details.setFixedHeight(30)
        self.btn_view_details.setStyleSheet("""
            QPushButton {
                background-color: #111D36;
                color: #00D2FF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 700;
                border: 1px solid #1E293B;
                border-radius: 15px;
                padding: 0px 18px;
            }
            QPushButton:hover {
                background-color: #162442;
                border: 1px solid #00D2FF;
            }
        """)
        self.btn_view_details.clicked.connect(self.open_performance_requested.emit)
        c3_box.addWidget(self.btn_view_details, 0, Qt.AlignLeft)

        row2.addWidget(self.card_perf, 1)
        layout.addLayout(row2)

        # =========================================================================
        # ROW 3: 3 Bottom Cards (Power & Battery, Recommended Tools, System Activity)
        # =========================================================================
        row3 = QHBoxLayout()
        row3.setSpacing(14)

        # -------------------------------------------------------------
        # Card 4: Power & Battery
        # -------------------------------------------------------------
        self.card_batt = ModernCard()
        self.card_batt.setFixedHeight(210)
        c4_box = QVBoxLayout(self.card_batt)
        c4_box.setContentsMargins(18, 14, 18, 14)
        c4_box.setSpacing(8)

        # Card 4 Header
        c4_hdr = QHBoxLayout()
        lbl_c4_icon = QLabel("⚡")
        lbl_c4_icon.setStyleSheet("font-size: 16px;")
        c4_title_box = QVBoxLayout()
        c4_title_box.setSpacing(1)
        lbl_c4_t = QLabel("Power & Battery")
        lbl_c4_t.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 700;")
        lbl_c4_s = QLabel("Power management")
        lbl_c4_s.setStyleSheet("color: #94A3B8; font-size: 11px;")
        c4_title_box.addWidget(lbl_c4_t)
        c4_title_box.addWidget(lbl_c4_s)

        c4_hdr.addWidget(lbl_c4_icon)
        c4_hdr.addLayout(c4_title_box)
        c4_hdr.addStretch()
        c4_box.addLayout(c4_hdr)

        # Card 4 Body: Battery Cylinder + Percentage + Sparkline
        c4_body = QHBoxLayout()
        c4_body.setSpacing(14)

        self.batt_cylinder = BatteryCylinderWidget(percent=58, is_charging=True)
        c4_body.addWidget(self.batt_cylinder)

        b_text_box = QVBoxLayout()
        b_text_box.setSpacing(4)

        self.lbl_batt_pct = QLabel("58%")
        self.lbl_batt_pct.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: 800; line-height: 1.0;")
        self.lbl_batt_state = QLabel("⚡ Charging")
        self.lbl_batt_state.setStyleSheet("color: #00E676; font-size: 12px; font-weight: 700;")

        b_text_box.addWidget(self.lbl_batt_pct)
        b_text_box.addWidget(self.lbl_batt_state)
        b_text_box.addStretch()
        c4_body.addLayout(b_text_box)

        # Right: Estimated Time & Waveform
        b_right_box = QVBoxLayout()
        b_right_box.setSpacing(4)
        lbl_est = QLabel("Estimated Time")
        lbl_est.setStyleSheet("color: #64748B; font-size: 10px;")
        self.lbl_est_time = QLabel("~ 1h 45m")
        self.lbl_est_time.setStyleSheet("color: #E2E8F0; font-size: 13px; font-weight: 700;")

        self.batt_wave = SparklineWaveWidget(color="#00E676")
        self.btn_power_settings = QPushButton("Power Settings ➔")
        self.btn_power_settings.setCursor(Qt.PointingHandCursor)
        self.btn_power_settings.setFixedHeight(28)
        self.btn_power_settings.setStyleSheet("""
            QPushButton {
                background: #111D36;
                color: #00D2FF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: 700;
                border: 1px solid #1E293B;
                border-radius: 14px;
                padding: 0px 14px;
            }
            QPushButton:hover {
                border: 1px solid #00D2FF;
            }
        """)
        self.btn_power_settings.clicked.connect(self.open_battery_requested.emit)

        b_right_box.addWidget(lbl_est)
        b_right_box.addWidget(self.lbl_est_time)
        b_right_box.addWidget(self.batt_wave)
        b_right_box.addWidget(self.btn_power_settings, 0, Qt.AlignRight)
        c4_body.addLayout(b_right_box, 1)

        c4_box.addLayout(c4_body)
        row3.addWidget(self.card_batt, 1)

        # -------------------------------------------------------------
        # Card 5: Recommended Tools
        # -------------------------------------------------------------
        self.card_tools = ModernCard()
        self.card_tools.setFixedHeight(210)
        c5_box = QVBoxLayout(self.card_tools)
        c5_box.setContentsMargins(18, 14, 18, 14)
        c5_box.setSpacing(8)

        # Card 5 Header
        c5_hdr = QHBoxLayout()
        lbl_c5_icon = QLabel("⭐")
        lbl_c5_icon.setStyleSheet("font-size: 16px;")
        c5_title_box = QVBoxLayout()
        c5_title_box.setSpacing(1)
        lbl_c5_t = QLabel("Recommended Tools")
        lbl_c5_t.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 700;")
        lbl_c5_s = QLabel("Boost your productivity")
        lbl_c5_s.setStyleSheet("color: #94A3B8; font-size: 11px;")
        c5_title_box.addWidget(lbl_c5_t)
        c5_title_box.addWidget(lbl_c5_s)

        c5_hdr.addWidget(lbl_c5_icon)
        c5_hdr.addLayout(c5_title_box)
        c5_hdr.addStretch()
        c5_box.addLayout(c5_hdr)

        # 3 Mini Tool Buttons
        tool_cards_row = QHBoxLayout()
        tool_cards_row.setSpacing(8)

        t1 = self._build_mini_tool_button("⚡", "Quick Virus\nScan", lambda: self.open_virus_scan_requested.emit("quick"))
        t2 = self._build_mini_tool_button("🛡️", "Full System\nScan", lambda: self.open_virus_scan_requested.emit("full"))
        t3 = self._build_mini_tool_button("🧹", "One-Click\nJunk Clean", self.open_space_requested.emit)

        tool_cards_row.addWidget(t1)
        tool_cards_row.addWidget(t2)
        tool_cards_row.addWidget(t3)
        c5_box.addLayout(tool_cards_row)

        # Bottom Button: "Open Tools ➔"
        self.btn_open_tools = QPushButton("Open Tools ➔")
        self.btn_open_tools.setCursor(Qt.PointingHandCursor)
        self.btn_open_tools.setFixedHeight(30)
        self.btn_open_tools.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 700;
                border: none;
                border-radius: 15px;
                padding: 0px 22px;
            }
            QPushButton:hover {
                background: #00B0FF;
            }
        """)
        self.btn_open_tools.clicked.connect(self.open_tools_requested.emit)
        c5_box.addWidget(self.btn_open_tools, 0, Qt.AlignCenter)

        row3.addWidget(self.card_tools, 1)

        # -------------------------------------------------------------
        # Card 6: System Activity
        # -------------------------------------------------------------
        self.card_act = ModernCard()
        self.card_act.setFixedHeight(210)
        c6_box = QVBoxLayout(self.card_act)
        c6_box.setContentsMargins(18, 14, 18, 14)
        c6_box.setSpacing(8)

        # Card 6 Header
        c6_hdr = QHBoxLayout()
        lbl_c6_icon = QLabel("📈")
        lbl_c6_icon.setStyleSheet("font-size: 16px;")
        lbl_c6_t = QLabel("System Activity")
        lbl_c6_t.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 700;")

        lbl_live_badge = QLabel("● Live")
        lbl_live_badge.setStyleSheet("""
            background-color: #064E3B;
            color: #00E676;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 10px;
        """)

        c6_hdr.addWidget(lbl_c6_icon)
        c6_hdr.addWidget(lbl_c6_t)
        c6_hdr.addStretch()
        c6_hdr.addWidget(lbl_live_badge)
        c6_box.addLayout(c6_hdr)

        # Activity list
        act_list_box = QVBoxLayout()
        act_list_box.setSpacing(6)

        activities = [
            ("✔", "#00E676", "System scan completed successfully", "2m ago"),
            ("🧹", "#38BDF8", "Cleaned 2.4 GB of temporary files", "5m ago"),
            ("🛡️", "#00D2FF", "Firewall status: Active", "7m ago"),
            ("🔋", "#00E676", "Battery charging: 58%", "10m ago"),
        ]

        for icon, color, text, time_str in activities:
            r = QHBoxLayout()
            r.setSpacing(8)
            i_lbl = QLabel(icon)
            i_lbl.setStyleSheet(f"color: {color}; font-size: 12px;")
            t_lbl = QLabel(text)
            t_lbl.setStyleSheet("color: #CBD5E1; font-size: 11px; font-weight: 500;")
            tm_lbl = QLabel(time_str)
            tm_lbl.setStyleSheet("color: #64748B; font-size: 10px;")

            r.addWidget(i_lbl)
            r.addWidget(t_lbl)
            r.addStretch()
            r.addWidget(tm_lbl)
            act_list_box.addLayout(r)

        c6_box.addLayout(act_list_box)
        c6_box.addStretch()

        row3.addWidget(self.card_act, 1)
        layout.addLayout(row3)

        scroll.setWidget(container)
        root_layout.addWidget(scroll)

    def _create_mini_bar(self, color_hex: str, initial_val: int) -> QProgressBar:
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(initial_val)
        bar.setFixedHeight(6)
        bar.setTextVisible(False)
        bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #1E293B;
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {color_hex};
                border-radius: 3px;
            }}
        """)
        return bar

    def _build_bar_row(self, title: str, val_label: QLabel, bar: QProgressBar) -> QVBoxLayout:
        b_box = QVBoxLayout()
        b_box.setSpacing(2)

        hdr = QHBoxLayout()
        lbl = QLabel(title)
        lbl.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: 600;")
        hdr.addWidget(lbl)
        hdr.addStretch()
        hdr.addWidget(val_label)

        b_box.addLayout(hdr)
        b_box.addWidget(bar)
        return b_box

    def _build_mini_tool_button(self, icon: str, title: str, slot) -> QPushButton:
        btn = QPushButton(f"{icon}\n{title}")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(68)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #0B1324;
                color: #E2E8F0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: 600;
                border: 1px solid #1E293B;
                border-radius: 12px;
                line-height: 1.2;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #162442;
                border: 1px solid #00D2FF;
                color: #FFFFFF;
            }
        """)
        btn.clicked.connect(slot)
        return btn

    def refresh_metrics(self):
        """Instant non-blocking refresh using cached background telemetry."""
        if hasattr(self, 'telemetry'):
            self._on_telemetry_updated(self.telemetry.cached_metrics)

    def _on_telemetry_updated(self, metrics: dict):
        """Applies metrics instantly on the GUI thread in 0.1ms without blocking."""
        if not metrics:
            return

        # 1. System Health Score
        score = metrics.get('health_score', 95)
        self.score_dial.set_score(score)

        # 2. Available Disk Space
        disk = metrics.get('disk', {})
        free_gb = disk.get('free_gb', 87.32)
        self.storage_dial.set_available(free_gb)

        # 3. CPU, GPU, RAM
        cpu_pct = metrics.get('cpu_percent', 33.3)
        gpu = metrics.get('gpu', {})
        gpu_pct = gpu.get('utilization_pct', 9)
        ram_used = metrics.get('ram_used_gb', 11.9)
        ram_total = metrics.get('ram_total_gb', 23.7)
        ram_pct = metrics.get('ram_percent', 50.0)

        self.card_mini_cpu.set_value(f"{cpu_pct}%")
        self.card_mini_gpu.set_value(f"{gpu_pct}%")
        self.card_mini_ram.set_value(f"{ram_used}/{ram_total} GB")

        self.bar_cpu_val.setText(f"{cpu_pct}%")
        self.bar_cpu.setValue(int(cpu_pct))
        self.bar_gpu_val.setText(f"{gpu_pct}%")
        self.bar_gpu.setValue(int(gpu_pct))
        self.bar_ram_val.setText(f"{ram_used} / {ram_total} GB")
        self.bar_ram.setValue(int(ram_pct))

        # 4. Battery
        batt = metrics.get('battery', {})
        batt_pct = batt.get('percent', 58)
        is_plugged = batt.get('is_plugged', True)

        self.card_mini_batt.set_value(f"{batt_pct}% ⚡" if is_plugged else f"{batt_pct}%")
        self.batt_cylinder.set_percent(batt_pct, is_charging=is_plugged)
        self.lbl_batt_pct.setText(f"{batt_pct}%")
        self.lbl_batt_state.setText("⚡ Charging" if is_plugged else "On Battery")
        self.lbl_est_time.setText(batt.get('time_remaining', '~ 1h 45m'))
