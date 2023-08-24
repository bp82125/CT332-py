from __future__ import annotations

import heapq
from state import State, StateMonad, Action, GOAL


def a_star(initial_state: State) -> StateMonad:
    priority_queue = []
    heapq.heappush(priority_queue, (initial_state.calculate_heuristic(), StateMonad(initial_state)))

    cost_so_far = {initial_state: 0}
    visited_states = set()

    while priority_queue:
        _, current_state_monad = heapq.heappop(priority_queue)
        current_state = current_state_monad.unwrap()

        if current_state == GOAL:
            return current_state_monad

        visited_states.add(current_state)

        for action in Action:
            next_state_monad = current_state_monad.bind(lambda state: state.apply_move(action))
            next_state = next_state_monad.unwrap()

            new_cost = cost_so_far[current_state] + 1

            if (next_state_monad.get_heuristic(), next_state_monad) not in priority_queue and next_state not in visited_states:
                heuristic_value = next_state_monad.get_heuristic()
                heapq.heappush(priority_queue, (heuristic_value, next_state_monad))
