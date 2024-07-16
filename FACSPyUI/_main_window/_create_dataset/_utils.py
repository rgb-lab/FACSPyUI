from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFileDialog, 
                             QMenu, QInputDialog, QAbstractItemView)
from PyQt5.QtCore import Qt
import pandas as pd
from PyQt5.QtGui import QDropEvent, QDragEnterEvent


class EditableTableWidget(QWidget):
    def __init__(self, instructions, default_headers):
        super().__init__()
        self.layout = QVBoxLayout()

        # Create a QLabel for instructions
        self.label = QLabel(instructions)

        # Create a QTableWidget
        self.table = QTableWidget()
        self.initialize_table(default_headers)

        # Add widgets to the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        # Enable right-click context menu on the table header for removing columns
        self.table.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.horizontalHeader().customContextMenuRequested.connect(self.header_context_menu)

        # Make header editable
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.edit_column_name)

        # Enable drag and drop
        self.setAcceptDrops(True)
        self.table.setDragDropMode(QAbstractItemView.DropOnly)

    def initialize_table(self, headers):
        """
        Initializes the table with given headers.
        """
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)  # Initialize with no rows

    def load_table(self, file_name):
        """
        Loads a table from a file.
        """
        try:
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_name, sep=';')
            elif file_name.endswith('.tsv'):
                df = pd.read_csv(file_name, sep='\t')
            else:
                raise ValueError("Unsupported file type. Only CSV and TSV files are supported.")

            # Update the table headers
            self.initialize_table(df.columns)

            # Set the table row count to the dataframe length
            self.table.setRowCount(len(df))

            # Populate the table with data
            for row_index, row_data in df.iterrows():
                for column_index, value in enumerate(row_data):
                    self.table.setItem(row_index, column_index, QTableWidgetItem(str(value)))

        except Exception as e:
            print(f"Failed to load file: {e}")

    def add_column(self):
        """
        Adds a new column named 'new column' to the table.
        """
        current_column_count = self.table.columnCount()
        self.table.insertColumn(current_column_count)
        self.table.setHorizontalHeaderItem(current_column_count, QTableWidgetItem("new column"))

    def add_row(self):
        """
        Adds a new empty row to the table.
        """
        current_row_count = self.table.rowCount()
        self.table.insertRow(current_row_count)

    def remove_row(self):
        """
        Removes the currently selected row from the table.
        """
        selected_indexes = self.table.selectedIndexes()
        if selected_indexes:
            selected_row = selected_indexes[0].row()
            self.table.removeRow(selected_row)

    def header_context_menu(self, position):
        """
        Creates a context menu on the header for removing columns.
        """
        index = self.table.horizontalHeader().logicalIndexAt(position)
        if index >= 0:
            menu = QMenu()
            remove_action = menu.addAction("Remove Column")
            action = menu.exec_(self.table.horizontalHeader().viewport().mapToGlobal(position))
            if action == remove_action:
                self.remove_column(index)

    def remove_column(self, index):
        """
        Removes the column at the given index.
        """
        self.table.removeColumn(index)

    def remove_selected_column(self):
        """
        Removes the currently selected column.
        """
        selected_indexes = self.table.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            column = selected_index.column()
            self.remove_column(column)

    def remove_column_via_input(self):
        """
        Removes the currently selected column.
        """
        self.remove_selected_column()

    def edit_column_name(self, index):
        """
        Allows the user to edit the column name.
        """
        current_name = self.table.horizontalHeaderItem(index).text()
        new_name, ok = QInputDialog.getText(self, "Edit Column Name", "Enter new column name:", text=current_name)
        if ok and new_name:
            self.table.horizontalHeaderItem(index).setText(new_name)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        Accept the drag event if it contains URLs.
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """
        Handle the drop event to load the table from the dropped file.
        """
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_table(file_path)
