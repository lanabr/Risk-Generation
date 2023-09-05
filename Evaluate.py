# Evaluate every setting of the parameters
import math
import os
import matplotlib.pyplot as plt
import networkx as nx
import Map as mp
import json
import numpy as np
from Parameters import Parameters
from AutomatedPlaytest import playtestNtimes
from GeneticOperations import calculateCriteria


def best_fitness():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    resultFiles = []

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    resultFiles.append(folder + "/" + f + "/" + file)

    allFitness = []

    for file in resultFiles:
        with open(file, 'r') as f:
            allText = f.readlines()

            allFitness.append(float(allText[2].split(":")[1]))

    bestFitness = min(allFitness)
    bestIndex = allFitness.index(bestFitness)

    allLines = []

    allLines.append("Best fitness: " + str(bestFitness) + "\n")
    allLines.append("Best fitness directory: " + resultFiles[bestIndex] + "\n")
    allLines.append("All fitnesses: " + str(allFitness) + "\n")

    sortedAllFitness = allFitness.copy()
    sortedAllFitness.sort()

    top10Fitness = sortedAllFitness[0:10]
    for fit in top10Fitness:
        allLines.append(str(fit) + " in config " + resultFiles[allFitness.index(fit)] + "\n")

    plt.clf()
    fig, ax = plt.subplots()
    plt.barh(range(1, 11), top10Fitness)
    plt.xlabel("Fitness")
    plt.ylabel("Execução")
    plt.title("10 melhores valores de fitness")
    plt.yticks(range(1, 11), range(1, 11))
    rects = ax.patches

    for rect in rects:
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        space = -5
        ha = 'right'
        label = "{:.4f}".format(x_value)

        # Create annotation
        plt.annotate(label, (x_value, y_value), xytext=(space, 0), textcoords="offset points", va='center', ha=ha, color="white")

    plt.savefig("results/top10fitness.png")

    with open("results/bestFitness.txt", 'w') as fl:
        fl.writelines(allLines)


def fitnessPerGeneration():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    minFitness = []
    avgFitness = []

    allFitness = [[], [], [], [], [], [], [], [], [], []]

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()

                        # 10, 30, 50, 70, 90, 110, 130, 150, 170, 190
                        for off in range(10, 200, 20):
                            if str(off) + "generation" in file:
                                allFitness[math.floor(off / 20)].append(float(allText[2].split(":")[1]))
                                continue

    for off in range(10, 200, 20):
        minFitness.append(min(allFitness[math.floor(off / 20)]))
        avgFitness.append(sum(allFitness[math.floor(off / 20)]) / len(allFitness[math.floor(off / 20)]))

    gen = [10, 30, 50, 70, 90, 110, 130, 150, 170, 190]

    allLines = []

    allLines.append("Best fitness in each generation: " + str(minFitness) + "\n")
    allLines.append("Average fitness in each generation: " + str(avgFitness) + "\n")
    allLines.append("Best generation: " + str(gen[minFitness.index(min(minFitness))]) + "\n")

    plt.clf()

    plt.plot(gen, avgFitness, label="Avg")
    plt.bar(gen, minFitness, width=7, color='red', label="Min")
    plt.xticks(list(range(10, 200, 20)), gen)
    plt.legend(loc="upper right")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Fitness for each value of generations")
    plt.savefig("results/fitness_along_generations.pdf")

    with open("results/fitnessPerGeneration.txt", 'w') as fl:
        fl.writelines(allLines)


def fitnessPerOffspring():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    minFitness = []
    avgFitness = []

    allFitness = [[], [], [], [], [], [], [], [], [], [], []]

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()
                        # 5, 10, 15, 20, 25, 30, 35, 40, 45, 50
                        for off in range(5, 51, 5):
                            if str(off) + "offspring" in file:
                                allFitness[int(off/5)].append(float(allText[2].split(":")[1]))
                                continue

    for off in range(5, 51, 5):
        minFitness.append(min(allFitness[int(off/5)]))
        avgFitness.append(sum(allFitness[int(off/5)]) / len(allFitness[int(off/5)]))

    off = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    allLines = []

    allLines.append("Best fitness in each offspring: " + str(minFitness) + "\n")
    allLines.append("Average fitness in each offspring: " + str(avgFitness) + "\n")
    allLines.append("Best offspring: " + str(off[minFitness.index(min(minFitness))]) + "\n")

    plt.clf()
    plt.plot(off, avgFitness, label="Avg")
    plt.bar(off, minFitness, width=1.8, color='red', label="Min")
    plt.xticks(list(range(5, 51, 5)), off)
    plt.legend(loc="upper right")
    plt.xlabel("Offspring size")
    plt.ylabel("Fitness")
    plt.title("Fitness for each value of offspring size")
    plt.savefig("results/fitness_along_offspring.pdf")

    with open("results/fitnessPerOffspring.txt", 'w') as fl:
        fl.writelines(allLines)


