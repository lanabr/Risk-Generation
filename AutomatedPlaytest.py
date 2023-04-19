from Game import Game
from Agents.RuleAgent import RuleAgent
from Structures.PlayerID import PlayerID
from Structures.ValidPlayerColors import ValidPlayerColors
from tqdm import tqdm
from Parameters import Parameters
from CalculateCriteria import run
import os


def playtestNtimes(gameParameters, numberOfTimes=100, exportFile=True, maxTurnCount=48, maxTime=20):
    for _ in tqdm(range(numberOfTimes)):
        agent1 = RuleAgent(PlayerID("Player1", ValidPlayerColors.BLUE))
        agent2 = RuleAgent(PlayerID("Player2", ValidPlayerColors.RED))

        newGame = Game(showActions=False, parameters=gameParameters, listOfPlayers=[agent1, agent2])
        metrics = newGame.playtest(maxNumberOfTurns=maxTurnCount, maxNumberOfSeconds=maxTime)

        if exportFile:
            metricsFile = "metrics/game" + str(gameParameters.troopsWonBeginTurn) + "-" + str(gameParameters.defenseDices) + "-" \
                            + gameParameters.initialTerritoriesMode + "-" + gameParameters.troopsToNewTerritory + ".txt"
            metrics.appendToFile(metricsFile)


'''
game = Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map6.json", 2, 2, "random", "min")
playtestNtimes(game)
run("/home/lana/PycharmProjects/Risk-Generation/metrics/game3-2-random-min.txt")
#os.remove("metrics/game3-attack-pick-min.txt")
'''
