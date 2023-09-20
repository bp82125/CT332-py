from __future__ import annotations

from typing import Callable

from Ex6.constants import GlassState, MAX_GLASSES, MOVING_GLASSES, GOAL_GLASS_STATE


class State:
    def __init__(self, glasses: list = None):
        if glasses is None:
            self.glasses = [GlassState.UP if i % 2 == 0 else GlassState.DOWN for i in range(MAX_GLASSES)]
        else:
            self.glasses = glasses

    def __str__(self):
        glass_strings = [glass.color for glass in self.glasses]
        glasses_str = "".join([f"{s:<6}" for s in glass_strings])
        index_str = "{}".format("     ".join(str(i + 1) for i in range(MAX_GLASSES))) + "\n"
        return glasses_str + "\n" + index_str

    def __eq__(self, other: State) -> bool:
        for i in range(MAX_GLASSES):
            if self.glasses[i] != other.glasses[i]:
                return False
        return True

    def goalCheck(self) -> bool:
        for state in self.glasses:
            if state != GOAL_GLASS_STATE:
                return False
        return True

    def move(self, flip_indices: range) -> 'State':
        new_glasses = list(
            map(
                lambda index, glass: glass.flip() if index in flip_indices else glass,
                range(MAX_GLASSES),
                self.glasses
            )
        )

        return State(new_glasses)

    def apply_move(self, startIndex: int) -> StateMonad:
        if startIndex < 0 or startIndex >= MAX_GLASSES - MOVING_GLASSES + 2:
            raise ValueError("Invalid startIndex")

        flip_indices = range(startIndex - 1, startIndex + MOVING_GLASSES - 1)
        return StateMonad(
            state=self.move(flip_indices),
            log=[f'Flip {MOVING_GLASSES} cups, start from {startIndex}: ' + " ".join(str(i + 1) for i in flip_indices)]
        )


class StateMonad:
    def __init__(self, state: State, log: list = None):
        self.state = state
        self.log = log if log is not None else ["First state: " + "\n" + str(state)]

    def __eq__(self, other: StateMonad) -> bool:
        return self.state == other.state

    def bind(self, func: Callable[[State], StateMonad]):
        new_state_monad = func(self.state)
        if new_state_monad.state is not self.state:
            return StateMonad(
                state=new_state_monad.state,
                log=self.log + [new_state_monad.log[0] + "\n" + str(new_state_monad.state)]
            )
        else:
            return self

    def unWrap(self) -> State:
        return self.state

    def getLog(self) -> list:
        return self.log
