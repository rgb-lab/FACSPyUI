import sys
import os
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView

from _main_window import ToolBar
from _stylesheets import breeze_resources

import plotly
from typing import Literal


class SplashScreen(QSplashScreen):
    def __init__(self, pixmap, delay=2000):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.delay = delay
        self.show()  # Ensure the splash screen is shown

    def show_message(self, message, alignment=Qt.AlignBottom | Qt.AlignCenter, color=Qt.black):
        """
        Displays a message on the splash screen.
        """
        self.showMessage(message, alignment, color)
        QApplication.processEvents()


# Run imports function
def run_imports(splash):
    """
    Sequentially imports packages and updates the splash screen.
    """
    import_list = [
        ("Initializing module matplotlib...", "import matplotlib.pyplot as plt"),
        ("Initializing module seaborn...", "import seaborn as sns"),
        ("Initializing module seaborn...", "import plotly"),
        ("Initializing module pandas...", "import pandas as pd"),
        ("Initializing module numpy...", "import numpy as np"),
        ("Initializing module scipy...", "import scipy"),
        ("Initializing module sklearn...", "import sklearn"),
        ("Initializing module scanpy...", "import scanpy"),
        ("Initializing FACSPy...", "import FACSPy as fp"),
    ]

    for message, imp in import_list:
        splash.show_message(message)
        exec(imp)


