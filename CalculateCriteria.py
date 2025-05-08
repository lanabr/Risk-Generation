import pandas as pd
from more_itertools import locate
import random
import numpy as np
import seaborn
import math
from collections import Counter

from networkx.utils.random_sequence import cumulative_distribution


class CalculateCriteria:
    def __init__(self):
        self.allHeuristic = []
        self.allMoves = []
        self.allWinners = []
        self.allTurnCounts = []

    def calculateCompletion(self):
        values, counts = np.unique(self.allWinners, return_counts=True)

        allWins = len(self.allWinners)
        if -1 in values:
            allWins = allWins - counts[locate(values, -1)]

        result = allWins / len(self.allTurnCounts)

        return result

    def calculateAdvantage(self):
        winnerCount = Counter(self.allWinners)

        winner = max(winnerCount)
        loser = min(winnerCount)

        diff = winnerCount[winner] - winnerCount[loser]
        rate = diff / len(self.allWinners)

        return rate

    def calculateMovement(self): # todo: quando o jogador foi eliminado, como passar pro outro jogador? faz a passagem por uma lista?
        cumulativeSum = []
        for player in range(len(self.allMoves[0][0])):
            cumulativeSum.append([])

        for game in range(len(self.allMoves)):
            playersMoves = []
            for player in range(len(self.allMoves[game][0])):
                playersMoves.append(0)

            player = 0
            for turn in range(len(self.allMoves[game])):
                if self.allMoves[game][turn][player] > 1:
                    playersMoves[player] += 1
                else:
                    if self.allMoves[game][turn][player] == 0 and self.allHeuristic[game][turn][player] == 0.0:
                        playersMoves[player] += 1

                player += 1
                if player >= len(self.allMoves[game][turn]):
                    player = 0

            for player in range(len(playersMoves)):
                cumulativeSum[player].append(playersMoves[player] / self.allTurnCounts[game])

        resultPerPlayer = []
        for player in cumulativeSum:
            resultPerPlayer.append(sum(player) / len(player))

        result = sum(resultPerPlayer) / len(resultPerPlayer)

        return result

    def calculateDuration(self):
        cumulativeSum = 0
        preferredLength = 24

        for i in self.allTurnCounts:  # somatório de todos os jogos
            cumulativeSum += (abs(preferredLength - i)) / preferredLength  # duração preferida - duração do jogo g / preferida

        return cumulativeSum / len(self.allTurnCounts)   # divide o valor do somatório pela quantidade de partidas

    def calculateDrama(self):
        cumulativeSum = 0

        for i in range(len(self.allWinners)):
            gameWinner = self.allWinners[i]
            if gameWinner == -1:
                continue
            gameWinner -= 1

            gameLosers = []

            for player in range(0, len(self.allHeuristic[i][0])):
                if player != gameWinner:
                    gameLosers.append(player)

            turnHeuristic = self.allHeuristic[i]

            turnsInDisadvantage = 0
            temporaryCumulativeSum = 0

            for turn in turnHeuristic:
                for gameLoser in gameLosers:
                    if turn[gameWinner] < turn[gameLoser]:
                        turnsInDisadvantage += 1
                        temporaryCumulativeSum += math.sqrt(turn[gameLoser] - turn[gameWinner])

            if turnsInDisadvantage > 0:
                cumulativeSum += temporaryCumulativeSum / turnsInDisadvantage

        return cumulativeSum / len(self.allHeuristic)   # divide o valor do somatório pela quantidade de partidas

    def calculateLeadChange(self):
        cumulativeSum = 0
        for game in self.allHeuristic:
            currentWinner = game[0].index(max(game[0]))

            currentLosers = []
            for player in range(0, len(game[0])):
                if player != currentWinner:
                    currentLosers.append(player)

            allChanges = 0
            for turn in game:
                if max(turn) != turn[currentWinner]:
                    allChanges += 1
                    currentLosers.append(currentWinner)
                    currentWinner = turn.index(max(turn))

            cumulativeSum += allChanges / (max((len(game) - 1), 1))

        return cumulativeSum / len(self.allHeuristic)

    def calculateBranchingFactor(self): # media da quantidade de movimentos por turno, 0 é baixo, 1 é alto
        branchingFactor = []
        for i in range(int(len(self.allMoves[0][0]))):
            branchingFactor.append(0)

        for game in range(len(self.allTurnCounts)):
            cumulativeSum = []
            for i in range(int(len(self.allMoves[0][0]))):
                cumulativeSum.append(0)

            for turn in range(round((self.allTurnCounts[game] - 1))):
                for pl in range(0, len(self.allMoves[0][0])):
                    cumulativeSum[pl] += self.allMoves[game][turn][pl]

            for i in range(len(cumulativeSum)):
                branchingFactor[i] += min(1.0, math.log10((cumulativeSum[i] / (self.allTurnCounts[game])) + 1) / 2)

        result = []
        for i in range(len(branchingFactor)):
            result.append(branchingFactor[i] / len(self.allTurnCounts))

        return sum(result) / len(result)

    def calculateKillerMovesAll(self):
        cumulativeSum = 0

        for game in range(len(self.allHeuristic)):
            gameSum = []

            for turn in range(1, len(self.allHeuristic[game]) - 1):
                for pl in range(len(self.allHeuristic[0][0])):
                    for op in range(pl+1, len(self.allHeuristic[0][0])):
                        gameSum.append((self.allHeuristic[game][turn][pl] - self.allHeuristic[game][turn][op]) - (self.allHeuristic[game][turn-1][pl] - self.allHeuristic[game][turn-1][op]))

            if len(gameSum) > 0:
                cumulativeSum += max(gameSum)

        return cumulativeSum / len(self.allHeuristic)

    def calculateKillerMovesWinner(self):
        cumulativeSum = 0

        for game in range(len(self.allHeuristic)):
            gameSum = []

            for turn in range(1, len(self.allHeuristic[game]) - 1):
                for op in range(len(self.allHeuristic[0][0])):
                    gameSum.append((self.allHeuristic[game][turn][self.allWinners[game]] - self.allHeuristic[game][turn][op]) - (self.allHeuristic[game][turn-1][self.allWinners[game]] - self.allHeuristic[game][turn-1][op]))

            if len(gameSum) > 0:
                cumulativeSum += max(gameSum)

        return cumulativeSum / len(self.allHeuristic)

    def calculateKillerMovesPlayer(self):
        cumulativeSum = 0

        for game in range(len(self.allHeuristic)):
            gameSum = []

            for turn in range(1, len(self.allHeuristic[game]) - 1):
                for pl in range(len(self.allHeuristic[0][0])):
                    gameSum.append(self.allHeuristic[game][turn][pl] - self.allHeuristic[game][turn-1][pl])

            if len(gameSum) > 0:
                cumulativeSum += max(gameSum)

        return cumulativeSum / len(self.allHeuristic)

    def calculateKillerMovesBestAnt(self):
        cumulativeSum = 0

        for game in range(len(self.allHeuristic)):
            gameSum = []

            for turn in range(1, len(self.allHeuristic[game]) - 1):
                bestAnt = 0
                bestValue = -1
                for pl in range(len(self.allHeuristic[0][0])):
                    if self.allHeuristic[game][turn-1][pl] > bestValue:
                        bestValue = self.allHeuristic[game][turn][pl]
                        bestAnt = pl
                for op in range(len(self.allHeuristic[0][0])):
                    if op != bestAnt:
                        gameSum.append((self.allHeuristic[game][turn][bestAnt] - self.allHeuristic[game][turn][op]) - (self.allHeuristic[game][turn-1][bestAnt] - self.allHeuristic[game][turn-1][op]))

            if len(gameSum) > 0:
                cumulativeSum += max(gameSum)

        return cumulativeSum / len(self.allHeuristic)

    def calculateKillerMovesBestAtual(self):
        cumulativeSum = 0

        for game in range(len(self.allHeuristic)):
            gameSum = []

            for turn in range(1, len(self.allHeuristic[game]) - 1):
                bestAnt = 0
                bestValue = -1
                for pl in range(len(self.allHeuristic[0][0])):
                    if self.allHeuristic[game][turn][pl] > bestValue:
                        bestValue = self.allHeuristic[game][turn][pl]
                        bestAnt = pl
                for op in range(len(self.allHeuristic[0][0])):
                    if op != bestAnt:
                        gameSum.append((self.allHeuristic[game][turn][bestAnt] - self.allHeuristic[game][turn][op]) - (self.allHeuristic[game][turn - 1][bestAnt] - self.allHeuristic[game][turn - 1][op]))

            if len(gameSum) > 0:
                cumulativeSum += max(gameSum)

        return cumulativeSum / len(self.allHeuristic)

    def importMetricsFromFile(self, fileName):
        with open(fileName, 'r') as f:
            allText = f.readlines()

        gameHeuristic = []
        gameMoves = []
        i = 0
        numPlayers = allText[i]
        i = i + 1
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
                gameHeuristic.append(allheuristic)
                gameMoves.append(allmoves)
                i = i + 1
            else:
                self.allTurnCounts.append(currentTurn)
                self.allWinners.append(int(allText[i+1]))
                self.allHeuristic.append(gameHeuristic)
                self.allMoves.append(gameMoves)
                gameHeuristic = []
                gameMoves = []
                i = i + 4

        return


def run(filename):
    cc = CalculateCriteria()
    cc.importMetricsFromFile("/home/lana/Documentos/Risk-Generation/" + filename)

    print("Movement:", cc.calculateMovement())
    """"
    print("Completion:", cc.calculateCompletion())
    print("Advantage:", cc.calculateAdvantage())
    
    print("Duration:", cc.calculateDuration())
    print("Drama:", cc.calculateDrama())
    print("Lead Change:", cc.calculateLeadChange())
    print("Branching Factor:", cc.calculateBranchingFactor())
    print("Killer Moves AllxAll:", cc.calculateKillerMovesAll())
    print("Killer Moves WinnerxAll:", cc.calculateKillerMovesWinner())
    print("Killer Moves BestAntxAll:", cc.calculateKillerMovesBestAnt())
    print("Killer Moves BestAtualxAll:", cc.calculateKillerMovesBestAtual())
    print("Killer Moves Player:", cc.calculateKillerMovesPlayer())
    """

run("parameters/game3-2-random-min.txt")