def fitnessPerTournamentSize():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    minFitness = []
    avgFitness = []

    allFitness = [[], [], [], [], [], [], [], [], [], [], [], [], []]

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()
                        # 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24
                        for tour in range(2, 25, 2):
                            if str(tour) + "tournamentsize" in file:
                                allFitness[int(tour/2)].append(float(allText[2].split(":")[1]))
                                continue

    for tour in range(2, 25, 2):
        minFitness.append(min(allFitness[int(tour/2)]))
        avgFitness.append(sum(allFitness[int(tour/2)]) / len(allFitness[int(tour/2)]))

    tour = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]

    allLines = []

    allLines.append("Best fitness in each tournament size: "  + str(minFitness) + "\n")
    allLines.append("Average fitness in each tournament size: " + str(avgFitness) + "\n")
    allLines.append("Best tournament size: " + str(tour[minFitness.index(min(minFitness))]) + "\n")

    plt.clf()
    plt.plot(tour, avgFitness, label="Avg")
    plt.bar(tour, minFitness, width=0.9, color='red', label="Min")
    plt.xticks(list(range(2, 25, 2)), tour)
    plt.legend(loc="upper right")
    plt.xlabel("Tournament size")
    plt.ylabel("Fitness")
    plt.title("Fitness for each value of tournament size")
    plt.savefig("results/fitness_along_tournament_size.pdf")

    with open("results/fitnessPerTournamentSize.txt", 'w') as fl:
        fl.writelines(allLines)


def fitnessPerMutationRate():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    minFitness = []
    avgFitness = []

    allFitness = [[], [], [], [], []]

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()
                        # 0.2, 0.4, 0.6, 0.8
                        for mut in range(2, 9, 2):
                            if str(mut/10) + "mutationrate" in file:
                                allFitness[int(mut/2)].append(float(allText[2].split(":")[1]))
                                continue
                        if str(0.1) + "mutationrate" in file:
                            allFitness[0].append(float(allText[2].split(":")[1]))

    minFitness.append(min(allFitness[0]))
    avgFitness.append(sum(allFitness[0]) / len(allFitness[0]))

    for mut in range(2, 9, 2):
        minFitness.append(min(allFitness[int(mut/2)]))
        avgFitness.append(sum(allFitness[int(mut/2)]) / len(allFitness[int(mut/2)]))

    mut = [0.1, 0.2, 0.4, 0.6, 0.8]

    allLines = []

    allLines.append("Best fitness in each tournament size: " + str(minFitness) + "\n")
    allLines.append("Average fitness in each tournament size: " + str(avgFitness) + "\n")
    allLines.append("Best tournament size: " + str(mut[minFitness.index(min(minFitness))]) + "\n")

    plt.clf()
    plt.plot(mut, avgFitness, label="Avg")
    plt.bar(mut, minFitness, width=0.03, color='red', label="Min")
    plt.xticks(mut, mut)
    plt.legend(loc="upper right")
    plt.xlabel("Mutation rate")
    plt.ylabel("Fitness")
    plt.title("Fitness for each value of mutation rate")
    plt.savefig("results/fitness_along_mutation_rate.pdf")

    with open("results/fitnessPerMutationRate.txt", 'w') as fl:
        fl.writelines(allLines)


