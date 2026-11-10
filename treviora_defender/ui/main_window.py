"""
TREVIORA AI DEFENDER - Main Window
Exact 1000% Implementation of Reference Image (media_1794294858477_ccea698a.jpg)
Developer: TREVIORA INDUSTRY
Target: Lenovo LOQ | AMD Ryzen 5 | NVIDIA RTX 3050 6GB | 24GB RAM
Platform: Windows 11 Desktop
"""
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QMessageBox, QApplication,
    QSystemTrayIcon, QMenu, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QIcon, QFont, QAction

from treviora_defender.config.constants import APP_NAME, APP_VERSION, DEVELOPER, RESOURCES_DIR
from treviora_defender.config.settings import SettingsManager
from treviora_defender.monitoring.real_time_monitor import RealTimeMonitor
from treviora_defender.monitoring.process_monitor import ProcessMonitor
from treviora_defender.monitoring.ransomware_guard import RansomwareGuard
from treviora_defender.monitoring.usb_monitor import USBMonitor
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.core.telemetry_service import TelemetryService
from treviora_defender.utils.logger import get_logger

# Import the Desktop Reference Views & Components
from treviora_defender.ui.views.desktop_dashboard_view import DesktopDashboardView
from treviora_defender.ui.views.optimize_view import OptimizeView
from treviora_defender.ui.views.security_view import SecurityView
from treviora_defender.ui.views.space_view import SpaceView
from treviora_defender.ui.views.performance_view import PerformanceView
from treviora_defender.ui.views.battery_view import BatteryView
from treviora_defender.ui.views.safeguard_view import SafeGuardView
from treviora_defender.ui.views.virus_scan_view import VirusScanView
from treviora_defender.ui.views.utilities_view import UtilitiesView
from treviora_defender.ui.pages.quarantine_page import QuarantinePage
from treviora_defender.ui.pages.assistant_page import AssistantPage
from treviora_defender.ui.custom_components import CircularAvatarWidget, BrandHeaderWidget, SafeGuardPillButton
from treviora_defender.ui.cyber_dashboard_widgets import HoloShieldWidget

logger = get_logger()


