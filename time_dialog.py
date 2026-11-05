from PySide6 import QtCore, QtWidgets


class TimeDialog(QtWidgets.QDialog):
    timeChanged = QtCore.Signal(QtCore.QTime)

    def __init__(self, time, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Time")

        self.time = QtWidgets.QTimeEdit(time)
        self.time.setDisplayFormat("mm:ss.z")
        self.time.setMinimumTime(QtCore.QTime(0, 0, 0, 0))
        self.time.setMaximumTime(QtCore.QTime(0, 10, 0, 0))
        self.close_button = QtWidgets.QPushButton("Close")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.time)
        layout.addWidget(self.close_button)
        self.time.timeChanged.connect(self.timeChanged)
        self.close_button.clicked.connect(self.close)
