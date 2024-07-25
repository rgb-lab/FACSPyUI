from PyQt5.QtWidgets import (QMenuBar, QAction, QMessageBox, QWidget,
                             QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QInputDialog, QHBoxLayout)
from PyQt5.QtGui import QKeySequence
import FACSPy as fp
import pandas as pd

class EditSupplementWindow(QWidget):
    def __init__(self, main_window, dataframe):
        super().__init__()
        self.main_window = main_window
        self.dataframe = dataframe.copy()

        self.setWindowTitle("Edit Supplementary Data")
        self.setGeometry(150, 150, 800, 600)

        layout = QVBoxLayout()

        # Create a menu bar for table modifications
        self.menu_bar = QMenuBar(self)
        self.modify_menu = self.menu_bar.addMenu("Modify Table")

        # Add Column action
        add_column_action = QAction("Add Column", self)
        add_column_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        add_column_action.triggered.connect(self.add_column)
        self.modify_menu.addAction(add_column_action)

        # Remove Column action
        remove_column_action = QAction("Remove Column", self)
        remove_column_action.setShortcut(QKeySequence("Ctrl+Shift+X"))
        remove_column_action.triggered.connect(self.remove_column)
        self.modify_menu.addAction(remove_column_action)

        # Add Row action
        add_row_action = QAction("Add Row", self)
        add_row_action.setShortcut(QKeySequence("Ctrl+Shift+R"))
        add_row_action.triggered.connect(self.add_row)
        self.modify_menu.addAction(add_row_action)

        # Remove Row action
        remove_row_action = QAction("Remove Row", self)
        remove_row_action.setShortcut(QKeySequence("Ctrl+Shift+E"))
        remove_row_action.triggered.connect(self.remove_row)
        self.modify_menu.addAction(remove_row_action)

        # Create a table widget
        self.table = QTableWidget()
        self.initialize_table(self.dataframe.columns)

        # Populate the table with metadata
        self.load_table(self.dataframe)

        # Enable double-click on headers to rename columns
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.rename_column)

        # Create a layout for the table and button
        table_button_layout = QVBoxLayout()
        table_button_layout.addWidget(self.table)

        layout.addWidget(self.menu_bar)
        layout.addLayout(table_button_layout)

        self.setLayout(layout)

    def initialize_table(self, headers):
        """
        Initializes the table with given headers.
        """
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)  # Initialize with no rows

    def load_table(self, df):
        """
        Loads the DataFrame into the table widget.
        """
        self.table.setRowCount(len(df))

        for row_index, row_data in df.iterrows():
            for column_index, value in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

    def add_column(self):
        """
        Adds a new column to the table.
        """
        current_column_count = self.table.columnCount()
        self.table.insertColumn(current_column_count)
        self.table.setHorizontalHeaderItem(current_column_count, QTableWidgetItem("new column"))

    def remove_column(self):
        """
        Removes the currently selected column.
        """
        current_column = self.table.currentColumn()
        if current_column >= 0:
            self.table.removeColumn(current_column)

    def add_row(self):
        """
        Adds a new row to the table.
        """
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)

    def remove_row(self):
        """
        Removes the currently selected row.
        """
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def rename_column(self, index):
        """
        Renames the column at the given index.
        """
        old_name = self.table.horizontalHeaderItem(index).text()
        new_name, ok = QInputDialog.getText(self, "Rename Column", f"Enter new name for column '{old_name}':")
        if ok and new_name:
            self.table.setHorizontalHeaderItem(index, QTableWidgetItem(new_name))


