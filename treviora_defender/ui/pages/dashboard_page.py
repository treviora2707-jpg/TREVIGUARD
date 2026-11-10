"""
TREVIORA AI DEFENDER - Page 1: Main Security Dashboard
Displays Protection Status, Real-Time Threat Monitoring, Quick/Full Scan Buttons,
System Security Score Meter, Threat Statistics, Recent Events, and AI Assistant Panel.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.ui.components.status_card import MetricCard, CircularScoreWidget


class DashboardPage(QWidget):
    # Signals to request navigation or scan start from MainWindow
    quick_scan_requested = Signal()
    full_scan_requested = Signal()
    navigate_requested = Signal(int)

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
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
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(20)

        # Header Title Banner
        header_row = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Security Operations Center")
        title.setProperty("class", "PageTitle")
        sub = QLabel("Real-Time AI-Driven Windows 11 Endpoint Protection • TREVIORA INDUSTRY")
        sub.setProperty("class", "PageSubtitle")
        title_box.addWidget(title)
        title_box.addWidget(sub)
        header_row.addLayout(title_box)
        header_row.addStretch()

        # Action Buttons
        self.btn_quick = QPushButton("⚡ Quick Scan")
        self.btn_quick.setProperty("class", "PrimaryButton")
        self.btn_quick.setCursor(Qt.PointingHandCursor)
        self.btn_quick.clicked.connect(self.quick_scan_requested.emit)

        self.btn_full = QPushButton("🛡️ Full System Scan")
        self.btn_full.setProperty("class", "SecondaryButton")
        self.btn_full.setCursor(Qt.PointingHandCursor)
        self.btn_full.clicked.connect(self.full_scan_requested.emit)

        header_row.addWidget(self.btn_quick)
        header_row.addWidget(self.btn_full)
        main_layout.addLayout(header_row)

        # Top Banner: Protection Status & Security Score Card
        hero_frame = QFrame()
        hero_frame.setProperty("class", "GlassCardHighlight")
        hero_layout = QHBoxLayout(hero_frame)
        hero_layout.setContentsMargins(24, 20, 24, 20)

        # Circular score
        self.score_widget = CircularScoreWidget(98)
        hero_layout.addWidget(self.score_widget)

        hero_text = QVBoxLayout()
        hero_text.setSpacing(6)
        self.shield_status = QLabel("SYSTEM SHIELD ACTIVE & SECURE")
        self.shield_status.setStyleSheet("color: #10B981; font-size: 18px; font-weight: 800; letter-spacing: 0.5px;")

        self.shield_desc = QLabel(
            "Treviora AI real-time monitoring and ransomware guard are actively protecting your system.\n"
            "Coexisting smoothly with Microsoft Defender and Windows Security."
        )
        self.shield_desc.setStyleSheet("color: #94A3B8; font-size: 12px; line-height: 1.4;")

        hero_text.addWidget(self.shield_status)
        hero_text.addWidget(self.shield_desc)
        hero_layout.addLayout(hero_text)
        hero_layout.addStretch()

        # Fast diagnostic button
        ai_diag_btn = QPushButton("Ask AI Assistant")
        ai_diag_btn.setProperty("class", "SecondaryButton")
        ai_diag_btn.clicked.connect(lambda: self.navigate_requested.emit(5)) # Page 6: AI Assistant
        hero_layout.addWidget(ai_diag_btn)

        main_layout.addWidget(hero_frame)

        # Metric Cards Grid
        grid = QGridLayout()
        grid.setSpacing(16)

        self.card_active = MetricCard("Active Threats", "0", "Requires zero action", "#10B981")
        self.card_scanned = MetricCard("Files Scanned", "0", "Across all scan tasks", "#00D2FF")
        self.card_quar = MetricCard("Quarantine Vault", "0", "Encrypted & Isolated", "#F59E0B")
        self.card_scans = MetricCard("Total Scans Run", "0", "Historical audits", "#38BDF8")

        grid.addWidget(self.card_active, 0, 0)
        grid.addWidget(self.card_scanned, 0, 1)
        grid.addWidget(self.card_quar, 0, 2)
        grid.addWidget(self.card_scans, 0, 3)
        main_layout.addLayout(grid)

        # Split Section: Recent Security Events & AI Advisory Panel
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(16)

        # Left: Recent Events Table
        events_frame = QFrame()
        events_frame.setProperty("class", "GlassCard")
        events_box = QVBoxLayout(events_frame)
        events_box.setContentsMargins(16, 14, 16, 14)

        events_title = QLabel("Recent Security Events")
        events_title.setProperty("class", "CardTitle")
        events_box.addWidget(events_title)

        self.events_table = QTableWidget()
        self.events_table.setColumnCount(3)
        self.events_table.setHorizontalHeaderLabels(["Timestamp", "Source", "Description"])
        self.events_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.events_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.events_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.events_table.verticalHeader().setVisible(False)
        self.events_table.setFixedHeight(180)
        events_box.addWidget(self.events_table)
        bottom_row.addWidget(events_frame, 2)

        # Right: AI Quick Insights Panel
        ai_frame = QFrame()
        ai_frame.setProperty("class", "GlassCard")
        ai_box = QVBoxLayout(ai_frame)
        ai_box.setContentsMargins(16, 14, 16, 14)
        ai_box.setSpacing(8)

        ai_title = QLabel("AI Threat Intelligence Insights")
        ai_title.setProperty("class", "CardTitle")
        ai_box.addWidget(ai_title)

        self.ai_insight_label = QLabel(
            "• Machine Learning PE model loaded.\n"
            "• Built-in YARA signature database initialized.\n"
            "• Zero unresolved threat anomalies currently detected.\n"
            "• Primary device optimized: AMD Ryzen 5 & NVIDIA RTX 3050."
        )
        self.ai_insight_label.setStyleSheet("color: #CBD5E1; font-size: 12px; line-height: 1.5;")
        self.ai_insight_label.setWordWrap(True)
        ai_box.addWidget(self.ai_insight_label)
        ai_box.addStretch()

        bottom_row.addWidget(ai_frame, 1)
        main_layout.addLayout(bottom_row)

        scroll.setWidget(container)
        root_layout.addWidget(scroll)

        self.refresh_data()

    def refresh_data(self):
        stats = self.db.get_dashboard_stats()
        active = stats.get("active_threats", 0)
        self.card_active.set_value(str(active))
        if active > 0:
            self.card_active.value_label.setStyleSheet("color: #EF4444; font-size: 26px; font-weight: 800;")
            self.shield_status.setText(f"ATTENTION: {active} ACTIVE THREAT(S) DETECTED")
            self.shield_status.setStyleSheet("color: #EF4444; font-size: 18px; font-weight: 800;")
            self.score_widget.set_score(max(40, 100 - active * 20))
        else:
            self.card_active.value_label.setStyleSheet("color: #10B981; font-size: 26px; font-weight: 800;")
            self.shield_status.setText("SYSTEM SHIELD ACTIVE & SECURE")
            self.shield_status.setStyleSheet("color: #10B981; font-size: 18px; font-weight: 800;")
            self.score_widget.set_score(98)

        self.card_scanned.set_value(f"{stats.get('total_scanned', 0):,}")
        self.card_quar.set_value(str(stats.get("quarantined_count", 0)))
        self.card_scans.set_value(str(stats.get("total_scans", 0)))

        # Refresh recent events
        events = self.db.get_recent_events(limit=8)
        self.events_table.setRowCount(0)
        for r, ev in enumerate(events):
            self.events_table.insertRow(r)
            ts = ev.get("timestamp", "").replace("T", " ")[:19]
            self.events_table.setItem(r, 0, QTableWidgetItem(ts))
            self.events_table.setItem(r, 1, QTableWidgetItem(ev.get("source", "System")))
            self.events_table.setItem(r, 2, QTableWidgetItem(ev.get("description", "")))
