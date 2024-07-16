import os
from PyQt5.QtCore import pyqtSlot, Qt, QPoint
from PyQt5.QtWidgets import (QFileDialog, QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QComboBox, QHBoxLayout, QDialogButtonBox,
                             QWidget, QSizeGrip, QErrorMessage)

from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWebEngineWidgets import QWebEngineView

import pandas as pd
from anndata import AnnData

from matplotlib import rcParams

import plotly.express as px
import plotly.graph_objs as go
import sys
import subprocess
from PyQt5.QtGui import QPixmap

COLORMAPS = {
    "tab10": [
        "rgb(31, 119, 180)", "rgb(255, 127, 14)", "rgb(44, 160, 44)", "rgb(214, 39, 40)",
        "rgb(148, 103, 189)", "rgb(140, 86, 75)", "rgb(227, 119, 194)", "rgb(127, 127, 127)",
        "rgb(188, 189, 34)", "rgb(23, 190, 207)"
    ],
    "Set1": px.colors.qualitative.Set1,
    "Set2": px.colors.qualitative.Set2,
    "Set3": px.colors.qualitative.Set3,
    "Paired": [
        "rgb(31, 120, 180)", "rgb(255, 127, 0)", "rgb(51, 160, 44)", "rgb(227, 26, 28)",
        "rgb(166, 206, 227)", "rgb(178, 223, 138)", "rgb(251, 154, 153)", "rgb(253, 191, 111)",
        "rgb(202, 178, 214)", "rgb(106, 61, 154)", "rgb(255, 255, 153)", "rgb(177, 89, 40)"
    ],
    "hls": [
        "rgb(255,0,0)", "rgb(255,255,0)", "rgb(0,255,0)", "rgb(0,255,255)",
        "rgb(0,0,255)", "rgb(255,0,255)", "rgb(255,127,0)", "rgb(127,255,0)",
        "rgb(0,255,127)", "rgb(0,127,255)", "rgb(127,0,255)", "rgb(255,0,127)"
    ]
}


class PlotWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add a placeholder message
        self.placeholder = QLabel("Plot will be displayed here.")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.placeholder)

        # Track the current plot widget
        self.current_plot_widget = None

    def instantiate_new_analysis_type(self,
                                      plot_config: dict):
        if self.current_plot_widget is None:
            return
        self.current_plot_widget.plot_requested.connect(self.update_plot)
        self.current_plot_widget.generate_plot(plot_config)

    @pyqtSlot(dict)
    def switch_to_specific_plot_window(self, plot_config):
        """
        Switches the plot area to the widget based on the plot configuration.
        """
        print("Received plot_config:", plot_config)  # Debug print
        plot_type = self.main_window.config_panel.analysis_dropdown.currentText().strip()

        if plot_type == "MFI":
            from . import PlotWindowMFI
            self.current_plot_widget = PlotWindowMFI(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "FOP":
            from . import PlotWindowFOP
            self.current_plot_widget = PlotWindowFOP(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Gate frequency":
            from . import PlotWindowGateFrequency
            self.current_plot_widget = PlotWindowGateFrequency(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Metadata":
            from . import PlotWindowMetadata
            self.current_plot_widget = PlotWindowMetadata(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Cell counts":
            from . import PlotWindowCellCounts
            self.current_plot_widget = PlotWindowCellCounts(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Marker correlations":
            from . import PlotWindowMarkerCorrelation
            self.current_plot_widget = PlotWindowMarkerCorrelation(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Sample correlations":
            from . import PlotWindowSampleCorrelation
            self.current_plot_widget = PlotWindowSampleCorrelation(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Sample distance":
            from . import PlotWindowSampleDistance
            self.current_plot_widget = PlotWindowSampleDistance(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Expression Heatmap":
            from . import PlotWindowExpressionHeatmap
            self.current_plot_widget = PlotWindowExpressionHeatmap(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Samplewise DimRed":
            from . import PlotWindowSamplewiseDimred
            self.current_plot_widget = PlotWindowSamplewiseDimred(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Singlecell DimRed":
            from . import PlotWindowSinglecellDimred
            self.current_plot_widget = PlotWindowSinglecellDimred(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Biaxial Scatter":
            from . import PlotWindowBiaxScatter
            self.current_plot_widget = PlotWindowBiaxScatter(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Marker Density":
            from . import PlotWindowMarkerDensity
            self.current_plot_widget = PlotWindowMarkerDensity(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Cluster Abundance":
            from . import PlotWindowClusterAbundance
            self.current_plot_widget = PlotWindowClusterAbundance(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Cluster Frequency":
            from . import PlotWindowClusterFrequency
            self.current_plot_widget = PlotWindowClusterFrequency(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Fold Change":
            from . import PlotWindowFoldChange
            self.current_plot_widget = PlotWindowFoldChange(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Cluster Heatmap":
            from . import PlotWindowClusterHeatmap
            self.current_plot_widget = PlotWindowClusterHeatmap(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)
        elif plot_type == "Transformation Plot":
            from . import PlotWindowTransformationPlot
            self.current_plot_widget = PlotWindowTransformationPlot(self.main_window, self)
            self.instantiate_new_analysis_type(plot_config)

        else:
            self.current_plot_widget = QLabel("Plot will be displayed here.")
            self.current_plot_widget.setAlignment(Qt.AlignCenter)

        self.clear_plotting_area()
        self.layout.addWidget(self.current_plot_widget)

    @pyqtSlot(dict)
    def update_plot(self, plot_config):
        """
        Updates the plot display with the generated plot.
        """
        print("Updating plot with config:", plot_config)  # Debug print
        if self.current_plot_widget and hasattr(self.current_plot_widget, 'generate_plot'):
            # self.clear_plotting_area()
            plot_widget = self.current_plot_widget.generate_plot(plot_config)
            self.layout.addWidget(plot_widget)

    def clear_plotting_area(self):
        """
        Clears the plotting area before displaying a new plot.
        """
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

class PlotWindowFunctionGeneric(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.current_plot_widget = None

        # For making the plot window resizable and draggable
        self.setWindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: white; border: 2px solid black;")  # Ensure transparent areas are filled

        # Add a QSizeGrip for resizing
        self.grip = QSizeGrip(self)
        self.grip.setFixedSize(20, 20)
        self.grip.setStyleSheet("background-color: transparent;")
        self.grip.show()


    @pyqtSlot(dict)
    def generate_plot(self, plot_config):
        """
        Generates and returns the plot based on the provided configuration.
        """
        # self.clear_plotting_area()

        backend = plot_config.get("backend", "matplotlib").lower()

        if backend == "plotly":
            self.generate_plotly(plot_config)
        else:
            self.generate_matplotlib(plot_config)

    def clear_plotting_area(self):
        """
        Clears the plotting area before displaying a new plot.
        """
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw black border
        pen = QPen(QColor(0, 0, 0), 2)  # Black border, 2px width
        painter.setPen(pen)
        rect = self.rect().adjusted(1, 1, -1, -1)  # Adjust for pen width
        painter.drawRect(rect)

        # Draw resizing triangle in the lower right corner
        triangle_size = 20
        points = [
            QPoint(rect.right() - triangle_size, rect.bottom()),
            QPoint(rect.right(), rect.bottom() - triangle_size),
            QPoint(rect.right(), rect.bottom())
        ]
        painter.setBrush(QColor(0, 0, 0))  # Fill with black color
        painter.drawPolygon(QPolygon(points))

        super().paintEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.grip.move(self.width() - self.grip.width(), self.height() - self.grip.height())
        if hasattr(self, "current_plot_widget") and hasattr(self.current_plot_widget, "figure"):
            if not hasattr(self, "no_tight_layout_upon_resizing"):
                self.current_plot_widget.figure.tight_layout()

    def show_error_dialog(self, message):
        """
        Shows an error dialog with the provided message.
        """
        error_dialog = QErrorMessage(self)
        error_dialog.showMessage(message)
        error_dialog.exec_()

    def retrieve_dataset(self) -> AnnData:
        # Retrieve the dataset from the main window's DATASHACK
        dataset_key = self.main_window.dataset_dropdown.currentText()
        dataset = self.main_window.DATASHACK.get(dataset_key, None)

        if dataset is None:
            self.show_error_dialog("Please select a dataset")
            return

        return dataset

    def save_plot(self):
        """
        Opens a dialog to save the current plot.
        """
        # Create a dialog window for file saving
        dialog = QDialog(self)
        dialog.setWindowTitle("Save Plot")

        layout = QVBoxLayout(dialog)

        # Directory selection
        dir_label = QLabel("Select directory:")
        dir_input = QLineEdit()
        dir_button = QPushButton("Browse")
        dir_button.clicked.connect(lambda: self.choose_directory(dir_input))

        dir_layout = QHBoxLayout()
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(dir_input)
        dir_layout.addWidget(dir_button)

        layout.addLayout(dir_layout)

        # File name input
        file_label = QLabel("File name:")
        file_input = QLineEdit()
        layout.addWidget(file_label)
        layout.addWidget(file_input)

        # File format dropdown
        format_label = QLabel("File format:")
        format_dropdown = QComboBox()
        if isinstance(self.current_plot_widget, QWebEngineView):
            format_dropdown.addItems([".pdf"])  # Only PDF for Plotly via QWebEngineView
        else:
            format_dropdown.addItems([".pdf", ".png", ".jpg"])  # All formats for Matplotlib

        layout.addWidget(format_label)
        layout.addWidget(format_dropdown)

        # Resolution dropdown
        resolution_label = QLabel("Resolution (DPI):")
        resolution_dropdown = QComboBox()
        resolution_dropdown.addItems(["150", "300", "600", "1200"])
        layout.addWidget(resolution_label)
        layout.addWidget(resolution_dropdown)

        # Save button
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.perform_save_plot(
            dir_input.text(),
            file_input.text(),
            format_dropdown.currentText(),
            resolution_dropdown.currentText(),
            dialog
        ))
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def choose_directory(self, line_edit):
        """
        Opens a directory dialog and sets the selected directory in the line edit.
        """
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            line_edit.setText(directory)

    def perform_save_plot(self, directory, filename, file_format, resolution, dialog):
        """
        Saves the current plot to the specified directory with the given filename, format, and resolution.
        """
        if not directory or not filename:
            self.show_error_dialog("Directory and file name cannot be empty.")
            return

        full_path = os.path.join(directory, f"{filename}{file_format}")
        if isinstance(self.current_plot_widget, FigureCanvas):
            # Matplotlib plot
            self.current_plot_widget.figure.savefig(full_path, dpi=int(resolution), bbox_inches = "tight")
        elif isinstance(self.current_plot_widget, QWebEngineView):
            # Plotly plot
            self.current_plot_widget.page().printToPdf(full_path)

        dialog.accept()

    def render_stripboxplot_plotly(self,
                                   data: pd.DataFrame,
                                   x: str,
                                   y: str,
                                   color: str,
                                   hover_data: dict,
                                   color_discrete_sequence):
        fig = px.strip(
            data_frame = data,
            x = x,
            y = y,
            stripmode = "overlay",
            color = color,
            hover_data = hover_data,
            color_discrete_sequence = color_discrete_sequence
        )

        for entry in data[x].unique():
            fig.add_trace(
                go.Box(
                    y = data.loc[data[x] == entry, y],
                    name=entry,
                    showlegend=False,
                    fillcolor="rgba(0,0,0,0)",
                    marker_color="black",
                    boxpoints=False,
                    line=dict(width=0.6)
                )
            )

        return fig

    def _apply_layout_parameters_matplotlib(self, ax, plot_config):
        title = plot_config.get("title")
        if not title:
            title = ax.get_title()
        title_fontsize = plot_config.get("title_fontsize")
        if not title_fontsize:
            title_fontsize = rcParams["axes.titlesize"]

        xlabel = plot_config.get("xlabel")
        if not xlabel:
            xlabel = ax.get_xlabel()

        xlabel_fontsize = plot_config.get("xlabel_fontsize")
        if not xlabel_fontsize:
            xlabel_fontsize = rcParams["axes.labelsize"]

        ylabel = plot_config.get("ylabel")
        if not ylabel:
            ylabel = ax.get_ylabel()

        ylabel_fontsize = plot_config.get("ylabel_fontsize")
        if not ylabel_fontsize:
            ylabel_fontsize = rcParams["axes.labelsize"]

        ax.set_title(title, fontsize = title_fontsize)
        ax.set_xlabel(xlabel, fontsize = xlabel_fontsize)
        ax.set_ylabel(ylabel, fontsize = ylabel_fontsize)

        xticklabel_fontsize = plot_config.get("xticklabel_fontsize")
        if not xticklabel_fontsize:
            xticklabel_fontsize = rcParams["xtick.labelsize"]
        yticklabel_fontsize = plot_config.get("yticklabel_fontsize")
        if not yticklabel_fontsize:
            yticklabel_fontsize = rcParams["ytick.labelsize"]

        ax.set_xticklabels(ax.get_xticklabels(), fontsize = xticklabel_fontsize)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize = yticklabel_fontsize)

        return

    def _apply_layout_parameters_plotly(self, fig, plot_config):
        title = plot_config.get("title")
        if not title:
            title = fig.layout.title.text
        title_fontsize = plot_config.get("title_fontsize")
        if not title_fontsize:
            title_fontsize = 18

        xlabel = plot_config.get("xlabel")
        if not xlabel:
            xlabel = fig.layout.xaxis.title.text
        xlabel_fontsize = plot_config.get("xlabel_fontsize")
        if not xlabel_fontsize:
            xlabel_fontsize = 12

        ylabel = plot_config.get("ylabel")
        if not ylabel:
            ylabel = fig.layout.yaxis.title.text

        ylabel_fontsize = plot_config.get("ylabel_fontsize")
        if not ylabel_fontsize:
            ylabel_fontsize = 12

        xticklabel_fontsize = plot_config.get("xticklabel_fontsize")
        if not xticklabel_fontsize:
            xticklabel_fontsize = 12
        yticklabel_fontsize = plot_config.get("yticklabel_fontsize")
        if not yticklabel_fontsize:
            yticklabel_fontsize = 12

        fig.update_layout(
            title = dict(text = title, font = dict(size = int(title_fontsize))),
            title_x = 0.5,
            xaxis_title = xlabel,
            yaxis_title = ylabel,
            margin = dict(l = 0, r = 0, t = 40, b = 0)
        )
        fig.update_xaxes(
            title_font=dict(size = int(xlabel_fontsize)),
            tickfont = dict(size = int(xticklabel_fontsize)),
        )
        fig.update_yaxes(
            title_font=dict(size = int(ylabel_fontsize)),
            tickfont = dict(size = int(yticklabel_fontsize))
        )


        return

    def _apply_dot_parameters_matplotlib(self, ax, plot_config):
        linewidth = plot_config.get("dot_linewidth")
        dotsize = plot_config.get("dotsize")
        linecolor = plot_config.get("dot_linecolor")
        for collection in ax.collections:
            if not linewidth:
                linewidth = collection.get_linewidths()
            collection.set_linewidth(float(linewidth))

            if not dotsize:
                dotsize = collection.get_sizes()
            collection.set_sizes([int(dotsize)])

            if not linecolor:
                linecolor = "black"
            collection.set_edgecolor(linecolor)

        return

    def _apply_dot_parameters_plotly(self, fig, plot_config):
        linewidth = plot_config.get("dot_linewidth")
        dotsize = plot_config.get("dotsize")

        for trace in fig.data:
            if not dotsize:
                dotsize = trace.marker.size or 8

            if not linewidth:
                linewidth = trace.marker.line.width or 1

            trace.update(
                marker=dict(
                    line=dict(
                        width=float(linewidth)
                    ),
                    size=int(dotsize),
                )
            )
        return
