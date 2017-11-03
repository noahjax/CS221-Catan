from game import *
from pieces import *

def incrementInDict(player, card):
    if card in player.devCards.keys():
        player.devCards[card] += 1
    else:
        player.devCards[card] = 1

class Knight :
    def __init__(self, board, player, players):
        self.player = player
        self.board = board
        self.players = players
        self.player.numKnights += 1
        incrementInDict(self.player, 'Knight')

    ##Definition for a player who wants to use it
    def play(self, board, player):
        ##Not sure how we want to do this yet
        ##Need to figure out how to ask where the player wants to the robber

    ##definition for our AI/ when we know position
    def play(self, board, position):
        Robber.place(board, position)
        for oppPlayer in self.players:
            if not oppPlayer == self.player:
                ##check if other player has piece near robber position
                ##if they do ask them for a card.
                self.player.devCards['Knight'] -= 1

        self.player.numKnights += 1
        if self.player.numKnights >= 3 and self.player.numKnights > Game.currMaxKnights:
            self.player.score += 2
            Game.currMaxKnights = self.player.numKnights


class Victory_Point:
    def __init__(self, player):
        self.player = player
        self.value = 1
        incrementInDict(self.player, 'Victory Point')

    def play(self):
        self.player.incrementScore(1)


class Road_Building:
    def __init__(self, player):
        self.player = player
        incrementInDict(self.player, 'Road Building')
        if self.player.resources['Road'] >= 9 and self.player.resources['Road'] > Game.currMaxRoad:
            Game.currMaxRoad = self.player.resources['Road']
            self.player.incrementScore(2)

    def play(self, board):
        ##Let the player build two roads
        self.player.devCards['Road Building'] -= 1

class Monopoly:
    def __init__(self, player, players):
        self.player = player
        self.players = players
        incrementInDict(self.player, 'Monopoly')

    def play(self, resource):
        for player in self.players:
            if not player == self.player:
                if resource in player.resources:
                    numResources = player.resources[resource]
                    self.player.resources[resource] += numResources
                    self.player.numResources += numResources
                    player.resources[resource] = 0
        self.player.devCards['Monopoly'] -= 1

class Year_Of_Plenty:
    def __init__(self, player, players):
        self.player = player
        self.players = players
        incrementInDict(self.player, 'Year Of Plenty')

    def play(self, resourceOne, resourceTwo):
        self.player.resources[resourceOne] += 1
        self.player.resources[resourceTwo] += 1
        self.player.devCards['Year Of Plenty'] -= 1




