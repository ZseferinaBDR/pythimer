import enum
import time
import sys

from threading import Thread
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox
from PyQt6.QtGui import QFont, QIcon, QCursor
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QThread, QRect, QSize, Qt
from datetime import timedelta
from enums.system_status import SystemState
from PyQt6 import QtWidgets


from timer.time_system import TimeSystem


class MainWindow(QWidget):

    status = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.timer_system = TimeSystem()

        self.__init_window_properties()
        self.__init_translucent_layout()

        self.__init_timer_label()
        self.__init_control_button()

        self.timer_system.timer.connect(self.on_timer_update)

    def __init_window_properties(self):
        self.setGeometry(200, 200, 400, 140)
        self.setFixedSize(400, 140)
        self.setWindowTitle("Pythimer")

    def __init_translucent_layout(self):
        self.visible_child = QtWidgets.QWidget(self)
        self.visible_child.setStyleSheet(
            'QWidget{background: rgba(12, 12, 12, .95); border-radius: 10px; border:1px solid #2b2b2b;}')
        self.visible_child.setObjectName('vc')
        self.visible_child.setFixedSize(300, 100)

        self.exit_button = QPushButton(self.visible_child)
        self.exit_button.setStyleSheet(
            'background:transparent; color:black;border: none;')
        self.exit_button.setGeometry(275, 5, 15, 15)
        self.exit_button.setIcon(QIcon('x.svg'))

        self.exit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.exit_button.clicked.connect(lambda: self.exit_application())

    def exit_application(self):
        sys.exit()

    def __init_timer_label(self):
        self.timer_controls_layout = QHBoxLayout(self.visible_child)
        self.timer_controls_layout.setContentsMargins(30, 0, 30, 0)
        self.timer_controls_layout.setSpacing(0)

        self.control_button_play = QPushButton()
        self.control_button_play.setFixedSize(50, 50)
        self.control_button_play.setStyleSheet(
            'color:#F4F4F4;background-color: #4EBE9E; border: 1px solid black; border-radius:5px;')

        self.control_button_play.setIcon(QIcon('play-circle.svg'))
        self.control_button_play.setIconSize(QSize(30, 30))

        self.control_button_pause = QPushButton()
        self.control_button_pause.setFixedSize(50, 50)
        self.control_button_pause.setStyleSheet(
            'color:#F4F4F4;background-color: #4869fd; border: 1px; border-radius:5px;')

        self.control_button_pause.setIcon(QIcon('pause-circle.svg'))
        self.control_button_pause.setIconSize(QSize(30, 30))
        self.control_button_pause.hide()

        self.control_button_pause.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))
        self.control_button_play.setCursor(
            QCursor(Qt.CursorShape.PointingHandCursor))

        self.timer_label = QLabel()
        self.timer_label.setText("00:00:00")
        self.timer_label.setFont(QFont("Sanserif", 30, 800))
        self.timer_label.setStyleSheet(
            'color:#F4F4F4;background-color: transparent;border:none;')

        self.timer_controls_layout.addWidget(self.timer_label)
        self.timer_controls_layout.addWidget(self.control_button_play)
        self.timer_controls_layout.addWidget(self.control_button_pause)

    def toggle_control_button_state(self, state):
        if state is SystemState.STARTED:
            self.control_button_play.hide()
            self.control_button_pause.show()
        if state is SystemState.PAUSED:
            self.control_button_pause.hide()
            self.control_button_play.show()

    def __init_control_button(self):
        self.timer_system.start(SystemState.STOPPED)

        self.control_button_play.clicked.connect(
            lambda: (self.timer_system.start_timer(), self.toggle_control_button_state(SystemState.STARTED)))
        self.control_button_pause.clicked.connect(
            lambda: (self.timer_system.pause_timer(), self.toggle_control_button_state(SystemState.PAUSED)))

    @QtCore.pyqtSlot(str)
    def on_timer_update(self, timer_value):
        self.timer_label.setText(self.tr(str(timer_value)))

    def on_start_action(self):
        self.timer_system.start(SystemState.STARTED)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()
        event.accept()


if __name__ == '__main__':

    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.

    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    # Create a Qt widget, which will be our window.
    window = MainWindow()
    window.setWindowFlags(
        window.windowFlags() |
        QtCore.Qt.WindowType.FramelessWindowHint |
        QtCore.Qt.WindowType.WindowStaysOnTopHint
    )

    window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

    window.show()

    # Start the event loop.
    app.exec()
