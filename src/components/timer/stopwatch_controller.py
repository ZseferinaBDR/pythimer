import time

from threading import Thread
from PyQt6 import QtCore

from enums.system_status import SystemState


class Stopwatch(QtCore.QObject):
    """
    Stopwatch Controller is used as a timing systems backend
    for the time keeping system of the GUI. This class will have 
    PyQt signals for emitting start, paused, stop events and
    communicating the current time value to the GUI.
    """

    # Default state of the application at startup
    _system_state = SystemState.STOPPED

    # Action events
    started = QtCore.pyqtSignal(str)
    stopped = QtCore.pyqtSignal(str)
    paused = QtCore.pyqtSignal(str)

    # Continuous current time elapsed event
    timer = QtCore.pyqtSignal(str)

    def start(self, flag: SystemState = SystemState.STOPPED, time_increment: int = 1) -> None:
        Thread(target=self.__run, args=(
            flag, time_increment,), daemon=True).start()

    def __run(self, flag, time_increment) -> None:
        self.system_state = flag
        self.start_time = time.time()
        self.current_time = 0

        while True:
            match self.system_state:
                case  SystemState.STARTED:
                    self.__increment_time(time_increment)
                    formatted_time = self.__get_time_hh_mm_ss(
                        self.current_time)

                    # Communicate timer value to listener
                    self.timer.emit(str(formatted_time))

                case  SystemState.STOPPED:
                    self.reset_timer()

                case SystemState.PAUSED:
                    pass

            time.sleep(1)

    def __get_time_hh_mm_ss(self, seconds: float) -> str:
        """
        Formatting method, takes input in seconds and will 
        format the seconds input into the HH:MM:SS format.
        """
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def __increment_time(self, time_increment: int) -> int:
        """
        Increments the current time by a given amount
        this amount should be specified in seconds.
        """
        self.current_time = self.current_time + time_increment
        return self.current_time

    def start_timer(self) -> None:
        self.system_state = SystemState.STARTED

    def stop_timer(self) -> None:
        self.system_state = SystemState.STOPPED

    def pause_timer(self) -> None:
        self.system_state = SystemState.PAUSED

    def reset_timer(self) -> None:
        self.current_time = 0
        self.system_state = SystemState.STOPPED

    @property
    def system_state(self) -> SystemState:
        return self._system_state

    @system_state.setter
    def system_state(self, state) -> None:
        self._system_state = state

    @property
    def current_time(self) -> int:
        return self._current_time

    @current_time.setter
    def current_time(self, time_in_secs) -> None:
        self._current_time = time_in_secs
