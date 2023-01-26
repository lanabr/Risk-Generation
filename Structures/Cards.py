import random
import itertools


class CardObj:
    def __init__(self, numberOfContinents):
        self.continent = None
        self.territories = None
        self.troops = None

        self.totalContinents = []
        for i in range(numberOfContinents):
            self.totalContinents.append(0)
        self.territoriesPercentage = 0
        self.troopsInTerritories = 0


'''
conquistar
    continente
    quantidade de paises
    continente com tropas
    quantidade de paises com tropas
'''


class ObjectiveCards:
    def __init__(self, map):
        self.deck = []

        for i in range(10):
            self.deck.append(CardObj(len(map.continents)))

        self.defineObjectives(map)

    def defineObjectives(self, map):
        continentCards = 0
        territoriesCards = 0

        for i in range(0, 10):
            temp = random.choice([0, 1])
            choices1 = [False, False]
            choices1[temp] = True
            choices2 = random.choice([True, False])

            self.deck[i].continent = choices1[0]
            self.deck[i].territories = choices1[1]
            self.deck[i].troops = choices2

            if self.deck[i].continent is True:
                continentCards += 1
            if self.deck[i].territories is True:
                territoriesCards += 1

        contTuples = random.sample(list(itertools.combinations(range(len(map.continents)), 2)), continentCards)
        terrPercentage = [round(random.uniform(0.6, 0.91), 2) for i in range(territoriesCards)]
        troopsQuantity = random.randrange(1, 4)

        a, b = 0, 0

        for k in range(0, len(self.deck)):
            if self.deck[k].continent is True:
                self.deck[k].totalContinents[contTuples[a][0]] = 1
                self.deck[k].totalContinents[contTuples[a][1]] = 1
                a += 1

            if self.deck[k].territories is True:
                self.deck[k].territoriesPercentage = terrPercentage[b]
                b += 1

            if self.deck[k].troops is True:
                self.deck[k].troopsInTerritories = troopsQuantity


class CardTerritory:
    def __init__(self, territory, design):
        self.territory = territory
        self.design = design


class TerritoryCards:
    def __init__(self, map):
        self.deck = []

        for terr in range(len(map.territories), 3):
            self.deck.append(CardTerritory(map.territories[terr].territoryId, "infantry"))
            if map.territories[terr+1]:
                self.deck.append(CardTerritory(map.territories[terr+1].territoryId, "cavalry"))
            if map.territories[terr+2]:
                self.deck.append(CardTerritory(map.territories[terr+2].territoryId, "artillery"))


if __name__ == "__main__":
    cards = ObjectiveCards(map)
