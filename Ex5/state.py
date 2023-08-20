from __future__ import annotations

from enum import Enum

from Ex5 import constants


class Action(Enum):
    ONE_PRIEST = "Move one priest"
    TWO_PRIESTS = "Move two priest"
    ONE_DEMON = "Move one demon"
    TWO_DEMONS = "Move two demons"
    ONE_PRIEST_ONE_DEMON = "Move one priest and one demon"


class State:
    def __init__(self, priest: int, demon: int, boat_position: str):
        self.priest = priest
        self.demon = demon
        self.boat_position = boat_position

    def __eq__(self, other: State) -> bool:
        return self.priest == other.priest and self.demon == other.demon and self.boat_position == other.boat_position

    def __str__(self):
        def str_boat_postion(boat: str) -> str:
            if boat == "A":
                return "|-B---------------------|"
            else:
                return "|---------------------B-|"

        return f'{self.priest}, {self.demon} {str_boat_postion(self.boat_position)} {constants.MAX_PRIESTS - self.priest}, {constants.MAX_DEMONS - self.demon}'

    def goalCheck(self) -> bool:
        return self == State(0, 0, constants.END_POSITION)

    def otherside(self) -> State:
        return State(
            priest=constants.MAX_PRIESTS - self.priest,
            demon=constants.MAX_DEMONS - self.demon,
            boat_position="B" if self.boat_position == "A" else "A"
        )

    def legal_state(self) -> bool:
        def alive(state: State) -> bool:
            if state.priest < 0 or state.priest > constants.MAX_PRIESTS:
                return False
            if state.demon < 0 or state.demon > constants.MAX_DEMONS:
                return False
            if state.demon > state.priest > 0:
                return False
            return True

        return alive(self) and alive(self.otherside())

    def move(self, amount: tuple[int, int]) -> State:

        if not self.legal_state():
            return self

        def amount_position(boat_position: str) -> int:
            return -1 if (boat_position == "A") else 1

        temp = State(
            priest=self.priest + amount[0] * amount_position(self.boat_position),
            demon=self.demon + amount[1] * amount_position(self.boat_position),
            boat_position=self.otherside().boat_position
        )
        if temp.legal_state():
            return temp
        else:
            return self

    def apply_move(self, action: Action) -> StateMonad:
        if action == Action.ONE_PRIEST:
            return StateMonad(self.move((1, 0)), [Action.ONE_PRIEST.value])
        elif action == Action.TWO_PRIESTS:
            return StateMonad(self.move((2, 0)), [Action.TWO_PRIESTS.value])
        elif action == Action.ONE_DEMON:
            return StateMonad(self.move((0, 1)), [Action.ONE_DEMON.value])
        elif action == Action.TWO_DEMONS:
            return StateMonad(self.move((0, 2)), [Action.TWO_DEMONS.value])
        elif action == Action.ONE_PRIEST_ONE_DEMON:
            return StateMonad(self.move((1, 1)), [Action.ONE_PRIEST_ONE_DEMON.value])
        else:
            return StateMonad(self)


class StateMonad:
    def __init__(self, state: State, log: list = None):
        self.state = state
        self.log = log if log is not None else ["First state:\n" + str(state)]

    def __eq__(self, other: StateMonad) -> bool:
        return self.state == other.state

    def bind(self, func) -> StateMonad:
        def get_route(state: State):
            return " from B to A:\n" if state.boat_position == "A" else " from A to B:\n"

        new_state_monad = func(self.state)
        if new_state_monad != self:
            return StateMonad(
                state=new_state_monad.state,
                log=self.log + [new_state_monad.log[0] + get_route(new_state_monad.state) + str(new_state_monad.state)]
            )
        else:
            return self
