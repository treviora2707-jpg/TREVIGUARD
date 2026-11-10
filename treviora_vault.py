"""
TREVIORA INDUSTRY — ARMORED SOURCE VAULT ENGINE
Cipher: AES-256-GCM (Authenticated Encryption with Associated Data)
Developer: TREVIORA INDUSTRY
Motto: "ENGINEERING TOMORROW, EMPOWERING HUMANITY"

Protects firewall architecture, port filters, honeypot signatures, and AI models
against reverse-engineering and loophole discovery.
"""
import os
import sys
import json
import base64
import hashlib
import secrets
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE_DIR = Path(__file__).resolve().parent
KEY_FILE = BASE_DIR / "key.txt"
VAULT_FILE = BASE_DIR / "data" / "treviora_armored_vault.enc"
VAULT_MAGIC = b"TREVIORA_ARMORED_VAULT_V1"

# Directories and files to protect
PROTECTED_DIRS = [
    BASE_DIR / "treviora_defender"
]
PROTECTED_ROOT_SCRIPTS = [
    "test_all_features.py",
    "test_complete_system.py",
    "test_header_buttons.py",
    "test_idle_performance.py",
    "test_installer_wizard.py",
    "test_safeguard_toggle.py",
]


def get_or_create_master_key() -> bytes:
    """Reads the 256-bit key from key.txt or generates a new one."""
    if KEY_FILE.exists():
        content = KEY_FILE.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("DECRYPTION_KEY:"):
                key_hex = line.split(":", 1)[1].strip()
                return bytes.fromhex(key_hex)
            elif line.startswith("KEY:"):
                key_hex = line.split(":", 1)[1].strip()
                return bytes.fromhex(key_hex)

    # Generate fresh 256-bit key
    key_bytes = secrets.token_bytes(32)
    key_hex = key_bytes.hex()
    save_key_file(key_hex)
    return key_bytes


def save_key_file(key_hex: str):
    """Saves the master key to key.txt (excluded from git)."""
    text = f"""================================================================================
TREVIORA INDUSTRY — ARMORED SOURCE DECRYPTION MASTER KEY
================================================================================
WARNING: STRICTLY CONFIDENTIAL & PROPRIETARY.
DO NOT SHARE, COMMIT, OR UPLOAD TO GITHUB OR ANY PUBLIC REPOSITORY.
THIS MASTER KEY IS REQUIRED TO DECRYPT FIREWALL ARCHITECTURE, PORT FILTERS,
HONEYPOT SIGNATURES, AND CORE NEURAL CLASSIFIER SOURCE CODE.
================================================================================

DECRYPTION_KEY: {key_hex}
CIPHER: AES-256-GCM (Authenticated Encryption with Associated Data)
KEY_LENGTH: 256 bits (32 bytes)
CONTROLLER: TREVIORA INDUSTRY
OFFICIAL_EMAIL: treviora2707@gmail.com
GENERATED_AT: 2026-11-10T18:57:00+05:30
REPOSITORY: https://github.com/treviora2707-jpg/TREVIGUARD
STATUS: ARMORED_ACTIVE

HOW TO RESTORE SOURCE CODE:
Run the unlock utility in terminal:
  python unlock_vault.py

The utility will automatically detect this key.txt file and restore all
source code from the encrypted vault to plaintext.
================================================================================
"""
    KEY_FILE.write_text(text, encoding="utf-8")
    print(f"[OK] Master Security Key saved locally to: {KEY_FILE}")


def collect_source_files() -> list:
    """Collects all sensitive source files to be armored."""
    files = []
    for d in PROTECTED_DIRS:
        if d.exists():
            for p in d.rglob("*.py"):
                if "__pycache__" not in p.parts:
                    files.append(p)
    for script_name in PROTECTED_ROOT_SCRIPTS:
        p = BASE_DIR / script_name
        if p.exists():
            files.append(p)
    return files


def generate_armored_stub(rel_path: str, ciphertext_b64: str) -> str:
    """Generates the secure armored stub for public git display."""
    return f'''# -*- coding: utf-8 -*-
"""
==============================================================================
TREVIORA AI DEFENDER 2.1 — ARMORED SECURITY CONTAINER (AES-256 ENCRYPTED)
PROPRIETARY & CONFIDENTIAL — DEVELOPED BY TREVIORA INDUSTRY
"ENGINEERING TOMORROW, EMPOWERING HUMANITY"
==============================================================================
[ANTI-REVERSE ENGINEERING & FIREWALL INTEGRITY PROTECTION ACTIVE]
This source module contains proprietary firewall rules, kernel packet filters,
heuristic anomaly weights, honeypot canary signatures, and anti-evasion algorithms.
To protect endpoint deployments against exploit analysis and firewall breaches,
this file is protected with 256-bit AES-GCM military-grade encryption.

HOW TO INSTALL & OPERATE (NO PYTHON REQUIRED):
Run the official compiled setup wizard:
    Treviora_Setup.exe
This automatically configures SafeGuard 3-Layer Firewall, neural models,
and desktop shortcuts without exposing source code.

DEVELOPER DECRYPTION:
To decrypt this file back to plaintext Python source code, run:
    python unlock_vault.py
(Requires authorized 256-bit Master Key from TREVIORA INDUSTRY in key.txt).
==============================================================================
"""
import sys

__TREVIORA_ARMORED__ = True
__CIPHER__ = "AES-256-GCM"
__FILE_ID__ = "{rel_path}"
__PAYLOAD__ = "{ciphertext_b64}"

if __name__ == "__main__":
    print("[!] TREVIORA ARMORED FILE: Source code is encrypted to prevent firewall loopholes.")
    print("    Run 'Treviora_Setup.exe' to install and run the production application.")
    print("    Or run 'python unlock_vault.py' with your master key to edit source.")
    sys.exit(1)
'''


