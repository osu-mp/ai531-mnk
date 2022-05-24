#!/usr/bin/python3

# AI 531 - m,n,k (MCTS)
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import math
import random
import unittest

from copy import deepcopy

from board import Board
from playout import Playout

branch_factor = 10
max_trials = 1000
uct_const = math.sqrt(2)            # constant term in uct evaluation

# def mcts_get_best_move(board: Board, player1, player2):

def mcts(board: Board, player1, policy=None):
    # for each possible square in the board, run a simulation
    # selection
    empty_squares = board.get_empty_squares()
    # if not empty_squares:
    #     raise Exception('matt')
    #     if board.did_player_win(player1):
    #         return 1
    #     else:
    #         return 0
    max_select = min(branch_factor, len(empty_squares))    # prevents from selecting more squares than remaining
    selected_squares = random.sample(empty_squares, max_select)

    # expansion
    #playouts = {}
    utilities = {}
    for square in selected_squares:
        # print(f'Expansion on square {square}')

        exp_board = Board(size=board.size, k=board.k, board=board.board, parent=board)
        exp_board.make_move(square, player1)
        # return if this move ends the game
        if exp_board.is_gameover(square, player1):
            # exp_board.show()
            if exp_board.is_tie():
                # playouts[square] = Playout(games=max_trials, wins=0)
                utilities[square] = 0
            elif exp_board.is_loss(player1):
                # playouts[square] = Playout(games=max_trials, wins=0)
                utilities[square] = 0
            else:
                # playouts[square] = Playout(games=max_trials, wins=max_trials)
                utilities[square] = 1
            continue

        # simulation
        playout = Playout()
        for i in range(max_trials):
            # print(f'Simulation {i} of square {square}')
            # sim_board = deepcopy(exp_board)
            #playout.add_game()

            score = trial(exp_board, player1)

            # backpropagation
            exp_board.add_game()

            if score == 1:
                exp_board.add_win()
                # playout.add_win()

        # backpropagation
        # playouts[square] = playout
        utilities[square] = uct(exp_board)

        # TODO : more than 1 node lookahead
        # create tree structure like astar from 15 puzzle
        # assign win ratio
        # create reward table
        # check ucb

    a = 1

    # select the move with the highest uct utility
    best_move = max(utilities, key=utilities.get)
    return best_move
    # return select_move(utilities)


def uct(board: Board):
    """
    Upper confidence bounds applied to trees
    Page 163 in AI book
    :param board:
    :return:
    """
    n = board.playout.games                                 # number of games simulated at this level
    value = board.playout.wins / board.playout.games        # exploitation
    value += uct_const * math.sqrt(math.log(n) * board.parent.playout.get_win_ratio() / n)

    return value


def select_move(playouts: {}):
    best_playout = None
    best_move = None
    for move, playout in playouts.items():
        if not best_playout:
            best_playout = playout
            best_move = move
            continue
        if playout.get_win_ratio() > best_playout.get_win_ratio():
            best_playout = playout
            best_move = move
        # if two playouts have the same win ration, pick the one with more games
        if playout.get_win_ratio() == best_playout.get_win_ratio():
            if playout.games > best_playout.games:
                best_playout = playout
                best_move = move

    return best_move




def get_other_player(player):
    """
    Get the alternate player (used to switch between for moves)
    :param player:
    :return:
    """
    if player == 1:
        return 2
    else:
        return 1

def trial(board, player1):
    """
    Playout the board for the given player
    :param board:
    :param player:
    :return:
    """
    board = Board(size=board.size, k=board.k, board=board.board)

    empty_squares = board.get_empty_squares()
    curr_player = get_other_player(player1)       # player2 should make first move since player1 selected square prior to trial
    while empty_squares:
        selected_square = empty_squares[random.randrange(len(empty_squares))]
        board.make_move(selected_square, curr_player)
        empty_squares = board.get_empty_squares()
        curr_player = get_other_player(curr_player)            # alternate between player 1 and 2 each loop

        if board.is_gameover(selected_square, player1):
            if board.is_win(selected_square, player1):
                return 1
            return 0

    try:
        if board.is_gameover(selected_square, player1):
            if board.is_win(selected_square, player1):
                return 1
            return 0
    except:
        a = 1


@staticmethod
def policy_random(board, player):
    """
    Random policy for mcts
    Given a board, select a random sqaure for the given player
    :param board:
    :param player:
    :return:
    """
    # get empty squares
    empty_squares = board.get_empty_squares()
    # pick random one
    selected = empty_squares[random.randrange(len(empty_squares))]
    return selected

class TestMCTS(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board((3, 3), 3)

    def skip_test_trial(self):
        pass#MCTS.trial(self.board, 1)

    def test_select_move(self):
        """
        Unit test for select_move, get the best move given playouts
        :return:
        """
        p1 = Playout()
        p1.add_game()
        p1.add_game()
        p1.add_win()
        p2 = Playout()
        p2.add_game()
        p2.add_win()

        playouts = {1: p1, 2: p2}

        self.assertEqual(2, select_move(playouts), 'p2 should be chosen (100% win ratio)')

    def test_mcts(self):
        """
        Work in progress test for mcts
        :return:
        """
        # mcts = MCTS(self.board, 1)
        player = 1
        while len(self.board.get_empty_squares()) > 0:
            best_move = mcts(self.board, player)
            self.board.make_move(best_move, player)
            if self.board.is_win(best_move, player):
                print(f'Player {player} wins!')
                self.board.show()
                break;
            print(f'Best move for player {player} is: {best_move}')
            self.board.show()
            player = get_other_player(player)

        print(f'Winning player: {self.board.winner}')


if __name__ == '__main__':
    unittest.main()
