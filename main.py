import sys

from PySide6 import QtWidgets

from scoreboard_controller import Scoreboard_Controller
from scoreboard_display import Scoreboard_Display
from time_dialog import TimeDialog

__all__ = ["Scoreboard_Controller", "Scoreboard_Display", "TimeDialog"]


def main():
    app = QtWidgets.QApplication([])

    controller = Scoreboard_Controller()
    controller.setWindowTitle("Scoreboard Controller")
    controller.resize(300, 200)
    controller.show()

    widget = Scoreboard_Display()
    widget.setWindowTitle("Scoreboard Display")
    widget.resize(400, 300)
    widget.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
