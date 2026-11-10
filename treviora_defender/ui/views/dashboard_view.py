"""
TREVIORA AI DEFENDER - Dashboard View (Vivo iManager Style)
Developer: TREVIORA INDUSTRY
Tagline: "ENGINEERING TOMORROW, EMPOWERING HUMANITY"
- Big Score "98"
- "Optimize" green pill button
- Segmented pulse progress bar
- 4 High-Tech Rounded Glass Cards: Space Cleanup, Security Scan, Performance, Battery
- Recommended Quick Tools
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
from treviora_defender.ui.animated_widgets import SegmentedProgressBar, StepSignalWidget
from treviora_defender.ui.custom_components import (
    ModernCard, PillOptimizeButton, ToolButton, SafeGuardPillButton, BrandHeaderWidget
)


class DashboardView(QWidget):
    open_optimize_requested = Signal()
    open_space_requested = Signal()
    open_security_requested = Signal()
    open_performance_requested = Signal()
    open_battery_requested = Signal()
    open_safeguard_requested = Signal()
    open_virus_scan_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self.refresh_metrics()

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #060911; border: none;")

        # Outer centering wrapper
        wrapper = QWidget()
        wrapper.setStyleSheet("background: #060911;")
        w_layout = QHBoxLayout(wrapper)
        w_layout.setContentsMargins(0, 0, 0, 0)
        w_layout.addStretch(1)

        # Centered container (fixed max-width for perfect proportions on any resolution)
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        container.setMaximumWidth(1100)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(18)

        # 1. Top Header Bar (Circular Framed Logo + SafeGuard 3-Layer Shield Pill)
        top_bar = QHBoxLayout()
        self.brand_header = BrandHeaderWidget()
        top_bar.addWidget(self.brand_header)

        top_bar.addStretch()

        self.btn_safeguard = SafeGuardPillButton("🛡️ SafeGuard 3-Layer Firewall: ACTIVE")
        self.btn_safeguard.clicked.connect(self.open_safeguard_requested.emit)
        top_bar.addWidget(self.btn_safeguard)

        layout.addLayout(top_bar)
        layout.addSpacing(6)

        # 2. Hero Section (Image 1): Big Score "98" + Optimize Green Pill Button
        hero_layout = QHBoxLayout()
        hero_layout.setSpacing(18)

        self.score_label = QLabel("98")
        self.score_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 72px;
                font-weight: 800;
                line-height: 1.0;
            }
        """)
        hero_layout.addWidget(self.score_label)

        hero_layout.addStretch()

        self.btn_optimize = PillOptimizeButton("Optimize")
        self.btn_optimize.clicked.connect(self.open_optimize_requested.emit)
        hero_layout.addWidget(self.btn_optimize)

        layout.addLayout(hero_layout)

        # Segmented Progress Bar (Image 1 & 2)
        self.segmented_bar = SegmentedProgressBar(segments=4)
        layout.addWidget(self.segmented_bar)
        layout.addSpacing(10)

        # 3. 2x2 Modern Cards Grid (Matches Image 1)
        grid = QGridLayout()
        grid.setSpacing(16)

        # Card 1: Space Cleanup
        self.card_space = ModernCard()
        self.card_space.setCursor(Qt.PointingHandCursor)
        self.card_space.setMinimumHeight(150)
        c1_layout = QVBoxLayout(self.card_space)
        c1_layout.setContentsMargins(22, 18, 22, 18)
        c1_layout.setSpacing(10)

        lbl_c1_hdr = QLabel("Space cleanup")
        lbl_c1_hdr.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        lbl_c1_title = QLabel("Free up more space")
        lbl_c1_title.setStyleSheet("color: #FFFFFF; font-size: 17px; font-weight: 700;")

        self.storage_bar = QProgressBar()
        self.storage_bar.setRange(0, 100)
        self.storage_bar.setValue(68)
        self.storage_bar.setFixedHeight(12)
        self.storage_bar.setTextVisible(False)
        self.storage_bar.setStyleSheet("""
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

        self.lbl_available = QLabel("45.47 GB available")
        self.lbl_available.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: 600;")
        self.lbl_available.setAlignment(Qt.AlignRight)

        c1_layout.addWidget(lbl_c1_hdr)
        c1_layout.addWidget(lbl_c1_title)
        c1_layout.addWidget(self.storage_bar)
        c1_layout.addWidget(self.lbl_available)
        self.card_space.mousePressEvent = lambda e: self.open_space_requested.emit()
        grid.addWidget(self.card_space, 0, 0)

        # Card 2: Security Scan
        self.card_security = ModernCard()
        self.card_security.setCursor(Qt.PointingHandCursor)
        self.card_security.setMinimumHeight(150)
        c2_layout = QVBoxLayout(self.card_security)
        c2_layout.setContentsMargins(22, 18, 22, 18)
        c2_layout.setSpacing(8)

        lbl_c2_hdr = QLabel("Security scan")
        lbl_c2_hdr.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        lbl_c2_title = QLabel("Security")
        lbl_c2_title.setStyleSheet("color: #FFFFFF; font-size: 17px; font-weight: 700;")

        c2_bottom = QHBoxLayout()
        lbl_c2_sub = QLabel("Protected")
        lbl_c2_sub.setStyleSheet("color: #00E676; font-size: 15px; font-weight: 800;")
        c2_bottom.addWidget(lbl_c2_sub)
        c2_bottom.addStretch()

        self.signal_widget = StepSignalWidget(active_bars=4)
        c2_bottom.addWidget(self.signal_widget)

        c2_layout.addWidget(lbl_c2_hdr)
        c2_layout.addWidget(lbl_c2_title)
        c2_layout.addStretch()
        c2_layout.addLayout(c2_bottom)
        self.card_security.mousePressEvent = lambda e: self.open_security_requested.emit()
        grid.addWidget(self.card_security, 0, 1)

        # Card 3: Performance (AMD Ryzen 5 & RTX 3050)
        self.card_perf = ModernCard()
        self.card_perf.setCursor(Qt.PointingHandCursor)
        self.card_perf.setMinimumHeight(150)
        c3_layout = QVBoxLayout(self.card_perf)
        c3_layout.setContentsMargins(22, 18, 22, 18)
        c3_layout.setSpacing(8)

        lbl_c3_hdr = QLabel("Hardware & Performance")
        lbl_c3_hdr.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        lbl_c3_title = QLabel("AMD Ryzen 5 & RTX 3050")
        lbl_c3_title.setStyleSheet("color: #FFFFFF; font-size: 17px; font-weight: 700;")

        self.lbl_perf_stats = QLabel("CPU: 12% | GPU: 7% (40°C) | RAM: 11.7/24GB")
        self.lbl_perf_stats.setStyleSheet("color: #00D2FF; font-size: 13px; font-weight: 700;")

        c3_layout.addWidget(lbl_c3_hdr)
        c3_layout.addWidget(lbl_c3_title)
        c3_layout.addStretch()
        c3_layout.addWidget(self.lbl_perf_stats)
        self.card_perf.mousePressEvent = lambda e: self.open_performance_requested.emit()
        grid.addWidget(self.card_perf, 1, 0)

        # Card 4: Battery & Power Scheme
        self.card_batt = ModernCard()
        self.card_batt.setCursor(Qt.PointingHandCursor)
        self.card_batt.setMinimumHeight(150)
        c4_layout = QVBoxLayout(self.card_batt)
        c4_layout.setContentsMargins(22, 18, 22, 18)
        c4_layout.setSpacing(8)

        lbl_c4_hdr = QLabel("Power & Battery")
        lbl_c4_hdr.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")
        lbl_c4_title = QLabel("Battery Health")
        lbl_c4_title.setStyleSheet("color: #FFFFFF; font-size: 17px; font-weight: 700;")

        self.lbl_batt_status = QLabel("100% • Plugged in (Lenovo Balanced)")
        self.lbl_batt_status.setStyleSheet("color: #00E676; font-size: 13px; font-weight: 700;")

        c4_layout.addWidget(lbl_c4_hdr)
        c4_layout.addWidget(lbl_c4_title)
        c4_layout.addStretch()
        c4_layout.addWidget(self.lbl_batt_status)
        self.card_batt.mousePressEvent = lambda e: self.open_battery_requested.emit()
        grid.addWidget(self.card_batt, 1, 1)

        layout.addLayout(grid)
        layout.addSpacing(6)

        # 4. Recommended Tools Section (Image 1 Bottom)
        sec_tools_hdr = QLabel("RECOMMENDED SECURITY & OPTIMIZATION TOOLS")
        sec_tools_hdr.setStyleSheet("""
            color: #64748B;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.8px;
        """)
        layout.addWidget(sec_tools_hdr)

        tools_row = QHBoxLayout()
        tools_row.setSpacing(14)

        btn_t_quick = ToolButton("⚡ Quick Virus Scan")
        btn_t_quick.clicked.connect(lambda: self.open_virus_scan_requested.emit("quick"))

        btn_t_full = ToolButton("🛡️ Full System Virus Scan")
        btn_t_full.clicked.connect(lambda: self.open_virus_scan_requested.emit("full"))

        btn_t_clean = ToolButton("🧹 One-Click Junk Clean")
        btn_t_clean.clicked.connect(self.open_space_requested.emit)

        for b in [btn_t_quick, btn_t_full, btn_t_clean]:
            tools_row.addWidget(b)

        layout.addLayout(tools_row)

        w_layout.addWidget(container)
        w_layout.addStretch(1)

        scroll.setWidget(wrapper)
        root_layout.addWidget(scroll)

    def refresh_metrics(self):
        # 1. Health Score
        score = SystemOptimizer.calculate_health_score()
        self.score_label.setText(str(score))
        if score >= 90:
            self.segmented_bar.set_progress_level(3)
        elif score >= 75:
            self.segmented_bar.set_progress_level(2)
        else:
            self.segmented_bar.set_progress_level(1)

        # 2. Available Space
        free_gb = SpaceCleaner.get_primary_available_gb()
        self.lbl_available.setText(f"{free_gb:.2f} GB available")
        pct = min(100, int((free_gb / 512.0) * 100))
        self.storage_bar.setValue(pct)

        # 3. Hardware & Battery
        perf = PerformanceMonitor.get_live_metrics()
        self.lbl_perf_stats.setText(
            f"CPU: {perf['cpu_percent']}% | GPU: {perf['gpu']['utilization_pct']}% ({perf['gpu']['temp_c']}°C) | RAM: {perf['ram_used_gb']}/{perf['ram_total_gb']}GB"
        )

        batt = BatteryMonitor.get_battery_info()
        self.lbl_batt_status.setText(f"{batt['percent']}% • {batt['status_text']}")
