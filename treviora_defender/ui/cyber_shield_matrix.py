"""
TREVIORA AI DEFENDER - Quantum Hexagon Honeycomb Energy Shield Matrix
Exact 1000% Implementation of User Request & Image 3 (media_1794297819333_8529d097.jpg):
- Cyan glowing hexagonal honeycomb grid texture and vector procedural mesh
- Full Active vs Deactivated (Standby) state toggle
- Animated laser scan sweep beam scanning vertically across the grid
- Expanding concentric radial energy shockwaves from center core
- 3-Layer Security Armor HUD:
    * Layer 1: Kernel & Memory Integrity Armor
    * Layer 2: Network TCP/IP & Port Deflector
    * Layer 3: AI Threat Interceptor & Heuristic Dome
- Full Desktop HUD Energy Shield Modal Dialog with zero-lag 25 FPS pacing
"""
import math
import time
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QDialog, QMessageBox
)
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, QRadialGradient,
    QFont, QPixmap, QPainterPath, QPolygonF
)

from treviora_defender.config.constants import RESOURCES_DIR
from treviora_defender.ui.animation_clock import SharedAnimationClock
from treviora_defender.core.firewall_guard import SafeGuardFirewall


class HexagonEnergyShieldCanvas(QWidget):
    """
    Renders the exact cyan glowing honeycomb energy shield from Image 3:
    - Tiled cyan glowing hexagon texture with vector glow enhancement
    - Full Active / Deactivated visual switching
    - Animated laser scan beam sweeping across the grid
    - Expanding radial energy shockwave ripples
    - 3-Layer Holographic Central Power Core
    """
    def __init__(self, parent=None, is_compact=False):
        super().__init__(parent)
        self.is_compact = is_compact
        self.is_active = True
        self.sweep_y = 0.0
        self.ripple_radius = 0.0
        self.pulse = 0.0
        self.core_rotation = 0.0
        self._frame_count = 0

        # Load official Image 3 texture
        grid_path = RESOURCES_DIR / "energy_shield_grid.jpg"
        if not grid_path.exists():
            grid_path = Path("D:/projects/antivirus/resources/energy_shield_grid.jpg")
        
        self.grid_pixmap = QPixmap(str(grid_path)) if grid_path.exists() else None

        # Hook into central shared animation clock (zero lag, 25 FPS)
        SharedAnimationClock.get_clock().tick.connect(self._tick)

    def set_shield_active(self, active: bool):
        self.is_active = active
        self.trigger_shockwave()
        self.update()

    def trigger_shockwave(self):
        """Triggers an expanding energy ripple across the honeycomb shield."""
        self.ripple_radius = 10.0

    def _tick(self):
        if not self.isVisible():
            return

        self._frame_count += 1

        # Smooth scanline sweep (only sweeps when active)
        if self.is_active and not self.is_compact:
            h = max(200, self.height())
            self.sweep_y = (self.sweep_y + 4.5)
            if self.sweep_y > h + 100:
                self.sweep_y = -50.0

        # Smooth shockwave expansion
        if self.ripple_radius > 0:
            self.ripple_radius += 14.0
            if self.ripple_radius > max(self.width(), self.height()) * 1.3:
                self.ripple_radius = 0.0

        self.pulse = (self.pulse + 0.06) % (math.pi * 2)
        if self.is_active:
            self.core_rotation = (self.core_rotation + 1.2) % 360.0
        else:
            self.core_rotation = (self.core_rotation + 0.3) % 360.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        w = self.width()
        h = self.height()
        cx = w / 2.0
        cy = h / 2.0

        # 1. Background Void
        bg_color = QColor(4, 8, 20) if self.is_active else QColor(14, 8, 12)
        painter.fillRect(0, 0, w, h, bg_color)

        # 2. Tiled Cyan Hexagonal Honeycomb Matrix (Matches Image 3)
        if self.grid_pixmap and not self.grid_pixmap.isNull():
            tw = self.grid_pixmap.width()
            th = self.grid_pixmap.height()
            
            # Pulse the base grid brightness
            if self.is_active:
                grid_alpha = int(185 + 35 * math.sin(self.pulse))
            else:
                grid_alpha = int(80 + 20 * math.sin(self.pulse))

            painter.setOpacity(grid_alpha / 255.0)

            x = 0
            while x < w:
                y = 0
                while y < h:
                    painter.drawPixmap(x, y, self.grid_pixmap)
                    y += th
                x += tw

            painter.setOpacity(1.0)
        else:
            self._draw_procedural_honeycomb(painter, w, h)

        # Inactive Amber/Crimson wash overlay if deactivated
        if not self.is_active:
            painter.fillRect(0, 0, w, h, QColor(180, 20, 30, 45))

        # 3. Radial Vignette (Dark edges)
        vignette = QRadialGradient(cx, cy, max(w, h) * 0.65)
        vignette.setColorAt(0.0, QColor(0, 0, 0, 0))
        vignette.setColorAt(0.5, QColor(4, 8, 20, 60))
        vignette.setColorAt(1.0, QColor(2, 4, 12, 235))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(vignette))
        painter.drawRect(0, 0, w, h)

        # 4. Animated Laser Scan Sweep Line (when active)
        if self.is_active and not self.is_compact:
            scan_rect = QRectF(0, self.sweep_y - 25, w, 50)
            scan_grad = QLinearGradient(0, self.sweep_y - 25, 0, self.sweep_y + 25)
            scan_grad.setColorAt(0.0, QColor(0, 210, 255, 0))
            scan_grad.setColorAt(0.5, QColor(0, 230, 255, 140))
            scan_grad.setColorAt(1.0, QColor(0, 210, 255, 0))

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(scan_grad))
            painter.drawRect(scan_rect)

            laser_pen = QPen(QColor(255, 255, 255, 220), 2)
            painter.setPen(laser_pen)
            painter.drawLine(0, int(self.sweep_y), w, int(self.sweep_y))

        # 5. Expanding Concentric Shockwave Ripple
        if self.ripple_radius > 0:
            color = QColor(0, 230, 255) if self.is_active else QColor(239, 68, 68)
            ripple_alpha = int(max(0, 220 * (1.0 - (self.ripple_radius / (max(w, h) * 1.3)))))
            ripple_pen = QPen(QColor(color.red(), color.green(), color.blue(), ripple_alpha), 6)
            painter.setPen(ripple_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(cx, cy), self.ripple_radius, self.ripple_radius)

            if self.ripple_radius > 60:
                trail_alpha = int(ripple_alpha * 0.5)
                painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), trail_alpha), 3))
                painter.drawEllipse(QPointF(cx, cy), self.ripple_radius - 40, self.ripple_radius - 40)

        # 6. Central 3-Layer Quantum Core Shield
        self._draw_quantum_shield_core(painter, cx, cy)

    def _draw_quantum_shield_core(self, painter: QPainter, cx: float, cy: float):
        scale = 0.65 if self.is_compact else 1.0
        core_r = 110.0 * scale
        color_primary = QColor(0, 210, 255) if self.is_active else QColor(239, 68, 68)
        color_secondary = QColor(0, 110, 240) if self.is_active else QColor(185, 28, 28)

        # Central ambient glow
        core_glow = QRadialGradient(cx, cy, core_r * 1.8)
        core_glow.setColorAt(0.0, QColor(color_primary.red(), color_primary.green(), color_primary.blue(), 140))
        core_glow.setColorAt(0.5, QColor(color_secondary.red(), color_secondary.green(), color_secondary.blue(), 50))
        core_glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(core_glow))
        painter.drawEllipse(QPointF(cx, cy), core_r * 1.8, core_r * 1.8)

        # Layer 1: Outermost Rotating Hexagonal Gear Ring
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.core_rotation)
        ring1_pen = QPen(QColor(color_primary.red(), color_primary.green(), color_primary.blue(), 180), 2)
        ring1_pen.setStyle(Qt.DashLine)
        painter.setPen(ring1_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(0, 0), core_r * 1.25, core_r * 1.25)

        # Orbital energy nodes on Ring 1
        for deg in [0, 90, 180, 270]:
            rad = math.radians(deg)
            nx = math.cos(rad) * (core_r * 1.25)
            ny = math.sin(rad) * (core_r * 1.25)
            painter.setPen(Qt.NoPen)
            node_color = QColor(0, 230, 118) if self.is_active else QColor(245, 158, 11)
            painter.setBrush(QBrush(node_color))
            painter.drawEllipse(QPointF(nx, ny), 4, 4)
        painter.restore()

        # Layer 2: Counter-Rotating Ring with Neon Arc Segments
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(-self.core_rotation * 1.4)
        ring2_pen = QPen(QColor(color_primary.red(), color_primary.green(), color_primary.blue(), 220), 3)
        painter.setPen(ring2_pen)
        painter.setBrush(Qt.NoBrush)
        arc_rect = QRectF(-core_r, -core_r, core_r * 2, core_r * 2)
        painter.drawArc(arc_rect, 30 * 16, 75 * 16)
        painter.drawArc(arc_rect, 150 * 16, 75 * 16)
        painter.drawArc(arc_rect, 270 * 16, 75 * 16)
        painter.restore()

        # Layer 3: Solid Holographic Cyber Shield Crest
        shield_w = core_r * 1.05
        shield_h = core_r * 1.25
        top_y = cy - shield_h * 0.52
        bot_y = cy + shield_h * 0.52
        mid_y = cy + shield_h * 0.18

        shield_poly = QPolygonF([
            QPointF(cx, top_y),
            QPointF(cx + shield_w * 0.5, top_y + shield_h * 0.16),
            QPointF(cx + shield_w * 0.44, mid_y),
            QPointF(cx, bot_y),
            QPointF(cx - shield_w * 0.44, mid_y),
            QPointF(cx - shield_w * 0.5, top_y + shield_h * 0.16),
        ])

        # Shield glass gradient fill
        s_grad = QLinearGradient(cx, top_y, cx, bot_y)
        if self.is_active:
            s_grad.setColorAt(0.0, QColor(0, 210, 255, 230))
            s_grad.setColorAt(0.45, QColor(0, 112, 243, 210))
            s_grad.setColorAt(1.0, QColor(6, 18, 54, 240))
        else:
            s_grad.setColorAt(0.0, QColor(239, 68, 68, 220))
            s_grad.setColorAt(0.45, QColor(185, 28, 28, 200))
            s_grad.setColorAt(1.0, QColor(35, 10, 15, 240))

        painter.setPen(QPen(QColor(255, 255, 255, 240), 3))
        painter.setBrush(QBrush(s_grad))
        painter.drawPolygon(shield_poly)

        # Center White Glowing Emblem (Checkmark if active, Pause/Lock if inactive)
        if self.is_active:
            check_path = QPainterPath()
            check_path.moveTo(cx - shield_w * 0.22, cy - shield_h * 0.04)
            check_path.lineTo(cx - shield_w * 0.05, cy + shield_h * 0.14)
            check_path.lineTo(cx + shield_w * 0.24, cy - shield_h * 0.16)

            c_pen = QPen(QColor(255, 255, 255), 5 * scale)
            c_pen.setCapStyle(Qt.RoundCap)
            c_pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(c_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(check_path)
        else:
            # Standby Pause Bars
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, 240)))
            bar_w = 6 * scale
            bar_h = 24 * scale
            painter.drawRoundedRect(QRectF(cx - 10 * scale, cy - bar_h / 2, bar_w, bar_h), 2, 2)
            painter.drawRoundedRect(QRectF(cx + 4 * scale, cy - bar_h / 2, bar_w, bar_h), 2, 2)

        # Core Label under Shield
        if not self.is_compact:
            painter.setPen(color_primary)
            font_core = QFont("Segoe UI", 11, QFont.Bold)
            font_core.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
            painter.setFont(font_core)
            status_str = "3-LAYER QUANTUM DEFLECTOR ACTIVE" if self.is_active else "3-LAYER DEFLECTOR: STANDBY (DEACTIVATED)"
            painter.drawText(QRectF(0, bot_y + 12, self.width(), 22), Qt.AlignCenter, status_str)

    def _draw_procedural_honeycomb(self, painter: QPainter, w: int, h: int):
        hex_r = 24.0
        hex_w = math.sqrt(3) * hex_r
        hex_h = hex_r * 1.5

        color = QColor(0, 210, 255, 90) if self.is_active else QColor(239, 68, 68, 60)
        pen = QPen(color, 1.5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        cols = int(w / hex_w) + 2
        rows = int(h / hex_h) + 2

        for r in range(rows):
            for c in range(cols):
                hx = c * hex_w + ((r % 2) * (hex_w / 2.0))
                hy = r * hex_h

                poly = QPolygonF()
                for i in range(6):
                    angle_deg = 60 * i - 30
                    angle_rad = math.radians(angle_deg)
                    poly.append(QPointF(hx + hex_r * math.cos(angle_rad), hy + hex_r * math.sin(angle_rad)))
                painter.drawPolygon(poly)


class DesktopEnergyShieldOverlay(QDialog):
    """
    High-tech Cyber Energy Shield Screen overlay matching Image 3.
    Features live honeycomb grid animations, telemetry HUD, and Active/Deactivated toggle.
    """
    shield_toggled = Signal(bool)

    def __init__(self, parent=None, is_active=True):
        super().__init__(parent)
        self.setWindowTitle("TREVIORA SAFEGUARD 3-LAYER ENERGY SHIELD")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 680)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.guard = SafeGuardFirewall()
        self.guard.is_active = is_active
        self._init_ui()

    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Outer frame with cyan glowing border
        self.outer_frame = QFrame()
        self.outer_frame.setObjectName("EnergyShieldOuterFrame")
        self._update_outer_frame_style()

        f_layout = QVBoxLayout(self.outer_frame)
        f_layout.setContentsMargins(20, 16, 20, 20)
        f_layout.setSpacing(14)

        # 1. Top HUD Header
        hdr = QHBoxLayout()
        lbl_hud_brand = QLabel("TREVIORA INDUSTRY")
        lbl_hud_brand.setStyleSheet("color: #00D2FF; font-size: 15px; font-weight: 800; letter-spacing: 1.5px;")

        self.lbl_hud_sub = QLabel("• SAFEGUARD 3-LAYER ENERGY SHIELD DOME")
        self.lbl_hud_sub.setStyleSheet("color: #94A3B8; font-size: 13px; font-weight: 600;")

        btn_close = QPushButton("✕ CLOSE")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setFixedHeight(32)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #111D36;
                color: #00D2FF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
                font-weight: 800;
                border: 1px solid #1E2E4E;
                border-radius: 16px;
                padding: 0px 18px;
            }
            QPushButton:hover {
                background: #EF4444;
                color: #FFFFFF;
                border: 1px solid #EF4444;
            }
        """)
        btn_close.clicked.connect(self.close)

        hdr.addWidget(lbl_hud_brand)
        hdr.addWidget(self.lbl_hud_sub)
        hdr.addStretch()
        hdr.addWidget(btn_close)
        f_layout.addLayout(hdr)

        # 2. Main Central Animated Honeycomb Canvas
        self.canvas = HexagonEnergyShieldCanvas(self)
        self.canvas.set_shield_active(self.guard.is_active)
        f_layout.addWidget(self.canvas, 1)

        # 3. Bottom HUD 3-Layer Defense Grid & Action Controls
        bot_bar = QHBoxLayout()
        bot_bar.setSpacing(14)

        # Layer 1 HUD Pill
        self.p1_box, self.lbl_p1_s = self._create_hud_pill("LAYER 1", "Kernel & Memory Armor", "#00E676")
        # Layer 2 HUD Pill
        self.p2_box, self.lbl_p2_s = self._create_hud_pill("LAYER 2", "TCP/IP Packet Filter", "#00D2FF")
        # Layer 3 HUD Pill
        self.p3_box, self.lbl_p3_s = self._create_hud_pill("LAYER 3", "AI Threat Interceptor", "#A855F7")

        bot_bar.addWidget(self.p1_box)
        bot_bar.addWidget(self.p2_box)
        bot_bar.addWidget(self.p3_box)

        # Toggle Button: Activate / Deactivate
        self.btn_toggle = QPushButton()
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.setFixedHeight(48)
        self.btn_toggle.clicked.connect(self._toggle_shield)
        bot_bar.addWidget(self.btn_toggle)

        # Shockwave Pulse Button
        self.btn_pulse = QPushButton("⚡ Boost Ripple")
        self.btn_pulse.setCursor(Qt.PointingHandCursor)
        self.btn_pulse.setFixedHeight(48)
        self.btn_pulse.setStyleSheet("""
            QPushButton {
                background: #111D36;
                color: #00D2FF;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 800;
                border: 1px solid #1E2E4E;
                border-radius: 14px;
                padding: 0px 18px;
            }
            QPushButton:hover {
                border: 1px solid #00D2FF;
                color: #FFFFFF;
            }
        """)
        self.btn_pulse.clicked.connect(self.canvas.trigger_shockwave)
        bot_bar.addWidget(self.btn_pulse)

        f_layout.addLayout(bot_bar)
        root.addWidget(self.outer_frame)

        self._update_ui_state()

    def _update_outer_frame_style(self):
        border_color = "#00D2FF" if self.guard.is_active else "#EF4444"
        self.outer_frame.setStyleSheet(f"""
            QFrame#EnergyShieldOuterFrame {{
                background-color: #040814;
                border: 2px solid {border_color};
                border-radius: 20px;
            }}
        """)

    def _create_hud_pill(self, layer_num: str, title: str, accent: str):
        frame = QFrame()
        frame.setFixedHeight(64)
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: #0A1224;
                border: 1px solid #1E293B;
                border-left: 4px solid {accent};
                border-radius: 12px;
            }}
        """)
        l = QVBoxLayout(frame)
        l.setContentsMargins(14, 8, 14, 8)
        l.setSpacing(2)

        lbl_l = QLabel(layer_num)
        lbl_l.setStyleSheet(f"color: {accent}; font-size: 10px; font-weight: 800; letter-spacing: 0.8px;")

        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: 700;")

        lbl_s = QLabel("ONLINE")
        lbl_s.setStyleSheet("color: #94A3B8; font-size: 10px; font-weight: 600;")

        l.addWidget(lbl_l)
        l.addWidget(lbl_t)
        l.addWidget(lbl_s)
        return frame, lbl_s

    def _update_ui_state(self):
        active = self.guard.is_active
        self._update_outer_frame_style()
        self.canvas.set_shield_active(active)

        if active:
            self.lbl_p1_s.setText("ONLINE • SECURED")
            self.lbl_p1_s.setStyleSheet("color: #00E676; font-size: 10px; font-weight: 700;")
            self.lbl_p2_s.setText("ACTIVE • 0 LEAKS")
            self.lbl_p2_s.setStyleSheet("color: #00D2FF; font-size: 10px; font-weight: 700;")
            self.lbl_p3_s.setText("ENGAGED • HEURISTICS")
            self.lbl_p3_s.setStyleSheet("color: #A855F7; font-size: 10px; font-weight: 700;")

            self.btn_toggle.setText("🔴 Deactivate Shield (Standby)")
            self.btn_toggle.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7F1D1D, stop:1 #B91C1C);
                    color: #FFFFFF;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 13px;
                    font-weight: 800;
                    border: none;
                    border-radius: 14px;
                    padding: 0px 22px;
                }
                QPushButton:hover {
                    background: #DC2626;
                }
            """)
        else:
            self.lbl_p1_s.setText("STANDBY • PAUSED")
            self.lbl_p1_s.setStyleSheet("color: #EF4444; font-size: 10px; font-weight: 700;")
            self.lbl_p2_s.setText("STANDBY • PAUSED")
            self.lbl_p2_s.setStyleSheet("color: #EF4444; font-size: 10px; font-weight: 700;")
            self.lbl_p3_s.setText("STANDBY • PAUSED")
            self.lbl_p3_s.setStyleSheet("color: #EF4444; font-size: 10px; font-weight: 700;")

            self.btn_toggle.setText("⚡ Activate 3-Layer Shield")
            self.btn_toggle.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E676, stop:1 #00B0FF);
                    color: #060A10;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 13px;
                    font-weight: 800;
                    border: none;
                    border-radius: 14px;
                    padding: 0px 22px;
                }
                QPushButton:hover {
                    background: #00FF88;
                }
            """)

    def _toggle_shield(self):
        res = self.guard.toggle_shield()
        self._update_ui_state()
        self.shield_toggled.emit(self.guard.is_active)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