def mapComparison():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    allLines = []

    for folder in resultFolders:
        f = os.listdir(folder)
        for subfolder in f:
            firstMaps = []
            lastMaps = []
            files = []
            genFiles = []

            files = os.listdir(folder + "/" + subfolder)

            genFiles = [file if file.startswith("generation") else None for file in files]
            genFiles = [file for file in genFiles if file is not None]
            sortedFiles = sorted(genFiles, key=lambda x: int(x.split(".")[0].split("on")[1]))

            with open(folder + "/" + subfolder + "/" + sortedFiles[0], 'r') as fl:
                allText = fl.readlines()

                for line in allText:
                    if line.startswith("Map"): # Map in parameters/map7.json with the following parameters:
                        l = line.split(" ")[2]
                        firstMaps.append(l.split("/")[1])

            with open(folder + "/" + subfolder + "/" + sortedFiles[-1], 'r') as fl:
                allText = fl.readlines()

                for line in allText:
                    if line.startswith("Map"):
                        l = line.split(" ")[2]
                        lastMaps.append(l.split("/")[1])

            for i in range(len(firstMaps)):
                if int(firstMaps[i].split(".")[0].split("p")[1]) <= 10:
                    fd1 = "parameters/" + firstMaps[i]
                else:
                    fd1 = folder + "/" + subfolder + "/" + firstMaps[i]
                fMap = mp.Map(fd1)
                for j in range(len(lastMaps)):
                    if int(lastMaps[i].split(".")[0].split("p")[1]) <= 10:
                        fd2 = "parameters/" + lastMaps[i]
                    else:
                        fd2 = folder + "/" + subfolder + "/" + lastMaps[i]
                    lMap = mp.Map(fd2)
                    if nx.is_isomorphic(fMap.map, lMap.map):
                        allLines.append("Mapas iguais: " + firstMaps[i] + " e " + lastMaps[j] + "\n")
                        allLines.append("Subfolder: " + subfolder + "\n")

    with open("results/mapComparision.txt", 'w') as fl:
        fl.writelines(allLines)


def printCriteria(gameParam):
    allLines = []

    allLines.append("Advantage: " + str(gameParam.criteria["advantage"]) + "\n")
    allLines.append("Drama: " + str(gameParam.criteria["drama"]) + "\n")
    allLines.append("Duration: " + str(gameParam.criteria["duration"]) + "\n")
    allLines.append("Lead change: " + str(gameParam.criteria["leadChange"]) + "\n")
    allLines.append("Branching factor: " + str(gameParam.criteria["branchingFactor"]) + "\n")
    allLines.append("Completion: " + str(gameParam.criteria["completion"]) + "\n")
    allLines.append("Killer moves: " + str(gameParam.criteria["killerMoves"]) + "\n")

    return allLines


def riskAndWarCriteria():
    gameParamRisk = Parameters("parameters/map1.json", 3, 2, "pick", "max")
    gameParamWar = Parameters("parameters/warmap.json", 2, 3, "random", "min")

    allLines = []

    playtestNtimes(gameParameters=gameParamRisk, numberOfTimes=300)
    gameParamRisk.criteria = calculateCriteria(gameParamRisk)
    os.remove("metrics/game" + str(gameParamRisk.troopsWonBeginTurn) + "-" + str(gameParamRisk.defenseDices) + "-"
              + gameParamRisk.initialTerritoriesMode + "-" + gameParamRisk.troopsToNewTerritory + ".txt")

    playtestNtimes(gameParameters=gameParamWar, numberOfTimes=300)
    gameParamWar.criteria = calculateCriteria(gameParamWar)
    os.remove("metrics/game" + str(gameParamWar.troopsWonBeginTurn) + "-" + str(gameParamWar.defenseDices) + "-"
              + gameParamWar.initialTerritoriesMode + "-" + gameParamWar.troopsToNewTerritory + ".txt")

    allLines.append("Risk criteria\n")
    for line in printCriteria(gameParamRisk):
        allLines.append(line)

    allLines.append("War criteria\n")
    for line in printCriteria(gameParamWar):
        allLines.append(line)

    with open("results/RiskAndWarCriteria.txt", 'w') as fl:
        fl.writelines(allLines)


