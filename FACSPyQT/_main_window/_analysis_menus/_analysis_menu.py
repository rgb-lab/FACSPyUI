from PyQt5.QtWidgets import (QMessageBox, QWidget, 
                             QPushButton, QLabel,
                             QLineEdit, QComboBox)
from PyQt5.QtCore import Qt


from .._utils import MultiSelectComboBox

class BaseAnalysisMenu(QWidget):
    def __init__(self, main_window, title, advanced_params):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet(self.main_window.stylesheet)
        self.setWindowTitle(title)
        self.advanced_params = advanced_params

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

