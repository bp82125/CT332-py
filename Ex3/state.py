from __future__ import annotations

from Ex3 import constants


class State:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'   X:{self.x}  Y:{self.y}'

    def __eq__(self, other: State) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def pourWaterFullX(self) -> StateMonad:
        if self.x < constants.TANK_CAPACITY_X:
            return StateMonad(
                state=State(constants.TANK_CAPACITY_X, self.y),
                log=["Pour water until X is full"]
            )

    def pourWaterFullY(self):
        if self.y < constants.TANK_CAPACITY_Y:
            return StateMonad(
                state=State(self.x, constants.TANK_CAPACITY_Y),
                log=["Pour water until Y is full"]
            )

    def pourWaterEmptyX(self):
        if self.x > 0:
            return StateMonad(
                state=State(constants.EMPTY, self.y),
                log=["Empty X"]
            )

    def pourWaterEmptyY(self):
        if self.y > 0:
            return StateMonad(
                state=State(self.x, constants.EMPTY),
                log=["Empty Y"]
            )

    def pourWaterXY(self):
        if self.x > 0 and self.y < constants.TANK_CAPACITY_Y:
            return StateMonad(
                state=State(
                    max(self.x - (constants.TANK_CAPACITY_Y - self.y), constants.EMPTY),
                    min(self.x + self.y, constants.TANK_CAPACITY_Y)
                ),
                log=["Pour water from X until full Y"]
            )

    def pourWaterYX(self):
        if self.y > 0 and self.x < constants.TANK_CAPACITY_X:
            return StateMonad(
                state=State(
                    min(self.x + self.y, constants.TANK_CAPACITY_X),
                    max(self.y - (constants.TANK_CAPACITY_X - self.x), constants.EMPTY)
                ),
                log=["Pour water from Y until full X"]
            )

    def goalCheck(self):
        return self.x == constants.GOAL or self.y == constants.GOAL


class StateMonad:
    state: State
    log: list

    def __init__(self, state: State, log: list = None) -> None:
        self.state = state
        self.log = log if log is not None else ["First state" + "\n" + str(state)]

    def __eq__(self, other: StateMonad) -> bool:
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def unWrap(self) -> State:
        return self.state

    def getLog(self) -> list:
        return self.log

    def bind(self, func) -> StateMonad:
        newStateMonad = func(self.unWrap())
        if newStateMonad is not None:
            return StateMonad(
                state=newStateMonad.state,
                log=self.getLog() + [newStateMonad.log[0] + "\n" + str(newStateMonad.state)]
            )
        else:
            return self
