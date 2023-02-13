import random
import shutil
import matplotlib.pyplot as plt

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
        self.allFitness = []

    def gameGenerator(self):
        print("------------ Generating games with " + str(self.numGenerations) + " generations, " + str(
            self.numOffspring) + " offspring per generation and " + str(
            self.tournamentSize) + " tournament size ------------")
        print("Creating initial population")
        self.createPopulation()

        for i in range(self.numGenerations):
            print("\nGeneration " + str(i) + " of " + str(self.numGenerations) + " generations")
            newPopulation = [self.population[0]]   # elitism

            while len(newPopulation) < self.numOffspring:
                parents = self.selection()

                offspring, mapParts = self.crossover(parents)
                offspring = self.checkMap(offspring)
                offspring = self.mutation(offspring, mapParts)
                offspring = self.checkMap(offspring)

                for child in offspring:
                    self.playtest(child)

                self.calculateFitness(i)
                newPopulation.extend(offspring)

            self.updatePopulation(newPopulation)

        print("Saving final population")
        self.showResults("results_risk_generation_" + str(self.numGenerations) + "generations_" + str(
            self.numOffspring) + "offspring_" + str(self.tournamentSize) + "tournamentsize.txt")

        print("Moving files")
        self.moveFiles()

        print("------------ Finished ------------")

    def createPopulation(self):
        for _ in range(self.numOffspring):
            mapPath = "/home/lana/PycharmProjects/Risk-Generation/parameters/map" + str(random.randint(1, 10)) + ".json"
            troopsWonBeginTurn = random.randint(1, 5)
            advantageAttack = random.choice(["attack", "defense"])
            initialTerritoriesMode = random.choice(["pick", "random"])
            troopsToNewTerritory = random.choice(["min", "max"])

            self.population.append(Parameters(mapPath, troopsWonBeginTurn, advantageAttack, initialTerritoriesMode, troopsToNewTerritory))

        for gameParam in self.population:
            playtestNtimes(gameParameters=gameParam, numberOfTimes=100)
            gameParam.criteria = op.calculateCriteria(gameParam)
            os.remove("metrics/game" + str(gameParam.troopsWonBeginTurn) + "-" + gameParam.advantageAttack + "-"
                      + gameParam.initialTerritoriesMode + "-" + gameParam.troopsToNewTerritory + ".txt")

        self.calculateFitness(0)

    def calculateFitness(self, geracao):
        if len(self.allFitness) < geracao + 1:
            self.allFitness.append([])

        for gameParam in self.population:
            if gameParam.fitness == 0:
                gameParam.fitness = op.calculateFitness(gameParam)
                self.allFitness[geracao].append(gameParam.fitness)

        self.population.sort(key=lambda x: x.fitness)

    def selection(self):
        parents = op.selectionTournament(self.population, self.tournamentSize)

        return parents

    def crossover(self, parents):
        offspring, mapParts = op.crossover(parents)

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
        self.population = offspring

    def showResults(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)

        strToWrite = "Final population:\n"

        for gameParam, i in zip(self.population, range(len(self.population))):
            strToWrite += "Child " + str(i) + "\n"
            strToWrite += "Map in " + gameParam.mapPath + " with the following parameters:\n"
            strToWrite += "troopsWonBeginTurn: " + str(gameParam.troopsWonBeginTurn) + "\n"
            strToWrite += "advantageAttack: " + str(gameParam.advantageAttack) + "\n"
            strToWrite += "initialTerritoriesMode: " + str(gameParam.initialTerritoriesMode) + "\n"
            strToWrite += "troopsToNewTerritory: " + str(gameParam.troopsToNewTerritory) + "\n"
            strToWrite += "Fitness: " + str(gameParam.fitness) + "\n"
            strToWrite += "_________________________________________________________________________________________" + "\n"

        with open(fileName, "w") as file:
            file.write(strToWrite)

        self.plotFitness()

    def moveFiles(self):
        maps = os.listdir("/home/lana/PycharmProjects/Risk-Generation/parameters")
        os.mkdir("/home/lana/PycharmProjects/Risk-Generation/parameters/results_risk_generation_" + str(self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(self.tournamentSize) + "tournamentsize")

        for map in maps:
            if map.startswith("map") and map.endswith(".json") and map not in ["map1.json", "map2.json", "map3.json",
                                                                               "map4.json", "map5.json", "map6.json",
                                                                               "map7.json", "map8.json", "map9.json",
                                                                               "map10.json"]:
                shutil.move("/home/lana/PycharmProjects/Risk-Generation/parameters/" + map,
                            "/home/lana/PycharmProjects/Risk-Generation/parameters/results_risk_generation_" + str(
                                self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
                                self.tournamentSize) + "tournamentsize")

        shutil.move("/home/lana/PycharmProjects/Risk-Generation/results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize.txt", "/home/lana/PycharmProjects/Risk-Generation/parameters/results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize/")

        shutil.move("/home/lana/PycharmProjects/Risk-Generation/fitness_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize.png", "/home/lana/PycharmProjects/Risk-Generation/parameters/results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize/")

        # remove metrics files
        metrics = os.listdir("/home/lana/PycharmProjects/Risk-Generation/metrics")
        for metric in metrics:
            if metric.startswith("game"):
                os.remove("/home/lana/PycharmProjects/Risk-Generation/metrics/" + metric)

    def plotFitness(self):
        # plot all fitness along generations, with min, max and average

        maxFitness = []
        minFitness = []
        avgFitness = []
        y = range(len(self.allFitness))

        for gen in self.allFitness:
            maxFitness.append(max(gen))
            minFitness.append(min(gen))
            avgFitness.append(sum(gen) / len(gen))

        plt.plot(maxFitness, y, label="Max")
        plt.plot(minFitness, y, label="Min")
        plt.plot(avgFitness, y, label="Avg")
        plt.xlabel("Child")
        plt.ylabel("Fitness")
        plt.title("Fitness along generations")
        plt.savefig("fitness_" + str(self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize.png")
        plt.show()


if __name__ == "__main__":

    for gen in range(10, 100, 10):
        for off in range(5, 20, 5):
            for tour in range(2, off, 2):
                s = Synthesis(numGenerations=gen, numOffspring=off, tournamentSize=tour)
                s.gameGenerator()
