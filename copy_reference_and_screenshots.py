"""
Copies and organizes all user reference images and application screenshots into docs/
for Git repository display.
"""
import shutil
from pathlib import Path

BASE_DIR = Path("D:/projects/antivirus").resolve()
ARTIFACT_DIR = Path(r"C:\Users\Thiruvel\.gemini\antigravity\brain\a84d44c0-3f89-4e98-ae62-15a899da9949")
USER_UPLOADED = ARTIFACT_DIR / ".user_uploaded"

REF_TARGET = BASE_DIR / "docs" / "reference_images"
SHOTS_TARGET = BASE_DIR / "docs" / "screenshots"

REF_TARGET.mkdir(parents=True, exist_ok=True)
SHOTS_TARGET.mkdir(parents=True, exist_ok=True)

# 1. Map and copy user reference images
ref_map = {
    "media_1794294858477_ccea698a.jpg": "01_windows_desktop_reference.jpg",
    "media_1794297819333_8529d097.jpg": "02_energy_shield_honeycomb_grid.jpg",
    "media_1794291395881_261f34fb.jpg": "03_clean_master_dashboard_ref.jpg",
    "media_1794291475951_12b2a8c4.jpg": "04_clean_master_optimization_ref.jpg",
    "media_1794291757767_d416727b.jpg": "05_security_scan_shield_ref.jpg",
    "media_1794292155328_20590475.jpg": "06_treviora_official_branding.jpg",
    "media_1794303188407_15fcdd8b.jpg": "07_app_cyber_shield_logo.jpg",
    "media_1794299873739_a5fd4c1c.png": "08_header_controls_reference.png",
}

print("--- COPYING USER REFERENCE IMAGES ---")
for src_name, dst_name in ref_map.items():
    src_file = USER_UPLOADED / src_name
    if src_file.exists():
        dst_file = REF_TARGET / dst_name
        shutil.copy2(src_file, dst_file)
        print(f"Copied: {src_name} -> {dst_name}")

# 2. Map and copy UI screenshots
shot_map = {
    "imanager_dashboard.png": "01_dashboard.png",
    "imanager_desktop_energy_shield.png": "02_desktop_energy_shield.png",
    "imanager_security.png": "03_security_scan.png",
    "imanager_optimize.png": "04_optimization.png",
    "imanager_space.png": "05_space_cleanup.png",
    "imanager_performance.png": "06_hardware_performance.png",
    "imanager_battery.png": "07_battery_power.png",
    "imanager_safeguard.png": "08_safeguard_active.png",
    "imanager_safeguard_deactivated.png": "09_safeguard_standby.png",
    "imanager_virus_destroyer.png": "10_virus_destroyer.png",
    "imanager_notifications_dialog.png": "11_notifications_dialog.png",
    "imanager_user_profile_dialog.png": "12_user_profile_dialog.png",
}

print("\n--- COPYING UI SCREENSHOTS ---")
for src_name, dst_name in shot_map.items():
    src_file = ARTIFACT_DIR / src_name
    if src_file.exists():
        dst_file = SHOTS_TARGET / dst_name
        shutil.copy2(src_file, dst_file)
        print(f"Copied: {src_name} -> {dst_name}")

print("\nALL REFERENCE IMAGES AND SCREENSHOTS ORGANIZED SUCCESSFULLY!")
