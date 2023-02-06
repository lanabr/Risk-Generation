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
            print("Player 1 heuristic: " + str(self.listOfHeuristic[i][0]))
            print("Player 1 move choices: " + str(self.listOfHeuristic[i][2]))
            print("Player 2 heuristics: " + str(self.listOfHeuristic[i][1]))
            print("Player 2 move choices: " + str(self.listOfHeuristic[i][3]))

            print()

        print()
        print("Winner: " + str(self.winner))

    def appendToFile(self, fileName):
        strToWrite = ""
        for i in range(len(self.listOfHeuristic)):
            strToWrite += str(i)
            strToWrite += "\n"
            strToWrite += "0:" + str(self.listOfHeuristic[i][0])
            strToWrite += "\n"
            strToWrite += "1:" + str(self.listOfHeuristic[i][1])
            strToWrite += "\n"
            strToWrite += "0:" + str(self.listOfHeuristic[i][2])
            strToWrite += "\n"
            strToWrite += "1:" + str(self.listOfHeuristic[i][3])
            strToWrite += "\n"

            strToWrite += "\n"

        strToWrite += "\n"
        strToWrite += str(self.winner)
        strToWrite += "\n"
        strToWrite += "\n"

        with open(fileName, 'a') as f:
            f.write(strToWrite)
