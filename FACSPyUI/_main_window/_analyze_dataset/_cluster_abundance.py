import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from matplotlib import pyplot as plt

from . import PlotWindowFunctionGeneric, BaseConfigPanel

class ConfigPanelClusterAbundance(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_groupby_input(label = "Group By")
        self.add_cluster_key_input()
        self.add_normalize_input()

        self.add_layout_parameters()

        self.add_fontsize_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowClusterAbundance(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self._plot_func = fp.pl.cluster_abundance

    def _instantiate_parameters(self,
                                plot_config,
                                dataset,
                                ax = None):
        self._raw_config = {
            "adata": dataset,
            "groupby": plot_config.get("groupby"),
            "cluster_key": plot_config.get("cluster_key"),
            "ax": ax,
            "show": False,
        }
        normalization_kwargs = {}
        normalize = plot_config.get("normalize")
        if normalize:
            normalization_kwargs["normalize"] = normalize == "True"
        self._normalization_kwargs = normalization_kwargs

    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()

        # Generate the figure using your custom function
        try:
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            self._instantiate_parameters(plot_config, dataset, ax)
            ax = self._plot_func(**self._raw_config, **self._normalization_kwargs)
            self._apply_layout_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot with fp.pl.mfi: {e}")
