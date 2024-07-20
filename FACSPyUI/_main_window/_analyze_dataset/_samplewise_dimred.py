import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout
from matplotlib import pyplot as plt

from . import PlotWindowFunctionGeneric, BaseConfigPanel


class ConfigPanelSamplewiseDimred(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_dimred_samplewise_input()

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



class PlotWindowSamplewiseDimred(PlotWindowFunctionGeneric):
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
            reduction = plot_config.get("reduction")
            if reduction == "PCA":
                plot_func = fp.pl.pca_samplewise
            elif reduction == "MDS":
                plot_func = fp.pl.mds_samplewise
            elif reduction == "TSNE":
                plot_func = fp.pl.tsne_samplewise
            else:
                assert reduction == "UMAP"
                plot_func = fp.pl.umap_samplewise


            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            
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

            ax = plot_func(
                dataset,
                gate=plot_config.get("gate"),
                layer=plot_config.get("layer"),
                color=plot_config.get("color"),
                data_metric=plot_config.get("data_metric"),
                cmap=plot_config.get("cmap"),
                ax = ax,
                show=False,
                **scale_kwargs
            )
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")

