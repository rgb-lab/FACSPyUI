from ._utils import EditableTableWidget

class MetadataTab(EditableTableWidget):
    def __init__(self):
        super().__init__(
            "Load a tabular text file to display and edit metadata:\n\n" + \
            "Drag-and-drop a .csv file or a .txt file\n" + \
            "or load the table via 'Modify Table > Load Table'\n" + \
            "or assemble the table by filling out the corresponding rows/columns",
            ["sample_ID", "file_name"]
        )