def riskToWar():
    war = Parameters("parameters/warmap.json", 2, 3, "random", "min")

    folders = os.listdir("parameters")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("parameters/" + folder)

    allLines = []

    for folder in resultFolders:
        files = os.listdir(folder + "/")
        allLines.append("\n")
        allLines.append(folder)

        genFiles = [file if file.startswith("generation") or file.startswith("result") else None for file in files]
        genFiles = [file for file in genFiles if file is not None]

        for file in genFiles:
            with open(folder + "/" + "/" + file, 'r') as fl:
                allText = fl.readlines()

                for line in allText:
                    if line.startswith("Map"):
                        l = line.split(" ")[2]
                        mapFile = l.split("/")[1]
                        if int(mapFile.split(".")[0].split("p")[1]) <= 10:
                            fd = "parameters/" + mapFile
                        else:
                            fd = folder + "/" + mapFile
                    elif line.startswith("troopsWonBeginTurn"):
                        troopsWonBeginTurn = int(line.split(":")[1])
                    elif line.startswith("defenseDices"):
                        defenseDices = int(line.split(":")[1])
                    elif line.startswith("initialTerritoriesMode"):
                        initialTerritoriesMode = line.split(":")[1].strip()
                    elif line.startswith("troopsToNewTerritory"):
                        troopsToNewTerritory = line.split(":")[1].strip()
                    elif line.startswith("Criteria:"):
                        if troopsWonBeginTurn == war.troopsWonBeginTurn and defenseDices == war.defenseDices and initialTerritoriesMode == war.initialTerritoriesMode and troopsToNewTerritory == war.troopsToNewTerritory:
                            allLines.append("Jogo igual ao War encontrado, apenas nos parâmetros\n")
                            mapTemp = mp.Map(fd)
                            warMap = mp.Map("parameters/warmap.json")
                            if nx.is_isomorphic(mapTemp.map, warMap.map):
                                allLines.append("Jogo igual ao War encontrado\n")
                                allLines.append("Mapa: " + mapFile + "\n")
                                allLines.append("Subfolder: " + folder + "\n")

    with open("results/RiskToWar.txt", 'w') as fl:
        fl.writelines(allLines)


