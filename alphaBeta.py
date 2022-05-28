from copy import deepcopy
import random
import time
timeFile_for_ab = open("abTime.txt", 'w')

#Player saved in the file from bot_Move
def save_player(player):
    f = open('cur_player.txt', 'w')
    f.write(str(player))
    f.close()
# Player retrived from the file    
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

def ab_bot(position, player):
    a = -2
    moveChoices = []
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
            moveChoices = [move]
        elif val == a:
            moveChoices.append(move)
    return random.choice(moveChoices)

def bot_move(position, player, algoType):
    save_player(player)
    # This check is only there to ensure that the correct parameter(i.e ab) is passed
    if algoType == 'ab':
        start = time.time()
        move = ab_bot(position, player)
        end = time.time()
        #Reccods time by creating a new file
        timeFile_for_ab.write(str(end - start) + '\n')
    return move

