from Ex1.stack import Stack
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


def DFS(state: State) -> StateMonad:
    def dfsRecursive(openDFS: Stack, closeDFS: Stack):
        if openDFS.isEmpty():
            return None

        node = openDFS.peek()
        newOpenStack = openDFS.pop()
        newCloseStack = closeDFS.push(node)

        if node.state.goalCheck():
            return node

        newStates = [
            callOperator(node, i + 1)
            for i in range(6)
        ]

        comparator = lambda stateMonad: not newCloseStack.inStack(stateMonad) and not newOpenStack.inStack(stateMonad)
        unvisitedStates = list(filter(comparator, newStates))

        newOpenStack = newOpenStack.pushAll(unvisitedStates)

        return dfsRecursive(newOpenStack, newCloseStack)

    initialStateMonad = StateMonad(state, [])
    initialOpenStack = Stack().push(initialStateMonad)
    initialCloseSTack = Stack()

    result = dfsRecursive(initialOpenStack, initialCloseSTack)
    return result
