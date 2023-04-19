# Evaluate every setting of the parameters
import math
import os
import matplotlib.pyplot as plt
import networkx as nx
import Map as mp
import json
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
    plt.barh(range(10), top10Fitness)
    plt.xlabel("Fitness")
    plt.ylabel("Execução")
    plt.title("10 melhores valores de fitness")
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
    plt.plot(gen, minFitness, label="Min")
    plt.xticks(list(range(10, 200, 20)), gen)
    plt.legend(loc="upper right")
    plt.xlabel("Gerações")
    plt.ylabel("Fitness")
    plt.title("Fitness ao longo das gerações")
    plt.savefig("results/fitness_along_generations.png")

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
    plt.plot(off, minFitness, label="Min")
    plt.xticks(list(range(5, 51, 5)), off)
    plt.legend(loc="upper right")
    plt.xlabel("População")
    plt.ylabel("Fitness")
    plt.title("Fitness ao longo do número de população")
    plt.savefig("results/fitness_along_offspring.png")

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
    plt.plot(tour, minFitness, label="Min")
    plt.xticks(list(range(2, 25, 2)), tour)
    plt.legend(loc="upper right")
    plt.xlabel("Torneio")
    plt.ylabel("Fitness")
    plt.title("Fitness ao longo do número de participantes no torneio")
    plt.savefig("results/fitness_along_tournament_size.png")

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
    plt.plot(mut, minFitness, label="Min")
    plt.xticks(mut, mut)
    plt.legend(loc="upper right")
    plt.xlabel("Taxa de mutação")
    plt.ylabel("Fitness")
    plt.title("Fitness ao longo dos valores de taxa de mutação")
    plt.savefig("results/fitness_along_mutation_rate.png")

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

    folders = os.listdir("results")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("results/" + folder)

    allLines = []

    for folder in resultFolders:
        files = os.listdir(folder + "/")

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

            for line in allText:
                if line.startswith("troopsWonBeginTurn"):
                    allTroopsWonBeginTurn.append(int(line.split(":")[1]))
                elif line.startswith("defenseDices"):
                    allDefenseDices.append(int(line.split(":")[1]))
                elif line.startswith("initialTerritoriesMode"):
                    allInitialTerritoriesMode.append(line.split(":")[1].strip())
                elif line.startswith("troopsToNewTerritory"):
                    allTroopsToNewTerritory.append(line.split(":")[1].strip())

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

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()

                        for line in allText:
                            if line.startswith("Map"):
                                l = line.split(" ")[2]
                                map = l.split("/")[1]

                                if int(map.split(".")[0].split("p")[1]) <= 10:
                                    fd1 = "parameters/" + map
                                else:
                                    fd1 = folder + "/" + f + "/" + map

                                allMap = open(fd1, 'r')
                                mapa = json.load(allMap)
                                allTerritories.append(mapa["territories"][-1])

    allLines = []

    allLines.append("Territories\n")
    allLines.append("Min: " + str(min(allTerritories)) + "\n")
    allLines.append("Max: " + str(max(allTerritories)) + "\n")
    allLines.append("Average: " + str(sum(allTerritories)/len(allTerritories)) + "\n")

    with open("results/territoryStatistics.txt", 'w') as fl:
        fl.writelines(allLines)


def evaluate():
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
    print("Risk to War-----------------------------------------------------------------")
    riskToWar()
    #print()
    #print("Parameter statistics--------------------------------------------------------")
    #parameterStatistics()
    #print()
    #print("Territory Statistics--------------------------------------------------------")
    #territoryStatistics()
    #print()

#evaluate()
