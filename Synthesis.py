import GeneticOperations as op
from Parameters import Parameters
from AutomatedPlaytest import playtestNtimes
import os


class Synthesis:
    def __init__(self):
        self.population = []
        self.numGenerations = 20
        self.numOffspring = 3
        self.tournamentSize = 5

    def gameGenerator(self):
        print("Creating initial population")
        self.createPopulation()

        for i in range(self.numGenerations):
            print("\nGeneration " + str(i) + " of " + str(self.numGenerations) + " generations")
            self.calculateFitness()
            parents = self.selection()

            offspring, mapParts = self.crossover(parents, i)
            offspring = self.mutation(offspring, mapParts)
            offspring = self.checkMap(offspring)

            for child in offspring:
                self.playtest(child)
                self.calculateCriteria(child)

            self.updatePopulation(offspring)

        print("Saving final population")
        self.showResults("results_risk_generation_" + str(self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(self.tournamentSize) + "tournamentsize.txt")

    def createPopulation(self):
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 2, "attack", "random", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map2.json", 3, "defense", "random", "max"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map3.json", 1, "attack", "pick", "max"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map4.json", 4, "defense", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map5.json", 5, "attack", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map6.json", 1, "defense", "pick", "max"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map7.json", 2, "attack", "random", "max"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map8.json", 3, "defense", "pick", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map9.json", 5, "attack", "random", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map10.json", 4, "attack", "pick", "max"))

        for gameParam in self.population:
            playtestNtimes(gameParameters=gameParam, numberOfTimes=100)
            gameParam.criteria = op.calculateCriteria(gameParam)

    def calculateFitness(self):
        for gameParam in self.population:
            if gameParam.fitness == 0:
                gameParam.fitness = op.calculateFitness(gameParam)

        self.population.sort(key=lambda x: x.fitness)

    def selection(self):
        parents = op.selectionTournament(self.population, self.tournamentSize)

        return parents

    def crossover(self, parents, generation):
        offspring, mapParts = op.crossover(parents, self.numOffspring, generation)

        return offspring, mapParts

    def mutation(self, offspring, mapParts):
        offspring = op.mutation(offspring, mapParts)

        return offspring

    def checkMap(self, offspring):
        offspring = op.checkMap(offspring)

        return offspring

    def playtest(self, gameParam):
        playtestNtimes(gameParameters=gameParam)

    def calculateCriteria(self, gameParam):
        gameParam.criteria = op.calculateCriteria(gameParam)

    def updatePopulation(self, offspring):
        self.population.extend(offspring)

    def showResults(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)

        strToWrite = "Final population:\n"

        for gameParam, i in zip(self.population, range(len(self.population))):
            strToWrite += "Child " + str(i) + "generation " + str(gameParam.generation) + "\n"
            strToWrite += "Map in " + gameParam.mapPath + " with the following parameters:\n"
            strToWrite += "troopsWonBeginTurn: " + str(gameParam.troopsWonBeginTurn) + "\n"
            strToWrite += "advantageAttack: " + str(gameParam.advantageAttack) + "\n"
            strToWrite += "initialTerritoriesMode: " + str(gameParam.initialTerritoriesMode) + "\n"
            strToWrite += "troopsToNewTerritory: " + str(gameParam.troopsToNewTerritory) + "\n"
            strToWrite += "Fitness: " + str(gameParam.fitness) + "\n"
            strToWrite += "_________________________________________________________________________________________" + "\n"

        with open(fileName, "w") as file:
            file.write(strToWrite)


if __name__ == "__main__":
    s = Synthesis()
    s.gameGenerator()