def lock_vault(key_bytes: bytes = None) -> bool:
    """
    Encrypts all proprietary source files and replaces them with armored stubs.
    Creates master encrypted archive in data/treviora_armored_vault.enc.
    """
    if key_bytes is None:
        key_bytes = get_or_create_master_key()

    aesgcm = AESGCM(key_bytes)
    files = collect_source_files()
    print(f"\n[VAULT] Armoring {len(files)} sensitive source files with AES-256-GCM...")

    vault_data = {}
    for file_path in files:
        rel_path = str(file_path.relative_to(BASE_DIR)).replace("\\", "/")
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        # If already armored, skip double-encryption
        if "__TREVIORA_ARMORED__ = True" in content:
            continue

        sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
        vault_data[rel_path] = {
            "content": content,
            "sha256": sha256
        }

    if not vault_data:
        print("[VAULT] All files are already armored or no plaintext files found.")
        return True

    # 1. Save master encrypted vault
    nonce = secrets.token_bytes(12)
    payload_json = json.dumps(vault_data).encode("utf-8")
    encrypted_blob = aesgcm.encrypt(nonce, payload_json, VAULT_MAGIC)

    VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VAULT_FILE, "wb") as f:
        f.write(VAULT_MAGIC)
        f.write(nonce)
        f.write(encrypted_blob)
    print(f"[OK] Master encrypted vault written: {VAULT_FILE} ({len(encrypted_blob)} bytes)")

    # 2. Replace individual files with armored stubs
    armored_count = 0
    for file_path in files:
        rel_path = str(file_path.relative_to(BASE_DIR)).replace("\\", "/")
        if rel_path in vault_data:
            content = vault_data[rel_path]["content"]
            file_nonce = secrets.token_bytes(12)
            file_cipher = aesgcm.encrypt(file_nonce, content.encode("utf-8"), rel_path.encode("utf-8"))
            combined = file_nonce + file_cipher
            b64_payload = base64.b64encode(combined).decode("ascii")

            stub_code = generate_armored_stub(rel_path, b64_payload)
            file_path.write_text(stub_code, encoding="utf-8")
            armored_count += 1

    print(f"[SUCCESS] {armored_count} files encrypted & armored for Git repository.")
    print("Firewall rules, port lists, and honeypots are now 100% hidden from public inspection.")
    return True


def unlock_vault(key_bytes: bytes = None) -> bool:
    """
    Decrypts the master encrypted vault and restores all original source files.
    """
    if key_bytes is None:
        key_bytes = get_or_create_master_key()

    if not VAULT_FILE.exists():
        print(f"[ERROR] Vault file not found: {VAULT_FILE}")
        return False

    with open(VAULT_FILE, "rb") as f:
        magic = f.read(len(VAULT_MAGIC))
        if magic != VAULT_MAGIC:
            print("[ERROR] Corrupted or invalid vault magic header.")
            return False
        nonce = f.read(12)
        encrypted_blob = f.read()

    try:
        aesgcm = AESGCM(key_bytes)
        decrypted_json = aesgcm.decrypt(nonce, encrypted_blob, VAULT_MAGIC)
        vault_data = json.loads(decrypted_json.decode("utf-8"))
    except Exception as e:
        print(f"[ERROR] Decryption failed! Invalid Master Key or corrupted vault. Details: {e}")
        return False

    print(f"\n[VAULT] Decrypting and restoring {len(vault_data)} files to plaintext...")
    restored_count = 0
    for rel_path, item in vault_data.items():
        target_path = BASE_DIR / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        content = item["content"]
        expected_sha = item.get("sha256")

        # Verify integrity
        calc_sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if expected_sha and calc_sha != expected_sha:
            print(f"[WARNING] Checksum mismatch for {rel_path}!")

        target_path.write_text(content, encoding="utf-8")
        restored_count += 1

    print(f"[SUCCESS] {restored_count} source files restored to original plaintext code!")
    print("Full developer editing mode is now active.")
    return True


if __name__ == "__main__":
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "help"
    if action == "lock":
        lock_vault()
    elif action == "unlock":
        unlock_vault()
    else:
        print("Treviora Security Vault CLI")
        print("Usage: python treviora_vault.py [lock|unlock]")
