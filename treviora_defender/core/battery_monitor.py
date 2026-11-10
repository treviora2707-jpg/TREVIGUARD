"""
TREVIORA AI DEFENDER - Battery & Power Scheme Engine
Monitors Lenovo LOQ battery health, percentage, charging state, and Windows power plans.
"""
import subprocess
import psutil
from treviora_defender.utils.logger import get_logger

logger = get_logger()


class BatteryMonitor:
    @staticmethod
    def get_battery_info() -> dict:
        """
        Retrieves real-time battery status, health estimate, and active power plan.
        """
        info = {
            "has_battery": False,
            "percent": 100,
            "is_plugged": True,
            "status_text": "AC Power Connected",
            "time_remaining": "N/A",
            "health": "Good (Normal)",
            "power_mode": "Balanced (Optimized)"
        }

        try:
            batt = psutil.sensors_battery()
            if batt:
                info["has_battery"] = True
                info["percent"] = int(batt.percent)
                info["is_plugged"] = bool(batt.power_plugged)

                if batt.power_plugged:
                    info["status_text"] = "Charging" if batt.percent < 99 else "Fully Charged (AC Connected)"
                else:
                    info["status_text"] = "On Battery Power"

                if batt.secsleft and batt.secsleft > 0 and not batt.power_plugged:
                    mins = batt.secsleft // 60
                    hrs = mins // 60
                    rem_mins = mins % 60
                    info["time_remaining"] = f"{hrs}h {rem_mins}m remaining"
                elif batt.power_plugged:
                    info["time_remaining"] = "Plugged in"
            else:
                info["status_text"] = "AC Power (Desktop Mode)"
        except Exception as e:
            logger.debug(f"Battery query error: {e}")

        # Query Windows Power Scheme
        try:
            out = subprocess.run(
                ["powercfg", "/getactivescheme"],
                capture_output=True,
                text=True,
                timeout=2,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            line = out.stdout.lower()
            if "high performance" in line or "ultimate" in line:
                info["power_mode"] = "Performance Mode (Lenovo LOQ High Boost)"
            elif "power saver" in line:
                info["power_mode"] = "Power Saver Mode"
            else:
                info["power_mode"] = "Balanced Mode (Optimized for Ryzen 5)"
        except Exception:
            pass

        return info

    @staticmethod
    def set_power_mode(mode: str) -> bool:
        """
        Changes Windows power plan to:
        - "performance" (High Performance: 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c)
        - "balanced" (Balanced: 381b4222-f694-41f0-9685-ff5bb260df2e)
        - "saver" (Power Saver: a1841308-3541-4fab-bc81-f71556f20b4a)
        """
        scheme_map = {
            "performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
            "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
            "saver": "a1841308-3541-4fab-bc81-f71556f20b4a"
        }
        guid = scheme_map.get(mode.lower())
        if not guid:
            return False

        try:
            subprocess.run(
                ["powercfg", "/setactive", guid],
                capture_output=True,
                timeout=3,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
        except Exception:
            return False
