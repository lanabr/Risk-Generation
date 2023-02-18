# Evaluate every setting of the parameters

import os


def evaluate():
    folders = os.listdir("parameters")
    resultFolders = []

    for folder in folders:
        if folder.startswith('results'):
            resultFolders.append(folder)

    resultFiles = []

    for folder in resultFolders:
        files = os.listdir("parameters/" + folder)
        for file in files:
            if file.startswith('result'):
                resultFiles.append("parameters/" + folder + "/" + file)

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