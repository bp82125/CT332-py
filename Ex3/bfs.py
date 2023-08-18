from collections import deque
from state import State, StateMonad


def callOperator(currentState: StateMonad, option: int) -> StateMonad:
    if option == 1:
        return currentState.bind(lambda state: state.pourWaterFullX())
    elif option == 2:
        return currentState.bind(lambda state: state.pourWaterFullY())
    elif option == 3:
        return currentState.bind(lambda state: state.pourWaterEmptyX())
    elif option == 4:
        return currentState.bind(lambda state: state.pourWaterEmptyY())
    elif option == 5:
        return currentState.bind(lambda state: state.pourWaterXY())
    elif option == 6:
        return currentState.bind(lambda state: state.pourWaterYX())
    else:
        return currentState


def BFS(state: State) -> StateMonad:
    initialStateMonad = StateMonad(state, [])
    openQueue = deque([initialStateMonad])
    closeStates = set()

    while openQueue:
        currentStateMonad = openQueue.popleft()
        closeStates.add(currentStateMonad)

        if currentStateMonad.state.goalCheck():
            return currentStateMonad

        newStates = (
            callOperator(currentStateMonad, i + 1)
            for i in range(6)
        )

        comparator = lambda stateMonad: stateMonad not in closeStates and stateMonad not in openQueue
        unvisitedStates = list(filter(comparator, newStates))

        openQueue.extend(unvisitedStates)

    return StateMonad(state)
