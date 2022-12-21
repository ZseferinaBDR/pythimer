import enum
import time
import sys

from threading import Thread
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QFont
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QThread, QRect
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
        self.__init_timer_label()
        self.__init_control_button()

        self.timer_system.timer.connect(self.on_timer_update)

    def __init_window_properties(self):
        self.setGeometry(200, 200, 400, 140)
        self.setFixedSize(400, 140)
        self.setWindowTitle("Pythimer")

        self.visible_child = QtWidgets.QWidget(self)
        self.visible_child.setStyleSheet('QWidget{background: rgba(13, 21, 28, .9); border-radius: 10px;}')
        self.visible_child.setObjectName('vc')
        self.visible_child.setFixedSize(400, 140)
        self.grid_layout = QGridLayout()

        # TODO: does nothing remove later on
        rect = QRect(200, 200, 400, 14)
        self.grid_layout.setGeometry(rect)


    def __init_timer_label(self):
        self.timer_label = QLabel(self.visible_child)
        self.timer_label.setText("00:00:00")
        self.timer_label.setFont(QFont("Sanserif", 35))
        self.timer_label.setGeometry(20, 10, 400, 50)
        self.timer_label.setStyleSheet('color:#F4F4F4')

    def __init_control_button(self):
        button_group_layout = QHBoxLayout(self.visible_child)

        start_button = QPushButton("start", self)
        pause_button = QPushButton("pause", self)
        stop_button = QPushButton("stop", self)

        button_group_layout.addWidget(start_button)
        button_group_layout.addWidget(pause_button)
        button_group_layout.addWidget(stop_button)

        self.timer_system.start(SystemState.STOPPED)

        start_button.clicked.connect(lambda: self.timer_system.start_timer())
        stop_button.clicked.connect(lambda: self.timer_system.stop_timer())
        pause_button.clicked.connect(lambda: self.timer_system.pause_timer())

        self.grid_layout.addChildLayout(button_group_layout)


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
