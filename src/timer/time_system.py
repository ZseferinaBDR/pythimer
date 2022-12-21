from threading import Thread
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSignal, QThread
from datetime import timedelta


import enum
import time
import sys

from enums.system_status import SystemState


class TimeSystem(QtCore.QObject):
    started = QtCore.pyqtSignal(str)
    stopped = QtCore.pyqtSignal(str)
    paused = QtCore.pyqtSignal(str)

    timer = QtCore.pyqtSignal(str)

    def start(self, flag):
        Thread(target=self._run, args=(flag,), daemon=True).start()

    def _run(self, flag):
        self.system_status = flag
        self.start_time = time.time()
        self.current_time = 0

        while True:
            if self.system_status is SystemState.STARTED:
                self.current_time = self.current_time + 1
                formatted_time = self.get_time_hh_mm_ss(self.current_time)
                self.timer.emit(str(formatted_time))

            time.sleep(1)

    def get_time_hh_mm_ss(self, sec: float):
        return time.strftime('%H:%M:%S', time.gmtime(sec))

    def start_timer(self) -> None:
        self.system_status = SystemState.STARTED

    def stop_timer(self) -> None:
        self.system_status = SystemState.STOPPED

    def pause_timer(self) -> None:
        self.system_status = SystemState.PAUSED

    def reset_timer(self) -> None:
        self._current_time = 0
        self.system_status = SystemState.STOPPED

    @property
    def current_time(self) -> int:
        return self._current_time

    @current_time.setter
    def current_time(self, value):
        self._current_time = value
