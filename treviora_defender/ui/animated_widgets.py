"""
TREVIORA AI DEFENDER - Custom High-Tech Cyber Animated Widgets
Developer: TREVIORA INDUSTRY
Tagline: "ENGINEERING TOMORROW, EMPOWERING HUMANITY"
Matches Vivo iManager / Clean Master visual aesthetics with 60 FPS GPU-accelerated QPainter animations:
- BrandHeaderWidget: Circular framed logo avatar with rotating cyber ring and official motto
- SegmentedProgressBar: 4-segment glowing green progress bar with laser sweep
- GlowingEnergyShieldWidget: 60 FPS 3-layer cyber energy shield with dual rotating orbit rings
- CyberCircularGauge: Radial cyber arc gauge for CPU, GPU, RAM, Thermals, & Battery
- StepSignalWidget: Stepped ascending cyber signal bars
"""
import math
from pathlib import Path
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, QConicalGradient,
    QFont, QPolygonF, QPixmap, QPainterPath
)

from treviora_defender.config.constants import RESOURCES_DIR
from treviora_defender.ui.animation_clock import SharedAnimationClock


class BrandHeaderWidget(QWidget):
    """
    Renders official TREVIORA INDUSTRY branding:
    - Circular framed logo avatar with rotating glowing cyber orbit ring (60 FPS)
    - Primary title: TREVIORA INDUSTRY
    - Official Motto: "ENGINEERING TOMORROW, EMPOWERING HUMANITY"
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(54)
        self.setMinimumWidth(340)

        self.rotation_angle = 0.0
        self.pulse_phase = 0.0

        # Load avatar pixmap
        avatar_path = RESOURCES_DIR / "treviora_circular_avatar.png"
        if not avatar_path.exists():
            avatar_path = RESOURCES_DIR / "treviora_logo.jpg"

        if avatar_path.exists():
            self.orig_pixmap = QPixmap(str(avatar_path))
        else:
            self.orig_pixmap = None

        # Hook into central shared animation clock (zero CPU overhead)
        SharedAnimationClock.get_clock().tick.connect(self._tick)

    def _tick(self):
        if not self.isVisible():
            return
        self.rotation_angle = (self.rotation_angle + 1.2) % 360.0
        self.pulse_phase = (self.pulse_phase + 0.05) % (math.pi * 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # 1. Draw Circular Logo Avatar with Rotating Neon Ring
        avatar_size = 44.0
        ax = 2.0
        ay = (self.height() - avatar_size) / 2.0
        cx = ax + avatar_size / 2.0
        cy = ay + avatar_size / 2.0
        radius = avatar_size / 2.0 - 2.0

        # Background circular glow
        pulse_alpha = int(80 + 35 * math.sin(self.pulse_phase))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 210, 255, pulse_alpha)))
        painter.drawEllipse(QPointF(cx, cy), radius + 2, radius + 2)

        # Circular masked avatar image
        if self.orig_pixmap:
            path = QPainterPath()
            path.addEllipse(QPointF(cx, cy), radius, radius)
            painter.save()
            painter.setClipPath(path)
            painter.drawPixmap(
                int(cx - radius), int(cy - radius),
                int(radius * 2), int(radius * 2),
                self.orig_pixmap
            )
            painter.restore()
        else:
            # Fallback stylized circle
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(15, 23, 42)))
            painter.drawEllipse(QPointF(cx, cy), radius, radius)
            painter.setPen(QPen(QColor(0, 210, 255), 2))
            painter.drawText(QRectF(ax, ay, avatar_size, avatar_size), Qt.AlignCenter, "TV")

        # Rotating outer neon ring with energy node
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.rotation_angle)

        ring_pen = QPen(QColor(0, 210, 255, 180), 2)
        ring_pen.setStyle(Qt.DashLine)
        painter.setPen(ring_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(0, 0), radius + 2, radius + 2)

        # Orbiting glowing energy node
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 230, 118, 240)))
        painter.drawEllipse(QPointF(radius + 2, 0), 3.0, 3.0)
        painter.restore()

        # 2. Draw Company Title: TREVIORA INDUSTRY
        text_x = ax + avatar_size + 14.0
        painter.setPen(QColor(255, 255, 255))
        font_title = QFont("Segoe UI", 13, QFont.Bold)
        font_title.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        painter.setFont(font_title)
        painter.drawText(int(text_x), int(cy - 2), "TREVIORA INDUSTRY")

        # Cyber blue accent dot beside title
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 210, 255)))
        painter.drawEllipse(QPointF(text_x + 185, cy - 8), 3.0, 3.0)

        # 3. Draw Official Subtitle Tagline: "ENGINEERING TOMORROW, EMPOWERING HUMANITY"
        painter.setPen(QColor(0, 210, 255))
        font_tag = QFont("Segoe UI", 8, QFont.DemiBold)
        font_tag.setLetterSpacing(QFont.AbsoluteSpacing, 0.8)
        painter.setFont(font_tag)
        painter.drawText(
            int(text_x), int(cy + 16),
            '"ENGINEERING TOMORROW, EMPOWERING HUMANITY"'
        )


class SegmentedProgressBar(QWidget):
    """
    Renders 4 rounded glowing green segments with an active laser scan sweep.
    Matches Image 1 and Image 2 with enhanced 60 FPS animation.
    """
    def __init__(self, segments=4, parent=None):
        super().__init__(parent)
        self.segments = segments
        self.active_segment = segments - 1
        self.pulse_phase = 0.0
        self.scan_pos = 0.0
        self.setFixedHeight(12)
        self.setMinimumWidth(260)

        # Hook into central shared animation clock
        SharedAnimationClock.get_clock().tick.connect(self._animate_pulse)

    def _animate_pulse(self):
        if not self.isVisible():
            return
        self.pulse_phase = (self.pulse_phase + 0.05) % (math.pi * 2)
        self.scan_pos = (self.scan_pos + 0.015)
        if self.scan_pos > 1.0:
            self.scan_pos = 0.0
        self.update()

    def set_progress_level(self, level: int):
        self.active_segment = max(0, min(self.segments - 1, level))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        gap = 8
        seg_w = (w - (self.segments - 1) * gap) / self.segments

        for i in range(self.segments):
            x = i * (seg_w + gap)
            rect = QRectF(x, 2, seg_w, h - 4)

            # Gradient from lime-green to emerald-cyan
            grad = QLinearGradient(rect.left(), 0, rect.right(), 0)
            if i <= self.active_segment:
                alpha = int(220 + 35 * math.sin(self.pulse_phase + i))
                grad.setColorAt(0.0, QColor(140, 230, 140, alpha))
                grad.setColorAt(1.0, QColor(0, 210, 180, alpha))
            else:
                grad.setColorAt(0.0, QColor(30, 41, 59, 180))
                grad.setColorAt(1.0, QColor(30, 41, 59, 180))

            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(grad))
            painter.drawRoundedRect(rect, 3, 3)

        # Laser scan pulse indicator on active segment
        if self.active_segment >= 0:
            active_x = self.active_segment * (seg_w + gap) + (seg_w * self.scan_pos)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
            painter.drawRoundedRect(QRectF(active_x - 3, 1, 6, h - 2), 2, 2)


class StepSignalWidget(QWidget):
    """
    Renders 4 ascending stepped signal bars as seen in Image 1 (Security Scan card)
    with animated gradient glow.
    """
    def __init__(self, active_bars=3, parent=None):
        super().__init__(parent)
        self.active_bars = active_bars
        self.pulse = 0.0
        self.setFixedSize(54, 38)

        # Hook into central shared animation clock
        SharedAnimationClock.get_clock().tick.connect(self._tick)

    def _tick(self):
        if not self.isVisible():
            return
        self.pulse = (self.pulse + 0.06) % (math.pi * 2)
        self.update()

    def set_active_bars(self, count: int):
        self.active_bars = count
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        heights = [12, 18, 26, 34]
        bar_w = 9
        gap = 4

        for i, h in enumerate(heights):
            x = i * (bar_w + gap)
            y = self.height() - h
            rect = QRectF(x, y, bar_w, h)

            if i < self.active_bars:
                alpha = int(220 + 35 * math.sin(self.pulse + i * 0.5))
                grad = QLinearGradient(rect.left(), rect.bottom(), rect.left(), rect.top())
                grad.setColorAt(0.0, QColor(0, 180, 216, alpha))
                grad.setColorAt(1.0, QColor(0, 230, 180, alpha))
                painter.setBrush(QBrush(grad))
            else:
                painter.setBrush(QBrush(QColor(40, 50, 70)))

            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, 3, 3)


class CyberCircularGauge(QWidget):
    """
    Radial Cyber Arc Gauge Widget:
    Renders an animated circular dial with pulsating neon arc, glowing needle,
    and value/title in center. Ideal for live CPU %, GPU %, RAM %, and Thermals.
    """
    def __init__(self, title="CPU", unit="%", size=130, color_theme="cyan", parent=None):
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.color_theme = color_theme  # "cyan", "emerald", "orange", "magenta"
        self.target_value = 0.0
        self.current_value = 0.0
        self.pulse_phase = 0.0

        self.setFixedSize(size, size)

        # Hook into central shared animation clock
        SharedAnimationClock.get_clock().tick.connect(self._animate)

    def set_value(self, val: float):
        self.target_value = max(0.0, min(100.0, float(val)))

    def _animate(self):
        if not self.isVisible():
            return
        # Smooth interpolation towards target
        diff = self.target_value - self.current_value
        if abs(diff) > 0.3:
            self.current_value += diff * 0.15
        else:
            self.current_value = self.target_value

        self.pulse_phase = (self.pulse_phase + 0.05) % (math.pi * 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2.0
        cy = h / 2.0
        radius = min(cx, cy) - 10

        # Colors based on theme
        if self.color_theme == "emerald":
            color1 = QColor(0, 230, 118)
            color2 = QColor(0, 210, 255)
        elif self.color_theme == "orange":
            color1 = QColor(255, 120, 20)
            color2 = QColor(255, 180, 50)
        elif self.color_theme == "magenta":
            color1 = QColor(217, 70, 239)
            color2 = QColor(147, 51, 234)
        else:  # cyan
            color1 = QColor(0, 210, 255)
            color2 = QColor(0, 112, 243)

        # 1. Background Arc Track
        bg_pen = QPen(QColor(25, 35, 55), 7)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.setBrush(Qt.NoBrush)

        # Span from 225 deg down to -45 deg (270 deg total span)
        start_angle = 225 * 16
        span_angle = -270 * 16
        painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2), start_angle, span_angle)

        # 2. Active Value Arc
        progress_ratio = self.current_value / 100.0
        active_span = int(-270.0 * progress_ratio * 16)

        if abs(active_span) > 0:
            # Gradient brush for active arc
            grad = QLinearGradient(cx - radius, cy - radius, cx + radius, cy + radius)
            grad.setColorAt(0.0, color1)
            grad.setColorAt(1.0, color2)

            act_pen = QPen(QBrush(grad), 7)
            act_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(act_pen)
            painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2), start_angle, active_span)

            # Glowing needle indicator at tip of active arc
            current_deg = 225.0 - 270.0 * progress_ratio
            rad = math.radians(current_deg)
            tip_x = cx + radius * math.cos(rad)
            tip_y = cy - radius * math.sin(rad)

            pulse_glow = int(180 + 75 * math.sin(self.pulse_phase))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(255, 255, 255, pulse_glow)))
            painter.drawEllipse(QPointF(tip_x, tip_y), 4.5, 4.5)

        # 3. Center Text: Value & Title
        painter.setPen(QColor(255, 255, 255))
        font_val = QFont("Segoe UI", 16, QFont.Bold)
        painter.setFont(font_val)
        val_str = f"{int(round(self.current_value))}{self.unit}"
        painter.drawText(QRectF(0, cy - 18, w, 24), Qt.AlignCenter, val_str)

        painter.setPen(QColor(148, 163, 184))
        font_title = QFont("Segoe UI", 9, QFont.DemiBold)
        font_title.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)
        painter.setFont(font_title)
        painter.drawText(QRectF(0, cy + 8, w, 16), Qt.AlignCenter, self.title)


class GlowingEnergyShieldWidget(QWidget):
    """
    High-Tech Animated Glowing Energy Shield (Matches Image 3 & Feature 6).
    Draws a glowing 3-layer cyber shield with dual rotating orbit rings,
    pulsing quantum arcs, expanding ripple waves, and central cyber cross emblem.
    60 FPS GPU-smooth animation.
    """
    def __init__(self, size=180, color_theme="cyan", parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.color_theme = color_theme  # "cyan", "orange", or "emerald"
        self.rotation_angle1 = 0.0
        self.rotation_angle2 = 0.0
        self.pulse_factor = 1.0
        self.pulse_dir = 0.02
        self.ripple_phase = 0.0

        # Hook into central shared animation clock
        SharedAnimationClock.get_clock().tick.connect(self._animate)

    def set_theme(self, theme: str):
        self.color_theme = theme
        self.update()

    def _animate(self):
        if not self.isVisible():
            return
        self.rotation_angle1 = (self.rotation_angle1 + 1.0) % 360.0
        self.rotation_angle2 = (self.rotation_angle2 - 0.7) % 360.0
        self.ripple_phase = (self.ripple_phase + 0.04) % (math.pi * 2)

        self.pulse_factor += self.pulse_dir
        if self.pulse_factor > 1.10:
            self.pulse_dir = -0.010
        elif self.pulse_factor < 0.96:
            self.pulse_dir = 0.010
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() / 2.0
        cy = self.height() / 2.0
        radius = min(cx, cy) - 14

        # Color palette
        if self.color_theme == "orange":
            main_color = QColor(255, 120, 20)
            glow_color = QColor(255, 160, 50, 70)
            inner_color = QColor(220, 70, 10)
        elif self.color_theme == "emerald":
            main_color = QColor(16, 215, 140)
            glow_color = QColor(0, 250, 160, 70)
            inner_color = QColor(10, 150, 90)
        else:  # cyan default
            main_color = QColor(0, 210, 255)
            glow_color = QColor(0, 180, 255, 70)
            inner_color = QColor(0, 110, 240)

        # 1. Concentric Expanding Ripple Waves
        ripple_radius = radius * (0.6 + 0.35 * (0.5 + 0.5 * math.sin(self.ripple_phase)))
        ripple_alpha = int(60 * (1.0 - (ripple_radius / radius)))
        painter.setPen(QPen(QColor(main_color.red(), main_color.green(), main_color.blue(), ripple_alpha), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(cx, cy), ripple_radius, ripple_radius)

        # 2. Dual Rotating Orbit Rings
        # Ring 1 (Clockwise)
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.rotation_angle1)

        orbit_pen1 = QPen(glow_color, 3)
        orbit_pen1.setStyle(Qt.DashLine)
        painter.setPen(orbit_pen1)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(0, 0), radius * self.pulse_factor, radius * self.pulse_factor)

        # 3 Orbiting energy nodes
        for deg in [0, 120, 240]:
            rad = math.radians(deg)
            nx = (radius * self.pulse_factor) * math.cos(rad)
            ny = (radius * self.pulse_factor) * math.sin(rad)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(main_color))
            painter.drawEllipse(QPointF(nx, ny), 5, 5)

        painter.restore()

        # Ring 2 (Counter-Clockwise)
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.rotation_angle2)

        orbit_pen2 = QPen(QColor(main_color.red(), main_color.green(), main_color.blue(), 45), 1.5)
        orbit_pen2.setStyle(Qt.DotLine)
        painter.setPen(orbit_pen2)
        painter.drawEllipse(QPointF(0, 0), radius * 0.85, radius * 0.85)
        painter.restore()

        # 3. Main Shield Contour
        shield_poly = QPolygonF([
            QPointF(cx, cy - radius * 0.72),
            QPointF(cx + radius * 0.62, cy - radius * 0.42),
            QPointF(cx + radius * 0.52, cy + radius * 0.35),
            QPointF(cx, cy + radius * 0.82),
            QPointF(cx - radius * 0.52, cy + radius * 0.35),
            QPointF(cx - radius * 0.62, cy - radius * 0.42),
        ])

        # Shield Fill Gradient
        shield_grad = QLinearGradient(cx, cy - radius, cx, cy + radius)
        shield_grad.setColorAt(0.0, main_color)
        shield_grad.setColorAt(1.0, inner_color)

        painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
        painter.setBrush(QBrush(shield_grad))
        painter.drawPolygon(shield_poly)

        # 4. Inner Cyber Cross / Shield Emblem
        cross_w = radius * 0.17
        cross_h = radius * 0.48

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255, 240)))

        # Vertical bar of cross
        painter.drawRoundedRect(QRectF(cx - cross_w / 2.0, cy - cross_h / 2.0, cross_w, cross_h), 4, 4)
        # Horizontal bar of cross
        painter.drawRoundedRect(QRectF(cx - cross_h / 2.0, cy - cross_w / 2.0, cross_h, cross_w), 4, 4)
