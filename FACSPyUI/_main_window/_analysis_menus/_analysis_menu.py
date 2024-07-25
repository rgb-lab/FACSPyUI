from PyQt5.QtWidgets import (QMessageBox, QWidget, 
                             QPushButton, QLabel,
                             QLineEdit, QComboBox,
                             QHBoxLayout)
from PyQt5.QtCore import Qt


from .._utils import MultiSelectComboBox, HoverLabel

class BaseAnalysisMenu(QWidget):
    def __init__(self, main_window, title, advanced_params):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet(self.main_window.stylesheet)
        self.setWindowTitle(title)
        self.advanced_params = advanced_params
        self.enable_documentation()

    def finalize_window_layout(self):
        # Populate dropdowns
        self.populate_dropdowns()

        # Set size policies
        self.set_input_size_policies()

        # Connect to adjust input sizes
        self.resizeEvent(None)

        # Flag to ensure we only set the fixed size once
        self.fixed_size_set = False

        self.height_without_advanced_settings = self.sizeHint().height()

    def showEvent(self, event):
        """
        Fixes the window size after the initial rendering.
        """
        if not self.fixed_size_set:
            self.setFixedSize(self.sizeHint())
            self.fixed_size_set = True
        super().showEvent(event)

    def set_input_size_policies(self):
        """
        Sets the size policies for input fields and buttons to be half the width of the parent container,
        excluding children of MultiSelectComboBox.
        """
        adjustment_factor = 0.9
        parent_width = self.size().width() * adjustment_factor
        half_width = int(parent_width // 2)

        def set_size_policy(widget):
            if isinstance(widget, (QLineEdit, QComboBox, QPushButton, QLabel)) and not isinstance(widget.parent(), MultiSelectComboBox):
                widget.setFixedWidth(half_width)

        # Apply size policies to direct children only
        for widget in self.form_layout.findChildren(QWidget, options=Qt.FindDirectChildrenOnly):
            set_size_policy(widget)

        for widget in self.advanced_settings_layout.findChildren(QWidget, options=Qt.FindDirectChildrenOnly):
            set_size_policy(widget)

    def toggle_advanced_settings(self):
        """
        Toggles the visibility of the advanced settings section.
        """
        is_visible = self.advanced_settings_checkbox.isChecked()
        self.advanced_settings_group.setVisible(is_visible)
        self.advanced_settings_checkbox.setText(
            "Hide Advanced Settings" if is_visible else "Show Advanced Settings"
        )
        self.adjust_window_size()

    def adjust_window_size(self):
        """
        Adjusts the window size based on the visibility of the advanced settings.
        """
        base_height = self.height_without_advanced_settings
        advanced_height = self.advanced_settings_group.sizeHint().height() if self.advanced_settings_checkbox.isChecked() else 0
        self.setFixedHeight(base_height + advanced_height)

    def add_advanced_settings(self):
        """
        Adds advanced settings input fields.
        """
        for param, default in self.advanced_params.items():
            label = QLabel(param.replace('_', ' ').capitalize() + ":")
            input_field = QLineEdit()
            input_field.setPlaceholderText(str(default))
            self.advanced_settings_layout.addRow(label, input_field)
            setattr(self, f"{param}_input", input_field)

    def show_error(self, title, message):
        """
        Displays an error message in a QMessageBox.
        """
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def add_tooltip(self,
                    widget: QWidget,
                    parameter: str) -> QHBoxLayout:
        tooltip = HoverLabel(
            dimension = widget.sizeHint().height(),
            hover_info = self._documentation[parameter],
            darkmode = self.main_window.is_dark
        )
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.addWidget(widget)
        container_layout.addWidget(tooltip)
        container_layout.setContentsMargins(0,0,0,0)
        container_layout.setSpacing(10)
        container.setLayout(container_layout)

        return container

    def enable_documentation(self):
        self._documentation = {
            "data_format": "Choose the data to be used for calculation.",
            "group_by_fluo_metrics":
                "Select a grouping. Usually, you want to use 'sample_ID' " +
                "in order to obtain the metric per sample. The grouping " +
                "for your variable of interest will then be performed by " +
                "the plot.",
            "aggregation_method":
                "Defines whether to use the 'median fluorescence intensity' " +
                "or the 'mean fluorescence intensity'",
            "use_markers_only":
                "If set to True, the calculations will only be applied to " +
                "channels that contain marker proteins. This will exclude " +
                "channels such as 'FSC', 'SSC' or technical channels in " +
                "CyTOF.",
            "aggregate":
                "If the groupby parameter is not set to sample_ID, this " +
                "option controls if you want to calculate the metric on " +
                "your groupby variable AND 'sample_ID' or just by your " +
                "groupby variable. Statistics are usually only possible " +
                "when set to False. For the cluster heatmap for instance " +
                "use 'aggregate = True' in order to display the intensities " +
                "per cluster and not per cluster and 'sample_ID'.",
            "cutoff":
                "Determines what numerical cutoff to be used. The intensity " +
                "values above the cutoff will be counted as positive, while " +
                "the intensity values below the cutoff are counted as negative. " +
                "Defaults to 'use cofactors', in which case the channel-specific " +
                "cofactors will be used. Can be any float, otherwise.",
            "gate":
                "Specify the population that is used for the calculation.",
            "exclude":
                "Specify channels that are excluded from the calculation. This " +
                "could be a live/dead stain or other uninformative markers. " +
                "The inclusion of Scatter- and technical channels is controlled " +
                "via the 'use marker channels only' option.",
            "scaling":
                "Controls whether to apply scaling to the input data. 'MinMaxScaler' " +
                "scales the data between 0 and 1, while  StandardScaler performs " +
                "Z-scaling. For further information refer to the scikit-learn documentation. ",
            "data_metric":
                "Specifies whether to calculate the reduction on the intensity values " +
                "(mfi) or the frequency of positives (fop)."

        }


