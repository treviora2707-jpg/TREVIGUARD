"""
TREVIORA AI DEFENDER - Dynamic Universal Hardware Detection & Tuning Engine
Supports any Windows PC:
- Automatic Intel Core (i3, i5, i7, i9, Ultra) vs AMD Ryzen (3, 5, 7, 9) vs Generic detection
- GPU Detection: NVIDIA GeForce, AMD Radeon, Intel Arc, Intel Iris Xe / UHD
- Dynamic RAM Sizing (8GB, 16GB, 24GB, 32GB, 64GB+)
- Machine Form Factor: Laptop (Battery Sensor) vs Desktop Workstation (Direct AC Line)
- Auto-Adaptive Performance Optimization Tuning
"""
import os
import re
import platform
import psutil
from pathlib import Path
from treviora_defender.utils.logger import get_logger

logger = get_logger()

# Optional winreg on Windows
try:
    import winreg
except ImportError:
    winreg = None


class HardwareProfile:
    _cached_profile = None

    @classmethod
    def get_profile(cls, force_refresh: bool = False) -> dict:
        """
        Returns full hardware discovery profile with zero lag and instant caching.
        """
        if cls._cached_profile and not force_refresh:
            return cls._cached_profile

        # 1. CPU Detection
        cpu_raw = cls._detect_cpu_raw_name()
        cpu_vendor, cpu_brand, cpu_family, cpu_short = cls._parse_cpu_branding(cpu_raw)

        # 2. GPU Detection
        gpus = cls._detect_gpus()
        primary_gpu = gpus[0] if gpus else {"name": "Standard Display Adapter", "is_dedicated": False}
        gpu_short = cls._parse_gpu_short_name(primary_gpu.get("name", ""))

        # 3. RAM Sizing
        mem = psutil.virtual_memory()
        ram_total_gb = round(mem.total / (1024**3), 1)

        # 4. Form Factor (Laptop vs Desktop)
        battery = psutil.sensors_battery()
        is_laptop = battery is not None
        device_type = "Laptop" if is_laptop else "Desktop Workstation"

        # 5. OS & Architecture
        os_info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "hostname": platform.node(),
            "user": os.getlogin() if hasattr(os, "getlogin") else os.environ.get("USERNAME", "Administrator")
        }

        # 6. Adaptive Optimization Tuning
        tuning = cls._compute_tuning_profile(cpu_vendor, cpu_family, ram_total_gb, primary_gpu.get("is_dedicated", False))

        profile = {
            "cpu": {
                "raw_name": cpu_raw,
                "vendor": cpu_vendor,          # "Intel", "AMD", or "Generic"
                "brand": cpu_brand,            # "INTEL", "AMD", or "NEURAL"
                "family": cpu_family,          # "Core i7", "Ryzen 5", etc.
                "short_name": cpu_short,       # "Intel Core i7", "AMD Ryzen 5"
                "cores_logical": psutil.cpu_count(logical=True) or 4,
                "cores_physical": psutil.cpu_count(logical=False) or 2,
            },
            "gpu": {
                "name": primary_gpu.get("name", "Standard Graphics"),
                "short_name": gpu_short,
                "is_dedicated": primary_gpu.get("is_dedicated", False),
                "all_gpus": gpus
            },
            "ram": {
                "total_gb": ram_total_gb,
                "formatted": f"{ram_total_gb:.1f} GB"
            },
            "form_factor": {
                "type": device_type,
                "is_laptop": is_laptop
            },
            "os": os_info,
            "tuning": tuning,
            "display_spec": f"{cpu_short} & {gpu_short}"
        }

        cls._cached_profile = profile
        logger.info(f"Hardware Profile Discovered: {profile['display_spec']} | {ram_total_gb}GB RAM | {device_type}")
        return profile

    @staticmethod
    def _detect_cpu_raw_name() -> str:
        name = ""
        # Method 1: Windows Registry (exact CPU model name string)
        if winreg:
            try:
                key_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as k:
                    val, _ = winreg.QueryValueEx(k, "ProcessorNameString")
                    name = str(val).strip()
            except Exception:
                pass

        # Method 2: Platform & Environment Fallbacks
        if not name:
            name = platform.processor() or os.environ.get("PROCESSOR_IDENTIFIER", "x86_64 Processor")

        return name

    @staticmethod
    def _parse_cpu_branding(raw_name: str):
        raw_lower = raw_name.lower()
        if "intel" in raw_lower:
            vendor = "Intel"
            brand = "INTEL"
            if "core" in raw_lower:
                m = re.search(r"i[3579]|ultra\s*\d+", raw_lower)
                family = f"Core {m.group(0).capitalize()}" if m else "Core"
            elif "xeon" in raw_lower:
                family = "Xeon"
            elif "celeron" in raw_lower:
                family = "Celeron"
            else:
                family = "Processor"
            short_name = f"Intel {family}"
        elif "amd" in raw_lower or "ryzen" in raw_lower:
            vendor = "AMD"
            brand = "AMD"
            if "ryzen" in raw_lower:
                m = re.search(r"ryzen\s*([3579]|threadripper)", raw_lower)
                family = f"Ryzen {m.group(1).capitalize()}" if m else "Ryzen"
            else:
                family = "APU/CPU"
            short_name = f"AMD {family}"
        else:
            vendor = "Generic"
            brand = "NEURAL"
            family = "Quantum NPU"
            short_name = "Neural NPU"

        return vendor, brand, family, short_name

    @staticmethod
    def _detect_gpus() -> list:
        gpus = []
        # Method 1: Query Windows Display Adapter Registry
        if winreg:
            try:
                base_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base_path) as k:
                    idx = 0
                    while True:
                        try:
                            sub_name = winreg.EnumKey(k, idx)
                            idx += 1
                            if sub_name.isdigit():
                                with winreg.OpenKey(k, sub_name) as sub_k:
                                    try:
                                        desc, _ = winreg.QueryValueEx(sub_k, "DriverDesc")
                                        d_str = str(desc).strip()
                                        if d_str and d_str not in [g["name"] for g in gpus]:
                                            is_ded = any(w in d_str.lower() for w in ["nvidia", "geforce", "rtx", "gtx", "radeon rx", "arc"])
                                            gpus.append({"name": d_str, "is_dedicated": is_ded})
                                    except Exception:
                                        pass
                        except OSError:
                            break
            except Exception:
                pass

        # Sort so dedicated GPU comes first
        gpus.sort(key=lambda g: 0 if g.get("is_dedicated") else 1)

        if not gpus:
            gpus.append({"name": "Standard Graphics Controller", "is_dedicated": False})

        return gpus

    @staticmethod
    def _parse_gpu_short_name(full_name: str) -> str:
        fn_lower = full_name.lower()
        if "rtx" in fn_lower:
            m = re.search(r"rtx\s*\d{4}(\s*ti)?", fn_lower)
            if m:
                return m.group(0).upper()
            return "NVIDIA RTX"
        elif "gtx" in fn_lower:
            m = re.search(r"gtx\s*\d{3,4}(\s*ti)?", fn_lower)
            if m:
                return m.group(0).upper()
            return "NVIDIA GTX"
        elif "radeon" in fn_lower:
            m = re.search(r"rx\s*\d{4}", fn_lower)
            if m:
                return f"Radeon {m.group(0).upper()}"
            return "AMD Radeon"
        elif "iris" in fn_lower:
            return "Intel Iris Xe"
        elif "arc" in fn_lower:
            return "Intel Arc"
        elif "uhd" in fn_lower:
            return "Intel UHD"
        elif "geforce" in fn_lower:
            return "GeForce GPU"
        return "Dedicated GPU" if "nvidia" in fn_lower or "amd" in fn_lower else "Integrated GPU"

    @staticmethod
    def _compute_tuning_profile(vendor: str, family: str, ram_gb: float, has_dedicated_gpu: bool) -> dict:
        """
        Dynamically configures app optimization based on machine capacity:
        - High Performance Profile for Gaming/Creator PCs (Ryzen 5/7/9, Intel i5/i7/i9, >=16GB RAM)
        - Balanced Profile for standard PCs
        - Eco/Lightweight Profile for low-power devices (<8GB RAM)
        """
        if ram_gb >= 16 or has_dedicated_gpu:
            return {
                "profile_name": "High-Performance Workstation Mode",
                "max_worker_threads": 4,
                "ai_batch_size": 32,
                "ui_animation_fps": 30,
                "memory_cache_mb": 512,
                "deep_heuristics": True,
                "description": f"Optimized for high-speed multi-threading on {vendor} {family} & Dedicated GPU."
            }
        elif ram_gb >= 8:
            return {
                "profile_name": "Balanced Performance Mode",
                "max_worker_threads": 2,
                "ai_batch_size": 16,
                "ui_animation_fps": 25,
                "memory_cache_mb": 256,
                "deep_heuristics": True,
                "description": f"Balanced real-time protection tuned for {vendor} architecture."
            }
        else:
            return {
                "profile_name": "Eco / Low-Power Mode",
                "max_worker_threads": 1,
                "ai_batch_size": 8,
                "ui_animation_fps": 15,
                "memory_cache_mb": 128,
                "deep_heuristics": False,
                "description": "Ultra-lightweight low-memory footprint mode to preserve system resources."
            }
