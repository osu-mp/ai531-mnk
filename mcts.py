#!/usr/bin/python3

# AI 531 - m,n,k (MCTS)
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import random
import unittest

from copy import deepcopy

from board import Board

class MCTS:
    def __init__(self, board: Board, player: int, branch_factor=5):
        '''
        Init Monte Carlo Tree Search with two players
        :param play1:
        :param play2:
        '''
        self.board = deepcopy(board)
        self.player = player
        # branch factor is number of nodes to generate at each selection
        self.branch_factor = branch_factor

    def run(self, policy=None):
        # for each possible square in the board, run a simulation
        # selection
        empty_squares = self.board.get_empty_squares()
        max_select = min(self.branch_factor, len(empty_squares))    # prevents from selecting more squares than remaining
        selected_squares = random.sample(empty_squares, max_select)

        # expansion
        for square in selected_squares:
            self.board.make_move(square, self.player)
            # return if this move ends the game
            if self.board.is_gameover(square, self.player):
                self.board.show()
                if self.board.is_tie():
                    print('Tie')
                    return 0
                elif self.board.is_loss(self.player):
                    print(f'Player lost: {self.player}')
                    return -1
                else:
                    print(f'Player won:  {self.player}')
                    return 0
            print(f'playout using square {square}')

        # simulation
        # backpropagation


    @staticmethod
    def trial(board, player, policy=None, depth=2):
        """
        Run trials through MCTS and determine best move
        :param board:
        :param player:
        :param policy:
        :return:
        """
        if not policy:          # default to random policy
            selected = MCTS.policy_random(board, player)
        board.make_move(selected, player)
        board.show()

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
        self.board = Board((2, 2), 2)

    def skip_test_trial(self):
        MCTS.trial(self.board, 1)

    def test_mcts(self):
        """
        Work in progress test for mcts
        :return:
        """
        mcts = MCTS(self.board, 1)
        mcts.run()

if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()
