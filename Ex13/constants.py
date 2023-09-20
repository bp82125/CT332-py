from enum import Enum, auto


class State(Enum):
    WA = "Western Australia"
    NT = "Northern Territory"
    SA = "South Australia"
    QL = "Queensland"
    NSW = "New South Wales"
    V = "Victoria"
    T = "Tasmanian"


class Color(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    NONE = "none"


