from PyQt5.QtWidgets import (QMessageBox, QVBoxLayout, 
                             QPushButton, QFormLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox,
                             QGroupBox)
from PyQt5.QtCore import pyqtSignal, QThread, QMutex, QMutexLocker

import FACSPy as fp

from .._utils import LoadingScreen, MultiSelectComboBox

from ._analysis_menu import BaseAnalysisMenu

class BaseClusteringWindow(BaseAnalysisMenu):
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

        # Use marker channels only
        self.use_marker_label = QLabel("Use marker channels only:")
        self.use_marker_dropdown = QComboBox()
        self.use_marker_dropdown.addItems(["True", "False"])
        self.form_layout.addRow(self.use_marker_label, self.use_marker_dropdown)

        # Exclude channels using MultiSelectComboBox
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

        # Calculate button
        self.calculate_button = QPushButton(f"Calculate {title.split()[0]}")
        self.calculate_button.clicked.connect(self.calculate_dimensionality_reduction)
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

            # Populate exclude channels dropdown
            self.exclude_channels_dropdown.clear()
            self.exclude_channels_dropdown.addItems(dataset.var.index.tolist())

        except Exception as e:
            self.show_error("Dropdown Population Error", str(e))

    def calculate_dimensionality_reduction(self):
        """
        Should be overridden in subclasses to perform the specific dimensionality reduction calculation.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class LeidenWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.gate = gate
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
                    self.error.emit("Leiden clustering calculation was canceled.")
                    return

            fp.tl.leiden(
                self.dataset,
                gate=self.gate,
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

class LeidenWindow(BaseClusteringWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Leiden", {
            "resolution": 1.0,
            "directed": "True",
            "use_weights": "True",
            "n_iterations": -1
        })

        self.leiden_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to Leiden clustering.
        """
        self.resolution_label = QLabel("Resolution:")
        self.resolution_input = QLineEdit()
        self.resolution_input.setPlaceholderText("e.g., 1.0")

        self.directed_label = QLabel("Directed:")
        self.directed_input = QComboBox()
        self.directed_input.addItems(["True", "False"])

        self.use_weights_label = QLabel("Use weights:")
        self.use_weights_input = QComboBox()
        self.use_weights_input.addItems(["True", "False"])

        self.n_iterations_label = QLabel("Number of iterations (n_iterations):")
        self.n_iterations_input = QLineEdit()
        self.n_iterations_input.setPlaceholderText("e.g., -1")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.resolution_label, self.resolution_input)
        self.advanced_settings_layout.addRow(self.directed_label, self.directed_input)
        self.advanced_settings_layout.addRow(self.use_weights_label, self.use_weights_input)
        self.advanced_settings_layout.addRow(self.n_iterations_label, self.n_iterations_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the Leiden clustering calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            gate = self.gate_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()
            if scaling == "None":
                scaling = None

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'resolution': float(self.resolution_input.text()) if self.resolution_input.text() else 1.0,
                'directed': self.directed_input.currentText() == "True",
                'use_weights': self.use_weights_input.currentText() == "True",
                'n_iterations': int(self.n_iterations_input.text()) if self.n_iterations_input.text() else -1
            }

            # Show loading screen
            loading_message = "Calculating Leiden clustering...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the Leiden worker thread
            self.calculation_canceled = False
            self.leiden_worker = LeidenWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.leiden_worker.finished.connect(self.on_leiden_finished)
            self.leiden_worker.error.connect(self.on_leiden_error)
            self.leiden_worker.start()

        except Exception as e:
            self.show_error("Leiden Calculation Error", str(e))

    def on_leiden_finished(self):
        """
        Handles the completion of the Leiden clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Leiden clustering completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_leiden_error(self, error_message):
        """
        Handles any error that occurs during the Leiden clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Leiden Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.leiden_worker:
            self.leiden_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Leiden clustering calculation has been cancelled.")


class FlowsomWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.gate = gate
        self.layer = layer
        self.use_only_fluo = use_only_fluo
        self.scaling = scaling
        self.exclude_channels = exclude_channels
        self.advanced_kwargs = advanced_kwargs
        self._is_running = True
        self._mutex = QMutex()  # Mutex for thread-safe flag

    def run(self):
        import traceback
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("FlowSOM clustering calculation was canceled.")
                    return
            print("running flowsom")
            print(self.dataset)
            print(self.gate)
            print(self.layer)
            print(self.use_only_fluo)
            print(self.exclude_channels)
            print(self.scaling)
            fp.tl.flowsom(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                exclude=self.exclude_channels,
                scaling=self.scaling,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            print(traceback.format_exc())
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False

class FlowsomWindow(BaseClusteringWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "FlowSOM", {
            "xdim": 10,
            "ydim": 10,
            "rlen": 10,
            "mst": 1,
            "alpha": "(0.05, 0.01)",
            "init": "False",
            "initf": "None",
            "n_clusters": 30,
            "K": "None",
            "H": 100,
            "resample_proportion": 0.9,
            "linkage": "average"
        })

        self.flowsom_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to FlowSOM clustering.
        """
        self.xdim_label = QLabel("X dimension (xdim):")
        self.xdim_input = QLineEdit()
        self.xdim_input.setPlaceholderText("e.g., 10")

        self.ydim_label = QLabel("Y dimension (ydim):")
        self.ydim_input = QLineEdit()
        self.ydim_input.setPlaceholderText("e.g., 10")

        self.rlen_label = QLabel("Rlen:")
        self.rlen_input = QLineEdit()
        self.rlen_input.setPlaceholderText("e.g., 10")

        self.mst_label = QLabel("MST:")
        self.mst_input = QComboBox()
        self.mst_input.addItems(["True", "False"])

        self.alpha_label = QLabel("Alpha:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setPlaceholderText("e.g., (0.05, 0.01)")

        self.init_label = QLabel("Initialize (init):")
        self.init_input = QComboBox()
        self.init_input.addItems(["True", "False"])
        self.init_input.setCurrentText("False")

        self.initf_label = QLabel("Initf:")
        self.initf_input = QLineEdit()
        self.initf_input.setPlaceholderText("e.g., None")

        self.n_clusters_label = QLabel("Number of clusters (n_clusters):")
        self.n_clusters_input = QLineEdit()
        self.n_clusters_input.setPlaceholderText("e.g., 30")

        self.K_label = QLabel("K:")
        self.K_input = QLineEdit()
        self.K_input.setPlaceholderText("e.g., None")

        self.H_label = QLabel("H:")
        self.H_input = QLineEdit()
        self.H_input.setPlaceholderText("e.g., 100")

        self.resample_proportion_label = QLabel("Resample proportion:")
        self.resample_proportion_input = QLineEdit()
        self.resample_proportion_input.setPlaceholderText("e.g., 0.9")

        self.linkage_label = QLabel("Linkage:")
        self.linkage_input = QComboBox()
        self.linkage_input.addItems(["average", "complete", "single", "ward"])

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.xdim_label, self.xdim_input)
        self.advanced_settings_layout.addRow(self.ydim_label, self.ydim_input)
        self.advanced_settings_layout.addRow(self.rlen_label, self.rlen_input)
        self.advanced_settings_layout.addRow(self.mst_label, self.mst_input)
        self.advanced_settings_layout.addRow(self.alpha_label, self.alpha_input)
        self.advanced_settings_layout.addRow(self.init_label, self.init_input)
        self.advanced_settings_layout.addRow(self.initf_label, self.initf_input)
        self.advanced_settings_layout.addRow(self.n_clusters_label, self.n_clusters_input)
        self.advanced_settings_layout.addRow(self.K_label, self.K_input)
        self.advanced_settings_layout.addRow(self.H_label, self.H_input)
        self.advanced_settings_layout.addRow(self.resample_proportion_label, self.resample_proportion_input)
        self.advanced_settings_layout.addRow(self.linkage_label, self.linkage_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the FlowSOM clustering calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            gate = self.gate_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()
            if scaling == "None":
                scaling = None

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'xdim': int(self.xdim_input.text()) if self.xdim_input.text() else 10,
                'ydim': int(self.ydim_input.text()) if self.ydim_input.text() else 10,
                'rlen': int(self.rlen_input.text()) if self.rlen_input.text() else 10,
                'mst': self.mst_input.currentText() == "True",
                'alpha': eval(self.alpha_input.text()) if self.alpha_input.text() else (0.05, 0.01),  # Convert text to tuple
                'init': self.init_input.currentText() == "True",
                'initf': self.initf_input.text() if self.initf_input.text() else None,
                'n_clusters': int(self.n_clusters_input.text()) if self.n_clusters_input.text() else 30,
                'K': int(self.K_input.text()) if self.K_input.text() else None,
                'H': int(self.H_input.text()) if self.H_input.text() else 100,
                'resample_proportion': float(self.resample_proportion_input.text()) if self.resample_proportion_input.text() else 0.9,
                'linkage': self.linkage_input.currentText() if self.linkage_input.currentText() else "average"
            }

            # Show loading screen
            loading_message = "Calculating FlowSOM clustering...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the FlowSOM worker thread
            self.calculation_canceled = False
            self.flowsom_worker = FlowsomWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.flowsom_worker.finished.connect(self.on_flowsom_finished)
            self.flowsom_worker.error.connect(self.on_flowsom_error)
            self.flowsom_worker.start()

        except Exception as e:
            self.show_error("FlowSOM Calculation Error", str(e))

    def on_flowsom_finished(self):
        """
        Handles the completion of the FlowSOM clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "FlowSOM clustering completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_flowsom_error(self, error_message):
        """
        Handles any error that occurs during the FlowSOM clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("FlowSOM Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.flowsom_worker:
            self.flowsom_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "FlowSOM clustering calculation has been cancelled.")


class ParcWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.gate = gate
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
                    self.error.emit("PARC clustering calculation was canceled.")
                    return

            fp.tl.parc(
                self.dataset,
                gate=self.gate,
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

class ParcWindow(BaseClusteringWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "PARC", {
            "dist_std_local": 3,
            "jac_std_global": "median",
            "keep_all_local_dist": "auto",
            "too_big_factor": 0.4,
            "small_pop": 10,
            "jac_weighted_edges": "True",
            "knn": 30,
            "n_iter_leiden": 5,
            "num_threads": -1,
            "distance": "l2",
            "time_smallpop": 15,
            "partition_type": "ModularityVP",
            "resolution_parameter": 1.0,
            "hnsw_param_ef_construction": 150
        })

        self.parc_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to PARC clustering.
        """
        self.dist_std_local_label = QLabel("Distance std local (dist_std_local):")
        self.dist_std_local_input = QLineEdit()
        self.dist_std_local_input.setPlaceholderText("e.g., 3")

        self.jac_std_global_label = QLabel("Jaccard std global (jac_std_global):")
        self.jac_std_global_input = QLineEdit()
        self.jac_std_global_input.setPlaceholderText("e.g., 'median'")

        self.keep_all_local_dist_label = QLabel("Keep all local dist (keep_all_local_dist):")
        self.keep_all_local_dist_input = QLineEdit()
        self.keep_all_local_dist_input.setPlaceholderText("e.g., 'auto'")

        self.too_big_factor_label = QLabel("Too big factor (too_big_factor):")
        self.too_big_factor_input = QLineEdit()
        self.too_big_factor_input.setPlaceholderText("e.g., 0.4")

        self.small_pop_label = QLabel("Small population size (small_pop):")
        self.small_pop_input = QLineEdit()
        self.small_pop_input.setPlaceholderText("e.g., 10")

        self.jac_weighted_edges_label = QLabel("Jac weighted edges (jac_weighted_edges):")
        self.jac_weighted_edges_input = QComboBox()
        self.jac_weighted_edges_input.addItems(["True", "False"])

        self.knn_label = QLabel("Number of neighbors (knn):")
        self.knn_input = QLineEdit()
        self.knn_input.setPlaceholderText("e.g., 30")

        self.n_iter_leiden_label = QLabel("Number of Leiden iterations (n_iter_leiden):")
        self.n_iter_leiden_input = QLineEdit()
        self.n_iter_leiden_input.setPlaceholderText("e.g., 5")

        self.num_threads_label = QLabel("Number of threads (num_threads):")
        self.num_threads_input = QLineEdit()
        self.num_threads_input.setPlaceholderText("e.g., -1")

        self.distance_label = QLabel("Distance metric (distance):")
        self.distance_input = QLineEdit()
        self.distance_input.setPlaceholderText("e.g., 'l2'")

        self.time_smallpop_label = QLabel("Time for small populations (time_smallpop):")
        self.time_smallpop_input = QLineEdit()
        self.time_smallpop_input.setPlaceholderText("e.g., 15")

        self.partition_type_label = QLabel("Partition type (partition_type):")
        self.partition_type_input = QLineEdit()
        self.partition_type_input.setPlaceholderText("e.g., 'ModularityVP'")

        self.resolution_parameter_label = QLabel("Resolution parameter:")
        self.resolution_parameter_input = QLineEdit()
        self.resolution_parameter_input.setPlaceholderText("e.g., 1.0")

        self.hnsw_param_ef_construction_label = QLabel("HNSW param ef construction:")
        self.hnsw_param_ef_construction_input = QLineEdit()
        self.hnsw_param_ef_construction_input.setPlaceholderText("e.g., 150")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.dist_std_local_label, self.dist_std_local_input)
        self.advanced_settings_layout.addRow(self.jac_std_global_label, self.jac_std_global_input)
        self.advanced_settings_layout.addRow(self.keep_all_local_dist_label, self.keep_all_local_dist_input)
        self.advanced_settings_layout.addRow(self.too_big_factor_label, self.too_big_factor_input)
        self.advanced_settings_layout.addRow(self.small_pop_label, self.small_pop_input)
        self.advanced_settings_layout.addRow(self.jac_weighted_edges_label, self.jac_weighted_edges_input)
        self.advanced_settings_layout.addRow(self.knn_label, self.knn_input)
        self.advanced_settings_layout.addRow(self.n_iter_leiden_label, self.n_iter_leiden_input)
        self.advanced_settings_layout.addRow(self.num_threads_label, self.num_threads_input)
        self.advanced_settings_layout.addRow(self.distance_label, self.distance_input)
        self.advanced_settings_layout.addRow(self.time_smallpop_label, self.time_smallpop_input)
        self.advanced_settings_layout.addRow(self.partition_type_label, self.partition_type_input)
        self.advanced_settings_layout.addRow(self.resolution_parameter_label, self.resolution_parameter_input)
        self.advanced_settings_layout.addRow(self.hnsw_param_ef_construction_label, self.hnsw_param_ef_construction_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the PARC clustering calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            gate = self.gate_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()
            if scaling == "None":
                scaling = None

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'dist_std_local': float(self.dist_std_local_input.text()) if self.dist_std_local_input.text() else 3,
                'jac_std_global': self.jac_std_global_input.text() if self.jac_std_global_input.text() else 'median',
                'keep_all_local_dist': self.keep_all_local_dist_input.text() if self.keep_all_local_dist_input.text() else 'auto',
                'too_big_factor': float(self.too_big_factor_input.text()) if self.too_big_factor_input.text() else 0.4,
                'small_pop': int(self.small_pop_input.text()) if self.small_pop_input.text() else 10,
                'jac_weighted_edges': self.jac_weighted_edges_input.currentText() == "True",
                'knn': int(self.knn_input.text()) if self.knn_input.text() else 30,
                'n_iter_leiden': int(self.n_iter_leiden_input.text()) if self.n_iter_leiden_input.text() else 5,
                'num_threads': int(self.num_threads_input.text()) if self.num_threads_input.text() else -1,
                'distance': self.distance_input.text() if self.distance_input.text() else 'l2',
                'time_smallpop': int(self.time_smallpop_input.text()) if self.time_smallpop_input.text() else 15,
                'partition_type': self.partition_type_input.text() if self.partition_type_input.text() else 'ModularityVP',
                'resolution_parameter': float(self.resolution_parameter_input.text()) if self.resolution_parameter_input.text() else 1.0,
                'hnsw_param_ef_construction': int(self.hnsw_param_ef_construction_input.text()) if self.hnsw_param_ef_construction_input.text() else 150,
            }

            # Show loading screen
            loading_message = "Calculating PARC clustering...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the PARC worker thread
            self.calculation_canceled = False
            self.parc_worker = ParcWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.parc_worker.finished.connect(self.on_parc_finished)
            self.parc_worker.error.connect(self.on_parc_error)
            self.parc_worker.start()

        except Exception as e:
            self.show_error("PARC Calculation Error", str(e))

    def on_parc_finished(self):
        """
        Handles the completion of the PARC clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "PARC clustering completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_parc_error(self, error_message):
        """
        Handles any error that occurs during the PARC clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("PARC Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.parc_worker:
            self.parc_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "PARC clustering calculation has been cancelled.")


class PhenographWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.gate = gate
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
                    self.error.emit("Phenograph clustering calculation was canceled.")
                    return

            # Perform Phenograph clustering computation here
            fp.tl.phenograph(
                self.dataset,
                gate=self.gate,
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

class PhenographWindow(BaseClusteringWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Phenograph", {
            "clustering_algo": "louvain",
            "k": 30,
            "directed": "False",
            "prune": "False",
            "min_cluster_size": 10,
            "jaccard": "True",
            "primary_metric": "euclidean",
            "n_jobs": -1,
            "q_tol": 1e-3,
            "louvain_time_limit": 2000,
            "nn_method": "kdtree",
            "resolution_parameter": 1,
            "n_iterations": -1,
            "use_weights": "True"
        })

        self.phenograph_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to Phenograph clustering.
        """
        self.clustering_algo_label = QLabel("Clustering algorithm (clustering_algo):")
        self.clustering_algo_input = QComboBox()
        self.clustering_algo_input.addItems(["louvain", "leiden"])

        self.k_label = QLabel("k:")
        self.k_input = QLineEdit()
        self.k_input.setPlaceholderText("e.g., 30")

        self.directed_label = QLabel("Directed:")
        self.directed_input = QComboBox()
        self.directed_input.addItems(["True", "False"])

        self.prune_label = QLabel("Prune:")
        self.prune_input = QComboBox()
        self.prune_input.addItems(["True", "False"])

        self.min_cluster_size_label = QLabel("Minimum cluster size:")
        self.min_cluster_size_input = QLineEdit()
        self.min_cluster_size_input.setPlaceholderText("e.g., 10")

        self.jaccard_label = QLabel("Jaccard:")
        self.jaccard_input = QComboBox()
        self.jaccard_input.addItems(["True", "False"])

        self.primary_metric_label = QLabel("Primary metric:")
        self.primary_metric_input = QComboBox()
        self.primary_metric_input.addItems(["euclidean", "manhattan", "correlation", "cosine"])

        self.n_jobs_label = QLabel("Number of jobs:")
        self.n_jobs_input = QLineEdit()
        self.n_jobs_input.setPlaceholderText("e.g., -1")

        self.q_tol_label = QLabel("q tolerance:")
        self.q_tol_input = QLineEdit()
        self.q_tol_input.setPlaceholderText("e.g., 1e-3")

        self.louvain_time_limit_label = QLabel("Louvain time limit:")
        self.louvain_time_limit_input = QLineEdit()
        self.louvain_time_limit_input.setPlaceholderText("e.g., 2000")

        self.nn_method_label = QLabel("Nearest neighbors method:")
        self.nn_method_input = QComboBox()
        self.nn_method_input.addItems(["kdtree", "brute"])

        self.resolution_parameter_label = QLabel("Resolution parameter:")
        self.resolution_parameter_input = QLineEdit()
        self.resolution_parameter_input.setPlaceholderText("e.g., 1.0")

        self.n_iterations_label = QLabel("Number of iterations:")
        self.n_iterations_input = QLineEdit()
        self.n_iterations_input.setPlaceholderText("e.g., -1")

        self.use_weights_label = QLabel("Use weights:")
        self.use_weights_input = QComboBox()
        self.use_weights_input.addItems(["True", "False"])

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.clustering_algo_label, self.clustering_algo_input)
        self.advanced_settings_layout.addRow(self.k_label, self.k_input)
        self.advanced_settings_layout.addRow(self.directed_label, self.directed_input)
        self.advanced_settings_layout.addRow(self.prune_label, self.prune_input)
        self.advanced_settings_layout.addRow(self.min_cluster_size_label, self.min_cluster_size_input)
        self.advanced_settings_layout.addRow(self.jaccard_label, self.jaccard_input)
        self.advanced_settings_layout.addRow(self.primary_metric_label, self.primary_metric_input)
        self.advanced_settings_layout.addRow(self.n_jobs_label, self.n_jobs_input)
        self.advanced_settings_layout.addRow(self.q_tol_label, self.q_tol_input)
        self.advanced_settings_layout.addRow(self.louvain_time_limit_label, self.louvain_time_limit_input)
        self.advanced_settings_layout.addRow(self.nn_method_label, self.nn_method_input)
        self.advanced_settings_layout.addRow(self.resolution_parameter_label, self.resolution_parameter_input)
        self.advanced_settings_layout.addRow(self.n_iterations_label, self.n_iterations_input)
        self.advanced_settings_layout.addRow(self.use_weights_label, self.use_weights_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the Phenograph clustering calculation with a loading screen.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            gate = self.gate_dropdown.currentText()
            layer = self.data_format_dropdown.currentText()
            use_only_fluo = self.use_marker_dropdown.currentText() == "True"
            exclude_channels = self.exclude_channels_dropdown.currentText()
            scaling = self.scaling_dropdown.currentText()
            if scaling == "None":
                scaling = None

            # Collect advanced parameters with defaults
            advanced_kwargs = {
                'clustering_algo': self.clustering_algo_input.currentText(),
                'k': int(self.k_input.text()) if self.k_input.text() else 30,
                'directed': self.directed_input.currentText() == "True",
                'prune': self.prune_input.currentText() == "True",
                'min_cluster_size': int(self.min_cluster_size_input.text()) if self.min_cluster_size_input.text() else 10,
                'jaccard': self.jaccard_input.currentText() == "True",
                'primary_metric': self.primary_metric_input.currentText() if self.primary_metric_input.currentText() else 'euclidean',
                'n_jobs': int(self.n_jobs_input.text()) if self.n_jobs_input.text() else -1,
                'q_tol': float(self.q_tol_input.text()) if self.q_tol_input.text() else 1e-3,
                'louvain_time_limit': int(self.louvain_time_limit_input.text()) if self.louvain_time_limit_input.text() else 2000,
                'nn_method': self.nn_method_input.currentText() if self.nn_method_input.currentText() else 'kdtree',
                'resolution_parameter': float(self.resolution_parameter_input.text()) if self.resolution_parameter_input.text() else 1,
                'n_iterations': int(self.n_iterations_input.text()) if self.n_iterations_input.text() else -1,
                'use_weights': self.use_weights_input.currentText() == "True",
            }

            # Show loading screen
            loading_message = "Calculating Phenograph clustering...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the Phenograph worker thread
            self.calculation_canceled = False
            self.phenograph_worker = PhenographWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.phenograph_worker.finished.connect(self.on_phenograph_finished)
            self.phenograph_worker.error.connect(self.on_phenograph_error)
            self.phenograph_worker.start()

        except Exception as e:
            self.show_error("Phenograph Calculation Error", str(e))

    def on_phenograph_finished(self):
        """
        Handles the completion of the Phenograph clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Phenograph clustering completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_phenograph_error(self, error_message):
        """
        Handles any error that occurs during the Phenograph clustering calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Phenograph Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.phenograph_worker:
            self.phenograph_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Phenograph clustering calculation has been cancelled.")

