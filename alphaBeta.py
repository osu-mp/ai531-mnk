from copy import deepcopy
import random
import time
from util import get_other_player
from board import Board
ab_time_filename = 'abTime.txt'

# timeFile_for_ab = open("abTime.txt", 'w')

#Player saved in the file from bot_Move
def save_player(player):
    f = open('cur_player.txt', 'w')
    f.write(str(player))
    f.close()
# Player retrived from the file
def get_player():
    f = open('cur_player.txt', 'r')
    player = int(f.readline())
    f.close()
    return player

def alphaBeta(position: Board, depth, alpha, beta, player, previousMove):
    if position.is_gameover(previousMove, get_other_player(player)) or depth == 0:
        activePlayer = get_player()
        if activePlayer == 2:
            return position.winner * (-1)
        elif activePlayer == 1:
            return position.winner
        return 0

    for i in position.get_empty_squares():
        positionCopy = deepcopy(position)
        positionCopy.make_move(i, player)
        # recursive call with a deepcopy of the position, opposing player, and the updated move or i
        val = alphaBeta(positionCopy, depth-1, alpha, beta, get_other_player(player), i)
        # If player is alpha
        if player ==  get_player():
            if alpha > val:
                # update max alpha
                alpha = val
            if alpha >= beta:
                return beta
            if beta < val:
                # update min alpha
                beta = val
            if beta <= alpha:
                return alpha
    if player == get_player():
        return alpha
    else:
        return beta

def ab_bot(position:Board, player):
    a = -2
    moveChoices = []

   # if len(position.get_empty_squares()) == position.size[][] ** 2: # best 1st move
    #    return position.size[1] ** 2 // 2 + 1

    players = [0,1,2]
    for move in position.get_empty_squares():
        clone = deepcopy(position)
        clone.make_move(move, player)
        val = alphaBeta(clone, 4, -2, 2, get_other_player(player), move)
        print("move", move, "causes player", players[val], "to win")
        if val > a:
            a = val
            moveChoices = [move]
        elif val == a:
            moveChoices.append(move)
    return random.choice(moveChoices)

def bot_move(position: Board, player, algoType):
    save_player(player)
    # This check is only there to ensure that the correct parameter(i.e ab) is passed
    if algoType == 'ab':
        start = time.time()
        move = ab_bot(position, player)
        end = time.time()
        #Reccods time by creating a new file
        with open(ab_time_filename, 'w+') as timeFile_for_ab:
            timeFile_for_ab.write(str(end - start) + '\n')
    return move

"""
Endpoint: Call obj.bot_move(1: position/board, 1/-1 depending on the player you want to go first, always 'ab')
"""