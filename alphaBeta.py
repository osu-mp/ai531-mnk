from copy import deepcopy
# import random
import time
from typing import Tuple, Union

from util import get_other_player, log
from board import Board

ab_time_filename = 'abTime.txt'
INF = float('inf')
# PRIORITY = False
PRIORITY = True
MAX_DEPTH = 6
M = 3
N = 3
K = 3


def reward_for_first_player(first_player, winner):
    if winner == 0:
        return 0

    if first_player == 1:
        if winner == 1:
            return 1
        else:
            return -1
    else:
        assert first_player == 2
        if winner == 2:
            return 1
        else:
            return -1


def is_terminal(board: Board, move: int, player: int, depth: int):
    if move is None:
        return False  # start of the game is False
    return board.is_gameover(move, player) or depth == 0


THRESHOLD_PRINT = 10000


def min_value(board: Board, depth: int, alpha: int, beta: int,
              player: int, first_player: int, previous_move: int) -> Tuple[int, Union[None, int]]:
    global cnt_node
    cnt_node += 1
    # if cnt_node % THRESHOLD_PRINT == 0:
    #     print(f'{cnt_node=}')

    previous_player = get_other_player(player)
    terminal = is_terminal(board, previous_move, previous_player, depth)
    if terminal:
        # log(f'is_terminal for player {previous_player}')
        # board.show()
        return reward_for_first_player(first_player, board.winner), None

    v = INF
    v_move = None
    # log(f'parent MAX, {terminal=}, {previous_move=}, {previous_player=}, {player=}')
    # board.show()

    # for move in board.get_empty_squares():
    for move in get_candidate_moves(board, PRIORITY):
        boardCopy = deepcopy(board)  # type: Board
        boardCopy.make_move(move, player)

        v_child, _ = max_value(boardCopy, depth - 1, alpha, beta,
                               get_other_player(player), first_player, move)
        # boardCopy.show()
        # log(f'{move=}, {v_child=}, {alpha=}, {beta=}')

        if v_child < v:
            v, v_move = v_child, move
            beta = min(beta, v)
        if v <= alpha:
            return v, v_move
    return v, v_move


def get_candidate_moves(board: Board, priority=False):
    if priority:
        queue = board.get_emtpy_cell_sorted()
        # if len(queue) == 0:
        #     res = [board.get_random_empty_square()]  # if queue is empty, pick a random square
        # else:
        queue.sort()
        res = [e[1] for e in queue]
        # res = []
        # while not queue.empty():
        #     best = queue.get()
        #     selected_square = best[1]
        #     res.append(selected_square)
    else:
        res = board.get_empty_squares()
    assert isinstance(res, list)
    return res


def max_value(board: Board, depth, alpha, beta, player, first_player, previous_move=None) -> Tuple[
    int, Union[int, None]]:
    global cnt_node
    cnt_node += 1
    if cnt_node % THRESHOLD_PRINT == 0:
        print(f'{cnt_node=}')

    previous_player = get_other_player(player)
    terminal = is_terminal(board, previous_move, previous_player, depth)
    if terminal:
        # log(f'is_terminal for player {previous_player}')
        # board.show()
        return reward_for_first_player(first_player, board.winner), None

    # log('parent MAX')
    # log(f'parent MAX, {terminal=}, {previous_move=}, {previous_player=}, {player=}')
    # board.show()

    v = -INF
    v_move = None
    candidates = get_candidate_moves(board, PRIORITY)
    for move in candidates:
        boardCopy = deepcopy(board)  # type: Board
        boardCopy.make_move(move, player)

        v_child, _ = min_value(boardCopy, depth - 1, alpha, beta,
                               get_other_player(player), first_player, move)
        # boardCopy.show()
        # log(f'{move=}, {v_child=}, {alpha=}, {beta=}')

        if v_child > v:
            v, v_move = v_child, move
            alpha = max(alpha, v)

        if v >= beta:
            return v, v_move

    return v, v_move


def ab_bot(board: Board, player: int):
    # TODO: change max depth
    if MAX_DEPTH is not None:
        max_depth = MAX_DEPTH
    else:
        max_depth = board.size[0] * board.size[1]
    global cnt_node
    cnt_node = 0
    val, move = max_value(board, max_depth, -2, 2, player, player, None)
    # print(f'{val=}, {move=}, {cnt_node=}')
    return move


def bot_move(board: Board, player, algoType):
    # save_player(player)
    # This check is only there to ensure that the correct parameter(i.e ab) is passed
    if algoType == 'ab':
        start = time.time()
        move = ab_bot(board, player)
        end = time.time()
        # Record time by creating a new file
        with open(ab_time_filename, 'w+') as timeFile_for_ab:
            timeFile_for_ab.write(str(end - start) + '\n')
    return move


"""
Endpoint: Call obj.bot_move(1: position/board, 1/-1 depending on the player you want to go first, always 'ab')
"""
cnt_node = 0


def test():
    # b = Board((3, 3), 3)
    b = Board((M, N), K)
    print(ab_bot(b, player=1))
    print(f'{cnt_node=}')
    # depth = 4 * 4
    # val, move = max_value(b, depth, -2, 2, 1, 1, None)
    # move = bot_move(b, 1, 'ab')
    # print(val, move)


if __name__ == '__main__':
    test()
