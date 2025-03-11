from Game import Game
from Agents.RuleAgent import RuleAgent
from Structures.PlayerID import PlayerID
from Structures.ValidPlayerColors import ValidPlayerColors
from tqdm import tqdm


def playtestNtimes(gameParameters, numberOfTimes=100, exportFile=True, maxTurnCount=48, maxTime=20, path="parameters"):
    for _ in tqdm(range(numberOfTimes)):
        agent1 = RuleAgent(PlayerID("Player1", ValidPlayerColors.BLUE))
        agent2 = RuleAgent(PlayerID("Player2", ValidPlayerColors.RED))
        agent3 = RuleAgent(PlayerID("Player3", ValidPlayerColors.GREEN))

        newGame = Game(showActions=False, parameters=gameParameters, listOfPlayers=[agent1, agent2, agent3])
        metrics = newGame.playtest(maxNumberOfTurns=maxTurnCount, maxNumberOfSeconds=maxTime)

        if exportFile:
            metricsFile = path + "/game" + str(gameParameters.troopsWonBeginTurn) + "-" + str(gameParameters.defenseDices) + "-" \
                            + gameParameters.initialTerritoriesMode + "-" + gameParameters.troopsToNewTerritory + ".txt"
            metrics.appendToFile(metricsFile)
