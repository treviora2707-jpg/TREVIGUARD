"""
TREVIORA INDUSTRY — UNLOCK ARMORED VAULT
Run this script to restore all source code from the AES-256 encrypted vault.
Requires: key.txt (local file) OR manual key entry.
"""
import sys
from pathlib import Path
from treviora_vault import unlock_vault, KEY_FILE

def main():
    print("======================================================================")
    print("        TREVIORA AI DEFENDER — ARMORED SOURCE DECRYPTOR")
    print("                 DEVELOPER: TREVIORA INDUSTRY")
    print("            'ENGINEERING TOMORROW, EMPOWERING HUMANITY'")
    print("======================================================================")

    key_bytes = None
    if KEY_FILE.exists():
        print(f"[+] Found local decryption key in: {KEY_FILE.name}")
        content = KEY_FILE.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("DECRYPTION_KEY:"):
                key_bytes = bytes.fromhex(line.split(":", 1)[1].strip())
                break
    
    if key_bytes is None:
        print("[!] Local key.txt not found.")
        user_input = input("Enter 256-bit Treviora Master Security Key (hex): ").strip()
        try:
            key_bytes = bytes.fromhex(user_input)
            if len(key_bytes) != 32:
                print("[ERROR] Key must be exactly 32 bytes (64 hex characters)!")
                sys.exit(1)
        except ValueError:
            print("[ERROR] Invalid hex string format!")
            sys.exit(1)

    success = unlock_vault(key_bytes)
    if success:
        print("======================================================================")
        print(" [✓] VAULT UNLOCKED: All source code files restored to plaintext.")
        print("======================================================================")
    else:
        print("======================================================================")
        print(" [✕] UNLOCK FAILED: Incorrect key or corrupted vault.")
        print("======================================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
