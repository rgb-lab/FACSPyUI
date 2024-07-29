# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata
import sys

sys.setrecursionlimit(5000)

datas = [
    ('_datasets/*', '_datasets/'),
    ('_icons/*', '_icons/'),
    ('_stylesheets/*', '_stylesheets/'),
    ('_main_window/*', '_main_window')
]
datas += copy_metadata('scanpy', recursive=True)

def collect_hidden_imports(dir_path, package_name):
    hidden_imports = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                module_path = os.path.relpath(os.path.join(root, file), dir_path).replace(os.sep, '.')
                hidden_imports.append(f"{package_name}.{module_path[:-3]}")
    return hidden_imports

# Collect hidden imports for '_stylesheets' and '_main_window' folders
hiddenimports = []
hiddenimports += collect_hidden_imports('_stylesheets', '_stylesheets')
hiddenimports += collect_hidden_imports('_main_window', '_main_window')


a = Analysis(
    ['FACSPyUI.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='FACSPyUI',
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
