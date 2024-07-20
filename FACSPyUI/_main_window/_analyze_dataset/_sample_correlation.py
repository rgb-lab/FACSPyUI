import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from . import PlotWindowFunctionGeneric, BaseConfigPanel


class ConfigPanelSampleCorrelation(BaseConfigPanel):
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

        self.add_correlation_method_input()

        self.add_data_metric_input()

        self.add_continous_cmaps_input()

        self.add_layout_parameters()

        self.add_fontsize_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowSampleCorrelation(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self.no_tight_layout_upon_resizing = True

    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()
        xticklabel_fontsize = plot_config.get("xticklabel_fontsize")
        if not xticklabel_fontsize:
            plot_config["xticklabel_fontsize"] = 12
        yticklabel_fontsize = plot_config.get("yticklabel_fontsize")
        if not yticklabel_fontsize:
            plot_config["yticklabel_fontsize"] = 12
        try:
            fig = fp.pl.sample_correlation(
                dataset,
                gate=plot_config.get("gate"),
                layer=plot_config.get("layer"),
                metadata_annotation=plot_config.get("metadata_annotation"),
                include_technical_channels = True,
                exclude=plot_config.get("exclude"),
                scaling=plot_config.get("scaling"),
                data_metric=plot_config.get("data_metric"),
                corr_method=plot_config.get("corr_method"),
                cmap = plot_config.get("cmap"),
                show=False,
                return_fig=True,
            )
            ax = fig.ax_heatmap
            self._apply_layout_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")
