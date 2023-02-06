from Game import Game
from Agents.RuleAgent import RuleAgent
from Structures.PlayerID import PlayerID
from Structures.ValidPlayerColors import ValidPlayerColors
from tqdm import tqdm


def playtestNtimes(gameParameters, numberOfTimes=300, exportFile=True, maxTurnCount=300, maxTime=20):
    for _ in tqdm(range(numberOfTimes)):
        agent1 = RuleAgent(PlayerID("Player1", ValidPlayerColors.BLUE))
        agent2 = RuleAgent(PlayerID("Player2", ValidPlayerColors.RED))

        newGame = Game(showActions=False, parameters=gameParameters, listOfPlayers=[agent1, agent2])
        metrics = newGame.playtest(maxNumberOfTurns=maxTurnCount, maxNumberOfSeconds=maxTime)

        if exportFile:
            metricsFile = "metrics/game" + gameParameters.mapPath[-6] + "-" + gameParameters.goalBasedOn + "-" \
                            + str(gameParameters.troopsWonBeginTurn) + "-" + gameParameters.advantageAttack + "-" \
                            + gameParameters.initialTerritoriesMode + "-" + gameParameters.troopsToNewTerritory + ".txt"
            metrics.appendToFile(metricsFile)
