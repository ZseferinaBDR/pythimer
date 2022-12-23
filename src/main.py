import enum
import time
import sys
import os
from typing import Tuple

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox
from PyQt6.QtGui import QFont, QIcon, QCursor
from PyQt6.QtCore import QSize, Qt
from components.timer.stopwatch_component import TimerWidget
from components.timer.stopwatch_controller import Stopwatch
from utils.pathutil import get_relative_path

# TODO: make this into a configuration class, should also be loaded from a file.
WINDOW_NAME: str = "Pythimer"
WINDOW_SIZE_H: int = 140
WINDOW_SIZE_W: int = 400
DEFAULT_POS: Tuple[int, int] = (200, 200)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.build_window()

        # Timer widget we are loading in the main window
        _ = TimerWidget(self.visible_child)

    def build_window(self):
        self.__init_base_window()
        self.__register_base_images()
        self.__init_translucent_layout()
        self.__load_styles()

        self.__build_window_exit_button()
        self.__register_window_actions()

    def __init_base_window(self):
        """
        Create the window with a name and geometry of the window.
        """
        self.setWindowTitle(WINDOW_NAME)

        self.setGeometry(DEFAULT_POS[0], DEFAULT_POS[1],
                         WINDOW_SIZE_W, WINDOW_SIZE_H)
        self.setFixedSize(WINDOW_SIZE_W, WINDOW_SIZE_H)

    def __init_translucent_layout(self):
        self.visible_child = QtWidgets.QWidget(self)
        self.visible_child.setObjectName('vc')

        # TODO: search for a better way to implement hardcoded values.
        self.visible_child.setFixedSize(300, 100)

    def __build_window_exit_button(self):
        self.exit_button = QPushButton(self.visible_child)
        self.exit_button.setObjectName('exitbtn')
        self.exit_button.setGeometry(275, 5, 15, 15)
        self.exit_button.setIcon(QIcon(self.exit_icon))
        self.exit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def __register_base_images(self):
        self.exit_icon = get_relative_path('src/icons/controls/x.svg')

    def __register_window_actions(self):
        self.exit_button.clicked.connect(lambda: self.exit_application())

    def __load_styles(self):
        """
        Dynamically load the base QSS class for the the
        whole widget, main layout and its sub components.
        """
        path = get_relative_path('src/base.qss')
        with open(path, "r") as f:
            _style = f.read()
            self.setStyleSheet(_style)

    def mousePressEvent(self, event):
        """
        Mouse Press Event handler implemented for capturing
        current window pos_x and window pos_y into a point when clicking.
        """
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """
        Mouse event handler implemented for making a frameless
        window draggable on the screen based on the captured coordinates
        from the mousePressEvent method.
        """
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()
        event.accept()

    def exit_application(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowFlags(
        window.windowFlags() |
        QtCore.Qt.WindowType.FramelessWindowHint |
        QtCore.Qt.WindowType.WindowStaysOnTopHint
    )

    window.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
    window.show()

    app.exec()
