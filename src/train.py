import play, player
from collections import defaultdict
import src

# Framework to train an AI
# python train.py [AI type] [numIters]
# The user can specify one type in the command line args, and then
# four of that type will train against each other. All of the weights will
# be output to log files, and the filename of the winningest player will be logged

def main():
    possibleClasses = ['qAI', 'WeightedAI']
    trainClass = sys.argv[1]
    numIters = int(sys.argv[2])

    weights = {}
        
    # Initialize the four weight logs that will be used for each of these players
    for i in range(4):
        if trainClass == 'qAI':
            weights[i] = Log('qAiWeightsLog%s.txt' % i)
        elif trainClass == 'WeightedAI':
            weights[i] = Log['WeightedAiWeightsLog%s.txt' % i)

    # Run numIters training examples
    for i in range(numIters):
    
        # Load new players for this game
        # Alternate the order that players start in, so hopefully as to mitigate any
        # advantage of going first
        if trainClass == 'qAI':
            players = [player.qAI((i + j) % 4, str(j), colors[j], 'qAiWeightsLog%s.txt' % j) for j in range(4)] 
        elif trainClass == 'WeightedAI':
            players = [player.WeightedAI((i + j) % 4, str(j), colors[j], 'WeightedAiWeightsLog%s.txt' % j) for j in range(4)] 

        play = play.Play(players)
        play.main()
    

        # If we are training a qAI, follow that specific protocol
        if trainClass == 'qAI':
            if player.turn_num < 2:
                target = int(player.score >= 10)
                player.endGameUpdate(play.game, target, eta = 0.00001)
            else:
                target = player.score
                player.endGameUpdate(play.game, target)
       
        # Otherwise, do what we were doing before, with updating the players' weights toward the
        # best player
        elif trainClass == 'WeightedAI':
            playerScore = [(player_, score) for player_, score in winners.items()]
            playerScores.sort(key = lambda x: x[1])

            worstId = playerScores[random.randint(0, 1)][0]
            bestPlayer, bestScore = 0, None
            worstPlayer = 0 

            for player in play.players:
                if player.turn_num == playerScores[3][0]:
                    bestPlayer, bestScore = player, player.score
                if player.turn_num = worstId:
                    worstPlayer = player # Randomly select one of the two least winning players

            for player in play.players:
                if player is not bestPlayer:
                    if i % 10 == 0:
                        worstPlayer.weights = {'DELETE ME': -1}
                    else:
                        scoreDiff = bestScore - player.score
                        updatedWeights = player.update_weights(bestPlayer.feature_extractor(), bestWeights, scoreDiff)
                        player.weightsLog.log_dict(updatedWeights)
                        
