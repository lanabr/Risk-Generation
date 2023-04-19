import random
import shutil
import matplotlib.pyplot as plt

import GeneticOperations as op
from Parameters import Parameters
from AutomatedPlaytest import playtestNtimes
import os
import copy
import Evaluate
import math


class Synthesis:
    def __init__(self, numGenerations, numOffspring, tournamentSize, mutationRate):
        self.population = []
        self.numGenerations = numGenerations
        self.numOffspring = numOffspring
        self.tournamentSize = tournamentSize
        self.mutationRate = mutationRate
        self.allFitness = []

    def gameGenerator(self):
        print("------------ Generating games with " + str(self.numGenerations) + " generations, " + str(
            self.numOffspring) + " offspring per generation,  " + str(self.tournamentSize) +
            " tournament size and" + str(self.mutationRate) + " mutation rate --------------")
        print("Creating initial population")
        self.createPopulation()

        for i in range(self.numGenerations):
            print("\nGeneration " + str(i + 1) + " of " + str(self.numGenerations) + " generations")
            newPopulation = self.createNewPopulation(self.population[0])   # elitism

            while len(newPopulation) < self.numOffspring:
                parents = self.selection()

                offspring, mapParts = self.crossover(parents)
                offspring = self.checkMap(offspring)
                offspring = self.mutation(offspring, mapParts)
                offspring = self.checkMap(offspring)

                for child in offspring:
                    self.playtest(child)

                newPopulation.extend(offspring)

            self.updatePopulation(newPopulation, i)
            self.calculateFitness(i)

        print("Saving final population")
        self.showResults("results_risk_generation_" + str(self.numGenerations) + "generations_" + str(
            self.numOffspring) + "offspring_" + str(self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate.txt")

        print("Moving files")
        self.moveFiles()

        print("------------ Finished ------------")

        op.MAPCOUNT = 11

    def createPopulation(self):
        for _ in range(self.numOffspring):
            mapPath = "parameters/map" + str(random.randint(1, 10)) + ".json"
            troopsWonBeginTurn = random.randint(1, 4)
            defenseDices = random.choice([2, 3])
            initialTerritoriesMode = random.choice(["pick", "random"])
            troopsToNewTerritory = random.choice(["min", "max"])

            self.population.append(Parameters(mapPath, troopsWonBeginTurn, defenseDices, initialTerritoriesMode, troopsToNewTerritory))

        for gameParam in self.population:
            playtestNtimes(gameParameters=gameParam)
            gameParam.criteria = op.calculateCriteria(gameParam)
            os.remove("metrics/game" + str(gameParam.troopsWonBeginTurn) + "-" + str(gameParam.defenseDices) + "-"
                      + gameParam.initialTerritoriesMode + "-" + gameParam.troopsToNewTerritory + ".txt")

        self.calculateFitness(0)

    def calculateFitness(self, geracao):
        if len(self.allFitness) < geracao + 1:
            self.allFitness.append([])

        for gameParam in self.population:
            gameParam.fitness = op.calculateFitness(gameParam)
            self.allFitness[geracao].append(gameParam.fitness)

        self.population.sort(key=lambda x: x.fitness)

    def createNewPopulation(self, best):
        newPopulation = []
        newPopulation.append(copy.copy(best))

        self.playtest(best)

        return newPopulation

    def selection(self):
        parents = op.selectionTournament(self.population, self.tournamentSize)

        return parents

    def crossover(self, parents):
        offspring, mapParts = op.crossover(parents)

        return offspring, mapParts

    def mutation(self, offspring, mapParts):
        offspring = op.mutation(offspring, mapParts, self.mutationRate)

        return offspring

    def checkMap(self, offspring):
        offspring = op.checkMap(offspring)

        return offspring

    def playtest(self, gameParam):
        playtestNtimes(gameParameters=gameParam)
        gameParam = self.calculateCriteria(gameParam)
        os.remove("metrics/game" + str(gameParam.troopsWonBeginTurn) + "-" + str(gameParam.defenseDices) + "-"
                      + gameParam.initialTerritoriesMode + "-" + gameParam.troopsToNewTerritory + ".txt")

    def calculateCriteria(self, gameParam):
        gameParam.criteria = op.calculateCriteria(gameParam)

        return gameParam

    def updatePopulation(self, offspring, generation):
        strToWrite = "Generation " + str(generation) + " of " + str(self.numGenerations) + " generations\n"
        strToWrite += "Best fitness: " + str(self.population[0].fitness) + "\n\n"
        strToWrite += "Population: \n"

        for child in self.population:
            strToWrite += "_________________________________________________________________________________________" + "\n"
            strToWrite += "Fitness: " + str(child.fitness) + "\n"
            strToWrite += "Parameters: \n"
            strToWrite += "Map in " + child.mapPath + " with the following parameters:\n"
            strToWrite += "troopsWonBeginTurn: " + str(child.troopsWonBeginTurn) + "\n"
            strToWrite += "defenseDices: " + str(child.defenseDices) + "\n"
            strToWrite += "initialTerritoriesMode: " + str(child.initialTerritoriesMode) + "\n"
            strToWrite += "troopsToNewTerritory: " + str(child.troopsToNewTerritory) + "\n"
            strToWrite += "Criteria: \n"
            strToWrite += "Advantage: " + str(child.criteria["advantage"]) + "\n"
            strToWrite += "Duration: " + str(child.criteria["duration"]) + "\n"
            strToWrite += "Drama: " + str(child.criteria["drama"]) + "\n"
            strToWrite += "Lead Change: " + str(child.criteria["leadChange"]) + "\n"
            strToWrite += "Branching Factor: " + str(child.criteria["branchingFactor"]) + "\n"
            strToWrite += "Completion: " + str(child.criteria["completion"]) + "\n"
            strToWrite += "Killer Moves: " + str(child.criteria["killerMoves"]) + "\n"

        fileName = "parameters/generation" + str(generation + 1) + ".txt"
        with open(fileName, "w") as file:
            file.write(strToWrite)

        self.population = offspring

    def showResults(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)

        strToWrite = "Final population:\n"

        for gameParam in self.population:
            strToWrite += "_________________________________________________________________________________________" + "\n"
            strToWrite += "Fitness: " + str(gameParam.fitness) + "\n"
            strToWrite += "Parameters: \n"
            strToWrite += "Map in " + gameParam.mapPath + " with the following parameters:\n"
            strToWrite += "troopsWonBeginTurn: " + str(gameParam.troopsWonBeginTurn) + "\n"
            strToWrite += "defenseDices: " + str(gameParam.defenseDices) + "\n"
            strToWrite += "initialTerritoriesMode: " + str(gameParam.initialTerritoriesMode) + "\n"
            strToWrite += "troopsToNewTerritory: " + str(gameParam.troopsToNewTerritory) + "\n"
            strToWrite += "Criteria: \n"
            strToWrite += "Advantage: " + str(gameParam.criteria["advantage"]) + "\n"
            strToWrite += "Duration: " + str(gameParam.criteria["duration"]) + "\n"
            strToWrite += "Drama: " + str(gameParam.criteria["drama"]) + "\n"
            strToWrite += "Lead Change: " + str(gameParam.criteria["leadChange"]) + "\n"
            strToWrite += "Branching Factor: " + str(gameParam.criteria["branchingFactor"]) + "\n"
            strToWrite += "Completion: " + str(gameParam.criteria["completion"]) + "\n"
            strToWrite += "Killer Moves: " + str(gameParam.criteria["killerMoves"]) + "\n"

        with open(fileName, "w") as file:
            file.write(strToWrite)

        self.plotFitness()

    def moveFiles(self):
        maps = os.listdir("parameters/")
        os.mkdir("parameters/results_risk_generation_" + str(self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate")

        for map in maps:
            if map.startswith("map") and map.endswith(".json") and map not in ["map1.json", "map2.json", "map3.json",
                                                                               "map4.json", "map5.json", "map6.json",
                                                                               "map7.json", "map8.json", "map9.json",
                                                                               "map10.json"]:
                shutil.move("parameters/" + map,
                            "parameters/results_risk_generation_" + str(
                                self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
                                self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate/")

        shutil.move("results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate.txt", "parameters/results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate/")

        shutil.move("fitness_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate.png", "parameters/results_risk_generation_" + str(
            self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate/")

        generations = os.listdir("parameters")
        for generation in generations:
            if generation.startswith("generation"):
                shutil.move("parameters/" + generation,
                            "parameters/results_risk_generation_" + str(
                                self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
                                self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate/")

        # remove metrics files
        metrics = os.listdir("metrics/")
        for metric in metrics:
            if metric.startswith("game"):
                os.remove("metrics/" + metric)

    def plotFitness(self):
        # plot all fitness along generations, with min, max and average

        maxFitness = []
        minFitness = []
        avgFitness = []
        idealFitness = []
        worstFitness = []
        x = range(1, len(self.allFitness) + 1)

        for gen in self.allFitness:
            maxFitness.append(max(gen))
            minFitness.append(min(gen))
            avgFitness.append(sum(gen) / len(gen))
            idealFitness.append(0)
            worstFitness.append(5)

        plt.clf()
        plt.plot(x, worstFitness, label="Worst")
        plt.plot(x, maxFitness, label="Max")
        plt.plot(x, avgFitness, label="Avg")
        plt.plot(x, minFitness, label="Min")
        plt.plot(x, idealFitness, label="Ideal")
        plt.legend(loc="upper right")
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.title("Fitness along generations")
        plt.savefig("fitness_" + str(self.numGenerations) + "generations_" + str(self.numOffspring) + "offspring_" + str(
            self.tournamentSize) + "tournamentsize_" + str(self.mutationRate) + "mutationrate.png")
        plt.show()


if __name__ == "__main__":
    #s = Synthesis(numGenerations=10, numOffspring=25, tournamentSize=8, mutationRate=0.8)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=30, numOffspring=35, tournamentSize=6, mutationRate=0.8)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=90, numOffspring=45, tournamentSize=20, mutationRate=0.6)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=30, numOffspring=45, tournamentSize=2, mutationRate=0.6)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=150, numOffspring=50, tournamentSize=6, mutationRate=0.4)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=150, numOffspring=20, tournamentSize=6, mutationRate=0.8)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=150, numOffspring=30, tournamentSize=8, mutationRate=0.6)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=50, numOffspring=50, tournamentSize=16, mutationRate=0.6)
    #s.gameGenerator()

    #s = Synthesis(numGenerations=150, numOffspring=30, tournamentSize=12, mutationRate=0.1)
    #s.gameGenerator()

    s = Synthesis(numGenerations=10, numOffspring=50, tournamentSize=22, mutationRate=0.6)
    s.gameGenerator()

