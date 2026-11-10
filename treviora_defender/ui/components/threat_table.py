# -*- coding: utf-8 -*-
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
__FILE_ID__ = "treviora_defender/ui/components/threat_table.py"
__PAYLOAD__ = "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"

if __name__ == "__main__":
    print("[!] TREVIORA ARMORED FILE: Source code is encrypted to prevent firewall loopholes.")
    print("    Run 'Treviora_Setup.exe' to install and run the production application.")
    print("    Or run 'python unlock_vault.py' with your master key to edit source.")
    sys.exit(1)