def main():
    app = QApplication(sys.argv)
    if hasattr(sys, "_MEIPASS"):
    # Create and display the splash screen
        pixmap = QPixmap(os.path.join(sys._MEIPASS, "_icons/facspyqt_logo.png"))
    else:
        pixmap = QPixmap("./_icons/facspyqt_logo.png")
    splash = SplashScreen(pixmap)
    splash.show()
    run_imports(splash)

    import FACSPy as fp
    from _main_window import ToolBar
    from _main_window._analyze_dataset import (ConfigPanel, PlotWindow)
    from _main_window._menubar import MenuBar

    from _main_window._paths import ICON_PATH as icon_path
    from _main_window._paths import DATA_PATH as data_path
    from _stylesheets import dark_stylesheet, light_stylesheet, breeze_resources
    import copy
    from PyQt5.QtWidgets import (QMainWindow, QSplitter, QVBoxLayout, QHBoxLayout, QWidget, QComboBox,
                                 QLabel, QScrollArea, QSizePolicy, QPushButton, QInputDialog, QMessageBox,
                                 QFrame)
    from PyQt5.QtGui import QIcon

    class FACSPyBrowser(QMainWindow):
        def __init__(self, light_stylesheet, dark_stylesheet):
            super().__init__()

            self.light_stylesheet = light_stylesheet
            self.dark_stylesheet = dark_stylesheet
            self.stylesheet = self.light_stylesheet

            DATASHACK = {
                "mouse_lineages": fp.read_dataset(data_path, "mouse_lineages_downsampled.h5ad")
            }

            # Set up the main window
            self.setWindowTitle("FACSPyBrowser")
            self.setGeometry(100, 100, 1200, 800)

            # Add the window icon
            self.setWindowIcon(QIcon(os.path.join(icon_path, "facspyqt_logo.png")))

            self.DATASHACK = DATASHACK

            # Initialize MenuBar and ToolBar
            self.menu_bar = MenuBar(self)
            self.setMenuBar(self.menu_bar)
            self.toolbar = ToolBar(self)
            self.addToolBar(self.toolbar)

            self.init_ui()

        def get_style_sheet(self,
                            which: Literal["light", "dark"]):
            if which == "light":
                return self.light_stylesheet
            else:
                assert which == "dark"
                return self.dark_stylesheet

        def set_style_sheet(self,
                            which: Literal["light", "dark"]):
            self.stylesheet = self.get_style_sheet(which)

        def init_ui(self):
            # Create a top container for the dataset selection and display
            top_layout = QHBoxLayout()
            top_layout.setSpacing(10)

            # Dataset selection dropdown
            self.dataset_dropdown = QComboBox()
            self.dataset_dropdown.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
            self.dataset_dropdown.currentIndexChanged.connect(self.on_dataset_selected)
            self.dataset_dropdown.addItem("Select Dataset")  # Placeholder option
            top_layout.addWidget(self.dataset_dropdown)

            # Create a scrollable area for the dataset display
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.dataset_display = QLabel("")
            self.dataset_display.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.dataset_display.setWordWrap(True)
            scroll_area.setWidget(self.dataset_display)
            top_layout.addWidget(scroll_area)

            # Create a vertical layout for the dataset action buttons
            button_layout = QVBoxLayout()

            self.copy_button = QPushButton("Copy Dataset")
            self.copy_button.clicked.connect(self.copy_dataset)
            button_layout.addWidget(self.copy_button)

            self.rename_button = QPushButton("Rename Dataset")
            self.rename_button.clicked.connect(self.rename_dataset)
            button_layout.addWidget(self.rename_button)

            self.remove_button = QPushButton("Remove Dataset")
            self.remove_button.clicked.connect(self.remove_dataset)
            button_layout.addWidget(self.remove_button)

            top_layout.addLayout(button_layout)  # Add button layout to the top layout

            # Create a container widget and set the top layout
            top_container = QWidget()
            top_container.setLayout(top_layout)
            top_container.setMaximumHeight(160)  # Initial height

            # Create the splitter to separate top and bottom areas
            self.main_splitter = QSplitter(Qt.Vertical)
            self.main_splitter.addWidget(top_container)
            self.main_splitter.setHandleWidth(2)  # Set handle width for visibility
            self.main_splitter.setStyleSheet("QSplitter::handle { background-color: gray; }")  # Set handle color

            # Create a bottom container for the splitter
            bottom_splitter = QSplitter(Qt.Horizontal)

            # ConfigPanel for the left side
            self.config_panel = ConfigPanel(self)
            bottom_splitter.addWidget(self.config_panel)

            # PlotWindow for the right side
            self.plot_window = PlotWindow(self)
            bottom_splitter.addWidget(self.plot_window)

            # Connect plot requested signal
            self.config_panel.plot_requested.connect(self.plot_window.switch_to_specific_plot_window)

            # Set sizes (66% for the right side, 34% for the left side)
            bottom_splitter.setStretchFactor(0, 1)
            bottom_splitter.setStretchFactor(1, 2)

            # Add the bottom splitter to the main splitter
            self.main_splitter.addWidget(bottom_splitter)
            self.main_splitter.setStretchFactor(0, 1)
            self.main_splitter.setStretchFactor(1, 10)  # Adjusting the initial size ratio

            # Create the main layout and add the splitter
            layout = QVBoxLayout()
            layout.addWidget(self.main_splitter)

            # Create a container widget and set the layout
            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

            # Initialize the dropdown with DATASHACK keys
            self.populate_dataset_dropdown()

        def create_horizontal_line(self):
            """
            Creates a QFrame that acts as a horizontal line (similar to <hr> in HTML).
            """
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            return line

        def populate_dataset_dropdown(self):
            """
            Populates the dataset dropdown with keys from DATASHACK.
            """
            self.dataset_dropdown.clear()
            self.dataset_dropdown.addItem("Select Dataset")  # Add placeholder first
            for key in self.DATASHACK:
                self.dataset_dropdown.addItem(key)
            self.dataset_dropdown.setCurrentIndex(0)  # Select the placeholder

        def on_dataset_selected(self):
            """
            Triggered when a dataset is selected from the dropdown.
            """
            if hasattr(self, "config_panel") and self.config_panel._config_panel is not None:
                self.config_panel._config_panel.update_plotting_dropdowns()
                self.config_panel._config_panel.update_calculation_dropdowns()

                self.config_panel.update_plotting_tab()  # Trigger dropdown updates in ConfigPanel
            self.update_current_dataset_display()


        def _parse_dimreds(self,
                           dataset):
            obsm_keys = list(dataset.obsm.keys())
            dimred_keys = [key for key in obsm_keys if any(k in key for k in ["umap", "tsne", "pca", "diffmap"])]
            dimred_str = ""
            for key in dimred_keys:
                _, red, gate, data_format = key.split("_")
                dimred_str += f"\t{red.upper()} ({gate}, {data_format})\n"

            return dimred_str
            
        def create_dataset_string(self,
                                  dataset):
            n_cells, n_channels = dataset.shape
            metadata_cols = list(dataset.obs.columns)
            layers = list(dataset.layers.keys())

            return (
                f"Dataset with {n_cells} cells and {n_channels} channels\n" +
                "Available metadata: \n" + 
                f"\t{', '.join(metadata_cols)}\n" + 
                "Available data formats:\n" + 
                f"\t{', '.join(layers)}\n" + 
                "Dimensionality Reductions performed:\n" +
                self._parse_dimreds(dataset)
            )

        def update_current_dataset_display(self):
            """
            Updates the display to show the current dataset's representation.
            """
            selected_key = self.dataset_dropdown.currentText()
            if not hasattr(self, "dataset_display"):
                return
            if (dataset := self.DATASHACK.get(selected_key)):
                dataset_repr = self.create_dataset_string(dataset)
                self.dataset_display.setText(dataset_repr)
            else:
                self.dataset_display.setText("")

        def load_dataset(self, dataset_key, dataset_value):
            """
            Loads a dataset into DATASHACK and updates the dropdown menu.
            """
            # Add the dataset to DATASHACK
            self.DATASHACK[dataset_key] = dataset_value

            # Update the dropdown menu
            self.populate_dataset_dropdown()
            self.dataset_dropdown.setCurrentText(dataset_key)

        def copy_dataset(self):
            """
            Copies the currently selected dataset.
            """
            selected_key = self.dataset_dropdown.currentText()
            if selected_key in self.DATASHACK:
                new_name, ok = QInputDialog.getText(self, "Copy Dataset", "Enter new dataset name:")
                if ok and new_name:
                    if new_name not in self.DATASHACK:
                        self.DATASHACK[new_name] = copy.deepcopy(self.DATASHACK[selected_key])
                        self.populate_dataset_dropdown()
                        self.dataset_dropdown.setCurrentText(new_name)  # Select the new dataset
                        QMessageBox.information(self, "Success", f"Dataset '{selected_key}' copied to '{new_name}'.")
                    else:
                        QMessageBox.warning(self, "Warning", f"Dataset '{new_name}' already exists.")
                else:
                    QMessageBox.warning(self, "Warning", "Invalid dataset name.")

        def rename_dataset(self):
            """
            Renames the currently selected dataset.
            """
            selected_key = self.dataset_dropdown.currentText()
            if selected_key in self.DATASHACK:
                new_name, ok = QInputDialog.getText(self, "Rename Dataset", "Enter new dataset name:")
                if ok and new_name:
                    if new_name not in self.DATASHACK:
                        self.DATASHACK[new_name] = self.DATASHACK.pop(selected_key)
                        self.populate_dataset_dropdown()
                        self.dataset_dropdown.setCurrentText(new_name)  # Select the renamed dataset
                        QMessageBox.information(self, "Success", f"Dataset '{selected_key}' renamed to '{new_name}'.")
                    else:
                        QMessageBox.warning(self, "Warning", f"Dataset '{new_name}' already exists.")
                else:
                    QMessageBox.warning(self, "Warning", "Invalid dataset name.")

        def remove_dataset(self):
            """
            Removes the currently selected dataset.
            """
            selected_key = self.dataset_dropdown.currentText()
            if selected_key in self.DATASHACK:
                reply = QMessageBox.question(self, "Remove Dataset",
                                             f"Are you sure you want to remove dataset '{selected_key}'?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    del self.DATASHACK[selected_key]
                    self.populate_dataset_dropdown()
                    QMessageBox.information(self, "Success", f"Dataset '{selected_key}' removed.")


    # light_file = QFile(":/light/stylesheet.qss")
    # light_file.open(QFile.ReadOnly | QFile.Text)
    # light_stream = QTextStream(light_file)
    # light_stylesheet = light_stream.readAll()

    # dark_file = QFile(":/dark/stylesheet.qss")
    # dark_file.open(QFile.ReadOnly | QFile.Text)
    # dark_stream = QTextStream(dark_file)
    # dark_stylesheet = dark_stream.readAll()

    window = FACSPyBrowser(light_stylesheet, dark_stylesheet)
    window.setStyleSheet(light_stylesheet)
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
