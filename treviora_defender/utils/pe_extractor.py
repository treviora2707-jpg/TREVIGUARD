"""
TREVIORA AI DEFENDER - PE (Portable Executable) Feature Extractor
Extracts static PE metadata, section entropy, suspicious imports, and header anomalies
used by the AI Malware Detection Engine.
"""
import math
import os
from pathlib import Path
from treviora_defender.utils.logger import get_logger

logger = get_logger()

# Suspicious Windows APIs categorized by malware behavior
SUSPICIOUS_APIS = {
    "Process Injection": {
        "virtualalloc", "virtualallocex", "writeprocessmemory", "createremotethread",
        "ntunmapviewofsection", "queueuserapc", "setthreadcontext", "resumethread", "loadlibrarya", "loadlibraryw"
    },
    "Keylogging & Spyware": {
        "setwindowshookexa", "setwindowshookexw", "getasynckeystate", "getkeystate",
        "registerhotkey", "getforegroundwindow"
    },
    "Anti-Analysis & Evasion": {
        "isdebuggerpresent", "checkremotedebuggerpresent", "ntqueryinformationprocess",
        "outputdebugstringa", "timegettime", "queryperformancecounter"
    },
    "Ransomware / Cryptography": {
        "cryptencrypt", "cryptdecrypt", "cryptgenkey", "bcryptencrypt",
        "cryptacquirecontexta", "cryptacquirecontextw"
    },
    "Execution & Persistence": {
        "winexec", "shellexecutea", "shellexecutew", "createprocessa", "createprocessw",
        "regsetvalueexa", "regsetvaluew"
    },
    "Network / C2 Communication": {
        "urldownloadtofilea", "urldownloadtofilew", "internetopena", "httpsendrequesta",
        "wsastartup", "connect", "internetconnecta"
    }
}


def calculate_entropy(data: bytes) -> float:
    """
    Computes Shannon Entropy of a byte buffer (0.0 to 8.0).
    Values > 7.0 indicate high packing, compression, or encryption.
    """
    if not data:
        return 0.0

    entropy = 0.0
    length = len(data)
    byte_counts = [0] * 256
    for b in data:
        byte_counts[b] += 1

    for count in byte_counts:
        if count == 0:
            continue
        p = count / length
        entropy -= p * math.log2(p)

    return round(entropy, 4)


def calculate_file_entropy(file_path: str, max_bytes: int = 10 * 1024 * 1024) -> float:
    try:
        with open(file_path, "rb") as f:
            data = f.read(max_bytes)
        return calculate_entropy(data)
    except Exception:
        return 0.0


def extract_pe_features(file_path: str) -> dict:
    """
    Analyzes an executable file and returns structured features for the AI Engine.
    """
    features = {
        "is_pe": False,
        "file_size": 0,
        "overall_entropy": 0.0,
        "num_sections": 0,
        "max_section_entropy": 0.0,
        "has_high_entropy_section": False,
        "has_packed_section_names": False,
        "has_wx_sections": False,  # Writable and Executable (shellcode indicator)
        "sections": [],
        "suspicious_apis_found": {},
        "total_suspicious_apis": 0,
        "imported_dlls": [],
        "anomaly_indicators": []
    }

    if not os.path.exists(file_path):
        return features

    file_size = os.path.getsize(file_path)
    features["file_size"] = file_size
    features["overall_entropy"] = calculate_file_entropy(file_path)

    # Try using pefile if available
    try:
        import pefile
        pe = pefile.PE(file_path, fast_load=False)
        features["is_pe"] = True
        features["num_sections"] = len(pe.sections)

        known_packer_names = {"upx0", "upx1", "upx2", ".vmp0", ".vmp1", ".aspack", ".themida", ".packer", "pec2"}

        max_ent = 0.0
        for section in pe.sections:
            try:
                sec_name = section.Name.decode("utf-8", errors="ignore").strip("\x00").lower()
            except Exception:
                sec_name = "unknown"

            sec_data = section.get_data()
            sec_ent = calculate_entropy(sec_data) if sec_data else 0.0
            if sec_ent > max_ent:
                max_ent = sec_ent

            # Check for W+X permissions (0x20000000 = EXECUTE, 0x80000000 = WRITE)
            chars = section.Characteristics
            is_wx = bool((chars & 0x20000000) and (chars & 0x80000000))
            if is_wx:
                features["has_wx_sections"] = True
                features["anomaly_indicators"].append(f"Section {sec_name} has both Write and Execute permissions (W^X violation)")

            if sec_name in known_packer_names:
                features["has_packed_section_names"] = True
                features["anomaly_indicators"].append(f"Packer signature section detected: '{sec_name}'")

            features["sections"].append({
                "name": sec_name,
                "virtual_size": section.Misc_VirtualSize,
                "raw_size": section.SizeOfRawData,
                "entropy": sec_ent,
                "is_wx": is_wx
            })

        features["max_section_entropy"] = round(max_ent, 4)
        if max_ent >= 7.2:
            features["has_high_entropy_section"] = True
            features["anomaly_indicators"].append(f"High section entropy detected ({max_ent}/8.0), likely packed/encrypted")

        # Parse Imports
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                try:
                    dll_name = entry.dll.decode("utf-8", errors="ignore").lower()
                    features["imported_dlls"].append(dll_name)
                    for imp in entry.imports:
                        if imp.name:
                            func_name = imp.name.decode("utf-8", errors="ignore").lower()
                            for cat, api_set in SUSPICIOUS_APIS.items():
                                if func_name in api_set:
                                    if cat not in features["suspicious_apis_found"]:
                                        features["suspicious_apis_found"][cat] = []
                                    features["suspicious_apis_found"][cat].append(func_name)
                                    features["total_suspicious_apis"] += 1
                except Exception:
                    pass

        pe.close()

    except Exception as e:
        # Not a valid PE or pefile error
        logger.debug(f"Non-PE or parse error for {file_path}: {e}")

    return features
