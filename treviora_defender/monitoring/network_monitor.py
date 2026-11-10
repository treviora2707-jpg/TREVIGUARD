"""
TREVIORA AI DEFENDER - Network Security Monitor
Inspects active TCP/UDP network connections, flags suspicious remote ports/IPs,
and verifies Windows Defender Firewall status.
Strictly read-only safe integration: Never modifies firewall rules without explicit user confirmation.
"""
import psutil
import socket
from treviora_defender.database.db_manager import DatabaseManager
from treviora_defender.utils.win_utils import check_windows_defender_status
from treviora_defender.utils.logger import get_logger

logger = get_logger()

# Suspicious port catalog (known C2 channels, IRC bots, crypto miners, Metasploit handlers)
SUSPICIOUS_PORTS = {
    4444: "Metasploit default reverse shell port",
    1337: "Common Hacker/Backdoor port",
    6667: "IRC Command & Control channel",
    3333: "Stratum Monero/Crypto Mining port",
    5555: "Suspicious mining / Android ADB exposed port",
    7777: "Default backdoor / miner port",
    8333: "Bitcoin raw node / mining proxy",
    14444: "Crypto miner pool connection",
    31337: "Back Orifice Trojan port"
}


class NetworkMonitor:
    def __init__(self):
        self.db = DatabaseManager()

    @staticmethod
    def get_firewall_status() -> dict:
        return check_windows_defender_status()

    def get_active_connections(self, filter_suspicious_only: bool = False) -> list:
        """
        Retrieves real-time network connections mapped to processes.
        Falls back to parsing netstat -ano if psutil lacks elevated privileges.
        """
        connections = []
        raw_conns = []

        try:
            raw_conns = psutil.net_connections(kind='inet')
        except Exception:
            # Fallback to netstat -ano
            try:
                import subprocess
                out = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True,
                    timeout=3,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                for line in out.stdout.splitlines():
                    parts = line.split()
                    if len(parts) >= 4 and parts[0] in ["TCP", "UDP"]:
                        try:
                            proto = parts[0]
                            laddr = parts[1]
                            raddr = parts[2]
                            state = parts[3] if proto == "TCP" and len(parts) >= 5 else "ESTABLISHED"
                            pid = int(parts[-1])
                            
                            remote_port = None
                            if ":" in raddr:
                                try:
                                    remote_port = int(raddr.split(":")[-1])
                                except ValueError:
                                    pass

                            is_suspicious = False
                            flag_reason = "Normal"
                            if remote_port and remote_port in SUSPICIOUS_PORTS:
                                is_suspicious = True
                                flag_reason = f"Suspicious Remote Port ({remote_port}): {SUSPICIOUS_PORTS[remote_port]}"

                            if filter_suspicious_only and not is_suspicious:
                                continue

                            proc_name = "Unknown"
                            proc_exe = "N/A"
                            try:
                                p = psutil.Process(pid)
                                proc_name = p.name()
                                proc_exe = p.exe()
                            except Exception:
                                pass

                            connections.append({
                                "pid": pid,
                                "process_name": proc_name,
                                "exe": proc_exe,
                                "protocol": proto,
                                "local_address": laddr,
                                "remote_address": raddr,
                                "status": state,
                                "is_suspicious": is_suspicious,
                                "reason": flag_reason
                            })
                        except Exception:
                            continue
                return connections
            except Exception:
                return []

        # Cache process names
        proc_cache = {}

        for conn in raw_conns:
            pid = conn.pid
            if not pid:
                continue

            # Resolve process info
            if pid not in proc_cache:
                try:
                    p = psutil.Process(pid)
                    proc_cache[pid] = {
                        "name": p.name(),
                        "exe": p.exe()
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    proc_cache[pid] = {"name": "System/Protected", "exe": "N/A"}

            p_info = proc_cache[pid]

            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
            remote_port = conn.raddr.port if conn.raddr else None

            # Suspicious port check
            is_suspicious = False
            flag_reason = "Normal"

            if remote_port and remote_port in SUSPICIOUS_PORTS:
                is_suspicious = True
                flag_reason = f"Suspicious Remote Port ({remote_port}): {SUSPICIOUS_PORTS[remote_port]}"
                logger.warning(f"Suspicious connection found: PID {pid} ({p_info['name']}) -> {raddr} [{flag_reason}]")

            if filter_suspicious_only and not is_suspicious:
                continue

            connections.append({
                "pid": pid,
                "process_name": p_info["name"],
                "exe": p_info["exe"],
                "protocol": "TCP" if conn.type == socket.SOCK_STREAM else "UDP",
                "local_address": laddr,
                "remote_address": raddr,
                "status": conn.status if conn.status else "ESTABLISHED",
                "is_suspicious": is_suspicious,
                "reason": flag_reason
            })

        return connections
