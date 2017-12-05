from play import *
from collections import defaultdict

'''
Class for testing multiple runs of the play class. Currently just runs it a 
bunch of times to keep track of the winner. 
'''

features = defaultdict(int)
score = defaultdict(float)
logger = Log("../logs/training_data_log.txt")

weightLogs = {} # Maps from a character number to a Log object

# Initialize the weightLogs to random
# Assume 4 players and initialized weights for all of them regardless of whether they are AI or human
# All are initialized with a placeholder dict that should be overwritten
for i in range(4):
    weightLogs[i] = Log('../logs/WeightLog_%s.txt' % i)
    weightLogs[i].log_dict({'DELETE ME' : -1})

runs = 5000

for i in range(runs):
    print(i)
    play = Play(weightLogs)
    play.main()

    #Get info from the game
    maxScore, bestPlayer = 0, None
    worstScore, worstPlayer = 100, None
    for player in play.players:
        if player.score > maxScore:
            maxScore = player.score
            bestPlayer = player
        if player.score < worstScore:
            worstScore = player.score
            worstPlayer = player

    bestWeights = bestPlayer.weights

    worstPlayer.weightsLog.log_dict({'DELETE ME': -1})

    for player in play.players:
        if player is not bestPlayer and player is not worstPlayer:
            scoreDiff = maxScore - player.score
            updatedWeights = player.update_weights(bestPlayer.feature_extractor(), bestWeights, scoreDiff)
            player.weightsLog.log_dict(updatedWeights)

    # print('devcards = ' + str(player.devCards))

# test_log = Log("test_log.txt")
# test_log.log_dict(winners)
# test_log.log("#######################################################")
# test_log.log_dict(score)
