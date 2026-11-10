# TREVIORA AI DEFENDER 2.1
### Professional AI-Powered Windows 11 Antivirus & Endpoint Cybersecurity System

**Developer:** TREVIORA INDUSTRY  
**Category:** AI-Powered Cybersecurity & Antivirus  
**Target Platform:** Windows 11  
**Primary Device Profile:** Lenovo LOQ (AMD Ryzen 5, NVIDIA GeForce RTX 3050 6GB, 24GB RAM)  
**Storage Architecture:** Dedicated `D:\` Drive Environment (`D:\projects\antivirus\`) — Strict Zero Footprint on C: Drive

---

## 1. Project Overview & Philosophy

**TREVIORA AI DEFENDER** is a Windows 11 antivirus and threat mitigation platform built by **TREVIORA INDUSTRY**. It combines traditional signature verification, cryptographic hash lookups, and YARA rule matching with an advanced **ONNX-based Machine Learning PE header classifier** and behavioral anomaly monitors.

### Safe Coexistence With Microsoft Defender
- **Non-Interfering Defense-in-Depth:** Treviora AI Defender never attempts to disable, replace, or tamper with Microsoft Defender Antivirus or Windows Defender Firewall.
- Operates smoothly alongside native Windows security features, providing an independent AI-driven second opinion and deep file/process telemetry.
- Follows Windows security best practices and operates with least-privilege principles.

---

## 2. Strict D: Drive Storage Policy

As requested by the user, **all necessary application files, databases, quarantine storage, AI models, logs, rules, and cache files reside strictly on the `D:\` drive**:
- **Application Directory:** `D:\projects\antivirus\`
- **Database (SQLite):** `D:\projects\antivirus\data\defender.db`
- **Quarantine Vault (AES-GCM Encrypted):** `D:\projects\antivirus\data\quarantine\`
- **Application Logs:** `D:\projects\antivirus\data\logs\defender.log`
- **AI Models (ONNX & Scikit-Learn):** `D:\projects\antivirus\data\models\`
- **YARA Threat Rules:** `D:\projects\antivirus\data\rules\`
- **Decoy Canary Honeypots:** `D:\projects\antivirus\data\canaries\`
- **Configuration:** `D:\projects\antivirus\data\config.json`

---

## 3. Core Architecture & Features

### A. Antivirus Scanner
- **Quick Scan:** Rapidly audits high-risk execution vectors (User Downloads, Desktop, Temp, Startup registry persistence keys, and Treviora directory).
- **Full System Scan:** Comprehensive inspection across `D:\` drive and user storage.
- **Custom Folder Scan:** User-directed file or folder inspection.
- **USB Drive Scan:** Targeted scanner for attached removable drives.
- **Download Folder Scan:** Dedicated scan of user Downloads.
- **File Hash Analysis:** Streams MD5, SHA-1, and SHA-256 checksums, cross-referencing against the local SQLite known threat signature database.
- **File Signature Verification:** Verifies Microsoft Authenticode digital certificates via native `wintrust.dll` / `WinVerifyTrust`.

### B. AI Malware Detection Engine
- **Modular Machine Learning Engine:** Utilizes an ONNX-runtime model trained on static PE (Portable Executable) feature vectors.
- **PE Feature Extractor:**
  - Shannon Entropy of overall file and individual sections (entropy > 7.2 signals packing or payload encryption).
  - Flags sections with both Write and Execute permissions ($W \oplus X$ violation).
  - Identifies known packer section signatures (UPX, Themida, ASPack, VMProtect).
  - Categorizes suspicious Windows API imports across:
    1. *Process Injection* (`VirtualAllocEx`, `WriteProcessMemory`, `CreateRemoteThread`)
    2. *Keylogging & Spyware* (`SetWindowsHookEx`, `GetAsyncKeyState`)
    3. *Anti-Debugging & Evasion* (`IsDebuggerPresent`, `NtQueryInformationProcess`)
    4. *Ransomware / Cryptography* (`CryptEncrypt`, `BCryptEncrypt`)
    5. *Execution & Persistence* (`ShellExecute`, `WinExec`)
- **Malware Risk Scoring:** Scores files from `0.0%` to `100.0%`, categorizing them as **Safe**, **Suspicious**, or **Malicious**.
- **Explainable AI (XAI):** Provides detailed bullet-point explanations of why a binary was flagged.
- *Notice: Never claims AI detection is 100% accurate; probabilistic indicators assist human decision-making.*

### C. Real-Time Background Protection
- **Filesystem Monitor:** Employs `watchdog` to monitor newly created and modified files across Downloads, Desktop, and Temp.
- **Process & Memory Monitor:** Continuous `psutil` background polling detecting suspicious command-line parameters (e.g., hidden/encoded PowerShell, living-off-the-land `certutil -urlcache` downloads, `mshta.exe` execution).
- **Startup Persistence Monitor:** Tracks additions to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` and `RunOnce`.

