"""
TREVIORA AI DEFENDER - Status Card & Circular Security Meter
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = "", accent_color: str = "#00D2FF"):
        super().__init__()
        self.setProperty("class", "GlassCard")
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        self.title_label = QLabel(title)
        self.title_label.setProperty("class", "CardTitle")

        self.value_label = QLabel(value)
        self.value_label.setProperty("class", "CardValue")
        self.value_label.setStyleSheet(f"color: {accent_color}; font-size: 26px; font-weight: 800;")

        self.sub_label = QLabel(subtitle)
        self.sub_label.setStyleSheet("color: #64748B; font-size: 11px;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.sub_label)

    def set_value(self, val: str):
        self.value_label.setText(val)

    def set_subtitle(self, sub: str):
        self.sub_label.setText(sub)


class CircularScoreWidget(QWidget):
    """
    Renders an animated circular security score meter (0 to 100)
    with color gradient ranging from Red (low score) to Emerald Green (100% score).
    """
    def __init__(self, score: int = 98):
        super().__init__()
        self.score = score
        self.setFixedSize(140, 140)

    def set_score(self, score: int):
        self.score = max(0, min(100, score))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(12, 12, self.width() - 24, self.height() - 24)

        # Background track
        bg_pen = QPen(QColor("#1E293B"), 10)
        bg_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(rect, -90 * 16, -360 * 16)

        # Foreground score arc
        if self.score >= 90:
            stroke_color = QColor("#10B981") # Green
        elif self.score >= 70:
            stroke_color = QColor("#00D2FF") # Cyan
        elif self.score >= 50:
            stroke_color = QColor("#F59E0B") # Amber
        else:
            stroke_color = QColor("#EF4444") # Red

        score_pen = QPen(stroke_color, 10)
        score_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(score_pen)

        span_angle = int(-(self.score / 100.0) * 360 * 16)
        painter.drawArc(rect, 90 * 16, span_angle)

        # Text in center
        painter.setPen(QColor("#FFFFFF"))
        font = QFont("Segoe UI", 24, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, f"{self.score}%")

        sub_font = QFont("Segoe UI", 9)
        painter.setFont(sub_font)
        painter.setPen(QColor("#94A3B8"))
        painter.drawText(QRectF(12, 92, self.width() - 24, 25), Qt.AlignCenter, "SECURITY")
