
import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from matplotlib import pyplot as plt

from . import PlotWindowFunctionGeneric, BaseConfigPanel

class ConfigPanelFoldChange(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_layer_input()
        self.add_gate_input()
        self.add_groupby_fold_change_input(label = "Group By")
        self.add_group1_input()
        self.add_group2_input()

        self.add_data_metric_input()

        self.add_layout_parameters()

        self.add_fontsize_parameters()

        self.add_dot_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowFoldChange(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self._plot_func = fp.pl.fold_change

    def _instantiate_parameters(self,
                                plot_config,
                                dataset,
                                ax = None):
        self._raw_config = {
            "adata": dataset,
            "gate": plot_config.get("gate"),
            "layer": plot_config.get("layer"),
            "groupby": plot_config.get("groupby"),
            "group1": plot_config.get("group1"),
            "group2": plot_config.get("group2"),
            "cmap": plot_config.get("cmap"),
            "data_metric": plot_config.get("data_metric"),
            "ax": ax,
            "show": False
        }

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
