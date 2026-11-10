"""
TREVIORA AI DEFENDER - Ultra-Premium Cyber Dashboard Widgets (Zero Lag Optimized)
Matches the Reference Desktop Layout (1000% visual fidelity):
- HoloShieldWidget: 3D Holographic Cyber Energy Shield on Pedestal
- RadialScoreWidget: Hero System Score 95 Gauge with Excellent Status
- RadialStorageWidget: Space Cleanup Gauge with Drive Emblem & Available GB
- SparklineWaveWidget: Animated Cyber Telemetry Waveform
- BatteryCylinderWidget: 3D Glowing Liquid Battery Cylinder
- AmdRyzenChipWidget: Realistic AMD Ryzen Processor with Circuit Traces
- MiniTelemetryCard: Compact CPU, GPU, RAM, Battery Monitoring Cards

Zero-lag optimizations:
- Driven by unified SharedAnimationClock (single 30 FPS timer across all widgets)
- Visibility checks: widgets pause painting completely when hidden or tabbed out
- Static widgets (Chip, Storage Gauge) draw once with zero timer churn
"""
import math
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, QRadialGradient,
    QFont, QPolygonF, QPainterPath
)

from treviora_defender.ui.animation_clock import SharedAnimationClock


class SparklineWaveWidget(QWidget):
    """Animated glowing wave/sparkline for telemetry cards driven by shared clock."""
    def __init__(self, color="#00E676", parent=None):
        super().__init__(parent)
        self.color_hex = color
        self.phase = 0.0
        self._frame_count = 0
        self.setFixedHeight(24)
        self.setMinimumWidth(80)

        # Hook into central shared animation clock (no dedicated timer)
        SharedAnimationClock.get_clock().tick.connect(self._tick)

    def _tick(self):
        if not self.isVisible():
            return
        self._frame_count += 1
        if self._frame_count % 2 != 0:
            return
        self.phase = (self.phase + 0.16) % (math.pi * 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        base_color = QColor(self.color_hex)

        path = QPainterPath()
        points = []
        num_points = 20
        dx = w / (num_points - 1)

        for i in range(num_points):
            x = i * dx
            # Smooth cyber waveform
            y = (h / 2.0) + math.sin(self.phase + i * 0.45) * (h * 0.30) + math.cos(self.phase * 0.7 + i * 0.2) * (h * 0.10)
            points.append(QPointF(x, y))

        path.moveTo(points[0])
        for i in range(1, len(points)):
            path.lineTo(points[i])

        # Draw glowing line
        glow_pen = QPen(QColor(base_color.red(), base_color.green(), base_color.blue(), 80), 4)
        painter.setPen(glow_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        main_pen = QPen(base_color, 2)
        painter.setPen(main_pen)
        painter.drawPath(path)


class RadialScoreWidget(QWidget):
    """
    Renders the Hero System Score gauge from the reference image:
    - Glowing neon emerald-cyan circular arc
    - Big bold '95' in center
    - 'Excellent' status
    - 'System Score' title at top
    """
    def __init__(self, score=95, size=150, parent=None):
        super().__init__(parent)
        self.score = score
        self.target_score = score
        self.pulse = 0.0
        self._frame_count = 0
        self.setFixedSize(size, size)

        # Hook into central shared animation clock
        SharedAnimationClock.get_clock().tick.connect(self._animate)

    def set_score(self, val: int):
        self.target_score = val
        self.update()

    def _animate(self):
        if not self.isVisible():
            return
        needs_update = False
        if self.score < self.target_score:
            self.score += 1
            needs_update = True
        elif self.score > self.target_score:
            self.score -= 1
            needs_update = True

        self._frame_count += 1
        if needs_update or (self._frame_count % 3 == 0):
            self.pulse = (self.pulse + 0.08) % (math.pi * 2)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2.0
        cy = h / 2.0
        radius = min(cx, cy) - 14

        # 1. Top label "System Score"
        painter.setPen(QColor(148, 163, 184))
        font_hdr = QFont("Segoe UI", 9, QFont.DemiBold)
        font_hdr.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)
        painter.setFont(font_hdr)
        painter.drawText(QRectF(0, 2, w, 16), Qt.AlignCenter, "System Score")

        # 2. Background Track Arc (240 degrees span, opening at bottom)
        start_angle = 210 * 16
        span_angle = -240 * 16
        track_pen = QPen(QColor(20, 32, 54), 8)
        track_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(track_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(QRectF(cx - radius, cy - radius + 4, radius * 2, radius * 2), start_angle, span_angle)

        # 3. Active Glowing Neon Arc
        active_span = int(-240.0 * (self.score / 100.0) * 16)
        arc_rect = QRectF(cx - radius, cy - radius + 4, radius * 2, radius * 2)

        grad = QLinearGradient(arc_rect.left(), arc_rect.top(), arc_rect.right(), arc_rect.bottom())
        grad.setColorAt(0.0, QColor(0, 230, 118))   # Mint emerald
        grad.setColorAt(1.0, QColor(0, 210, 255))   # Electric cyan

        # Outer soft glow
        pulse_alpha = int(60 + 20 * math.sin(self.pulse))
        glow_pen = QPen(QColor(0, 230, 180, pulse_alpha), 12)
        glow_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(glow_pen)
        painter.drawArc(arc_rect, start_angle, active_span)

        # Main crisp arc
        act_pen = QPen(QBrush(grad), 8)
        act_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(act_pen)
        painter.drawArc(arc_rect, start_angle, active_span)

        # 4. Center Number: "95"
        painter.setPen(QColor(255, 255, 255))
        font_num = QFont("Segoe UI", 32, QFont.Bold)
        painter.setFont(font_num)
        painter.drawText(QRectF(0, cy - 22, w, 38), Qt.AlignCenter, str(self.score))

        # 5. Bottom status: "Excellent"
        painter.setPen(QColor(0, 230, 118))
        font_sub = QFont("Segoe UI", 10, QFont.DemiBold)
        painter.setFont(font_sub)
        status_text = "Excellent" if self.score >= 90 else ("Good" if self.score >= 75 else "Needs Care")
        painter.drawText(QRectF(0, cy + 16, w, 20), Qt.AlignCenter, status_text)


class HoloShieldWidget(QWidget):
    """
    3D Holographic Cyber Energy Shield on Pedestal (Exact match with reference image).
    Used in Hero card, Security Scan card, and Sidebar priority card.
    Zero-lag optimized with shared clock.
    """
    def __init__(self, size=150, show_lock=False, show_check=True, parent=None):
        super().__init__(parent)
        self.show_lock = show_lock
        self.show_check = show_check
        self.setFixedSize(size, size)

        self.angle = 0.0
        self.pulse = 0.0
        self._frame_count = 0

        # Hook into central shared animation clock
        SharedAnimationClock.get_clock().tick.connect(self._tick)

    def _tick(self):
        if not self.isVisible():
            return
        self._frame_count += 1
        if self.width() < 100 and (self._frame_count % 2 != 0):
            return
        self.angle = (self.angle + 1.2) % 360.0
        self.pulse = (self.pulse + 0.06) % (math.pi * 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2.0
        cy = h / 2.0

        # 1. Circular Cyber Energy Pedestal at Base
        ped_y = cy + h * 0.32
        ped_w = w * 0.72
        ped_h = h * 0.22

        # Glowing concentric pedestal rings
        for i, scale in enumerate([1.0, 0.75, 0.5]):
            pw = ped_w * scale
            ph = ped_h * scale
            alpha = int(110 - i * 35 + 20 * math.sin(self.pulse + i))
            pen = QPen(QColor(0, 210, 255, alpha), 2)
            if i == 0:
                pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor(0, 110, 240, 25)))
            painter.drawEllipse(QRectF(cx - pw / 2.0, ped_y - ph / 2.0, pw, ph))

        # Pedestal core glow
        radial = QRadialGradient(cx, ped_y, ped_w * 0.4)
        radial.setColorAt(0.0, QColor(0, 210, 255, 130))
        radial.setColorAt(1.0, QColor(0, 210, 255, 0))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(radial))
        painter.drawEllipse(QRectF(cx - ped_w * 0.4, ped_y - ped_h * 0.4, ped_w * 0.8, ped_h * 0.8))

        # 2. Holographic Upright Energy Shield
        shield_cy = cy - h * 0.06
        shield_w = w * 0.44
        shield_h = h * 0.54

        # Shield contour polygon
        top_y = shield_cy - shield_h / 2.0
        bot_y = shield_cy + shield_h / 2.0
        mid_y = shield_cy + shield_h * 0.15

        shield_poly = QPolygonF([
            QPointF(cx, top_y),
            QPointF(cx + shield_w / 2.0, top_y + shield_h * 0.18),
            QPointF(cx + shield_w * 0.45, mid_y),
            QPointF(cx, bot_y),
            QPointF(cx - shield_w * 0.45, mid_y),
            QPointF(cx - shield_w / 2.0, top_y + shield_h * 0.18),
        ])

        # Multi-layer shield bloom
        bloom_alpha = int(55 + 20 * math.sin(self.pulse))
        painter.setPen(QPen(QColor(0, 210, 255, bloom_alpha), 5))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(shield_poly)

        # Shield glass fill gradient
        shield_grad = QLinearGradient(cx, top_y, cx, bot_y)
        shield_grad.setColorAt(0.0, QColor(0, 210, 255, 220))
        shield_grad.setColorAt(0.4, QColor(0, 140, 255, 190))
        shield_grad.setColorAt(1.0, QColor(10, 30, 80, 230))

        painter.setPen(QPen(QColor(255, 255, 255, 240), 2))
        painter.setBrush(QBrush(shield_grad))
        painter.drawPolygon(shield_poly)

        # 3. Inner Symbol: Checkmark or Padlock
        if self.show_check:
            # Crisp white glowing checkmark
            check_path = QPainterPath()
            check_path.moveTo(cx - shield_w * 0.22, shield_cy - shield_h * 0.02)
            check_path.lineTo(cx - shield_w * 0.05, shield_cy + shield_h * 0.14)
            check_path.lineTo(cx + shield_w * 0.24, shield_cy - shield_h * 0.16)

            check_pen = QPen(QColor(255, 255, 255), 4)
            check_pen.setCapStyle(Qt.RoundCap)
            check_pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(check_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(check_path)

        elif self.show_lock:
            # Padlock icon
            lock_w = shield_w * 0.32
            lock_h = shield_h * 0.28
            body_rect = QRectF(cx - lock_w / 2.0, shield_cy - lock_h * 0.1, lock_w, lock_h * 0.9)

            # Shackle
            shackle_rect = QRectF(cx - lock_w * 0.35, shield_cy - lock_h * 0.6, lock_w * 0.7, lock_h * 0.7)
            painter.setPen(QPen(QColor(255, 255, 255), 2.5))
            painter.setBrush(Qt.NoBrush)
            painter.drawArc(shackle_rect, 0, 180 * 16)

            # Body
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawRoundedRect(body_rect, 3, 3)

            # Keyhole
            painter.setBrush(QBrush(QColor(0, 110, 240)))
            painter.drawEllipse(QPointF(cx, shield_cy + lock_h * 0.25), 2.5, 2.5)


class RadialStorageWidget(QWidget):
    """
    Renders the Space Cleanup circular radial gauge from the reference image:
    - Glowing cyan arc
    - Hard drive icon in center
    - Underneath: '87.32 GB Available'
    Zero-timer static render (updates only when storage changes).
    """
    def __init__(self, available_gb=87.32, total_gb=250.0, size=130, parent=None):
        super().__init__(parent)
        self.available_gb = available_gb
        self.total_gb = total_gb
        self.setFixedSize(size, size + 36)

    def set_available(self, gb: float):
        if abs(self.available_gb - gb) > 0.05:
            self.available_gb = gb
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        cx = w / 2.0
        cy = 60.0
        radius = 48.0

        # Background track
        bg_pen = QPen(QColor(20, 32, 54), 7)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2), 225 * 16, -270 * 16)

        # Active cyan arc
        pct = min(1.0, max(0.0, (self.total_gb - self.available_gb) / self.total_gb))
        active_span = int(-270.0 * pct * 16)

        grad = QLinearGradient(cx - radius, cy - radius, cx + radius, cy + radius)
        grad.setColorAt(0.0, QColor(0, 112, 243))
        grad.setColorAt(1.0, QColor(0, 210, 255))

        act_pen = QPen(QBrush(grad), 7)
        act_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(act_pen)
        painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2), 225 * 16, active_span)

        # Center Drive Icon Box
        drive_w = 32.0
        drive_h = 32.0
        drive_rect = QRectF(cx - drive_w / 2.0, cy - drive_h / 2.0, drive_w, drive_h)

        painter.setPen(QPen(QColor(0, 210, 255, 120), 1))
        painter.setBrush(QBrush(QColor(10, 22, 45)))
        painter.drawRoundedRect(drive_rect, 6, 6)

        # Platter circle on drive
        painter.setPen(QPen(QColor(0, 210, 255), 1.5))
        painter.setBrush(QBrush(QColor(0, 112, 243)))
        painter.drawEllipse(QPointF(cx, cy - 2), 7, 7)

        # Indicator LED
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 230, 118)))
        painter.drawEllipse(QPointF(cx + 8, cy + 9), 2, 2)

        # Bottom Labels: "87.32 GB Available"
        painter.setPen(QColor(255, 255, 255))
        font_gb = QFont("Segoe UI", 13, QFont.Bold)
        painter.setFont(font_gb)
        painter.drawText(QRectF(0, cy + radius + 10, w, 20), Qt.AlignCenter, f"{self.available_gb:.2f} GB")

        painter.setPen(QColor(148, 163, 184))
        font_sub = QFont("Segoe UI", 9, QFont.DemiBold)
        painter.setFont(font_sub)
        painter.drawText(QRectF(0, cy + radius + 28, w, 16), Qt.AlignCenter, "Available")


