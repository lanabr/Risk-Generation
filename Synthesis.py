import GeneticOperations as op
from Parameters import Parameters
from AutomatedPlaytest import playtestNtimes


class Synthesis:
    def __init__(self):
        self.population = []
        self.numGenerations = 1
        self.numOffspring = 3
        self.tournamentSize = 5

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

        self.showResults()

    def createPopulation(self):
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 2, "attack", "random", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 3, "defense", "random", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 1, "attack", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 4, "defense", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 5, "attack", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 1, "defense", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 2, "attack", "random", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 3, "defense", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 5, "attack", "random", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 4, "attack", "pick", "min"))

        for gameParam in self.population:
            #playtestNtimes(gameParameters=gameParam, numberOfTimes=100)
            gameParam.criteria = op.calculateCriteria(gameParam)

    def calculateFitness(self):
        for gameParam in self.population:
            if gameParam.fitness == 0:
                gameParam.fitness = op.calculateFitness(gameParam)

        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def selection(self):
        parents = op.selectionTournament(self.population, self.tournamentSize)

        return parents

    def crossover(self, parents):
        offspring = op.crossover(parents, self.numOffspring)

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

    def showResults(self):
        print("Final population:")
        for gameParam, i in zip(self.population, range(len(self.population))):
            print("Child", i)
            print("Map in", gameParam.mapPath, "with the following parameters:")
            print("troopsWonBeginTurn: ", gameParam.troopsWonBeginTurn)
            print("advantageAttack: ", gameParam.advantageAttack)
            print("initialTerritoriesMode: ", gameParam.initialTerritoriesMode)
            print("troopsToNewTerritory: ", gameParam.troopsToNewTerritory)
            print("Fitness: ", gameParam.fitness)
            print("_________________________________________________________________________________________")


if __name__ == "__main__":
    s = Synthesis()
    s.gameGenerator()
