import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from matplotlib import pyplot as plt

from . import PlotWindowFunctionGeneric, BaseConfigPanel

class ConfigPanelMarkerDensity(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_layer_input()
        self.add_gate_input()
        self.add_marker_input()
        self.add_groupby_input(label = "Group By")
        self.add_splitby_input()

        # implement later
        # self.add_ridge_input()

        self.add_layout_parameters()

        self.add_fontsize_parameters()

        self.add_xscale_parameters()

        # implement later
        # self.add_aspect_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()



class PlotWindowMarkerDensity(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to the main window

    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()

        try:
            splitby = plot_config.get("splitby")
            groupby = plot_config.get("groupby")
            ridge = plot_config.get("ridge")
            plot_aspect = plot_config.get("plot_aspect")
            plot_height = plot_config.get("plot_height")
            plot_spacing = plot_config.get("plot_spacing")

            x_scale = plot_config.get("x_scale")
            scale_params = {}
            if x_scale:
                scale_params["x_scale"] = x_scale

            aspect_params = {}
            if ridge:
                aspect_params["ridge"] = ridge == "True"
            if plot_aspect:
                aspect_params["plot_aspect"] = plot_aspect
            if plot_height:
                aspect_params["plot_height"] = plot_height
            if plot_spacing:
                aspect_params["plot_spacing"] = plot_spacing
            
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            ax = fp.pl.marker_density(
                dataset,
                gate=plot_config.get("gate"),
                layer=plot_config.get("layer"),
                marker=plot_config.get("marker"),
                groupby=groupby,
                colorby=splitby if splitby != groupby else None,
                cmap = plot_config.get("cmap"),
                ax = ax,
                show=False,
                **aspect_params,
                **scale_params
            )
            self._apply_layout_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")
