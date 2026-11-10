"""
TREVIORA AI DEFENDER - Hash Analyzer & Known Threat Matcher
Calculates MD5, SHA1, SHA256 checksums and matches against known threat signatures.
All signatures and hash lookups occur on D: drive SQLite database.
"""
import hashlib
import os
from pathlib import Path
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.config.constants import (
    SEVERITY_CRITICAL, SEVERITY_HIGH, CATEGORY_MALWARE,
    CATEGORY_RANSOMWARE, CATEGORY_TROJAN, CATEGORY_EICAR
)
from treviora_defender.utils.logger import get_logger

logger = get_logger()

# Standard Known Threat Signatures (including EICAR and prominent real-world malware hashes)
BUILTIN_KNOWN_THREATS = [
    {
        "sha256": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
        "name": "EICAR-Standard-AV-Test-File",
        "category": CATEGORY_EICAR,
        "severity": SEVERITY_CRITICAL
    },
    {
        "sha256": "44d88612fea8a8f36de82e1278abb02f",  # EICAR MD5
        "name": "EICAR-Standard-AV-Test-File.MD5",
        "category": CATEGORY_EICAR,
        "severity": SEVERITY_CRITICAL
    },
    {
        "sha256": "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa",
        "name": "Ransomware.WannaCry.MSRef",
        "category": CATEGORY_RANSOMWARE,
        "severity": SEVERITY_CRITICAL
    },
    {
        "sha256": "d60f5454641e76b5d92cfd3a43653112c2a7df58d689fb8c56fa769ebc8b090a",
        "name": "Trojan.Emotet.Gen",
        "category": CATEGORY_TROJAN,
        "severity": SEVERITY_CRITICAL
    },
    {
        "sha256": "70979f280fd2887221918a804d38374eab917ad0468b0743a846aa0b400793e0",
        "name": "Ransomware.LockBit.3",
        "category": CATEGORY_RANSOMWARE,
        "severity": SEVERITY_CRITICAL
    },
    {
        "sha256": "2bc815b3e2da382daefee279d45e0fbba212ce78ee895bb1203612f0e0dfb9ef",
        "name": "Trojan.Mimikatz.CredentialStealer",
        "category": CATEGORY_TROJAN,
        "severity": SEVERITY_HIGH
    },
    {
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "name": "Empty-Zero-Byte-File",
        "category": "ZeroByte",
        "severity": "Clean"
    }
]


class HashAnalyzer:
    def __init__(self):
        self.db = DatabaseManager()
        self.db.populate_seed_threat_hashes(BUILTIN_KNOWN_THREATS)
        # In-memory O(1) hash cache to completely eliminate disk I/O lag during scans
        self._cache = {t["sha256"].lower(): t for t in BUILTIN_KNOWN_THREATS}
        # Pre-seed common MD5 as well
        self._cache_md5 = {t.get("md5", ""): t for t in BUILTIN_KNOWN_THREATS if "md5" in t}

    @staticmethod
    def compute_hashes(file_path: str, chunk_size: int = 65536) -> dict:
        """
        Streams file to compute MD5, SHA1, and SHA256 hashes safely without loading full file into memory.
        """
        if not os.path.exists(file_path):
            return {"md5": "", "sha1": "", "sha256": ""}

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()

        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    md5.update(chunk)
                    sha1.update(chunk)
                    sha256.update(chunk)
            return {
                "md5": md5.hexdigest(),
                "sha1": sha1.hexdigest(),
                "sha256": sha256.hexdigest()
            }
        except Exception as e:
            logger.debug(f"Error computing hashes for {file_path}: {e}")
            return {"md5": "", "sha1": "", "sha256": ""}

    def analyze(self, file_path: str) -> dict:
        """
        Calculates hashes and checks against known malware databases.
        """
        hashes = self.compute_hashes(file_path)
        sha256_val = hashes.get("sha256", "")

        result = {
            "is_threat": False,
            "threat_name": None,
            "category": None,
            "severity": None,
            "hashes": hashes
        }

        if not sha256_val:
            return result

        # Fast O(1) in-memory cache check first (zero disk lag)
        match = self._cache.get(sha256_val.lower())
        if not match:
            # Check SQLite known threat table and cache result
            match = self.db.check_known_hash(sha256_val)
            if match:
                self._cache[sha256_val.lower()] = match

        if match and match.get("severity") != "Clean":
            result["is_threat"] = True
            threat_name = match.get("threat_name") or match.get("name", "Unknown Threat")
            result["threat_name"] = threat_name
            result["category"] = match.get("category", "Malware")
            result["severity"] = match.get("severity", "High")
            logger.info(f"Hash Match Detected: {threat_name} in {file_path}")

        return result