class BatteryCylinderWidget(QWidget):
    """
    3D Liquid Glowing Battery Cylinder (Matches reference image Power & Battery card).
    Zero-lag optimized.
    """
    def __init__(self, percent=58, is_charging=True, parent=None):
        super().__init__(parent)
        self.percent = percent
        self.is_charging = is_charging
        self.setFixedSize(54, 88)

    def set_percent(self, pct: int, is_charging: bool = True):
        if self.percent != pct or self.is_charging != is_charging:
            self.percent = pct
            self.is_charging = is_charging
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2.0

        # Battery body dimensions
        bw = 42.0
        bh = 72.0
        bx = cx - bw / 2.0
        by = 12.0

        # 1. Battery Top Terminal
        term_w = 16.0
        term_h = 6.0
        term_rect = QRectF(cx - term_w / 2.0, by - term_h + 1, term_w, term_h)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(100, 116, 139)))
        painter.drawRoundedRect(term_rect, 2, 2)

        # 2. Outer Glass Cylinder Frame
        body_rect = QRectF(bx, by, bw, bh)
        painter.setPen(QPen(QColor(51, 65, 85, 200), 2))
        painter.setBrush(QBrush(QColor(15, 23, 42, 220)))
        painter.drawRoundedRect(body_rect, 8, 8)

        # 3. Inner Liquid Glow Fill
        liquid_h = (bh - 6) * (self.percent / 100.0)
        liquid_y = by + bh - 3 - liquid_h
        liquid_rect = QRectF(bx + 3, liquid_y, bw - 6, liquid_h)

        liquid_grad = QLinearGradient(bx, liquid_y, bx + bw, liquid_y + liquid_h)
        if self.percent > 40:
            liquid_grad.setColorAt(0.0, QColor(0, 230, 118))
            liquid_grad.setColorAt(1.0, QColor(0, 180, 90))
        elif self.percent > 20:
            liquid_grad.setColorAt(0.0, QColor(245, 158, 11))
            liquid_grad.setColorAt(1.0, QColor(217, 119, 6))
        else:
            liquid_grad.setColorAt(0.0, QColor(239, 68, 68))
            liquid_grad.setColorAt(1.0, QColor(185, 28, 28))

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(liquid_grad))
        painter.drawRoundedRect(liquid_rect, 6, 6)

        # 4. Lightning Bolt in center
        if self.is_charging:
            bolt = QPolygonF([
                QPointF(cx + 2, by + bh * 0.28),
                QPointF(cx - 5, by + bh * 0.52),
                QPointF(cx + 1, by + bh * 0.52),
                QPointF(cx - 2, by + bh * 0.74),
                QPointF(cx + 6, by + bh * 0.46),
                QPointF(cx, by + bh * 0.46),
            ])
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, 240)))
            painter.drawPolygon(bolt)


