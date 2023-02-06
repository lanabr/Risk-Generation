from Game import Game
from Metrics import Metrics
from Parameters import Parameters
from Agents.RuleAgent import RuleAgent
from Structures.PlayerID import PlayerID
from Structures.ValidPlayerColors import ValidPlayerColors
#from tqdm import tqdm


class AutomatedPlaytest():
    def __init__(self, parametersFile="parameters/map8test.json", metricsFile="map8test"):
        self.parametersFile = parametersFile
        self.groupOfMetrics = []
        self.metricsFile = "metrics/" + metricsFile + ".txt"

    def playtestNtimes(self, gameParameters, numberOfTimes=100, exportFile=True, maxTurnCount=300, maxTime=20):
        for i in range(numberOfTimes):
            agent1 = RuleAgent(PlayerID("Player1", ValidPlayerColors.BLUE))
            agent2 = RuleAgent(PlayerID("Player2", ValidPlayerColors.RED))

            newGame = Game(showActions=False, parameters=gameParameters, listOfPlayers=[agent1, agent2])
            metrics = newGame.playtest(maxNumberOfTurns=maxTurnCount, maxNumberOfSeconds=maxTime)
            self.groupOfMetrics.append(metrics)

            if exportFile:
                self.metricsFile = "metrics/game" + str(i) + ".txt"
                metrics.appendToFile(self.metricsFile)


for g in ["cards", "all"]:
    goalBasedOn = g

    for tw in [1, 2, 3, 4, 5]:
        troopsWonBeginTurn = tw

        for a in ["attack", "defense"]:
            advantageAttack = a

            for i in ["random", "pick"]:
                initialTerritoriesMode = i

                for tt in ["min", "max"]:
                    troopsToNewTerritory = tt
                    parameters = Parameters("C:/Users/LanaR/PycharmProjects/Risk-Generation/parameters/map.json", goalBasedOn, troopsWonBeginTurn, advantageAttack, initialTerritoriesMode, troopsToNewTerritory)

                    AutomatedPlaytest().playtestNtimes(parameters)
