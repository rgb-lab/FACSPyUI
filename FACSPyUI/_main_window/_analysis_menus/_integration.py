from PyQt5.QtWidgets import (QMessageBox, QVBoxLayout, 
                             QPushButton, QFormLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox,
                             QGroupBox)
from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QMutexLocker

import FACSPy as fp

from .._utils import LoadingScreen
from ._analysis_menu import BaseAnalysisMenu

class BaseIntegrationWindow(BaseAnalysisMenu):
    def __init__(self, main_window, title, advanced_params):
        super().__init__(main_window, title, advanced_params)

        # Main layout
        self.main_layout = QVBoxLayout()

        # Form layout for global options
        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        # Gate
        self.gate_label = QLabel("Gate:")
        self.gate_dropdown = QComboBox()
        self.form_layout.addRow(self.gate_label, self.gate_dropdown)

        # Data format
        self.data_format_label = QLabel("Data format:")
        self.data_format_dropdown = QComboBox()
        self.form_layout.addRow(self.data_format_label, self.data_format_dropdown)

        # Batch column
        self.batch_column_label = QLabel("Batch column:")
        self.batch_column_dropdown = QComboBox()
        self.form_layout.addRow(self.batch_column_label, self.batch_column_dropdown)

        # Embedding to integrate
        self.embedding_label = QLabel("Embedding to integrate:")
        self.embedding_dropdown = QComboBox()
        self.form_layout.addRow(self.embedding_label, self.embedding_dropdown)

        # Integrated embedding name
        self.integrated_embedding_label = QLabel("Integrated embedding name:")
        self.integrated_embedding_input = QLineEdit()
        self.form_layout.addRow(self.integrated_embedding_label, self.integrated_embedding_input)

        # Advanced settings checkbox
        self.advanced_settings_checkbox = QCheckBox("Show Advanced Settings")
        self.advanced_settings_checkbox.stateChanged.connect(self.toggle_advanced_settings)
        self.main_layout.addWidget(self.advanced_settings_checkbox)

        # Advanced settings section
        self.advanced_settings_layout = QFormLayout()
        self.advanced_settings_group = QGroupBox("Advanced Settings")
        self.advanced_settings_group.setLayout(self.advanced_settings_layout)
        self.advanced_settings_group.setVisible(False)
        self.main_layout.addWidget(self.advanced_settings_group)

        # Add advanced settings
        self.add_advanced_settings()

        # Calculate button
        self.calculate_button = QPushButton(f"Calculate {title.split()[0]}")
        self.calculate_button.clicked.connect(self.calculate_integration)
        self.main_layout.addWidget(self.calculate_button)

        self.setLayout(self.main_layout)

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

            # Populate gate dropdown
            self.gate_dropdown.clear()
            self.gate_dropdown.addItems(dataset.uns.get("gating_cols", []))

            # Populate data format dropdown
            self.data_format_dropdown.clear()
            self.data_format_dropdown.addItems(dataset.layers.keys())

            # Populate batch column dropdown
            self.batch_column_dropdown.clear()
            self.batch_column_dropdown.addItems(dataset.obs.columns.tolist())

            # Populate embedding to integrate dropdown
            self.embedding_dropdown.clear()
            self.embedding_dropdown.addItems([key for key in dataset.obsm.keys() if key != "gating"])

        except Exception as e:
            self.show_error("Dropdown Population Error", str(e))

    def calculate_integration(self):
        """
        Should be overridden in subclasses to perform the specific integration calculation.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class HarmonyWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, gate, layer, batch_column, embedding_to_integrate, integrated_embedding_name, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.gate = gate
        self.layer = layer
        self.batch_column = batch_column
        self.embedding_to_integrate = embedding_to_integrate
        self.integrated_embedding_name = integrated_embedding_name
        self.advanced_kwargs = advanced_kwargs
        self._is_running = True
        self._mutex = QMutex()

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Harmony integration was canceled.")
                    return

            fp.tl.harmony_integrate(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                key=self.batch_column,
                basis=self.embedding_to_integrate,
                adjusted_basis=self.integrated_embedding_name,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        self._is_running = False


class HarmonyWindow(BaseIntegrationWindow):
    def __init__(self, main_window):
        advanced_params = {
            "theta": None,
            "lamb": None,
            "sigma": 0.1,
            "nclust": None,
            "tau": 0,
            "block_size": 0.05,
            "max_iter_harmony": 10,
            "max_iter_kmeans": 20,
            "epsilon_cluster": 1e-5,
            "epsilon_harmony": 1e-4,
            "plot_convergence": False,
            "verbose": True,
            "reference_values": None,
            "cluster_prior": None,
            "random_state": 0
        }
        super().__init__(main_window, "Harmony Integration", advanced_params)
        self.harmony_worker = None
        self.calculation_canceled = False

    def calculate_integration(self):
        """
        Performs the Harmony integration with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            gate = self.gate_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            batch_column = self.batch_column_dropdown.currentText()
            embedding_to_integrate = self.embedding_dropdown.currentText()
            integrated_embedding_name = self.integrated_embedding_input.text()

            # Collect advanced parameters
            advanced_kwargs = {}
            for param, default in self.advanced_params.items():
                input_field = getattr(self, f"{param}_input")
                value = input_field.text() or str(default)
                if value.lower() == "none":
                    advanced_kwargs[param] = None
                elif value.lower() == "true":
                    advanced_kwargs[param] = True
                elif value.lower() == "false":
                    advanced_kwargs[param] = False
                else:
                    try:
                        advanced_kwargs[param] = float(value) if '.' in value else int(value)
                    except ValueError:
                        advanced_kwargs[param] = value

            # Show loading screen
            loading_message = "Calculating Harmony Integration...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the Harmony worker thread
            self.calculation_canceled = False
            self.harmony_worker = HarmonyWorker(
                dataset, gate, layer, batch_column, embedding_to_integrate, integrated_embedding_name, advanced_kwargs
            )
            self.harmony_worker.finished.connect(self.on_integration_finished)
            self.harmony_worker.error.connect(self.on_integration_error)
            self.harmony_worker.start()

        except Exception as e:
            self.show_error("Harmony Integration Error", str(e))

    def on_integration_finished(self):
        """
        Handles the completion of the Harmony integration.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Harmony integration completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_integration_error(self, error_message):
        """
        Handles any error that occurs during the Harmony integration.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Harmony Integration Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.harmony_worker:
            self.harmony_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Harmony integration has been cancelled.")


class ScanoramaWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, gate, layer, batch_column, embedding_to_integrate, integrated_embedding_name, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.gate = gate
        self.layer = layer
        self.batch_column = batch_column
        self.embedding_to_integrate = embedding_to_integrate
        self.integrated_embedding_name = integrated_embedding_name
        self.advanced_kwargs = advanced_kwargs
        self._is_running = True
        self._mutex = QMutex()

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Scanorama integration was canceled.")
                    return

            fp.tl.scanorama_integrate(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                key=self.batch_column,
                basis=self.embedding_to_integrate,
                adjusted_basis=self.integrated_embedding_name,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        self._is_running = False


class ScanoramaWindow(BaseIntegrationWindow):
    def __init__(self, main_window):
        advanced_params = {
            "knn": 20,
            "sigma": 15,
            "approx": True,
            "alpha": 0.10,
            "batch_size": 5000,
        }
        super().__init__(main_window, "Scanorama Integration", advanced_params)
        self.scanorama_worker = None
        self.calculation_canceled = False

    def calculate_integration(self):
        """
        Performs the Scanorama integration with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            gate = self.gate_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            batch_column = self.batch_column_dropdown.currentText()
            embedding_to_integrate = self.embedding_dropdown.currentText()
            integrated_embedding_name = self.integrated_embedding_input.text()

            # Collect advanced parameters
            advanced_kwargs = {}
            for param, default in self.advanced_params.items():
                input_field = getattr(self, f"{param}_input")
                value = input_field.text() or str(default)
                if value.lower() == "none":
                    advanced_kwargs[param] = None
                elif value.lower() == "true":
                    advanced_kwargs[param] = True
                elif value.lower() == "false":
                    advanced_kwargs[param] = False
                else:
                    try:
                        advanced_kwargs[param] = float(value) if '.' in value else int(value)
                    except ValueError:
                        advanced_kwargs[param] = value

            # Show loading screen
            loading_message = "Calculating Scanorama Integration...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the Scanorama worker thread
            self.calculation_canceled = False
            self.scanorama_worker = ScanoramaWorker(
                dataset, gate, layer, batch_column, embedding_to_integrate, integrated_embedding_name, advanced_kwargs
            )
            self.scanorama_worker.finished.connect(self.on_integration_finished)
            self.scanorama_worker.error.connect(self.on_integration_error)
            self.scanorama_worker.start()

        except Exception as e:
            self.show_error("Scanorama Integration Error", str(e))

    def on_integration_finished(self):
        """
        Handles the completion of the Scanorama integration.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Scanorama integration completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_integration_error(self, error_message):
        """
        Handles any error that occurs during the Scanorama integration.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Scanorama Integration Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.scanorama_worker:
            self.scanorama_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Scanorama integration has been cancelled.")

