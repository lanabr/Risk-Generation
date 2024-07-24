class PlayerID:
    def __init__(self, playerName, playerColor):
        self.playerName = playerName
        self.playerColor = playerColor
        self.active = True

    def __eq__(self, other):
        if other is None:
            return False
        return self.playerName == other.playerName
