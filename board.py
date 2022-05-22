from copy import deepcopy
from typing import Tuple, Literal
from termcolor import colored
import numpy as np

import unittest

class Board:
    def __init__(self, size: Tuple[int, int], k: int, board=None):
        self.k = k
        self.size = size
        self.gameover = False
        self.winner = 0
        if board is not None:
            self.board = deepcopy(board)
        else:
            self.board = np.zeros(self.size, dtype=int)

    def get_diagonal(self, coord: Tuple[int, int], vec: Tuple[int, int]):
        res = []
        coord = coord[0] + vec[0], coord[1] + vec[1]
        while self.is_within_board_cell(coord):
            res.append(self.board[coord[0]][coord[1]])
            coord = coord[0] + vec[0], coord[1] + vec[1]
        return res

    def __str__(self):
        s = ''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                s += '{0:^3}'.format(self.board[i][j])
            s += '\n'
        return s

    def is_gameover(self, pos: int, val: Literal[0, 1, 2]):
        self.is_win(pos, val)
        if len(self.get_empty_squares()) == 0:
            self.gameover = True
        return self.gameover

    def get_empty_squares(self):
        """
        Return indices of all empty squares
        :return:
        """
        empty_squares = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j] == 0:
                    # size is a tuple m,n so use the m-index to get a unique id for each square
                    empty_squares += [i * self.size[0] + j]
        return empty_squares

    def is_within_board_pos(self, pos: int):
        return 0 <= pos < self.size[0] * self.size[1]

    def is_within_board_cell(self, coord: Tuple[int, int]):
        return 0 <= coord[0] < self.size[0] and 0 <= coord[1] < self.size[1]

    def is_empty_pos(self, pos: int):
        return self.board[pos // self.size[0]][pos % self.size[0]] == 0

    def is_move_OK(self, pos: int):
        return self.is_within_board_pos(pos) and self.is_empty_pos(pos)

    def make_move(self, pos: int, val: Literal[0, 1, 2]):
        """

        :param pos:
        :param val: 0: empty, 1: X player; 2: O player
        """
        x, y = pos // self.size[0], pos % self.size[0]
        self.board[x][y] = val

        # if this is the final move of the game, check for winner
        if len(self.get_empty_squares()) == 0:
            self.is_win(pos, val)

    def did_player_win(self, player):
        """
        Once the board has been filled, return True only if the given player won
        :param player:
        :return:
        """
        # this should not be called until the game is over
        if not self.gameover:
            raise Exception('Game not over')
        # return True if given player won, else false
        return self.winner == player

    def is_win(self, pos: int, val: Literal[0, 1, 2]):
        assert val in [0, 1, 2]
        flag = False
        r, c = pos // self.size[0], pos % self.size[0]
        matrix = self.board

        # horizon = matrix[r][max(c - (self.k - 1), 0):c] + \
        #           [matrix[r][c]] + \
        #           matrix[r][c + 1:min(c + (self.k - 1), self.size[1] - 1) + 1]
        horizon = matrix[r]
        vertical = matrix[:, c]
        topleft_dg = self.get_diagonal((r, c), (-1, -1)) + [matrix[r][c]] + self.get_diagonal((r, c), (1, 1))
        topright_dg = self.get_diagonal((r, c), (-1, 1)) + [matrix[r][c]] + self.get_diagonal((r, c), (1, -1))

        # vertical = [matrix[a][c] for a in range(max(r - (self.k - 1), 0), r)] + \
        #            [matrix[r][c]] + \
        #            [matrix[a][c] for a in range(r + 1, min(r + (self.k - 1), self.size - 1) + 1)]
        #
        # d1 = [matrix[r - a][c - a] for a in range(min(r, c, (self.k - 1)) + 1 - 1, 1 - 1, -1)] + \
        #      [matrix[r][c]] + [matrix[r + a][c + a] for a in
        #                        range(1, min(self.size - r - 1, self.size - c - 1, (self.k - 1)) + 1)]
        #
        # d2 = [matrix[r - a][c + a] for a in range(min(r, self.size - c - 1, (self.k - 1)) + 1 - 1, 1 - 1, -1)] + \
        #      [matrix[r][c]] + [matrix[r + a][c - a] for a in range(1, min(self.size - r - 1, c, (self.k - 1)) + 1)]

        lines = [horizon, vertical, topleft_dg, topright_dg]
        # lines = [horizon]
        # print(f'{lines=}')

        player = ['.', 'X', 'O']  # converting -1, 1, 0 to O, X, .
        if val == 1 or val == 2:
            five_pieces = player[val] * self.k
        else:
            five_pieces = '#' * self.k
        # print(f'{five_pieces=}')

        for line in lines:
            c = ''
            for elem in line:
                c += player[elem]
                if five_pieces in c:
                    flag = True
                    break
            # print(f'{c=}')

        if flag:
            self.gameover = True
            self.winner = val
        return flag

    def is_tie(self):
        """
        Return True if the board is full and there is no winner
        :return:
        """

        if len(self.get_empty_squares()) > 0:
            return False
        # return True if the winner is neither player 1 or 2
        return self.winner == 0

    def is_loss(self, player):
        """
        Return True if the given player lost the game
        Else False (either game is still ongoing or a tie)
        :param player:
        :return:
        """
        if len(self.get_empty_squares()) > 0:
            return False
        # a tie is not a loss
        if self.is_tie():
            return False
        # if the board is full, it's not a tie and the other player won, that is a loss
        return self.winner != player

    def show(self):
        s = ''
        colors = ['white', 'red', 'blue']
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                square = self.board[i][j]
                cell_id = i * self.size[0] + j
                piece = [str(cell_id), 'X', 'O']
                s += colored(str('{0:^3}'.format(piece[square])), colors[square])
            s += '\n'
        print(s)


def test():
    board = Board((5, 4), 3)
    board.make_move(15, 2)
    board.make_move(16, 2)
    board.make_move(17, 2)
    print(f'{board.is_win(17, 2)=}')
    board.show()

    board.make_move(0, 1)
    board.make_move(6, 1)
    board.make_move(12, 1)
    print(f'{board.is_win(12, 1)=}')
    board.show()
    # print(board)

class TestBoard(unittest.TestCase):
    def test_is_tie_true(self):
        """
        Unit test for tie checker (tie case)
        Also covers is_loss
        :return:
        """
        # start with 3x3 board, need 3 consecutive to win
        board = Board((3, 3), 3)
        board.make_move(0, 1)
        board.make_move(1, 2)
        board.make_move(2, 1)
        board.make_move(3, 2)
        board.make_move(4, 1)
        board.make_move(5, 2)
        board.make_move(7, 1)
        board.make_move(8, 2)
        board.is_win(6, 1)
        self.assertFalse(board.is_tie(), 'Game not over yet, should not be a tie')
        board.make_move(6, 2)
        # board.is_win(6, 2)
        board.show()
        print(f'Winner is player {board.winner}')
        self.assertTrue(board.is_tie(), 'Neither player won, this should be a tie')
        self.assertFalse(board.is_loss(1), 'Neither player lost')
        self.assertFalse(board.is_loss(2), 'Neither player lost')

    def test_is_tie_false(self):
        """
        Unit test for tie checker (NOT a tie case)
        Also covers is_loss
        Player 1 wins
        :return:
        """
        # start with 3x3 board, need 3 consecutive to win
        board = Board((3, 3), 3)
        board.make_move(0, 1)
        board.make_move(1, 2)
        board.make_move(2, 1)
        board.make_move(3, 2)
        board.make_move(4, 1)
        board.make_move(5, 2)
        board.make_move(7, 1)
        board.make_move(8, 2)
        board.is_win(6, 1)
        board.make_move(6, 1)
        board.show()
        print(f'Winner is player {board.winner}')
        self.assertFalse(board.is_tie(), 'Player 1 won, is not a tie')
        self.assertFalse(board.is_loss(1), 'Player 1 won (not a loss)')
        self.assertTrue(board.is_loss(2), 'Player 2 lost')


if __name__ == '__main__':
    test()