import GeneticOperations as op
from Parameters import Parameters
from AutomatedPlaytest import playtestNtimes


class Synthesis:
    def __init__(self):
        self.population = []
        self.numGenerations = 10

    def gameGenerator(self):
        self.createPopulation()

        for i in range(self.numGenerations):
            self.calculateFitness()
            parents = self.selection()
            offspring = self.crossover(parents)
            offspring = self.mutation(offspring)

            for child in offspring:
                self.playtest(child)
                self.calculateCriteria(child)

            self.updatePopulation(offspring)

    def createPopulation(self):
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map1.json", "all", 2, "attack", "random", "min"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map2.json", "cards", 3, "defense", "random", "min"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map3.json", "all", 1, "attack", "pick", "max"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map4.json", "cards", 4, "defense", "pick", "max"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map5.json", "cards", 5, "attack", "pick", "min"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map1.json", "cards", 1, "defense", "pick", "max"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map2.json", "all", 2, "attack", "random", "min"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map3.json", "cards", 3, "defense", "random", "max"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map4.json", "all", 5, "attack", "pick", "min"))
        self.population.append(Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map5.json", "cards", 5, "attack", "pick", "max"))

        for gameParam in self.population:
            playtestNtimes(gameParameters=gameParam, numberOfTimes=100)
            gameParam.criteria = op.calculateCriteria(gameParam)

    def calculateFitness(self):
        for gameParam in self.population:
            if gameParam.fitness == 0:
                gameParam.fitness = op.calculateFitness(gameParam)

        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def selection(self):
        parents = op.selectionTournament(self.population)

        return parents

    def crossover(self, parents):
        offspring = op.crossover(parents)

        return offspring

    def mutation(self, offspring):
        offspring = op.mutation(offspring)

        return offspring

    def playtest(self, gameParam):
        playtestNtimes(gameParameters=gameParam)

    def calculateCriteria(self, gameParam):
        gameParam.criteria = op.calculateCriteria(gameParam)

    def updatePopulation(self, offspring):
        self.population.extend(offspring)


if __name__ == "__main__":
    s = Synthesis()
    s.gameGenerator()