import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout
from matplotlib import pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from . import PlotWindowFunctionGeneric, BaseConfigPanel


class ConfigPanelSinglecellDimred(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_dimred_input()

        self.add_layer_input()
        self.add_gate_input()

        self.add_colorby_input()

        self.add_data_metric_input()

        # Add layout parameters section
        self.add_layout_parameters()

        # Add font size parameters section
        self.add_fontsize_parameters()

        # Add dot parameters section
        self.add_dot_parameters()

        # Add colorscale parameter section
        self.add_colorscale_parameters()

        # Add stretch to keep layout parameters aligned
        self.scroll_layout.addStretch()

        # Buttons
        self.add_buttons()

        self.setLayout(self.main_layout)

        # Populate dropdowns
        self.populate_dropdowns()



class PlotWindowSinglecellDimred(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to the main window

    def generate_matplotlib(self, plot_config):
        """
        Generates a plot using fp.pl.mfi function.
        """
        dataset = self.retrieve_dataset()

        # Generate the figure using your custom function
        try:
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
                cmap=plot_config.get("cmap"),
                ax = ax,
                show=False,
                **scale_kwargs
            )
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)

            # Add the canvas to the layout
            self.current_plot_widget = FigureCanvas(fig)
            self.layout.addWidget(self.current_plot_widget)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")

