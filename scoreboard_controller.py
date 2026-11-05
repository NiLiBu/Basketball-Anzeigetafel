from pathlib import Path

from PySide6 import QtCore, QtGui, QtMultimedia, QtWidgets

from custum_spin_box import CustomSpinBox
from update_quarter_dialog import UpdateQuarterDialog
from time_dialog import TimeDialog


class Scoreboard_Controller(QtWidgets.QWidget):
    timeChanged = QtCore.Signal(QtCore.QTime)
    pointsHomeChanged = QtCore.Signal(int)
    pointsAwayChanged = QtCore.Signal(int)
    foulsHomeChanged = QtCore.Signal(str)
    foulsAwayChanged = QtCore.Signal(str)
    timeoutChanged = QtCore.Signal(str)
    quarterChanged = QtCore.Signal(str)

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
        self.points_home.valueChanged.connect(self.pointsHomeChanged)
        self.points_away = QtWidgets.QSpinBox()
        self.points_away.setRange(0, 999)
        self.set_line_edit_selection_color(self.points_away.lineEdit())
        self.points_away.setFocusPolicy(QtCore.Qt.NoFocus)
        self.points_away.valueChanged.connect(self.pointsAwayChanged)
        self.fouls_home = CustomSpinBox()
        self.set_line_edit_selection_color(self.fouls_home.lineEdit())
        self.fouls_home.addItems(["0", "1", "2", "3", "4", "🟥"])
        self.set_fouls_home(0)
        self.fouls_home.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fouls_home.currentTextChanged.connect(self.foulsHomeChanged)
        self.fouls_away = CustomSpinBox()
        self.set_line_edit_selection_color(self.fouls_away.lineEdit())
        self.fouls_away.addItems(["0", "1", "2", "3", "4", "🟥"])
        self.set_fouls_away(0)
        self.fouls_away.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fouls_away.currentTextChanged.connect(self.foulsAwayChanged)
        self.time = QtWidgets.QPushButton("00:00.0")
        self.timeout = QtWidgets.QPushButton("00:00.0")
        self.timeout_time = QtCore.QTime(0, 0, 0, 0)
        self._history = QtWidgets.QListWidget()
        self._history.setMinimumHeight(140)
        self._history.setAlternatingRowColors(True)
        self._history_clock = QtCore.QElapsedTimer()
        self._history_clock.start()
        self._history_group = None
        self.timeout.clicked.connect(self._action("Timeout", self._start_timeout))
        self.buzzer = QtWidgets.QPushButton("Buzzer")
        self.buzzer_audio_output = QtMultimedia.QAudioOutput(self)
        self.buzzer_audio_output.setVolume(1.0)
        self.buzzer_player = QtMultimedia.QMediaPlayer(self)
        self.buzzer_player.setAudioOutput(self.buzzer_audio_output)
        self.buzzer_player.setSource(
            QtCore.QUrl.fromLocalFile(
                str(Path(__file__).resolve().with_name("Buzzer_Sound.mp3"))
            )
        )
        self.buzzer.clicked.connect(self._action("Buzzer", self._play_buzzer))

        self.time_dialog = TimeDialog(QtCore.QTime(0, 0), self)
        self.time.clicked.connect(self.time_dialog.open)
        self.time_dialog.timeChanged.connect(self._time_changed)

        self.quarter_end_dialog = UpdateQuarterDialog(self)
        self.quarter_end_dialog.rejected.connect(self._reject_quarter_end)
        self.quarter_end_dialog.accepted.connect(self._accept_quarter_end)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._tick)

        self.timeout_timer = QtCore.QTimer(self)
        self.timeout_timer.setInterval(100)
        self.timeout_timer.timeout.connect(self._tick_timeout)

        self.quarter = CustomSpinBox()
        self.set_line_edit_selection_color(self.quarter.lineEdit())
        self.quarter.addItems(["1", "2", "HT", "3", "4", "E"])
        self.set_quarter("1")
        self.quarter.setFocusPolicy(QtCore.Qt.NoFocus)
        self.quarter.currentTextChanged.connect(self.quarterChanged)

        self._shortcuts = []
        self._add_shortcut(
            self.KEY_POINTS_HOME_DOWN,
            lambda: self.set_points_home(self.get_points_home() - 1),
            "Points Home -1",
        )
        self._add_shortcut(
            self.KEY_POINTS_HOME_1,
            lambda: self.set_points_home(self.get_points_home() + 1),
            "Points Home +1",
        )
        self._add_shortcut(
            self.KEY_POINTS_HOME_2,
            lambda: self._add_points(self.get_points_home, self.set_points_home, 2),
            "Points Home +2",
        )
        self._add_shortcut(
            self.KEY_POINTS_HOME_3,
            lambda: self._add_points(self.get_points_home, self.set_points_home, 3),
            "Points Home +3",
        )
        self._add_shortcut(
            self.KEY_POINTS_AWAY_DOWN,
            lambda: self.set_points_away(self.get_points_away() - 1),
            "Points Away -1",
        )
        self._add_shortcut(
            self.KEY_POINTS_AWAY_1,
            lambda: self.set_points_away(self.get_points_away() + 1),
            "Points Away +1",
        )
        self._add_shortcut(
            self.KEY_POINTS_AWAY_2,
            lambda: self._add_points(self.get_points_away, self.set_points_away, 2),
            "Points Away +2",
        )
        self._add_shortcut(
            self.KEY_POINTS_AWAY_3,
            lambda: self._add_points(self.get_points_away, self.set_points_away, 3),
            "Points Away +3",
        )
        self._add_shortcut(
            self.KEY_FOULS_HOME_DOWN,
            lambda: self.set_fouls_home(self.get_fouls_home() - 1),
        )
        self._add_shortcut(
            self.KEY_FOULS_HOME_UP,
            lambda: self.set_fouls_home(self.get_fouls_home() + 1),
        )
        self._add_shortcut(
            self.KEY_FOULS_AWAY_UP,
            lambda: self.set_fouls_away(self.get_fouls_away() + 1),
        )
        self._add_shortcut(
            self.KEY_FOULS_AWAY_DOWN,
            lambda: self.set_fouls_away(self.get_fouls_away() - 1),
        )
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
        layout.addRow("Timeout:", self.timeout)
        layout.addRow("Quarter:", self.quarter)
        layout.addRow("History:", self._history)

        controls = QtWidgets.QGroupBox("Controls")
        controls_layout = QtWidgets.QFormLayout(controls)
        controls_layout.addRow(
            "Points Home",
            self._points_control_buttons(
                lambda: self.set_points_home(self.get_points_home() - 1),
                lambda: self._add_points(self.get_points_home, self.set_points_home, 1),
                lambda: self._add_points(self.get_points_home, self.set_points_home, 2),
                lambda: self._add_points(self.get_points_home, self.set_points_home, 3),
                self.KEY_POINTS_HOME_DOWN,
                self.KEY_POINTS_HOME_1,
                self.KEY_POINTS_HOME_2,
                self.KEY_POINTS_HOME_3,
                "Points Home",
            ),
        )
        controls_layout.addRow(
            "Points Away",
            self._points_control_buttons(
                lambda: self.set_points_away(self.get_points_away() - 1),
                lambda: self._add_points(self.get_points_away, self.set_points_away, 1),
                lambda: self._add_points(self.get_points_away, self.set_points_away, 2),
                lambda: self._add_points(self.get_points_away, self.set_points_away, 3),
                self.KEY_POINTS_AWAY_DOWN,
                self.KEY_POINTS_AWAY_1,
                self.KEY_POINTS_AWAY_2,
                self.KEY_POINTS_AWAY_3,
                "Points Away",
            ),
        )
        controls_layout.addRow(
            "Fouls Home",
            self._control_buttons(
                "+1",
                "-1",
                lambda: self.set_fouls_home(self.get_fouls_home() + 1),
                lambda: self.set_fouls_home(self.get_fouls_home() - 1),
                self.KEY_FOULS_HOME_DOWN,
                self.KEY_FOULS_HOME_UP,
            ),
        )
        controls_layout.addRow(
            "Fouls Away",
            self._control_buttons(
                "+1",
                "-1",
                lambda: self.set_fouls_away(self.get_fouls_away() + 1),
                lambda: self.set_fouls_away(self.get_fouls_away() - 1),
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
        controls_layout.addRow(
            "Timeout",
            self._control_buttons(
                "Timeout",
                "Reset",
                self._start_timeout,
                self._reset_timeout,
                None,
                None,
            ),
        )
        controls_layout.addRow(
            "Quarter Break",
            self._control_buttons(
                "Quarter Break",
                "Reset",
                self._start_quarter_break,
                self._reset_timeout,
                None,
                None,
            ),
        )
        controls_layout.addRow("Buzzer", self.buzzer)

        layout.addRow(controls)

    def get_points_home(self):
        return self.points_home.value()

    def set_points_home(self, value):
        self.points_home.setValue(value)

    def get_points_away(self):
        return self.points_away.value()

    def set_points_away(self, value):
        self.points_away.setValue(value)

    def get_fouls_home(self):
        return self.fouls_home.currentIndex()

    def set_fouls_home(self, value):
        self.fouls_home.setCurrentIndex(max(0, min(5, int(value))))

    def get_fouls_away(self):
        return self.fouls_away.currentIndex()

    def set_fouls_away(self, value):
        self.fouls_away.setCurrentIndex(max(0, min(5, int(value))))

    def get_time(self):
        return self.time_dialog.time.time()

    def set_time(self, value):
        self.time_dialog.time.setTime(value)

    def get_quarter(self):
        return self.quarter.currentText()

    def set_quarter(self, value):
        self.quarter.setCurrentText(str(value))

    def _add_shortcut(self, key, callback, description=None):
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(key), self)
        shortcut.setContext(QtCore.Qt.WindowShortcut)
        shortcut.activated.connect(
            self._action(description or f"Taste {key}", callback)
        )
        self._shortcuts.append(shortcut)

    def _action(self, description, callback):
        def action():
            self._add_history_entry(description)
            callback()

        return action

    def _add_history_entry(self, description):
        timer_time = self.get_time()
        real_time = self._history_clock.elapsed()
        group = self._history_group
        same_group = group is not None and (
            abs(group["timer"].msecsTo(timer_time)) <= 1000
            or real_time - group["real"] <= 2000
        )
        if same_group:
            group["actions"].append(description)
            group["timer"] = timer_time
            group["real"] = real_time
            self._history.item(0).setText(self._history_text(group))
        else:
            group = {
                "timer": timer_time,
                "real": real_time,
                "actions": [description],
            }
            self._history_group = group
            self._history.insertItem(0, self._history_text(group))
        self._history.scrollToTop()

    @staticmethod
    def _history_text(group):
        return f"{group['timer'].toString('mm:ss.z')} – " + ", ".join(group["actions"])

    def set_line_edit_selection_color(self, widget):
        """Set the selection color of a QLineEdit."""
        widget.setStyleSheet(
            "selection-background-color: white; selection-color: black"
        )

    def _points_control_buttons(
        self,
        minus_one,
        plus_one,
        plus_two,
        plus_three,
        minus_one_key,
        plus_one_key,
        plus_two_key,
        plus_three_key,
        description_prefix,
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
            button.clicked.connect(
                self._action(f"{description_prefix} {text}", callback)
            )
            button_layout.addWidget(button)
        return widget

    def _control_buttons(
        self,
        first_text,
        second_text,
        first_callback,
        second_callback,
        first_key,
        second_key,
    ):
        widget = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(widget)
        button_layout.setContentsMargins(0, 0, 0, 0)

        if first_key is None:
            first_button = QtWidgets.QPushButton(first_text)
        else:
            first_button = QtWidgets.QPushButton(f"{first_text} ({first_key})")
        if second_key is None:
            second_button = QtWidgets.QPushButton(second_text)
        else:
            second_button = QtWidgets.QPushButton(f"{second_text} ({second_key})")
        first_button.clicked.connect(
            self._action(f"{first_text} ({first_key})", first_callback)
        )
        second_button.clicked.connect(
            self._action(f"{second_text} ({second_key})", second_callback)
        )
        button_layout.addWidget(first_button)
        button_layout.addWidget(second_button)
        return widget

    @staticmethod
    @staticmethod
    def _add_points(get_points, set_points, points):
        set_points(get_points() + points)

    def _change_time(self, milliseconds):
        current = self.time_dialog.time.time()
        changed = current.addMSecs(milliseconds)
        minimum = QtCore.QTime(0, 0, 0, 0)
        maximum = QtCore.QTime(0, 50, 0, 0)
        self.time_dialog.time.setTime(max(minimum, min(maximum, changed)))

    def _tick(self):
        if self.time_dialog.time.time() <= QtCore.QTime(0, 0, 0, 100):
            self.set_time(QtCore.QTime(0, 0, 0, 0))
            self._play_buzzer()
            self._stop_timer()
        elif self.time_dialog.time.time() > QtCore.QTime(0, 50, 0, 0):

            self._stop_timer()
            self.set_time(QtCore.QTime(0, 0, 0, 0))
        else:
            self.time_dialog.time.setTime(self.time_dialog.time.time().addMSecs(-100))

    def _tick_timeout(self):
        if self.timeout_time <= QtCore.QTime(0, 0, 0, 100):
            self.timeout_time = QtCore.QTime(0, 0, 0, 0)
            self.timeout_timer.stop()
            self.timeout.setStyleSheet("")
            self._play_buzzer()
        else:
            self.timeout_time = self.timeout_time.addMSecs(-100)
        self._set_timeout_text()

    def _set_timeout_text(self):
        text = self.timeout_time.toString("mm:ss.z")
        self.timeout.setText(text)
        self.timeoutChanged.emit(text)

    def _start_timeout(self):
        if not self.timeout_timer.isActive():
            self.timeout_time = QtCore.QTime(0, 1, 0, 0)
            self._set_timeout_text()
            self.timeout_timer.start()
            self.timeout.setStyleSheet("background-color: lightgreen;")

    def _start_quarter_break(self):
        if not self.timeout_timer.isActive():
            self.timeout_time = QtCore.QTime(0, 2, 0, 0)
            self._set_timeout_text()
            self.timeout_timer.start()
            self.timeout.setStyleSheet("background-color: lightgreen;")

    def _reset_timeout(self):
        self.timeout_timer.stop()
        self.timeout_time = QtCore.QTime(0, 0, 0, 0)
        self._set_timeout_text()
        self.timeout.setStyleSheet("")

    def _play_buzzer(self):
        self.buzzer_player.setPosition(0)
        self.buzzer_player.play()

    def _toggle_timer(self):
        if self.timer.isActive():
            self._stop_timer()
        else:
            self._start_timer()

    def _start_timer(self):
        if self.time_dialog.time.time() != QtCore.QTime(0, 0, 0, 0):
            self.timer.start()
            self.time.setStyleSheet("background-color: lightgreen;")

    def _stop_timer(self):
        self.timer.stop()
        self.time.setStyleSheet("")
        if self.time_dialog.time.time() == QtCore.QTime(0, 0, 0, 0):

            self.quarter_end_dialog.show()

    def _reject_quarter_end(self):
        pass

    def _accept_quarter_end(self):
        match self.quarter.currentText():
            case "1":
                self.set_quarter("2")
                self.set_fouls_away(0)
                self.set_fouls_home(0)
                self.set_time(QtCore.QTime(0, 10, 0, 0))
                self._start_quarter_break()
            case "2":
                self.set_quarter("HT")
                self.set_fouls_away(0)
                self.set_fouls_home(0)
                self.set_time(QtCore.QTime(0, 15, 0, 0))
                self._start_timer()
            case "HT":
                self.set_quarter("3")
                self.set_fouls_away(0)
                self.set_fouls_home(0)
                self.set_time(QtCore.QTime(0, 10, 0, 0))
            case "3":
                self.set_quarter("4")
                self.set_fouls_away(0)
                self.set_fouls_home(0)
                self.set_time(QtCore.QTime(0, 10, 0, 0))
                self._start_quarter_break()
            case "4":
                self.set_quarter("E")
                self.set_fouls_away(0)
                self.set_fouls_home(0)
                self.set_time(QtCore.QTime(0, 5, 0, 0))
                self._start_quarter_break()
            case "E":
                self.set_quarter("E")
                self.set_fouls_away(0)
                self.set_fouls_home(0)
                self.set_time(QtCore.QTime(0, 5, 0, 0))
                self._start_quarter_break()

    def _time_changed(self, time):
        self.time.setText(time.toString("mm:ss.z"))
        self.timeChanged.emit(time)
