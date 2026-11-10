# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\projects\\antivirus\\treviora_defender\\main.py'],
    pathex=['d:/projects/antivirus'],
    binaries=[],
    datas=[('D:\\projects\\antivirus\\resources', 'resources'), ('D:\\projects\\antivirus\\data\\rules', 'data/rules'), ('D:\\projects\\antivirus\\data\\models', 'data/models')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='TrevioraAIDefender',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\projects\\antivirus\\resources\\icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TrevioraAIDefender',
)
