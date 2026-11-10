"""
TREVIORA AI DEFENDER - Custom Dedicated UI Components
Guarantees 100% reliable styling, backgrounds, borders, and animations in Qt.
Developer: TREVIORA INDUSTRY
Tagline: "ENGINEERING TOMORROW, EMPOWERING HUMANITY"
"""
import math
from pathlib import Path
from PySide6.QtWidgets import (
    QFrame, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QPixmap, QPainterPath, QFont
)

from treviora_defender.config.constants import RESOURCES_DIR
from treviora_defender.ui.animation_clock import SharedAnimationClock


class ModernCard(QFrame):
    """
    Guaranteed dark glassmorphism card with rounded corners, dark background,
    and responsive cyan glowing border on hover.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ModernCard")
        self.setStyleSheet("""
            QFrame#ModernCard {
                background-color: #0F1726;
                border: 1px solid #1E293B;
                border-radius: 18px;
            }
            QFrame#ModernCard:hover {
                background-color: #131E33;
                border: 1px solid #00D2FF;
            }
        """)


class PillOptimizeButton(QPushButton):
    """
    Prominent mint-green to cyan gradient pill button matching Image 1 & Image 2.
    """
    def __init__(self, text="Optimize", parent=None):
        super().__init__(text, parent)
        self.setObjectName("PillOptimizeButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(42)
        self.setStyleSheet("""
            QPushButton#PillOptimizeButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E676, stop:1 #00B0FF);
                color: #060A10;
                font-family: 'Segoe UI', sans-serif;
                font-size: 15px;
                font-weight: 800;
                border: none;
                border-radius: 21px;
                padding: 0px 32px;
            }
            QPushButton#PillOptimizeButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00FF88, stop:1 #33C5FF);
            }
            QPushButton#PillOptimizeButton:pressed {
                background: #00C853;
            }
        """)


class ToolButton(QPushButton):
    """
    Modern dark secondary button with hover cyan glow for Recommended Tools.
    """
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setObjectName("ToolButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(44)
        self.setStyleSheet("""
            QPushButton#ToolButton {
                background-color: #0F1726;
                color: #E2E8F0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 600;
                border: 1px solid #1E293B;
                border-radius: 14px;
                padding: 0px 20px;
            }
            QPushButton#ToolButton:hover {
                background-color: #162442;
                border: 1px solid #00D2FF;
                color: #FFFFFF;
            }
            QPushButton#ToolButton:pressed {
                background-color: #0B1220;
            }
        """)


class SafeGuardPillButton(QPushButton):
    """
    Top SafeGuard Firewall status pill button with dynamic Active/Deactivated toggle styling.
    """
    def __init__(self, text="🛡️ SafeGuard 3-Layer Firewall: ACTIVE ●", parent=None):
        super().__init__(text, parent)
        self.setObjectName("SafeGuardPillButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(36)
        self.is_active = True
        self.set_shield_active(True)

    def set_shield_active(self, active: bool):
        self.is_active = active
        if active:
            self.setText("🛡️ SafeGuard 3-Layer Firewall: ACTIVE ●")
            self.setStyleSheet("""
                QPushButton#SafeGuardPillButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0B1930, stop:1 #132A52);
                    color: #00D2FF;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 12px;
                    font-weight: 700;
                    border: 1px solid #00D2FF;
                    border-radius: 18px;
                    padding: 0px 18px;
                }
                QPushButton#SafeGuardPillButton:hover {
                    background: #1B3A70;
                    border: 1px solid #38BDF8;
                    color: #FFFFFF;
                }
            """)
        else:
            self.setText("🛡️ SafeGuard 3-Layer Firewall: DEACTIVATED ○")
            self.setStyleSheet("""
                QPushButton#SafeGuardPillButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2A1215, stop:1 #3B1A1E);
                    color: #F87171;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 12px;
                    font-weight: 700;
                    border: 1px solid #EF4444;
                    border-radius: 18px;
                    padding: 0px 18px;
                }
                QPushButton#SafeGuardPillButton:hover {
                    background: #4C1D24;
                    border: 1px solid #FCA5A5;
                    color: #FFFFFF;
                }
            """)


class CircularAvatarWidget(QWidget):
    """
    Renders the official logo inside an anti-aliased circular frame
    with a 60 FPS glowing neon orbit ring.
    """
    def __init__(self, size=48, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.rotation_angle = 0.0
        self.pulse_phase = 0.0
        self._frame_count = 0

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
        self._frame_count += 1
        if self._frame_count % 2 != 0:
            return
        self.rotation_angle = (self.rotation_angle + 2.0) % 360.0
        self.pulse_phase = (self.pulse_phase + 0.07) % (math.pi * 2)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        cx = self.width() / 2.0
        cy = self.height() / 2.0
        radius = min(cx, cy) - 3.0

        # Background circular glow
        pulse_alpha = int(70 + 35 * math.sin(self.pulse_phase))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 210, 255, pulse_alpha)))
        painter.drawEllipse(QPointF(cx, cy), radius + 2, radius + 2)

        # Circular masked avatar
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
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(15, 23, 42)))
            painter.drawEllipse(QPointF(cx, cy), radius, radius)

        # Rotating outer neon dashed ring
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.rotation_angle)

        ring_pen = QPen(QColor(0, 210, 255, 200), 2)
        ring_pen.setStyle(Qt.DashLine)
        painter.setPen(ring_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPointF(0, 0), radius + 1, radius + 1)

        # Orbiting glowing energy node
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 230, 118, 240)))
        painter.drawEllipse(QPointF(radius + 1, 0), 3.0, 3.0)
        painter.restore()


class BrandHeaderWidget(QWidget):
    """
    Official TREVIORA INDUSTRY brand header:
    - Circular logo avatar with 60 FPS neon orbit ring
    - Company title: TREVIORA INDUSTRY
    - Official Motto: "ENGINEERING TOMORROW, EMPOWERING HUMANITY" (Never clipped)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(54)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # Circular avatar
        self.avatar = CircularAvatarWidget(size=46)
        layout.addWidget(self.avatar)

        # Text stack
        t_box = QVBoxLayout()
        t_box.setContentsMargins(0, 4, 0, 4)
        t_box.setSpacing(2)

        self.lbl_title = QLabel("TREVIORA INDUSTRY")
        self.lbl_title.setStyleSheet("""
            color: #FFFFFF;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 1.2px;
        """)

        self.lbl_motto = QLabel('"ENGINEERING TOMORROW, EMPOWERING HUMANITY"')
        self.lbl_motto.setStyleSheet("""
            color: #00D2FF;
            font-family: 'Segoe UI', 'Inter', sans-serif;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 0.8px;
        """)

        t_box.addWidget(self.lbl_title)
        t_box.addWidget(self.lbl_motto)
        layout.addLayout(t_box)
        layout.addStretch()
