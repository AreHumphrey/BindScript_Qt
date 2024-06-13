# -*- mode: python ; coding: utf-8 -*-

import os

# Получаем абсолютные пути для правильного включения файлов
script_path = os.path.abspath('focusapp-ui/main.py')
tolchki_path = os.path.abspath('focusapp-ui/tolchki.py')
poli_path = os.path.abspath('focusapp-ui/poli.py')
burger_path = os.path.abspath('focusapp-ui/burger.py')
musorka_path = os.path.abspath('focusapp-ui/musorka.py')

a = Analysis(
    [script_path],
    pathex=[os.path.dirname(script_path)],
    binaries=[],
    datas=[
        (tolchki_path, 'focusapp-ui'),
        (poli_path, 'focusapp-ui'),
        (burger_path, 'focusapp-ui'),
        (musorka_path, 'focusapp-ui')
    ],
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
    name='main',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main'
)
