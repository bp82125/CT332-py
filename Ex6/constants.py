from __future__ import annotations
from enum import Enum


class GlassState(Enum):
    DOWN = "DOWN"
    UP = "UP"

    def flip(self) -> GlassState:
        return GlassState.DOWN if self == GlassState.UP else GlassState.UP


MAX_GLASSES = 6
MOVING_GLASSES = 3
GOAL_GLASS_STATE = GlassState.UP
DEFAULT_STATE = [GlassState.DOWN if i % 2 == 0 else GlassState.UP for i in range(MAX_GLASSES)]
