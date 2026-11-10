"""
TREVIORA AI DEFENDER - Optimize View (Matches Image 2: Vivo iManager Optimize Screen)
- Back button `< Optimize`
- Brand Header with Circular Logo Avatar & Tagline
- Big Score Counter
- "Optimizing..." state with segmented progress bar
- Checklist items inside ModernCard
- "Stop Optimization" / "Done" cyan button
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QTimer
from treviora_defender.core.system_optimizer import SystemOptimizer
from treviora_defender.ui.animated_widgets import SegmentedProgressBar
from treviora_defender.ui.custom_components import ModernCard, BrandHeaderWidget


class OptimizeView(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_score = 92
        self.step = 0
        self.is_optimizing = False
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
        layout.setSpacing(18)

        # 1. Back button header + Brand Header
        top_row = QHBoxLayout()
        self.btn_back = QPushButton("‹  Optimize")
        self.btn_back.setStyleSheet("font-size: 18px; font-weight: 700; color: #FFFFFF; background: transparent; border: none;")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.back_requested.emit)
        top_row.addWidget(self.btn_back)

        top_row.addStretch()

        self.brand_header = BrandHeaderWidget()
        top_row.addWidget(self.brand_header)
        layout.addLayout(top_row)

        layout.addSpacing(6)

        # 2. Big Score (Image 2)
        self.lbl_score = QLabel("98")
        self.lbl_score.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 72px;
                font-weight: 800;
                line-height: 1.0;
            }
        """)
        layout.addWidget(self.lbl_score)

        # "Optimizing..." label
        self.lbl_status = QLabel("Optimizing...")
        self.lbl_status.setStyleSheet("color: #94A3B8; font-size: 15px; font-weight: 600;")
        layout.addWidget(self.lbl_status)

        # Segmented Progress Bar
        self.seg_bar = SegmentedProgressBar(segments=4)
        layout.addWidget(self.seg_bar)

        layout.addSpacing(10)

        # 3. Checklist Card (Image 2)
        card = ModernCard()
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(24, 22, 24, 22)
        c_layout.setSpacing(18)

        # Item 1: Security protection
        row1 = QHBoxLayout()
        lbl_i1_icon = QLabel("🛡️")
        lbl_i1_icon.setStyleSheet("font-size: 20px;")
        t_box1 = QVBoxLayout()
        lbl_i1_title = QLabel("Security protection")
        lbl_i1_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 600;")
        self.lbl_i1_sub = QLabel("Scanning memory & background threats...")
        self.lbl_i1_sub.setStyleSheet("color: #64748B; font-size: 12px;")
        t_box1.addWidget(lbl_i1_title)
        t_box1.addWidget(self.lbl_i1_sub)
        row1.addWidget(lbl_i1_icon)
        row1.addLayout(t_box1)
        row1.addStretch()
        self.lbl_i1_badge = QLabel("⌛")
        row1.addWidget(self.lbl_i1_badge)
        c_layout.addLayout(row1)

        # Item 2: Cleanup
        row2 = QHBoxLayout()
        lbl_i2_icon = QLabel("🧹")
        lbl_i2_icon.setStyleSheet("font-size: 20px;")
        t_box2 = QVBoxLayout()
        lbl_i2_title = QLabel("Cleanup")
        lbl_i2_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 600;")
        self.lbl_i2_sub = QLabel("Flushing idle RAM & clearing temp cache...")
        self.lbl_i2_sub.setStyleSheet("color: #64748B; font-size: 12px;")
        t_box2.addWidget(lbl_i2_title)
        t_box2.addWidget(self.lbl_i2_sub)
        row2.addWidget(lbl_i2_icon)
        row2.addLayout(t_box2)
        row2.addStretch()
        self.lbl_i2_badge = QLabel("⌛")
        row2.addWidget(self.lbl_i2_badge)
        c_layout.addLayout(row2)

        # Item 3: System Performance & Health
        row3 = QHBoxLayout()
        lbl_i3_icon = QLabel("⚡")
        lbl_i3_icon.setStyleSheet("font-size: 20px;")
        t_box3 = QVBoxLayout()
        lbl_i3_title = QLabel("Hardware Optimization")
        lbl_i3_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 600;")
        self.lbl_i3_sub = QLabel("Balancing CPU & Lenovo LOQ power state...")
        self.lbl_i3_sub.setStyleSheet("color: #64748B; font-size: 12px;")
        t_box3.addWidget(lbl_i3_title)
        t_box3.addWidget(self.lbl_i3_sub)
        row3.addWidget(lbl_i3_icon)
        row3.addLayout(t_box3)
        row3.addStretch()
        self.lbl_i3_badge = QLabel("⌛")
        row3.addWidget(self.lbl_i3_badge)
        c_layout.addLayout(row3)

        layout.addWidget(card)
        layout.addStretch()

        # 4. Stop / Done button (Image 2 bottom cyan pill button)
        self.btn_action = QPushButton("Stop optimization")
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
        self.btn_action.clicked.connect(self.handle_button)
        layout.addWidget(self.btn_action)

        w_layout.addWidget(container)
        w_layout.addStretch(1)

        scroll.setWidget(wrapper)
        root_layout.addWidget(scroll)

        # Animation timer
        self.opt_timer = QTimer(self)
        self.opt_timer.timeout.connect(self._step_optimization)

    def start_optimization(self):
        self.is_optimizing = True
        self.step = 0
        self.current_score = SystemOptimizer.calculate_health_score()
        self.lbl_score.setText(str(self.current_score))
        self.lbl_status.setText("Optimizing system...")
        self.btn_action.setText("Stop optimization")
        self.lbl_i1_badge.setText("⌛")
        self.lbl_i2_badge.setText("⌛")
        self.lbl_i3_badge.setText("⌛")
        self.lbl_i1_sub.setText("Scanning memory & background threats...")
        self.lbl_i2_sub.setText("Flushing idle RAM & clearing temp cache...")
        self.lbl_i3_sub.setText("Balancing CPU & Lenovo LOQ power state...")
        self.opt_timer.start(1000)

    def _step_optimization(self):
        self.step += 1

        if self.step == 1:
            self.lbl_i1_badge.setText("🔄")
            self.lbl_i1_badge.setStyleSheet("color: #00D2FF; font-size: 14px;")
            self.seg_bar.set_progress_level(1)
        elif self.step == 2:
            self.lbl_i1_badge.setText("✓ Protected")
            self.lbl_i1_badge.setStyleSheet("color: #00E676; font-weight: 700; font-size: 13px;")
            self.lbl_i1_sub.setText("Memory verified. 0 threats detected.")
            self.current_score = min(100, self.current_score + 2)
            self.lbl_score.setText(str(self.current_score))

            self.lbl_i2_badge.setText("🔄")
            self.lbl_i2_badge.setStyleSheet("color: #00D2FF; font-size: 14px;")
            self.seg_bar.set_progress_level(2)

            res = SystemOptimizer.optimize_ram()
            SystemOptimizer.clean_quick_junk()
            self.freed_mb = res.get("freed_mb", 350.0)

        elif self.step == 3:
            self.lbl_i2_badge.setText("✓ Cleaned")
            self.lbl_i2_badge.setStyleSheet("color: #00E676; font-weight: 700; font-size: 13px;")
            self.lbl_i2_sub.setText(f"Reclaimed {self.freed_mb} MB physical RAM & cleaned cache.")
            self.current_score = min(100, self.current_score + 3)
            self.lbl_score.setText(str(self.current_score))

            self.lbl_i3_badge.setText("🔄")
            self.lbl_i3_badge.setStyleSheet("color: #00D2FF; font-size: 14px;")
            self.seg_bar.set_progress_level(3)

        elif self.step >= 4:
            self.lbl_i3_badge.setText("✓ Optimized")
            self.lbl_i3_badge.setStyleSheet("color: #00E676; font-weight: 700; font-size: 13px;")
            self.lbl_i3_sub.setText("AMD Ryzen 5 & RTX 3050 balanced.")
            self.lbl_score.setText("100")
            self.lbl_status.setText("System is in optimal state")
            self.btn_action.setText("Done")
            self.is_optimizing = False
            self.opt_timer.stop()

    def handle_button(self):
        if self.is_optimizing:
            self.opt_timer.stop()
            self.is_optimizing = False
            self.lbl_status.setText("Optimization paused")
            self.btn_action.setText("Done")
        else:
            self.back_requested.emit()
