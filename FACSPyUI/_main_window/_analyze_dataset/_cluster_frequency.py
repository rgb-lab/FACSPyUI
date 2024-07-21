import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from matplotlib import pyplot as plt

from . import PlotWindowFunctionGeneric, BaseConfigPanel

class ConfigPanelClusterFrequency(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_gate_input()
        self.add_cluster_key_input()
        self.add_cluster_selection_input()
        self.add_groupby_input()
        self.add_splitby_input()
        self.add_stat_test_input()
        self.add_normalize_input()

        self.add_layout_parameters()

        self.add_fontsize_parameters()
        self.add_dot_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowClusterFrequency(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self._plot_func = fp.pl.cluster_frequency

    def _instantiate_parameters(self,
                                plot_config,
                                dataset,
                                ax = None):
        self._raw_config = {
            "adata": dataset,
            "gate": plot_config.get("gate"),
            "groupby": plot_config.get("groupby"),
            "splitby": plot_config.get("splitby"),
            "cluster_key": plot_config.get("cluster_key"),
            "cluster": plot_config.get("cluster"),
            "stat_test": plot_config.get("stat_test"),
            "cmap": plot_config.get("cmap"),
            "ax": ax,
            "show": False
        }
        normalization_kwargs = {}
        normalize = plot_config.get("normalize")
        if normalize:
            normalization_kwargs["normalize"] = normalize == "True"
        self._normalization_kwargs = normalization_kwargs
        if self._raw_config.get("splitby") == self._raw_config.get("groupby"):
            self._raw_config["splitby"] = None
        if self._raw_config.get("stat_test") == "None":
            self._raw_config["stat_test"] = None

    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()

        try:
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            self._instantiate_parameters(plot_config, dataset, ax)
            ax = self._plot_func(**self._raw_config, **self._normalization_kwargs)
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")

