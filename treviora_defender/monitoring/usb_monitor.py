"""
TREVIORA AI DEFENDER - USB Storage Guardian
Detects USB drive insertion, scans for autorun.inf anomalies and shortcut malware,
and triggers automatic security reports.
"""
import time
import threading
from pathlib import Path
from treviora_defender.config.settings import SettingsManager
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.utils.win_utils import get_removable_drives
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class USBMonitor:
    def __init__(self, insertion_callback=None):
        self.insertion_callback = insertion_callback
        self.settings = SettingsManager()
        self.db = DatabaseManager()
        self._is_running = False
        self._thread = None
        self._stop_event = threading.Event()
        self._known_drives = set()

    def start(self):
        if self._is_running:
            return
        self._is_running = True
        self._stop_event.clear()
        self._known_drives = set(get_removable_drives())
        self._thread = threading.Thread(target=self._poll_loop, daemon=True, name="USBMonitorThread")
        self._thread.start()
        logger.info(f"USB Monitor started. Initial connected removable drives: {list(self._known_drives)}")

    def stop(self):
        self._is_running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=0.3)
            self._thread = None
        logger.info("USB Monitor stopped.")

    def _poll_loop(self):
        while self._is_running and not self._stop_event.is_set():
            try:
                current_drives = set(get_removable_drives())
                new_drives = current_drives - self._known_drives

                for drive in new_drives:
                    logger.info(f"New USB Removable Drive detected: {drive}")
                    self.db.log_event(
                        event_type="USBConnected",
                        source="USBMonitor",
                        description=f"Removable storage volume {drive} connected to system.",
                        severity="Info"
                    )
                    # Check for classic USB worm artifacts
                    quick_usb_check = self.inspect_usb_drive(drive)

                    if self.insertion_callback:
                        self.insertion_callback({
                            "drive": drive,
                            "quick_check": quick_usb_check,
                            "auto_scan": self.settings.get("usb_auto_scan", True)
                        })

                self._known_drives = current_drives
            except Exception as e:
                logger.debug(f"USB poll loop error: {e}")

            # Non-blocking interruptible sleep
            self._stop_event.wait(timeout=3.0)

    @staticmethod
    def inspect_usb_drive(drive_path: str) -> dict:
        """
        Fast inspection of a USB drive root for typical malware artifacts:
        - autorun.inf files
        - hidden .exe or .scr files
        - suspicious .lnk shortcuts
        """
        p = Path(drive_path)
        artifacts = []

        if not p.exists():
            return {"artifacts": [], "is_suspicious": False}

        autorun = p / "autorun.inf"
        if autorun.exists():
            artifacts.append("Detected autorun.inf file (legacy auto-execution vector)")

        try:
            for item in p.iterdir():
                if item.is_file():
                    ext = item.suffix.lower()
                    if ext in [".exe", ".bat", ".cmd", ".scr", ".vbs"] and item.name.startswith("."):
                        artifacts.append(f"Hidden executable on USB root: {item.name}")
                    elif ext == ".lnk":
                        artifacts.append(f"Shortcut file on USB root: {item.name}")
        except Exception:
            pass

        return {
            "drive": drive_path,
            "artifacts": artifacts,
            "is_suspicious": (len(artifacts) > 0)
        }
