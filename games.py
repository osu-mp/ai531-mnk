#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

from typing import Tuple, Literal

from board import Board
from mcts import mcts_new
from util import get_other_player, log
from alphaBeta import *

import cfg

"""
Central location for simulating games with various combinations of players including:
-mcts bot vs. mcts bot
-TODO other configs
-minimax bot vs. minimax bot
-mcts bot vs. minmmax bot (player1 = mcts)
-minimax bot vs. mcts bot (player1 = minimax)
"""
def mcts_vs_mcts(n_games: int, m: int, n: int, k: int):
    '''
    Simulate n games of mcts vs. mcts using m by n board (k consecutive to win)
    :param n_games: number of games to simulate
    :return: player1 wins, player2 wins, ties
    '''
    player1_wins = 0
    player2_wins = 0
    ties = 0

    for n_game in range(n_games):
        player = 1
        board = Board((m, n), k)
        while len(board.get_empty_squares()) > 0:
            best_move = mcts_new(board, player)
            board.make_move(best_move, player)
            if board.is_win(best_move, player):
                print(f'Player {player} wins!')
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


def ab_vs_ab(n_games: int, m: int, n: int, k: int):
    '''
    Simulate n games of alpha-beta vs. alpha-beta using m by n board (k consecutive to win)
    :param n_games: number of games to simulate
    :return: player1 wins, player2 wins, ties
    '''
    player1_wins = 0
    player2_wins = 0
    ties = 0

    for n_game in range(n_games):
        player = 1
        board = Board((m, n), k)
        while len(board.get_empty_squares()) > 0:
            best_move = bot_move(board,player,'ab')
            board.make_move(best_move, player)
            if board.is_win(best_move, player):
                print(f'Player {player} wins! ({n_game} of {n_games}')
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