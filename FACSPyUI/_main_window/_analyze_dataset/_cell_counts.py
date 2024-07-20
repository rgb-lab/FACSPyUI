import FACSPy as fp

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFormLayout

from matplotlib import pyplot as plt

from . import PlotWindowFunctionGeneric, BaseConfigPanel, COLORMAPS

class ConfigPanelCellCounts(BaseConfigPanel):
    def __init__(self, main_window):
        super().__init__(main_window)

        # Data parameters section
        self.add_data_parameters_label()

        self.form_layout = QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)

        self.add_gate_input()
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



class PlotWindowCellCounts(PlotWindowFunctionGeneric):
    plot_requested = pyqtSignal(dict)

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Store reference to the main window

    def generate_plotly(self, plot_config):
        """
        Generates a scatter plot using plotly with random data and displays it in a QWebEngineView.
        """
        dataset = self.retrieve_dataset()

        try:
            splitby = plot_config.get("splitby")
            groupby = plot_config.get("groupby")

            data = fp.pl.cell_counts(
                dataset,
                gate=plot_config.get("gate"),
                groupby=groupby,
                splitby=splitby if splitby != groupby else None,
                return_dataframe = True
            )

            fig = self.render_stripboxplot_plotly(data = data,
                                                  x = groupby,
                                                  y = "counts",
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
            splitby = plot_config.get("splitby")
            groupby = plot_config.get("groupby")
            stat_test = plot_config.get("stat_test")

            if stat_test == "None":
                stat_test = None
            fig, ax = plt.subplots(ncols = 1, nrows = 1)
            ax = fp.pl.cell_counts(
                dataset,
                gate=plot_config.get("gate"),
                groupby=groupby,
                splitby=splitby if splitby != groupby else None,
                stat_test = stat_test,
                cmap = plot_config.get("cmap"),
                ax = ax,
                show=False
            )
            self._apply_layout_parameters_matplotlib(ax, plot_config)
            self._apply_dot_parameters_matplotlib(ax, plot_config)

            self._show_matplotlib(fig)


        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot: {e}")
