
import enum
import time
import sys
import os

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox
from PyQt6.QtGui import QFont, QIcon, QCursor
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt

from components.timer.stopwatch_controller import Stopwatch
from enums.system_status import SystemState
from utils.pathutil import get_relative_path


class TimerWidget(QWidget):
    status = QtCore.pyqtSignal(str)

    def __init__(self, parent: QWidget):
        super().__init__()

        self.timer_system = Stopwatch()
        self.parent_widget = parent

        self.build()
        self.__register_images()
        self.__init_timer_label()
        self.__init_control_button()
        self.__load_styles()

        self.timer_system.timer.connect(self.on_timer_update)

    def build(self):
        self.__init_layout()

    def __register_images(self):
        self.play_icon = get_relative_path(
            'src/icons/controls/play-circle.svg')
        self.pause_icon = get_relative_path(
            'src/icons/controls/pause-circle.svg')

    def __init_layout(self):
        self.timer_controls_layout = QHBoxLayout(self.parent_widget)
        self.timer_controls_layout.setContentsMargins(30, 0, 30, 0)
        self.timer_controls_layout.setSpacing(0)

    def __init_timer_label(self):
        self.control_button_play = QPushButton()
        self.control_button_play.setObjectName('timerplaybtn')
        self.control_button_play.setFixedSize(50, 50)
        self.control_button_play.setIcon(QIcon(self.play_icon))
        self.control_button_play.setIconSize(QSize(30, 30))

        self.control_button_pause = QPushButton()
        self.control_button_pause.setFixedSize(50, 50)
        self.control_button_pause.setObjectName('timerpausebtn')

        self.control_button_pause.setIcon(QIcon(self.pause_icon))
        self.control_button_pause.setIconSize(QSize(30, 30))
        self.control_button_pause.hide()

        self.control_button_pause.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.control_button_play.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))

        self.timer_label = QLabel()
        self.timer_label.setText("00:00:00")
        self.timer_label.setFont(QFont("Sanserif", 30, 800))
        self.timer_label.setObjectName('timerlbl')

        self.timer_controls_layout.addWidget(self.timer_label)
        self.timer_controls_layout.addWidget(self.control_button_play)
        self.timer_controls_layout.addWidget(self.control_button_pause)

    def toggle_control_button_state(self, state):
        """
        Timer button state manager for toggling between play and pause.
        """
        match state:
            case SystemState.STARTED:
                self.control_button_play.hide()
                self.control_button_pause.show()
            case SystemState.PAUSED:
                self.control_button_pause.hide()
                self.control_button_play.show()

    def __init_control_button(self):
        self.timer_system.start()

        self.control_button_play.clicked.connect(
            lambda: (self.timer_system.start_timer(), self.toggle_control_button_state(SystemState.STARTED)))
        self.control_button_pause.clicked.connect(
            lambda: (self.timer_system.pause_timer(), self.toggle_control_button_state(SystemState.PAUSED)))

    @ QtCore.pyqtSlot(str)
    def on_timer_update(self, timer_value):
        self.timer_label.setText(self.tr(str(timer_value)))

    def on_start_action(self):
        self.timer_system.start(SystemState.STARTED)

    def __load_styles(self):
        """
        Dynamically load the base QSS class for the the
        whole widget, main layout and its sub components.
        """
        path = get_relative_path('src/components/timer/stopwatch.qss')
        with open(path, "r") as f:
            _style = f.read()
            self.parent_widget.setStyleSheet(_style)
