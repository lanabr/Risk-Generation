class Parameters:
    """
    This class contains all parameters that can be modified through each iteration of our search.
    """

    def __init__(self, mapPath, goalBasedOn, troopsWonBeginTurn, advantageAttack, initialTerritoriesMode):
        self.mapPath = mapPath
        self.goalBasedOn = goalBasedOn                         # cards, all           #vai usar cartas de objetivo ou conquistar o mapa inteiro
        self.troopsWonBeginTurn = troopsWonBeginTurn           # 1, 2, 3, 4, 5        #divisor do total de tropas ganhas no inicio do turno
        self.advantageAttack = advantageAttack                 # attack, defense      #ataque = defesa usa 2 dados, defesa = defesa usa 3 dados
        self.initialTerritoriesMode = initialTerritoriesMode   # random, pick         #escolha inicial dos territorios é aleatoria ou escolhida pelos jogadores
