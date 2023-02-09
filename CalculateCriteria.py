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
        cumulativeSum = 0

        for i in self.allTurnCounts:  # somatório de todos os jogos
            cumulativeSum += (abs(preferredLength - i)) / preferredLength  # duração preferida - duração do jogo g / preferida

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

    def calculateBranchingFactor(self): # media da quantidade de movimentos por turno, 0 é baixo, 1 é alto
        branchingFactorP1 = 0
        branchingFactorP2 = 0

        for game in range(len(self.allTurnCounts)):
            cumulativeSum = [0, 0]

            for turn in range(round((self.allTurnCounts[game] - 1))):
                cumulativeSum[0] += self.allMetrics[game][turn][2]
                cumulativeSum[1] += self.allMetrics[game][turn][3]

            branchingFactorP1 += min(1.0, math.log10((cumulativeSum[0] / self.allTurnCounts[game]) + 1) / 2)
            branchingFactorP2 += min(1.0, math.log10((cumulativeSum[1] / self.allTurnCounts[game]) + 1) / 2)

        resultP1 = branchingFactorP1 / len(self.allTurnCounts)
        resultP2 = branchingFactorP2 / len(self.allTurnCounts)

        return (resultP1 + resultP2) / 2

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
cc.importMetricsFromFile("/home/lana/PycharmProjects/Risk-Generation/metrics/game1-1-attack-pick-min.txt")

print(cc.calculateBranchingFactor())

print(cc.calculateAdvantage())
print(cc.calculateDuration())
print(cc.calculateDrama())
print(cc.calculateLeadChange())

print(cc.calculateCompletion())
print(cc.calculateKillerMoves())
'''


