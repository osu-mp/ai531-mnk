#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

from collections import defaultdict

from tqdm import tqdm

from mcts import mcts_new
from alphaBeta import *

import cfg

"""
Central location for simulating games with various combinations of players including:
-mcts bot vs. mcts bot
-alphabeta bot vs. alphabeta bot
-mcts bot vs. alphabeta bot (player1 = mcts)
-alphabeta bot vs. mcts bot (player1 = alphabeta)
"""


def time_selected_move(move_func, board, player):
    """
    Get the best move from move_func (using board and player)
    Also return the runtime (sec) that the algo took to decide
    :param move_func:
    :param board:
    :param player:
    :return: move (sqaure to take) and runtime
    """
    start = time.time()
    best_move = move_func(board, player)
    runtime = time.time() - start

    return best_move, runtime


def bot_vs_bot(p1_func, p2_func, n_games: int, m: int, n: int, k: int, filename=None, player_mcts_loops=None):
    '''
    Simulate n games of p1_func vs. p2_func using m by n board (k consecutive to win)
    p*_func will be either the mcts algo or the alpha beta algo
    :param p1_func: player1 move decision function (mcts or ab)
    :param p2_func: player2 move decision function (mcts or ab)
    :param n_games: number of games to simulate
    :param m: board dimension
    :param n: board dimension
    :param k: number of consecutive cells to win
    :return: winning percentage of each player, tie percent and average runtime per player for each move
    '''
    '''
    :param n_games: number of games to simulate
    :return: player1 wins, player2 wins, ties
    '''

    wins = {
        0: 0,  # player 1 win count
        1: 0,  # player 2 win count
        2: 0  # tie count
    }

    runtimes = defaultdict(float)  # total runtime for each player (cumulative for all games)
    moves = defaultdict(int)  # total number of moves for each player (cumulative for all games)

    move_funcs = {  # dictionary used within loop to call correct player function (key = player)
        1: p1_func,
        2: p2_func
    }

    for n_game in tqdm(range(n_games)):
    # for n_game in range(n_games):
        player = 1
        board = Board((m, n), k)
        while len(board.get_empty_squares()) > 0:
            if player_mcts_loops:  # allow for different mcts loop values per player
                cfg.max_mcts_loops = player_mcts_loops[player]
            best_move, runtime = time_selected_move(move_funcs[player], board, player)
            runtimes[player] += runtime
            moves[player] += 1
            board.make_move(best_move, player)
            if board.is_win(best_move, player):
                # print only if there is a winner (do not care about ties as much)
                # print(f'Player {player} wins! ({n_game} of {n_games})')
                if cfg.DEBUG:
                    board.show()
                break
            log(f'Best move for player {player} is: {best_move}')
            if cfg.show_each_move:
                board.show()
            player = get_other_player(player)

        if board.winner == 1:
            wins[1] += 1
        elif board.winner == 2:
            wins[2] += 1
        else:
            wins[0] += 1
            # print(f'Tie! ({n_game} of {n_games})')

    p1_win_pct = int(wins[1] / n_games * 100)
    p2_win_pct = int(wins[2] / n_games * 100)
    tie_pct = int(wins[0] / n_games * 100)
    p1_avg_time = runtimes[1] / moves[1]
    p2_avg_time = runtimes[2] / moves[2]

    if filename:
        if p1_func == mcts_new:
            p1 = 'mcts'
        else:
            p1 = 'ab'
        if p2_func == mcts_new:
            p2 = 'mcts'
        else:
            p2 = 'ab'
        with open(filename, 'a') as csv:  # append to file as sim progresses
            line = ','.join([str(val) for val in [m, n, k, p1, p2, p1_win_pct, p2_win_pct, tie_pct, n_games, f'{p1_avg_time:.4f}', f'{p2_avg_time:.4f}']])

            if player_mcts_loops:
                line += f',{str(player_mcts_loops[1])},{str(player_mcts_loops[2])}'

            csv.write(line + '\n')
            print(line)
            # print(f'{p1} vs {p2} sim complete: {line}')

    return p1_win_pct, p2_win_pct, tie_pct, p1_avg_time, p2_avg_time


