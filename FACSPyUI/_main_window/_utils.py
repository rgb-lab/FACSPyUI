from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QDialog,
                             QVBoxLayout, QListWidget, QListWidgetItem,
                             QDialogButtonBox, QLabel, QLineEdit,
                             QPushButton, QSizePolicy, QToolTip)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtSvg import QSvgWidget
import os
from ._paths import ICON_PATH as icon_dir
from functools import wraps

class LoadingScreen(QWidget):
    cancel_signal = pyqtSignal()  # Signal to cancel the operation

    def __init__(self, main_window, message="Processing..."):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet(self.main_window.stylesheet)
        self.setWindowTitle("Loading")
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.spinner = QMovie(os.path.join(icon_dir, "spinner.gif"))

        self.label.setAlignment(Qt.AlignCenter)
        self.spinner_label = QLabel()
        self.spinner_label.setScaledContents(True)
        self.spinner_label.setFixedSize(30,30)
        self.spinner_label.setAlignment(Qt.AlignCenter)
        self.spinner_label.setMovie(self.spinner)
        self.spinner.start()

        layout.addWidget(self.label, alignment = Qt.AlignCenter)
        layout.addWidget(self.spinner_label, alignment = Qt.AlignCenter)

        # Create and add the Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        # Set the minimum size of the window
        self.setMinimumSize(300, 150)

        # Optionally, set a size hint if you want the window to have an initial size
        self.resize(self.sizeHint())

    def on_cancel(self):
        """
        Handle the cancel button click.
        Emit a signal that the operation should be canceled.
        """
        self.cancel_signal.emit()
        self.close()

class MultiSelectComboBox(QWidget):
    selection_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

        self.items = []
        self.selected_items = []
        self.current_items_text = ""

    def old_layout(self):
        self.setLayout(QHBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # Create a line edit to display selected items
        self.line_edit = QLineEdit(self)
        self.line_edit.setReadOnly(True)
        self.line_edit.setPlaceholderText("Select multiple values")
        self.layout().addWidget(self.line_edit)

        # Create a button to open the selection dialog
        self.select_button = QPushButton("...", self)
        self.select_button.setFixedWidth(30)
        self.select_button.clicked.connect(self.show_selection_dialog)
        self.layout().addWidget(self.select_button)


    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container_widget = QWidget(self)
        container_layout = QHBoxLayout(container_widget)
        
        self.line_edit = QLineEdit(container_widget)
        self.line_edit.setReadOnly(True)
        self.line_edit.setPlaceholderText("Select multiple values")
        self.line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.select_button = QPushButton("...", container_widget)
        self.select_button.setContentsMargins(0,0,0,0)
        self.select_button.setFixedWidth(30)
        self.select_button.setFixedHeight(self.line_edit.sizeHint().height())
        self.select_button.clicked.connect(self.show_selection_dialog)
        
        container_layout.addWidget(self.line_edit)
        container_layout.addWidget(self.select_button)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)

        main_layout.addWidget(container_widget)

    def addItems(self, items):
        """
        Adds multiple items to the combo box.
        """
        self.items.extend(items)
        self.updateSelection()

    def addItem(self, item):
        """
        Adds a single item to the combo box.
        """
        self.items.append(item)
        self.updateSelection()

    def show_selection_dialog(self):
        # Open dialog for selecting items
        dialog = MultiSelectDialog(self.items, self.selected_items, self)
        if dialog.exec_() == QDialog.Accepted:
            self.selected_items = dialog.selected_items
            self.updateSelection()
            self.selection_changed.emit(self.selected_items)

    def updateSelection(self):
        # Update the line edit text to show selected items
        if len(self.selected_items) == len(self.items):
            self.current_items_text = "All values selected"
        else:
            self.current_items_text = ", ".join(self.selected_items)
        self.line_edit.setText(self.current_items_text)

    def currentText(self):
        # Return selected items as list of strings
        return self.selected_items

    def clear(self):
        """
        Clears the items in the combo box.
        """
        self.items.clear()
        self.selected_items.clear()
        self.updateSelection()


class MultiSelectDialog(QDialog):
    def __init__(self, items, selected_items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Items")
        self.selected_items = selected_items[:]

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)
            list_item.setCheckState(Qt.Checked if item in selected_items else Qt.Unchecked)
            self.list_widget.addItem(list_item)

        layout.addWidget(self.list_widget)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def accept(self):
        # Collect selected items
        self.selected_items = [self.list_widget.item(i).text() for i in range(self.list_widget.count()) if self.list_widget.item(i).checkState() == Qt.Checked]
        super().accept()

    def reject(self):
        super().reject()

def error_handler(error_origin):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.show_error(error_origin, str(e))
        return wrapper
    return decorator

class HoverLabel(QLabel):
    def __init__(self,
                 dimension = 30,
                 darkmode: bool = False,
                 hover_info: str = "For further information refer to FACSPy documentation.",
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        if darkmode:
            icon = os.path.join(icon_dir, "_info_dark.svg")
        else:
            icon = os.path.join(icon_dir, "_info_light.svg")
        self.svg_widget = QSvgWidget(icon)
        self.svg_widget.setFixedSize(dimension, dimension)
        layout.addWidget(self.svg_widget)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.setFixedSize(dimension, dimension)

        tooltip_text = f"""
         <div style="width: 500px;">
            {hover_info}
        </div>
        """
        tooltip_text = self._parse_documentation(hover_info)
        self.setToolTip(tooltip_text)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        QToolTip.showText(event.globalPos(), self.toolTip())
        super().enterEvent(event)

    def _parse_documentation(self, text):
        text = "<p>" + text + "</p"
        return text

