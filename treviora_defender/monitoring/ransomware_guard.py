"""
TREVIORA AI DEFENDER - Ransomware Protection & Canary Guard
Monitors for:
- Rapid mass file modifications/renames (>15 within 4 seconds)
- Known ransomware extensions (.locked, .crypto, .crypted, .wncry, .lockbit, etc.)
- Canary honeypot alteration (decoy files located strictly on D: drive)
- Uncontrolled mass encryption behavior
"""
import os
import time
import threading
from pathlib import Path
from collections import deque
from treviora_defender.config.constants import DATA_DIR
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.utils.logger import get_logger

logger = get_logger()

KNOWN_RANSOM_EXTENSIONS = {
    ".locked", ".crypto", ".crypt", ".crypted", ".wncry", ".lockbit",
    ".blackcat", ".darkside", ".revil", ".ryuk", ".enc", ".encrypted",
    ".ransom", ".pay_here", ".wallet"
}

CANARY_DIR = DATA_DIR / "canaries"


class RansomwareGuard:
    def __init__(self, alert_callback=None):
        self.alert_callback = alert_callback
        self.db = DatabaseManager()
        self._recent_file_events = deque()  # (timestamp, path, action)
        self._lock = threading.Lock()
        self._is_active = False
        self._canary_hashes = {}
        self._init_canary_honeypots()

    def _init_canary_honeypots(self):
        r"""
        Deploys safe decoy canary files in D:\projects\antivirus\data\canaries.
        If an autonomous ransomware starts encrypting directories on D: or C:,
        the canaries will be touched first, triggering immediate containment.
        """
        CANARY_DIR.mkdir(parents=True, exist_ok=True)
        canary_names = ["passwords_backup.xlsx", "personal_photos.zip", "finance_2026.docx"]

        for name in canary_names:
            c_path = CANARY_DIR / name
            if not c_path.exists():
                with open(c_path, "wb") as f:
                    f.write(f"TREVIORA_CANARY_INTEGRITY_CHECK_{name}".encode("utf-8") * 20)
            self._canary_hashes[str(c_path)] = c_path.stat().st_size

    def record_file_event(self, file_path: str, action: str):
        """
        Receives notification from filesystem listener and checks for ransomware velocity.
        """
        now = time.time()
        p = Path(file_path)
        ext = p.suffix.lower()

        with self._lock:
            # Check 1: Known Ransomware Extension
            if ext in KNOWN_RANSOM_EXTENSIONS:
                alert = {
                    "type": "Ransomware Extension",
                    "file_path": file_path,
                    "extension": ext,
                    "severity": "Critical",
                    "description": f"File created or renamed with known ransomware extension '{ext}'."
                }
                self._dispatch_alert(alert)
                return

            # Check 2: Canary Honeypot Tampering
            if str(p) in self._canary_hashes:
                if not p.exists() or p.stat().st_size != self._canary_hashes[str(p)]:
                    alert = {
                        "type": "Canary Honeypot Tripped",
                        "file_path": file_path,
                        "severity": "Critical",
                        "description": "Decoy canary document was modified or deleted! Potential active ransomware!"
                    }
                    self._dispatch_alert(alert)
                    return

            # Check 3: Velocity Check (>15 modifications within 4 seconds)
            self._recent_file_events.append((now, file_path, action))

            # Evict entries older than 4 seconds
            while self._recent_file_events and (now - self._recent_file_events[0][0]) > 4.0:
                self._recent_file_events.popleft()

            if len(self._recent_file_events) >= 15:
                affected_sample = [e[1] for e in list(self._recent_file_events)[:5]]
                alert = {
                    "type": "Mass File Modification Velocity",
                    "count": len(self._recent_file_events),
                    "sample": affected_sample,
                    "severity": "High",
                    "description": f"Rapid mass file modifications detected ({len(self._recent_file_events)} events in 4s). Typical of ransomware encryption."
                }
                self._dispatch_alert(alert)
                self._recent_file_events.clear()

    def _dispatch_alert(self, alert: dict):
        logger.warning(f"[RansomwareGuard ALERT] {alert['description']}")
        self.db.log_event(
            event_type="RansomwareAlert",
            source="RansomwareGuard",
            description=alert["description"],
            severity=alert.get("severity", "Critical")
        )
        if self.alert_callback:
            self.alert_callback(alert)

    def start(self):
        self._is_active = True
        logger.info("Ransomware Guard initialized and active.")

    def stop(self):
        self._is_active = False
        logger.info("Ransomware Guard stopped.")
