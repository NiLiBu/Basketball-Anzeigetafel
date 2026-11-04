from PySide6 import QtCore, QtGui, QtWidgets

from CostumSpinBox import CustomSpinBox
from time_dialog import TimeDialog


class Scoreboard_Controller(QtWidgets.QWidget):
    timeChanged = QtCore.Signal(QtCore.QTime)

    KEY_POINTS_HOME_DOWN = "Q"
    KEY_POINTS_HOME_1 = "1"
    KEY_POINTS_HOME_2 = "2"
    KEY_POINTS_HOME_3 = "3"

    KEY_POINTS_AWAY_DOWN = "O"
    KEY_POINTS_AWAY_1 = "0"
    KEY_POINTS_AWAY_2 = "9"
    KEY_POINTS_AWAY_3 = "8"

    KEY_FOULS_HOME_UP = "Y"
    KEY_FOULS_HOME_DOWN = "X"

    KEY_FOULS_AWAY_UP = "N"
    KEY_FOULS_AWAY_DOWN = "M"

    KEY_TIME_UP = "Up"
    KEY_TIME_DOWN = "Down"

    KEY_TIMER_START_STOP = "Space"
    KEY_TIMER_STOP = "Escape"

    def __init__(self):

        super().__init__()

        self.points_home = QtWidgets.QSpinBox()
        self.points_home.setRange(0, 999)
        self.set_line_edit_selection_color(self.points_home.lineEdit())
        self.points_home.setFocusPolicy(QtCore.Qt.NoFocus)
        self.points_away = QtWidgets.QSpinBox()
        self.points_away.setRange(0, 999)
        self.set_line_edit_selection_color(self.points_away.lineEdit())
        self.points_away.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fouls_home = QtWidgets.QSpinBox()
        self.set_line_edit_selection_color(self.fouls_home.lineEdit())
        self.fouls_home.setRange(0, 5)
        self.fouls_home.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fouls_away = QtWidgets.QSpinBox()
        self.set_line_edit_selection_color(self.fouls_away.lineEdit())
        self.fouls_away.setRange(0, 5)
        self.fouls_away.setFocusPolicy(QtCore.Qt.NoFocus)
        self.time = QtWidgets.QPushButton("00:00.0")

        self.time_dialog = TimeDialog(QtCore.QTime(0, 0), self)
        self.time.clicked.connect(self.time_dialog.open)
        self.time_dialog.timeChanged.connect(self._time_changed)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._tick)

        self.quarter = CustomSpinBox()
        self.set_line_edit_selection_color(self.quarter.lineEdit())
        self.quarter.addItems(["1", "2", "HT", "3", "4", "E"])
        self.quarter.setCurrentIndex(0)
        self.quarter.setFocusPolicy(QtCore.Qt.NoFocus)

        self._shortcuts = []
        self._add_shortcut(self.KEY_POINTS_HOME_DOWN, self.points_home.stepDown)
        self._add_shortcut(self.KEY_POINTS_HOME_1, self.points_home.stepUp)
        self._add_shortcut(
            self.KEY_POINTS_HOME_2,
            lambda: self._add_points(self.points_home, 2),
        )
        self._add_shortcut(
            self.KEY_POINTS_HOME_3,
            lambda: self._add_points(self.points_home, 3),
        )
        self._add_shortcut(self.KEY_POINTS_AWAY_DOWN, self.points_away.stepDown)
        self._add_shortcut(self.KEY_POINTS_AWAY_1, self.points_away.stepUp)
        self._add_shortcut(
            self.KEY_POINTS_AWAY_2,
            lambda: self._add_points(self.points_away, 2),
        )
        self._add_shortcut(
            self.KEY_POINTS_AWAY_3,
            lambda: self._add_points(self.points_away, 3),
        )
        self._add_shortcut(self.KEY_FOULS_HOME_DOWN, self.fouls_home.stepDown)
        self._add_shortcut(self.KEY_FOULS_HOME_UP, self.fouls_home.stepUp)
        self._add_shortcut(self.KEY_FOULS_AWAY_UP, self.fouls_away.stepUp)
        self._add_shortcut(self.KEY_FOULS_AWAY_DOWN, self.fouls_away.stepDown)
        self._add_shortcut(self.KEY_TIME_UP, lambda: self._change_time(100))
        self._add_shortcut(self.KEY_TIME_DOWN, lambda: self._change_time(-100))
        self._add_shortcut(self.KEY_TIMER_START_STOP, self._toggle_timer)
        self._add_shortcut(self.KEY_TIMER_STOP, self._stop_timer)

        layout = QtWidgets.QFormLayout(self)
        layout.addRow("Points Home:", self.points_home)
        layout.addRow("Points Away:", self.points_away)
        layout.addRow("Fouls Home:", self.fouls_home)
        layout.addRow("Fouls Away:", self.fouls_away)
        layout.addRow("Time:", self.time)
        layout.addRow("Quarter:", self.quarter)

        controls = QtWidgets.QGroupBox("Controls")
        controls_layout = QtWidgets.QFormLayout(controls)
        controls_layout.addRow(
            "Points Home",
            self._points_control_buttons(
                self.points_home.stepDown,
                lambda: self._add_points(self.points_home, 1),
                lambda: self._add_points(self.points_home, 2),
                lambda: self._add_points(self.points_home, 3),
                self.KEY_POINTS_HOME_DOWN,
                self.KEY_POINTS_HOME_1,
                self.KEY_POINTS_HOME_2,
                self.KEY_POINTS_HOME_3,
            ),
        )
        controls_layout.addRow(
            "Points Away",
            self._points_control_buttons(
                self.points_away.stepDown,
                lambda: self._add_points(self.points_away, 1),
                lambda: self._add_points(self.points_away, 2),
                lambda: self._add_points(self.points_away, 3),
                self.KEY_POINTS_AWAY_DOWN,
                self.KEY_POINTS_AWAY_1,
                self.KEY_POINTS_AWAY_2,
                self.KEY_POINTS_AWAY_3,
            ),
        )
        controls_layout.addRow(
            "Fouls Home",
            self._control_buttons(
                "+1",
                "-1",
                self.fouls_home.stepUp,
                self.fouls_home.stepDown,
                self.KEY_FOULS_HOME_DOWN,
                self.KEY_FOULS_HOME_UP,
            ),
        )
        controls_layout.addRow(
            "Fouls Away",
            self._control_buttons(
                "+1",
                "-1",
                self.fouls_away.stepUp,
                self.fouls_away.stepDown,
                self.KEY_FOULS_AWAY_DOWN,
                self.KEY_FOULS_AWAY_UP,
            ),
        )
        controls_layout.addRow(
            "Time",
            self._control_buttons(
                "+0.1",
                "-0.1",
                lambda: self._change_time(100),
                lambda: self._change_time(-100),
                self.KEY_TIME_UP,
                self.KEY_TIME_DOWN,
            ),
        )
        controls_layout.addRow(
            "Timer",
            self._control_buttons(
                "Start/Stop",
                "Stop",
                self._toggle_timer,
                self._stop_timer,
                self.KEY_TIMER_START_STOP,
                self.KEY_TIMER_STOP,
            ),
        )
        layout.addRow(controls)

    def _add_shortcut(self, key, callback):
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(key), self)
        shortcut.setContext(QtCore.Qt.WindowShortcut)
        shortcut.activated.connect(callback)
        self._shortcuts.append(shortcut)

    @staticmethod
    def set_line_edit_selection_color(widget):
        """Set the selection color of a QLineEdit."""
        widget.setStyleSheet(
            "selection-background-color: white; selection-color: black"
        )

    @staticmethod
    def _points_control_buttons(
        minus_one,
        plus_one,
        plus_two,
        plus_three,
        minus_one_key,
        plus_one_key,
        plus_two_key,
        plus_three_key,
    ):
        widget = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(widget)
        button_layout.setContentsMargins(0, 0, 0, 0)

        for text, callback, key in (
            ("-1", minus_one, minus_one_key),
            ("+1", plus_one, plus_one_key),
            ("+2", plus_two, plus_two_key),
            ("+3", plus_three, plus_three_key),
        ):
            button = QtWidgets.QPushButton(f"{text} ({key})")
            button.clicked.connect(callback)
            button_layout.addWidget(button)
        return widget

    @staticmethod
    def _control_buttons(
        first_text, second_text, first_callback, second_callback, first_key, second_key
    ):
        widget = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(widget)
        button_layout.setContentsMargins(0, 0, 0, 0)

        first_button = QtWidgets.QPushButton(f"{first_text} ({first_key})")
        second_button = QtWidgets.QPushButton(f"{second_text} ({second_key})")
        first_button.clicked.connect(first_callback)
        second_button.clicked.connect(second_callback)
        button_layout.addWidget(first_button)
        button_layout.addWidget(second_button)
        return widget

    @staticmethod
    def _add_points(spinbox, points):
        spinbox.setValue(spinbox.value() + points)

    def _change_time(self, milliseconds):
        current = self.time_dialog.time.time()
        changed = current.addMSecs(milliseconds)
        minimum = QtCore.QTime(0, 0)
        maximum = QtCore.QTime(10, 0)
        self.time_dialog.time.setTime(max(minimum, min(maximum, changed)))

    def _tick(self):
        if self.time_dialog.time.time() == QtCore.QTime(0, 0):
            self._stop_timer()
        else:
            self.time_dialog.time.setTime(self.time_dialog.time.time().addMSecs(-100))

    def _toggle_timer(self):
        if self.timer.isActive():
            self._stop_timer()
        else:
            self._start_timer()

    def _start_timer(self):
        if self.time_dialog.time.time() != QtCore.QTime(0, 0):
            self.timer.start()
            self.time.setStyleSheet("background-color: lightgreen;")

    def _stop_timer(self):
        self.timer.stop()
        self.time.setStyleSheet("")

    def _time_changed(self, time):
        self.time.setText(time.toString("mm:ss.z"))
        self.timeChanged.emit(time)
