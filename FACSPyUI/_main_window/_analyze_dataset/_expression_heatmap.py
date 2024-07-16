import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from . import PlotWindowFunctionGeneric, BaseConfigPanel


class ConfigPanelExpressionHeatmap(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_layer_input()
        self.add_gate_input()

        self.add_metadata_annotation_input()

        self.add_use_marker_input()
        self.add_exclude_channels_input()

        self.add_scaling_input()

        self.add_cluster_method_input()

        self.add_correlation_method_input()

        self.add_data_metric_input()

        self.add_continous_cmaps_input()


        # Add layout parameters section
        self.add_layout_parameters()

        # Add font size parameters section
        self.add_fontsize_parameters()

        # Add stretch to keep layout parameters aligned
        self.scroll_layout.addStretch()

        # Buttons
        self.add_buttons()

        self.setLayout(self.main_layout)

        # Populate dropdowns
        self.populate_dropdowns()



class PlotWindowExpressionHeatmap(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self.no_tight_layout_upon_resizing = True

    def generate_matplotlib(self, plot_config):
        """
        Generates a plot using fp.pl.marker_correlation function.
        """
        dataset = self.retrieve_dataset()
        xticklabel_fontsize = plot_config.get("xticklabel_fontsize")
        if not xticklabel_fontsize:
            plot_config["xticklabel_fontsize"] = 12
        yticklabel_fontsize = plot_config.get("yticklabel_fontsize")
        if not yticklabel_fontsize:
            plot_config["yticklabel_fontsize"] = 12
        # Generate the figure using your custom function
        include_technicals = plot_config.get("include_technical_channels") == "True"
        include_technicals = not include_technicals
        try:
            fig = fp.pl.expression_heatmap(
                dataset,
                gate=plot_config.get("gate"),
                layer=plot_config.get("layer"),
                metadata_annotation=plot_config.get("metadata_annotation"),
                include_technical_channels = include_technicals,
                exclude=plot_config.get("exclude"),
                scaling=plot_config.get("scaling"),
                data_metric=plot_config.get("data_metric"),
                corr_method=plot_config.get("corr_method"),
                cluster_method=plot_config.get("cluster_method"),
                cmap = plot_config.get("cmap"),
                show=False,
                return_fig=True,
            )
            ax = fig.ax_heatmap
            self._apply_layout_parameters_matplotlib(ax, plot_config)

            self.current_plot_widget = FigureCanvas(fig.fig)
            self.layout.addWidget(self.current_plot_widget)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot with fp.pl.expression_heatmap: {e}")
