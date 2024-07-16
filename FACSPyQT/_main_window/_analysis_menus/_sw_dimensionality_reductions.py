from PyQt5.QtWidgets import (QMessageBox, QWidget, QVBoxLayout, 
                             QPushButton, QFormLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox,
                             QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QMutex, QMutexLocker

import FACSPy as fp

from .._utils import LoadingScreen, MultiSelectComboBox
from ._analysis_menu import BaseAnalysisMenu


class BaseSamplewiseDimensionalityReductionWindow(BaseAnalysisMenu):
    def __init__(self, main_window, title, advanced_params):
        super().__init__(main_window, title, advanced_params)

        # Main layout
        self.main_layout = QVBoxLayout()

        # Form layout for global options
        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        # Data metric
        self.data_metric_label = QLabel("Data metric:")
        self.data_metric_dropdown = QComboBox()
        self.data_metric_dropdown.addItems(["mfi", "fop"])
        self.form_layout.addRow(self.data_metric_label, self.data_metric_dropdown)

        # Data format
        self.data_format_label = QLabel("Data format:")
        self.data_format_dropdown = QComboBox()
        self.form_layout.addRow(self.data_format_label, self.data_format_dropdown)

        # Use marker channels only
        self.use_marker_label = QLabel("Use marker channels only:")
        self.use_marker_dropdown = QComboBox()
        self.use_marker_dropdown.addItems(["True", "False"])
        self.form_layout.addRow(self.use_marker_label, self.use_marker_dropdown)

        # Exclude channels
        self.exclude_channels_label = QLabel("Exclude channels:")
        self.exclude_channels_dropdown = MultiSelectComboBox()
        self.form_layout.addRow(self.exclude_channels_label, self.exclude_channels_dropdown)

        # Scaling
        self.scaling_label = QLabel("Scale data:")
        self.scaling_dropdown = QComboBox()
        self.scaling_dropdown.addItems(["MinMaxScaler", "StandardScaler", "RobustScaler", "None"])
        self.form_layout.addRow(self.scaling_label, self.scaling_dropdown)

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

        # Transform button
        self.calculate_button = QPushButton(f"Calculate samplewise {title.split()[0]}")
        self.calculate_button.clicked.connect(self.calculate_dimensionality_reduction)
        self.main_layout.addWidget(self.calculate_button)

        self.setLayout(self.main_layout)

        self.finalize_window_layout()

    def calculate_dimensionality_reduction(self):
        """
        Should be overridden in subclasses to perform the dimensionality reduction.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def populate_dropdowns(self):
        """
        Populates the dropdowns with dataset-specific values.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            self.data_format_dropdown.clear()
            self.data_format_dropdown.addItems(dataset.layers.keys())

            self.exclude_channels_dropdown.addItems(dataset.var.index.to_list())
        except Exception as e:
            self.show_error("Dropdown Population Error", str(e))


class SamplewisePCAWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.data_metric = data_metric
        self.layer = layer
        self.use_only_fluo = use_only_fluo
        self.scaling = scaling
        self.exclude_channels = exclude_channels
        self.advanced_kwargs = advanced_kwargs
        self._is_running = True
        self._mutex = QMutex()  # Mutex for thread-safe flag

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Samplewise PCA calculation was canceled.")
                    return

            fp.tl.pca_samplewise(
                self.dataset,
                data_metric=self.data_metric,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                exclude=self.exclude_channels,
                scaling=self.scaling,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class SamplewisePCAWindow(BaseSamplewiseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Samplewise PCA", ["n_components", "whiten", "svd_solver", "tol", "iterated_power", "n_oversamples", "power_iteration_normalizer", "random_state"])

        self.pca_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to PCA.
        """
        self.n_components_label = QLabel("Number of components (n_components):")
        self.n_components_input = QLineEdit()
        self.n_components_input.setPlaceholderText("e.g., 10")

        self.whiten_label = QLabel("Whiten:")
        self.whiten_input = QComboBox()
        self.whiten_input.addItems(["True", "False"])

        self.svd_solver_label = QLabel("SVD Solver:")
        self.svd_solver_input = QComboBox()
        self.svd_solver_input.addItems(["auto", "full", "arpack", "randomized"])

        self.tol_label = QLabel("Tolerance (tol):")
        self.tol_input = QLineEdit()
        self.tol_input.setPlaceholderText("e.g., 0.0")

        self.iterated_power_label = QLabel("Iterated Power:")
        self.iterated_power_input = QLineEdit()
        self.iterated_power_input.setPlaceholderText("e.g., auto")

        self.n_oversamples_label = QLabel("Number of Oversamples:")
        self.n_oversamples_input = QLineEdit()
        self.n_oversamples_input.setPlaceholderText("e.g., 10")

        self.power_iteration_normalizer_label = QLabel("Power Iteration Normalizer:")
        self.power_iteration_normalizer_input = QLineEdit()
        self.power_iteration_normalizer_input.setPlaceholderText("e.g., auto")

        self.random_state_label = QLabel("Random State:")
        self.random_state_input = QLineEdit()
        self.random_state_input.setPlaceholderText("e.g., None")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.n_components_label, self.n_components_input)
        self.advanced_settings_layout.addRow(self.whiten_label, self.whiten_input)
        self.advanced_settings_layout.addRow(self.svd_solver_label, self.svd_solver_input)
        self.advanced_settings_layout.addRow(self.tol_label, self.tol_input)
        self.advanced_settings_layout.addRow(self.iterated_power_label, self.iterated_power_input)
        self.advanced_settings_layout.addRow(self.n_oversamples_label, self.n_oversamples_input)
        self.advanced_settings_layout.addRow(self.power_iteration_normalizer_label, self.power_iteration_normalizer_input)
        self.advanced_settings_layout.addRow(self.random_state_label, self.random_state_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the PCA calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            data_metric = self.data_metric_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'n_components': int(self.n_components_input.text()) if self.n_components_input.text() else 3,
                'whiten': self.whiten_input.currentText() == "True",
                'svd_solver': self.svd_solver_input.currentText() if self.svd_solver_input.currentText() else 'auto',
                'tol': float(self.tol_input.text()) if self.tol_input.text() else 0.0,
                'iterated_power': self.iterated_power_input.text() if self.iterated_power_input.text() else 'auto',
                'n_oversamples': int(self.n_oversamples_input.text()) if self.n_oversamples_input.text() else 10,
                'power_iteration_normalizer': self.power_iteration_normalizer_input.text() if self.power_iteration_normalizer_input.text() else 'auto',
                'random_state': None if not self.random_state_input.text() or self.random_state_input.text().lower() == "none" else int(self.random_state_input.text())
            }

            # Show loading screen
            loading_message = "Calculating samplewise PCA...\n\n"
            loading_message += f"Data metric: {data_metric}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the PCA worker thread
            self.calculation_canceled = False
            self.pca_worker = SamplewisePCAWorker(dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.pca_worker.finished.connect(self.on_pca_finished)
            self.pca_worker.error.connect(self.on_pca_error)
            self.pca_worker.start()

        except Exception as e:
            self.show_error("PCA Calculation Error", str(e))

    def on_pca_finished(self):
        """
        Handles the completion of the PCA calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Samplewise PCA calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_pca_error(self, error_message):
        """
        Handles any error that occurs during the PCA calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("PCA Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.pca_worker:
            self.pca_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Samplewise PCA calculation has been cancelled.")

class SamplewiseMDSWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.data_metric = data_metric
        self.layer = layer
        self.use_only_fluo = use_only_fluo
        self.scaling = scaling
        self.exclude_channels = exclude_channels
        self.advanced_kwargs = advanced_kwargs
        self._is_running = True
        self._mutex = QMutex()  # Mutex for thread-safe flag

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Samplewise MDS calculation was canceled.")
                    return

            fp.tl.mds_samplewise(
                self.dataset,
                data_metric=self.data_metric,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                exclude=self.exclude_channels,
                scaling=self.scaling,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class SamplewiseMDSWindow(BaseSamplewiseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "MDS", [
            "metric", "n_init", "max_iter", "verbose", "eps", 
            "n_jobs", "random_state", "dissimilarity", "normalized_stress", "n_components"
        ])

        self.mds_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to MDS.
        """
        self.metric_label = QLabel("Metric:")
        self.metric_input = QComboBox()
        self.metric_input.addItems(["True", "False"])

        self.n_init_label = QLabel("Number of initializations (n_init):")
        self.n_init_input = QLineEdit()
        self.n_init_input.setPlaceholderText("e.g., 4")

        self.max_iter_label = QLabel("Maximum iterations (max_iter):")
        self.max_iter_input = QLineEdit()
        self.max_iter_input.setPlaceholderText("e.g., 300")

        self.verbose_label = QLabel("Verbosity (verbose):")
        self.verbose_input = QLineEdit()
        self.verbose_input.setPlaceholderText("e.g., 0")

        self.eps_label = QLabel("Epsilon (eps):")
        self.eps_input = QLineEdit()
        self.eps_input.setPlaceholderText("e.g., 0.001")

        self.n_jobs_label = QLabel("Number of jobs (n_jobs):")
        self.n_jobs_input = QLineEdit()
        self.n_jobs_input.setPlaceholderText("e.g., None")

        self.random_state_label = QLabel("Random state:")
        self.random_state_input = QLineEdit()
        self.random_state_input.setPlaceholderText("e.g., None")

        self.dissimilarity_label = QLabel("Dissimilarity:")
        self.dissimilarity_input = QComboBox()
        self.dissimilarity_input.addItems(["euclidean", "precomputed"])

        self.normalized_stress_label = QLabel("Normalized Stress:")
        self.normalized_stress_input = QLineEdit()
        self.normalized_stress_input.setPlaceholderText("e.g., auto")

        self.n_components_label = QLabel("Number of components (n_components):")
        self.n_components_input = QLineEdit()
        self.n_components_input.setPlaceholderText("e.g., 3")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.metric_label, self.metric_input)
        self.advanced_settings_layout.addRow(self.n_init_label, self.n_init_input)
        self.advanced_settings_layout.addRow(self.max_iter_label, self.max_iter_input)
        self.advanced_settings_layout.addRow(self.verbose_label, self.verbose_input)
        self.advanced_settings_layout.addRow(self.eps_label, self.eps_input)
        self.advanced_settings_layout.addRow(self.n_jobs_label, self.n_jobs_input)
        self.advanced_settings_layout.addRow(self.random_state_label, self.random_state_input)
        self.advanced_settings_layout.addRow(self.dissimilarity_label, self.dissimilarity_input)
        self.advanced_settings_layout.addRow(self.normalized_stress_label, self.normalized_stress_input)
        self.advanced_settings_layout.addRow(self.n_components_label, self.n_components_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the MDS calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            data_metric = self.data_metric_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'metric': self.metric_input.currentText() == "True",
                'n_init': int(self.n_init_input.text()) if self.n_init_input.text() else 4,
                'max_iter': int(self.max_iter_input.text()) if self.max_iter_input.text() else 300,
                'verbose': int(self.verbose_input.text()) if self.verbose_input.text() else 0,
                'eps': float(self.eps_input.text()) if self.eps_input.text() else 0.001,
                'n_jobs': None if not self.n_jobs_input.text() or self.n_jobs_input.text().lower() == "none" else int(self.n_jobs_input.text()),
                'random_state': None if not self.random_state_input.text() or self.random_state_input.text().lower() == "none" else int(self.random_state_input.text()),
                'dissimilarity': self.dissimilarity_input.currentText() if self.dissimilarity_input.currentText() else 'euclidean',
                'normalized_stress': self.normalized_stress_input.text() if self.normalized_stress_input.text() else 'auto',
                'n_components': int(self.n_components_input.text()) if self.n_components_input.text() else 3
            }

            # Show loading screen
            loading_message = "Calculating samplewise MDS...\n\n"
            loading_message += f"Data metric: {data_metric}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the MDS worker thread
            self.calculation_canceled = False
            self.mds_worker = SamplewiseMDSWorker(dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.mds_worker.finished.connect(self.on_mds_finished)
            self.mds_worker.error.connect(self.on_mds_error)
            self.mds_worker.start()

        except Exception as e:
            self.show_error("MDS Calculation Error", str(e))

    def on_mds_finished(self):
        """
        Handles the completion of the MDS calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Samplewise MDS calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_mds_error(self, error_message):
        """
        Handles any error that occurs during the MDS calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("MDS Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.mds_worker:
            self.mds_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Samplewise MDS calculation has been cancelled.")

class SamplewiseUMAPWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.data_metric = data_metric
        self.layer = layer
        self.use_only_fluo = use_only_fluo
        self.scaling = scaling
        self.exclude_channels = exclude_channels
        self.advanced_kwargs = advanced_kwargs
        self._is_running = True
        self._mutex = QMutex()  # Mutex for thread-safe flag

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Samplewise UMAP calculation was canceled.")
                    return

            fp.tl.umap_samplewise(
                self.dataset,
                data_metric=self.data_metric,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                exclude=self.exclude_channels,
                scaling=self.scaling,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False



class SamplewiseUMAPWindow(BaseSamplewiseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "UMAP", [
            "n_neighbors", "n_components", "metric", "output_metric", "n_epochs",
            "learning_rate", "init", "min_dist", "spread", "low_memory",
            "n_jobs", "set_op_mix_ratio", "local_connectivity", "repulsion_strength",
            "negative_sample_rate", "transform_queue_size", "a", "b"
        ])

        self.umap_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to UMAP.
        """
        self.n_neighbors_label = QLabel("Number of neighbors (n_neighbors):")
        self.n_neighbors_input = QLineEdit()
        self.n_neighbors_input.setPlaceholderText("e.g., 15")

        self.n_components_label = QLabel("Number of components (n_components):")
        self.n_components_input = QLineEdit()
        self.n_components_input.setPlaceholderText("e.g., 3")

        self.metric_label = QLabel("Metric:")
        self.metric_input = QLineEdit()
        self.metric_input.setPlaceholderText("e.g., euclidean")

        self.output_metric_label = QLabel("Output Metric:")
        self.output_metric_input = QLineEdit()
        self.output_metric_input.setPlaceholderText("e.g., euclidean")

        self.n_epochs_label = QLabel("Number of epochs (n_epochs):")
        self.n_epochs_input = QLineEdit()
        self.n_epochs_input.setPlaceholderText("e.g., None")

        self.learning_rate_label = QLabel("Learning rate (learning_rate):")
        self.learning_rate_input = QLineEdit()
        self.learning_rate_input.setPlaceholderText("e.g., 1.0")

        self.init_label = QLabel("Initialization method (init):")
        self.init_input = QLineEdit()
        self.init_input.setPlaceholderText("e.g., spectral")

        self.min_dist_label = QLabel("Minimum distance (min_dist):")
        self.min_dist_input = QLineEdit()
        self.min_dist_input.setPlaceholderText("e.g., 0.1")

        self.spread_label = QLabel("Spread:")
        self.spread_input = QLineEdit()
        self.spread_input.setPlaceholderText("e.g., 1.0")

        self.low_memory_label = QLabel("Low memory:")
        self.low_memory_input = QComboBox()
        self.low_memory_input.addItems(["True", "False"])

        self.n_jobs_label = QLabel("Number of jobs (n_jobs):")
        self.n_jobs_input = QLineEdit()
        self.n_jobs_input.setPlaceholderText("e.g., -1")

        self.set_op_mix_ratio_label = QLabel("Set operation mix ratio (set_op_mix_ratio):")
        self.set_op_mix_ratio_input = QLineEdit()
        self.set_op_mix_ratio_input.setPlaceholderText("e.g., 1.0")

        self.local_connectivity_label = QLabel("Local connectivity (local_connectivity):")
        self.local_connectivity_input = QLineEdit()
        self.local_connectivity_input.setPlaceholderText("e.g., 1.0")

        self.repulsion_strength_label = QLabel("Repulsion strength (repulsion_strength):")
        self.repulsion_strength_input = QLineEdit()
        self.repulsion_strength_input.setPlaceholderText("e.g., 1.0")

        self.negative_sample_rate_label = QLabel("Negative sample rate (negative_sample_rate):")
        self.negative_sample_rate_input = QLineEdit()
        self.negative_sample_rate_input.setPlaceholderText("e.g., 5")

        self.transform_queue_size_label = QLabel("Transform queue size (transform_queue_size):")
        self.transform_queue_size_input = QLineEdit()
        self.transform_queue_size_input.setPlaceholderText("e.g., 4.0")

        self.a_label = QLabel("Parameter a:")
        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("e.g., None")

        self.b_label = QLabel("Parameter b:")
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("e.g., None")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.n_neighbors_label, self.n_neighbors_input)
        self.advanced_settings_layout.addRow(self.n_components_label, self.n_components_input)
        self.advanced_settings_layout.addRow(self.metric_label, self.metric_input)
        self.advanced_settings_layout.addRow(self.output_metric_label, self.output_metric_input)
        self.advanced_settings_layout.addRow(self.n_epochs_label, self.n_epochs_input)
        self.advanced_settings_layout.addRow(self.learning_rate_label, self.learning_rate_input)
        self.advanced_settings_layout.addRow(self.init_label, self.init_input)
        self.advanced_settings_layout.addRow(self.min_dist_label, self.min_dist_input)
        self.advanced_settings_layout.addRow(self.spread_label, self.spread_input)
        self.advanced_settings_layout.addRow(self.low_memory_label, self.low_memory_input)
        self.advanced_settings_layout.addRow(self.n_jobs_label, self.n_jobs_input)
        self.advanced_settings_layout.addRow(self.set_op_mix_ratio_label, self.set_op_mix_ratio_input)
        self.advanced_settings_layout.addRow(self.local_connectivity_label, self.local_connectivity_input)
        self.advanced_settings_layout.addRow(self.repulsion_strength_label, self.repulsion_strength_input)
        self.advanced_settings_layout.addRow(self.negative_sample_rate_label, self.negative_sample_rate_input)
        self.advanced_settings_layout.addRow(self.transform_queue_size_label, self.transform_queue_size_input)
        self.advanced_settings_layout.addRow(self.a_label, self.a_input)
        self.advanced_settings_layout.addRow(self.b_label, self.b_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the UMAP calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            data_metric = self.data_metric_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'n_neighbors': int(self.n_neighbors_input.text()) if self.n_neighbors_input.text() else 15,
                'n_components': int(self.n_components_input.text()) if self.n_components_input.text() else 3,
                'metric': self.metric_input.text() if self.metric_input.text() else "euclidean",
                'output_metric': self.output_metric_input.text() if self.output_metric_input.text() else "euclidean",
                'n_epochs': None if not self.n_epochs_input.text() or self.n_epochs_input.text().lower() == "none" else int(self.n_epochs_input.text()),
                'learning_rate': float(self.learning_rate_input.text()) if self.learning_rate_input.text() else 1.0,
                'init': self.init_input.text() if self.init_input.text() else "spectral",
                'min_dist': float(self.min_dist_input.text()) if self.min_dist_input.text() else 0.1,
                'spread': float(self.spread_input.text()) if self.spread_input.text() else 1.0,
                'low_memory': self.low_memory_input.currentText() == "True",
                'n_jobs': int(self.n_jobs_input.text()) if self.n_jobs_input.text() else -1,
                'set_op_mix_ratio': float(self.set_op_mix_ratio_input.text()) if self.set_op_mix_ratio_input.text() else 1.0,
                'local_connectivity': float(self.local_connectivity_input.text()) if self.local_connectivity_input.text() else 1.0,
                'repulsion_strength': float(self.repulsion_strength_input.text()) if self.repulsion_strength_input.text() else 1.0,
                'negative_sample_rate': int(self.negative_sample_rate_input.text()) if self.negative_sample_rate_input.text() else 5,
                'transform_queue_size': float(self.transform_queue_size_input.text()) if self.transform_queue_size_input.text() else 4.0,
                'a': None if not self.a_input.text() or self.a_input.text().lower() == "none" else float(self.a_input.text()),
                'b': None if not self.b_input.text() or self.b_input.text().lower() == "none" else float(self.b_input.text())
            }

            # Show loading screen
            loading_message = "Calculating samplewise UMAP...\n\n"
            loading_message += f"Data metric: {data_metric}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the UMAP worker thread
            self.calculation_canceled = False
            self.umap_worker = SamplewiseUMAPWorker(dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.umap_worker.finished.connect(self.on_umap_finished)
            self.umap_worker.error.connect(self.on_umap_error)
            self.umap_worker.start()

        except Exception as e:
            self.show_error("UMAP Calculation Error", str(e))

    def on_umap_finished(self):
        """
        Handles the completion of the UMAP calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Samplewise UMAP calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_umap_error(self, error_message):
        """
        Handles any error that occurs during the UMAP calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("UMAP Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.umap_worker:
            self.umap_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Samplewise UMAP calculation has been cancelled.")


class SamplewiseTSNEWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.data_metric = data_metric
        self.layer = layer
        self.use_only_fluo = use_only_fluo
        self.scaling = scaling
        self.exclude_channels = exclude_channels
        self.advanced_kwargs = advanced_kwargs
        self._is_running = True
        self._mutex = QMutex()  # Mutex for thread-safe flag

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Samplewise t-SNE calculation was canceled.")
                    return

            fp.tl.tsne_samplewise(
                self.dataset,
                data_metric=self.data_metric,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                exclude=self.exclude_channels,
                scaling=self.scaling,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class SamplewiseTSNEWindow(BaseSamplewiseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "t-SNE", [
            "n_components", "perplexity", "early_exaggeration", "learning_rate",
            "max_iter", "n_iter_without_progress", "min_grad_norm", "metric",
            "metric_params", "init", "verbose", "random_state", "method", "angle", "n_jobs"
        ])

        self.tsne_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to t-SNE.
        """
        self.n_components_label = QLabel("Number of components (n_components):")
        self.n_components_input = QLineEdit()
        self.n_components_input.setPlaceholderText("e.g., 2")

        self.perplexity_label = QLabel("Perplexity:")
        self.perplexity_input = QLineEdit()
        self.perplexity_input.setPlaceholderText("e.g., 30.0")

        self.early_exaggeration_label = QLabel("Early exaggeration:")
        self.early_exaggeration_input = QLineEdit()
        self.early_exaggeration_input.setPlaceholderText("e.g., 12.0")

        self.learning_rate_label = QLabel("Learning rate (learning_rate):")
        self.learning_rate_input = QLineEdit()
        self.learning_rate_input.setPlaceholderText("e.g., auto")

        self.max_iter_label = QLabel("Max iterations (max_iter):")
        self.max_iter_input = QLineEdit()
        self.max_iter_input.setPlaceholderText("e.g., None")

        self.n_iter_without_progress_label = QLabel("N iterations without progress (n_iter_without_progress):")
        self.n_iter_without_progress_input = QLineEdit()
        self.n_iter_without_progress_input.setPlaceholderText("e.g., 300")

        self.min_grad_norm_label = QLabel("Min gradient norm (min_grad_norm):")
        self.min_grad_norm_input = QLineEdit()
        self.min_grad_norm_input.setPlaceholderText("e.g., 1e-7")

        self.metric_label = QLabel("Metric:")
        self.metric_input = QLineEdit()
        self.metric_input.setPlaceholderText("e.g., euclidean")

        self.metric_params_label = QLabel("Metric params (metric_params):")
        self.metric_params_input = QLineEdit()
        self.metric_params_input.setPlaceholderText("e.g., None")

        self.init_label = QLabel("Initialization (init):")
        self.init_input = QLineEdit()
        self.init_input.setPlaceholderText("e.g., pca")

        self.verbose_label = QLabel("Verbose:")
        self.verbose_input = QLineEdit()
        self.verbose_input.setPlaceholderText("e.g., 0")

        self.random_state_label = QLabel("Random state:")
        self.random_state_input = QLineEdit()
        self.random_state_input.setPlaceholderText("e.g., None")

        self.method_label = QLabel("Method:")
        self.method_input = QLineEdit()
        self.method_input.setPlaceholderText("e.g., barnes_hut")

        self.angle_label = QLabel("Angle:")
        self.angle_input = QLineEdit()
        self.angle_input.setPlaceholderText("e.g., 0.5")

        self.n_jobs_label = QLabel("Number of jobs (n_jobs):")
        self.n_jobs_input = QLineEdit()
        self.n_jobs_input.setPlaceholderText("e.g., None")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.n_components_label, self.n_components_input)
        self.advanced_settings_layout.addRow(self.perplexity_label, self.perplexity_input)
        self.advanced_settings_layout.addRow(self.early_exaggeration_label, self.early_exaggeration_input)
        self.advanced_settings_layout.addRow(self.learning_rate_label, self.learning_rate_input)
        self.advanced_settings_layout.addRow(self.max_iter_label, self.max_iter_input)
        self.advanced_settings_layout.addRow(self.n_iter_without_progress_label, self.n_iter_without_progress_input)
        self.advanced_settings_layout.addRow(self.min_grad_norm_label, self.min_grad_norm_input)
        self.advanced_settings_layout.addRow(self.metric_label, self.metric_input)
        self.advanced_settings_layout.addRow(self.metric_params_label, self.metric_params_input)
        self.advanced_settings_layout.addRow(self.init_label, self.init_input)
        self.advanced_settings_layout.addRow(self.verbose_label, self.verbose_input)
        self.advanced_settings_layout.addRow(self.random_state_label, self.random_state_input)
        self.advanced_settings_layout.addRow(self.method_label, self.method_input)
        self.advanced_settings_layout.addRow(self.angle_label, self.angle_input)
        self.advanced_settings_layout.addRow(self.n_jobs_label, self.n_jobs_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the t-SNE calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            data_metric = self.data_metric_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'n_components': int(self.n_components_input.text()) if self.n_components_input.text() else 2,
                'perplexity': float(self.perplexity_input.text()) if self.perplexity_input.text() else 30.0,
                'early_exaggeration': float(self.early_exaggeration_input.text()) if self.early_exaggeration_input.text() else 12.0,
                'learning_rate': self.learning_rate_input.text() if self.learning_rate_input.text() else 'auto',
                'max_iter': None if not self.max_iter_input.text() or self.max_iter_input.text().lower() == "none" else int(self.max_iter_input.text()),
                'n_iter_without_progress': int(self.n_iter_without_progress_input.text()) if self.n_iter_without_progress_input.text() else 300,
                'min_grad_norm': float(self.min_grad_norm_input.text()) if self.min_grad_norm_input.text() else 1e-07,
                'metric': self.metric_input.text() if self.metric_input.text() else 'euclidean',
                'metric_params': None if not self.metric_params_input.text() or self.metric_params_input.text().lower() == "none" else self.metric_params_input.text(),
                'init': self.init_input.text() if self.init_input.text() else 'pca',
                'verbose': int(self.verbose_input.text()) if self.verbose_input.text() else 0,
                'random_state': None if not self.random_state_input.text() or self.random_state_input.text().lower() == "none" else int(self.random_state_input.text()),
                'method': self.method_input.text() if self.method_input.text() else 'barnes_hut',
                'angle': float(self.angle_input.text()) if self.angle_input.text() else 0.5,
                'n_jobs': None if not self.n_jobs_input.text() or self.n_jobs_input.text().lower() == "none" else int(self.n_jobs_input.text())
            }

            # Show loading screen
            loading_message = "Calculating samplewise t-SNE...\n\n"
            loading_message += f"Data metric: {data_metric}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the t-SNE worker thread
            self.calculation_canceled = False
            self.tsne_worker = SamplewiseTSNEWorker(dataset, data_metric, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.tsne_worker.finished.connect(self.on_tsne_finished)
            self.tsne_worker.error.connect(self.on_tsne_error)
            self.tsne_worker.start()

        except Exception as e:
            self.show_error("t-SNE Calculation Error", str(e))

    def on_tsne_finished(self):
        """
        Handles the completion of the t-SNE calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Samplewise t-SNE calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_tsne_error(self, error_message):
        """
        Handles any error that occurs during the t-SNE calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("t-SNE Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.tsne_worker:
            self.tsne_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Samplewise t-SNE calculation has been cancelled.")

