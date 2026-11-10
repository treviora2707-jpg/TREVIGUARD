r"""
TREVIORA AI DEFENDER - YARA Rule Scanning Engine
Loads and compiles YARA rules stored on D: drive (D:\projects\antivirus\data\rules\).
"""
import os
from pathlib import Path
from treviora_defender.config.constants import RULES_DIR
from treviora_defender.utils.logger import get_logger

logger = get_logger()

try:
    import yara
    YARA_AVAILABLE = True
except ImportError:
    YARA_AVAILABLE = False
    logger.warning("yara-python not imported; falling back to internal heuristics")


class YaraEngine:
    def __init__(self):
        self.rules = None
        self.rules_loaded = False
        self.load_rules()

    def load_rules(self):
        if not YARA_AVAILABLE:
            return

        rule_files = {}
        if RULES_DIR.exists():
            for f in RULES_DIR.glob("*.yar"):
                rule_files[f.stem] = str(f)

        if not rule_files:
            logger.warning(f"No .yar rule files found in {RULES_DIR}")
            return

        try:
            self.rules = yara.compile(filepaths=rule_files)
            self.rules_loaded = True
            logger.info(f"Loaded {len(rule_files)} YARA rule file(s) successfully.")
        except Exception as e:
            logger.error(f"Error compiling YARA rules: {e}")
            self.rules = None
            self.rules_loaded = False

    def scan_file(self, file_path: str) -> list:
        """
        Scans a file with compiled YARA rules.
        Returns a list of match dicts:
        [{
            "rule": rule_name,
            "description": meta.get("description"),
            "category": meta.get("category", "Malware"),
            "severity": meta.get("threat_level", "High")
        }]
        """
        matches = []
        if not self.rules_loaded or not self.rules or not os.path.exists(file_path):
            return matches

        try:
            # Avoid scanning files larger than 100MB with YARA to maintain real-time speed
            if os.path.getsize(file_path) > 100 * 1024 * 1024:
                return matches

            raw_matches = self.rules.match(file_path, timeout=5)
            for m in raw_matches:
                matches.append({
                    "rule": m.rule,
                    "description": m.meta.get("description", "Matched YARA signature rule"),
                    "category": m.meta.get("category", "Malware"),
                    "severity": m.meta.get("threat_level", "High")
                })
        except Exception as e:
            logger.debug(f"YARA scan error for {file_path}: {e}")

        return matches
