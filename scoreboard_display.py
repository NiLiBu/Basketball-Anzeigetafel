from PySide6 import QtCore, QtWidgets


class Scoreboard_Display(QtWidgets.QWidget):
    style_label = "font-weight: bold;"

    def __init__(self):
        super().__init__()
        self.dark_theme = False

        self.points_home = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.points_home_label = QtWidgets.QLabel(
            "Points Home", alignment=QtCore.Qt.AlignCenter
        )
        self.points_home_layout = QtWidgets.QVBoxLayout()
        self.points_home_layout.addWidget(self.points_home_label)
        self.points_home_layout.addWidget(self.points_home)
        self.points_home_layout.setContentsMargins(0, 0, 0, 0)

        self.points_away = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.points_away_label = QtWidgets.QLabel(
            "Points Away", alignment=QtCore.Qt.AlignCenter
        )
        self.points_away_layout = QtWidgets.QVBoxLayout()
        self.points_away_layout.addWidget(self.points_away_label)
        self.points_away_layout.addWidget(self.points_away)
        self.points_away_layout.setContentsMargins(0, 0, 0, 0)

        self.fouls_home = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.fouls_home_label = QtWidgets.QLabel(
            "Fouls Home", alignment=QtCore.Qt.AlignCenter
        )
        self.fouls_home_layout = QtWidgets.QVBoxLayout()
        self.fouls_home_layout.addWidget(self.fouls_home_label)
        self.fouls_home_layout.addWidget(self.fouls_home)
        self.fouls_home_layout.setContentsMargins(0, 0, 0, 0)

        self.fouls_away = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.fouls_away_label = QtWidgets.QLabel(
            "Fouls Away", alignment=QtCore.Qt.AlignCenter
        )
        self.fouls_away_layout = QtWidgets.QVBoxLayout()
        self.fouls_away_layout.addWidget(self.fouls_away_label)
        self.fouls_away_layout.addWidget(self.fouls_away)
        self.fouls_away_layout.setContentsMargins(0, 0, 0, 0)

        self.timeout = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.timeout_label = QtWidgets.QLabel(
            "Timeout", alignment=QtCore.Qt.AlignCenter
        )
        self.timeout_layout = QtWidgets.QVBoxLayout()
        self.timeout_layout.addWidget(self.timeout_label)
        self.timeout_layout.addWidget(self.timeout)
        self.timeout_layout.setContentsMargins(0, 0, 0, 0)
        self._update_timeout_visibility()

        self.time = QtWidgets.QLabel("10:00.0", alignment=QtCore.Qt.AlignCenter)
        self.time_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.time_layout = QtWidgets.QVBoxLayout()
        self.time_layout.addWidget(self.time_label)
        self.time_layout.addWidget(self.time)
        self.time_layout.setContentsMargins(0, 0, 0, 0)

        self.quarter = QtWidgets.QLabel("1", alignment=QtCore.Qt.AlignCenter)
        self.quarter_label = QtWidgets.QLabel(
            "Quarter", alignment=QtCore.Qt.AlignCenter
        )
        self.quarter_layout = QtWidgets.QVBoxLayout()
        self.quarter_layout.addWidget(self.quarter_label)
        self.quarter_layout.addWidget(self.quarter)

        self.theme_toggle = QtWidgets.QCheckBox("Dark Theme")
        self.theme_toggle.toggled.connect(self._set_dark_theme)

        self.top_layout = QtWidgets.QGridLayout(self)
        self.top_layout.addLayout(self.points_home_layout, 0, 0)
        self.top_layout.addLayout(self.points_away_layout, 0, 2)
        self.top_layout.addLayout(self.fouls_home_layout, 2, 0)
        self.top_layout.addLayout(self.fouls_away_layout, 2, 2)
        self.top_layout.addLayout(self.timeout_layout, 2, 1)
        self.top_layout.addLayout(self.time_layout, 1, 1)
        self.top_layout.addLayout(self.quarter_layout, 0, 1)
        self.top_layout.addWidget(self.theme_toggle, 3, 0, 1, 3, QtCore.Qt.AlignCenter)
        self._update_font_sizes()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_sizes()

    def _update_font_sizes(self):
        scale = min(self.width() / 400, self.height() / 300)
        label_size = max(12, round(24 * scale))
        value_size = max(30, round(45 * scale))
        label_style = self._label_style()

        for label in (
            self.points_home_label,
            self.points_away_label,
            self.fouls_home_label,
            self.fouls_away_label,
            self.time_label,
            self.quarter_label,
            self.timeout_label,
        ):
            label.setStyleSheet(f"{label_style} font-size: {label_size}px;")

        for value, style in (
            (self.points_home, self._points_style()),
            (self.points_away, self._points_style()),
            (self.fouls_home, self._fouls_style()),
            (self.fouls_away, self._fouls_style()),
            (self.time, self._time_style()),
            (self.quarter, self._quarter_style()),
            (self.timeout, self._time_style()),
        ):
            value.setStyleSheet(f"{style} font-size: {value_size}px;")

    def _label_style(self):
        color = "#f0f0f0" if self.dark_theme else "black"
        return f"{self.style_label} color: {color};"

    def _points_style(self):
        color = "#f0f0f0" if self.dark_theme else "black"
        return f"font-weight: bold; color: {color};"

    def _fouls_style(self):
        color = "#66b3ff" if self.dark_theme else "blue"
        return f"font-weight: bold; color: {color};"

    def _time_style(self):
        return "font-weight: bold; color: red;"

    def _quarter_style(self):
        color = "#66e066" if self.dark_theme else "green"
        return f"font-weight: bold; color: {color};"

    @QtCore.Slot(bool)
    def _set_dark_theme(self, enabled):
        self.dark_theme = enabled
        if enabled:
            self.setStyleSheet(
                "Scoreboard_Display { background-color: #121212; }"
                " QCheckBox { color: #f0f0f0; }"
            )
        else:
            self.setStyleSheet("")
        self._update_font_sizes()

    def _update_timeout_visibility(self):
        timeout = QtCore.QTime.fromString(self.timeout.text(), "mm:ss.z")
        if timeout.isValid():
            visible = timeout != QtCore.QTime(0, 0, 0, 0)
        else:
            visible = self.timeout.text().strip() not in ("", "0", "0.0")
        self.timeout.setVisible(visible)
        self.timeout_label.setVisible(visible)

    @QtCore.Slot(int)
    def set_points_home(self, value):
        self.points_home.setText(str(value))

    @QtCore.Slot(int)
    def set_points_away(self, value):
        self.points_away.setText(str(value))

    @QtCore.Slot(str)
    def set_fouls_home(self, value):
        self.fouls_home.setText(value)

    @QtCore.Slot(str)
    def set_fouls_away(self, value):
        self.fouls_away.setText(value)

    @QtCore.Slot(QtCore.QTime)
    def set_time(self, value):
        self.time.setText(value.toString("mm:ss.z"))

    @QtCore.Slot(str)
    def set_timeout(self, value):
        self.timeout.setText(value)
        self._update_timeout_visibility()

    @QtCore.Slot(str)
    def set_quarter(self, value):
        self.quarter.setText(value)
