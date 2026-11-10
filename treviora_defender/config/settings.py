"""
TREVIORA AI DEFENDER - Settings Management
"""
import json
from pathlib import Path
from treviora_defender.config.constants import CONFIG_FILE, DATA_DIR, QUARANTINE_DIR, LOGS_DIR, RULES_DIR, MODELS_DIR

DEFAULT_SETTINGS = {
    "app_name": "TREVIORA AI DEFENDER",
    "version": "2.1.0",
    "real_time_protection": True,
    "ai_engine_enabled": True,
    "ransomware_protection": True,
    "network_monitor_enabled": True,
    "usb_auto_scan": True,
    "cloud_ai_enabled": False,
    "cloud_ai_api_key": "",
    "cloud_ai_endpoint": "https://api.openai.com/v1",
    "cloud_ai_provider": "OpenAI Compatible",
    "local_ai_endpoint": "http://localhost:11434",
    "ai_risk_threshold": 65,
    "auto_quarantine_critical": True,
    "scan_archive_files": True,
    "scan_max_file_size_mb": 250,
    "sound_alerts": True,
    "start_with_windows": False,
    "exclusions": [
        "D:\\projects\\antivirus\\data\\quarantine",
        "C:\\Windows\\System32\\ntoskrnl.exe"
    ],
    "storage_drive": "D:",
    "last_quick_scan": None,
    "last_full_scan": None,
    "theme": "cyber_dark"
}


class SettingsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance._init_settings()
        return cls._instance

    def _init_settings(self):
        # Ensure directories exist strictly on D:
        for d in [DATA_DIR, QUARANTINE_DIR, LOGS_DIR, RULES_DIR, MODELS_DIR]:
            d.mkdir(parents=True, exist_ok=True)

        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.settings.update(saved)
            except Exception as e:
                print(f"[SettingsManager] Warning loading config: {e}")
        else:
            self.save()

    def save(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"[SettingsManager] Failed saving config: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def add_exclusion(self, path_str: str):
        excls = self.settings.get("exclusions", [])
        norm = str(Path(path_str).resolve())
        if norm not in excls:
            excls.append(norm)
            self.settings["exclusions"] = excls
            self.save()

    def remove_exclusion(self, path_str: str):
        excls = self.settings.get("exclusions", [])
        norm = str(Path(path_str).resolve())
        if norm in excls:
            excls.remove(norm)
            self.settings["exclusions"] = excls
            self.save()

    def is_excluded(self, path_str: str) -> bool:
        try:
            target = Path(path_str).resolve()
            for excl in self.settings.get("exclusions", []):
                excl_path = Path(excl).resolve()
                if target == excl_path or excl_path in target.parents:
                    return True
        except Exception:
            pass
        return False
