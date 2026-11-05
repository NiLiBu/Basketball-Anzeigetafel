from PySide6 import QtCore, QtWidgets, QtGui


class CustomSpinBox(QtWidgets.QAbstractSpinBox):
    currentTextChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []
        self._index = -1
        self.lineEdit().setReadOnly(True)

    def addItems(self, items):
        self._items.extend(str(item) for item in items)
        if self._index == -1 and self._items:
            self.setCurrentIndex(0)

    def setCurrentIndex(self, index):
        if not self._items:
            self._index = -1
            self.lineEdit().clear()
            return

        new_index = max(0, min(index, len(self._items) - 1))
        if new_index == self._index:
            return

        self._index = new_index
        self.lineEdit().setText(self._items[self._index])
        self.currentTextChanged.emit(self.currentText())

    def currentIndex(self):
        return self._index

    def currentText(self):
        return self._items[self._index] if self._index >= 0 else ""

    def setCurrentText(self, text):
        if text in self._items:
            self.setCurrentIndex(self._items.index(text))
        else:
            raise ValueError(f"Text '{text}' not found in items.")

    def stepBy(self, steps):
        self.setCurrentIndex(self._index + steps)

    def stepEnabled(self):
        if not self._items:
            return QtWidgets.QAbstractSpinBox.StepNone

        enabled = QtWidgets.QAbstractSpinBox.StepNone
        if self._index > 0:
            enabled |= QtWidgets.QAbstractSpinBox.StepDownEnabled
        if self._index < len(self._items) - 1:
            enabled |= QtWidgets.QAbstractSpinBox.StepUpEnabled
        return enabled
