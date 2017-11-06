from game import *
from pieces import *


def buyDevCard(player, type, players):
    if type == 'Knight':
        return Knight(player, players)
    elif type == 'Victory Point':
        return Victory_Point(player)
    elif type == 'Monopoly':
        return Monopoly(player, players)
    elif type == 'Road Building':
        return Road_Building(player)
    elif type == 'Year of Plenty':
        return Year_Of_Plenty(player, players)


class Knight :
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.player.numKnights += 1

    ##Definition for a player who wants to use it
    def play(self, board, player):
        ##Not sure how we want to do this yet
        ##Need to figure out how to ask where the player wants to the robber
        return True

    ##definition for our AI/ when we know position
    def play(self, board, position):
        Robber.place(board, position)
        for oppPlayer in self.players:
            if not oppPlayer == self.player:
                ##check if other player has piece near robber position
                ##if they do ask them for a card.
                continue

        self.player.numKnights += 1
        if self.player.numKnights >= 3 and self.player.numKnights > Game.currMaxKnights:
            self.player.score += 2
            Game.currMaxKnights = self.player.numKnights


class Victory_Point:
    def __init__(self, player):
        self.player = player
        self.value = 1

    def play(self):
        self.player.incrementScore(1)


class Road_Building:
    def __init__(self, player):
        self.player = player
        if self.player.pieces['Road'] >= 9 and self.player.pieces['Road'] > Game.currMaxRoad:
            Game.currMaxRoad = self.player.resources['Road']
            self.player.incrementScore(2)

    def play(self, board):
        ##Let the player build two roads
        return True


class Monopoly:
    def __init__(self, player, players):
        self.player = player
        self.players = players

    def play(self, resource):
        for player in self.players:
            if not player == self.player:
                if resource in player.resources:
                    numResources = player.resources[resource]
                    self.player.resources[resource] += numResources
                    self.player.numResources += numResources
                    player.resources[resource] = 0

class Year_Of_Plenty:
    def __init__(self, player, players):
        self.player = player
        self.players = players

    def play(self, resourceOne, resourceTwo):
        self.player.resources[resourceOne] += 1
        self.player.resources[resourceTwo] += 1




