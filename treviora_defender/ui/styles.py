"""
TREVIORA AI DEFENDER - Premium Dark Cybersecurity QSS Stylesheet
Theme: Cyberpunk Deep Charcoal & Electric Cyan/Blue Glassmorphism
"""

MAIN_STYLE = """
/* Global Window & Fonts */
QWidget {
    background-color: #0B0F19;
    color: #E2E8F0;
    font-family: 'Segoe UI', 'Inter', -apple-system, sans-serif;
    font-size: 13px;
    selection-background-color: #0070F3;
    selection-color: #FFFFFF;
}

/* Sidebar Navigation */
#SidebarWidget {
    background-color: #0F172A;
    border-right: 1px solid #1E293B;
}

#AppLogoTitle {
    color: #00D2FF;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

#AppSubTitle {
    color: #64748B;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.0px;
}

QPushButton.NavButton {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}

QPushButton.NavButton:hover {
    background-color: #1E293B;
    color: #38BDF8;
}

QPushButton.NavButton:checked, QPushButton.NavButton.active {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
    color: #FFFFFF;
    font-weight: 700;
}

/* Glassmorphism Cards */
QFrame.GlassCard {
    background-color: #131B2E;
    border: 1px solid #1E293B;
    border-radius: 12px;
}

QFrame.GlassCard:hover {
    border: 1px solid #334155;
}

QFrame.GlassCardHighlight {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #111C38, stop:1 #131B2E);
    border: 1px solid #00D2FF;
    border-radius: 12px;
}

/* Headings */
QLabel.PageTitle {
    color: #F8FAFC;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

QLabel.PageSubtitle {
    color: #94A3B8;
    font-size: 12px;
}

QLabel.CardTitle {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

QLabel.CardValue {
    color: #F8FAFC;
    font-size: 26px;
    font-weight: 800;
}

/* Primary Action Buttons */
QPushButton.PrimaryButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
}

QPushButton.PrimaryButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0060DF, stop:1 #00BEF0);
}

QPushButton.PrimaryButton:pressed {
    background-color: #0050BF;
}

QPushButton.SecondaryButton {
    background-color: #1E293B;
    color: #E2E8F0;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}

QPushButton.SecondaryButton:hover {
    background-color: #334155;
    color: #FFFFFF;
    border-color: #475569;
}

QPushButton.DangerButton {
    background-color: #EF4444;
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
}

QPushButton.DangerButton:hover {
    background-color: #DC2626;
}

QPushButton.SuccessButton {
    background-color: #10B981;
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 12px;
}

QPushButton.SuccessButton:hover {
    background-color: #059669;
}

/* Tables */
QTableWidget {
    background-color: #10172A;
    alternate-background-color: #0E1626;
    border: 1px solid #1E293B;
    border-radius: 8px;
    gridline-color: #1E293B;
    color: #E2E8F0;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #1E293B;
}

QTableWidget::item:selected {
    background-color: #1E293B;
    color: #00D2FF;
}

QHeaderView::section {
    background-color: #0F172A;
    color: #94A3B8;
    padding: 8px;
    font-weight: 600;
    border: none;
    border-bottom: 1px solid #334155;
}

/* Checkboxes */
QCheckBox {
    color: #E2E8F0;
    font-size: 13px;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid #334155;
    background-color: #0F172A;
}

QCheckBox::indicator:hover {
    border-color: #00D2FF;
}

QCheckBox::indicator:checked {
    background-color: #0070F3;
    border-color: #00D2FF;
}

/* Dialogs & Message Boxes */
QDialog, QMessageBox {
    background-color: #0F172A;
    color: #F8FAFC;
    border: 1px solid #1E293B;
    border-radius: 12px;
}

QMessageBox QLabel {
    color: #F8FAFC;
    font-size: 13px;
}

/* Inputs & Text Edits */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #00D2FF;
}

/* Progress Bar */
QProgressBar {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 6px;
    text-align: center;
    color: #FFFFFF;
    font-weight: 600;
    height: 18px;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0070F3, stop:1 #00D2FF);
    border-radius: 5px;
}

/* Scrollbars */
QScrollBar:vertical {
    background-color: #0B0F19;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #1E293B;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #334155;
}

QScrollBar:horizontal {
    background-color: #0B0F19;
    height: 8px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #1E293B;
    border-radius: 4px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #334155;
}

QScrollBar::add-line, QScrollBar::sub-line {
    width: 0px;
    height: 0px;
}

/* Top bar device info pill */
#DevicePill {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 4px 10px;
    color: #94A3B8;
    font-size: 11px;
}

/* Modern Rounded Cards (iManager High-Tech Glass Style) */
QFrame.ModernCard {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #111A2E, stop:1 #0B1220);
    border: 1px solid #1E293B;
    border-radius: 18px;
}

QFrame.ModernCard:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #162442, stop:1 #0F1A2E);
    border: 1px solid #00D2FF;
}

#HeroScoreLabel {
    color: #FFFFFF;
    font-size: 68px;
    font-weight: 800;
    line-height: 1.0;
}

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
    padding: 8px 24px;
}

QPushButton.BottomNavBtn:hover {
    color: #00D2FF;
}

QPushButton.BottomNavBtn:checked, QPushButton.BottomNavBtn.active {
    color: #00E676;
    font-weight: 800;
}
"""
