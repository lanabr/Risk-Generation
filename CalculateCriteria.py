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

    def calculateDuration(self):
        cumulativeSum = 0
        preferredLength = 24

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
            heuristc = []
            for i in range(int(len(self.allMetrics[0][0])/2)):
                heuristc.append(gameTurns[0][i])

            currentWinner = heuristc.index(max(heuristc))
            currentLoser = heuristc.index(min(heuristc))

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
        branchingFactor = []
        for i in range(int(len(self.allMetrics[0][0])/2)):
            branchingFactor.append(0)

        for game in range(len(self.allTurnCounts)):
            cumulativeSum = []
            for i in range(int(len(self.allMetrics[0][0])/2)):
                cumulativeSum.append(0)

            for turn in range(round((self.allTurnCounts[game] - 1))):
                for pl in range(0, len(self.allMetrics[0][0]), 2):
                    cumulativeSum[int(pl/2)] += self.allMetrics[game][turn][pl+1]

            for i in range(len(cumulativeSum)):
                branchingFactor[i] += min(1.0, math.log10((cumulativeSum[i] / (self.allTurnCounts[game])) + 1) / 2)

        result = []
        for i in range(len(branchingFactor)):
            result.append(branchingFactor[i] / len(self.allTurnCounts))

        return sum(result) / len(result)

    def calculateCompletion(self):
        allWins = self.allWinners.count(0) + self.allWinners.count(1)

        result = allWins / len(self.allTurnCounts)

        return result

    def calculateKillerMoves(self):
        cumulativeSum = 0

        for game in range(len(self.allMetrics)):
            gameSum = []

            for turn in range(0, len(self.allMetrics[game]) - 1):
                gameSum.append((self.allMetrics[game][turn][0] - self.allMetrics[game][turn][1]) - (self.allMetrics[game][turn-1][0] - self.allMetrics[game][turn-1][1]))

            if len(gameSum) > 0:
                cumulativeSum += max(gameSum)

        return cumulativeSum / len(self.allMetrics)

    def importMetricsFromFile(self, fileName):
        with open(fileName, 'r') as f:
            allText = f.readlines()

        gameMetrics = []
        i = 0
        while i < len(allText):
            if allText[i] != '\n':
                currentTurn = int(allText[i])
                i = i + 1
                allheuristic = []
                allmoves = []
                while allText[i] != '\n':
                    allheuristic.append(float(allText[i].split(":")[1]))
                    allmoves.append(float(allText[i+1].split(":")[1]))
                    i = i + 2
                for moves in allmoves:
                    allheuristic.append(moves)
                gameMetrics.append(allheuristic)
                i = i + 1
            else:
                self.allTurnCounts.append(currentTurn)
                self.allWinners.append(int(allText[i+1]))
                self.allMetrics.append(gameMetrics)
                gameMetrics = []
                i = i + 3

        return


def run(filename):
    cc = CalculateCriteria()
    cc.importMetricsFromFile(filename)

    print(cc.calculateAdvantage())
    print(cc.calculateDuration())
    print(cc.calculateDrama())
    print(cc.calculateLeadChange())
    print(cc.calculateBranchingFactor())
    print(cc.calculateCompletion())
    print(cc.calculateKillerMoves())

