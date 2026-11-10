"""
Verification of SafeGuard 3-Layer Firewall Toggle (Activate / Deactivate Lifecycle)
Tests both engine and UI synchronization.
"""
import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PySide6.QtWidgets import QApplication
from treviora_defender.ui.styles import MAIN_STYLE
from treviora_defender.ui.main_window import MainWindow
from treviora_defender.core.firewall_guard import SafeGuardFirewall
from treviora_defender.ui.cyber_shield_matrix import DesktopEnergyShieldOverlay


def test_toggle():
    print("=" * 60)
    print("VERIFYING SAFEGUARD 3-LAYER FIREWALL ACTIVATE / DEACTIVATE")
    print("=" * 60)

    # 1. Engine Test
    guard = SafeGuardFirewall()
    print(f"[1/4] Initial Engine State: Active={guard.is_active}")
    assert guard.is_active is True

    # Test Deactivate
    deact = guard.deactivate_shield()
    print(f"[2/4] After Deactivate: Active={guard.is_active} | Message={deact['message']}")
    assert guard.is_active is False
    assert guard.layers["layer1"]["status"] == "Standby / Inactive"

    # Test Toggle back to Active
    act = guard.toggle_shield()
    print(f"[3/4] After Toggle: Active={guard.is_active} | Message={act['message']}")
    assert guard.is_active is True
    assert guard.layers["layer1"]["status"] == "Active & Enforcing"

    # 2. UI Test with MainWindow
    print("\n[4/4] Testing GUI Synchronization in MainWindow...")
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)

    window = MainWindow()
    window.show()

    # Initial state
    assert window.btn_safeguard.is_active is True
    assert "ACTIVE" in window.btn_safeguard.text()
    print(" -> Initial Top Pill Button: ACTIVE (verified)")

    # Click 1: Deactivate
    window._open_safeguard_screen()
    assert window.view_safeguard.guard.is_active is False
    assert window.btn_safeguard.is_active is False
    assert "DEACTIVATED" in window.btn_safeguard.text()
    print(" -> Click 1 (Deactivate): Top Button is DEACTIVATED ○ (verified)")

    # Click 2: Reactivate
    window._open_safeguard_screen()
    assert window.view_safeguard.guard.is_active is True
    assert window.btn_safeguard.is_active is True
    assert "ACTIVE" in window.btn_safeguard.text()
    print(" -> Click 2 (Reactivate): Top Button is REACTIVATED ACTIVE ● (verified)")

    # Test Overlay Dialog toggle
    overlay = DesktopEnergyShieldOverlay(is_active=False)
    assert overlay.guard.is_active is False
    overlay._toggle_shield()
    assert overlay.guard.is_active is True
    assert "Deactivate" in overlay.btn_toggle.text()
    print(" -> Desktop Energy Shield Dialog Toggle: Successfully switched to ACTIVE (verified)")

    overlay._toggle_shield()
    assert overlay.guard.is_active is False
    assert "Activate" in overlay.btn_toggle.text()
    print(" -> Desktop Energy Shield Dialog Toggle: Successfully switched to STANDBY (verified)")

    window.stop_monitors()
    print("\n" + "=" * 60)
    print("ALL SAFEGUARD ACTIVATE / DEACTIVATE TESTS PASSED 100%!")
    print("=" * 60)


if __name__ == "__main__":
    test_toggle()
