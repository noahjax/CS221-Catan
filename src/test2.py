from play import *
from collections import defaultdict

raise Exception('DO NOT USE THIS FILE')

'''
Class for testing multiple runs of the play class. Currently just runs it a 
bunch of times to keep track of the winner. 
'''

features = defaultdict(int)
score = defaultdict(float)
logger = Log("../logs/training_data_log.txt")

weightLogs = {}  # Maps from a character number to a Log object

# Initialize the weightLogs to random
# Assume 4 players and initialized weights for all of them regardless of whether they are AI or human
# All are initialized with a placeholder dict that should be overwritten


for i in range(4):
    if i == 0:
        weightLogs[i] = Log('../logs/WeightLog_2.txt')
    if i != 0:
        weightLogs[i] = Log('../logs/WeightLog_unimp_%s.txt' % i)
        weightLogs[i].log_dict({'DELETE ME': -1})


winners = {}  # Map from the player turn index to the number of wins they have had
runs = 50 
numWinners = 0

for i in range(runs):
    print(i)
    play = Play(weightLogs)
    play.main()

    if not winners:
        for player in play.players:
            winners[player.turn_num] = 0

    for player in play.players:
        if player.score == 10:
            numWinners += 1
            print "Currently have had this many winners: ", numWinners
            winners[player.turn_num] += 1
            print(player.color + ' wins')
    '''
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
    '''
    # Get info from the game
    # '''
    # maxScore, bestPlayer = 0, None
    # worstScore, worstPlayer = 100, None
    # for player in play.players:
    #     if player.score > maxScore:
    #         maxScore = player.score
    #         bestPlayer = player
    #     if player.score < worstScore:
    #         worstScore = player.score
    #         worstPlayer = player
    # '''
    # Randomly select one of the two least winning players to be cut
    '''
    bestWeights = bestPlayer.weights

    if i % 10 == 0:
        worstPlayer.weights = {'DELETE ME': -1}

    for player in play.players:
        if player is not bestPlayer:
            if i%10 == 0 and player == worstPlayer: continue
            scoreDiff = bestScore - player.score
            updatedWeights = player.update_weights(bestPlayer.feature_extractor(), bestWeights, scoreDiff)
            player.weightsLog.log_dict(updatedWeights)
    '''
    print(winners)
    print('num Winners = ' + str(numWinners))
# test_log = Log("test_log.txt")
# test_log.log_dict(winners)
# test_log.log("#######################################################")
# test_log.log_dict(score)
