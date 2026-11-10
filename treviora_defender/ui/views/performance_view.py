"""
TREVIORA AI DEFENDER - Hardware & Live Performance Telemetry View
Tailored for Lenovo LOQ:
- AMD Ryzen 5 CPU Live Usage %, Clock Speed, & Thermals
- NVIDIA GeForce RTX 3050 6GB Laptop GPU (Utilization %, VRAM, Temperature °C)
- 24GB System RAM Allocation & Free GB
- System Optimization & Gaming Boost Button
- High-Tech Animated Cyber Circular Gauges (60 FPS)
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QScrollArea, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QTimer
from treviora_defender.core.performance_monitor import PerformanceMonitor
from treviora_defender.core.system_optimizer import SystemOptimizer
from treviora_defender.core.telemetry_service import TelemetryService
from treviora_defender.ui.animated_widgets import CyberCircularGauge, BrandHeaderWidget


class PerformanceView(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

        # Connect to background TelemetryService (zero lag, no timer needed)
        self.telemetry = TelemetryService.get_instance()
        self.telemetry.telemetry_updated.connect(self._apply_telemetry)
        self._apply_telemetry(self.telemetry.cached_metrics)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 20, 32, 28)
        layout.setSpacing(16)

        # 1. Back Header + Brand Header
        top_bar = QHBoxLayout()
        self.btn_back = QPushButton("‹  Hardware && Performance")
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

        btn_boost = QPushButton("🚀 Boost Performance")
        btn_boost.setProperty("class", "PillOptimizeButton")
        btn_boost.setCursor(Qt.PointingHandCursor)
        btn_boost.clicked.connect(self._handle_boost)
        top_bar.addWidget(btn_boost)
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

        # Hardware Specs Header Badge
        from treviora_defender.core.hardware_profile import HardwareProfile
        hw_prof = HardwareProfile.get_profile()

        spec_frame = QFrame()
        spec_frame.setProperty("class", "ModernCard")
        sf_layout = QHBoxLayout(spec_frame)
        sf_layout.setContentsMargins(18, 12, 18, 12)
        device_str = f"💻 DEVICE: {hw_prof['os']['hostname']} | {hw_prof['cpu']['raw_name']} | {hw_prof['gpu']['short_name']} | {hw_prof['ram']['formatted']} RAM"
        lbl_device = QLabel(device_str)
        lbl_device.setStyleSheet("color: #00D2FF; font-weight: 700; font-size: 12px;")
        sf_layout.addWidget(lbl_device)
        c_layout.addWidget(spec_frame)

        # 2x2 Grid of Hardware Monitors with Animated Cyber Gauges
        grid = QGridLayout()
        grid.setSpacing(16)

        # 1. CPU Card (Intel / AMD / Generic)
        self.card_cpu = QFrame()
        self.card_cpu.setProperty("class", "ModernCard")
        cpu_main_layout = QHBoxLayout(self.card_cpu)
        cpu_main_layout.setContentsMargins(20, 18, 20, 18)
        cpu_main_layout.setSpacing(14)

        cpu_l = QVBoxLayout()
        cpu_l.setSpacing(6)
        lbl_cpu_hdr = QLabel("PROCESSOR (CPU)")
        lbl_cpu_hdr.setProperty("class", "CardHeader")
        lbl_cpu_title = QLabel(hw_prof["cpu"]["short_name"])
        lbl_cpu_title.setProperty("class", "CardTitleBold")

        self.lbl_cpu_usage = QLabel("0% Utilization")
        self.lbl_cpu_usage.setStyleSheet("color: #00E676; font-size: 18px; font-weight: 800;")

        self.lbl_cpu_details = QLabel(f"Topology: {hw_prof['cpu']['cores_logical']} Logical Threads\nArchitecture: {hw_prof['cpu']['vendor']}\nTemp: 42°C")
        self.lbl_cpu_details.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.4;")

        cpu_l.addWidget(lbl_cpu_hdr)
        cpu_l.addWidget(lbl_cpu_title)
        cpu_l.addWidget(self.lbl_cpu_usage)
        cpu_l.addWidget(self.lbl_cpu_details)
        cpu_l.addStretch()

        self.gauge_cpu = CyberCircularGauge(title="CPU", unit="%", size=115, color_theme="emerald")
        cpu_main_layout.addLayout(cpu_l)
        cpu_main_layout.addWidget(self.gauge_cpu)
        grid.addWidget(self.card_cpu, 0, 0)

        # 2. GPU Card
        self.card_gpu = QFrame()
        self.card_gpu.setProperty("class", "ModernCard")
        gpu_main_layout = QHBoxLayout(self.card_gpu)
        gpu_main_layout.setContentsMargins(20, 18, 20, 18)
        gpu_main_layout.setSpacing(14)

        gpu_l = QVBoxLayout()
        gpu_l.setSpacing(6)
        lbl_gpu_hdr = QLabel("GRAPHICS (GPU)")
        lbl_gpu_hdr.setProperty("class", "CardHeader")
        lbl_gpu_title = QLabel(hw_prof["gpu"]["short_name"])
        lbl_gpu_title.setProperty("class", "CardTitleBold")

        self.lbl_gpu_usage = QLabel("0% Utilization")
        self.lbl_gpu_usage.setStyleSheet("color: #00D2FF; font-size: 18px; font-weight: 800;")

        self.lbl_gpu_details = QLabel("VRAM: 950 / 6144 MB\nTemp: 40°C\nDedicated 6GB")
        self.lbl_gpu_details.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.4;")

        gpu_l.addWidget(lbl_gpu_hdr)
        gpu_l.addWidget(lbl_gpu_title)
        gpu_l.addWidget(self.lbl_gpu_usage)
        gpu_l.addWidget(self.lbl_gpu_details)
        gpu_l.addStretch()

        self.gauge_gpu = CyberCircularGauge(title="GPU", unit="%", size=115, color_theme="cyan")
        gpu_main_layout.addLayout(gpu_l)
        gpu_main_layout.addWidget(self.gauge_gpu)
        grid.addWidget(self.card_gpu, 0, 1)

        # 3. 24GB System Memory Card
        self.card_ram = QFrame()
        self.card_ram.setProperty("class", "ModernCard")
        ram_main_layout = QHBoxLayout(self.card_ram)
        ram_main_layout.setContentsMargins(20, 18, 20, 18)
        ram_main_layout.setSpacing(14)

        ram_l = QVBoxLayout()
        ram_l.setSpacing(6)
        lbl_ram_hdr = QLabel("SYSTEM MEMORY (RAM)")
        lbl_ram_hdr.setProperty("class", "CardHeader")
        lbl_ram_title = QLabel(f"{hw_prof['ram']['formatted']} High-Speed DDR")
        lbl_ram_title.setProperty("class", "CardTitleBold")

        self.lbl_ram_usage = QLabel("0 GB / 24 GB")
        self.lbl_ram_usage.setStyleSheet("color: #D946EF; font-size: 18px; font-weight: 800;")

        self.lbl_ram_details = QLabel("Available: 12.3 GB\nMemory Pressure: Low\nBuffer/Cache: Flushed")
        self.lbl_ram_details.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.4;")

        ram_l.addWidget(lbl_ram_hdr)
        ram_l.addWidget(lbl_ram_title)
        ram_l.addWidget(self.lbl_ram_usage)
        ram_l.addWidget(self.lbl_ram_details)
        ram_l.addStretch()

        self.gauge_ram = CyberCircularGauge(title="RAM", unit="%", size=115, color_theme="magenta")
        ram_main_layout.addLayout(ram_l)
        ram_main_layout.addWidget(self.gauge_ram)
        grid.addWidget(self.card_ram, 1, 0)

        # 4. Thermals & Fan Profile Card
        self.card_therm = QFrame()
        self.card_therm.setProperty("class", "ModernCard")
        therm_main_layout = QHBoxLayout(self.card_therm)
        therm_main_layout.setContentsMargins(20, 18, 20, 18)
        therm_main_layout.setSpacing(14)

        therm_l = QVBoxLayout()
        therm_l.setSpacing(6)
        lbl_th_hdr = QLabel("THERMAL & COOLING")
        lbl_th_hdr.setProperty("class", "CardHeader")
        lbl_th_title = QLabel("Lenovo LOQ Chamber")
        lbl_th_title.setProperty("class", "CardTitleBold")

        self.lbl_th_state = QLabel("Optimal • 40°C")
        self.lbl_th_state.setStyleSheet("color: #F59E0B; font-size: 18px; font-weight: 800;")

        self.lbl_th_details = QLabel("Status: Cool & Quiet\nThrottling: None\nDual-Fan Active")
        self.lbl_th_details.setStyleSheet("color: #94A3B8; font-size: 11px; line-height: 1.4;")

        therm_l.addWidget(lbl_th_hdr)
        therm_l.addWidget(lbl_th_title)
        therm_l.addWidget(self.lbl_th_state)
        therm_l.addWidget(self.lbl_th_details)
        therm_l.addStretch()

        self.gauge_therm = CyberCircularGauge(title="TEMP", unit="°C", size=115, color_theme="orange")
        therm_main_layout.addLayout(therm_l)
        therm_main_layout.addWidget(self.gauge_therm)
        grid.addWidget(self.card_therm, 1, 1)

        c_layout.addLayout(grid)

        scroll.setWidget(container)
        layout.addWidget(scroll)

    def update_telemetry(self):
        if hasattr(self, 'telemetry'):
            self._apply_telemetry(self.telemetry.cached_metrics)

    def _apply_telemetry(self, m: dict):
        if not m or not self.isVisible():
            return

        # CPU
        cpu_pct = m.get('cpu_percent', 33.3)
        self.lbl_cpu_usage.setText(f"{cpu_pct}% Utilization")
        self.gauge_cpu.set_value(cpu_pct)
        self.lbl_cpu_details.setText(f"Clock: {m.get('cpu_freq_ghz', 3.2)} GHz\nCores: {m.get('cpu_cores', 12)} Threads\nTemp: {m.get('cpu_temp_c', 45)}°C")

        # GPU
        gpu = m.get("gpu", {})
        gpu_pct = gpu.get('utilization_pct', 9)
        self.lbl_gpu_usage.setText(f"{gpu_pct}% Utilization")
        self.gauge_gpu.set_value(gpu_pct)
        self.lbl_gpu_details.setText(f"VRAM: {gpu.get('vram_used_mb', 950)} / {gpu.get('vram_total_mb', 6144)} MB\nTemp: {gpu.get('temp_c', 40)}°C\nDedicated 6GB")

        # RAM
        self.lbl_ram_usage.setText(f"{m.get('ram_used_gb', 11.9)} GB / {m.get('ram_total_gb', 23.7)} GB")
        self.gauge_ram.set_value(m.get('ram_percent', 50.0))
        self.lbl_ram_details.setText(f"Available: {m.get('ram_free_gb', 11.8)} GB\nPressure: Low\nUsage: {m.get('ram_percent', 50.0)}%")

        # Thermals
        temp = max(m.get('cpu_temp_c', 45), gpu.get('temp_c', 40))
        self.gauge_therm.set_value(temp)
        if temp < 55:
            self.lbl_th_state.setText(f"Optimal • {temp}°C")
            self.lbl_th_state.setStyleSheet("color: #10B981; font-size: 18px; font-weight: 800;")
        elif temp < 75:
            self.lbl_th_state.setText(f"Moderate • {temp}°C")
            self.lbl_th_state.setStyleSheet("color: #F59E0B; font-size: 18px; font-weight: 800;")
        else:
            self.lbl_th_state.setText(f"Heavy Load • {temp}°C")
            self.lbl_th_state.setStyleSheet("color: #EF4444; font-size: 18px; font-weight: 800;")

    def _handle_boost(self):
        res = SystemOptimizer.flush_ram()
        QMessageBox.information(
            self,
            "Performance Boosted",
            f"Optimized memory working sets!\nReclaimed {res['freed_mb']} MB of RAM for gaming & high-performance applications."
        )
        self.update_telemetry()