### D. Ransomware Protection & Canary Honeypots
- **Velocity Tracker:** Flags rapid bursts of file modifications (> 15 events in 4 seconds).
- **Extension Blocker:** Detects files renamed with known ransomware extensions (`.locked`, `.crypto`, `.wncry`, `.lockbit`, `.blackcat`).
- **Canary Decoy System:** Places canary honeypot files in `D:\projects\antivirus\data\canaries\`. Any modification or deletion of these decoy documents immediately raises a Critical Ransomware Outbreak alert.

### E. Quarantine Vault
- **Safe Isolation:** Quarantined files are encrypted in-memory using **AES-GCM (256-bit)** and stored with a `.tquar` extension in `D:\projects\antivirus\data\quarantine\`.
- Quarantined payloads are rendered inert and cannot be executed, indexed, or triggered.
- **Restoration & Permanent Shredding:** Supports decrypting back to the original location, or permanent zero-overwrite cryptographic shredding with user confirmation.

### F. AI Security Assistant
- **Built-in Cybersecurity Knowledge Base:** Offline encyclopedia explaining ransomware mechanisms, Trojan droppers, process hollowing, living-off-the-land binaries, and safe Defender coexistence.
- **Explain Threat Forensics:** Interactively breaks down detected threat risks and recommended remediation.
- **External AI Compatibility:** Optional support for local Ollama endpoints (`http://localhost:11434`) or OpenAI-compatible APIs configured in Settings.
- **Privacy Assurance:** Never transmits private files or telemetry to external AI without explicit consent.

### G. Network Security Monitoring
- Displays active TCP and UDP connections mapped to PID, process name, and remote endpoint.
- Flags suspicious remote ports (Metasploit 4444, IRC C2 6667, Stratum Monero mining 3333/5555/14444).
- Safe integration with Windows Firewall (audits profile states without unauthorized policy changes).
- Allows terminating suspicious networking processes with user confirmation.

### H. USB Storage Sentinel
- Automatically detects removable media insertion.
- Scans removable root volumes for legacy `autorun.inf` files, hidden executables, and malicious shortcut files (`.lnk`).

---

## 4. Dark Cyberpunk Dashboard UI

Built with **PySide6 (Qt for Python)** featuring a premium dark cybersecurity theme:
- Deep black and charcoal tones (`#0B0F19`, `#0F172A`, `#131B2E`) with glowing cyan and royal blue accents (`#00D2FF`, `#0070F3`).
- Circular animated Security Score widget (0-100%).
- 10 Dedicated Sidebar Pages:
  1. **Dashboard:** Protection Status, System Score, Quick Metrics, Recent Security Events, AI Insights.
  2. **Antivirus Scanner:** Quick, Full, Custom Folder, USB, and Downloads scan tabs with live progress, file ticker, and threat table.
  3. **Real-Time Protection:** Toggleable shields (Filesystem, Process, Ransomware, USB, AI), Live Telemetry, and safe EICAR test trigger.
  4. **Threat Detection:** Active incident response center with XAI forensic modal.
  5. **Quarantine Vault:** Encrypted items table, SHA-256 auditing, Restore and Shred actions.
  6. **AI Security Assistant:** Interactive cyber advisory chat with instant prompt suggestions.
  7. **Network Security:** Real-time socket inspector, suspicious port filter, and process termination.
  8. **USB Protection:** Removable volume scanner and auto-scan configuration.
  9. **Security Reports:** Forensic audit history with one-click export to CSV and JSON.
  10. **Settings:** Storage policy confirmation, Whitelist/Exclusion manager, AI API configuration, and hardware specs.

---

## 5. How to Run & Install

### Quick Run (From Source)
Double-click `run_treviora.bat` or run:
```bash
python D:\projects\antivirus\treviora_defender\main.py
```

### Install with Installer Wizard
Run the installer script to deploy shortcuts and setup:
```bash
python D:\projects\antivirus\installer.py
```
- Installs application to `D:\Program Files\TrevioraAIDefender`
- Creates Desktop shortcut
- Creates Start Menu shortcut
- Creates `uninstall.bat` uninstaller

### Compile Standalone Windows Executable
To build a binary using PyInstaller:
```bash
python D:\projects\antivirus\build_installer.py
```
The executable will be generated at:
`D:\projects\antivirus\dist\TrevioraAIDefender\TrevioraAIDefender.exe`

---

## 6. Verification & Testing

All modules have undergone comprehensive unit and integration testing:
- **Database:** SQLite schema, threat persistence, scan logging verified.
- **AI Model:** Random Forest trained and exported to ONNX format; ONNX Runtime inference verified.
- **PE Header Extractor:** Shannon entropy and API import categorization verified.
- **Quarantine:** AES-GCM encryption, isolation, and decryption restoration verified.
- **GUI:** All 10 pages and background monitoring services validated.

---
*© 2026 TREVIORA INDUSTRY. All Rights Reserved.*
