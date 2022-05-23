from copy import deepcopy
import random
import time
fout_ab = open("ab_time.txt", 'w')
# For diver/testing
def get_player():
    f = open('cur_player.txt', 'r')
    player = int(f.readline())
    return player

def get_oppossing_player(player):
    if player == -1:
        return 1
    return -1

def alphaBeta(position, depth, alpha, beta, player, previousMove):
    if position.is_gameover(previousMove, get_oppossing_player(player)) or depth == 0:
        activePlayer = get_player()
        if activePlayer == -1:
            return position.winner() * (-1)
        elif activePlayer == 1:
            return position.winner()
        return 0

    for i in position.get_empty_squares():
        positionCopy = deepcopy(position)
        positionCopy.make_move(i, player)
        # recursive call with a deepcopy of the position, oppositing player, and the updated move or i
        val = alphaBeta(positionCopy, depth-1, alpha, beta, get_oppossing_player(player), i)
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

""" These functions are for testing purposes"""

def save_player(player):
    f = open('cur_player.txt', 'w')
    f.write(str(player))
    f.close()

def ab_bot(position, player):
    # player = -1
    a = -2
    choices = []
    if len(position.get_empty_squares()) == position.size ** 2: # best 1st move
        return position.size ** 2 // 2 + 1
    players = [None, 'O', 'X']
    for move in position.get_empty_squares():
        clone = deepcopy(position)
        clone.make_move(move, player)
        val = alphaBeta(clone, 4, -2, 2, get_oppossing_player(player), move)
        print("move", move, "causes to", players[val], "wins!")
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)

def bot_move(position, player, t):
    save_player(player)
    if t == None:
        players = [None, 'X', 'O']
        ans = str(input("I'm '" + str(players[player]) + "'. Which Bot do u prefer? [mm/ab/mc/r] "))
        if ans == 'ab':
            move = ab_bot(position, player)

        print("My move is...")
    else:
        if t == 'ab':
            start = time.time()
            move = ab_bot(position, player)
            end = time.time()
            fout_ab.write(str(end - start) + '\n')
            # move = ab_bot(position, player)
    return move