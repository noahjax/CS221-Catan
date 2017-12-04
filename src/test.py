from play import *
from collections import defaultdict

'''
Class for testing multiple runs of the play class. Currently just runs it a 
bunch of times to keep track of the winner. 
'''

features = defaultdict(int)
score = defaultdict(float)
logger = Log("../logs/training_data_log.txt")

runs = 1
for i in range(runs):
    print('i = ' + str(i))
    play = Play()
    play.main()

    #Get info from the game
    for player in play.players:
        features = player.feature_extractor()
        score = player.score
        logger.log_dict_second(features, score)
    

# test_log = Log("test_log.txt")
# test_log.log_dict(winners)
# test_log.log("#######################################################")
# test_log.log_dict(score)
