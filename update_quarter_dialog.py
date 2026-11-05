from PySide6 import QtWidgets


class UpdateQuarterDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Skip to Next Quarter")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(
            QtWidgets.QLabel("Do you want to skip to the next quarter?", self)
        )

        self.ask_user_for_next_quarter = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        layout.addWidget(self.ask_user_for_next_quarter)
        self.ask_user_for_next_quarter.accepted.connect(self.accept)
        self.ask_user_for_next_quarter.rejected.connect(self.reject)
