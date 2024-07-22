import pandas as pd
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QLineEdit, QFileDialog,
                             QComboBox, QHBoxLayout, QFrame,
                             QMessageBox, QFormLayout)
from .._utils import MultiSelectComboBox
from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QMutexLocker

from .._utils import LoadingScreen

import FACSPy as fp

class DatasetCreator(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, main_window, input_dir, metadata, panel, wsp, subsample_fcs_to,
                 transform, cofactor_table, key_added):
        super().__init__()
        self.main_window = main_window
        self.input_dir = input_dir
        self.metadata = metadata
        self.panel = panel
        self.wsp = wsp
        self.subsample_fcs_to = subsample_fcs_to

        self.transform = transform
        self.cofactor_table = cofactor_table
        self.key_added = key_added
        self._is_running = True
        self._mutex = QMutex()  # Mutex for thread-safe flag

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Dataset creation was canceled.")
                    return

            dataset = fp.dt.create_dataset(
                    input_directory = self.input_dir,
                    metadata = self.metadata,
                    panel = self.panel,
                    workspace = self.wsp,
                    subsample_fcs_to = self.subsample_fcs_to
            )
            if self.transform != "None":
                fp.dt.transform(dataset,
                                transform = self.transform,
                                cofactor_table = self.cofactor_table,
                                key_added = self.key_added)

            self.main_window.DATASHACK["user-created"] = dataset

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False

