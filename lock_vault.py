"""
TREVIORA INDUSTRY — LOCK ARMORED VAULT
Run this script before committing to Git to encrypt all proprietary source files.
Encrypts firewall definitions, port filters, honeypot signatures, and models.
"""
import sys
from pathlib import Path
from treviora_vault import lock_vault, KEY_FILE, get_or_create_master_key

def main():
    print("======================================================================")
    print("         TREVIORA AI DEFENDER — ARMORED SOURCE ENCRYPTOR")
    print("                 DEVELOPER: TREVIORA INDUSTRY")
    print("            'ENGINEERING TOMORROW, EMPOWERING HUMANITY'")
    print("======================================================================")

    key_bytes = get_or_create_master_key()
    success = lock_vault(key_bytes)
    if success:
        print("======================================================================")
        print(" [✓] VAULT LOCKED: All source files encrypted with AES-256-GCM.")
        print("     Safe to commit & push to GitHub (key.txt remains strictly local).")
        print("======================================================================")
    else:
        print("======================================================================")
        print(" [✕] LOCK FAILED: An error occurred while armoring files.")
        print("======================================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
