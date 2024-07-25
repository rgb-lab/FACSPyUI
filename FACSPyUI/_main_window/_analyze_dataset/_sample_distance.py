import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from . import PlotWindowFunctionGeneric, BaseConfigPanel


class ConfigPanelSampleDistance(BaseConfigPanel):
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

        self.add_data_metric_input()

        self.add_continous_cmaps_input()

        # self.add_layout_parameters()

        # self.add_fontsize_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowSampleDistance(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.no_tight_layout_upon_resizing = True
        self._plot_func = fp.pl.sample_distance

    def _instantiate_parameters(self,
                                plot_config,
                                dataset,
                                ax = None):
        self._raw_config = {
            "adata": dataset,
            "gate": plot_config.get("gate"),
            "layer": plot_config.get("layer"),
            "metadata_annotation": plot_config.get("metadata_annotation"),
            "include_technical_channels": plot_config.get("include_technical_channels") != "True",
            "exclude": plot_config.get("exclude"),
            "scaling": plot_config.get("scaling"),
            "data_metric": plot_config.get("data_metric"),
            "cmap": plot_config.get("cmap"),
            "show": False,
            "return_fig": True,
        }

    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()
        try:
            xticklabel_fontsize = plot_config.get("xticklabel_fontsize")
            if not xticklabel_fontsize:
                plot_config["xticklabel_fontsize"] = 12
            yticklabel_fontsize = plot_config.get("yticklabel_fontsize")
            if not yticklabel_fontsize:
                plot_config["yticklabel_fontsize"] = 12

            self._instantiate_parameters(plot_config, dataset)
            fig = self._plot_func(**self._raw_config)
            ax = fig.ax_heatmap
            self._apply_layout_parameters_matplotlib(ax, plot_config)

            fig.fig.tight_layout()

            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")