class SettingsTab(QWidget):
    def __init__(self, main_window, create_dataset_window):
        super().__init__()
        self.main_window = main_window
        self.create_dataset_window = create_dataset_window

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create sections with fixed heights
        section_height = 80

        # Section 1: Select input directory
        self.input_dir_label = QLabel("Select input directory:")
        self.input_dir_display = QLineEdit()
        self.input_dir_display.setReadOnly(True)
        self.select_input_dir_button = QPushButton("Select Directory")
        self.select_input_dir_button.clicked.connect(self.open_directory_dialog)

        # Section 2: Upload workspace
        self.upload_workspace_label = QLabel("Upload workspace:")
        self.upload_workspace_text = QLineEdit()
        self.upload_workspace_text.setReadOnly(True)
        self.upload_workspace_button = QPushButton("Load")
        self.upload_workspace_button.clicked.connect(self.open_file_dialog)

        # Section 3: Subsample FCS to
        self.subsample_fcs_label = QLabel("Subsample FCS to:")
        self.subsample_fcs_input = QLineEdit()

        # Section 4: Select transformation
        self.transformation_label = QLabel("Select transformation:")
        self.transformation_combo = QComboBox()
        self.transformation_combo.addItems(["asinh", "logicle", "log", "hyperlog", "None"])

        # Section 5: Choose transformed layer name
        self.transformed_layer_label = QLabel("Choose transformed layer name:")
        self.transformed_layer_input = QLineEdit()

        # Section 6: Buttons line
        self.check_metadata_button = QPushButton("Check metadata")
        self.create_dataset_button = QPushButton("Create Dataset")

        # Create QFormLayout and add widgets
        self.form_layout = QFormLayout()
        self.form_layout.addRow(self.input_dir_label, self.create_horizontal_layout(self.input_dir_display, self.select_input_dir_button))
        self.form_layout.addRow(self.upload_workspace_label, self.create_horizontal_layout(self.upload_workspace_text, self.upload_workspace_button))
        self.form_layout.addRow(self.subsample_fcs_label, self.subsample_fcs_input)
        self.form_layout.addRow(self.transformation_label, self.transformation_combo)
        self.form_layout.addRow(self.transformed_layer_label, self.transformed_layer_input)
        self.form_layout.addRow("", self.create_horizontal_layout(self.check_metadata_button, self.create_dataset_button))

        # Add form layout to main layout
        main_layout.addLayout(self.form_layout)

        self.main_layout = main_layout

        # Connect buttons to their respective methods
        self.check_metadata_button.clicked.connect(self.check_metadata)
        self.create_dataset_button.clicked.connect(self.create_dataset)

        self.set_input_size_policies()

    def set_input_size_policies(self):
        """
        Sets the size policies for input fields and buttons to be half the width of the parent container,
        excluding children of MultiSelectComboBox.
        """
        adjustment_factor = 0.9
        parent_width = self.size().width() * adjustment_factor
        half_width = int(parent_width // 2)

        def set_size_policy(widget):
            if isinstance(widget, (QLineEdit, QComboBox, QPushButton, QLabel)) and not isinstance(widget.parent(), MultiSelectComboBox):
                widget.setFixedWidth(half_width)

        # Apply size policies to direct children only
        for widget in self.form_layout.findChildren(QWidget):
            set_size_policy(widget)

    def create_horizontal_layout(self, widget1, widget2):
        """
        Creates a QHBoxLayout with two widgets.
        """
        layout = QHBoxLayout()
        layout.addWidget(widget1)
        layout.addWidget(widget2)
        return layout

    def add_horizontal_line(self, layout):
        """
        Adds a horizontal line (QFrame) to the layout.
        """
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

    def open_directory_dialog(self):
        """
        Opens a directory dialog and displays the selected directory.
        """
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.input_dir_display.setText(directory)

    def open_file_dialog(self):
        """
        Opens a file dialog and displays the selected file.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_name:
            self.upload_workspace_text.setText(file_name)

    def check_metadata(self):
        """
        Gathers the tables from MetadataTab and PanelTab and checks if they are correct.
        We let FACSPy do the checking for us
        """
        metadata_tab = self.parent().findChild(QWidget, "Metadata")
        panel_tab = self.parent().findChild(QWidget, "Panel")
        cofactors_tab = self.parent().findChild(QWidget, "Cofactor Table")

        metadata_table = self.table_to_dataframe(metadata_tab.table)
        panel_table = self.table_to_dataframe(panel_tab.table)
        cofactor_table = self.table_to_dataframe(cofactors_tab.table)

        try:
            if metadata_table.shape[0] == 0:
                raise ValueError("No entries in Metadata found")
            if panel_table.shape[0] == 0:
                raise ValueError("No entries in Panel found")
            _ = fp.dt.Metadata(metadata = metadata_table)
            _ = fp.dt.Panel(panel = panel_table)
            if cofactor_table.shape[0] != 0:
                _ = fp.dt.CofactorTable(cofactors = cofactor_table)
        except Exception as e:
            self.show_error("Supplement Error", str(e))
            return

        QMessageBox.information(self, "Check Metadata", "Metadata are fine!")

    def create_dataset(self):
        """
        Creates an empty pandas DataFrame and displays a message in the main window.
        """
        metadata_tab = self.parent().findChild(QWidget, "Metadata")
        panel_tab = self.parent().findChild(QWidget, "Panel")
        cofactors_tab = self.parent().findChild(QWidget, "Cofactor Table")

        metadata_table = self.table_to_dataframe(metadata_tab.table)
        panel_table = self.table_to_dataframe(panel_tab.table)
        cofactor_table = self.table_to_dataframe(cofactors_tab.table)

        metadata = fp.dt.Metadata(metadata = metadata_table)
        panel = fp.dt.Panel(panel = panel_table)
        if cofactor_table.shape[0] != 0:
            cofactors = fp.dt.CofactorTable(cofactors = cofactor_table)
        else:
            cofactors = None
        input_dir = self.input_dir_display.text()
        wsp_name = self.upload_workspace_text.text()
        wsp = fp.dt.FlowJoWorkspace(wsp_name)
        subsample_fcs_to = int(self.subsample_fcs_input.text())

        key_added = self.transformed_layer_input.text()
        transform = self.transformation_combo.currentText()

        # Show loading screen
        loading_message = "Creating dataset...\n\n"
        self.loading_screen = LoadingScreen(message=loading_message)
        self.loading_screen.cancel_signal.connect(self.cancel_calculation)
        self.loading_screen.show()

        self.calculation_canceled = False
        self.worker = DatasetCreator(
            self.main_window, input_dir, metadata, panel, wsp, subsample_fcs_to,
            transform, cofactors, key_added
        )
        self.worker.finished.connect(self.on_creation_finished)
        self.worker.error.connect(self.on_creation_error)
        self.worker.start()

    def on_creation_finished(self):
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "dataset creation completed.")
            self.main_window.update_current_dataset_display()
            self.main_window.populate_dataset_dropdown()
            self.create_dataset_window.close()

    def on_creation_error(self, error_message):
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Creation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.worker:
            self.worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Dataset Creation has been cancelled.")

    def show_error(self, title, message):
        """
        Displays an error message in a QMessageBox.
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def table_to_dataframe(self, table_widget):
        """
        Converts a QTableWidget to a pandas DataFrame.
        """
        rows = table_widget.rowCount()
        columns = table_widget.columnCount()
        headers = [table_widget.horizontalHeaderItem(c).text() for c in range(columns)]
        data = []

        for row in range(rows):
            row_data = {}
            for column in range(columns):
                item = table_widget.item(row, column)
                row_data[headers[column]] = item.text() if item else ""
            data.append(row_data)

        return pd.DataFrame(data, columns=headers)