class EditMetadataWindow(EditSupplementWindow):
    def __init__(self, main_window, dataset_key, dataframe):
        super().__init__(main_window, dataframe)
        self.dataset_key = dataset_key

        # Create a submit button and place it at the bottom, centered
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 60)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        self.layout().addLayout(button_layout)
        self.submit_button.clicked.connect(self.submit_changes)

    def submit_changes(self):
        """
        Submits the changes made to the metadata and updates the dataset.
        """
        try:
            # Extract data from the table and update the DataFrame
            new_data = []
            for row in range(self.table.rowCount()):
                row_data = {}
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    row_data[self.table.horizontalHeaderItem(column).text()] = item.text() if item else ""
                new_data.append(row_data)

            new_metadata_df = pd.DataFrame(new_data)
            metadata = fp.dt.Metadata(metadata=new_metadata_df)
            dataset = self.main_window.DATASHACK[self.dataset_key]
            dataset.uns["metadata"] = metadata
            fp.sync.synchronize_dataset(dataset)

            # Update the dataset display
            self.main_window.update_current_dataset_display()

            # Show success message and close the window
            QMessageBox.information(self, "Success", "Metadata changed successfully.")
            self.close()

        except Exception as e:
            error_message = str(e)
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")


class EditPanelWindow(EditSupplementWindow):
    def __init__(self, main_window, dataset_key, dataframe):
        super().__init__(main_window, dataframe)
        self.dataset_key = dataset_key

        # Create a submit button and place it at the bottom, centered
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 60)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        self.layout().addLayout(button_layout)
        self.submit_button.clicked.connect(self.submit_changes)

    def submit_changes(self):
        """
        Submits the changes made to the panel and updates the dataset.
        """
        try:
            # Extract data from the table and update the DataFrame
            new_data = []
            for row in range(self.table.rowCount()):
                row_data = {}
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    row_data[self.table.horizontalHeaderItem(column).text()] = item.text() if item else ""
                new_data.append(row_data)

            new_panel_df = pd.DataFrame(new_data)
            panel = fp.dt.Panel(panel=new_panel_df)
            dataset = self.main_window.DATASHACK[self.dataset_key]
            dataset.uns["panel"] = panel
            fp.sync.synchronize_dataset(dataset)

            # Update the dataset display
            self.main_window.update_current_dataset_display()

            # Show success message and close the window
            QMessageBox.information(self, "Success", "Panel changed successfully.")
            self.close()

        except Exception as e:
            # Show error message
            error_message = str(e)
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

class EditCofactorTableWindow(EditSupplementWindow):
    def __init__(self, main_window, dataset_key, dataframe):
        super().__init__(main_window, dataframe)
        self.dataset_key = dataset_key
        self.selected_layer = None

        # Create a submit button and a retransform button
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 60)
        self.retransform_button = QPushButton("Retransform Dataset")
        self.retransform_button.setFixedSize(180, 60)

        # Center both buttons at the bottom
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.retransform_button)
        button_layout.addStretch()

        self.layout().addLayout(button_layout)

        self.submit_button.clicked.connect(self.submit_changes)
        self.retransform_button.clicked.connect(self.retransform_dataset)

    def retransform_dataset(self):
        """
        Opens a dialog to select the transformed data layer for retransformation.
        """
        dataset = self.main_window.DATASHACK[self.dataset_key]
        layers = list(dataset.layers.keys())
        self.selected_layer, ok = QInputDialog.getItem(self, "Select Transformed Layer", "Select transformed layer:", layers, 0, False)
        if ok:
            # Proceed to submit the changes
            self.submit_changes()

    def submit_changes(self):
        """
        Submits the changes made to the cofactor table and retransforms the dataset.
        """
        try:
            # Extract data from the table and update the DataFrame
            new_data = []
            for row in range(self.table.rowCount()):
                row_data = {}
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    row_data[self.table.horizontalHeaderItem(column).text()] = item.text() if item else ""
                new_data.append(row_data)

            new_cofactors = pd.DataFrame(new_data)
            cofactor_table = fp.dt.CofactorTable(cofactors=new_cofactors)
            dataset = self.main_window.DATASHACK[self.dataset_key]
            dataset.uns["cofactors"] = cofactor_table

            # Perform transformation if a layer was selected
            if self.selected_layer:
                fp.dt.transform(dataset,
                                transform="asinh",
                                key_added=self.selected_layer,
                                cofactor_table=cofactor_table)

            fp.sync.synchronize_dataset(dataset)

            # Update the dataset display
            self.main_window.update_current_dataset_display()

            # Show success message and close the window
            QMessageBox.information(self, "Success", "Cofactor table changed successfully.")
            self.close()
        except Exception as e:
            # Show error message
            error_message = str(e)
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

