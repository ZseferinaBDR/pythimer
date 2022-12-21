from enum import Enum, auto


class SystemState(Enum):
    STARTED = auto()
    PAUSED = auto()
    STOPPED = auto()
