from Ex5 import constants
from Ex5.stack import Stack
from Ex5.state import State, Action, StateMonad


def DFS(initial_state: State) -> StateMonad:
    def dfsRecursive(openDFS: Stack, closeDFS: Stack) -> StateMonad:
        if openDFS.isEmpty():
            return StateMonad(
                state=State(constants.MAX_PRIESTS, constants.MAX_DEMONS, constants.START_POSITION),
                log=["Impossible to solve!"]
            )

        node: StateMonad = openDFS.peek()
        newOpenStack = openDFS.pop()
        newCloseStack = closeDFS.push(node)

        if node.state.goalCheck():
            return node

        newStates = [
            node.bind(lambda state: state.apply_move(action))
            for action in Action
        ]

        def comparator(current_state: StateMonad) -> bool:
            return not newCloseStack.inStack(current_state) and not newOpenStack.inStack(current_state)

        unvisitedStates = list(filter(comparator, newStates))

        newOpenDFS = newOpenStack.pushAll(unvisitedStates)

        return dfsRecursive(newOpenDFS, newCloseStack)

    initial_state_monad = StateMonad(initial_state)
    initialOpenStack = Stack().push(initial_state_monad)
    initialCloseStack = Stack()

    result = dfsRecursive(initialOpenStack, initialCloseStack)
    return result
