from PyQt5.QtWidgets import (QMessageBox, QWidget, QVBoxLayout, 
                             QPushButton, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox)

import FACSPy as fp
import scanpy as sc

class SubsampleDatasetWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Subsample Dataset")
        self.setGeometry(150, 150, 400, 200)

        # Main layout
        layout = QVBoxLayout()

        # Instructions
        instructions = QLabel(
            "Subsample the dataset.\n\nEnter a number of cells to be subsampled randomly from the dataset.\n\n"
            "If you enter a fraction, the dataset will be subsampled randomly to that percentage."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Input for number of cells
        self.cells_input = QLineEdit()
        self.cells_input.setPlaceholderText("Number of cells (integer)")

        # Input for fraction
        self.fraction_input = QLineEdit()
        self.fraction_input.setPlaceholderText("Fraction (between 0 and 1)")

        # Create a submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 60)
        self.submit_button.clicked.connect(self.submit)

        # Create a layout for inputs and button
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.cells_input)
        input_layout.addWidget(self.fraction_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        layout.addLayout(input_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def submit(self):
        """
        Subsamples the dataset based on user input.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            if dataset_key not in self.main_window.DATASHACK:
                raise ValueError("Invalid dataset selected.")

            dataset = self.main_window.DATASHACK[dataset_key]

            cells = self.cells_input.text().strip()
            fraction = self.fraction_input.text().strip()

            if cells and fraction:
                raise ValueError("Please enter either 'Number of cells' or 'Fraction', not both.")
            elif cells:
                if not cells.isdigit():
                    raise ValueError("Number of cells must be an integer.")
                n_obs = int(cells)
                sc.pp.subsample(dataset, n_obs=n_obs)
            elif fraction:
                try:
                    fraction = float(fraction)
                except ValueError:
                    raise ValueError("Fraction must be a float.")
                if not (0 < fraction <= 1):
                    raise ValueError("Fraction must be between 0 and 1.")
                sc.pp.subsample(dataset, fraction=fraction)
            else:
                raise ValueError("Please enter either 'Number of cells' or 'Fraction'.")

            fp.sync.synchronize_dataset(dataset)

            # Update the dataset display
            self.main_window.update_current_dataset_display()

            # Show success message and close the window
            QMessageBox.information(self, "Success", "Dataset subsampled successfully.")
            self.close()

        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

class EqualizeGroupSizesWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Equalize Group Sizes")
        self.setGeometry(150, 150, 500, 250)

        # Main layout
        layout = QVBoxLayout()

        # Instructions
        instructions = QLabel(
            "Equalize group sizes. \n\n This is used to sample a certain number of cells per condition in order to match the group sizes.\n\n"
            "Select a group you want to equalize and either enter a number of cells to be kept per group or a fraction.\n\n"
            "The fraction will be calculated from the group with the fewest cells. If you want to keep all cells of the smallest group, enter a fraction of 1.\n\n"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Dropdown for selecting .obs column
        self.obs_column_dropdown = QComboBox()
        self.obs_column_dropdown.setPlaceholderText("Select group to equalize")
        self.populate_obs_columns()

        # Input for number of cells
        self.cells_input = QLineEdit()
        self.cells_input.setPlaceholderText("Number of cells (integer)")

        # Input for fraction
        self.fraction_input = QLineEdit()
        self.fraction_input.setPlaceholderText("Fraction (between 0 and 1)")

        # Create a submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 60)
        self.submit_button.clicked.connect(self.submit)

        # Create layouts for inputs and button
        dropdown_layout = QHBoxLayout()
        dropdown_layout.addWidget(self.obs_column_dropdown)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.cells_input)
        input_layout.addWidget(self.fraction_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        layout.addLayout(dropdown_layout)
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def populate_obs_columns(self):
        """
        Populates the dropdown with .obs columns from the current dataset.
        """
        dataset_key = self.main_window.dataset_dropdown.currentText()
        if dataset_key in self.main_window.DATASHACK:
            dataset = self.main_window.DATASHACK[dataset_key]
            self.obs_column_dropdown.addItems(dataset.obs.columns)
        else:
            self.obs_column_dropdown.addItem("No dataset selected")

    def submit(self):
        """
        Equalizes group sizes based on user input.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            if dataset_key not in self.main_window.DATASHACK:
                raise ValueError("Invalid dataset selected.")

            dataset = self.main_window.DATASHACK[dataset_key]
            obs_column = self.obs_column_dropdown.currentText()
            cells = self.cells_input.text().strip()
            fraction = self.fraction_input.text().strip()

            if obs_column == "No dataset selected" or obs_column == "":
                raise ValueError("Please select a valid group to equalize.")

            if cells and fraction:
                raise ValueError("Please enter either 'Number of cells' or 'Fraction', not both.")
            elif cells:
                if not cells.isdigit():
                    raise ValueError("Number of cells must be an integer.")
                n_obs = int(cells)
                fp.equalize_groups(dataset, on=obs_column, n_obs=n_obs)
            elif fraction:
                try:
                    fraction = float(fraction)
                except ValueError:
                    raise ValueError("Fraction must be a float.")
                if not (0 < fraction <= 1):
                    raise ValueError("Fraction must be between 0 and 1.")
                fp.equalize_groups(dataset, on=obs_column, fraction=fraction)
            else:
                raise ValueError("Please enter either 'Number of cells' or 'Fraction'.")

            fp.sync.synchronize_dataset(dataset)

            # Update the dataset display
            self.main_window.update_current_dataset_display()

            # Show success message and close the window
            QMessageBox.information(self, "Success", "Group sizes equalized successfully.")
            self.close()

        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")


class SubsetGateWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Subset Gate")
        self.setGeometry(150, 150, 400, 200)

        # Main layout
        layout = QVBoxLayout()

        # Instructions
        instructions = QLabel(
            "Subset Gate.\n\nSelect a population that you want to isolate."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Dropdown for selecting .uns["gating_cols"]
        self.gating_cols_dropdown = QComboBox()
        self.gating_cols_dropdown.setPlaceholderText("Select population")
        self.populate_gating_columns()

        # Create a submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 60)
        self.submit_button.clicked.connect(self.submit)

        # Create layouts for inputs and button
        dropdown_layout = QHBoxLayout()
        dropdown_layout.addWidget(self.gating_cols_dropdown)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        layout.addLayout(dropdown_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def populate_gating_columns(self):
        """
        Populates the dropdown with .uns["gating_cols"] from the current dataset.
        """
        dataset_key = self.main_window.dataset_dropdown.currentText()
        if dataset_key in self.main_window.DATASHACK:
            dataset = self.main_window.DATASHACK[dataset_key]
            if "gating_cols" in dataset.uns:
                self.gating_cols_dropdown.addItems(dataset.uns["gating_cols"])
            else:
                self.gating_cols_dropdown.addItem("No gating columns found")
        else:
            self.gating_cols_dropdown.addItem("No dataset selected")

    def submit(self):
        """
        Subsets the dataset based on the selected gating column.
        """
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            if dataset_key not in self.main_window.DATASHACK:
                raise ValueError("Invalid dataset selected.")

            dataset = self.main_window.DATASHACK[dataset_key]
            gating_col = self.gating_cols_dropdown.currentText()

            if gating_col == "No gating columns found" or gating_col == "":
                raise ValueError("Please select a valid gating column.")

            # Subset the dataset based on the selected gating column
            fp.subset_gate(dataset, gate = gating_col)

            # Synchronize the subset dataset
            fp.sync.synchronize_dataset(dataset)

            # Replace the original dataset with the subset
            self.main_window.DATASHACK[dataset_key] = dataset

            # Update the dataset display
            self.main_window.update_current_dataset_display()

            # Show success message and close the window
            QMessageBox.information(self, "Success", f"Dataset subsetted successfully using {gating_col}.")
            self.close()

        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")


