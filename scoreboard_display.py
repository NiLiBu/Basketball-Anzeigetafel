from PySide6 import QtCore, QtWidgets


class Scoreboard_Display(QtWidgets.QWidget):
    style_label = "font-weight: bold;"
    style_points = "font-weight: bold; color: black;"
    style_time = "font-weight: bold; color: red;"
    style_fouls = "font-weight: bold; color: blue;"
    style_quarter = "font-weight: bold; color: green;"

    def __init__(self):
        super().__init__()

        self.points_home = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.points_home.setStyleSheet(self.style_points)
        self.points_home_label = QtWidgets.QLabel(
            "Points Home", alignment=QtCore.Qt.AlignCenter
        )
        self.points_home_label.setStyleSheet(self.style_label)
        self.points_home_layout = QtWidgets.QVBoxLayout()
        self.points_home_layout.addWidget(self.points_home_label)
        self.points_home_layout.addWidget(self.points_home)
        self.points_home_layout.setContentsMargins(0, 0, 0, 0)

        self.points_away = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.points_away.setStyleSheet(self.style_points)
        self.points_away_label = QtWidgets.QLabel(
            "Points Away", alignment=QtCore.Qt.AlignCenter
        )
        self.points_away_label.setStyleSheet(self.style_label)
        self.points_away_layout = QtWidgets.QVBoxLayout()
        self.points_away_layout.addWidget(self.points_away_label)
        self.points_away_layout.addWidget(self.points_away)
        self.points_away_layout.setContentsMargins(0, 0, 0, 0)

        self.fouls_home = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.fouls_home.setStyleSheet(self.style_fouls)
        self.fouls_home_label = QtWidgets.QLabel(
            "Fouls Home", alignment=QtCore.Qt.AlignCenter
        )
        self.fouls_home_label.setStyleSheet(self.style_label)
        self.fouls_home_layout = QtWidgets.QVBoxLayout()
        self.fouls_home_layout.addWidget(self.fouls_home_label)
        self.fouls_home_layout.addWidget(self.fouls_home)
        self.fouls_home_layout.setContentsMargins(0, 0, 0, 0)

        self.fouls_away = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        self.fouls_away.setStyleSheet(self.style_fouls)
        self.fouls_away_label = QtWidgets.QLabel(
            "Fouls Away", alignment=QtCore.Qt.AlignCenter
        )
        self.fouls_away_label.setStyleSheet(self.style_label)
        self.fouls_away_layout = QtWidgets.QVBoxLayout()
        self.fouls_away_layout.addWidget(self.fouls_away_label)
        self.fouls_away_layout.addWidget(self.fouls_away)
        self.fouls_away_layout.setContentsMargins(0, 0, 0, 0)

        self.time = QtWidgets.QLabel("00:00.0", alignment=QtCore.Qt.AlignCenter)
        self.time.setStyleSheet(self.style_time)
        self.time_label = QtWidgets.QLabel("Time", alignment=QtCore.Qt.AlignCenter)
        self.time_label.setStyleSheet(self.style_label)
        self.time_layout = QtWidgets.QVBoxLayout()
        self.time_layout.addWidget(self.time_label)
        self.time_layout.addWidget(self.time)
        self.time_layout.setContentsMargins(0, 0, 0, 0)

        self.quarter = QtWidgets.QLabel("1", alignment=QtCore.Qt.AlignCenter)
        self.quarter.setStyleSheet(self.style_quarter)
        self.quarter_label = QtWidgets.QLabel(
            "Quarter", alignment=QtCore.Qt.AlignCenter
        )
        self.quarter_label.setStyleSheet(self.style_label)
        self.quarter_layout = QtWidgets.QVBoxLayout()
        self.quarter_layout.addWidget(self.quarter_label)
        self.quarter_layout.addWidget(self.quarter)

        self.top_layout = QtWidgets.QGridLayout(self)
        self.top_layout.addLayout(self.points_home_layout, 0, 0)
        self.top_layout.addLayout(self.points_away_layout, 0, 2)
        self.top_layout.addLayout(self.fouls_home_layout, 2, 0)
        self.top_layout.addLayout(self.fouls_away_layout, 2, 2)
        self.top_layout.addLayout(self.time_layout, 1, 1)
        self.top_layout.addLayout(self.quarter_layout, 0, 1)
        self._update_font_sizes()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_font_sizes()

    def _update_font_sizes(self):
        scale = min(self.width() / 300, self.height() / 200)
        label_size = max(8, round(16 * scale))
        value_size = max(12, round(24 * scale))

        for label in (
            self.points_home_label,
            self.points_away_label,
            self.fouls_home_label,
            self.fouls_away_label,
            self.time_label,
            self.quarter_label,
        ):
            label.setStyleSheet(f"{self.style_label} font-size: {label_size}px;")

        for value, style in (
            (self.points_home, self.style_points),
            (self.points_away, self.style_points),
            (self.fouls_home, self.style_fouls),
            (self.fouls_away, self.style_fouls),
            (self.time, self.style_time),
            (self.quarter, self.style_quarter),
        ):
            value.setStyleSheet(f"{style} font-size: {value_size}px;")
