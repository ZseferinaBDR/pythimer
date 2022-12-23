from enum import Enum, auto


class SystemState(Enum):
    """
    System State Enum defines if the stopwatch system
    is either running, paused or stopped at any given moment.
    Auto is used because we don't particularly need the values
    of the enum itself.
    """
    STARTED = auto()
    PAUSED = auto()
    STOPPED = auto()
