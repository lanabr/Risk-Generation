class Parameters:
    """
    This class contains all parameters that can be modified through each iteration of our search.
    """

    def __init__(self, mapPath, troopsWonBeginTurn, defenseDices, initialTerritoriesMode, troopsToNewTerritory):
        self.mapPath = mapPath
        self.troopsWonBeginTurn = int(troopsWonBeginTurn)           # 1, 2, 3, 4           divisor do total de tropas ganhas no inicio do turno
        self.defenseDices = int(defenseDices)                       # 2, 3                 quantos dados a defesa usa
        self.initialTerritoriesMode = initialTerritoriesMode   # random, pick         escolha inicial dos territorios é aleatoria ou escolhida pelos jogadores
        self.troopsToNewTerritory = troopsToNewTerritory       # min, max             tropas a serem colocadas em um novo territorio

        print(troopsWonBeginTurn, self.troopsWonBeginTurn)

        self.criteria = {}
        self.fitness = 0
        self.mapNumber = 0
