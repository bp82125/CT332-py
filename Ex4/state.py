from __future__ import annotations

from Ex4 import constants


class State:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'   X:{self.x}  Y:{self.y}  Z:{self.z}'

    def __eq__(self, other: State) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def pourWaterXY(self):
        if self.x > 0 and self.y < constants.TANK_CAPACITY_Y:
            return StateMonad(
                state=State(
                    x=max(self.x - (constants.TANK_CAPACITY_Y - self.y), constants.EMPTY),
                    y=min(self.x + self.y, constants.TANK_CAPACITY_Y),
                    z=self.z
                ),
                log=["Pour milk from X until full Y"]
            )

    def pourWaterYX(self):
        if self.y > 0 and self.x < constants.TANK_CAPACITY_X:
            return StateMonad(
                state=State(
                    x=min(self.x + self.y, constants.TANK_CAPACITY_X),
                    y=max(self.y - (constants.TANK_CAPACITY_X - self.x), constants.EMPTY),
                    z=self.z
                ),
                log=["Pour milk from Y until full X"]
            )

    def pourWaterXZ(self):
        if self.x > 0 and self.z < constants.TANK_CAPACITY_Z:
            return StateMonad(
                state=State(
                    x=max(self.x - (constants.TANK_CAPACITY_Z - self.z), constants.EMPTY),
                    y=self.y,
                    z=min(self.x + self.z, constants.TANK_CAPACITY_Z)
                ),
                log=["Pour milk from X until full Z"]
            )

    def pourWaterZX(self):
        if self.z > 0 and self.x < constants.TANK_CAPACITY_X:
            return StateMonad(
                state=State(
                    x=min(self.x + self.z, constants.TANK_CAPACITY_X),
                    y=self.y,
                    z=max(self.z - (constants.TANK_CAPACITY_X - self.x), constants.EMPTY)
                ),
                log=["Pour milk from Y until full Z"]
            )

    def pourWaterZY(self):
        if self.z > 0 and self.y < constants.TANK_CAPACITY_Y:
            return StateMonad(
                state=State(
                    x=self.x,
                    y=min(self.z + self.y, constants.TANK_CAPACITY_Y),
                    z=max(self.z - (constants.TANK_CAPACITY_Y - self.y), constants.EMPTY)
                ),
                log=["Pour milk from Z until full Y"]
            )

    def pourWaterYZ(self):
        if self.y > 0 and self.z < constants.TANK_CAPACITY_Z:
            return StateMonad(
                state=State(
                    x=self.x,
                    y=max(self.y - (constants.TANK_CAPACITY_Z - self.z), constants.EMPTY),
                    z=min(self.z + self.y, constants.TANK_CAPACITY_Z)
                ),
                log=["Pour milk from Y until full X"]
            )

    def goalCheck(self):
        return self.x == constants.GOAL or self.y == constants.GOAL or self.z == constants.GOAL


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

    def printLog(self):
        for i in range(len(self.log)):
            print(f"Action {i}: {self.log[i]}")
