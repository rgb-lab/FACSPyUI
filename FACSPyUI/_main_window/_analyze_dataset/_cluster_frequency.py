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
        self.main_window = main_window  # Store reference to the main window

    def generate_matplotlib(self, plot_config):
        """
        Generates a plot using fp.pl.mfi function.
        """
        dataset = self.retrieve_dataset()

        try:
            splitby = plot_config.get("splitby")
            groupby = plot_config.get("groupby")
            stat_test = plot_config.get("stat_test")

            normalization_kwargs = {}
            normalize = plot_config.get("normalize")
            if normalize:
                normalization_kwargs["normalize"] = normalize == "True"

            if stat_test == "None":
                stat_test = None
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            ax = fp.pl.cluster_frequency(
                dataset,
                gate=plot_config.get("gate"),
                groupby=groupby,
                splitby=splitby if splitby != groupby else None,
                cluster_key=plot_config.get("cluster_key"),
                cluster=plot_config.get("cluster"),
                stat_test = stat_test,
                cmap = plot_config.get("cmap"),
                ax = ax,
                show=False,
                **normalization_kwargs
            )
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)


        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot with fp.pl.mfi: {e}")

