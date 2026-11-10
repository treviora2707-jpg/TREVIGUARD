"""
TREVIORA AI DEFENDER - AI Cybersecurity Knowledge Base
Rich built-in cybersecurity encyclopedia providing offline threat explanations,
security recommendations, and malware behavior insights.
"""

KNOWLEDGE_ENTRIES = {
    "ransomware": {
        "title": "Ransomware Extortion Malware",
        "description": "Ransomware is malicious software that encrypts user documents, databases, and photos, demanding a cryptocurrency ransom payment for the decryption key.",
        "indicators": [
            "Mass modification of files with unusual extensions (.locked, .wncry, .crypto)",
            "Shadow volume deletion attempts using 'vssadmin delete shadows'",
            "Ransom notes dropped across desktop and user folders",
            "High disk write activity and CPU spikes"
        ],
        "recommendations": [
            "Immediately isolate the affected machine from the local network and Wi-Fi.",
            "Do not pay the ransom; recovery is not guaranteed.",
            "Use Treviora Quarantine to isolate the active encryptor binary.",
            "Restore critical data from secure offline or cloud backups."
        ]
    },
    "trojan": {
        "title": "Trojan Horse & Droppers",
        "description": "Trojans disguise themselves as legitimate software to gain unauthorized access, establish backdoors, or download secondary malware payloads.",
        "indicators": [
            "Suspicious parent-child processes (e.g. Word launching PowerShell or cmd.exe)",
            "Unsigned executables running out of %TEMP% or %APPDATA%",
            "New unverified registry Run keys or scheduled tasks for persistence"
        ],
        "recommendations": [
            "Quarantine the suspicious binary immediately.",
            "Check active network connections in the Treviora Network Security tab.",
            "Review startup applications and disable unverified entries."
        ]
    },
    "injection": {
        "title": "Process Injection & Memory Hollowing",
        "description": "Malware injects hostile shellcode or DLLs into legitimate Windows processes (like explorer.exe or svchost.exe) using VirtualAllocEx and WriteProcessMemory.",
        "indicators": [
            "Use of VirtualAllocEx, WriteProcessMemory, and CreateRemoteThread APIs",
            "PE sections with both Write and Execute permissions (W^X violation)",
            "Legitimate Windows processes opening unexpected outbound network connections"
        ],
        "recommendations": [
            "Terminate or isolate the injecting parent process.",
            "Run a Full System Scan in Treviora AI Defender."
        ]
    },
    "living_off_the_land": {
        "title": "Living-Off-The-Land Binaries (LOLBins)",
        "description": "Attackers exploit built-in trusted Windows utilities (e.g., certutil.exe, mshta.exe, powershell.exe) to evade signature detection.",
        "indicators": [
            "certutil.exe used with -urlcache to download remote payloads",
            "Encoded PowerShell strings executed with -EncodedCommand or -enc",
            "mshta.exe executing inline VBScript or remote HTA files"
        ],
        "recommendations": [
            "Restrict unrestricted PowerShell execution policy.",
            "Monitor command-line parameters in Treviora Process Monitor."
        ]
    },
    "eicar": {
        "title": "EICAR Standard Antivirus Test String",
        "description": "A harmless 68-character ASCII string designed by the European Institute for Computer Antivirus Research to safely test if antivirus scanning engines are operating correctly.",
        "indicators": [
            "Contains harmless text: 'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'"
        ],
        "recommendations": [
            "No action needed; this is a standard test file confirming Treviora Defender scanner is fully operational."
        ]
    },
    "defender_coexistence": {
        "title": "Microsoft Defender Coexistence",
        "description": "Treviora AI Defender is architected to safely operate alongside Microsoft Defender Antivirus without modifying Windows security policies or disabling system firewalls.",
        "indicators": [
            "Treviora operates in user-mode with least-privilege security safeguards",
            "Provides an independent AI-driven second opinion on file risk and behavioral anomalies"
        ],
        "recommendations": [
            "Keep Microsoft Defender active for primary OS protection.",
            "Use Treviora for real-time AI scoring, deep PE inspection, and quarantine isolation."
        ]
    }
}


def search_knowledge_base(query: str) -> dict:
    q = query.lower()
    for key, data in KNOWLEDGE_ENTRIES.items():
        if key in q or data["title"].lower() in q:
            return data

    if "eicar" in q or "test file" in q:
        return KNOWLEDGE_ENTRIES["eicar"]
    if "ransom" in q or "encrypt" in q or "bitcoin" in q or "locked" in q:
        return KNOWLEDGE_ENTRIES["ransomware"]
    if "trojan" in q or "dropper" in q or "backdoor" in q:
        return KNOWLEDGE_ENTRIES["trojan"]
    if "inject" in q or "memory" in q or "hollowing" in q:
        return KNOWLEDGE_ENTRIES["injection"]
    if "powershell" in q or "certutil" in q or "cmd" in q:
        return KNOWLEDGE_ENTRIES["living_off_the_land"]
    if "microsoft" in q or "windows defender" in q or "coexist" in q:
        return KNOWLEDGE_ENTRIES["defender_coexistence"]

    return None
