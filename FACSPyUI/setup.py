from distutils.core import setup
import py2exe
import sys
import os

# Include the icon files and datasets in the executable
data_files = [
    ('_datasets', [os.path.join('_datasets', f) for f in os.listdir('_datasets')]),
    ('_icons', [os.path.join('_icons', f) for f in os.listdir('_icons')])
]

# Append the 'py2exe' command if it's not present (required for py2exe)
if 'py2exe' not in sys.argv:
    sys.argv.append('py2exe')

# Main script to convert to executable
script = 'app.py'

# py2exe options
options = {
    'py2exe': {
        'bundle_files': 1,  # Bundle everything into a single file
        'compressed': True,
        'includes': ['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'scanpy', 'FACSPy'],
        'excludes': [],
        'dll_excludes': ['w9xpopen.exe'],  # Exclude DLLs that are not needed
        'optimize': 2,
        'dist_dir': 'py2exe',  # Output directory for the built files
    }
}

# Setup configuration
setup(
    name='FACSPyUI',
    version='1.0',
    description='FACSPyUI',
    author='Tarik Exner',
    options=options,
    data_files=data_files,
    windows=[{'script': script, 'dest_base': 'FACSPyUI'}],  # Use 'windows=[script]' if it's a GUI application without a console window
    zipfile=None,
    py_modules=['app']
)
