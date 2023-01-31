class ContinentHandler():
    def __init__(self, mapContinents, mapTerritories, continentsValue):
        self.continents = mapContinents
        self.territories = mapTerritories
        self.continentsValue = continentsValue

    def checkContinentsForPlayer(self, playerID):
        results = []
        for continentID in self.continents.keys():
            continentTerritories = [self.territories[i]  # type: ignore
                                    for i in self.continents[continentID]]
            # Reason for typeignore: https://stackoverflow.com/questions/67991240/iterating-over-typeddicts-keys

            continentDominated = True
            for territory in continentTerritories:
                if territory.ownedByPlayer != playerID:
                    continentDominated = False
                    break
            if continentDominated:
                results.append(continentID)

        return results

    def continentValueByContinent(self, continent):
        if isinstance(continent, int):
            continent = str(continent)
        return self.continentsValue[continent]
