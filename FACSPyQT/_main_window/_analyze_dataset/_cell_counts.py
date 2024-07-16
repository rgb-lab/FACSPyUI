import FACSPy as fp

from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

import plotly.io as pio
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

        # Add layout parameters section
        self.add_layout_parameters()

        # Add font size parameters section
        self.add_fontsize_parameters()

        # Add dot parameters section
        self.add_dot_parameters()

        # Add stretch to keep layout parameters aligned
        self.scroll_layout.addStretch()

        # Buttons
        self.add_buttons()

        self.setLayout(self.main_layout)

        # Populate dropdowns
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

            # Convert Plotly figure to HTML
            html = pio.to_html(fig, full_html=True, include_plotlyjs='cdn')  # Use full_html=True for proper rendering

            # Create a QWebEngineView
            plotly_widget = QWebEngineView()

            # Set HTML asynchronously with a timer to ensure proper rendering
            QTimer.singleShot(0, lambda: plotly_widget.setHtml(html))

            # Add the QWebEngineView to the layout
            self.current_plot_widget = plotly_widget
            self.layout.addWidget(self.current_plot_widget)

        except Exception as e:
            self.show_error_dialog(f"Error generating Plotly plot: {str(e)}")

    def generate_matplotlib(self, plot_config):
        """
        Generates a plot using fp.pl.mfi function.
        """
        dataset = self.retrieve_dataset()

        # Generate the figure using your custom function
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

            # Add the canvas to the layout

            self.current_plot_widget = FigureCanvas(fig)
            self.layout.addWidget(self.current_plot_widget)

        except Exception as e:
            self.show_error_dialog(f"Error generating Matplotlib plot with fp.pl.gate_frequency: {e}")
