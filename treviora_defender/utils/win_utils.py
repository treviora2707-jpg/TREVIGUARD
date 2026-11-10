"""
TREVIORA AI DEFENDER - Windows Security & API Utilities
Uses native Windows APIs (ctypes and winreg) to check Authenticode signatures,
query removable USB drives, inspect Windows Firewall, and check persistence.
Safe coexistence with Windows Defender without disabling any Windows security features.
"""
import ctypes
import os
import subprocess
import winreg
from pathlib import Path
from ctypes import wintypes
from treviora_defender.utils.logger import get_logger

logger = get_logger()

# Authenticode Trust Provider GUIDs
WINTRUST_ACTION_GENERIC_VERIFY_V2 = "{00AAC56B-CD44-11d0-8CC2-00C04FC295EE}"
WTD_CHOICE_FILE = 1
WTD_UI_NONE = 2
WTD_REVOKE_NONE = 0
WTD_REVOKE_WHOLECHAIN = 1
WTD_STATEACTION_IGNORE = 0


class WINTRUST_FILE_INFO(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pcwszFilePath", wintypes.LPCWSTR),
        ("hFile", wintypes.HANDLE),
        ("pgKnownSubject", ctypes.c_void_p),
    ]


class WINTRUST_DATA(ctypes.Structure):
    _fields_ = [
        ("cbStruct", wintypes.DWORD),
        ("pPolicyCallbackData", ctypes.c_void_p),
        ("pSIPClientData", ctypes.c_void_p),
        ("dwUIChoice", wintypes.DWORD),
        ("fdwRevocationChecks", wintypes.DWORD),
        ("dwUnionChoice", wintypes.DWORD),
        ("pFile", ctypes.POINTER(WINTRUST_FILE_INFO)),
        ("dwStateAction", wintypes.DWORD),
        ("hWVTStateData", wintypes.HANDLE),
        ("pwszURLReference", wintypes.LPCWSTR),
        ("dwProvFlags", wintypes.DWORD),
        ("dwUIContext", wintypes.DWORD),
        ("pSignatureSettings", ctypes.c_void_p),
    ]


class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]


def verify_authenticode_signature(file_path: str) -> dict:
    """
    Verifies the digital signature (Authenticode) of an executable using WinVerifyTrust.
    Returns:
        {
            "signed": bool,
            "status": "Valid" | "UntrustedRoot" | "NotSigned" | "BadDigest" | "Error",
            "code": int
        }
    """
    if not os.path.exists(file_path):
        return {"signed": False, "status": "FileNotFound", "code": -1}

    try:
        wintrust = ctypes.windll.wintrust
        wintrust_guid = GUID()
        ole32 = ctypes.windll.ole32
        ole32.CLSIDFromString(WINTRUST_ACTION_GENERIC_VERIFY_V2, ctypes.byref(wintrust_guid))

        file_info = WINTRUST_FILE_INFO()
        file_info.cbStruct = ctypes.sizeof(WINTRUST_FILE_INFO)
        file_info.pcwszFilePath = file_path
        file_info.hFile = None
        file_info.pgKnownSubject = None

        trust_data = WINTRUST_DATA()
        trust_data.cbStruct = ctypes.sizeof(WINTRUST_DATA)
        trust_data.pPolicyCallbackData = None
        trust_data.pSIPClientData = None
        trust_data.dwUIChoice = WTD_UI_NONE
        trust_data.fdwRevocationChecks = WTD_REVOKE_NONE
        trust_data.dwUnionChoice = WTD_CHOICE_FILE
        trust_data.pFile = ctypes.pointer(file_info)
        trust_data.dwStateAction = WTD_STATEACTION_IGNORE
        trust_data.hWVTStateData = None
        trust_data.pwszURLReference = None
        trust_data.dwProvFlags = 0x00000040  # WTD_CACHE_ONLY_URL_RETRIEVAL
        trust_data.dwUIContext = 0
        trust_data.pSignatureSettings = None

        res = wintrust.WinVerifyTrust(
            None,
            ctypes.byref(wintrust_guid),
            ctypes.byref(trust_data)
        )

        signed = (res == 0)
        status_map = {
            0: "Valid (Trusted)",
            -2146762487: "NotSigned (TRUST_E_NOSIGNATURE)",
            -2146762496: "InvalidProvider (TRUST_E_PROVIDER_UNKNOWN)",
            -2146762486: "UntrustedRoot (CERT_E_UNTRUSTEDROOT)",
            -2146869244: "BadDigest / Tampered (TRUST_E_BAD_DIGEST)",
            -2146762479: "ExplicitlyDistrusted (CERT_E_UNTRUSTEDTESTROOT)"
        }
        status_str = status_map.get(res, f"Untrusted (0x{res & 0xFFFFFFFF:08X})")
        return {"signed": signed, "status": status_str, "code": res}

    except Exception as e:
        logger.debug(f"Signature check exception for {file_path}: {e}")
        return {"signed": False, "status": "CheckError", "code": -1}


def get_removable_drives() -> list:
    """
    Returns list of removable (USB) drive paths currently connected (e.g. ['E:\\', 'F:\\'])
    """
    drives = []
    try:
        kernel32 = ctypes.windll.kernel32
        bitmask = kernel32.GetLogicalDrives()
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if bitmask & 1:
                drive_path = f"{letter}:\\"
                drive_type = kernel32.GetDriveTypeW(drive_path)
                # DRIVE_REMOVABLE = 2
                if drive_type == 2:
                    drives.append(drive_path)
            bitmask >>= 1
    except Exception as e:
        logger.error(f"Error enumerating removable drives: {e}")
    return drives


def check_windows_defender_status() -> dict:
    """
    Checks if Microsoft Defender Antivirus and Windows Firewall are active.
    Safe coexistence check - does NOT modify Defender.
    """
    status = {
        "defender_running": False,
        "firewall_active": False,
        "details": "Microsoft Defender Antivirus coexists safely."
    }

    try:
        # Check WinDefend service via sc query
        out = subprocess.run(
            ["sc", "query", "WinDefend"],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if "RUNNING" in out.stdout:
            status["defender_running"] = True
    except Exception:
        pass

    try:
        # Check Windows Firewall profile status
        out_fw = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles", "state"],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if "ON" in out_fw.stdout:
            status["firewall_active"] = True
    except Exception:
        pass

    return status


def get_startup_persistence_entries() -> list:
    """
    Scans registry Run / RunOnce keys for persistence mechanisms.
    """
    entries = []
    reg_locations = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU Run"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKCU RunOnce"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce", "HKLM RunOnce"),
    ]

    for hive, subkey, label in reg_locations:
        try:
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as key:
                num_values = winreg.QueryInfoKey(key)[1]
                for i in range(num_values):
                    try:
                        name, val, val_type = winreg.EnumValue(key, i)
                        entries.append({
                            "name": name,
                            "command": str(val),
                            "location": label,
                            "type": val_type
                        })
                    except OSError:
                        pass
        except OSError:
            pass

    return entries
