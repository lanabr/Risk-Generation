from enum import Enum, auto


class TurnPhase(Enum):
    """
    Structure that stores which game phase the game is
    """

    EXCHANGE_CARDS = 1
    ADD_UNITS = 2
    ATTACK_ENEMY = 3
    MOVE_UNITS = 4
