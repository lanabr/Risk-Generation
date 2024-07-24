import os

class Metrics:
    def __init__(self):
        self.turnCount = 0
        self.listOfHeuristic = []
        self.winner = None

    def addTurn(self, heuristics):
        self.listOfHeuristic.append(heuristics)
        self.turnCount += 1

    def endGame(self, heuristics, winner):
        self.listOfHeuristic.append(heuristics)
        self.winner = winner

    def printMetrics(self):
        for i in range(len(self.listOfHeuristic)):
            print("Turn " + str(i))
            for j in range(len(self.listOfHeuristic[i])):
                print("Player " + str(j+1) + " heuristic: " + str(self.listOfHeuristic[i][j][1]))
                print("Player " + str(j+1) + " move choices: " + str(self.listOfHeuristic[i][j][2]))

            print()

        print()
        print("Winner: " + str(self.winner))

    def appendToFile(self, fileName):
        strToWrite = ""
        for i in range(len(self.listOfHeuristic)):
            strToWrite += str(i)
            strToWrite += "\n"
            for j in range(len(self.listOfHeuristic[i])):
                strToWrite += str(self.listOfHeuristic[i][j][0].playerID) + ": " + str(self.listOfHeuristic[i][j][1])
                strToWrite += "\n"
                strToWrite += str(self.listOfHeuristic[i][j][0].playerID) + ": " + str(self.listOfHeuristic[i][j][2])
                strToWrite += "\n"

            strToWrite += "\n"

        strToWrite += "\n"
        strToWrite += str(self.winner)
        strToWrite += "\n"
        strToWrite += "\n"

        with open(fileName, 'a') as f:
            f.write(strToWrite)
