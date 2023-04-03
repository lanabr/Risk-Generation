# Evaluate every setting of the parameters

import os
import matplotlib.pyplot as plt

#arrumar os axis


def best_fitness():
    folders = os.listdir("C:/Users/LanaR/Downloads/results")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("C:/Users/LanaR/Downloads/results/" + folder)

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

    print("Best fitness: " + str(bestFitness))
    print("Best fitness directory: " + resultFiles[bestIndex])
    print("All fitnesses: " + str(allFitness))

    sortedAllFitness = allFitness.copy()
    sortedAllFitness.sort()

    top10Fitness = sortedAllFitness[0:10]
    for fit in top10Fitness:
        print(str(fit) + "in config " + resultFiles[allFitness.index(fit)])

    plt.clf()
    plt.barh(range(10), top10Fitness)
    plt.xlabel("Fitness")
    plt.ylabel("Configuration")
    plt.title("Top 10 fitness")
    plt.savefig("top10fitness.png")
    plt.show()


def fitnessPerGeneration():
    folders = os.listdir("C:/Users/LanaR/Downloads/results")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("C:/Users/LanaR/Downloads/results/" + folder)

    minFitness = []
    avgFitness = []

    for folder in resultFolders:
        subfolder = os.listdir(folder)
        allFitness = []

        for f in subfolder:
            files = os.listdir(folder + "/" + f)
            for file in files:
                if file.startswith('result'):
                    with open(folder + "/" + f + "/" + file, 'r') as fl:
                        allText = fl.readlines()

                        allFitness.append(float(allText[2].split(":")[1]))

        minFitness.append(min(allFitness))
        avgFitness.append(sum(allFitness)/len(allFitness))

    gen = [10, 30, 50, 70, 90, 110, 130, 150, 170, 190]

    print("Best fitness in each generation: ", minFitness)
    print("Average fitness in each generation: ", avgFitness)
    print("Best generation: ", str(gen[minFitness.index(min(minFitness))]))

    plt.clf()
    plt.plot(list(range(10, 111, 20)), avgFitness, label="Avg")
    plt.plot(list(range(10, 111, 20)), minFitness, label="Min")
    plt.legend(loc="upper right")
    plt.xlabel("Configurations")
    plt.ylabel("Fitness")
    plt.title("Fitness along generations")
    plt.savefig("fitness_along_generations.png")
    plt.show()


def fitnessPerOffspring():
    folders = os.listdir("C:/Users/LanaR/Downloads/results")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("C:/Users/LanaR/Downloads/results/" + folder)

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

    print("Best fitness in each offspring: ", minFitness)
    print("Average fitness in each offspring: ", avgFitness)
    print("Best offspring: ", str(off[minFitness.index(min(minFitness))]))

    plt.clf()
    plt.plot(list(range(5, 51, 5)), avgFitness, label="Avg")
    plt.plot(list(range(5, 51, 5)), minFitness, label="Min")
    plt.legend(loc="upper right")
    plt.xlabel("Offspring")
    plt.ylabel("Fitness")
    plt.title("Fitness along offspring")
    plt.savefig("fitness_along_offspring.png")
    plt.show()


def fitnessPerTournamentSize():
    folders = os.listdir("C:/Users/LanaR/Downloads/results")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("C:/Users/LanaR/Downloads/results/" + folder)

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

    print("Best fitness in each tournament size: ", minFitness)
    print("Average fitness in each tournament size: ", avgFitness)
    print("Best tournament size: ", str(tour[minFitness.index(min(minFitness))]))

    plt.clf()
    plt.plot(list(range(2, 25, 2)), avgFitness, label="Avg")
    plt.plot(list(range(2, 25, 2)), minFitness, label="Min")
    plt.legend(loc="upper right")
    plt.xlabel("Tournament size")
    plt.ylabel("Fitness")
    plt.title("Fitness along tournament sizes")
    plt.savefig("fitness_along_tournament_size.png")
    plt.show()


def fitnessPerMutationRate():
    folders = os.listdir("C:/Users/LanaR/Downloads/results")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append("C:/Users/LanaR/Downloads/results/" + folder)

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
                        # 0.2, 0.4, 0.6, 0.8
                        for mut in range(2, 9, 2):
                            if str(mut/10) + "mutationrate" in file:
                                allFitness[int(mut/2)].append(float(allText[2].split(":")[1]))
                                continue

    for mut in range(2, 9, 2):
        minFitness.append(min(allFitness[int(mut/2)]))
        avgFitness.append(sum(allFitness[int(mut/2)]) / len(allFitness[int(mut/2)]))

    mut = [0.2, 0.4, 0.6, 0.8]

    print("Best fitness in each tournament size: ", minFitness)
    print("Average fitness in each tournament size: ", avgFitness)
    print("Best tournament size: ", str(mut[minFitness.index(min(minFitness))]))

    plt.clf()
    plt.plot(list(range(2, 9, 2)), avgFitness, label="Avg")
    plt.plot(list(range(2, 9, 2)), minFitness, label="Min")
    plt.legend(loc="upper right")
    plt.xlabel("Mutation rate")
    plt.ylabel("Fitness")
    plt.title("Fitness along mutation rates")
    plt.savefig("fitness_along_mutation_rate.png")
    plt.show()


def evaluate():
    #best_fitness()
    #print("\n\n")
    #fitnessPerGeneration()
    #print("\n\n")
    #fitnessPerOffspring()
    #print("\n\n")
    #fitnessPerTournamentSize()
    #print("\n\n")
    fitnessPerMutationRate()

evaluate()