def best_fitness_over_all_generations():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    allLines = []

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)

            allFitness = []
            allBestFitness = 0
            allFiles = []
            for file in files:
                if file.startswith('generation'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()

                        allFitness.append(float(allText[1].split(":")[1]))
                        allFiles.append(file)
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()

                        allBestFitness = float(allText[2].split(":")[1])

            bestFitness = min(allFitness)

            if bestFitness < allBestFitness:
                allLines += "------------------------------------------------------------------------\n"
                allLines += "Final best fitness is not the best fitness\n"
                allLines += "Best fitness: " + str(bestFitness) + " in " + allFiles[allFitness.index(bestFitness)] + "\n"
                allLines += "Found in folder: " + f + "\n"

    with open("results/bestFitnessOverAllGenerations.txt", 'w') as fl:
        fl.writelines(allLines)


def parameterStatistics():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    resultFiles = []

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    resultFiles.append(folder + "/" + f + "/" + file)

    allTroopsWonBeginTurn = []
    allDefenseDices = []
    allInitialTerritoriesMode = []
    allTroopsToNewTerritory = []

    for file in resultFiles:
        with open(file, 'r') as f:
            allText = f.readlines()

            allTroopsWonBeginTurn.append(int(allText[5].split(":")[1]))
            allDefenseDices.append(int(allText[6].split(":")[1]))
            allInitialTerritoriesMode.append(allText[7].split(":")[1].strip())
            allTroopsToNewTerritory.append(allText[8].split(":")[1].strip())

    allLines = []

    allLines.append("Troops Won Begin Turn\n")
    allLines.append("1: " + str(allTroopsWonBeginTurn.count(1)) + "\n")
    allLines.append("2: " + str(allTroopsWonBeginTurn.count(2)) + "\n")
    allLines.append("3: " + str(allTroopsWonBeginTurn.count(3)) + "\n")
    allLines.append("4: " + str(allTroopsWonBeginTurn.count(4)) + "\n")
    allLines.append("Defense Dices\n")
    allLines.append("2: " + str(allDefenseDices.count(2)) + "\n")
    allLines.append("3: " + str(allDefenseDices.count(3)) + "\n")
    allLines.append("Initial Territories Mode\n")
    allLines.append("Random: " + str(allInitialTerritoriesMode.count("random")) + "\n")
    allLines.append("Pick: " + str(allInitialTerritoriesMode.count("pick")) + "\n")
    allLines.append("Troops to New Territory\n")
    allLines.append("Min: " + str(allTroopsToNewTerritory.count("min")) + "\n")
    allLines.append("Max: " + str(allTroopsToNewTerritory.count("max")) + "\n")
    allLines.append("Min e Max\n")
    allLines.append("Troops Won Begin Turn: " + str(min(allTroopsWonBeginTurn)) + " e " + str(max(allTroopsWonBeginTurn)) + "\n")
    allLines.append("Defense Dices: " + str(min(allDefenseDices)) + " e " + str(max(allDefenseDices)) + "\n")
    allLines.append("Initial Territories Mode: " + str(min(allInitialTerritoriesMode)) + " e " + str(max(allInitialTerritoriesMode)) + "\n")
    allLines.append("Troops to New Territory: " + str(min(allTroopsToNewTerritory)) + " e " + str(max(allTroopsToNewTerritory)) + "\n")

    with open("results/parameterStatistics.txt", 'w') as fl:
        fl.writelines(allLines)


def territoryStatistics():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    allTerritories = []
    twoTerritories = []

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()

                        l = allText[4].split(" ")[2]
                        map = l.split("/")[1]

                        if int(map.split(".")[0].split("p")[1]) <= 10:
                            fd1 = "parameters/" + map
                        else:
                            fd1 = folder + "/" + f + "/" + map

                        allMap = open(fd1, 'r')
                        mapa = json.load(allMap)
                        allTerritories.append(mapa["territories"][-1] + 1)
                        if allTerritories[-1] == 3:
                            twoTerritories.append(folder + "/" + f + "/" + map)


    allLines = []

    allLines.append("Territories\n")
    allLines.append("Min: " + str(min(allTerritories)) + "\n")
    allLines.append("Max: " + str(max(allTerritories)) + "\n")
    allLines.append("Average: " + str(sum(allTerritories)/len(allTerritories)) + "\n")

    all10 = 0
    for ter in allTerritories:
        if ter <= 10:
            all10 += 1

    allLines.append("Até 10 territórios: " + str(all10) + "\n")

    allLines.append("Two Territories Folders\n")
    for folder in twoTerritories:
        allLines.append(folder + "\n")

    allLines.append("All Territories:\n")
    for ter in allTerritories:
        allLines.append(str(ter) + "\n")

    with open("results/territoryStatistics.txt", 'w') as fl:
        fl.writelines(allLines)


def newGraphics():
    # gerar os graficos de cada pasta de novo mas com titulo e legenda em portugues

    resultFolders = [
                     #"/home/lana/Documentos/results risk generation/result_10generations",
                     #"/home/lana/Documentos/results risk generation/result_30generations",
                     #"/home/lana/Documentos/results risk generation/result_50generations",
                     #"/home/lana/Documentos/results risk generation/result_70generations",
                     #"/home/lana/Documentos/results risk generation/result_90generations",
                     #"/home/lana/Documentos/results risk generation/result_110generations",
                     #"/home/lana/Documentos/results risk generation/result_150generations",
                     #"/home/lana/Documentos/results risk generation/result_170generations",
                     #"/home/lana/Documentos/results risk generation/result_130generations"
                     #"/home/lana/Documentos/results risk generation/result_190generations"
                    ]

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        print(folder)

        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            allFitness = []
            for file in files:
                if file.startswith('generation'):
                    allFitness.append([])
            allFitness.append([])
            for file in files:
                if file.startswith('generation'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()
                        for line in allText:
                            if line.startswith("Fitness"):
                                index = int(file.split("generation")[1].split(".")[0]) - 1
                                allFitness[index].append(float(line.split(":")[1].strip()))
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()
                        for line in allText:
                            if line.startswith("Fitness"):
                                allFitness[-1].append(float(line.split(":")[1].strip()))

            maxFitness = []
            minFitness = []
            avgFitness = []
            idealFitness = []
            worstFitness = []
            x = range(0, len(allFitness))

            for gen in allFitness:
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

            numGenerations = f.split("_")[3].split("generations")[0]
            numOffspring = f.split("_")[4].split("offspring")[0]
            tournamentSize = f.split("_")[5].split("tournament")[0]
            mutationRate = f.split("_")[6].split("mutation")[0]

            plt.savefig(folder + "/" + f + "/" +
                "fitness3_" + str(numGenerations) + "generations_" + str(numOffspring) + "offspring_" + str(
                    tournamentSize) + "tournamentsize_" + str(mutationRate) + "mutationrate.pdf")
            plt.show()


def diffFitness():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    resultFiles = []

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    resultFiles.append(folder + "/" + f + "/" + file)

    allFitness = []
    allAdvantage = []
    allDuration = []
    allDrama = []
    allLeadChange = []
    allBranchingfactor = []
    allCompletion = []
    allKillerMoves = []

    for file in resultFiles:
        with open(file, 'r') as f:
            allText = f.readlines()

            allFitness.append(float(allText[2].split(":")[1]))
            allAdvantage.append(float(allText[10].split(":")[1]))
            allDuration.append(float(allText[11].split(":")[1]))
            allDrama.append(float(allText[12].split(":")[1]))
            allLeadChange.append(float(allText[13].split(":")[1]))
            allBranchingfactor.append(float(allText[14].split(":")[1]))
            allCompletion.append(float(allText[15].split(":")[1]))
            allKillerMoves.append(float(allText[16].split(":")[1]))

    allLines = []

    allLines.append("Difference in criteria values")

    for i in range(len(allFitness)):
        allLines.append("Fitness: " + str(allFitness[i]) + "\n")
        diffAdvantage = abs(allAdvantage[i] - 0)
        diffDuration = abs(allDuration[i] - 0)
        diffDrama = abs(allDrama[i] - 0.5)
        diffLeadChange = abs(allLeadChange[i] - 0.5)
        diffBranchingFactor = abs(allBranchingfactor[i] - 0.5)
        diffCompletion = abs(allCompletion[i] - 1)
        diffKillerMoves = abs(allKillerMoves[i] - 0.5)

        diffs = [diffAdvantage, diffDuration, diffDrama, diffLeadChange, diffBranchingFactor, diffCompletion, diffKillerMoves]

        allLines.append("Bigger difference: \n")
        if max(diffs) == diffAdvantage:
            allLines.append("Advantage: " + str(diffAdvantage) + "\n")
            diffs.remove(diffAdvantage)
        elif max(diffs) == diffDrama:
            allLines.append("Drama: " + str(diffDrama) + "\n")
            diffs.remove(diffDrama)
        elif max(diffs) == diffLeadChange:
            allLines.append("Lead Change: " + str(diffLeadChange) + "\n")
            diffs.remove(diffLeadChange)
        elif max(diffs) == diffBranchingFactor:
            allLines.append("Branching Factor: " + str(diffBranchingFactor) + "\n")
            diffs.remove(diffBranchingFactor)
        elif max(diffs) == diffCompletion:
            allLines.append("Completion: " + str(diffCompletion) + "\n")
            diffs.remove(diffCompletion)
        elif max(diffs) == diffKillerMoves:
            allLines.append("Killer Moves: " + str(diffKillerMoves) + "\n")
            diffs.remove(diffKillerMoves)
        elif max(diffs) == diffDuration:
            allLines.append("Duration: " + str(diffDuration) + "\n")
            diffs.remove(diffDuration)

        '''
        if max(diffs) == diffAdvantage:
            allLines.append("Advantage: " + str(diffAdvantage) + "\n")
        elif max(diffs) == diffDuration:
            allLines.append("Duration: " + str(diffDuration) + "\n")
        elif max(diffs) == diffDrama:
            allLines.append("Drama: " + str(diffDrama) + "\n")
        elif max(diffs) == diffLeadChange:
            allLines.append("Lead Change: " + str(diffLeadChange) + "\n")
        elif max(diffs) == diffBranchingFactor:
            allLines.append("Branching Factor: " + str(diffBranchingFactor) + "\n")
        elif max(diffs) == diffCompletion:
            allLines.append("Completion: " + str(diffCompletion) + "\n")
        elif max(diffs) == diffKillerMoves:
            allLines.append("Killer Moves: " + str(diffKillerMoves) + "\n")
        '''

    with open("results/diffCriteriaFitness.txt", 'w') as fl:
        fl.writelines(allLines)


def mapCentrality():
    folders = os.listdir("/home/lana/Documentos/results risk generation")
    resultFolders = []

    for folder in folders:
        if folder.startswith('result'):
            resultFolders.append("/home/lana/Documentos/results risk generation/" + folder)

    degreeCentrality = []
    betweennessCentrality = []
    territories = []
    fitness = []
    bottleneck = []
    nameMaps = []

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()

                        l = allText[4].split(" ")[2]
                        map = l.split("/")[1]

                        if int(map.split(".")[0].split("p")[1]) <= 10:
                            fd1 = "parameters/" + map
                        else:
                            fd1 = folder + "/" + f + "/" + map

                        allMap = open(fd1, 'r')
                        mapa = json.load(allMap)
                        mapaClass = mp.Map(fd1)

                        fitness.append(float(allText[2].split(":")[1]))
                        territories.append(mapa["territories"][-1] + 1)

                        degree = nx.degree_centrality(mapaClass.map)
                        degreeCentrality.append(sum(degree.values())/len(degree))

                        betweenness = nx.betweenness_centrality(mapaClass.map)
                        betweennessCentrality.append(sum(betweenness.values())/len(betweenness))

                        bottleneck.append(max(betweenness.values()))
                        nameMaps.append(fd1)

    plt.clf()
    plt.scatter(territories, bottleneck)
    plt.ylabel("Highest bottleneck")
    plt.xlabel("Territories")
    plt.savefig("results/bottleneckPerTerritories.png")

    plt.clf()
    plt.scatter(territories, degreeCentrality)
    plt.ylabel("Degree Centrality")
    plt.xlabel("Territories")
    plt.savefig("results/degreePerTerritories.png")

    plt.clf()
    plt.scatter(territories, betweennessCentrality)
    plt.ylabel("Betweenness Centrality")
    plt.xlabel("Territories")
    plt.savefig("results/betweennessPerTerritories.png")

    plt.clf()
    plt.scatter(fitness, degreeCentrality)
    plt.ylabel("Degree Centrality")
    plt.xlabel("Fitness")
    plt.savefig("results/degreePerFitness.png")

    plt.clf()
    plt.scatter(fitness, betweennessCentrality)
    plt.ylabel("Betweenness Centrality")
    plt.xlabel("Fitness")
    plt.savefig("results/betweennessPerFitness.png")

    plt.clf()
    plt.scatter(territories, fitness)
    plt.xlabel("Territories")
    plt.ylabel("Fitness")
    plt.savefig("results/territoriesFitness.png")


def newFitness():
    folders = os.listdir("/home/lana/Documentos/results risk generation/new criteria")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("/home/lana/Documentos/results risk generation/new criteria/" + folder)

    allLines = []

    for folder in resultFolders:
        files = os.listdir(folder)
        sum = 0
        criteria = []
        for file in files:
            if file.startswith('result'):
                with open(folder + "/" + file, 'r') as f:
                    allText = f.readlines()

                    allLines.append(folder + "\n")
                    allLines.append("Fitness: " + allText[2].split(":")[1])
                    allLines.append("New Fitness: ")

                    if "advantage" in folder:
                        sum += 0
                        criteria.append("advantage")
                    if "duration" in folder:
                        sum += 0
                        criteria.append("duration")
                    if "drama" in folder:
                        sum += 0.5
                        criteria.append("drama")
                    if "leadChange" in folder:
                        sum += 0.5
                        criteria.append("leadChange")
                    if "branchingFactor" in folder:
                        sum += 0.5
                        criteria.append("branchingFactor")
                    if "completion" in folder:
                        sum += 1
                        criteria.append("completion")
                    if "killerMoves" in folder:
                        sum += 0.5
                        criteria.append("killerMoves")

                    fitness = allText[2].split(":")[1]
                    result = (float(fitness[1:-2]) * 5.0) / sum
                    allLines.append(str(result) + "\n\n")

    with open("results/newFitness.txt", 'w') as fl:
        fl.writelines(allLines)


def avgExec():
    folders = os.listdir("/home/lana/Documentos/results risk generation/execs")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("/home/lana/Documentos/results risk generation/execs/" + folder)

    execs = []

    for folder in resultFolders:
        execs.append(folder[:-1])

    uniqueExecs = list(set(execs))

    execsFitness = []

    for exec in uniqueExecs:
        execsFitness.append([])

    for folder in resultFolders:
        files = os.listdir(folder)
        sum = 0
        criteria = []
        for file in files:
            if file.startswith('result'):
                with open(folder + "/" + file, 'r') as f:
                    allText = f.readlines()

                    if "advantage" in folder:
                        sum += 0
                        criteria.append("advantage")
                    if "duration" in folder:
                        sum += 0
                        criteria.append("duration")
                    if "drama" in folder:
                        sum += 0.5
                        criteria.append("drama")
                    if "leadChange" in folder:
                        sum += 0.5
                        criteria.append("leadChange")
                    if "branchingFactor" in folder:
                        sum += 0.5
                        criteria.append("branchingFactor")
                    if "completion" in folder:
                        sum += 1
                        criteria.append("completion")
                    if "killerMoves" in folder:
                        sum += 0.5
                        criteria.append("killerMoves")

                    fitness = allText[2].split(":")[1]
                    result = (float(fitness[1:-2]) * 5.0) / sum
                    execsFitness[uniqueExecs.index(folder[:-1])].append(result)

    allLines = []

    for i in range(len(uniqueExecs)):
        allLines.append(uniqueExecs[i] + "\n")
        allLines.append("Average: " + str(math.fsum(execsFitness[i]) / len(execsFitness[i])) + "\n")
        allLines.append("Std: " + str(np.std(execsFitness[i])) + "\n")
        allLines.append("Fitness: " + str(execsFitness[i]) + "\n\n")

        plt.clf()
        plt.bar(range(1, len(execsFitness[i])+1), execsFitness[i], width=0.3)
        plt.plot(range(1, len(execsFitness[i])+1), [math.fsum(execsFitness[i]) / len(execsFitness[i])] * len(execsFitness[i]), color='red')
        plt.plot(range(1, len(execsFitness[i])+1), [math.fsum(execsFitness[i]) / len(execsFitness[i]) + np.std(execsFitness[i])] * len(execsFitness[i]), color='green')
        plt.plot(range(1, len(execsFitness[i])+1), [math.fsum(execsFitness[i]) / len(execsFitness[i]) - np.std(execsFitness[i])] * len(execsFitness[i]), color='green')
        plt.title(uniqueExecs[i].split("/")[-1])
        plt.xlabel("Execs")
        plt.ylabel("Fitness")

        plt.savefig("results/" + uniqueExecs[i].split("/")[-1] + ".png")
        plt.show()

    with open("results/newExecsFitness.txt", 'w') as fl:
        fl.writelines(allLines)


def evaluate():
    pass
    #print("Best fitness----------------------------------------------------------------")
    #best_fitness()
    #print()
    #print("Best fitness over all generations-------------------------------------------")
    #best_fitness_over_all_generations()
    #print()
    #print("Per Generation--------------------------------------------------------------")
    #fitnessPerGeneration()
    #print()
    #print("Per Offspring---------------------------------------------------------------")
    #fitnessPerOffspring()
    #print()
    #print("Per Tournament Size---------------------------------------------------------")
    #fitnessPerTournamentSize()
    #print()
    #print("Per Mutation Rate-----------------------------------------------------------")
    #fitnessPerMutationRate()
    #print()
    #print("Map Comparison-------------------------------------------------------------")
    #mapComparison()
    #print()
    #print("Risk and War Criteria-------------------------------------------------------")
    #riskAndWarCriteria()
    #print()
    #print("Risk to War-----------------------------------------------------------------")
    #riskToWar()
    #print()
    #print("Parameter statistics--------------------------------------------------------")
    #parameterStatistics()
    #print()
    #print("Territory Statistics--------------------------------------------------------")
    #territoryStatistics()
    #print()
    #print("New graphics-----------------------------------------------------------------")
    #newGraphics()
    #print()
    #print("Diff fitness-----------------------------------------------------------------")
    #diffFitness()
    #print()
    #print("Map Centrality--------------------------------------------------------------")
    #mapCentrality()
    #print()
    #print("New Fitness-----------------------------------------------------------------")
    #newFitness()
    #print()
    #print("Avg Exec--------------------------------------------------------------------")
    #avgExec()
    print()


evaluate()
