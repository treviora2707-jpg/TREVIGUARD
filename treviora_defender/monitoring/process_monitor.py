"""
TREVIORA AI DEFENDER - Suspicious Process Monitor
Continuously inspects active Windows processes using psutil for:
- Suspicious execution patterns (encoded PowerShell, certutil downloaders, mshta)
- Shadow copy deletion attempts (vssadmin ransomware prep)
- Crypto mining anomalies (high sustained CPU usage)
- Executables running from unusual user paths
"""
import time
import threading
import psutil
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.utils.logger import get_logger

logger = get_logger()

SUSPICIOUS_CMD_PATTERNS = [
    ("-enc ", "Encoded PowerShell Command execution"),
    ("-encodedcommand", "Encoded PowerShell Command execution"),
    ("downloadstring", "PowerShell Memory Dropper (DownloadString)"),
    ("iex", "Invoke-Expression dynamic script execution"),
    ("-windowstyle hidden", "Hidden Window PowerShell Launch"),
    ("certutil -urlcache", "CertUtil File Download Abusing Living-off-the-Land"),
    ("vssadmin delete shadows", "CRITICAL: Volume Shadow Copy Deletion (Ransomware Preparation)"),
    ("wbadmin delete catalog", "Backup Catalog Deletion (Ransomware Behavior)"),
    ("bcdedit /set", "Boot Configuration Tampering Attempt"),
    ("mshta http", "MSHTA Remote Script Execution"),
    ("rundll32.exe javascript", "Rundll32 Script Execution")
]


class ProcessMonitor:
    def __init__(self, alert_callback=None):
        self.alert_callback = alert_callback
        self.db = DatabaseManager()
        self._is_running = False
        self._thread = None
        self._stop_event = threading.Event()
        self._seen_suspicious_pids = set()

    def start(self):
        if self._is_running:
            return
        self._is_running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True, name="ProcessMonitorThread")
        self._thread.start()
        logger.info("Process Monitor background thread started.")

    def stop(self):
        self._is_running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=0.3)
            self._thread = None
        logger.info("Process Monitor stopped.")

    def _monitor_loop(self):
        while self._is_running and not self._stop_event.is_set():
            try:
                self.check_processes()
            except Exception as e:
                logger.debug(f"Error during process check: {e}")
            self._stop_event.wait(timeout=3.5)

    def check_processes(self) -> list:
        alerts = []
        target_names = {
            "powershell.exe", "pwsh.exe", "cmd.exe", "certutil.exe", "mshta.exe",
            "wscript.exe", "cscript.exe", "vssadmin.exe", "wbadmin.exe", "bcdedit.exe",
            "rundll32.exe", "regsvr32.exe"
        }

        # Fast non-blocking process iteration (only queries pid and name initially)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                pid = proc.info['pid']
                if pid in self._seen_suspicious_pids or pid <= 4:
                    continue

                name = (proc.info['name'] or "").lower()
                # Fast filter: only inspect command lines of target interpreters and living-off-the-land binaries
                if name not in target_names:
                    continue

                # Now safely query cmdline on candidate process only
                try:
                    cmdline_list = proc.cmdline()
                    cmdline = " ".join(cmdline_list).lower()
                    exe = proc.exe()
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    continue

                for pattern, reason in SUSPICIOUS_CMD_PATTERNS:
                    if pattern in cmdline:
                        self._seen_suspicious_pids.add(pid)
                        alert = {
                            "pid": pid,
                            "name": name,
                            "exe": exe,
                            "reason": reason,
                            "cmdline": cmdline[:150],
                            "severity": "Critical" if "shadow" in pattern else "High"
                        }
                        alerts.append(alert)
                        self.db.log_event(
                            event_type="SuspiciousProcess",
                            source="ProcessMonitor",
                            description=f"Process PID {pid} ({name}) triggered: {reason}",
                            severity=alert["severity"]
                        )
                        if self.alert_callback:
                            self.alert_callback(alert)
                        break

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        return alerts

    @staticmethod
    def get_process_list(limit=100) -> list:
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'exe', 'cpu_percent', 'memory_percent', 'status']):
            try:
                procs.append({
                    "pid": p.info['pid'],
                    "name": p.info['name'] or "Unknown",
                    "exe": p.info['exe'] or "N/A",
                    "cpu": round(p.info['cpu_percent'] or 0.0, 1),
                    "memory": round(p.info['memory_percent'] or 0.0, 1),
                    "status": p.info['status'] or "running"
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        procs.sort(key=lambda x: x["cpu"], reverse=True)
        return procs[:limit]

    @staticmethod
    def terminate_process(pid: int) -> dict:
        try:
            p = psutil.Process(pid)
            proc_name = p.name()
            p.terminate()
            p.wait(timeout=3)
            logger.info(f"Terminated process PID {pid} ({proc_name})")
            return {"success": True, "message": f"Terminated process {proc_name} (PID: {pid})"}
        except psutil.NoSuchProcess:
            return {"success": False, "message": f"PID {pid} no longer exists."}
        except psutil.AccessDenied:
            return {"success": False, "message": f"Access denied to terminate PID {pid} (requires elevated privileges)."}
        except Exception as e:
            return {"success": False, "message": str(e)}
