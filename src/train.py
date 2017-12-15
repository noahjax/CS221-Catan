from play import *
from player import *
from log import *
from collections import defaultdict
import sys 
import numpy as np

# Framework to train an AI
# python train.py [AI type] [numIters]
# The user can specify one type in the command line args, and then
# four of that type will train against each other. All of the weights will
# be output to log files, and the filename of the winningest player will be logged

def main():

    colors = ['orange', 'red', 'green', 'blue']

    possibleClasses = ['qAI', 'WeightedAI', 'qAI_win', 'qAI_minimax']
    trainClass = sys.argv[1]
    numIters = int(sys.argv[2])
    
    assert trainClass in possibleClasses
    
    weights = {}
        
    # Initialize the four weight logs that will be used for each of these players
    for i in range(4):
        if trainClass == 'qAI':
            weights[i] = Log('qAiWeightsLog%s.txt' % i)
        elif trainClass == 'WeightedAI':
            weights[i] = Log('WeightedAiWeightsLog%s.txt' % i)
        elif trainClass == 'qAIWin':
            weights[i] = Log('qAi_win_WeightsLog%s.txt' % i) 
        elif trainClass == 'qAI_minimax':
            weights[i] = Log('qAi_minimax_WeightsLog%s.txt' % i) 
        weights[i].log_dict({'DELETE ME': -1})

    # Give each a default win, just so as to avoid errors later
    winners = defaultdict(int) 
    for i in range(4):
        winners[i] = 1

    # Run numIters training examples
    for i in range(numIters):
        print(i)
        # In order to switch up the turn order, each player will randomly draw from this array
        # to determine their order
        nums = [0, 1, 2, 3]

        # Load new players for this game
        # Alternate the order that players start in, so hopefully as to mitigate any
        # advantage of going first
        if trainClass == 'qAI':
            players = [qAI(nums.pop(random.randint(0, len(nums) - 1)), str(j), colors[j], weights[j]) for j in range(4)] 
        elif trainClass == 'WeightedAI':
            players = [WeightedAI(nums.pop(random.randint(0, len(nums) - 1)), str(j), colors[j], weights[j]) for j in range(4)] 
        elif trainClass == 'qAI_win':
            players = [qAI_win(nums.pop(random.randint(0, len(nums) - 1)), str(j), colors[j], weights[j]) for j in range(4)] 
        elif trainClass == 'qAI_minimax':
            players = [qAI_minimax(nums.pop(random.randint(0, len(nums) - 1)), str(j), colors[j], weights[j]) for j in range(4)] 
             
        players.sort(key = lambda p: p.turn_num)
        play = Play(players)
        play.main()
   
        for player in play.players:
            if player.score >= 10:
                winners[int(player.name)] += 1

        # If we are training a qAI, follow that specific protocol
        if trainClass == 'qAI' or trainClass == 'qAI_win' or trainClass == 'qAI_minimax':
            for player in play.players:
                player.endGameUpdate(play.game)
           
        # Otherwise, do what we were doing before, with updating the players' weights toward the
        # best player
        elif trainClass == 'WeightedAI':
            playerScores = [(player_, score) for player_, score in winners.items()]
            playerScores.sort(key = lambda x: x[1])
            worstId = playerScores[random.randint(0, 1)][0]
            bestPlayer, bestScore = None, 0 
            worstPlayer = None 
        
            for player in play.players:
                if player.turn_num == playerScores[3][0]:
                    bestPlayer, bestScore = player, player.score
                if player.turn_num == worstId:
                    worstPlayer = player # Randomly select one of the two least winning players
          
            assert bestPlayer is not None
            assert worstPlayer is not None
            bestWeights = bestPlayer.weights

            for player in play.players:
                if player is not bestPlayer:
                    if i % 10 == 0:
                        worstPlayer.weights = {'DELETE ME': -1}
                    else:
                        scoreDiff = bestScore - player.score
                        updatedWeights = player.update_weights(bestPlayer.feature_extractor(), bestWeights, scoreDiff)
                        player.weightsLog.log_dict(updatedWeights)
   
    # Pull out the player who won the largest number of games
    # Can modify this if we want access to the others as well
    winningestPlayer = None
    for k, v in winners.items():
        if v == max(winners.values()):
            winningestPlayer = k
            break
    assert winningestPlayer is not None
    bestWeights = Log('bestWeights.txt')
    bestWeights.log_dict(weights[winningestPlayer].readDict())

    print('finished')

if __name__ == '__main__':
    main()
