"""
TREVIORA AI DEFENDER - iManager High-Tech Cyber Dark Theme
Aesthetics: Vivo iManager / Clean Master Mobile-Inspired Elegance for Windows 11
"""

IMANAGER_STYLE = """
/* Base Window & Global Typography */
QWidget {
    background-color: #060911;
    color: #F1F5F9;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
    font-size: 13px;
    outline: none;
}

/* Scroll Area & Viewport */
QScrollArea {
    background-color: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

/* Modern Rounded Cards (iManager Style) */
QFrame.ModernCard {
    background-color: #0F1726;
    border: 1px solid #1E293B;
    border-radius: 16px;
}

QFrame.ModernCard:hover {
    background-color: #131E33;
    border: 1px solid #334155;
}

/* Clickable Modern Card Highlight */
QFrame.CardHighlight {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #101E38, stop:1 #0F1726);
    border: 1px solid #00D2FF;
    border-radius: 16px;
}

/* Top App Header */
#AppHeaderTitle {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

#AppHeaderSub {
    color: #64748B;
    font-size: 11px;
    font-weight: 600;
}

/* Big Hero Score Number */
#HeroScoreLabel {
    color: #FFFFFF;
    font-size: 68px;
    font-weight: 800;
    line-height: 1.0;
}

/* Mint Green Pill Button (Optimize Button from Image 1) */
QPushButton.PillOptimizeButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E676, stop:1 #00B0FF);
    color: #060A10;
    font-size: 14px;
    font-weight: 800;
    border: none;
    border-radius: 20px;
    padding: 10px 24px;
}

QPushButton.PillOptimizeButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00FF88, stop:1 #33C5FF);
}

QPushButton.PillOptimizeButton:pressed {
    background-color: #00C853;
}

/* Stop Button / Cancel Button (Image 2 & 3) */
QPushButton.StopButton {
    background-color: #00D2FF;
    color: #060A10;
    font-size: 14px;
    font-weight: 800;
    border: none;
    border-radius: 22px;
    padding: 12px 28px;
}

QPushButton.StopButton:hover {
    background-color: #38BDF8;
}

/* Secondary Action Button */
QPushButton.ModernSecondary {
    background-color: #1E293B;
    color: #E2E8F0;
    font-size: 13px;
    font-weight: 600;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 8px 16px;
}

QPushButton.ModernSecondary:hover {
    background-color: #334155;
    color: #FFFFFF;
}

/* Safe Guard Top Energy Shield Button */
QPushButton.SafeGuardPill {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0B1930, stop:1 #132A52);
    color: #00D2FF;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid #00D2FF;
    border-radius: 16px;
    padding: 6px 16px;
}

QPushButton.SafeGuardPill:hover {
    background-color: #1B3A70;
}

/* Card Titles and Text */
QLabel.CardHeader {
    color: #94A3B8;
    font-size: 12px;
    font-weight: 600;
}

QLabel.CardTitleBold {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 700;
}

QLabel.CardDesc {
    color: #64748B;
    font-size: 12px;
}

/* Storage Bar */
QProgressBar.StorageBar {
    background-color: #1E293B;
    border: none;
    border-radius: 5px;
    height: 10px;
    text-align: right;
}

QProgressBar.StorageBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
    border-radius: 5px;
}

/* Bottom Tab Navigation Bar (iManager Style) */
#BottomNavBar {
    background-color: #080D18;
    border-top: 1px solid #1E293B;
}

QPushButton.BottomNavBtn {
    background-color: transparent;
    color: #64748B;
    border: none;
    font-size: 12px;
    font-weight: 600;
    padding: 8px 16px;
}

QPushButton.BottomNavBtn:hover {
    color: #00D2FF;
}

QPushButton.BottomNavBtn:checked, QPushButton.BottomNavBtn.active {
    color: #00E676;
    font-weight: 800;
}

/* Tables */
QTableWidget {
    background-color: #0F1726;
    alternate-background-color: #0A111C;
    border: 1px solid #1E293B;
    border-radius: 12px;
    gridline-color: #1E293B;
    color: #F1F5F9;
}

QTableWidget::item {
    padding: 10px;
    border-bottom: 1px solid #1E293B;
}

QHeaderView::section {
    background-color: #090E17;
    color: #94A3B8;
    padding: 10px;
    font-weight: 700;
    border: none;
    border-bottom: 1px solid #1E293B;
}

/* Scrollbars */
QScrollBar:vertical {
    background-color: transparent;
    width: 6px;
}

QScrollBar::handle:vertical {
    background-color: #1E293B;
    border-radius: 3px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00D2FF;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0px;
}
"""
