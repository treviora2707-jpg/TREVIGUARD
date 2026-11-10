"""
TREVIORA AI DEFENDER - Real-Time Filesystem Monitor
Uses watchdog to monitor newly created and modified files across Downloads, Desktop, and Temp.
Performs immediate AI & Hash analysis on new executables and documents.
"""
import os
import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

from treviora_defender.config.settings import SettingsManager
from treviora_defender.core.scanner import AntivirusScanner
from treviora_defender.quarantine.quarantine_manager import QuarantineManager
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class RealTimeFileHandler(FileSystemEventHandler):
    def __init__(self, scanner: AntivirusScanner, quarantine_mgr: QuarantineManager, event_callback=None):
        super().__init__()
        self.scanner = scanner
        self.quarantine_mgr = quarantine_mgr
        self.event_callback = event_callback
        self.settings = SettingsManager()
        self.db = DatabaseManager()
        self._recently_scanned = {}
        self._lock = threading.Lock()

    def _process_file(self, file_path: str, action: str):
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            return

        now = time.time()
        with self._lock:
            # Debounce rapid duplicate events on the same file within 3 seconds
            if file_path in self._recently_scanned and (now - self._recently_scanned[file_path]) < 3.0:
                return
            self._recently_scanned[file_path] = now

        # Ignore project internal files, databases, logs, source code, and cache
        lower_path = file_path.lower().replace("\\", "/")
        ignored_patterns = [
            "/quarantine", "/data/", "/build/", "/dist/", "/__pycache__/", "/.git/",
            "/treviora_defender/", ".pyc", ".db", ".log", ".tquar", ".json", ".md", ".spec", ".png", ".jpg"
        ]
        if any(ig in lower_path for ig in ignored_patterns):
            return

        # Target executable and high-risk payload formats
        target_exts = {".exe", ".dll", ".sys", ".scr", ".vbs", ".ps1", ".hta", ".js", ".docm", ".xlsm", ".iso", ".bat", ".cmd"}
        if p.suffix.lower() not in target_exts:
            return

        try:
            # Let file settle if it's being written
            time.sleep(0.1)
            res = self.scanner.scan_single_file(file_path)

            if res.is_threat:
                logger.warning(f"[RealTimeAlert] Threat detected: {res.threat_name} in {file_path}")
                self.db.log_event(
                    event_type="RealTimeThreat",
                    source="RealTimeMonitor",
                    description=f"Detected {res.threat_name} ({res.severity}) during {action} in '{file_path}'",
                    severity=res.severity
                )

                quarantined = False
                if self.settings.get("auto_quarantine_critical", True):
                    q_res = self.quarantine_mgr.quarantine_file(file_path, threat_name=res.threat_name)
                    quarantined = q_res.get("success", False)

                if self.event_callback:
                    self.event_callback({
                        "file_path": file_path,
                        "action": action,
                        "threat_name": res.threat_name,
                        "severity": res.severity,
                        "risk_score": res.risk_score,
                        "quarantined": quarantined,
                        "explanation": res.ai_explanation
                    })
        except Exception as e:
            logger.debug(f"Error in real-time processing of {file_path}: {e}")

    def on_created(self, event):
        if not event.is_directory:
            self._process_file(event.src_path, "Created")

    def on_modified(self, event):
        if not event.is_directory:
            self._process_file(event.src_path, "Modified")


class RealTimeMonitor:
    def __init__(self, event_callback=None):
        self.settings = SettingsManager()
        self.scanner = AntivirusScanner()
        self.quarantine_mgr = QuarantineManager()
        self.event_callback = event_callback
        self.observer = None
        self.is_running = False

    def start(self):
        if self.is_running:
            return

        watch_dirs = []
        user_home = Path.home()

        # Watch honeypot canary decoys and common drop folders
        canary_dir = Path("D:/projects/antivirus/data/canaries")
        if canary_dir.exists():
            watch_dirs.append(str(canary_dir))

        for sub in ["Downloads", "Desktop"]:
            p = user_home / sub
            if p.exists() and os.access(p, os.R_OK):
                watch_dirs.append(str(p))

        handler = RealTimeFileHandler(self.scanner, self.quarantine_mgr, self.event_callback)

        # Attempt native Win32 ReadDirectoryChangesW observer, fallback to PollingObserver
        try:
            self.observer = Observer()
            for d in watch_dirs:
                try:
                    self.observer.schedule(handler, d, recursive=False)
                    logger.info(f"Real-Time File Protection actively watching: {d}")
                except Exception as e:
                    logger.warning(f"Could not watch directory {d}: {e}")

            self.observer.start()
            self.is_running = True
            logger.info("Real-Time Monitor started with native Windows observer.")
        except Exception as e:
            logger.warning(f"Native observer initialization failed ({e}), switching to reliable PollingObserver...")
            try:
                self.observer = PollingObserver(timeout=2.0)
                for d in watch_dirs:
                    self.observer.schedule(handler, d, recursive=False)
                self.observer.start()
                self.is_running = True
                logger.info("Real-Time Monitor started with PollingObserver.")
            except Exception as e2:
                logger.error(f"Failed to start fallback PollingObserver: {e2}")

    def stop(self):
        if self.observer and self.is_running:
            try:
                self.observer.stop()
                self.observer.join(timeout=3)
            except Exception as e:
                logger.debug(f"Error stopping observer: {e}")
            self.is_running = False
            logger.info("Real-Time Monitor stopped.")
