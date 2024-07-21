import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout
from matplotlib import pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from . import PlotWindowFunctionGeneric, BaseConfigPanel


class ConfigPanelSinglecellDimred(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_dimred_input()

        self.add_layer_input()
        self.add_gate_input()

        self.add_colorby_input()

        self.add_data_metric_input()

        self.add_layout_parameters()

        self.add_fontsize_parameters()

        self.add_dot_parameters()

        self.add_colorscale_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowSinglecellDimred(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self._plot_func = None

    def _instantiate_parameters(self,
                                plot_config,
                                dataset,
                                ax = None):
        reduction = plot_config.get("reduction")
        if reduction == "PCA":
            plot_func = fp.pl.pca
        elif reduction == "DMAP":
            plot_func = fp.pl.diffmap
        elif reduction == "TSNE":
            plot_func = fp.pl.tsne
        else:
            assert reduction == "UMAP"
            plot_func = fp.pl.umap

        self._plot_func = plot_func

        self._raw_config = {
            "adata": dataset,
            "gate": plot_config.get("gate"),
            "layer": plot_config.get("layer"),
            "color": plot_config.get("color"),
            "cmap": plot_config.get("cmap"),
            "ax": ax,
            "show": False,
        }
        vmin = plot_config.get("vmin")
        vmax = plot_config.get("vmax")
        color_scale = plot_config.get("color_scale")
        scale_kwargs = {}
        if vmin:
            scale_kwargs["vmin"] = float(vmin)
        if vmax:
            scale_kwargs["vmax"] = float(vmax)
        if color_scale:
            scale_kwargs["color_scale"] = color_scale

        self._scale_kwargs = scale_kwargs


    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()

        try:
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            self._instantiate_parameters(plot_config, dataset, ax)
            assert self._plot_func is not None, "no plot func defined"
            ax = self._plot_func(**self._raw_config, **self._scale_kwargs)
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)
        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")
