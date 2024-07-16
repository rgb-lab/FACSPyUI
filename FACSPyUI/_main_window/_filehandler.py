import os
from PyQt5.QtWidgets import (QFileDialog, QMessageBox)
import FACSPy as fp
from ._create_dataset import CreateDatasetWindow

class FileHandler:
    def set_main_window(self, main_window):
        self.main_window = main_window

    def create_new_dataset(self):
        self.dataset_window = CreateDatasetWindow(self.main_window)
        self.dataset_window.show()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.main_window, "Open File", "", "H5AD Files (*.h5ad)")
        if file_name:
            try:
                dataset = fp.read_dataset(file_name = file_name)
                dataset_key = os.path.splitext(os.path.basename(file_name))[0]
                if dataset_key in self.main_window.DATASHACK:
                    dataset_key += "-1"
                self.main_window.DATASHACK[dataset_key] = dataset
                self.main_window.load_dataset(dataset_key, dataset)
                QMessageBox.information(self.main_window, "Success", f"Dataset '{dataset_key}' opened successfully.")
            except Exception as e:
                QMessageBox.critical(self.main_window, "Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        dataset_key = self.main_window.dataset_dropdown.currentText()
        if dataset_key not in self.main_window.DATASHACK:
            QMessageBox.warning(self.main_window, "Warning", "No dataset selected to save.")
            return

        # Open a dialog to select a file path for saving the file
        file_path, _ = QFileDialog.getSaveFileName(self.main_window, "Save File", f"{dataset_key}.h5ad", "H5AD Files (*.h5ad)")
        if file_path:
            output_directory = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)

            dataset = self.main_window.DATASHACK[dataset_key]

            try:
                # the OS handles the case of an existing filename
                fp.save_dataset(dataset, output_directory, file_name, overwrite = True)
                QMessageBox.information(self.main_window, "Success", f"Dataset saved successfully at {file_path}.")

            except Exception as e:
                QMessageBox.critical(self.main_window, "Error", f"Failed to save file: {str(e)}")
