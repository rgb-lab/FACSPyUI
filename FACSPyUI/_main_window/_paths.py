import sys
import os

if getattr(sys, "frozen", False):
    DATA_PATH = os.path.join(sys._MEIPASS, "_datasets/")
    ICON_PATH = os.path.join(sys._MEIPASS, "_icons/")
else:
    DATA_PATH = "./_datasets"
    ICON_PATH = "./_icons"

