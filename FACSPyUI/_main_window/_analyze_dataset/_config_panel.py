from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QLabel,
                             QHBoxLayout, QPushButton, QGroupBox,
                             QMessageBox, QScrollArea, QLineEdit, QCheckBox,
                             QFormLayout)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QColor
from PyQt5.QtCore import pyqtSignal
from typing import Optional
from .._utils import MultiSelectComboBox, HoverLabel

CATEGORICAL_CMAPS = [
    "Set1", "Set2", "tab10", "Set3", "hls", "Paired"
]

CONTINUOUS_CMAPS = [
    "RdYlBu_r", "RdYlBu",
    "inferno_r", "inferno",
    "magma_r", "magma", 
    "plasma_r", "plasma", 
    "viridis_r", "viridis", 
    "cividis_r", "cividis", 
    "jet",
    "Reds", "Reds_r",
    "Blues", "Blues_r",
    "Greens", "Greens_r"
]


class ConfigPanel(QWidget):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # we instantiate it as None
        # and later reference it with the correct
        # function-specific ConfigPanels
        self._config_panel = None

        layout = QVBoxLayout()

        # Dropdown menu for selecting a plot
        analysis_label = QLabel("Select a plot:")
        self.analysis_dropdown = QComboBox()
        self.populate_analysis_dropdown()
        self.analysis_dropdown.currentIndexChanged.connect(self.on_analysis_type_selected)

        dropdown_layout = QHBoxLayout()
        dropdown_layout.addWidget(analysis_label)
        dropdown_layout.addWidget(self.analysis_dropdown)

        # Placeholder layout for future configuration panels
        self.config_panel_layout = QVBoxLayout()

        layout.addLayout(dropdown_layout)
        layout.addLayout(self.config_panel_layout)

        self.setLayout(layout)

        # Add default placeholder
        self.add_default_placeholder()


    def populate_analysis_dropdown(self):
        model = QStandardItemModel(self.analysis_dropdown)

        default_item = QStandardItem("Select a plot")
        default_item.setEnabled(False)
        model.appendRow(default_item)

        section_headings = ["Intensity metrics", "Gate metrics", "QC", "Dimensionality Reduction", "Clustering", "Cofactors"]
        section_items = [
            ["MFI", "FOP", "Expression Heatmap", "Marker correlations",
             "Sample correlations", "Sample distance", "Marker Density",
             "Biaxial Scatter", "Fold Change"],
            ["Gate frequency"],
            ["Metadata", "Cell counts"],
            ["Samplewise DimRed", "Singlecell DimRed"],
            ["Cluster Heatmap", "Cluster Abundance", "Cluster Frequency"],
            ["Transformation Plot"]
        ]
        # todo: Cluster Heatmap, Cofactor Distribution, Transformation Plot

        for section_idx, section_heading in enumerate(section_headings):
            heading_item = QStandardItem(section_heading)
            heading_item.setFont(QFont("Arial", weight=QFont.Bold))
            heading_item.setSelectable(False)
            heading_item.setEnabled(False)
            color = "white" if self.main_window.toolbar.is_dark_mode else "black"
            heading_item.setForeground(QColor(color))
            model.appendRow(heading_item)

            for item_text in section_items[section_idx]:
                item = QStandardItem("   " + item_text)
                model.appendRow(item)

        self.analysis_dropdown.setModel(model)
        self.analysis_dropdown.setCurrentIndex(0)

    def add_default_placeholder(self):
        """
        Adds a default placeholder for the initial state.
        """
        self.clear_config_panel_layout()

        placeholder = QLabel("Select an analysis to continue")
        self.config_panel_layout.addWidget(placeholder)

    def clear_config_panel_layout(self):
        """
        Clears the current config panel layout.
        """
        while self.config_panel_layout.count() > 0:
            item = self.config_panel_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def on_analysis_type_selected(self):
        """
        Handles the selection of an analysis type.
        """
        selected_analysis = self.analysis_dropdown.currentText().strip()
        self.switch_calculation_settings(selected_analysis)

    def instantiate_new_analysis_type(self):
        if self._config_panel is None:
            return
        self._config_panel.plot_requested.connect(self.emit_plot_requested)
        
        self.clear_config_panel_layout()
        self.config_panel_layout.addWidget(self._config_panel)

    def switch_calculation_settings(self, analysis_type):
        """
        Switches the settings displayed in the panel based on the analysis type.
        """
        # Clear existing layout
        self.clear_config_panel_layout()

        if analysis_type == "MFI":
            from . import ConfigPanelMFI
            self._config_panel = ConfigPanelMFI(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "FOP":
            from . import ConfigPanelFOP
            self._config_panel = ConfigPanelFOP(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Gate frequency":
            from . import ConfigPanelGateFrequency
            self._config_panel = ConfigPanelGateFrequency(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Metadata":
            from . import ConfigPanelMetadata
            self._config_panel = ConfigPanelMetadata(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Cell counts":
            from . import ConfigPanelCellCounts
            self._config_panel = ConfigPanelCellCounts(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Marker correlations":
            from . import ConfigPanelMarkerCorrelation
            self._config_panel = ConfigPanelMarkerCorrelation(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Sample correlations":
            from . import ConfigPanelSampleCorrelation
            self._config_panel = ConfigPanelSampleCorrelation(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Sample distance":
            from . import ConfigPanelSampleDistance
            self._config_panel = ConfigPanelSampleDistance(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Expression Heatmap":
            from . import ConfigPanelExpressionHeatmap
            self._config_panel = ConfigPanelExpressionHeatmap(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Samplewise DimRed":
            from . import ConfigPanelSamplewiseDimred
            self._config_panel = ConfigPanelSamplewiseDimred(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Singlecell DimRed":
            from . import ConfigPanelSinglecellDimred
            self._config_panel = ConfigPanelSinglecellDimred(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Biaxial Scatter":
            from . import ConfigPanelBiaxScatter
            self._config_panel = ConfigPanelBiaxScatter(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Marker Density":
            from . import ConfigPanelMarkerDensity
            self._config_panel = ConfigPanelMarkerDensity(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Cluster Abundance":
            from . import ConfigPanelClusterAbundance
            self._config_panel = ConfigPanelClusterAbundance(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Cluster Frequency":
            from . import ConfigPanelClusterFrequency
            self._config_panel = ConfigPanelClusterFrequency(self.main_window)
            self.instantiate_new_analysis_type()
        
        elif analysis_type == "Fold Change":
            from . import ConfigPanelFoldChange
            self._config_panel = ConfigPanelFoldChange(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Cluster Heatmap":
            from . import ConfigPanelClusterHeatmap
            self._config_panel = ConfigPanelClusterHeatmap(self.main_window)
            self.instantiate_new_analysis_type()

        elif analysis_type == "Transformation Plot":
            from . import ConfigPanelTransformationPlot
            self._config_panel = ConfigPanelTransformationPlot(self.main_window)
            self.instantiate_new_analysis_type()

        else:
            # Add default placeholder
            self.add_default_placeholder()

    def emit_plot_requested(self, plot_config):
        """
        Emit the plot requested signal from the current analysis panel.
        """
        print("Relaying plot_requested signal with config:", plot_config)  # Debug print
        self.plot_requested.emit(plot_config)

    def update_plotting_tab(self):
        """
        Updates the plotting tab with dynamic dropdowns based on the AnnData object.
        """
        if self._config_panel is not None:
            self._config_panel.populate_dropdowns()


class BaseConfigPanel(QWidget):
    plot_requested = pyqtSignal(dict)
    submenu_opened = pyqtSignal(int, QWidget)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.submenu_opened.connect(self.resize_window_for_additional_menus)

        # Scroll area widget contents
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)
        self.enable_documentation()

    def resize_window_for_additional_menus(self,
                                           height_increase,
                                           widget):
        widget.setFixedHeight(height_increase)

    def render_plot(self):
        """
        Handles the rendering of the plot.
        """
        try:
            # Collect parameters and emit the plot requested signal
            plot_config = self.generate_plot_config()
            self.plot_requested.emit(plot_config)
        except Exception as e:
            self.show_error("Render Plot Error", str(e))

    def resizeEvent(self, event):
        """
        Adjust input sizes when the window is resized.
        """
        super().resizeEvent(event)

    def populate_dropdowns(self):
        """
        Populates the dropdowns with relevant dataset information.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            if hasattr(self, 'layer_dropdown'):
                self.layer_dropdown.clear()
                self.layer_dropdown.addItems(dataset.layers.keys())

            if hasattr(self, 'gate_dropdown'):
                self.gate_dropdown.clear()
                self.gate_dropdown.addItems(dataset.uns.get("gating_cols", []))

            if hasattr(self, 'freq_of_gate_dropdown'):
                self.freq_of_gate_dropdown.clear()
                self.freq_of_gate_dropdown.addItems(dataset.uns.get("gating_cols", []))

            if hasattr(self, 'marker_dropdown'):
                self.marker_dropdown.clear()
                self.marker_dropdown.addItems(dataset.var_names)

            obs_columns = dataset.obs.columns
            if hasattr(self, 'split_by_dropdown'):
                self.split_by_dropdown.clear()
                self.split_by_dropdown.addItems(obs_columns)

            if hasattr(self, 'group_by_dropdown'):
                self.group_by_dropdown.clear()
                self.group_by_dropdown.addItems(obs_columns)

            if hasattr(self, 'group_by_fold_change_dropdown'):
                self.group_by_fold_change_dropdown.clear()
                self.group_by_fold_change_dropdown.addItems(obs_columns)

            if hasattr(self, 'group1_dropdown'):
                self.group1_dropdown.clear()
                cluster_col = self.group_by_fold_change_dropdown.currentText()
                self.group1_dropdown.addItems(dataset.obs[cluster_col].unique().tolist())

            if hasattr(self, 'group2_dropdown'):
                self.group2_dropdown.clear()
                cluster_col = self.group_by_fold_change_dropdown.currentText()
                self.group2_dropdown.addItems(dataset.obs[cluster_col].unique().tolist())

            if hasattr(self, 'colorby_dropdown'):
                self.colorby_dropdown.clear()
                if hasattr(self, "_additional_colorby"):
                    self.colorby_dropdown.addItems(self._additional_colorby)
                self.colorby_dropdown.addItems(obs_columns)
                self.colorby_dropdown.addItems(dataset.var_names)

            if hasattr(self, 'metadata_marker_dropdown'):
                self.metadata_marker_dropdown.clear()
                self.metadata_marker_dropdown.addItems(obs_columns)

            if hasattr(self, 'exclude_channels_dropdown'):
                self.exclude_channels_dropdown.clear()
                self.exclude_channels_dropdown.addItems(dataset.var_names)

            if hasattr(self, 'metadata_annotation_dropdown'):
                self.metadata_annotation_dropdown.clear()
                self.metadata_annotation_dropdown.addItems(obs_columns)

            if hasattr(self, 'sample_identifier_dropdown'):
                self.sample_identifier_dropdown.clear()
                self.sample_identifier_dropdown.addItems(
                    dataset.obs["sample_ID"].unique().tolist() + 
                    dataset.obs["file_name"].unique().tolist()
                )

            if hasattr(self, 'scatter_dropdown'):
                self.scatter_dropdown.clear()
                self.scatter_dropdown.addItems(dataset.var_names)

            if hasattr(self, 'xchannel_dropdown'):
                self.xchannel_dropdown.clear()
                self.xchannel_dropdown.addItems(dataset.var_names)

            if hasattr(self, 'ychannel_dropdown'):
                self.ychannel_dropdown.clear()
                self.ychannel_dropdown.addItems(dataset.var_names)

            if hasattr(self, 'xscale_dropdown'):
                self.xscale_dropdown.clear()
                self.xscale_dropdown.addItems(["biex", "linear", "log"])

            if hasattr(self, 'yscale_dropdown'):
                self.yscale_dropdown.clear()
                self.yscale_dropdown.addItems(["biex", "linear", "log"])

            if hasattr(self, 'colorscale_dropdown'):
                self.colorscale_dropdown.clear()
                self.colorscale_dropdown.addItems(["biex", "linear", "log"])

            if hasattr(self, 'cluster_key_dropdown'):
                self.cluster_key_dropdown.clear()
                cluster_columns = [
                    col for col in obs_columns
                    if any(k in col for k in ["phenograph", "flowsom", "leiden", "parc"])
                ]
                self.cluster_key_dropdown.addItems(cluster_columns)

            if hasattr(self, 'cluster_selection_dropdown'):
                self.cluster_selection_dropdown.clear()
                cluster_col = self.cluster_key_dropdown.currentText()
                clusters = dataset.obs[cluster_col].unique().tolist()
                clusters = [str(cl) for cl in clusters]
                self.cluster_selection_dropdown.addItems(clusters)

        except Exception as e:
            self.show_error("Dropdown Population Error", str(e))

    def generate_plot_config(self):
        plot_config = {}
        
        # General parameters
        if hasattr(self, 'layer_dropdown'):
            plot_config["layer"] = self.layer_dropdown.currentText()

        if hasattr(self, 'gate_dropdown'):
            plot_config["gate"] = self.gate_dropdown.currentText()

        if hasattr(self, 'sample_size_input'):
            plot_config["sample_size"] = self.sample_size_input.text()

        if hasattr(self, 'marker_dropdown'):
            plot_config["marker"] = self.marker_dropdown.currentText()

        if hasattr(self, 'group_by_dropdown'):
            plot_config["groupby"] = self.group_by_dropdown.currentText()

        if hasattr(self, 'split_by_dropdown'):
            plot_config["splitby"] = self.split_by_dropdown.currentText()

        if hasattr(self, 'stat_test_dropdown'):
            plot_config["stat_test"] = self.stat_test_dropdown.currentText()

        if hasattr(self, 'backend_dropdown'):
            plot_config["backend"] = self.backend_dropdown.currentText()
        else:
            plot_config["backend"] = "matplotlib" # there is no plot for only plotly

        if hasattr(self, 'metadata_marker_dropdown'):
            plot_config["metadata_marker"] = self.metadata_marker_dropdown.currentText()

        if hasattr(self, 'freq_of_gate_dropdown'):
            plot_config["freq_of"] = self.freq_of_gate_dropdown.currentText()

        if hasattr(self, 'use_marker_dropdown'):
            plot_config["include_technical_channels"] = self.use_marker_dropdown.currentText()

        if hasattr(self, 'exclude_channels_dropdown'):
            plot_config["exclude"] = self.exclude_channels_dropdown.currentText()

        if hasattr(self, 'scaling_dropdown'):
            plot_config["scaling"] = self.scaling_dropdown.currentText()

        if hasattr(self, 'data_metric_dropdown'):
            plot_config["data_metric"] = self.data_metric_dropdown.currentText()

        if hasattr(self, 'corr_method_dropdown'):
            plot_config["corr_method"] = self.corr_method_dropdown.currentText()

        if hasattr(self, 'metadata_annotation_dropdown'):
            plot_config["metadata_annotation"] = self.metadata_annotation_dropdown.currentText()

        if hasattr(self, 'continuous_colormap_dropdown'):
            plot_config["cmap"] = self.continuous_colormap_dropdown.currentText()

        if hasattr(self, 'full_colormap_dropdown'):
            plot_config["cmap"] = self.full_colormap_dropdown.currentText()

        if hasattr(self, 'cluster_method_dropdown'):
            plot_config["cluster_method"] = self.cluster_method_dropdown.currentText()

        if hasattr(self, 'colorby_dropdown'):
            plot_config["color"] = self.colorby_dropdown.currentText()

        if hasattr(self, 'samplewise_dimred_dropdown'):
            plot_config["reduction"] = self.samplewise_dimred_dropdown.currentText()

        if hasattr(self, 'dimred_dropdown'):
            plot_config["reduction"] = self.dimred_dropdown.currentText()

        if hasattr(self, 'sample_identifier_dropdown'):
            plot_config["sample_identifier"] = self.sample_identifier_dropdown.currentText()

        if hasattr(self, 'scatter_dropdown'):
            plot_config["scatter"] = self.scatter_dropdown.currentText()

        if hasattr(self, 'xchannel_dropdown'):
            plot_config["x_channel"] = self.xchannel_dropdown.currentText()

        if hasattr(self, 'ychannel_dropdown'):
            plot_config["y_channel"] = self.ychannel_dropdown.currentText()

        if hasattr(self, 'ridge_dropdown'):
            plot_config["ridge"] = self.ridge_dropdown.currentText()

        if hasattr(self, 'normalize_dropdown'):
            plot_config["normalize"] = self.normalize_dropdown.currentText()

        if hasattr(self, 'cluster_key_dropdown'):
            plot_config["cluster_key"] = self.cluster_key_dropdown.currentText()

        if hasattr(self, 'cluster_selection_dropdown'):
            plot_config["cluster"] = self.cluster_selection_dropdown.currentText()

        if hasattr(self, 'group_by_fold_change_dropdown'):
            plot_config["groupby"] = self.group_by_fold_change_dropdown.currentText()

        if hasattr(self, 'group1_dropdown'):
            plot_config["group1"] = self.group1_dropdown.currentText()

        if hasattr(self, 'group2_dropdown'):
            plot_config["group2"] = self.group2_dropdown.currentText()

        # Layout parameters
        if hasattr(self, 'title_input'):
            plot_config["title"] = self.title_input.text()
        if hasattr(self, 'xlabel_input'):
            plot_config["xlabel"] = self.xlabel_input.text()
        if hasattr(self, 'ylabel_input'):
            plot_config["ylabel"] = self.ylabel_input.text()

        # Fontsize parameters
        if hasattr(self, 'title_fontsize_input'):
            plot_config["title_fontsize"] = self.title_fontsize_input.text()
        if hasattr(self, 'xlabel_fontsize_input'):
            plot_config["xlabel_fontsize"] = self.xlabel_fontsize_input.text()
        if hasattr(self, 'ylabel_fontsize_input'):
            plot_config["ylabel_fontsize"] = self.ylabel_fontsize_input.text()
        if hasattr(self, 'xticklabels_fontsize_input'):
            plot_config["xticklabel_fontsize"] = self.xticklabels_fontsize_input.text()
        if hasattr(self, 'yticklabels_fontsize_input'):
            plot_config["yticklabel_fontsize"] = self.yticklabels_fontsize_input.text()

        if hasattr(self, 'dot_size_input'):
            plot_config["dotsize"] = self.dot_size_input.text()
        if hasattr(self, 'dot_linewidth_input'):
            plot_config["dot_linewidth"] = self.dot_linewidth_input.text()
        if hasattr(self, 'dot_linecolor_input'):
            plot_config["dot_linecolor"] = self.dot_linecolor_input.text()
        if hasattr(self, 'colormap_dropdown'):
            plot_config["cmap"] = self.colormap_dropdown.currentText()

        # Colorscale parameters
        if hasattr(self, 'colorscale_dropdown'):
            plot_config["color_scale"] = self.colorscale_dropdown.currentText()
        if hasattr(self, 'vmin_input'):
            plot_config["vmin"] = self.vmin_input.text()
        if hasattr(self, 'vmax_input'):
            plot_config["vmax"] = self.vmax_input.text()

        # X scale parameters
        if hasattr(self, 'xscale_dropdown'):
            plot_config["x_scale"] = self.xscale_dropdown.currentText()
        # Y scale parameters
        if hasattr(self, 'yscale_dropdown'):
            plot_config["y_scale"] = self.yscale_dropdown.currentText()

        # Aspect parameters
        if hasattr(self, 'plot_height_input'):
            plot_config["plot_height"] = self.plot_height_input.text()
        if hasattr(self, 'plot_aspect_input'):
            plot_config["plot_aspect"] = self.plot_aspect_input.text()
        if hasattr(self, 'plot_spacing_input'):
            plot_config["plot_spacing"] = self.plot_spacing_input.text()
        
        return plot_config



    def add_layer_input(self):
        self.layer_label = QLabel("Data format:")
        self.layer_dropdown = QComboBox()
        container = self.add_tooltip(self.layer_dropdown, parameter = "layer")
        self.form_layout.addRow(self.layer_label, container)

    def add_gate_input(self):
        self.gate_label = QLabel("Select gate:")
        self.gate_dropdown = QComboBox()
        container = self.add_tooltip(self.gate_dropdown, parameter = "gate")
        self.form_layout.addRow(self.gate_label, container)

    def add_sample_size_input(self):
        self.sample_size_label = QLabel("Subsample to:")
        self.sample_size_input = QLineEdit()
        container = self.add_tooltip(self.sample_size_input, parameter = "sample_size")
        self.form_layout.addRow(self.sample_size_label, container)

    def add_xchannel_input(self):
        self.xchannel_label = QLabel("Select x:")
        self.xchannel_dropdown = QComboBox()
        container = self.add_tooltip(self.xchannel_dropdown, parameter = "channel")
        self.form_layout.addRow(self.xchannel_label, container)

    def add_ychannel_input(self):
        self.ychannel_label = QLabel("Select y:")
        self.ychannel_dropdown = QComboBox()
        container = self.add_tooltip(self.ychannel_dropdown, parameter = "channel")
        self.form_layout.addRow(self.ychannel_label, container)

    def add_sample_identifier_input(self):
        self.sample_identifier_label = QLabel("Select sample:")
        self.sample_identifier_dropdown = QComboBox()
        container = self.add_tooltip(self.sample_identifier_dropdown, parameter = "sample_identifier")
        self.form_layout.addRow(self.sample_identifier_label, container)

    def add_scatter_input(self):
        self.scatter_label = QLabel("Select Scatter:")
        self.scatter_dropdown = QComboBox()
        container = self.add_tooltip(self.scatter_dropdown, parameter = "scatter_channel")
        self.form_layout.addRow(self.scatter_label, container)

    def add_cluster_key_input(self):
        self.cluster_key_label = QLabel("Select clusters:")
        self.cluster_key_dropdown = QComboBox()
        self.cluster_key_dropdown.currentIndexChanged.connect(self.update_cluster_selection_dropdown)
        container = self.add_tooltip(self.cluster_key_dropdown, parameter = "cluster_key")
        self.form_layout.addRow(self.cluster_key_label, container)

    def update_cluster_selection_dropdown(self):
        if not hasattr(self, 'cluster_selection_dropdown'):
            return
        dataset_key = self.main_window.dataset_dropdown.currentText()
        dataset = self.main_window.DATASHACK.get(dataset_key, None)
        cluster_col = self.cluster_key_dropdown.currentText()
        self.cluster_selection_dropdown.clear()
        options = dataset.obs[cluster_col].unique().tolist()
        options = [str(entry) for entry in options]
        self.cluster_selection_dropdown.addItems(options)


    def add_cluster_selection_input(self):
        self.cluster_selection_label = QLabel("Select cluster to display:")
        self.cluster_selection_dropdown = QComboBox()
        container = self.add_tooltip(self.cluster_selection_dropdown, parameter = "cluster_selection")
        self.form_layout.addRow(self.cluster_selection_label, container)

    def add_colorby_input(self,
                          additional_parameters: Optional[list[str]] = None):
        if additional_parameters:
            self._additional_colorby = additional_parameters
        else:
            self._additional_colorby = []
        self.colorby_label = QLabel("Select color:")
        self.colorby_dropdown = QComboBox()
        container = self.add_tooltip(self.colorby_dropdown, parameter = "colorby")
        self.form_layout.addRow(self.colorby_label, container)

    def add_frequency_of_input(self):
        self.freq_of_gate_label = QLabel("Select parent:")
        self.freq_of_gate_dropdown = QComboBox()
        container = self.add_tooltip(self.freq_of_gate_dropdown, parameter = "freq_of")
        self.form_layout.addRow(self.freq_of_gate_label, container)

    def add_groupby_fold_change_input(self,
                                      label: str = "Group by (x-axis)"):
        self.group_by_fold_change_label = QLabel(label)
        self.group_by_fold_change_dropdown = QComboBox()
        self.group_by_fold_change_dropdown.currentIndexChanged.connect(self.update_group_selection_dropdown)
        container = self.add_tooltip(self.group_by_fold_change_dropdown, parameter = "groupby")
        self.form_layout.addRow(self.group_by_fold_change_label, container)

    def update_group_selection_dropdown(self):
        dataset_key = self.main_window.dataset_dropdown.currentText()
        dataset = self.main_window.DATASHACK.get(dataset_key, None)
        cluster_col = self.group_by_fold_change_dropdown.currentText()
        options = dataset.obs[cluster_col].unique().tolist()
        options = [str(entry) for entry in options]

        if hasattr(self, 'group1_dropdown'):
            self.group1_dropdown.clear()
            self.group1_dropdown.addItems(options)

        if hasattr(self, 'group2_dropdown'):
            self.group2_dropdown.clear()
            self.group2_dropdown.addItems(options)

    def add_group1_input(self):
        self.group1_label = QLabel("Select group 1:")
        self.group1_dropdown = QComboBox()
        container = self.add_tooltip(self.group1_dropdown, parameter = "group")
        self.form_layout.addRow(self.group1_label, container)

    def add_group2_input(self):
        self.group2_label = QLabel("Select group 2:")
        self.group2_dropdown = QComboBox()
        container = self.add_tooltip(self.group2_dropdown, parameter = "group")
        self.form_layout.addRow(self.group2_label, container)
    
    def add_marker_input(self):
        self.marker_label = QLabel("Select marker:")
        self.marker_dropdown = QComboBox()
        container = self.add_tooltip(self.marker_dropdown, parameter = "marker")
        self.form_layout.addRow(self.marker_label, container)

    def add_metadata_marker_input(self):
        self.metadata_marker_label = QLabel("Select marker:")
        self.metadata_marker_dropdown = QComboBox()
        container = self.add_tooltip(self.metadata_marker_dropdown, parameter = "metadata_marker")
        self.form_layout.addRow(self.metadata_marker_label, container)

    def add_groupby_input(self,
                          label: str = "Group by (x-axis)"):
        self.group_by_label = QLabel(label)
        self.group_by_dropdown = QComboBox()
        container = self.add_tooltip(self.group_by_dropdown, parameter = "groupby")
        self.form_layout.addRow(self.group_by_label, container)

    def add_splitby_input(self):
        self.split_by_label = QLabel("Color by:")
        self.split_by_dropdown = QComboBox()
        container = self.add_tooltip(self.split_by_dropdown, parameter = "splitby")
        self.form_layout.addRow(self.split_by_label, container)

    def add_stat_test_input(self):
        self.stat_test_label = QLabel("Stat test:")
        self.stat_test_dropdown = QComboBox()
        self.stat_test_dropdown.addItems(["Kruskal", "Wilcoxon", "None"])
        container = self.add_tooltip(self.stat_test_dropdown, parameter = "stat_test")
        self.form_layout.addRow(self.stat_test_label, container)

    def add_ridge_input(self):
        self.ridge_label = QLabel("As ridgeplot:")
        self.ridge_dropdown = QComboBox()
        self.ridge_dropdown.addItems(["True", "False"])
        container = self.add_tooltip(self.ridge_dropdown, parameter = "ridge")
        self.form_layout.addRow(self.ridge_label, container)

    def add_backend_input(self):
        self.backend_label = QLabel("Backend:")
        self.backend_dropdown = QComboBox()
        self.backend_dropdown.addItems(["matplotlib", "plotly"])
        container = self.add_tooltip(self.backend_dropdown, parameter = "backend")
        self.form_layout.addRow(self.backend_label, container)

    def add_metadata_annotation_input(self):
        self.metadata_annotation_label = QLabel("Annotate metadata:")
        self.metadata_annotation_dropdown = MultiSelectComboBox()
        container = self.add_tooltip(self.metadata_annotation_dropdown, parameter = "metadata_annotation")
        self.form_layout.addRow(self.metadata_annotation_label, container)

    def add_use_marker_input(self):
        self.use_marker_label = QLabel("Use marker channels only:")
        self.use_marker_dropdown = QComboBox()
        self.use_marker_dropdown.addItems(["True", "False"])
        container = self.add_tooltip(self.use_marker_dropdown, parameter = "use_markers_only")
        self.form_layout.addRow(self.use_marker_label, container)

    def add_exclude_channels_input(self):
        self.exclude_channels_label = QLabel("Exclude channels:")
        self.exclude_channels_dropdown = MultiSelectComboBox()
        container = self.add_tooltip(self.exclude_channels_dropdown, parameter = "exclude")
        self.form_layout.addRow(self.exclude_channels_label, container)

    def add_correlation_method_input(self):
        self.corr_method_label = QLabel("Correlation method:")
        self.corr_method_dropdown = QComboBox()
        self.corr_method_dropdown.addItems(["pearson", "spearman", "kendall"])
        container = self.add_tooltip(self.corr_method_dropdown, parameter = "corr_method")
        self.form_layout.addRow(self.corr_method_label, container)

    def add_data_metric_input(self):
        self.data_metric_label = QLabel("Calculated on:")
        self.data_metric_dropdown = QComboBox()
        self.data_metric_dropdown.addItems(["mfi", "fop"])
        container = self.add_tooltip(self.data_metric_dropdown, parameter = "data_metric")
        self.form_layout.addRow(self.data_metric_label, container)

    def add_normalize_input(self):
        self.normalize_label = QLabel("Normalize:")
        self.normalize_dropdown = QComboBox()
        self.normalize_dropdown.addItems(["True", "False"])
        container = self.add_tooltip(self.normalize_dropdown, parameter = "normalize")
        self.form_layout.addRow(self.normalize_label, container)

    def add_cluster_method_input(self):
        self.cluster_method_label = QLabel("Cluster metric:")
        self.cluster_method_dropdown = QComboBox()
        self.cluster_method_dropdown.addItems(["correlation", "distance"])
        container = self.add_tooltip(self.cluster_method_dropdown, parameter = "cluster_method")
        self.form_layout.addRow(self.cluster_method_label, container)

    def add_dimred_samplewise_input(self):
        self.samplewise_dimred_label = QLabel("Dimensionality Reduction:")
        self.samplewise_dimred_dropdown = QComboBox()
        self.samplewise_dimred_dropdown.addItems(["PCA", "MDS", "TSNE", "UMAP"])
        container = self.add_tooltip(self.samplewise_dimred_dropdown, parameter = "dimred")
        self.form_layout.addRow(self.samplewise_dimred_label, container)

    def add_dimred_input(self):
        self.dimred_label = QLabel("Dimensionality Reduction:")
        self.dimred_dropdown = QComboBox()
        self.dimred_dropdown.addItems(["PCA", "DMAP", "TSNE", "UMAP"])
        container = self.add_tooltip(self.dimred_dropdown, parameter = "dimred")
        self.form_layout.addRow(self.dimred_label, container)

    def add_data_parameters_label(self):
        data_parameters_label = QLabel("<b>Data Parameters</b>")
        data_parameters_label.setContentsMargins(0, 0, 0, 0)
        data_parameters_label.setFixedHeight(50)
        self.scroll_layout.addWidget(data_parameters_label)

    def add_scaling_input(self):
        self.scaling_label = QLabel("Scale data:")
        self.scaling_dropdown = QComboBox()
        self.scaling_dropdown.addItems(["MinMaxScaler", "StandardScaler", "RobustScaler", "None"])
        container = self.add_tooltip(self.scaling_dropdown, parameter = "scaling")
        self.form_layout.addRow(self.scaling_label, container)

    def add_buttons(self):
        self.render_button = QPushButton("Render\nPlot")
        self.download_plot_button = QPushButton("Download\nPlot")
        self.download_data_button = QPushButton("Download\nRaw Data")

        self.render_button.clicked.connect(self.render_plot)
        self.download_plot_button.clicked.connect(self.download_plot)
        self.download_data_button.clicked.connect(self.download_raw_data)

        # Arrange buttons horizontally
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.render_button)
        button_layout.addWidget(self.download_plot_button)
        button_layout.addWidget(self.download_data_button)
        self.scroll_layout.addLayout(button_layout)

    def add_layout_parameters(self,
                              show_title: bool = True,
                              show_xlabel: bool = True,
                              show_ylabel: bool = True):
        """
        Adds layout parameters section.
        """
        self.layout_parameters_checkbox = QCheckBox("Show Layout Parameters")
        self.layout_parameters_checkbox.stateChanged.connect(self.toggle_layout_parameters)
        self.scroll_layout.addWidget(self.layout_parameters_checkbox)

        self.layout_parameters_group = QGroupBox("Layout Parameters")

        self.layout_parameters_layout = QFormLayout()

        self.layout_parameters_group.setLayout(self.layout_parameters_layout)
        self.layout_parameters_group.setVisible(False)
    
        if show_title:
            self.title_label = QLabel("Title:")
            self.title_input = QLineEdit()
            title_container = self.add_tooltip(self.title_input, parameter = "plot_title")
            self.layout_parameters_layout.addRow(self.title_label, title_container)

        if show_xlabel:
            self.xlabel_label = QLabel("X-axis label:")
            self.xlabel_input = QLineEdit()
            xlabel_container = self.add_tooltip(self.xlabel_input, parameter = "plot_axis_label")
            self.layout_parameters_layout.addRow(self.xlabel_label, xlabel_container)

        if show_ylabel:
            self.ylabel_label = QLabel("Y-axis label:")
            self.ylabel_input = QLineEdit()
            ylabel_container = self.add_tooltip(self.ylabel_input, parameter = "plot_axis_label")
            self.layout_parameters_layout.addRow(self.ylabel_label, ylabel_container)

        self.scroll_layout.addWidget(self.layout_parameters_group)

    def add_fontsize_parameters(self,
                                show_title: bool = True,
                                show_xlabel: bool = True,
                                show_ylabel: bool = True,
                                show_xticklabel: bool = True,
                                show_yticklabel: bool = True):
        """
        Adds font size parameters section.
        """
        self.fontsize_parameters_checkbox = QCheckBox("Show Font Size Parameters")
        self.fontsize_parameters_checkbox.stateChanged.connect(self.toggle_fontsize_parameters)
        self.scroll_layout.addWidget(self.fontsize_parameters_checkbox)

        self.fontsize_parameters_group = QGroupBox("Font Sizes")
        self.fontsize_parameters_layout = QFormLayout()
        self.fontsize_parameters_group.setLayout(self.fontsize_parameters_layout)
        self.fontsize_parameters_group.setVisible(False)
        self.scroll_layout.addWidget(self.fontsize_parameters_group)

        # Title font size
        if show_title:
            self.title_fontsize_label = QLabel("Title font size:")
            self.title_fontsize_input = QLineEdit()
            title_container = self.add_tooltip(self.title_fontsize_input, parameter = "title_fontsize")
            self.fontsize_parameters_layout.addRow(self.title_fontsize_label, title_container)

        # X-axis label font size
        if show_xlabel:
            self.xlabel_fontsize_label = QLabel("X label font size:")
            self.xlabel_fontsize_input = QLineEdit()
            xlabel_container = self.add_tooltip(self.xlabel_fontsize_input, parameter = "axis_label_fontsize")
            self.fontsize_parameters_layout.addRow(self.xlabel_fontsize_label, xlabel_container)

        # Y-axis label font size
        if show_ylabel:
            self.ylabel_fontsize_label = QLabel("Y label font size:")
            self.ylabel_fontsize_input = QLineEdit()
            ylabel_container = self.add_tooltip(self.ylabel_fontsize_input, parameter = "axis_label_fontsize")
            self.fontsize_parameters_layout.addRow(self.ylabel_fontsize_label, ylabel_container)

        # X tick labels font size
        if show_xticklabel:
            self.xticklabels_fontsize_label = QLabel("X tick labels font size:")
            self.xticklabels_fontsize_input = QLineEdit()
            xticklabel_container = self.add_tooltip(self.xticklabels_fontsize_input, parameter = "axis_ticklabel_fontsize")
            self.fontsize_parameters_layout.addRow(self.xticklabels_fontsize_label, xticklabel_container)

        # Y tick labels font size
        if show_yticklabel:
            self.yticklabels_fontsize_label = QLabel("Y tick labels font size:")
            self.yticklabels_fontsize_input = QLineEdit()
            yticklabel_container = self.add_tooltip(self.yticklabels_fontsize_input, parameter = "axis_ticklabel_fontsize")
            self.fontsize_parameters_layout.addRow(self.yticklabels_fontsize_label, yticklabel_container)

    def add_dot_parameters(self,
                           label: str = "Show Dot Parameters",
                           show_dot_size: bool = True,
                           show_linewidth: bool = True,
                           show_linecolor: bool = True,
                           show_cmap: bool = True):
        """
        Adds dot parameters section.
        """
        self.dot_parameters_checkbox = QCheckBox(label)
        self.dot_parameters_checkbox.stateChanged.connect(self.toggle_dot_parameters)
        self.scroll_layout.addWidget(self.dot_parameters_checkbox)

        self.dot_parameters_group = QGroupBox("Dot Parameters")
        self.dot_parameters_layout = QFormLayout()
        self.dot_parameters_group.setLayout(self.dot_parameters_layout)
        self.dot_parameters_group.setVisible(False)
        self.scroll_layout.addWidget(self.dot_parameters_group)

        if show_dot_size:
            self.dot_size_label = QLabel("Dot size:")
            self.dot_size_input = QLineEdit()
            dot_size_container = self.add_tooltip(self.dot_size_input, parameter = "dotsize")
            self.dot_parameters_layout.addRow(self.dot_size_label, dot_size_container)

        if show_linewidth:
            self.dot_linewidth_label = QLabel("Linewidth:")
            self.dot_linewidth_input = QLineEdit()
            dot_linewidth_container = self.add_tooltip(self.dot_linewidth_input, parameter = "dot_linewidth")
            self.dot_parameters_layout.addRow(self.dot_linewidth_label, dot_linewidth_container)

        if show_linecolor:
            self.dot_linecolor_label = QLabel("Linecolor:")
            self.dot_linecolor_input = QLineEdit()
            dot_linecolor_container = self.add_tooltip(self.dot_linecolor_input , parameter = "dot_linecolor")
            self.dot_parameters_layout.addRow(self.dot_linecolor_label, dot_linecolor_container)

        if show_cmap:
            self.colormap_label = QLabel("Colormap:")
            self.colormap_dropdown = QComboBox()
            self.colormap_dropdown.addItems(CATEGORICAL_CMAPS + CONTINUOUS_CMAPS)
            cmap_container = self.add_tooltip(self.colormap_dropdown, parameter = "cmap")
            self.dot_parameters_layout.addRow(self.colormap_label, cmap_container)

    def add_aspect_parameters(self):
        """
        adds parameters to control the color scale
        """
        self.aspect_parameters_checkbox = QCheckBox("Show Aspect Parameters")
        self.aspect_parameters_checkbox.stateChanged.connect(self.toggle_aspect_parameters)
        self.scroll_layout.addWidget(self.aspect_parameters_checkbox)

        self.aspect_parameters_group = QGroupBox("Aspect Parameters")
        self.aspect_parameters_layout = QFormLayout()
        self.aspect_parameters_group.setLayout(self.aspect_parameters_layout)
        self.aspect_parameters_group.setVisible(False)
        self.scroll_layout.addWidget(self.aspect_parameters_group)

        # Plot Height
        self.plot_height_label = QLabel("Plot Height:")
        self.plot_height_input = QLineEdit()
        plot_height_container = self.add_tooltip(self.plot_height_input, parameter = "plot_height")
        self.aspect_parameters_layout.addRow(self.plot_height_label, plot_height_container)

        # Plot Aspect
        self.plot_aspect_label = QLabel("Plot Aspect:")
        self.plot_aspect_input = QLineEdit()
        plot_aspect_container = self.add_tooltip(self.plot_aspect_input, parameter = "plot_aspect")
        self.aspect_parameters_layout.addRow(self.plot_aspect_label, plot_aspect_container)

        # Plot Spacing
        self.plot_spacing_label = QLabel("Plot Spacing:")
        self.plot_spacing_input = QLineEdit()
        plot_spacing_container = self.add_tooltip(self.plot_spacing_input, parameter = "plot_spacing")
        self.aspect_parameters_layout.addRow(self.plot_spacing_label, plot_spacing_container)

    def add_xscale_parameters(self):
        """
        adds parameters to control the color scale
        """
        self.xscale_parameters_checkbox = QCheckBox("Show X scale Parameters")
        self.xscale_parameters_checkbox.stateChanged.connect(self.toggle_xscale_parameters)
        self.scroll_layout.addWidget(self.xscale_parameters_checkbox)

        self.xscale_parameters_group = QGroupBox("X Axis Parameters")
        self.xscale_parameters_layout = QFormLayout()
        self.xscale_parameters_group.setLayout(self.xscale_parameters_layout)
        self.xscale_parameters_group.setVisible(False)
        self.scroll_layout.addWidget(self.xscale_parameters_group)

        self.xscale_label = QLabel("Scale:")
        self.xscale_dropdown = QComboBox()
        container = self.add_tooltip(self.xscale_dropdown, parameter = "axis_scale")
        self.xscale_parameters_layout.addRow(self.xscale_label, container)

    def add_yscale_parameters(self):
        """
        adds parameters to control the color scale
        """
        self.yscale_parameters_checkbox = QCheckBox("Show Y scale Parameters")
        self.yscale_parameters_checkbox.stateChanged.connect(self.toggle_yscale_parameters)
        self.scroll_layout.addWidget(self.yscale_parameters_checkbox)

        self.yscale_parameters_group = QGroupBox("Y Axis Parameters")
        self.yscale_parameters_layout = QFormLayout()
        self.yscale_parameters_group.setLayout(self.yscale_parameters_layout)
        self.yscale_parameters_group.setVisible(False)
        self.scroll_layout.addWidget(self.yscale_parameters_group)

        self.yscale_label = QLabel("Scale:")
        self.yscale_dropdown = QComboBox()
        container = self.add_tooltip(self.yscale_dropdown, parameter = "axis_scale")
        self.yscale_parameters_layout.addRow(self.yscale_label, container)

    def add_colorscale_parameters(self,
                                  show_scale: bool = True,
                                  show_vmin: bool = True,
                                  show_vmax: bool = True):
        """
        adds parameters to control the color scale
        """
        self.colorscale_parameters_checkbox = QCheckBox("Show Colorscale Parameters")
        self.colorscale_parameters_checkbox.stateChanged.connect(self.toggle_colorscale_parameters)
        self.scroll_layout.addWidget(self.colorscale_parameters_checkbox)

        self.colorscale_parameters_group = QGroupBox("Color Scale Parameters")
        self.colorscale_parameters_layout = QFormLayout()
        self.colorscale_parameters_group.setLayout(self.colorscale_parameters_layout)
        self.colorscale_parameters_group.setVisible(False)
        self.scroll_layout.addWidget(self.colorscale_parameters_group)

        if show_scale:
            self.colorscale_label = QLabel("Scale:")
            self.colorscale_dropdown = QComboBox()
            colorscale_container = self.add_tooltip(self.colorscale_dropdown, parameter = "color_scale")
            self.colorscale_parameters_layout.addRow(self.colorscale_label, colorscale_container)

        # VMIN
        if show_vmin:
            self.vmin_label = QLabel("vmin:")
            self.vmin_input = QLineEdit()
            vmin_container = self.add_tooltip(self.vmin_input, parameter = "vmin")
            self.colorscale_parameters_layout.addRow(self.vmin_label, vmin_container)

        # VMAX
        if show_vmax:
            self.vmax_label = QLabel("vmax:")
            self.vmax_input = QLineEdit()
            vmax_container = self.add_tooltip(self.vmax_input, parameter = "vmax")
            self.colorscale_parameters_layout.addRow(self.vmax_label, vmax_container)
        
    def add_continous_cmaps_input(self):
        self.continuous_colormap_label = QLabel("Colormap:")
        self.continuous_colormap_dropdown = QComboBox()
        self.continuous_colormap_dropdown.addItems(CONTINUOUS_CMAPS)
        container = self.add_tooltip(self.continuous_colormap_dropdown, parameter = "cmap")
        self.form_layout.addRow(self.continuous_colormap_label, container)

    def add_full_cmaps_input(self):
        self.full_colormap_label = QLabel("Colormap:")
        self.full_colormap_dropdown = QComboBox()
        self.full_colormap_dropdown.addItems(CATEGORICAL_CMAPS + CONTINUOUS_CMAPS)
        container = self.add_tooltip(self.full_colormap_dropdown, parameter = "cmap")
        self.form_layout.addRow(self.full_colormap_label, container)

    def toggle_layout_parameters(self):
        """
        Toggles the visibility of the layout parameters section.
        """
        self.layout_parameters_group.setVisible(self.layout_parameters_checkbox.isChecked())
        self.submenu_opened.emit(
            self.layout_parameters_group.sizeHint().height(),
            self.layout_parameters_group
        )

    def toggle_fontsize_parameters(self):
        """
        Toggles the visibility of the font size parameters section.
        """
        self.fontsize_parameters_group.setVisible(self.fontsize_parameters_checkbox.isChecked())
        self.submenu_opened.emit(
            self.fontsize_parameters_group.sizeHint().height(),
            self.fontsize_parameters_group
        )

    def toggle_dot_parameters(self):
        """
        Toggles the visibility of the dot parameters section.
        """
        self.dot_parameters_group.setVisible(self.dot_parameters_checkbox.isChecked())
        self.submenu_opened.emit(
            self.dot_parameters_group.sizeHint().height(),
            self.dot_parameters_group
        )

    def toggle_aspect_parameters(self):
        """
        Toggles the visibility of the dot parameters section.
        """
        self.aspect_parameters_group.setVisible(self.aspect_parameters_checkbox.isChecked())
        self.submenu_opened.emit(
            self.aspect_parameters_group.sizeHint().height(),
            self.aspect_parameters_group
        )

    def toggle_colorscale_parameters(self):
        """
        Toggles the visibility of the colorscale parameters section.
        """
        self.colorscale_parameters_group.setVisible(self.colorscale_parameters_checkbox.isChecked())
        self.submenu_opened.emit(
            self.colorscale_parameters_group.sizeHint().height(),
            self.colorscale_parameters_group
        )

    def toggle_xscale_parameters(self):
        """
        Toggles the visibility of the colorscale parameters section.
        """
        self.xscale_parameters_group.setVisible(self.xscale_parameters_checkbox.isChecked())
        self.submenu_opened.emit(
            self.xscale_parameters_group.sizeHint().height(),
            self.xscale_parameters_group
        )

    def toggle_yscale_parameters(self):
        """
        Toggles the visibility of the colorscale parameters section.
        """
        self.yscale_parameters_group.setVisible(self.yscale_parameters_checkbox.isChecked())
        self.submenu_opened.emit(
            self.yscale_parameters_group.sizeHint().height(),
            self.yscale_parameters_group
        )

    def download_plot(self):
        """
        Trigger the save plot functionality in the PlotWindow.
        """
        if hasattr(self.main_window.plot_window.current_plot_widget, 'save_plot'):
            self.main_window.plot_window.current_plot_widget.save_plot()
        else:
            self.show_error_dialog("Saving is not supported for this plot.")

    def download_raw_data(self):
        """
        Trigger the save data functionality in the PlotWindow.
        """

        plot_config = self.generate_plot_config()
        if hasattr(self.main_window.plot_window.current_plot_widget, 'save_raw_data'):
            self.main_window.plot_window.current_plot_widget.save_raw_data(plot_config)
        else:
            self.show_error_dialog("Saving of the raw data was not successful.")

    def show_error(self, title, message):
        """
        Displays an error message in a QMessageBox.
        """
        error_dialog = QMessageBox(self)
        error_dialog.setStyleSheet(self.main_window.stylesheet)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def show_error_dialog(self, message):
        """
        Displays an error dialog with the provided message.
        """
        error_dialog = QMessageBox(self)
        error_dialog.setStyleSheet(self.main_window.stylesheet)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec_()

    def add_tooltip(self,
                    widget: QWidget,
                    parameter: str) -> QHBoxLayout:
        tooltip = HoverLabel(
            dimension = widget.sizeHint().height(),
            hover_info = self._documentation[parameter],
            darkmode = self.main_window.is_dark
        )
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.addWidget(widget)
        container_layout.addWidget(tooltip)
        container_layout.setContentsMargins(0,0,0,0)
        container_layout.setSpacing(10)
        container.setLayout(container_layout)

        return container

    def enable_documentation(self):
        self._documentation = {
            "gate":
                "Specify the population that is used for the plot.",
            "layer":
                "Specify the data to be plotted.",
            "sample_size":
                "Specify how many events you want to plot.",
            "channel":
                "Specify the channel to be plotted.",
            "sample_identifier":
                "Choose the sample_ID or file_name that corresponds to the " +
                "sample you want to plot.",
            "scatter_channel":
                "Specify which channel should be plotted on the y-axis.",
            "cluster_key":
                "Specifies the name of the cluster annotations.",
            "cluster_selection":
                "Specify which cluster you want to use to display data from.",
            "colorby":
                "Choose the coloring of the plot.",
            "freq_of":
                "Choose the parent gate of which the frequency is calculated.",
            "groupby":
                "Choose the grouping to be analyzed.",
            "group":
                "Choose a group that should be compared against.",
            "marker":
                "Specify the channel that is displayed.",
            "metadata_marker":
                "Specify the channel that is displayed. It must be a numeric variable.",
            "splitby":
                "Choose the variable to split the plot by. Can be the same as " +
                "'groupby', in which case only the 'groupby' variable will be " +
                "used on the x-axis.",
            "stat_test":
                "Specify the statistical test that is applied and displayed. If " +
                "set to 'None', no statistical analysis will be performed.",
            "ridge":
                "If True, the plot will be displayed as an overlaying ridge-plot " +
                "instead of a line plot.",
            "backend":
                "Plots will be rendered according to the backend. matplotlib offers " +
                "publication-ready, high resolution plots, while plotly allows " +
                "for interactive visualization of the metadata on the respective " +
                "data points.",
            "metadata_annotation":
                "Specify which metadata are used for the column annotation. The " +
                "entries will be colorcoded and displayed as small bars adjacent " +
                "to the columns of the heatmap.",
            "use_markers_only":
                "If set to True, the display will only be applied to " +
                "channels that contain marker proteins. This will exclude " +
                "channels such as 'FSC', 'SSC' or technical channels in " +
                "CyTOF.",
            "exclude":
                "Specify channels that are excluded from the plotting. This " +
                "could be a live/dead stain or other uninformative markers. ",
            "corr_method":
                "Specify the method of correlation of the data. Can be 'pearson' " +
                "'spearman' or 'kendall'.",
            "data_metric":
                "Specifies whether to show the intensity values " +
                "(mfi) or the frequency of positives (fop).",
            "normalize":
                "Normalization will scale the data between 0 and 1 and display " +
                "them as a percentage, while no " +
                "normalization will display the raw counts.",
            "cluster_method":
                "The method used to cluster the heatmap data. If clustered by " +
                "'correlation', the correlation coefficients will be used. If " +
                "'distance', the euclidean distance of the samples will be used",
            "dimred":
                "Specify the dimensionality reduction to be displayed.",
            "scaling":
                "Controls whether to apply scaling to the plot data. 'MinMaxScaler' " +
                "scales the data between 0 and 1, while  StandardScaler performs " +
                "Z-scaling. For further information refer to the scikit-learn documentation. ",
            "plot_title":
                "Enter the plot title to be displayed.",
            "plot_axis_label":
                "Enter the axis label to be displayed.",
            "title_fontsize":
                "Enter the fontsize to control the label height of the title.",
            "axis_label_fontsize":
                "Enter the fontsize to control the label height of the axis label.",
            "axis_ticklabel_fontsize":
                "Enter the fontsize to control the label height of the individual tick labels.",
            "dotsize":
                "Controls the size of the data points.",
            "dot_linewidth":
                "Controls the thickness of the line surrounding the data points.",
            "dot_linecolor":
                "Controls the color of the line surrounding the data points.",
            "cmap":
                "Choose the colormap to use. There are categorical and continuous colormaps " +
                "that have to be specified based on the coloring variable you chose. The " +
                "categorical colormaps are 'Set1', 'Set2', 'Set3', 'tab10', 'Paired' and 'hls' " +
                "while the other ones are continuous.",
            "plot_height":
                "Controls the height of the total plot. Use in conjunction with 'aspect' to " +
                "control the overlap of the individual ridges. ",
            "plot_aspect":
                "Controls the aspect of the total plot. Use in conjunction with 'height' to " +
                "control the overlap of the individual ridges. ",
            "plot_spacing":
                "Controls the spacing of the individual plots. Use in conjunction with 'height' to " +
                "control the overlap of the individual ridges. ",
            "axis_scale":
                "Controls the scaling of the axis. Can be 'linear', 'log' or 'biex'. In the " +
                "latter case, the axis will have a linear region and a log region.",
            "color_scale":
                "Controls the scale of the color bar. Can be 'linear', 'log' or 'biex'. In the " +
                "latter case, the axis will have a linear region and a log region.",
            "vmin":
                "Sets the lowest intensity value to be displayed on the colorscale.",
            "vmax":
                "Sets the highest intensity value to be displayed on the colorscale.",

        }


