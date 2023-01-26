from enum import Enum


class GamePhase(Enum):
    """
    Structure that stores which game phase the game is
    """

    ALLOCATION_PHASE = 1
    CONFLICT_PHASE = 2
    GAME_OVER = 3
