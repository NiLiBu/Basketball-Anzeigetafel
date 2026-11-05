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

    controller.pointsHomeChanged.connect(widget.set_points_home)
    controller.pointsAwayChanged.connect(widget.set_points_away)
    controller.foulsHomeChanged.connect(widget.set_fouls_home)
    controller.foulsAwayChanged.connect(widget.set_fouls_away)
    controller.timeChanged.connect(widget.set_time)
    controller.timeoutChanged.connect(widget.set_timeout)
    controller.quarterChanged.connect(widget.set_quarter)

    widget.set_points_home(controller.get_points_home())
    widget.set_points_away(controller.get_points_away())
    widget.set_fouls_home(controller.fouls_home.currentText())
    widget.set_fouls_away(controller.fouls_away.currentText())
    widget.set_time(controller.get_time())
    widget.set_timeout(controller.timeout.text())
    widget.set_quarter(controller.get_quarter())

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
