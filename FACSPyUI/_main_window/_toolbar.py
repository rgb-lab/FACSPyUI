import os
from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from ._paths import ICON_PATH as icon_path
from ._filehandler import FileHandler

class ToolBar(QToolBar, FileHandler):
    def __init__(self, main_window):
        QToolBar.__init__(self, "Main Toolbar", main_window)
        self.set_main_window(main_window)  # Set the main window for FileHandler

        self.setIconSize(QSize(24, 24))


        self.new_action = QAction(QIcon(os.path.join(icon_path, "_new_analysis_light.svg")), "New Analysis", self)
        self.open_action = QAction(QIcon(os.path.join(icon_path, "_open_dir_light.svg")), "Open", self)
        self.save_action = QAction(QIcon(os.path.join(icon_path, "_save_light.svg")), "Save", self)

        self.addAction(self.new_action)
        self.addAction(self.open_action)
        self.addAction(self.save_action)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.addWidget(spacer)

        self.toggle_mode_action = QAction("Toggle Light/Dark Mode", self)
        self.addAction(self.toggle_mode_action)

        self.new_action.triggered.connect(self.create_new_dataset)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.toggle_mode_action.triggered.connect(self.toggle_mode)

        self.is_dark_mode = False
        self.update_mode_icon()

    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.set_dark_mode()
        else:
            self.set_light_mode()
        self.update_mode_icon()
        self.update_config_panel()
        self.update_file_icons()

    def update_file_icons(self):
        if self.is_dark_mode:
            self.new_action.setIcon(QIcon(os.path.join(icon_path, "_new_analysis_dark.svg")))
            self.open_action.setIcon(QIcon(os.path.join(icon_path, "_open_dir_dark.svg")))
            self.save_action.setIcon(QIcon(os.path.join(icon_path, "_save_dark.svg")))
        else:
            self.new_action.setIcon(QIcon(os.path.join(icon_path, "_new_analysis_light.svg")))
            self.open_action.setIcon(QIcon(os.path.join(icon_path, "_open_dir_light.svg")))
            self.save_action.setIcon(QIcon(os.path.join(icon_path, "_save_light.svg")))


    def update_config_panel(self):
        config_panel = self.main_window.config_panel
        current_index = config_panel.analysis_dropdown.currentIndex()
        config_panel.analysis_dropdown.currentIndexChanged.disconnect(config_panel.on_analysis_type_selected)
        config_panel.populate_analysis_dropdown()
        config_panel.analysis_dropdown.currentIndexChanged.connect(config_panel.on_analysis_type_selected)
        config_panel.analysis_dropdown.setCurrentIndex(current_index)

    def update_mode_icon(self):
        # if self.is_dark_mode:
        #     self.toggle_mode_action.setIcon(QIcon(os.path.join(icon_path, "sun_icon.svg")))
        # else:
        #     self.toggle_mode_action.setIcon(QIcon(os.path.join(icon_path, "moon_icon.svg")))
        return

    def set_dark_mode(self):
        self.main_window.set_style_sheet("dark")

    def set_light_mode(self):
        self.main_window.set_style_sheet("light")
