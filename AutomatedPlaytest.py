from Game import Game
from Agents.RuleAgent import RuleAgent
from Structures.PlayerID import PlayerID
from Structures.ValidPlayerColors import ValidPlayerColors
from tqdm import tqdm
from Parameters import Parameters
from CalculateCriteria import run
import os


def playtestNtimes(gameParameters, numberOfTimes=10, exportFile=True, maxTurnCount=48, maxTime=20):
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
game = Parameters("/home/lana/PycharmProjects/Risk-Generation/parameters/map125.json", 3, "defense", "random", "max")
playtestNtimes(game)
run("/home/lana/PycharmProjects/Risk-Generation/metrics/game3-defense-random-max.txt")
#os.remove("metrics/game3-attack-pick-min.txt")
'''
