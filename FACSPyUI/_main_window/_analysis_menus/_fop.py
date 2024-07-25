from PyQt5.QtWidgets import (QMessageBox, QVBoxLayout, 
                             QPushButton, QFormLayout, QLabel,
                             QComboBox, QLineEdit)

from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QMutexLocker

import FACSPy as fp

from .._utils import LoadingScreen
from ._analysis_menu import BaseAnalysisMenu


class BaseFOPWindow(BaseAnalysisMenu):
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
        data_format_container = self.add_tooltip(self.data_format_dropdown, parameter = "data_format")
        self.form_layout.addRow(self.data_format_label, data_format_container)

        # Cutoff
        self.cutoff_label = QLabel("Cutoff:")
        self.cutoff_input = QLineEdit()
        self.cutoff_input.setPlaceholderText("use cofactors")
        cutoff_container = self.add_tooltip(self.cutoff_input, parameter = "cutoff")
        self.form_layout.addRow(self.cutoff_label, cutoff_container)

        # Group by
        self.group_by_label = QLabel("Group by:")
        self.group_by_dropdown = QComboBox()
        groupby_container = self.add_tooltip(self.group_by_dropdown, parameter = "group_by_fluo_metrics")
        self.form_layout.addRow(self.group_by_label, groupby_container)

        # Use markers only
        self.use_markers_only_label = QLabel("Use markers only:")
        self.use_markers_only_dropdown = QComboBox()
        self.use_markers_only_dropdown.addItems(["True", "False"])
        self.use_markers_only_dropdown.setCurrentText("False")
        use_markers_only_container = self.add_tooltip(self.use_markers_only_dropdown, parameter = "use_markers_only")
        self.form_layout.addRow(self.use_markers_only_label, use_markers_only_container)

        # Aggregate
        self.aggregate_label = QLabel("Aggregate:")
        self.aggregate_dropdown = QComboBox()
        self.aggregate_dropdown.addItems(["True", "False"])
        self.aggregate_dropdown.setCurrentText("False")
        aggregate_container = self.add_tooltip(self.aggregate_dropdown, parameter = "aggregate")

        self.form_layout.addRow(self.aggregate_label, aggregate_container)

        # Advanced settings section
        self.advanced_settings_layout = QFormLayout()

        # Calculate button
        self.calculate_button = QPushButton("Calculate FOP")
        self.calculate_button.clicked.connect(self.calculate_fop)
        self.main_layout.addWidget(self.calculate_button)

        self.setLayout(self.main_layout)

        # Populate dropdowns
        self.populate_dropdowns()
        
        self.finalize_window_layout()

    def populate_dropdowns(self):
        """
        Populates the dropdowns with relevant dataset information.
        """
        try:
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

        except Exception as e:
            self.show_error("Dropdown Population Error", str(e))

    def calculate_fop(self):
        """
        Should be overridden in subclasses to perform the FOP calculation.
        """
        raise NotImplementedError("Subclasses should implement this method.")


class FOPWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, data_format, cutoff, group_by, use_markers_only, aggregate):
        super().__init__()
        self.dataset = dataset
        self.data_format = data_format
        self.cutoff = cutoff if cutoff != "use cofactors" else None
        self.group_by = group_by
        self.use_markers_only = use_markers_only
        self.aggregate = aggregate
        self._is_running = True
        self._mutex = QMutex()

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("FOP calculation was canceled.")
                    return

            if not self.cutoff:
                self.cutoff = None

            fp.tl.fop(
                self.dataset,
                layer=self.data_format,
                cutoff=self.cutoff,
                groupby=self.group_by,
                use_only_fluo=self.use_markers_only,
                aggregate=self.aggregate
            )

            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class FOPWindow(BaseFOPWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Calculate FOP", [])

        self.fop_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        pass

    def calculate_fop(self):
        """
        Performs the FOP calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            data_format = self.data_format_dropdown.currentText()
            cutoff = self.cutoff_input.text()
            group_by = self.group_by_dropdown.currentText()
            use_markers_only = self.use_markers_only_dropdown.currentText() == "True"
            aggregate = self.aggregate_dropdown.currentText() == "True"

            # Show loading screen
            loading_message = "Calculating FOP..."
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the worker thread
            self.calculation_canceled = False
            self.fop_worker = FOPWorker(dataset, data_format, cutoff, group_by, use_markers_only, aggregate)
            self.fop_worker.finished.connect(self.on_fop_finished)
            self.fop_worker.error.connect(self.on_fop_error)
            self.fop_worker.start()

        except Exception as e:
            self.show_error("FOP Calculation Error", str(e))

    def on_fop_finished(self):
        """
        Handles the completion of the FOP calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "FOP calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_fop_error(self, error_message):
        """
        Handles any error that occurs during the FOP calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("FOP Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.fop_worker:
            self.fop_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "FOP calculation has been cancelled.")

