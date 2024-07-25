from PyQt5.QtWidgets import (QMessageBox, QWidget, QVBoxLayout, 
                             QPushButton, QFormLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox,
                             QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QMutex, QMutexLocker

import FACSPy as fp

from .._utils import LoadingScreen, MultiSelectComboBox
from ._analysis_menu import BaseAnalysisMenu


class BaseDimensionalityReductionWindow(BaseAnalysisMenu):
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


class PCAWorker(QThread):
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
                    self.error.emit("PCA calculation was canceled.")
                    return

            fp.tl.pca(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                scaling=self.scaling,
                exclude=self.exclude_channels,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False

class SinglecellPCAWindow(BaseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "PCA", ["n_components", "zero_center", "svd_solver"])

        self.pca_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to PCA.
        """
        self.n_components_label = QLabel("Number of components (n_components):")
        self.n_components_input = QLineEdit()
        self.n_components_input.setPlaceholderText("e.g., 10")

        self.zero_center_label = QLabel("Zero center:")
        self.zero_center_input = QComboBox()
        self.zero_center_input.addItems(["True", "False"])

        self.svd_solver_label = QLabel("SVD Solver:")
        self.svd_solver_input = QComboBox()
        self.svd_solver_input.addItems(["auto", "full", "arpack", "randomized"])

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.n_components_label, self.n_components_input)
        self.advanced_settings_layout.addRow(self.zero_center_label, self.zero_center_input)
        self.advanced_settings_layout.addRow(self.svd_solver_label, self.svd_solver_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the PCA calculation with a loading screen.
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

            # Collect advanced parameters
            n_components = self.n_components_input.text()
            zero_center = self.zero_center_input.currentText() == "True"
            svd_solver = self.svd_solver_input.currentText()

            advanced_kwargs = {}
            if n_components:
                advanced_kwargs['n_components'] = int(n_components)
            advanced_kwargs['zero_center'] = zero_center
            advanced_kwargs['svd_solver'] = svd_solver

            # Show loading screen
            loading_message = "Calculating PCA...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the PCA worker thread
            self.calculation_canceled = False
            self.pca_worker = PCAWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
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
            QMessageBox.information(self, "Success", "PCA calculation completed.")
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
            QMessageBox.information(self, "Cancelled", "PCA calculation has been cancelled.")



class UMAPWorker(QThread):
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
                    self.error.emit("UMAP calculation was canceled.")
                    return

            fp.tl.umap(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                scaling=self.scaling,
                exclude=self.exclude_channels,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class SinglecellUMAPWindow(BaseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "UMAP", ["min_dist", "spread", "n_components", "maxiter", "alpha", "gamma", "negative_sample_rate", "init_pos", "a", "b", "method", "neighbors_key"])

        self.umap_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to UMAP.
        """
        self.min_dist_label = QLabel("Minimum distance (min_dist):")
        self.min_dist_input = QLineEdit()
        self.min_dist_input.setPlaceholderText("e.g., 0.1")

        self.spread_label = QLabel("Spread:")
        self.spread_input = QLineEdit()
        self.spread_input.setPlaceholderText("e.g., 1.0")

        self.n_components_label = QLabel("Number of components (n_components):")
        self.n_components_input = QLineEdit()
        self.n_components_input.setPlaceholderText("e.g., 3")

        self.maxiter_label = QLabel("Max iterations (maxiter):")
        self.maxiter_input = QLineEdit()
        self.maxiter_input.setPlaceholderText("Leave blank for default")

        self.alpha_label = QLabel("Alpha:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setPlaceholderText("e.g., 1.0")

        self.gamma_label = QLabel("Gamma:")
        self.gamma_input = QLineEdit()
        self.gamma_input.setPlaceholderText("e.g., 1.0")

        self.negative_sample_rate_label = QLabel("Negative sample rate:")
        self.negative_sample_rate_input = QLineEdit()
        self.negative_sample_rate_input.setPlaceholderText("e.g., 5")

        self.init_pos_label = QLabel("Initial position (init_pos):")
        self.init_pos_input = QLineEdit()
        self.init_pos_input.setPlaceholderText("e.g., spectral")

        self.a_label = QLabel("a:")
        self.a_input = QLineEdit()
        self.a_input.setPlaceholderText("Leave blank for default")

        self.b_label = QLabel("b:")
        self.b_input = QLineEdit()
        self.b_input.setPlaceholderText("Leave blank for default")

        self.method_label = QLabel("Method:")
        self.method_input = QComboBox()
        self.method_input.addItems(["umap", "rapids"])

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.min_dist_label, self.min_dist_input)
        self.advanced_settings_layout.addRow(self.spread_label, self.spread_input)
        self.advanced_settings_layout.addRow(self.n_components_label, self.n_components_input)
        self.advanced_settings_layout.addRow(self.maxiter_label, self.maxiter_input)
        self.advanced_settings_layout.addRow(self.alpha_label, self.alpha_input)
        self.advanced_settings_layout.addRow(self.gamma_label, self.gamma_input)
        self.advanced_settings_layout.addRow(self.negative_sample_rate_label, self.negative_sample_rate_input)
        self.advanced_settings_layout.addRow(self.init_pos_label, self.init_pos_input)
        self.advanced_settings_layout.addRow(self.a_label, self.a_input)
        self.advanced_settings_layout.addRow(self.b_label, self.b_input)
        self.advanced_settings_layout.addRow(self.method_label, self.method_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the UMAP calculation with a loading screen.
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

            # Collect advanced parameters
            advanced_kwargs = {
                'min_dist': float(self.min_dist_input.text()) if self.min_dist_input.text() else 0.5,
                'spread': float(self.spread_input.text()) if self.spread_input.text() else 1.0,
                'n_components': int(self.n_components_input.text()) if self.n_components_input.text() else 3,
                'maxiter': int(self.maxiter_input.text()) if self.maxiter_input.text() else None,
                'alpha': float(self.alpha_input.text()) if self.alpha_input.text() else 1.0,
                'gamma': float(self.gamma_input.text()) if self.gamma_input.text() else 1.0,
                'negative_sample_rate': int(self.negative_sample_rate_input.text()) if self.negative_sample_rate_input.text() else 5,
                'init_pos': self.init_pos_input.text() if self.init_pos_input.text() else 'spectral',
                'a': float(self.a_input.text()) if self.a_input.text() else None,
                'b': float(self.b_input.text()) if self.b_input.text() else None,
                'method': self.method_input.currentText(),
            }

            # Show loading screen
            loading_message = "Calculating UMAP...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the UMAP worker thread
            self.calculation_canceled = False
            self.umap_worker = UMAPWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
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
            QMessageBox.information(self, "Success", "UMAP calculation completed.")
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
            QMessageBox.information(self, "Cancelled", "UMAP calculation has been cancelled.")


class TSNEWorker(QThread):
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
                    self.error.emit("TSNE calculation was canceled.")
                    return

            fp.tl.tsne(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                scaling=self.scaling,
                exclude=self.exclude_channels,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class SinglecellTSNEWindow(BaseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "t-SNE", ["n_pcs", "perplexity", "early_exaggeration", "learning_rate", "metric"])

        self.tsne_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to t-SNE.
        """
        self.n_pcs_label = QLabel("Number of PCs (n_pcs):")
        self.n_pcs_input = QLineEdit()
        self.n_pcs_input.setPlaceholderText("e.g., 50")

        self.perplexity_label = QLabel("Perplexity:")
        self.perplexity_input = QLineEdit()
        self.perplexity_input.setPlaceholderText("e.g., 30")

        self.early_exaggeration_label = QLabel("Early Exaggeration:")
        self.early_exaggeration_input = QLineEdit()
        self.early_exaggeration_input.setPlaceholderText("e.g., 12")

        self.learning_rate_label = QLabel("Learning Rate:")
        self.learning_rate_input = QLineEdit()
        self.learning_rate_input.setPlaceholderText("e.g., auto")

        self.metric_label = QLabel("Metric:")
        self.metric_input = QLineEdit()
        self.metric_input.setPlaceholderText("e.g., euclidean")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.n_pcs_label, self.n_pcs_input)
        self.advanced_settings_layout.addRow(self.perplexity_label, self.perplexity_input)
        self.advanced_settings_layout.addRow(self.early_exaggeration_label, self.early_exaggeration_input)
        self.advanced_settings_layout.addRow(self.learning_rate_label, self.learning_rate_input)
        self.advanced_settings_layout.addRow(self.metric_label, self.metric_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the t-SNE calculation with a loading screen.
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

            # Collect advanced parameters
            advanced_kwargs = {
                'n_pcs': int(self.n_pcs_input.text()) if self.n_pcs_input.text() else None,
                'perplexity': float(self.perplexity_input.text()) if self.perplexity_input.text() else 30,
                'early_exaggeration': float(self.early_exaggeration_input.text()) if self.early_exaggeration_input.text() else 12,
                'learning_rate': self.learning_rate_input.text() if self.learning_rate_input.text() else 'auto',
                'metric': self.metric_input.text() if self.metric_input.text() else 'euclidean'
            }

            # Show loading screen
            loading_message = "Calculating t-SNE...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the t-SNE worker thread
            self.calculation_canceled = False
            self.tsne_worker = TSNEWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
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
            QMessageBox.information(self, "Success", "t-SNE calculation completed.")
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
            QMessageBox.information(self, "Cancelled", "t-SNE calculation has been cancelled.")


class DiffmapWorker(QThread):
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
                    self.error.emit("Diffusion Map calculation was canceled.")
                    return

            fp.tl.diffmap(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                scaling=self.scaling,
                exclude=self.exclude_channels,
                **self.advanced_kwargs
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False

class SinglecellDiffmapWindow(BaseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Diffusion Map", ["n_comps"])

        self.diffmap_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to Diffusion Map.
        """
        self.n_comps_label = QLabel("Number of components (n_comps):")
        self.n_comps_input = QLineEdit()
        self.n_comps_input.setPlaceholderText("e.g., 15")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.n_comps_label, self.n_comps_input)

    def calculate_dimensionality_reduction(self):
        """
        Performs the Diffusion Map calculation with a loading screen.
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

            # Collect advanced parameters
            advanced_kwargs = {
                'n_comps': int(self.n_comps_input.text()) if self.n_comps_input.text() else dataset.shape[1]-1,
            }

            # Show loading screen
            loading_message = "Calculating Diffusion Map...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the Diffusion Map worker thread
            self.calculation_canceled = False
            self.diffmap_worker = DiffmapWorker(dataset, gate, layer, use_only_fluo, scaling, exclude_channels, advanced_kwargs)
            self.diffmap_worker.finished.connect(self.on_diffmap_finished)
            self.diffmap_worker.error.connect(self.on_diffmap_error)
            self.diffmap_worker.start()

        except Exception as e:
            self.show_error("Diffusion Map Calculation Error", str(e))

    def on_diffmap_finished(self):
        """
        Handles the completion of the Diffusion Map calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Diffusion Map calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_diffmap_error(self, error_message):
        """
        Handles any error that occurs during the Diffusion Map calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Diffusion Map Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.diffmap_worker:
            self.diffmap_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Diffusion Map calculation has been cancelled.")


class NeighborsWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self,
                 dataset,
                 gate,
                 layer,
                 use_only_fluo,
                 scaling,
                 exclude_channels,
                 n_neighbors,
                 use_rep,
                 n_pcs,
                 advanced_kwargs):
        super().__init__()
        self.dataset = dataset
        self.gate = gate
        self.layer = layer
        self.use_only_fluo = use_only_fluo
        self.scaling = scaling
        self.exclude_channels = exclude_channels
        self.n_neighbors = n_neighbors
        self.use_rep = use_rep
        self.n_pcs = n_pcs
        self._is_running = True
        self._mutex = QMutex()  # Mutex for thread-safe flag

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Neighbors calculation was canceled.")
                    return

            fp.tl.neighbors(
                self.dataset,
                gate=self.gate,
                layer=self.layer,
                use_only_fluo=self.use_only_fluo,
                scaling=self.scaling,
                exclude=self.exclude_channels,
                n_neighbors=self.n_neighbors,
                use_rep=self.use_rep if self.use_rep != "" else None,
                n_pcs=int(self.n_pcs) if self.n_pcs else None,
            )

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False


class SinglecellNeighborsWindow(BaseDimensionalityReductionWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Neighbors", [])

        self.neighbors_worker = None
        self.calculation_canceled = False

    def add_advanced_settings(self):
        """
        Adds advanced settings specific to Neighbors.
        """
        self.n_neighbors_label = QLabel("Number of neighbors (n_neighbors):")
        self.n_neighbors_input = QLineEdit()
        self.n_neighbors_input.setPlaceholderText("e.g., 15")

        self.use_rep_label = QLabel("Use representation (use_rep):")
        self.use_rep_dropdown = QComboBox()

        self.n_pcs_label = QLabel("Number of PCs (n_pcs):")
        self.n_pcs_input = QLineEdit()
        self.n_pcs_input.setPlaceholderText("e.g., None")

        # Add to advanced settings layout
        self.advanced_settings_layout.addRow(self.n_neighbors_label, self.n_neighbors_input)
        self.advanced_settings_layout.addRow(self.use_rep_label, self.use_rep_dropdown)
        self.advanced_settings_layout.addRow(self.n_pcs_label, self.n_pcs_input)

    def populate_dropdowns(self):
        """
        Populates the dropdowns with appropriate values.
        """
        super().populate_dropdowns()
        
        # Populate use_rep dropdown with keys from dataset.obsm
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            self.use_rep_dropdown.clear()
            self.use_rep_dropdown.addItem("")  # Add empty option for None
            self.use_rep_dropdown.addItems(dataset.obsm.keys())

        except Exception as e:
            self.show_error("Data Format Error", str(e))

    def calculate_dimensionality_reduction(self):
        """
        Performs the Neighbors calculation with a loading screen.
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

            # Collect advanced parameters
            n_neighbors = int(self.n_neighbors_input.text()) if self.n_neighbors_input.text() else 15
            use_rep = self.use_rep_dropdown.currentText() if self.use_rep_dropdown.currentText() else None
            n_pcs = int(self.n_pcs_input.text()) if self.n_pcs_input.text() else None

            advanced_kwargs = {
                # we keep it empty for now as we pass it explicitly.
            }

            # Show loading screen
            loading_message = "Calculating Neighbors...\n\n"
            loading_message += f"Population: {gate}\n"
            loading_message += f"Data: {layer}"
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the Neighbors worker thread
            self.calculation_canceled = False
            self.neighbors_worker = NeighborsWorker(
                dataset,
                gate,
                layer,
                use_only_fluo,
                scaling,
                exclude_channels,
                n_neighbors,
                use_rep,
                n_pcs,
                advanced_kwargs
            )
            self.neighbors_worker.finished.connect(self.on_neighbors_finished)
            self.neighbors_worker.error.connect(self.on_neighbors_error)
            self.neighbors_worker.start()

        except Exception as e:
            self.show_error("Neighbors Calculation Error", str(e))

    def on_neighbors_finished(self):
        """
        Handles the completion of the Neighbors calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Neighbors calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_neighbors_error(self, error_message):
        """
        Handles any error that occurs during the Neighbors calculation.
        """
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Neighbors Calculation Error", error_message)

    def cancel_calculation(self):
        """
        Handle the cancel signal from the loading screen.
        """
        self.calculation_canceled = True
        if self.neighbors_worker:
            self.neighbors_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Neighbors calculation has been cancelled.")

