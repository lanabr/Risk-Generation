import shutil

import GeneticOperations as op
from Parameters import Parameters
from AutomatedPlaytest import playtestNtimes
import os


class Synthesis:
    def __init__(self, numGenerations, numOffspring, tournamentSize):
        self.population = []
        self.numGenerations = numGenerations
        self.numOffspring = numOffspring
        self.tournamentSize = tournamentSize

    def gameGenerator(self):
        print("------------ Generating games with " + str(self.numGenerations) + " generations, " + str(
            self.numOffspring) + " offspring per generation and " + str(
            self.tournamentSize) + " tournament size ------------")
        print("Creating initial population")
        self.createPopulation()

        for i in range(self.numGenerations):
            print("\nGeneration " + str(i) + " of " + str(self.numGenerations) + " generations")
            parents = self.selection()

            offspring, mapParts = self.crossover(parents, i)
            offspring = self.mutation(offspring, mapParts)
            offspring = self.checkMap(offspring)

            for child in offspring:
                self.playtest(child)

            self.calculateFitness()
            self.updatePopulation(offspring)

        print("Saving final population")
        self.showResults("results_risk_generation_" + str(self.numGenerations) + "generations_" + str(
            self.numOffspring) + "offspring_" + str(self.tournamentSize) + "tournamentsize.txt")

        print("Moving files")
        self.moveFiles()

        print("------------ Finished ------------")

    def createPopulation(self):
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map1.json", 2, "attack", "random", "min"))
        self.population.append(Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map2.json", 3, "defense", "random","max"))
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
            os.remove("metrics/game" + str(gameParam.troopsWonBeginTurn) + "-" + gameParam.advantageAttack + "-"
                      + gameParam.initialTerritoriesMode + "-" + gameParam.troopsToNewTerritory + ".txt")

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
        self.calculateCriteria(gameParam)
        os.remove("metrics/game" + str(gameParam.troopsWonBeginTurn) + "-" + gameParam.advantageAttack + "-"
                      + gameParam.initialTerritoriesMode + "-" + gameParam.troopsToNewTerritory + ".txt")

    def calculateCriteria(self, gameParam):
        gameParam.criteria = op.calculateCriteria(gameParam)

    def updatePopulation(self, offspring):
        self.population.extend(offspring)

    def showResults(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)

        strToWrite = "Final population:\n"

        for gameParam, i in zip(self.population, range(len(self.population))):
            strToWrite += "Child " + str(i) + " generation " + str(gameParam.generation) + "\n"
            strToWrite += "Map in " + gameParam.mapPath + " with the following parameters:\n"
            strToWrite += "troopsWonBeginTurn: " + str(gameParam.troopsWonBeginTurn) + "\n"
            strToWrite += "advantageAttack: " + str(gameParam.advantageAttack) + "\n"
            strToWrite += "initialTerritoriesMode: " + str(gameParam.initialTerritoriesMode) + "\n"
            strToWrite += "troopsToNewTerritory: " + str(gameParam.troopsToNewTerritory) + "\n"
            strToWrite += "Fitness: " + str(gameParam.fitness) + "\n"
            strToWrite += "_________________________________________________________________________________________" + "\n"

        with open(fileName, "w") as file:
            file.write(strToWrite)

    def moveFiles(self):
        maps = os.listdir("/home/lana/PycharmProjects/Risk-Generation/parameters")

        for map in maps:
            if map.startswith("map") and map.endswith(".json") and map not in ["map1.json", "map2.json", "map3.json",
                                                                               "map4.json", "map5.json", "map6.json",
                                                                               "map7.json", "map8.json", "map9.json",
                                                                               "map10.json"]:
                shutil.move("/home/lana/PycharmProjects/Risk-Generation/parameters/" + map,
                            "/home/lana/PycharmProjects/Risk-Generation/parameters/")

        shutil.move("/home/lana/PycharmProjects/Risk-Generation/results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize.txt", "/home/lana/PycharmProjects/Risk-Generation/parameters/" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize/results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize")

        # remove metrics files
        metrics = os.listdir("/home/lana/PycharmProjects/Risk-Generation/metrics")
        for metric in metrics:
            if metric.startswith("game"):
                os.remove("/home/lana/PycharmProjects/Risk-Generation/metrics/" + metric)


if __name__ == "__main__":

    for gen in range(10, 100, 10):
        for off in range(3, 10, 2):
            for tour in range(2, 10, 2):
                s = Synthesis(numGenerations=gen, numOffspring=off, tournamentSize=tour)
                s.gameGenerator()
