import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout
from matplotlib import pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from . import PlotWindowFunctionGeneric, BaseConfigPanel

class ConfigPanelBiaxScatter(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_layer_input()
        self.add_gate_input()

        self.add_xchannel_input()
        self.add_ychannel_input()

        self.add_sample_identifier_input()

        self.add_colorby_input(additional_parameters = ["density"])

        self.add_layout_parameters()

        self.add_fontsize_parameters()

        self.add_dot_parameters()

        self.add_xscale_parameters()

        self.add_yscale_parameters()

        self.add_colorscale_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()


class PlotWindowBiaxScatter(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self._plot_func = fp.pl.biax

    def _instantiate_parameters(self,
                                plot_config: dict,
                                dataset,
                                ax = None) -> None:
        self._raw_config = {
            "adata": dataset, 
            "sample_identifier": plot_config.get("sample_identifier"),
            "gate": plot_config.get("gate"),
            "layer": plot_config.get("layer"),
            "x_channel": plot_config.get("x_channel"),
            "y_channel": plot_config.get("y_channel"),
            "color": plot_config.get("color"),
            "cmap": plot_config.get("cmap"),
            "ax": ax,
            "show": False,
            "return_fig": True
        }
        scale_kwargs = {}
        color_scale = plot_config.get("color_scale")
        x_scale = plot_config.get("x_scale")
        y_scale = plot_config.get("y_scale")
        vmin = plot_config.get("vmin")
        vmax = plot_config.get("vmax")
        scale_kwargs = {}
        if color_scale:
            scale_kwargs["color_scale"] = color_scale
        if x_scale:
            scale_kwargs["x_scale"] = x_scale
        if y_scale:
            scale_kwargs["y_scale"] = y_scale
        if vmax:
            scale_kwargs["vmax"] = float(vmax)
        if vmin:
            scale_kwargs["vmin"] = float(vmin)
        self._scale_kwargs = scale_kwargs


    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()
        try:
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            self._instantiate_parameters(plot_config, dataset, ax)
            ax = self._plot_func(**self._raw_config, **self._scale_kwargs)
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)
            
            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")
