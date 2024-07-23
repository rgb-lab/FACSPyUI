from PyQt5.QtWidgets import (QMessageBox, QVBoxLayout, 
                             QPushButton, QFormLayout, QLabel,
                             QComboBox)

from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QMutexLocker

import FACSPy as fp

from .._utils import LoadingScreen
from .._utils import error_handler
from ._analysis_menu import BaseAnalysisMenu


class BaseExpressionWindow(BaseAnalysisMenu):
    def __init__(self, main_window, title, advanced_params):
        super().__init__(main_window, title, advanced_params)

        # Main layout
        self.main_layout = QVBoxLayout()

        # Form layout for global options
        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        # Data format
        self.data_format_label = QLabel("Data format:")
        self.data_format_dropdown = QComboBox()
        self.form_layout.addRow(self.data_format_label, self.data_format_dropdown)

        # Group by
        self.group_by_label = QLabel("Group by:")
        self.group_by_dropdown = QComboBox()
        self.form_layout.addRow(self.group_by_label, self.group_by_dropdown)

        # Aggregation method
        self.agg_method_label = QLabel("Aggregation method:")
        self.agg_method_dropdown = QComboBox()
        self.agg_method_dropdown.addItems(["median", "mean"])
        self.agg_method_dropdown.setCurrentText("median")
        self.form_layout.addRow(self.agg_method_label, self.agg_method_dropdown)

        # Use markers only
        self.use_markers_only_label = QLabel("Use markers only:")
        self.use_markers_only_dropdown = QComboBox()
        self.use_markers_only_dropdown.addItems(["True", "False"])
        self.use_markers_only_dropdown.setCurrentText("False")
        self.form_layout.addRow(self.use_markers_only_label, self.use_markers_only_dropdown)

        # Aggregate
        self.aggregate_label = QLabel("Aggregate:")
        self.aggregate_dropdown = QComboBox()
        self.aggregate_dropdown.addItems(["True", "False"])
        self.aggregate_dropdown.setCurrentText("False")
        self.form_layout.addRow(self.aggregate_label, self.aggregate_dropdown)

        # Advanced settings section
        self.advanced_settings_layout = QFormLayout()

        # Calculate button
        self.calculate_button = QPushButton("Calculate Marker Expression")
        self.calculate_button.clicked.connect(self.calculate_marker_expression)
        self.main_layout.addWidget(self.calculate_button)

        self.setLayout(self.main_layout)

        # Populate dropdowns
        self.populate_dropdowns()
        
        self.finalize_window_layout()

    @error_handler("Dropdown Population Error")
    def populate_dropdowns(self):
        """
        Populates the dropdowns with relevant dataset information.
        """
        # try:
        dataset_key = self.main_window.dataset_dropdown.currentText()
        dataset = self.main_window.DATASHACK.get(dataset_key, None)

        if dataset is None:
            raise ValueError("No dataset selected or dataset not found.")

        # Populate data format dropdown
        self.data_format_dropdown.clear()
        self.data_format_dropdown.addItems(dataset.layers.keys())

        # Populate group by dropdown
        self.group_by_dropdown.clear()
        self.group_by_dropdown.addItems(dataset.obs.columns)

        # except Exception as e:
        #     self.show_error("Dropdown Population Error", str(e))

    def calculate_dimensionality_reduction(self):
        """
        Should be overridden in subclasses to perform the specific dimensionality reduction calculation.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class MFIWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, data_format, group_by, agg_method, use_markers_only, aggregate):
        super().__init__()
        self.dataset = dataset
        self.data_format = data_format
        self.group_by = group_by
        self.agg_method = agg_method
        self.use_markers_only = use_markers_only
        self.aggregate = aggregate
        self._is_running = True
        self._mutex = QMutex()

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Marker expression calculation was canceled.")
                    return

            fp.tl.mfi(self.dataset,
                      layer=self.data_format,
                      groupby=self.group_by,
                      method=self.agg_method,
                      use_only_fluo=self.use_markers_only,
                      aggregate=self.aggregate)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class MFIWindow(BaseExpressionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Calculate marker expression", [])

        self.pca_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        pass

    def calculate_marker_expression(self):
        """
        Performs the marker expression calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            data_format = self.data_format_dropdown.currentText()
            group_by = self.group_by_dropdown.currentText()
            agg_method = self.agg_method_dropdown.currentText()
            use_markers_only = self.use_markers_only_dropdown.currentText() == "True"
            aggregate = self.aggregate_dropdown.currentText() == "True"

            # Show loading screen
            loading_message = "Calculating marker expression..."
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the worker thread
            self.calculation_canceled = False
            self.mfi_worker = MFIWorker(dataset, data_format, group_by, agg_method, use_markers_only, aggregate)
            self.mfi_worker.finished.connect(self.on_mfi_finished)
            self.mfi_worker.error.connect(self.on_mfi_error)
            self.mfi_worker.start()

        except Exception as e:
            self.show_error("Marker Expression Calculation Error", str(e))

    def on_mfi_finished(self):
        """
        Handles the completion of the marker expression calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Marker expression calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_mfi_error(self, error_message):
        """
        Handles any error that occurs during the marker expression calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Marker Expression Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.mfi_worker:
            self.mfi_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Marker expression calculation has been cancelled.")


