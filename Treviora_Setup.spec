# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\projects\\antivirus\\treviora_defender\\installer\\setup_wizard.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\projects\\antivirus\\data', 'data'), ('D:\\projects\\antivirus\\resources', 'resources')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtWidgets', 'PySide6.QtGui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Treviora_Setup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['D:\\projects\\antivirus\\resources\\icon.png'],
)
