from __future__ import annotations

import copy
from enum import Enum
from typing import Callable

from constants import ROWS, COLS, EIGHT_PUZZLE_GOAL, EMPTY_ROW, EMPTY_COL


class Action(Enum):
    UP = "Up", (-1, 0)
    DOWN = "Down", (1, 0)
    LEFT = "Left", (0, -1)
    RIGHT = "Right", (0, 1)


class State:
    def __init__(self, eightPuzzle: list[list[int]], emptyRow: int, emptyCol: int):
        self.eightPuzzle = eightPuzzle
        self.emptyRow = emptyRow
        self.emptyCol = emptyCol

    def __str__(self) -> str:
        puzzle_str = ""
        for row in self.eightPuzzle:
            puzzle_str += "|" + " |".join(str(tile) for tile in row) + "|\n"
        return puzzle_str.strip()

    def __eq__(self, other: State) -> bool:
        if self.emptyCol != other.emptyCol or self.emptyRow != other.emptyRow:
            return False

        for i in range(ROWS):
            for j in range(COLS):
                if self.eightPuzzle[i][j] != other.eightPuzzle[i][j]:
                    return False

        return True

    def __hash__(self):
        puzzle_hash = tuple(tuple(row) for row in self.eightPuzzle)
        empty_pos = (self.emptyRow, self.emptyCol)
        return hash((puzzle_hash, empty_pos))

    def move(self, distance: (int, int)) -> State:
        newEmptyRow = self.emptyRow + distance[0]
        newEmptyCol = self.emptyCol + distance[1]
        if newEmptyRow in range(ROWS) and newEmptyCol in range(COLS):
            newEightPuzzle = copy.deepcopy(self.eightPuzzle)

            newEightPuzzle[self.emptyRow][self.emptyCol] = newEightPuzzle[newEmptyRow][newEmptyCol]
            newEightPuzzle[newEmptyRow][newEmptyCol] = 0

            return State(
                eightPuzzle=newEightPuzzle,
                emptyRow=newEmptyRow,
                emptyCol=newEmptyCol
            )

    def apply_move(self, action: Action) -> StateMonad:
        newState = self.move(action.value[1])
        if newState is not None:
            return StateMonad(
                state=newState,
                log=[action.value[0]]
            )
        return StateMonad(
            state=self,
            log=["Error when calling operator: " + action.value[0]]
        )

    def calculate_distance(self) -> int:
        total_distance = 0
        for i in range(ROWS):
            for j in range(COLS):
                num = self.eightPuzzle[i][j]
                if num != 0:
                    goal_position = self.find_position(EIGHT_PUZZLE_GOAL, num)
                    total_distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
        return total_distance

    @staticmethod
    def find_position(matrix, num) -> (int, int):
        for i in range(3):
            for j in range(3):
                if matrix[i][j] == num:
                    return i, j

    def goal_check(self) -> bool:
        return self == GOAL


GOAL = State(
    eightPuzzle=EIGHT_PUZZLE_GOAL,
    emptyRow=EMPTY_ROW,
    emptyCol=EMPTY_COL
)


class StateMonad:
    def __init__(self, state: State, log: list = None):
        self.state = state
        self.log = log if log is not None else ["First state" + "\n" + str(self.state)]
        self.h_score = state.calculate_distance()
        self.g_score = 0

    def __eq__(self, other: StateMonad) -> bool:
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def bind(self, func: Callable[[State], StateMonad]) -> StateMonad:
        if self is not None:
            newState = func(self.unwrap())
            if newState is not None:
                return StateMonad(
                    state=newState.unwrap(),
                    log=self.log + [newState.log[0] + "\n" + str(newState.unwrap())]
                )
        return self

    def unwrap(self) -> State:
        return self.state