class MonitorSignalBridge(QObject):
    file_alert = Signal(dict)
    process_alert = Signal(dict)
    ransomware_alert = Signal(dict)
    usb_alert = Signal(dict)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION} - {DEVELOPER}")
        self.resize(1400, 860)
        self.setMinimumSize(1200, 740)

        self.settings = SettingsManager()
        self.db = DatabaseManager()

        # Thread-safe Signal Bridge (eliminates background thread lag & UI lockups)
        self.bridge = MonitorSignalBridge()
        self.bridge.file_alert.connect(self._handle_file_alert_gui)
        self.bridge.process_alert.connect(self._handle_process_alert_gui)
        self.bridge.ransomware_alert.connect(self._handle_ransomware_alert_gui)
        self.bridge.usb_alert.connect(self._handle_usb_alert_gui)

        # Initialize background monitoring services
        self._init_monitors()

        # Build Full Desktop UI matching reference image
        self._init_ui()

        # System Tray setup
        self._setup_system_tray()

        # Start background monitors
        self.start_monitors()

    def _init_monitors(self):
        self.ransomware_guard = RansomwareGuard(alert_callback=self._on_ransomware_alert)
        self.real_time_monitor = RealTimeMonitor(event_callback=self._on_file_alert)
        self.process_monitor = ProcessMonitor(alert_callback=self._on_process_alert)
        self.usb_monitor = USBMonitor(insertion_callback=self._on_usb_inserted)

    def start_monitors(self):
        TelemetryService.get_instance().start()
        if self.settings.get("real_time_protection", True):
            self.real_time_monitor.start()
        self.process_monitor.start()
        self.ransomware_guard.start()
        if self.settings.get("usb_auto_scan", True):
            self.usb_monitor.start()

    def stop_monitors(self):
        TelemetryService.get_instance().stop()
        self.real_time_monitor.stop()
        self.process_monitor.stop()
        self.ransomware_guard.stop()
        self.usb_monitor.stop()

    def _init_ui(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #040814;")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Left Sidebar Navigation (Matches Reference Image)
        sidebar = self._create_sidebar()
        root_layout.addWidget(sidebar)

        # 2. Main Content Area (Top Header + Stacked Pages + Bottom Footer)
        content_box = QVBoxLayout()
        content_box.setContentsMargins(0, 0, 0, 0)
        content_box.setSpacing(0)

        # Top Header Bar
        top_bar = self._create_top_bar()
        content_box.addWidget(top_bar)

        # Central Stacked Views
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #040814;")

        # Page 0: Reference Desktop Dashboard View
        self.view_dashboard = DesktopDashboardView()
        self.stack.addWidget(self.view_dashboard)

        # Page 1: Security View
        self.view_security = SecurityView()
        self.stack.addWidget(self.view_security)

        # Page 2: Performance View
        self.view_perf = PerformanceView()
        self.stack.addWidget(self.view_perf)

        # Page 3: Space Cleanup / Optimization View
        self.view_space = SpaceView()
        self.stack.addWidget(self.view_space)

        # Page 4: Utilities / Tools View
        self.view_utilities = UtilitiesView()
        self.stack.addWidget(self.view_utilities)

        # Page 5: Optimize View
        self.view_optimize = OptimizeView()
        self.stack.addWidget(self.view_optimize)

        # Page 6: Battery View
        self.view_batt = BatteryView()
        self.stack.addWidget(self.view_batt)

        # Page 7: SafeGuard Firewall View
        self.view_safeguard = SafeGuardView()
        self.stack.addWidget(self.view_safeguard)

        # Page 8: Virus Scanner & Threat Destroyer View
        self.view_virus = VirusScanView()
        self.stack.addWidget(self.view_virus)

        # Page 9: Quarantine Page
        self.page_quarantine = QuarantinePage()
        self.stack.addWidget(self.page_quarantine)

        # Page 10: AI Security Assistant
        self.page_assistant = AssistantPage()
        self.stack.addWidget(self.page_assistant)

        content_box.addWidget(self.stack, 1)

        # Bottom Footer Bar
        footer = self._create_footer_bar()
        content_box.addWidget(footer)

        root_layout.addLayout(content_box, 1)

        # Wire all navigation signals
        self._wire_navigation()

    def _create_sidebar(self) -> QWidget:
        """Creates the left vertical sidebar matching the reference image."""
        sidebar = QFrame()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #060B18;
                border-right: 1px solid #10192D;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(14, 18, 14, 16)
        layout.setSpacing(10)

        # Top Logo + Brand (Reference Image Sidebar Top)
        top_brand = QVBoxLayout()
        top_brand.setAlignment(Qt.AlignCenter)
        top_brand.setSpacing(6)

        avatar = CircularAvatarWidget(size=46)
        top_brand.addWidget(avatar, 0, Qt.AlignCenter)

        lbl_b1 = QLabel("TREVIORA")
        lbl_b1.setStyleSheet("color: #FFFFFF; font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: 800; letter-spacing: 1.5px;")
        lbl_b1.setAlignment(Qt.AlignCenter)

        lbl_b2 = QLabel("INDUSTRY")
        lbl_b2.setStyleSheet("color: #00D2FF; font-family: 'Segoe UI', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 1.8px;")
        lbl_b2.setAlignment(Qt.AlignCenter)

        top_brand.addWidget(lbl_b1)
        top_brand.addWidget(lbl_b2)
        layout.addLayout(top_brand)
        layout.addSpacing(14)

        # Navigation Buttons (Pills with icons)
        self.nav_buttons = []
        nav_items = [
            ("🏠", "Dashboard", 0),
            ("🛡️", "Security", 1),
            ("⚡", "Performance", 2),
            ("🧹", "Optimization", 3),
            ("🛠️", "Tools", 4),
            ("⚙️", "Settings", 4),
            ("ℹ️", "About", 0),
        ]

        for icon, label, page_idx in nav_items:
            btn = QPushButton(f"  {icon}   {label}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(38)
            btn.clicked.connect(lambda _, idx=page_idx, b=btn: self._on_sidebar_nav_clicked(idx, b))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)

        # Set first button active (Glowing bright blue pill)
        self._set_active_sidebar_button(self.nav_buttons[0])

        layout.addStretch()

        # Bottom Holographic Card: "Your System Our Priority"
        card_prio = QFrame()
        card_prio.setFixedHeight(140)
        card_prio.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0F1D38, stop:1 #091326);
                border: 1px solid #1E2E4E;
                border-radius: 14px;
            }
        """)
        cp_layout = QVBoxLayout(card_prio)
        cp_layout.setContentsMargins(10, 10, 10, 10)
        cp_layout.setSpacing(4)
        cp_layout.setAlignment(Qt.AlignCenter)

        shield_small = HoloShieldWidget(size=64, show_lock=True, show_check=False)
        cp_layout.addWidget(shield_small, 0, Qt.AlignCenter)

        lbl_cp_title = QLabel("Your System\nOur Priority")
        lbl_cp_title.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: 800; line-height: 1.1;")
        lbl_cp_title.setAlignment(Qt.AlignCenter)

        lbl_cp_sub = QLabel("Stay Secure. Stay Productive.")
        lbl_cp_sub.setStyleSheet("color: #64748B; font-size: 9px;")
        lbl_cp_sub.setAlignment(Qt.AlignCenter)

        cp_layout.addWidget(lbl_cp_title)
        cp_layout.addWidget(lbl_cp_sub)
        layout.addWidget(card_prio)

        return sidebar

    def _set_active_sidebar_button(self, active_btn: QPushButton):
        inactive_style = """
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 600;
                border: none;
                border-radius: 19px;
                text-align: left;
                padding-left: 18px;
            }
            QPushButton:hover {
                background-color: #111B30;
                color: #00D2FF;
            }
        """
        active_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 800;
                border: none;
                border-radius: 19px;
                text-align: left;
                padding-left: 18px;
            }
        """
        for b in self.nav_buttons:
            b.setStyleSheet(inactive_style)
        active_btn.setStyleSheet(active_style)

    def _on_sidebar_nav_clicked(self, page_idx: int, btn: QPushButton):
        self._set_active_sidebar_button(btn)
        self.stack.setCurrentIndex(page_idx)

    def _create_top_bar(self) -> QWidget:
        """Creates top bar matching the reference image."""
        bar = QFrame()
        bar.setFixedHeight(54)
        bar.setStyleSheet("""
            QFrame {
                background-color: #050A17;
                border-bottom: 1px solid #10192D;
            }
        """)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)

        # Brand Header Widget (Circular avatar + TREVIORA INDUSTRY + Tagline)
        self.brand_header = BrandHeaderWidget()
        layout.addWidget(self.brand_header)

        layout.addStretch()

        # Right Controls (SafeGuard button, bell, theme, avatar)
        self.btn_safeguard = SafeGuardPillButton("🛡️ SafeGuard 3-Layer Firewall: ACTIVE ●")
        self.btn_safeguard.clicked.connect(self._open_safeguard_screen)
        layout.addWidget(self.btn_safeguard)

        # 1. Notification Bell Button (with live click handler)
        self.btn_bell = QPushButton("🔔")
        self.btn_bell.setToolTip("Security Notifications & Threat Feed")
        self.btn_bell.setCursor(Qt.PointingHandCursor)
        self.btn_bell.setStyleSheet("""
            QPushButton {
                background: #0D162B;
                color: #FFFFFF;
                border: 1px solid #1E2E4E;
                border-radius: 16px;
                font-size: 13px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                border: 1px solid #00D2FF;
                background: #132448;
            }
        """)
        self.btn_bell.clicked.connect(self._open_notifications_dialog)
        layout.addWidget(self.btn_bell)

        # 2. Theme / Brightness Toggle Button (with live click handler)
        self.is_stealth_mode = False
        self.btn_theme = QPushButton("🔅")
        self.btn_theme.setToolTip("Display Theme: Cyber Neon Mode (Click to toggle Stealth Night Mode)")
        self.btn_theme.setCursor(Qt.PointingHandCursor)
        self.btn_theme.setStyleSheet("""
            QPushButton {
                background: #0D162B;
                color: #FFFFFF;
                border: 1px solid #1E2E4E;
                border-radius: 16px;
                font-size: 13px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                border: 1px solid #00D2FF;
                background: #132448;
            }
        """)
        self.btn_theme.clicked.connect(self._toggle_theme_brightness)
        layout.addWidget(self.btn_theme)

        # 3. User Avatar Profile Button (with live click handler)
        self.btn_profile = QPushButton("👤")
        self.btn_profile.setToolTip("Operator Profile, Device Specs & Lifetime License")
        self.btn_profile.setCursor(Qt.PointingHandCursor)
        self.btn_profile.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0070F3, stop:1 #00D2FF);
                color: #FFFFFF;
                font-size: 14px;
                border-radius: 16px;
                border: 1px solid #00D2FF;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background: #00B0FF;
            }
        """)
        self.btn_profile.clicked.connect(self._open_user_profile_dialog)
        layout.addWidget(self.btn_profile)

        return bar

    def _create_footer_bar(self) -> QWidget:
        """Creates the bottom footer bar matching the reference image."""
        footer = QFrame()
        footer.setFixedHeight(30)
        footer.setStyleSheet("""
            QFrame {
                background-color: #030610;
                border-top: 1px solid #0E1626;
            }
        """)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(18, 0, 18, 0)

        # Left: TREVIORA INDUSTRY | Smart Security • Optimal Performance • Maximum Productivity
        lbl_f_brand = QLabel("TREVIORA INDUSTRY")
        lbl_f_brand.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 800; letter-spacing: 0.8px;")
        lbl_sep = QLabel("|")
        lbl_sep.setStyleSheet("color: #334155; font-size: 10px;")
        lbl_f_tag = QLabel("Smart Security • Optimal Performance • Maximum Productivity")
        lbl_f_tag.setStyleSheet("color: #64748B; font-size: 10px;")

        layout.addWidget(lbl_f_brand)
        layout.addWidget(lbl_sep)
        layout.addWidget(lbl_f_tag)
        layout.addStretch()

        # Right: All Systems Online | v2.1.0 | Signal bars
        lbl_online = QLabel("● All Systems Online")
        lbl_online.setStyleSheet("color: #00E676; font-size: 10px; font-weight: 700;")
        lbl_sep2 = QLabel("|")
        lbl_sep2.setStyleSheet("color: #334155; font-size: 10px;")
        lbl_ver = QLabel(f"v{APP_VERSION}")
        lbl_ver.setStyleSheet("color: #64748B; font-size: 10px;")
        lbl_sep3 = QLabel("|")
        lbl_sep3.setStyleSheet("color: #334155; font-size: 10px;")
        lbl_sig = QLabel("📶")
        lbl_sig.setStyleSheet("font-size: 10px;")

        layout.addWidget(lbl_online)
        layout.addWidget(lbl_sep2)
        layout.addWidget(lbl_ver)
        layout.addWidget(lbl_sep3)
        layout.addWidget(lbl_sig)

        return footer

    def _wire_navigation(self):
        # From Dashboard:
        self.view_dashboard.open_optimize_requested.connect(self._open_optimize_view)
        self.view_dashboard.open_space_requested.connect(lambda: self.switch_view(3))
        self.view_dashboard.open_security_requested.connect(lambda: self.switch_view(1))
        self.view_dashboard.open_performance_requested.connect(lambda: self.switch_view(2))
        self.view_dashboard.open_battery_requested.connect(lambda: self.switch_view(6))
        self.view_dashboard.open_virus_scan_requested.connect(self.go_to_virus_scan)
        self.view_dashboard.open_tools_requested.connect(lambda: self.switch_view(4))

        # From Utilities:
        self.view_utilities.open_space_requested.connect(lambda: self.switch_view(3))
        self.view_utilities.open_security_requested.connect(lambda: self.switch_view(1))
        self.view_utilities.open_virus_scan_requested.connect(self.go_to_virus_scan)
        self.view_utilities.open_safeguard_requested.connect(lambda: self.switch_view(7))
        self.view_utilities.open_performance_requested.connect(lambda: self.switch_view(2))
        self.view_utilities.open_battery_requested.connect(lambda: self.switch_view(6))
        self.view_utilities.open_quarantine_requested.connect(lambda: self.switch_view(9))
        self.view_utilities.open_assistant_requested.connect(lambda: self.switch_view(10))

        # Back buttons:
        self.view_optimize.back_requested.connect(lambda: self.switch_view(0))
        self.view_security.back_requested.connect(lambda: self.switch_view(0))
        self.view_space.back_requested.connect(lambda: self.switch_view(0))
        self.view_perf.back_requested.connect(lambda: self.switch_view(0))
        self.view_batt.back_requested.connect(lambda: self.switch_view(0))
        self.view_safeguard.back_requested.connect(lambda: self.switch_view(0))
        self.view_safeguard.shield_state_changed.connect(self._on_safeguard_state_changed)
        self.view_virus.back_requested.connect(lambda: self.switch_view(0))

    def switch_view(self, index: int):
        self.stack.setCurrentIndex(index)
        # Update sidebar active state if matches main pages
        if index < len(self.nav_buttons):
            self._set_active_sidebar_button(self.nav_buttons[index])

    def go_to_dashboard(self):
        self.switch_view(0)

    def _open_optimize_view(self):
        self.switch_view(5)
        self.view_optimize.start_optimization()

    def _open_safeguard_screen(self):
        new_state = not self.view_safeguard.guard.is_active
        self.view_safeguard.set_shield_active(new_state)
        self.btn_safeguard.set_shield_active(new_state)
        self.switch_view(7)
        if new_state:
            self.view_safeguard.launch_desktop_shield_overlay()
        else:
            if hasattr(self, "tray") and self.tray.isVisible():
                self.tray.showMessage(
                    "SafeGuard Firewall",
                    "SafeGuard 3-Layer Firewall has been set to STANDBY (DEACTIVATED).",
                    QSystemTrayIcon.Warning,
                    2500
                )

    def _on_safeguard_state_changed(self, active: bool):
        self.btn_safeguard.set_shield_active(active)

    def _open_notifications_dialog(self):
        """Opens the Cyberpunk Security Notifications & Intel dialog (Bell button)."""
        from treviora_defender.ui.header_dialogs import SecurityNotificationsDialog
        self.notif_dialog = SecurityNotificationsDialog(self)
        if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
            self.notif_dialog.show()
        else:
            self.notif_dialog.exec()

    def _toggle_theme_brightness(self):
        """Toggles between Cyber Neon Mode (🔅) and Stealth Obsidian Night Mode (🌙)."""
        self.is_stealth_mode = not getattr(self, "is_stealth_mode", False)
        if self.is_stealth_mode:
            self.btn_theme.setText("🌙")
            self.btn_theme.setToolTip("Display Theme: Stealth Obsidian Night Mode (Click for Cyber Neon)")
            self.setStyleSheet("""
                QMainWindow, QWidget#CentralWidget {
                    background-color: #020409;
                }
            """)
            if hasattr(self, "tray") and self.tray.isVisible():
                self.tray.showMessage("Theme Mode", "Stealth Obsidian Night Mode (Zero-Glare OLED)", QSystemTrayIcon.Information, 1500)
        else:
            self.btn_theme.setText("🔅")
            self.btn_theme.setToolTip("Display Theme: Cyber Neon Mode (Click for Stealth Night Mode)")
            from treviora_defender.ui.styles import MAIN_STYLE
            self.setStyleSheet(MAIN_STYLE)
            if hasattr(self, "tray") and self.tray.isVisible():
                self.tray.showMessage("Theme Mode", "Cyber Neon Matrix Mode Activated", QSystemTrayIcon.Information, 1500)

    def _open_user_profile_dialog(self):
        """Opens the Operator Profile, Device Hardware Specs & Lifetime License dialog (User Avatar)."""
        from treviora_defender.ui.header_dialogs import UserProfileDialog
        self.user_dialog = UserProfileDialog(self)
        if os.environ.get("QT_QPA_PLATFORM") == "offscreen":
            self.user_dialog.show()
        else:
            self.user_dialog.exec()

    def go_to_virus_scan(self, mode: str = "quick"):
        self.switch_view(8)
        self.view_virus.start_scan(mode)

    # Background Monitor Callbacks (Safe Bridge Dispatch)
    def _on_file_alert(self, alert_data: dict):
        self.bridge.file_alert.emit(alert_data)

    def _on_process_alert(self, alert_data: dict):
        self.bridge.process_alert.emit(alert_data)

    def _on_ransomware_alert(self, alert_data: dict):
        self.bridge.ransomware_alert.emit(alert_data)

    def _on_usb_inserted(self, usb_data: dict):
        self.bridge.usb_alert.emit(usb_data)

    def _handle_file_alert_gui(self, alert: dict):
        logger.info(f"File Alert: {alert}")
        self.view_dashboard.refresh_metrics()

    def _handle_process_alert_gui(self, alert: dict):
        logger.warning(f"Process Alert: {alert}")
        self.view_dashboard.refresh_metrics()

    def _handle_ransomware_alert_gui(self, alert: dict):
        logger.critical(f"Ransomware Guard Triggered: {alert}")
        self.view_dashboard.refresh_metrics()
        QMessageBox.critical(
            self,
            "CRITICAL: Ransomware Behavior Detected!",
            f"Treviora Ransomware Guard detected suspicious mass file activity:\n\n"
            f"{alert.get('description', 'Decoy canary files altered')}\n\n"
            "Active protection has isolated the offending path."
        )

    def _handle_usb_alert_gui(self, usb_data: dict):
        logger.info(f"USB Insertion Event: {usb_data}")
        drive = usb_data.get("drive", "")
        if drive:
            self.go_to_virus_scan("custom")
            self.view_virus.start_scan("custom", drive)

    def _setup_system_tray(self):
        icon_path = RESOURCES_DIR / "icon.png"
        tray_icon = QIcon(str(icon_path)) if icon_path.exists() else self.windowIcon()

        self.tray = QSystemTrayIcon(tray_icon, self)
        self.tray.setToolTip(f"{APP_NAME} - Real-Time Shield Active")

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #0F172A;
                color: #E2E8F0;
                border: 1px solid #1E293B;
                padding: 4px;
            }
            QMenu::item:selected {
                background-color: #0070F3;
                color: #FFFFFF;
            }
        """)

        act_dashboard = menu.addAction("📊 Open Dashboard")
        act_dashboard.triggered.connect(lambda: (self.show_window(), self.switch_view(0)))

        act_scan = menu.addAction("⚡ Run Quick Scan")
        act_scan.triggered.connect(lambda: (self.show_window(), self.go_to_virus_scan("quick")))

        act_quar = menu.addAction("📦 Quarantine Vault")
        act_quar.triggered.connect(lambda: (self.show_window(), self.switch_view(9)))

        menu.addSeparator()

        act_exit = menu.addAction("❌ Exit Treviora Defender")
        act_exit.triggered.connect(self.quit_app)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _on_tray_activated(self, reason):
        if reason in [QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick]:
            self.show_window()

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def quit_app(self):
        self.stop_monitors()
        self.tray.hide()
        QApplication.quit()

    def closeEvent(self, event):
        if self.settings.get("minimize_to_tray", False) and hasattr(self, "tray") and self.tray.isVisible():
            self.hide()
            self.tray.showMessage(
                APP_NAME,
                "Treviora AI Defender continues protecting your endpoint in the background.",
                QSystemTrayIcon.Information,
                2000
            )
            event.ignore()
        else:
            self.stop_monitors()
            if hasattr(self, "tray"):
                self.tray.hide()
            event.accept()
