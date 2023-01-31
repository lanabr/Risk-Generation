from enum import Enum


class AddUnitsPhase(Enum):
    """
    Structure that stores which game phase the game is
    """

    CONTINENT_PHASE = 1
    TERRITORY_PHASE = 2
    PICK_PHASE = 3
