"""
TREVIORA AI DEFENDER - Core Antivirus Scanner
Coordinates File Hash Analysis, YARA Signature Scanning, Digital Signature Verification,
and AI-Powered Threat Scoring.
Provides Quick Scan, Full System Scan, Custom Folder Scan, USB Drive Scan, and Download Folder Scan.
"""
import os
import time
import threading
from pathlib import Path
from treviora_defender.config.constants import (
    EXECUTABLE_EXTENSIONS, CATEGORY_MALWARE, CATEGORY_TROJAN, CATEGORY_PUA,
    SEVERITY_HIGH, SEVERITY_CRITICAL
)
from treviora_defender.config.settings import SettingsManager
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.core.hash_analyzer import HashAnalyzer
from treviora_defender.core.yara_engine import YaraEngine
from treviora_defender.core.ai_engine import AIEngine
from treviora_defender.utils.win_utils import get_startup_persistence_entries, get_removable_drives
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class ScanResult:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.is_threat = False
        self.threat_name = "Clean"
        self.category = "None"
        self.severity = "Clean"
        self.risk_score = 0.0
        self.detection_method = "None"
        self.ai_explanation = ""
        self.file_hash = ""
        self.signed = False


class AntivirusScanner:
    def __init__(self):
        self.settings = SettingsManager()
        self.db = DatabaseManager()
        self.hash_analyzer = HashAnalyzer()
        self.yara_engine = YaraEngine()
        self.ai_engine = AIEngine()

        self._cancel_requested = False
        self._pause_requested = False
        self._is_scanning = False
        self._lock = threading.Lock()

    def request_cancel(self):
        with self._lock:
            self._cancel_requested = True

    def is_cancelled(self) -> bool:
        with self._lock:
            return self._cancel_requested

    def scan_single_file(self, file_path: str) -> ScanResult:
        """
        Inspects an individual file through the multi-layer pipeline:
        Layer 1: Exclusion Check
        Layer 2: Known Threat Hash Database
        Layer 3: YARA Rules Matching
        Layer 4: AI Model & Heuristic Anomaly Scoring
        """
        result = ScanResult(file_path)
        path_obj = Path(file_path)

        if not path_obj.exists() or not path_obj.is_file():
            return result

        if self.settings.is_excluded(file_path):
            return result

        # Compute hash
        hashes = self.hash_analyzer.compute_hashes(file_path)
        result.file_hash = hashes.get("sha256", "")

        # Layer 1: Known Hash Lookup
        hash_res = self.hash_analyzer.analyze(file_path)
        if hash_res["is_threat"]:
            result.is_threat = True
            result.threat_name = hash_res["threat_name"]
            result.category = hash_res["category"]
            result.severity = hash_res["severity"]
            result.risk_score = 100.0
            result.detection_method = "Hash Signature Match"
            result.ai_explanation = f"Exact SHA-256 hash match against known malware signature '{result.threat_name}'."
            return result

        # Layer 2: YARA Signature Matching
        yara_matches = self.yara_engine.scan_file(file_path)
        if yara_matches:
            top_match = yara_matches[0]
            result.is_threat = True
            result.threat_name = top_match["rule"]
            result.category = top_match.get("category", CATEGORY_MALWARE)
            result.severity = top_match.get("severity", SEVERITY_HIGH)
            result.risk_score = 95.0
            result.detection_method = "YARA Signature Engine"
            result.ai_explanation = f"Triggered YARA rule '{top_match['rule']}': {top_match['description']}"
            return result

        # Layer 3: AI Threat Analysis (for executables or suspicious extensions)
        ext = path_obj.suffix.lower()
        if ext in EXECUTABLE_EXTENSIONS or path_obj.stat().st_size > 0:
            ai_res = self.ai_engine.analyze_file(file_path)
            result.risk_score = ai_res["risk_score"]
            result.signed = ai_res.get("pe_details", {}).get("is_signed", False)

            if ai_res["is_threat"]:
                result.is_threat = True
                result.threat_name = f"AI.Detection.{ai_res['classification']}"
                result.category = CATEGORY_TROJAN if ai_res["risk_score"] > 85 else CATEGORY_PUA
                result.severity = ai_res["severity"]
                result.detection_method = f"AI Detection Engine ({ai_res['model_engine']})"
                result.ai_explanation = "\n".join(ai_res["reasons"]) + f"\n\n{ai_res['ai_summary']}\n({ai_res['disclaimer']})"
                return result

        return result

    def scan_path_generator(self, target_paths, progress_callback=None):
        """
        Scans a list of files or directories, yielding (ScanResult, stats) for each inspected file.
        """
        self._cancel_requested = False
        self._is_scanning = True

        files_scanned = 0
        threats_found = 0
        start_time = time.time()

        for target in target_paths:
            p = Path(target)
            if not p.exists():
                continue

            if p.is_file():
                if self.is_cancelled():
                    break
                files_scanned += 1
                res = self.scan_single_file(str(p))
                if res.is_threat:
                    threats_found += 1
                    # Save threat in database
                    self.db.add_threat(
                        file_path=res.file_path,
                        file_hash=res.file_hash,
                        threat_name=res.threat_name,
                        category=res.category,
                        severity=res.severity,
                        risk_score=int(res.risk_score),
                        detection_method=res.detection_method,
                        ai_explanation=res.ai_explanation
                    )
                elapsed = max(time.time() - start_time, 0.001)
                speed = int(files_scanned / elapsed)
                if progress_callback:
                    progress_callback(str(p), files_scanned, threats_found, speed, res)
                yield res

            elif p.is_dir():
                for root, _, files in os.walk(p):
                    if self.is_cancelled():
                        break
                    for file in files:
                        if self.is_cancelled():
                            break
                        full_path = os.path.join(root, file)
                        files_scanned += 1

                        res = self.scan_single_file(full_path)
                        if res.is_threat:
                            threats_found += 1
                            self.db.add_threat(
                                file_path=res.file_path,
                                file_hash=res.file_hash,
                                threat_name=res.threat_name,
                                category=res.category,
                                severity=res.severity,
                                risk_score=int(res.risk_score),
                                detection_method=res.detection_method,
                                ai_explanation=res.ai_explanation
                            )
                        elapsed = max(time.time() - start_time, 0.001)
                        speed = int(files_scanned / elapsed)
                        if progress_callback:
                            progress_callback(full_path, files_scanned, threats_found, speed, res)
                        yield res

        self._is_scanning = False

    def get_quick_scan_targets(self) -> list:
        r"""
        Gathers critical execution paths:
        - User Downloads & Desktop
        - User Startup folder & Registry startup paths
        - User Temp folder
        - Treviora installation folder (D:\projects\antivirus)
        """
        targets = []
        user_home = Path.home()

        targets.append(str(Path("D:/projects/antivirus")))

        downloads = user_home / "Downloads"
        if downloads.exists():
            targets.append(str(downloads))

        desktop = user_home / "Desktop"
        if desktop.exists():
            targets.append(str(desktop))

        temp_dir = Path(os.environ.get("TEMP", "C:/Windows/Temp"))
        if temp_dir.exists():
            targets.append(str(temp_dir))

        # Startup persistence executables
        for entry in get_startup_persistence_entries():
            cmd = entry.get("command", "").strip('"').split(" ")[0]
            if cmd and Path(cmd).exists():
                targets.append(cmd)

        return list(dict.fromkeys(targets))

    def get_full_scan_targets(self) -> list:
        """
        Gathers full system targets, prioritizing D: drive and primary user profiles.
        """
        targets = ["D:\\"]
        if os.path.exists("C:\\Users"):
            targets.append("C:\\Users")
        return targets

    def get_download_scan_targets(self) -> list:
        user_home = Path.home()
        dl = user_home / "Downloads"
        return [str(dl)] if dl.exists() else []

    def get_usb_scan_targets(self) -> list:
        return get_removable_drives()
