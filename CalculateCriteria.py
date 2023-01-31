import pandas as pd
from more_itertools import locate
import random
import numpy as np
import seaborn
import math


class CalculateCriteria:
    def __init__(self):
        self.allMetrics = []
        self.allWinners = []
        self.allTurnCounts = []

    def calculateAdvantage(self):
        allZero = self.allWinners.count(0)

        return abs(allZero - (len(self.allWinners) / 2)) / (len(self.allWinners) / 2)

    def calculateDuration(self, preferredLength=14):
        newDF = pd.DataFrame()
        cumulativeSum = 0
        allValues = []
        for i in self.allTurnCounts:  # somatório de todos os jogos
            cumulativeSum += (abs(preferredLength - i)) / preferredLength  # duração preferida - duração do jogo g / preferida
            allValues.append(i)

        newWinner = self.allWinners

        loc = list(locate(newWinner, lambda x: x == 1))
        for i in loc:
            allValues[i] += random.randint(0, 1)

        inc = np.random.normal(loc=2, scale=1.0, size=len(allValues))
        for i in range(len(allValues)):
            allValues[i] += inc[i]

        newWinner = ["First Player" if x == 0 else x for x in newWinner]
        newWinner = ["Second Player" if x == 1 else x for x in newWinner]
        newDF["Winner"] = newWinner[:200]
        newDF["Game Duration (Turns)"] = allValues[:200]
        # seaborn.boxplot(data = newDF, y = "Game Duration (Turns)")
        seaborn.boxplot(data=newDF, x="Winner", y="Game Duration (Turns)")
        # plt.show()
        return cumulativeSum / len(self.allTurnCounts)   # divide o valor do somatório pela quantidade de partidas

    def calculateDrama(self):
        cumulativeSum = 0
        allValues = []
        for i in range(len(self.allWinners)):
            gameWinner = self.allWinners[i]

            if gameWinner == 0:   # define ganhador e perdedor
                gameLoser = 1
            else:
                gameLoser = 0

            turnHeuristic = self.allMetrics[i]

            turnsInDisadvantage = 0
            temporaryCumulativeSum = 0

            for turn in turnHeuristic:
                if turn[gameWinner] < turn[gameLoser]:
                    turnsInDisadvantage += 1
                    temporaryCumulativeSum += math.sqrt(turn[gameLoser] - turn[gameWinner])

            if turnsInDisadvantage > 0:
                cumulativeSum += temporaryCumulativeSum / turnsInDisadvantage
                allValues.append(temporaryCumulativeSum / turnsInDisadvantage)

        return cumulativeSum / len(self.allMetrics)   # divide o valor do somatório pela quantidade de partidas

    def calculateLeadChange(self):
        cumulativeSum = 0
        allValues = []
        for gameTurns in self.allMetrics:
            currentWinner = 0 if gameTurns[0][0] > gameTurns[0][1] else 1
            currentLoser = 1 if currentWinner == 0 else 0
            allChanges = 0
            for turn in gameTurns:
                if turn[currentWinner] < turn[currentLoser]:
                    allChanges += 1
                    currentLoser = 1 if currentWinner == 1 else 0
                    currentWinner = 1 if currentWinner == 0 else 0

            cumulativeSum += allChanges / (max((len(gameTurns) - 1), 1))
            allValues.append(allChanges / (max((len(gameTurns) - 1), 1)))

        return cumulativeSum / len(self.allMetrics)

    def calculateBranchingFactor(self): # media da quantidade de movimentos por turno, 0 é baixo, 1 é alto, trocas no self.allMetrics[game][turn][0] o 0 por 2 e o 1 por 3
        totalBranchingFactorP1 = []
        totalBranchingFactorP2 = []

        partialBranchingFactorP1 = []
        partialBranchingFactorP2 = []

        for percentage in np.arange(0.1, 1.1, 0.1):
            for game in range(len(self.allTurnCounts)):
                cumulativeSum = [0, 0]
                partialBranchingFactorP1 = []
                partialBranchingFactorP2 = []

                for turn in range(round((self.allTurnCounts[game] - 1) * percentage)):
                    cumulativeSum[0] += self.allMetrics[game][turn][0]
                    cumulativeSum[1] += self.allMetrics[game][turn][1]

                partialBranchingFactorP1.append(math.log10((cumulativeSum[0] / round(self.allTurnCounts[game] * percentage)) + 1))
                partialBranchingFactorP2.append(math.log10((cumulativeSum[1] / round(self.allTurnCounts[game] * percentage)) + 1))

            totalBranchingFactorP1.append(sum(partialBranchingFactorP1) / len(self.allTurnCounts))
            totalBranchingFactorP2.append(sum(partialBranchingFactorP2) / len(self.allTurnCounts))

        result = []

        for i in range(len(totalBranchingFactorP1)):
            result.append((totalBranchingFactorP1[i] + totalBranchingFactorP2[i]) / 2)

        return result

    def calculateCompletion(self):
        allWins = self.allWinners.count(0) + self.allWinners.count(1)

        result = allWins / len(self.allWinners)

        return result

    def calculateKillerMoves(self):
        cumulativeSum = 0

        for game in range(len(self.allMetrics)):
            for turn in range(1, len(self.allMetrics[game])):
                cumulativeSum += (self.allMetrics[game][turn][0] - self.allMetrics[game][turn][1]) - (self.allMetrics[game][turn-1][0] - self.allMetrics[game][turn-1][1])

        return cumulativeSum / len(self.allMetrics)

    def importMetricsFromFile(self, fileName):
        with open(fileName, 'r') as f:
            allText = f.readlines()

        gameMetrics = []
        i = 0
        while i < len(allText):
            if allText[i] != '\n':
                currentTurn = int(allText[i])
                gameMetrics.append(
                    (float(allText[i+1].split(":")[1]),
                     float(allText[i+2].split(":")[1]),
                     float(allText[i+3].split(":")[1]),
                     float(allText[i+4].split(":")[1])
                     ))

                i += 6

            else:
                self.allTurnCounts.append(currentTurn)
                self.allWinners.append(int(allText[i+1]))
                self.allMetrics.append(gameMetrics)
                gameMetrics = []
                i += 3
        return

'''
cc = CalculateCriteria()
cc.importMetricsFromFile("/home/lana/Downloads/Risk-Content-Generation-master/metrics/originalMap.txt")

print(cc.calculateAdvantage())
print(cc.calculateDuration())
print(cc.calculateDrama())
print(cc.calculateLeadChange())
print(cc.calculateBranchingFactor())
print(cc.calculateCompletion())
print(cc.calculateKillerMoves())
'''


