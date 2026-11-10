"""
TREVIORA AI DEFENDER - Constants and Configurations
All data, models, quarantine, and database files reside strictly in D: drive.
"""
from pathlib import Path

APP_NAME = "TREVIORA AI DEFENDER"
APP_VERSION = "2.1.0"
DEVELOPER = "TREVIORA INDUSTRY"
TAGLINE = "ENGINEERING TOMORROW, EMPOWERING HUMANITY"
COPYRIGHT = "© 2026 TREVIORA INDUSTRY. All Rights Reserved."

# STRICT D: DRIVE PATHS ONLY - As requested by user, no data stored on C:
BASE_DIR = Path("D:/projects/antivirus").resolve()
DATA_DIR = BASE_DIR / "data"
QUARANTINE_DIR = DATA_DIR / "quarantine"
LOGS_DIR = DATA_DIR / "logs"
RULES_DIR = DATA_DIR / "rules"
MODELS_DIR = DATA_DIR / "models"
RESOURCES_DIR = BASE_DIR / "resources"
DB_PATH = DATA_DIR / "defender.db"
CONFIG_FILE = DATA_DIR / "config.json"

# Threat Severity Levels
SEVERITY_CLEAN = "Clean"
SEVERITY_LOW = "Low"
SEVERITY_MEDIUM = "Medium"
SEVERITY_HIGH = "High"
SEVERITY_CRITICAL = "Critical"

# Threat Categories
CATEGORY_MALWARE = "Malware"
CATEGORY_TROJAN = "Trojan"
CATEGORY_RANSOMWARE = "Ransomware"
CATEGORY_SPYWARE = "Spyware"
CATEGORY_PUA = "Potentially Unwanted Application"
CATEGORY_SUSPICIOUS = "Suspicious Behavior"
CATEGORY_HEURISTIC = "Heuristic Anomaly"
CATEGORY_EICAR = "EICAR Test String"

# Default Exclusions & Safe Extensions
SAFE_EXTENSIONS = {
    ".txt", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".mp3", ".mp4",
    ".avi", ".wav", ".csv", ".xlsx", ".docx", ".pptx", ".md", ".json"
}

EXECUTABLE_EXTENSIONS = {
    ".exe", ".dll", ".sys", ".bat", ".cmd", ".vbs", ".ps1", ".scr",
    ".com", ".pif", ".cpl", ".hta", ".wsf", ".jar", ".msi"
}

# AI Engine Weights
RISK_THRESHOLD_SAFE = 25
RISK_THRESHOLD_SUSPICIOUS = 65
RISK_THRESHOLD_MALICIOUS = 80