def mcts_vs_mcts(n_games: int, m: int, n: int, k: int):
    '''
    Simulate n games of mcts vs. mcts using m by n board (k consecutive to win)
    :param n_games: number of games to simulate
    :return: player1 wins, player2 wins, ties
    '''
    raise Exception('Deprecated: use bot_vs_bot instead')
    player1_wins = 0
    player2_wins = 0
    ties = 0

    runtimes = defaultdict(float)  # total runtime for each player (cumulative for all games)
    moves = defaultdict(int)  # total number of moves for each player (cumulative for all games)

    for n_game in tqdm(range(n_games)):
        player = 1
        board = Board((m, n), k)
        while len(board.get_empty_squares()) > 0:
            best_move, runtime = time_selected_move(mcts_new, board, player)  # mcts_new(board, player)
            runtimes[player] += runtime
            moves[player] += 1
            board.make_move(best_move, player)
            if board.is_win(best_move, player):
                # print only if there is a winner (do not care about ties as much)
                print(f'Player {player} wins! ({n_game} of {n_games})')
                if cfg.DEBUG:
                    board.show()
                break
            log(f'Best move for player {player} is: {best_move}')
            if cfg.show_each_move:
                board.show()
            player = get_other_player(player)

        if board.winner == 1:
            player1_wins += 1
        elif board.winner == 2:
            player2_wins += 1
        else:
            ties += 1

        # board.show()
    p1_win_pct = int(player1_wins / n_games * 100)
    p2_win_pct = int(player2_wins / n_games * 100)
    tie_pct = int(ties / n_games * 100)
    p1_avg_time = runtimes[1] / moves[1]
    p2_avg_time = runtimes[2] / moves[2]
    return p1_win_pct, p2_win_pct, tie_pct, p1_avg_time, p2_avg_time


def ab_vs_ab(n_games: int, m: int, n: int, k: int):
    '''
    Simulate n games of alpha-beta vs. alpha-beta using m by n board (k consecutive to win)
    :param n_games: number of games to simulate
    :return: player1 wins, player2 wins, ties
    '''
    raise Exception('Deprecated: use bot_vs_bot instead')
    player1_wins = 0
    player2_wins = 0
    ties = 0

    for n_game in tqdm(range(n_games)):
        player = 1
        board = Board((m, n), k)
        while len(board.get_empty_squares()) > 0:
            best_move = bot_move(board, player, 'ab')
            board.make_move(best_move, player)
            if board.is_win(best_move, player):
                # print only if there is a winner (do not care about ties as much)
                print(f'Player {player} wins! ({n_game} of {n_games})')
                if cfg.DEBUG:
                    board.show()
                break
            log(f'Best move for player {player} is: {best_move}')
            if cfg.DEBUG:
                board.show()
            player = get_other_player(player)

        if board.winner == 1:
            player1_wins += 1
        elif board.winner == 2:
            player2_wins += 1
        else:
            ties += 1

    return player1_wins, player2_wins, ties


def mcts_vs_ab(n_games: int, m: int, n: int, k: int):
    '''
    Simulate n games of mcts vs. ab using m by n board (k consecutive to win)
    :param n_games: number of games to simulate
    :return: player1 wins, player2 wins, ties
    '''
    raise Exception('Deprecated: use bot_vs_bot instead')
    player1_wins = 0
    player2_wins = 0
    ties = 0

    for n_game in tqdm(range(n_games)):
        player = 1
        board = Board((m, n), k)
        while len(board.get_empty_squares()) > 0:
            if player == 1:  # player 1 uses mcts to pick move
                best_move = mcts_new(board, player)
            else:  # player 2 uses ab to pick move
                best_move = ab_bot(board, player)
            board.make_move(best_move, player)
            if board.is_win(best_move, player):
                # print only if there is a winner (do not care about ties as much)
                print(f'Player {player} wins! ({n_game} of {n_games})')
                if cfg.DEBUG:
                    board.show()
                break
            # log(f'Best move for player {player} is: {best_move}')
            if cfg.show_each_move:
                board.show()
            player = get_other_player(player)

        if board.winner == 1:
            player1_wins += 1
        elif board.winner == 2:
            player2_wins += 1
        else:
            ties += 1

        # board.show()

    return player1_wins, player2_wins, ties


def ab_vs_mcts(n_games: int, m: int, n: int, k: int):
    '''
    Simulate n games of ab vs. mcts using m by n board (k consecutive to win)
    :param n_games: number of games to simulate
    :return: player1 wins, player2 wins, ties
    '''
    raise Exception('Deprecated: use bot_vs_bot instead')
    player1_wins = 0
    player2_wins = 0
    ties = 0

    for n_game in tqdm(range(n_games)):
        player = 1
        board = Board((m, n), k)
        while len(board.get_empty_squares()) > 0:
            if player == 1:  # player 1 uses ab to pick move
                best_move = ab_bot(board, player)
            else:  # player 2 uses mcts to pick move
                best_move = ab_bot(board, player)
            board.make_move(best_move, player)
            if board.is_win(best_move, player):
                # print only if there is a winner (do not care about ties as much)
                print(f'Player {player} wins! ({n_game} of {n_games})')
                if cfg.DEBUG:
                    board.show()
                break
            # log(f'Best move for player {player} is: {best_move}')
            if cfg.show_each_move:
                board.show()
            player = get_other_player(player)

        if board.winner == 1:
            player1_wins += 1
        elif board.winner == 2:
            player2_wins += 1
        else:
            ties += 1

        # board.show()

    return player1_wins, player2_wins, ties
