from PyQt5.QtWidgets import (QMessageBox, QWidget, QVBoxLayout, 
                             QPushButton, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox,
                             QGroupBox, QFileDialog, QFormLayout)
import pandas as pd

import FACSPy as fp

class BaseTransformationWindow(QWidget):
    def __init__(self, main_window, title, default_kwargs):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle(title)
        self.default_kwargs = default_kwargs

        # Create main layout
        self.main_layout = QVBoxLayout()

        # Create a form layout to maintain consistent spacing
        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)

        # Data format dropdown
        self.data_format_label = QLabel("Select data to transform:")
        self.data_format_dropdown = QComboBox()
        self.form_layout.addRow(self.data_format_label, self.data_format_dropdown)

        # Transformed layer name input
        self.transformed_layer_label = QLabel("Select transformed layer name:")
        self.transformed_layer_input = QLineEdit()
        self.form_layout.addRow(self.transformed_layer_label, self.transformed_layer_input)

        # Placeholder layout for subclass-specific widgets
        self.custom_layout = QHBoxLayout()
        self.main_layout.addLayout(self.custom_layout)

        # Advanced settings checkbox
        self.advanced_settings_checkbox = QCheckBox("Show Advanced Settings")
        self.advanced_settings_checkbox.stateChanged.connect(self.toggle_advanced_settings)
        self.main_layout.addWidget(self.advanced_settings_checkbox)

        # Advanced settings section
        self.advanced_settings_layout = QFormLayout()
        self.advanced_settings_group = QGroupBox("Advanced Settings")
        self.advanced_settings_group.setLayout(self.advanced_settings_layout)
        self.advanced_settings_group.setVisible(False)
        self.main_layout.addWidget(self.advanced_settings_group)

        # Transform button
        self.transform_button = QPushButton("Transform Data")
        self.transform_button.clicked.connect(self.transform_data)
        self.main_layout.addWidget(self.transform_button)

        self.setLayout(self.main_layout)

        # Populate the data format dropdown
        self.populate_data_format_dropdown()

        # Adjust input sizes initially
        self.adjust_input_widths()
        
        # Connect to adjust input sizes
        self.resizeEvent(None)

        # Flag to ensure we only set the fixed size once
        self.fixed_size_set = False

        self.height_without_advanced_settings = self.sizeHint().height()

    def set_input_size_policies(self, *widgets):
        """
        Sets the size policies for input fields and buttons to be half the width of the parent container.
        """
        adjustment_factor = 0.9
        parent_width = self.size().width() * adjustment_factor
        half_width = int(parent_width // 2)
        for widget in widgets:
            if isinstance(widget, (QLineEdit, QComboBox, QPushButton, QLabel)):
                widget.setFixedWidth(half_width)

    def adjust_input_widths(self):
        """
        Adjust widths of input fields and dropdowns to half the width of their parent container.
        """
        adjustment_factor = 0.9
        parent_width = self.size().width() * adjustment_factor
        half_width = int(parent_width // 2)
        widgets = self.findChildren(QWidget)

        for widget in widgets:
            if isinstance(widget, (QLineEdit, QComboBox, QPushButton, QLabel)) and widget != self.transform_button:
                widget.setFixedWidth(half_width)

    def showEvent(self, event):
        """
        Fixes the window size after the initial rendering.
        """
        if not self.fixed_size_set:
            self.setFixedSize(self.sizeHint())
            self.fixed_size_set = True
        super().showEvent(event)

    def toggle_advanced_settings(self):
        """
        Toggles the visibility of the advanced settings section and adjusts the window size.
        """
        width = self.size().width()
        is_visible = self.advanced_settings_checkbox.isChecked()
        self.advanced_settings_group.setVisible(is_visible)
        self.advanced_settings_checkbox.setText(
            "Hide Advanced Settings" if is_visible else "Show Advanced Settings"
        )

        # Adjust window size
        self.adjust_window_size(width = width)

    def adjust_window_size(self, width = None):
        """
        Adjusts the window size based on the visibility of the advanced settings.
        """
        if width is None:
            width = self.size().width()
        width = self.size().width()
        base_height = self.height_without_advanced_settings
        advanced_height = self.advanced_settings_group.sizeHint().height() if self.advanced_settings_checkbox.isChecked() else 0
        self.setFixedHeight(base_height + advanced_height)
        self.setFixedWidth(width)

    def get_transform_kwargs(self):
        """
        Gathers keyword arguments for the transformation based on the inputs in advanced settings.
        """
        kwargs = {}
        for kwarg, input_field in self.default_kwargs.items():
            if isinstance(input_field, QLineEdit):
                try:
                    value = float(input_field.text().strip())
                except ValueError:
                    value = self.default_kwargs[kwarg]
                kwargs[kwarg] = value
        return kwargs

    def transform_data(self):
        """
        Should be overridden in subclasses to perform the transformation.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def show_error(self, title, message):
        """
        Displays an error message in a QMessageBox.
        """
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def populate_data_format_dropdown(self):
        """
        Populates the data format dropdown with the keys from the dataset's layers.
        """
        try:
            # Assuming the current dataset is selected in the main window
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            # Populate the dropdown with layer keys
            self.data_format_dropdown.clear()
            self.data_format_dropdown.addItems(dataset.layers.keys())

        except Exception as e:
            self.show_error("Data Format Error", str(e))


class AsinhTransformationWindow(BaseTransformationWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Asinh Transformation", {})
        self.default_kwargs = {"constant_cofactor": None}  # Default kwargs specific to Asinh

        # Cofactor file upload section
        self.cofactor_file_label = QLabel("Cofactor table:")
        self.cofactor_file_button = QPushButton("Upload or drag-and-drop")
        self.cofactor_file_button.setToolTip("Upload or drag-and-drop a cofactor table file")
        self.cofactor_file_button.clicked.connect(self.open_cofactor_file_dialog)

        # Insert cofactor upload section into the custom layout
        self.custom_layout.addWidget(self.cofactor_file_label)
        self.custom_layout.addWidget(self.cofactor_file_button)

        # Advanced settings: Add the constant cofactor input field to the advanced settings
        self.cofactor_constant_label = QLabel("Constant cofactor:")
        self.cofactor_constant_input = QLineEdit()
        self.cofactor_constant_input.setPlaceholderText("Enter constant cofactor")

        # Set size policies
        self.set_input_size_policies(self.data_format_dropdown, self.transformed_layer_input,
                                     self.cofactor_file_button, self.cofactor_constant_input,
                                     self.data_format_label, self.transformed_layer_label,
                                     self.cofactor_file_label, self.cofactor_constant_label)

        # Adding advanced settings
        self.advanced_settings_layout.addRow(self.cofactor_constant_label, self.cofactor_constant_input)

        self.height_without_advanced_settings = self.sizeHint().height()

        # Enable drag and drop for cofactor file
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.load_cofactor_file(file_path)

    def open_cofactor_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Cofactor File", "", "CSV Files (*.csv);;TSV Files (*.tsv);;All Files (*)", options=options)
        if file_name:
            self.load_cofactor_file(file_name)

    def load_cofactor_file(self, file_name):
        self.cofactor_file_button.setText(f"File selected: {file_name}")
        self.cofactor_constant_input.clear()  # Clear constant cofactor input when a file is loaded

    def transform_data(self):
        """
        Handles the Asinh transformation using the selected settings.
        """
        try:
            dataset_key = self.data_format_dropdown.currentText()
            layer_name = self.transformed_layer_input.text().strip()

            if not layer_name:
                raise ValueError("Transformed layer name must be provided.")

            # Check if cofactor file or constant cofactor is provided
            cofactor_file = None if "File selected: " not in self.cofactor_file_button.text() else self.cofactor_file_button.text().replace("File selected: ", "")
            constant_cofactor = self.cofactor_constant_input.text().strip()

            if cofactor_file and constant_cofactor:
                raise ValueError("Only one cofactor input method can be used at a time. Please choose either a cofactor file or a constant cofactor.")
            elif cofactor_file:
                cofactors_df = pd.read_csv(cofactor_file)
                cofactor_table = fp.dt.CofactorTable(cofactors=cofactors_df)
                cofactor_arg = cofactor_table
            elif constant_cofactor:
                cofactors_df = pd.DataFrame({
                    "fcs_colname": list(self.main_window.DATASHACK[dataset_key].var.index),
                    "cofactors": [float(constant_cofactor)] * len(self.main_window.DATASHACK[dataset_key].var.index)
                })
                cofactor_table = fp.dt.CofactorTable(cofactors=cofactors_df)
                cofactor_arg = cofactor_table
            else:
                raise ValueError("A cofactor must be provided. Please either upload a cofactor file or enter a constant cofactor.")

            dataset = self.main_window.DATASHACK[dataset_key]
            transform_kwargs = self.get_transform_kwargs()  # Retrieve additional transformation arguments
            fp.dt.transform(dataset, transform="asinh", key_added=layer_name, cofactor_table=cofactor_arg, transform_kwargs = transform_kwargs)
            fp.sync.synchronize_dataset(dataset)

            # Update the dataset display
            self.main_window.update_current_dataset_display()

            # Show success message and close the window
            QMessageBox.information(self, "Success", "Data transformed successfully.")
            self.main_window.update_current_dataset_display()
            self.close()

        except Exception as e:
            self.show_error("Transformation Error", str(e))

class LogTransformationWindow(BaseTransformationWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Log Transformation", {"m": 4.5, "t": 262144})

        # Advanced settings for Log
        self.m_label = QLabel("m:")
        self.m_input = QLineEdit()
        self.m_input.setText(str(self.default_kwargs["m"]))

        self.t_label = QLabel("t:")
        self.t_input = QLineEdit()
        self.t_input.setText(str(self.default_kwargs["t"]))

        # Set size policies
        self.set_input_size_policies(self.m_input, self.t_input, self.m_label, self.t_label)

        # Adding advanced settings
        self.advanced_settings_layout.addRow(self.m_label, self.m_input)
        self.advanced_settings_layout.addRow(self.t_label, self.t_input)

    def transform_data(self):
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK[dataset_key]
            layer_name = self.transformed_layer_input.text()
            transform_kwargs = self.get_transform_kwargs()

            # Transform the data
            fp.dt.transform(dataset, transform="log", key_added=layer_name, transform_kwargs=transform_kwargs)
            fp.sync.synchronize_dataset(dataset)
            QMessageBox.information(self, "Success", f"Data transformed with log. New layer: {layer_name}")
            self.main_window.update_current_dataset_display()
            self.close()
        except Exception as e:
            self.show_error("Transformation Error", str(e))


class HyperlogTransformationWindow(BaseTransformationWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Hyperlog Transformation", {"m": 4.5, "t": 262144, "w": 0.5, "a": 0})

        # Advanced settings for Hyperlog
        self.m_label = QLabel("m:")
        self.m_input = QLineEdit()
        self.m_input.setText(str(self.default_kwargs["m"]))

        self.t_label = QLabel("t:")
        self.t_input = QLineEdit()
        self.t_input.setText(str(self.default_kwargs["t"]))

        self.w_label = QLabel("w:")
        self.w_input = QLineEdit()
        self.w_input.setText(str(self.default_kwargs["w"]))

        self.a_label = QLabel("a:")
        self.a_input = QLineEdit()
        self.a_input.setText(str(self.default_kwargs["a"]))

        # Set size policies
        self.set_input_size_policies(self.m_input, self.t_input, self.w_input, self.a_input, 
                                     self.m_label, self.t_label, self.w_label, self.a_label)

        # Adding advanced settings
        self.advanced_settings_layout.addRow(self.m_label, self.m_input)
        self.advanced_settings_layout.addRow(self.t_label, self.t_input)
        self.advanced_settings_layout.addRow(self.w_label, self.w_input)
        self.advanced_settings_layout.addRow(self.a_label, self.a_input)

    def transform_data(self):
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK[dataset_key]
            layer_name = self.transformed_layer_input.text()
            transform_kwargs = self.get_transform_kwargs()

            # Transform the data
            fp.dt.transform(dataset, transform="hyperlog", key_added=layer_name, transform_kwargs = transform_kwargs)
            fp.sync.synchronize_dataset(dataset)
            QMessageBox.information(self, "Success", f"Data transformed with hyperlog. New layer: {layer_name}")
            self.main_window.update_current_dataset_display()
            self.close()
        except Exception as e:
            self.show_error("Transformation Error", str(e))


class LogicleTransformationWindow(BaseTransformationWindow):
    def __init__(self, main_window):
        super().__init__(main_window, "Logicle Transformation", {"m": 4.5, "t": 262144, "w": 0.5, "a": 0})

        # Advanced settings for Logicle
        self.m_label = QLabel("m:")
        self.m_input = QLineEdit()
        self.m_input.setText(str(self.default_kwargs["m"]))

        self.t_label = QLabel("t:")
        self.t_input = QLineEdit()
        self.t_input.setText(str(self.default_kwargs["t"]))

        self.w_label = QLabel("w:")
        self.w_input = QLineEdit()
        self.w_input.setText(str(self.default_kwargs["w"]))

        self.a_label = QLabel("a:")
        self.a_input = QLineEdit()
        self.a_input.setText(str(self.default_kwargs["a"]))

        # Set size policies
        self.set_input_size_policies(self.m_input, self.t_input, self.w_input, self.a_input, 
                                     self.m_label, self.t_label, self.w_label, self.a_label)

        # Adding advanced settings
        self.advanced_settings_layout.addRow(self.m_label, self.m_input)
        self.advanced_settings_layout.addRow(self.t_label, self.t_input)
        self.advanced_settings_layout.addRow(self.w_label, self.w_input)
        self.advanced_settings_layout.addRow(self.a_label, self.a_input)

    def transform_data(self):
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK[dataset_key]
            layer_name = self.transformed_layer_input.text()
            transform_kwargs = self.get_transform_kwargs()

            # Transform the data
            fp.dt.transform(dataset, transform="logicle", key_added=layer_name, transform_kwargs=transform_kwargs)
            fp.sync.synchronize_dataset(dataset)
            QMessageBox.information(self, "Success", f"Data transformed with logicle. New layer: {layer_name}")
            self.main_window.update_current_dataset_display()
            self.close()
        except Exception as e:
            self.show_error("Transformation Error", str(e))


class CalculateCofactorsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Calculate Cofactors")

        # Create main layout
        self.main_layout = QVBoxLayout(self)

        # Add the gating columns dropdown
        self.gating_cols_label = QLabel("Select Gating Column:")
        self.gating_cols_dropdown = QComboBox()
        gating_layout = QHBoxLayout()
        gating_layout.addWidget(self.gating_cols_label)
        gating_layout.addWidget(self.gating_cols_dropdown)
        self.main_layout.addLayout(gating_layout)

        # Populate dropdown
        self.populate_gating_cols_dropdown()

        # Add the calculate cofactors button
        self.calculate_button = QPushButton("Calculate Cofactors")
        self.calculate_button.clicked.connect(self.calculate_cofactors)
        self.main_layout.addWidget(self.calculate_button)

        # Set size policies for the dropdown and button
        self.set_input_size_policies(self.gating_cols_dropdown)
        self.set_button_size_policy(self.calculate_button)

        # Adjust size policies initially
        self.adjust_input_widths()

        # Connect to adjust input sizes
        self.resizeEvent(None)

        # Set initial size and minimum size
        self.setGeometry(200, 200, 400, 200)  # Example size, adjust as needed
        self.setMinimumSize(400, 200)

    def set_button_size_policy(self, button):
        """
        Sets the size policy for the button to span the full width.
        """
        button.setFixedHeight(40)  # Set the desired fixed height

    def set_input_size_policies(self, *widgets):
        """
        Sets the size policies for input fields and buttons to be half the width of the parent container.
        """
        adjustment_factor = 0.9
        parent_width = self.size().width() * adjustment_factor
        half_width = int(parent_width // 2)
        for widget in widgets:
            if isinstance(widget, (QLineEdit, QComboBox, QPushButton, QLabel)):
                widget.setFixedWidth(half_width)

    def adjust_input_widths(self):
        """
        Adjust widths of input fields and dropdowns to half the width of their parent container.
        """
        adjustment_factor = 0.9
        parent_width = self.size().width() * adjustment_factor
        half_width = int(parent_width // 2)
        widgets = self.findChildren(QWidget)

        for widget in widgets:
            if isinstance(widget, (QLineEdit, QComboBox, QPushButton, QLabel)) and widget != self.calculate_button:
                widget.setFixedWidth(half_width)

    def showEvent(self, event):
        """
        Fixes the window size after the initial rendering.
        """
        if not self.fixed_size_set:
            self.setFixedSize(self.size())
            self.fixed_size_set = True
        super().showEvent(event)

    def resizeEvent(self, event):
        """
        Adjust input sizes when the window is resized.
        """
        self.adjust_input_widths()
        if event:
            super().resizeEvent(event)

    def populate_gating_cols_dropdown(self):
        """
        Populates the gating columns dropdown with values from dataset.uns["gating_cols"].
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            if dataset_key in self.main_window.DATASHACK:
                dataset = self.main_window.DATASHACK[dataset_key]
                gating_cols = dataset.uns.get("gating_cols", [])
                self.gating_cols_dropdown.addItems(gating_cols)
        except Exception as e:
            self.show_error("Error", f"Failed to populate gating columns: {str(e)}")

    def show_error(self, title, message):
        """
        Displays an error message in a QMessageBox.
        """
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def calculate_cofactors(self):
        """
        Function to calculate cofactors.
        """
        # Retrieve selected gating column
        selected_gating_col = self.gating_cols_dropdown.currentText()

        # Ensure a gating column is selected
        if not selected_gating_col:
            self.show_error("Error", "Please select a gating column.")
            return

        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK[dataset_key]

            fp.dt.calculate_cofactors(dataset, add_to_adata = True)

            # Close the window and update the dataset display
            self.main_window.update_current_dataset_display()
            self.close()

        except Exception as e:
            self.show_error("Calculation Error", str(e))
