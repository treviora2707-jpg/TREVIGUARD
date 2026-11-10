/*
    TREVIORA AI DEFENDER - Built-in Threat YARA Rules
    Detects Ransomware, Trojans, WebShells, Credential Dumpers, and Suspicious Scripts.
    Location: D:\projects\antivirus\data\rules\default_rules.yar
*/

rule EICAR_Test_File {
    meta:
        description = "Standard EICAR Antivirus Test File"
        threat_level = "Critical"
        category = "EICAR"
    strings:
        $eicar = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    condition:
        $eicar
}

rule Generic_Ransomware_Note {
    meta:
        description = "Detects common ransomware payment notes and extortion patterns"
        threat_level = "Critical"
        category = "Ransomware"
    strings:
        $s1 = "Your personal files are encrypted" nocase
        $s2 = "All your files have been encrypted" nocase
        $s3 = "pay the ransom" nocase
        $s4 = "send bitcoin to" nocase
        $s5 = ".onion" nocase
        $s6 = "DECRYPT_FILES" nocase
        $s7 = "HOW_TO_RESTORE_FILES" nocase
        $s8 = "Your private key will be destroyed" nocase
    condition:
        2 of ($s1, $s2, $s3, $s4, $s5, $s6, $s7, $s8)
}

rule Suspicious_PowerShell_DownloadCradle {
    meta:
        description = "Detects hidden PowerShell download cradles commonly used by droppers"
        threat_level = "High"
        category = "Trojan"
    strings:
        $ps1 = "powershell" nocase
        $ps2 = "DownloadString(" nocase
        $ps3 = "Net.WebClient" nocase
        $ps4 = "IEX" nocase
        $ps5 = "-WindowStyle Hidden" nocase
        $ps6 = "-enc " nocase
        $ps7 = "-EncodedCommand" nocase
        $ps8 = "Bypass" nocase
    condition:
        ($ps1 and $ps2 and ($ps3 or $ps4)) or
        ($ps1 and ($ps5 or $ps8) and ($ps6 or $ps7))
}

rule Mimikatz_Credential_Dumper {
    meta:
        description = "Detects Mimikatz and LSASS credential dumping signatures"
        threat_level = "Critical"
        category = "Trojan"
    strings:
        $m1 = "sekurlsa::logonpasswords" nocase
        $m2 = "lsadump::sam" nocase
        $m3 = "privilege::debug" nocase
        $m4 = "kerberos::golden" nocase
        $m5 = "gentilkiwi" nocase
    condition:
        2 of ($m1, $m2, $m3, $m4, $m5)
}

rule Generic_Webshell_PHP {
    meta:
        description = "Detects obfuscated PHP WebShell backdoors"
        threat_level = "High"
        category = "Malware"
    strings:
        $w1 = "eval(base64_decode(" nocase
        $w2 = "eval(gzinflate(" nocase
        $w3 = "passthru($_POST" nocase
        $w4 = "shell_exec($_POST" nocase
        $w5 = "system($_REQUEST" nocase
    condition:
        any of ($w1, $w2, $w3, $w4, $w5)
}

rule Suspicious_Process_Hollowing {
    meta:
        description = "PE imports typical of process hollowing or remote injection"
        threat_level = "High"
        category = "Trojan"
    strings:
        $a1 = "VirtualAllocEx" ascii
        $a2 = "WriteProcessMemory" ascii
        $a3 = "CreateRemoteThread" ascii
        $a4 = "NtUnmapViewOfSection" ascii
        $a5 = "SetThreadContext" ascii
    condition:
        3 of ($a1, $a2, $a3, $a4, $a5)
}
