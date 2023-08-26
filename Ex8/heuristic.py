from __future__ import annotations

from heapdict import heapdict

from state import State, StateMonad, Action


def a_star(initial_state: State) -> StateMonad:
    open_queue = heapdict()
    close_set = heapdict()

    initial_state_monad = StateMonad(initial_state)
    initial_state_monad.g_score = 0
    open_queue[initial_state_monad] = initial_state_monad.h_score + initial_state_monad.g_score

    while open_queue:
        current_state_monad, _ = open_queue.popitem()
        close_set[current_state_monad] = current_state_monad.g_score

        if current_state_monad.unwrap().goal_check():
            return current_state_monad

        for action in Action:

            next_state_monad = current_state_monad.bind(lambda state: state.apply_move(action))
            next_state_monad.g_score = current_state_monad.g_score + 1

            if next_state_monad in open_queue and next_state_monad.g_score >= open_queue[next_state_monad] - next_state_monad.h_score:
                continue

            if next_state_monad in close_set and next_state_monad.g_score >= close_set[next_state_monad]:
                continue

            if next_state_monad in close_set and next_state_monad.g_score < close_set[next_state_monad]:
                close_set.pop(next_state_monad)

            open_queue[next_state_monad] = next_state_monad.h_score + next_state_monad.g_score



