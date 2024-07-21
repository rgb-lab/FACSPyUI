
import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from matplotlib import pyplot as plt

from . import PlotWindowFunctionGeneric, BaseConfigPanel, COLORMAPS

class ConfigPanelGateFrequency(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_gate_input()
        self.add_frequency_of_input()
        self.add_groupby_input()
        self.add_splitby_input()
        self.add_stat_test_input()
        self.add_backend_input()

        self.add_layout_parameters()

        self.add_fontsize_parameters()

        self.add_dot_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowGateFrequency(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self._plot_func = fp.pl.gate_frequency

    def _instantiate_parameters(self,
                                plot_config,
                                dataset,
                                ax = None):
        self._raw_config = {
            "adata": dataset,
            "gate": plot_config.get("gate"),
            "freq_of": plot_config.get("freq_of"),
            "groupby": plot_config.get("groupby"),
            "splitby": plot_config.get("splitby"),
            "stat_test": plot_config.get("stat_test"),
            "cmap": plot_config.get("cmap"),
            "ax": ax,
            "show": False
        }
        if self._raw_config.get("splitby") == self._raw_config.get("groupby"):
            self._raw_config["splitby"] = None
        if self._raw_config.get("stat_test") == "None":
            self._raw_config["stat_test"] = None


    def generate_plotly(self, plot_config):
        try:
            data = self.get_raw_data(plot_config)
            groupby = self._raw_config.get("groupby")
            splitby = self._raw_config.get("splitby")
            fig = self.render_stripboxplot_plotly(data = data,
                                                  x = groupby,
                                                  y = "freq",
                                                  color = splitby,
                                                  hover_data = {}, #hover_data = {col: True for col in dataset.obs.columns},
                                                  color_discrete_sequence = COLORMAPS[plot_config.get("cmap")])

            self._apply_layout_parameters_plotly(fig, plot_config)
            self._apply_dot_parameters_plotly(fig, plot_config)

            self._show_plotly(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Plotly plot: {str(e)}")

    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()

        try:
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            self._instantiate_parameters(plot_config, dataset, ax)
            ax = self._plot_func(**self._raw_config)
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)
            
            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")

