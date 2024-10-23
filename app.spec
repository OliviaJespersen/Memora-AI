# -*- mode: python ; coding: utf-8 -*-
# vi: ft=python


import sys
from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.osx import BUNDLE


name = 'Memora AI' if sys.platform == 'win32' else 'memora_ai'
icon = None
if sys.platform == 'win32':
    icon = 'resources/boykisser.ico'
elif sys.platform == 'darwin':
    icon = 'resources/boykisser.icns'


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("resources", "resources"),
        ("config.json", ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    excludes=[],
    runtime_hooks=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    bootloader_ignore_signals=False,
    console=False,
    hide_console='hide-early',
    disable_windowed_traceback=False,
    debug=False,
    name=name,
    exclude_binaries=True,
    icon=icon,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name=name,
    strip=False,
    upx=True,
    upx_exclude=[],
)


app = BUNDLE(
    exe if coll is None else coll,
    name='MemoraAI.app',
    icon=icon,
    bundle_identifier='com.github.OliviaJespersen',
    version='0.0.0',
    info_plist={
        'NSAppleScriptEnabled': False,
        'NSPrincipalClass': 'NSApplication',
    }
)
