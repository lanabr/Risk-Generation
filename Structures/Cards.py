class CardTerritory:
    def __init__(self, territory, design):
        self.territory = territory
        self.design = design


class TerritoryCards:
    def __init__(self, map):
        self.deck = []

        for terr in range(0, len(map.territories), 3):
            self.deck.append(CardTerritory(map.territories[terr], "infantry"))
            if map.territories[terr+1]:
                self.deck.append(CardTerritory(map.territories[terr+1], "cavalry"))
            if map.territories[terr+2]:
                self.deck.append(CardTerritory(map.territories[terr+2], "artillery"))
