"""
TREVIORA AI DEFENDER - Utilities & Security Toolbox View
Matches the "Utilities" tab from Vivo iManager (Image 1 Bottom Nav).
Provides direct access to all defensive and optimization tools:
- Space Cleanup
- Security Scan
- Virus Scanner & Threat Destroyer
- SafeGuard 3-Layer Firewall
- Hardware & Live Performance (Lenovo LOQ)
- Battery & Power Scheme
- Quarantine Vault
- AI Security Assistant
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from treviora_defender.ui.animated_widgets import BrandHeaderWidget


class UtilitiesView(QWidget):
    open_space_requested = Signal()
    open_security_requested = Signal()
    open_virus_scan_requested = Signal(str)
    open_safeguard_requested = Signal()
    open_performance_requested = Signal()
    open_battery_requested = Signal()
    open_quarantine_requested = Signal()
    open_assistant_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 28)
        layout.setSpacing(16)

        # 1. Header
        top_bar = QHBoxLayout()
        self.brand_header = BrandHeaderWidget()
        top_bar.addWidget(self.brand_header)
        top_bar.addStretch()

        title = QLabel("Utilities & Security Toolbox")
        title.setObjectName("AppHeaderTitle")
        top_bar.addWidget(title)
        layout.addLayout(top_bar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(16)

        # 2. Grid of Tools
        grid = QGridLayout()
        grid.setSpacing(14)

        tools = [
            ("🧹 Space Cleanup", "Clean temp files, junk caches & duplicates", self.open_space_requested.emit),
            ("🛡️ Security Scan", "Scan network, apps & memory threats", self.open_security_requested.emit),
            ("🦠 Virus Destroyer", "Quick & Full AI scanning with shredder", lambda: self.open_virus_scan_requested.emit("quick")),
            ("⚡ SafeGuard Firewall", "Super-Power 3-layer cyber energy shield", self.open_safeguard_requested.emit),
            ("💻 Hardware Telemetry", "Live AMD Ryzen 5 & RTX 3050 monitor", self.open_performance_requested.emit),
            ("🔋 Power & Battery", "Battery health index & Windows power modes", self.open_battery_requested.emit),
            ("📦 Quarantine Vault", "Encrypted AES-GCM isolated file store", self.open_quarantine_requested.emit),
            ("🤖 AI Security Assistant", "Cybersecurity advice & threat explanation", self.open_assistant_requested.emit),
        ]

        for i, (tool_title, desc, slot) in enumerate(tools):
            card = QFrame()
            card.setProperty("class", "ModernCard")
            card.setCursor(Qt.PointingHandCursor)
            card.setFixedHeight(105)

            cl = QVBoxLayout(card)
            cl.setContentsMargins(18, 14, 18, 14)
            cl.setSpacing(4)

            lbl_t = QLabel(tool_title)
            lbl_t.setProperty("class", "CardTitleBold")
            lbl_d = QLabel(desc)
            lbl_d.setProperty("class", "CardDesc")

            cl.addWidget(lbl_t)
            cl.addWidget(lbl_d)
            cl.addStretch()

            card.mousePressEvent = lambda e, s=slot: s()
            grid.addWidget(card, i // 2, i % 2)

        c_layout.addLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
