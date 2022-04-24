## Name: Furkan Goktas Date: 2/9/2022
## Assignment: Module 5 &6: Project - Adversarial Search  Due Date: 2/13/2022
## About this project: The goal of the game is to avoid taking the last object.
## Computer selects its next moved using an Alpha-beta pruning algorithm.
## Assumptions: The program assumes user input will be string.
## The computer moves are getting slower if the pile number is high (pileNumber > 5 is calculating very slowly)
## References: The games.py file provided on Canvas

import random
from collections import namedtuple

import numpy as np
from utils import *

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


def minmax_decision(state, game):
    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


# Search game to determine best action; use alpha-beta pruning.
def alpha_beta_search(state, game):
    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def query_player(game, state):
    # print("current state:")
    # game.display(state)
    # print("available moves: {}".format(game.actions(state)))

    # display board
    print("-" * 25)
    for i in range(0, len(state.board)):
        print('Pile {}: {}'.format(i + 1, 'O' * state.board[i]))
    print("-" * 25)

    move = None
    if game.actions(state):
        while True:
            stones = int(input('How many stones to remove: '))
            piles = int(input('Pick a pile to remove from: '))

            move = (piles - 1, stones)
            # print(move)
            # If all conditions for input are CORRECT, break out of the while loop
            if (int(stones) > 0) and (int(piles) <= len(state.board)) and (int(piles) > 0):
                if int(stones) <= state.board[int(piles) - 1]:
                    if (int(stones) != 0) and (int(piles) != 0):
                        break
            # If not, display this statement
            print("Hmmm. you entered an invalid value. Please try again.")

    return move


def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)


def minmax_player(game, state):
    return minmax_decision(state, game)


def create_board(rockList, randPile):
    # create board
    for i in range(0, randPile):
        randRock = random.randint(1, 8)
        rockList.append(randRock)
    print("-" * 25)


if __name__ == "__main__":

    # Define an empty rocklist to append rocks to, define random integers, call functions
    rockList = []

    # random number of rock piles
    randPile = random.randint(2, 5)

    # random number of rocks
    randRock = random.randint(1, 9)

    create_board(rockList, randPile)
    playerName = input('What is the player name: ')
    nim = GameOfNim(board=rockList)

    utility = nim.play_game(query_player, alpha_beta_player)  # computer moves first

    if utility < 0:
        print("Computer is the winner :'(")
    else:
        print(f"{playerName} is the winner :)")
