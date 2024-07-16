from ._utils import EditableTableWidget

class PanelTab(EditableTableWidget):
    def __init__(self):
        super().__init__(
            "Manage panel data with columns for FCS and antigens:\n\n" + \
            "Drag-and-drop a .csv file or a .txt file\n" + \
            "or load the table via 'Modify Table > Load Table'\n" + \
            "or assemble the table by filling out the corresponding rows/columns",
            ["fcs_colname", "antigens"]
        )
