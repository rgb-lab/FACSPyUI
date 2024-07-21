import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from . import PlotWindowFunctionGeneric, BaseConfigPanel

class ConfigPanelTransformationPlot(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_layer_input()
        self.add_gate_input()

        self.add_marker_input()
        self.add_sample_identifier_input()
        self.add_scatter_input()

        self.add_sample_size_input()

        self.add_dot_parameters()

        self.scroll_layout.addStretch()

        self.add_buttons()

        self.setLayout(self.main_layout)

        self.populate_dropdowns()


class PlotWindowTransformationPlot(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self._plot_func = fp.pl.transformation_plot

    def _instantiate_parameters(self,
                                plot_config,
                                dataset,
                                ax = None):
        self._raw_config = {
                "adata": dataset,
                "gate": plot_config.get("gate"),
                "sample_identifier": plot_config.get("sample_identifier"),
                "marker": plot_config.get("marker"),
                "scatter": plot_config.get("scatter"),
                "show": False,
                "return_fig": True,
        }

    def generate_matplotlib(self, plot_config):
        dataset = self.retrieve_dataset()

        try:
            self._instantiate_parameters(plot_config, dataset)
            fig = self._plot_func(**self._raw_config)
            for _ax in fig.axes[:2]:
                self._apply_dot_parameters_matplotlib(_ax, plot_config)

            self._show_matplotlib(fig)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")
