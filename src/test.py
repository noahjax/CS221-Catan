from play import *
from collections import defaultdict

'''
Class for testing multiple runs of the play class. Currently just runs it a 
bunch of times to keep track of the winner. 
'''

winners = defaultdict(int)
score = defaultdict(float)

runs = 500
for i in range(runs):
    print(i)
    play = Play()
    play.main()

    #Get info from the game
    for i, player in enumerate(play.players):
        # if i == 0: print player.resource_weights
        score[i] += float(player.score)/ runs
        if player.score == 10:
            winners[i] += 1./runs

print winners
print score

# test_log = Log("test_log.txt")
# test_log.log_dict(winners)
# test_log.log("#######################################################")
# test_log.log_dict(score)
