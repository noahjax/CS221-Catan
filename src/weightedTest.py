from play import *
from collections import defaultdict

'''
Class for testing multiple runs of the play class. Currently just runs it a 
bunch of times to keep track of the winner. 
'''

features = defaultdict(int)
score = defaultdict(float)
logger = Log("../logs/training_data_log.txt")

colors = ['orange', 'red', 'green', 'blue']

weightLogs = {}  # Maps from a character number to a Log object
players = []
for i in range(4):
    weightLogs[i] = Log('../logs/WeightedAIPlayer%s.txt' % i)
    if i != 2:
        weightLogs[i].log_dict({'DELETE ME': -1})
    players.append(WeightedAI(i, 'WeightedAI%s' % i, colors[i], weightLogs[i]))

winners = {}  # Map from the player turn index to the number of wins they have had
runs = 50 
numWinners = 0

for i in range(runs):
    play = Play(players)
    play.main()

    if not winners:
        for player in play.players:
            winners[player.turn_num] = 0

    #Print numWinners
    for player in play.players:
        if player.score >= 10:
            numWinners += 1
            print "Currently have had this many winners: ", numWinners
            winners[player.turn_num] += 1
            print(player.color + ' wins')

    playerScores = [(player_, score) for player_, score in winners.items()]
    playerScores.sort(key = lambda x: x[1])

    worstId = playerScores[random.randint(0, 1)][0]
    bestPlayer, bestScore = 0, None
    worstPlayer = 0
    for player in play.players:
        if player.turn_num == playerScores[3][0]:
            bestPlayer, bestScore = player, player.score
        if player.turn_num == worstId:
            worstPlayer = player # Randomly select one of the two least winning players
    bestWeights = bestPlayer.weights
    #if i % 10 == 0:
    #    worstPlayer.weights = {'DELETE ME': -1}

    for player in play.players:
        if player is not bestPlayer:
            if i%10 == 0 and player == worstPlayer: continue
            scoreDiff = bestScore - player.score
            updatedWeights = player.update_weights(bestPlayer.feature_extractor(), bestWeights, scoreDiff)
            player.weightsLog.log_dict(updatedWeights)

    # print('num Winners = ' + str(numWinners))

# test_log = Log("test_log.txt")
# test_log.log_dict(winners)
# test_log.log("#######################################################")
# test_log.log_dict(score)
