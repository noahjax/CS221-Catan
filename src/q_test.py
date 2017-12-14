from play import *
from collections import defaultdict

'''
Class for testing multiple runs of the play class. Currently just runs it a 
bunch of times to keep track of the winner. 
'''

features = defaultdict(int)
score = defaultdict(float)
logger = Log("../logs/q_test.txt")

weightLogs = {}  # Maps from a character number to a Log object

# Initialize the weightLogs to random
# Assume 4 players and initialized weights for all of them regardless of whether they are AI or human
# All are initialized with a placeholder dict that should be overwritten
for i in range(4):
    weightLogs[i] = Log('../logs/q_test_%s.txt' % i)
    weightLogs[i].log_dict({'DELETE ME': -1})

winners = defaultdict(int)  # Map from the player turn index to the number of wins they have had
runs = 100
numWinners = 0
# total_miss = 0

colors = ["orange", "red", "green", "blue"]

#Helper to print percentages nice
def print_win_percentages(winners, numWinners):
    for player, val in winners.items():
        print "Player ", player, " wins: ", float(val)/numWinners



for i in range(runs):

    #Initialize players
    player0 = qAI(0, "qAI_0", "orange", weightLogs[0])
    player1 = qAI(1, "qAI_1", "red", weightLogs[1])
    player2 = qAI(2, "qAI_2", "green", weightLogs[2])
    player3 = qAI(3, "qAI_3", "blue", weightLogs[3])

    players = [player0, player1, player2, player3]

    print "Game number ", (i+1)

    play = Play(players)
    play.main()

    for player in play.players:
        player.endGameUpdate(play.game)
        
        if player.score >= 10:
            winners[player.turn_num] += 1
            numWinners += 1

    print_win_percentages(winners, numWinners)

    


    












   