from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QMenuBar, QAction, QFileDialog, QHBoxLayout, QLabel)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSignal

from ._metadata_tab import MetadataTab
from ._panel_tab import PanelTab
from ._settings_tab import SettingsTab
from ._cofactors_tab import CofactorsTab

import pandas as pd

class CreateDatasetWindow(QWidget):
    dataset_created = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet(self.main_window.stylesheet)

        self.setWindowTitle("New Analysis")
        self.setGeometry(100, 100, 800, 600)

        # Create layout
        main_layout = QVBoxLayout()

        # Create QMenuBar
        self.menubar = QMenuBar(self)

        # Create the "Modify" menu
        modify_menu = self.menubar.addMenu("Modify Table")
        
        # Load File action
        load_action = QAction("Load Table", self)
        load_action.setShortcut(QKeySequence("Ctrl+L"))  # Shortcut for Load
        load_action.triggered.connect(self.open_file_dialog)
        modify_menu.addAction(load_action)
        
        # Add Column action
        add_column_action = QAction("Add Column", self)
        add_column_action.setShortcut(QKeySequence("Ctrl+Shift+C"))  # Shortcut for Add Column
        add_column_action.triggered.connect(self.add_column_to_current_tab)
        modify_menu.addAction(add_column_action)

        # Remove Column action
        remove_column_action = QAction("Remove Column", self)
        remove_column_action.setShortcut(QKeySequence("Ctrl+Shift+X"))  # Shortcut for Remove Column
        remove_column_action.triggered.connect(self.remove_column_from_current_tab)
        modify_menu.addAction(remove_column_action)

        # Add Row action
        add_row_action = QAction("Add Row", self)
        add_row_action.setShortcut(QKeySequence("Ctrl+Shift+R"))  # Shortcut for Add Row
        add_row_action.triggered.connect(self.add_row_to_current_tab)
        modify_menu.addAction(add_row_action)

        # Remove Row action
        remove_row_action = QAction("Remove Row", self)
        remove_row_action.setShortcut(QKeySequence("Ctrl+Shift+E"))  # Shortcut for Remove Row
        remove_row_action.triggered.connect(self.remove_row_from_current_tab)
        modify_menu.addAction(remove_row_action)

        # Create QTabWidget
        self.tabs = QTabWidget()
        
        # Create and add tabs
        self.metadata_tab = MetadataTab()
        self.panel_tab = PanelTab()
        self.cofactors_tab = CofactorsTab()
        self.settings_tab = SettingsTab(self.main_window, self)
        
        # Add tabs to QTabWidget and set object names
        self.tabs.addTab(self.metadata_tab, "Metadata")
        self.metadata_tab.setObjectName("Metadata")
        self.tabs.addTab(self.panel_tab, "Panel")
        self.panel_tab.setObjectName("Panel")
        self.tabs.addTab(self.cofactors_tab, "Cofactor Table")
        self.cofactors_tab.setObjectName("Cofactor Table")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.settings_tab.setObjectName("Settings")

        # Add the menubar and tabs to the main layout
        main_layout.setMenuBar(self.menubar)
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Tabular File", "", "CSV Files (*.csv);;TSV Files (*.tsv);;All Files (*)", options=options)
        if file_name:
            current_tab = self.tabs.currentWidget()
            if hasattr(current_tab, 'load_table'):
                current_tab.load_table(file_name)

    def add_column_to_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if hasattr(current_tab, 'add_column'):
            current_tab.add_column()

    def remove_column_from_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if hasattr(current_tab, 'remove_selected_column'):
            current_tab.remove_selected_column()

    def add_row_to_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if hasattr(current_tab, 'add_row'):
            current_tab.add_row()

    def remove_row_from_current_tab(self):
        current_tab = self.tabs.currentWidget()
        if hasattr(current_tab, 'remove_row'):
            current_tab.remove_row()

    def create_dataset(self):
        """
        Creates an empty pandas DataFrame and emits a signal to notify that the dataset has been loaded.
        """
        # Create an empty DataFrame
        self.dataset = pd.DataFrame()

        # Emit a signal with the message
        self.dataset_created.emit("The dataset has been loaded.")