class AmdRyzenChipWidget(QWidget):
    """
    Renders realistic processor chip with metallic heatsink plate and glowing circuit traces.
    Dynamically adapts to Intel, AMD Ryzen, or Generic CPU based on detected hardware profile.
    Consumes 0% CPU (static render).
    """
    def __init__(self, size=100, vendor=None, family=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        from treviora_defender.core.hardware_profile import HardwareProfile
        profile = HardwareProfile.get_profile()
        self.vendor = vendor or profile["cpu"]["vendor"]
        self.brand = profile["cpu"]["brand"]
        self.family = family or profile["cpu"]["family"]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2.0
        cy = h / 2.0

        # Outer PCB border with pins
        pcb_size = min(w, h) - 10
        pcb_rect = QRectF(cx - pcb_size / 2.0, cy - pcb_size / 2.0, pcb_size, pcb_size)

        # Circuit trace color based on vendor
        is_intel = self.vendor.lower() == "intel"
        trace_color = QColor(0, 160, 255, 120) if is_intel else QColor(0, 210, 255, 90)

        # Glowing circuit traces
        painter.setPen(QPen(trace_color, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(pcb_rect, 10, 10)

        # PCB base
        pcb_base = QColor(5, 20, 45) if is_intel else QColor(10, 18, 35)
        painter.setPen(QPen(QColor(0, 140, 255), 1.5))
        painter.setBrush(QBrush(pcb_base))
        painter.drawRoundedRect(pcb_rect, 10, 10)

        # Metallic Integrated Heat Spreader (IHS)
        ihs_size = pcb_size * 0.76
        ihs_rect = QRectF(cx - ihs_size / 2.0, cy - ihs_size / 2.0, ihs_size, ihs_size)

        ihs_grad = QLinearGradient(ihs_rect.left(), ihs_rect.top(), ihs_rect.right(), ihs_rect.bottom())
        if is_intel:
            ihs_grad.setColorAt(0.0, QColor(20, 60, 120))
            ihs_grad.setColorAt(0.5, QColor(10, 35, 75))
            ihs_grad.setColorAt(1.0, QColor(5, 20, 45))
            border_color = QColor(0, 130, 255)
            top_txt = "intel"
            bot_txt = "CORE" if "core" in self.family.lower() else "inside"
        elif self.vendor.lower() == "amd":
            ihs_grad.setColorAt(0.0, QColor(45, 60, 85))
            ihs_grad.setColorAt(0.5, QColor(25, 38, 60))
            ihs_grad.setColorAt(1.0, QColor(15, 24, 40))
            border_color = QColor(70, 95, 130)
            top_txt = "AMD"
            bot_txt = "RYZEN"
        else:
            ihs_grad.setColorAt(0.0, QColor(40, 50, 70))
            ihs_grad.setColorAt(0.5, QColor(20, 30, 50))
            ihs_grad.setColorAt(1.0, QColor(10, 18, 30))
            border_color = QColor(0, 210, 255)
            top_txt = "NEURAL"
            bot_txt = "QUANTUM"

        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QBrush(ihs_grad))
        painter.drawRoundedRect(ihs_rect, 6, 6)

        # Top Text (e.g. AMD or intel)
        painter.setPen(QColor(255, 255, 255))
        font_top = QFont("Segoe UI", 10, QFont.Bold)
        if is_intel:
            font_top.setItalic(True)
        font_top.setLetterSpacing(QFont.AbsoluteSpacing, 1.0)
        painter.setFont(font_top)
        painter.drawText(QRectF(ihs_rect.left(), cy - 14, ihs_size, 14), Qt.AlignCenter, top_txt)

        # Bottom Text (e.g. RYZEN or CORE)
        bot_color = QColor(0, 210, 255) if is_intel or self.vendor.lower() == "amd" else QColor(0, 230, 118)
        painter.setPen(bot_color)
        font_bot = QFont("Segoe UI", 11, QFont.Bold)
        font_bot.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        painter.setFont(font_bot)
        painter.drawText(QRectF(ihs_rect.left(), cy + 1, ihs_size, 16), Qt.AlignCenter, bot_txt)

# Alias for universal support
DynamicProcessorChipWidget = AmdRyzenChipWidget


class MiniTelemetryCard(QFrame):
    """
    Renders one of the 4 Mini Telemetry Cards (CPU, GPU, RAM, Battery)
    from the top row of the reference image.
    """
    def __init__(self, icon_str: str, title: str, initial_value: str, spark_color: str, parent=None):
        super().__init__(parent)
        self.setObjectName("MiniTelemetryCard")
        self.setFixedHeight(84)
        self.setMinimumWidth(120)
        self.setStyleSheet("""
            QFrame#MiniTelemetryCard {
                background-color: #0B1324;
                border: 1px solid #1E293B;
                border-radius: 14px;
            }
            QFrame#MiniTelemetryCard:hover {
                background-color: #111D36;
                border: 1px solid #00D2FF;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(2)

        # Header: Icon + Title
        hdr = QHBoxLayout()
        hdr.setSpacing(6)
        lbl_icon = QLabel(icon_str)
        lbl_icon.setStyleSheet("font-size: 14px;")

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #94A3B8; font-size: 11px; font-weight: 600;")

        hdr.addWidget(lbl_icon)
        hdr.addWidget(lbl_title)
        hdr.addStretch()
        layout.addLayout(hdr)

        # Big Value
        self.lbl_value = QLabel(initial_value)
        self.lbl_value.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: 800;")
        layout.addWidget(self.lbl_value)

        # Sparkline Wave
        self.sparkline = SparklineWaveWidget(color=spark_color)
        layout.addWidget(self.sparkline)

    def set_value(self, val_str: str):
        self.lbl_value.setText(val_str)
