
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QMutex, QMutexLocker

import FACSPy as fp

from .._utils import LoadingScreen

class GateFrequenciesWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, dataset):
        super().__init__()
        self.dataset = dataset
        self._is_running = True
        self._mutex = QMutex()

    def run(self):
        try:
            with QMutexLocker(self._mutex):
                if not self._is_running:
                    self.error.emit("Gate frequency calculation was canceled.")
                    return

            fp.tl.gate_frequencies(self.dataset)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        with QMutexLocker(self._mutex):
            self._is_running = False

class GateFrequencyWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Calculate Gate Frequencies")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.calculate_gate_frequencies()

    def calculate_gate_frequencies(self):
        try:
            dataset_key = self.main_window.dataset_dropdown.currentText()
            dataset = self.main_window.DATASHACK.get(dataset_key, None)

            if dataset is None:
                raise ValueError("No dataset selected or dataset not found.")

            # Show loading screen
            loading_message = "Calculating gate frequencies..."
            self.loading_screen = LoadingScreen(main_window = self.main_window, message=loading_message)
            self.loading_screen.cancel_signal.connect(self.cancel_calculation)
            self.loading_screen.show()

            # Create and start the worker thread
            self.calculation_canceled = False
            self.gate_frequencies_worker = GateFrequenciesWorker(dataset)
            self.gate_frequencies_worker.finished.connect(self.on_gate_frequencies_finished)
            self.gate_frequencies_worker.error.connect(self.on_gate_frequencies_error)
            self.gate_frequencies_worker.start()

        except Exception as e:
            self.show_error("Gate Frequencies Calculation Error", str(e))

    def on_gate_frequencies_finished(self):
        self.loading_screen.close()
        if not self.calculation_canceled:
            QMessageBox.information(self, "Success", "Gate frequencies calculation completed.")
            self.main_window.update_current_dataset_display()
            self.close()

    def on_gate_frequencies_error(self, error_message):
        self.loading_screen.close()
        if not self.calculation_canceled:
            self.show_error("Gate Frequencies Calculation Error", error_message)

    def cancel_calculation(self):
        self.calculation_canceled = True
        if self.gate_frequencies_worker:
            self.gate_frequencies_worker.stop()
            self.loading_screen.close()
            QMessageBox.information(self, "Cancelled", "Gate frequencies calculation has been cancelled.")

    def show_error(self, title, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()
