from copy import deepcopy
from typing import Tuple, Literal
from termcolor import colored
import numpy as np
import random

from collections import defaultdict
from queue import PriorityQueue
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
        self.board_cell = np.arange(self.size[0] * self.size[1]).reshape(self.size)

    def get_diagonal(self, coord: Tuple[int, int], vec: Tuple[int, int]):
        res = []
        coord = coord[0] + vec[0], coord[1] + vec[1]
        while self.is_within_board_cell(coord):
            res.append(self.board[coord[0]][coord[1]])
            coord = coord[0] + vec[0], coord[1] + vec[1]
        return list(reversed(res))

    def __str__(self):
        s = ''
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                s += '{0:^3}'.format(self.board[i][j])
            s += '\n'
        return s

    def is_gameover(self, pos: int, val):  # paceym: commented out to run on flip Literal[0, 1, 2]):
        self.is_win(pos, val)
        if len(self.get_empty_squares()) == 0:
            self.gameover = True
        return self.gameover

    def pos_to_cell_id(self, x: int, y: int):
        return x * self.size[1] + y
    #
    # def get_empty_squares(self):
    #     """
    #     Return indices of all empty squares
    #     :return:
    #     """
    #     empty_squares = []
    #     for i in range(self.size[0]):
    #         for j in range(self.size[1]):
    #             if self.board[i][j] == 0:
    #                 # size is a tuple m,n so use the m-index to get a unique id for each square
    #                 cell_id = self.pos_to_cell_id(i, j)
    #                 empty_squares += [cell_id]
    #     return empty_squares

    def get_empty_squares(self):
        return list(self.board_cell[self.board == 0])

    def get_random_empty_square(self):
        # of the empty cells, return a randomly selected one
        empty_squares = self.get_empty_squares()
        return empty_squares[random.randrange(len(empty_squares))]

    def is_within_board_pos(self, pos: int):
        return 0 <= pos < self.size[0] * self.size[1]

    def is_within_board_cell(self, coord: Tuple[int, int]):
        return 0 <= coord[0] < self.size[0] and 0 <= coord[1] < self.size[1]

    def pos_to_xy(self, pos: int):
        return pos // self.size[1], pos % self.size[1]

    def is_empty_pos(self, pos: int):
        x, y = self.pos_to_xy(pos)
        return self.board[x][y] == 0

    def is_move_OK(self, pos: int):
        return self.is_within_board_pos(pos) and self.is_empty_pos(pos)

    def make_move(self, pos: int, val):  #: Literal[0, 1, 2]):
        """

        :param pos:
        :param val: 0: empty, 1: X player; 2: O player
        """
        x, y = self.pos_to_xy(pos)
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

    def get_diagonal_topleft(self, r: int, c: int):
        return self.get_diagonal((r, c), (-1, -1)) + [self.board[r][c]] + self.get_diagonal((r, c), (1, 1))

    def get_diagonal_topright(self, r: int, c: int):
        return self.get_diagonal((r, c), (-1, 1)) + [self.board[r][c]] + self.get_diagonal((r, c), (1, -1))

    def is_game_ending_move(self, pos: int):
        """
        Test whether taking the square is a game ending move (if either player wins with that square)
        :param pos:
        :return:    True if taking the square wins the game for either player, else false
        """
        game_over = False
        for player in [1, 2]:
            self.make_move(pos, player)
            if self.is_win(pos, player):
                game_over = True
                break

        self.make_move(pos, 0)  # be sure to undo move
        return game_over

    def is_win(self, pos: int, val):  # Literal[0, 1, 2]):
        assert val in [0, 1, 2]
        flag = False
        x, y = self.pos_to_xy(pos)
        matrix = self.board

        horizon = matrix[x]
        vertical = matrix[:, y]
        topleft_dg = self.get_diagonal_topleft(x, y)
        topright_dg = self.get_diagonal_topright(x, y)

        lines = [horizon, vertical, topleft_dg, topright_dg]
        # print(f'{pos=}, {x=}, {y=}, {lines=}')

        player = ['.', 'X', 'O']  # converting -1, 1, 0 to O, X, .
        if val == 1 or val == 2:
            five_pieces = player[val] * self.k
        else:
            five_pieces = '#' * self.k
        # print(f'{five_pieces=}')

        for line in lines:
            y = ''
            for elem in line:
                y += player[elem]
                if five_pieces in y:
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

    def show(self, show_ids=False):
        s = ''
        colors = ['white', 'red', 'blue']

        # print column ids
        if show_ids:
            header = colored(str('{0:^3}'.format(str(0))), 'yellow')
            for i in range(self.size[1]):
                header += colored(str('{0:^3}'.format(str(i))), 'yellow')
            header += '\n'
            s += header

        for i in range(self.size[0]):

            # print row id
            # if i > 0:
            if show_ids:
                s += colored(str('{0:^3}'.format(str(i))), 'yellow')

            for j in range(self.size[1]):
                square = self.board[i][j]
                cell_id = self.pos_to_cell_id(i, j)
                # print(f'{i=}, {j=}, {cell_id=}')
                piece = [str(cell_id), 'X', 'O']
                s += colored(str('{0:^3}'.format(piece[square])), colors[square])
            s += '\n'
        print(s)

    def get_cells_with_n_neighbors(self, n: int):
        """
        Return a list of all cells that have at least n neighbors (X or 0 touching it, including diagonals)
        Cells with 0 do not count
        :param x:
        :return:
        """
        raise Exception('not implmented')

    def get_emtpy_cell_neighbor_count(self):
        """
        Return a dictionary where the key is the cell number and the value is number of adjacent filled cells (value != 0)
        :return:
        """
        counts = defaultdict(int)
        for cell in self.get_empty_squares():
            x, y = self.pos_to_xy(cell)
            # check the cells to the left, left up, up, up right,
            #                        right, down right, down, down left
            # if valid cell and empty, increment counter
            for i, j in [(-1, 0), (-1, 1), (0, 1), (1, 1),
                         (1, 0), (1, -1), (0, -1), (-1, -1)]:
                if self.is_within_board_cell((x + i, y + j)) and self.board[x + i][y + j] != 0:
                    counts[cell] += 1
                    # print(f'Cell {cell} has occupied neighbor {x + i},{y + j} {self.board[x + i][y + j]}')

        return counts

    def get_emtpy_cell_priority_queue(self, player):
        """
        Return a priority queue for the empty cells, ordered by cells with most filled cells
        Each entry is (neighbors, cell id)
        :return:
        """
        queue = PriorityQueue()
        cells_counts = self.get_emtpy_cell_neighbor_count()
        if len(cells_counts) > 0:
            for cell in cells_counts.keys():
                # if a win, set the value as negative 9; no cell can have more than 8 neighbors, so this will
                # ensure the cell is at the front of the priority queue (lowest numbers first)
                if self.is_game_ending_move(cell):
                    queue.put((-9, cell))
                    continue

                # multiply filled neighbor count by negative 1 to put most constrained empty cells first
                # i.e. a cell with only 1 open neighbor is more valuable than one with 8 (no filled neighbors)
                # the priority queue would then be -1, -8
                queue.put((cells_counts[cell] * -1, cell))

        return queue

    def get_common_cells_for_player(self, player):
        """
        Find the cells neighboring at least 2 of the given player's cells
        For the example below, if the player is 1 (X), this function would return cells ordered by count:
         6, 0, 15  (6 has the higher utility (2) than 0 and 15 (1))
        For player 2 (O) it should return 6, 4, 8, 12, 13, 14
        -  1  2  3
        4  X  6  7
        8  X  O  8
        12 13 14 15
        Intersection of values are more valuable
        :param player:
        :return:
        """
        raise Exception('Do not use until the get_cells heuristic above is completed')


# def test():


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

    def test_is_win(self):
        # player 1 (X) gets all top row (0, 1, 2)
        board = Board((3, 3), 3)
        board.make_move(0, 1)
        board.make_move(4, 2)
        board.make_move(1, 1)
        board.make_move(5, 2)
        board.make_move(2, 1)
        self.assertTrue(board.is_win(2, 1), 'Player1 wins with top row')

    def test_3_4_board(self):
        # player 1 (X) gets middle row in 3x4 board (4, 5, 6)
        # NOTE: this should be a win, but the board looks wrong
        # TODO
        print('Skipped 3_4_board')
        return
        board = Board((3, 4), 3)
        board.make_move(3, 1)
        board.show()
        board.make_move(2, 2)
        board.make_move(4, 1)
        board.make_move(8, 2)
        board.make_move(5, 1)
        board.show()
        self.assertTrue(board.is_win(5, 1), 'Player1 wins with middle row')
        self.assertFalse(board.is_win(7, 2), 'Player2 loses with middle row')
        # board.make_move(5, 1)

    def test_get_cells_with_n_neighbors(self):
        """
        Unit test for get_cells_with_n_neighbors
        :return:
        """
        '''
        Using this board
        0  1  2  3
        4  X  6  7
        8  O  X  11
        12 13 14 15
        
        n of 1 should return cells: 0, 1, 2, 4, 6, 7, 8, 11, 13, 14, 15
        n of 2 should return cells: 4, 6, 8, 13, 14
        '''

    # def test_diagonal(self):
    # board = Board((5, 4), 3)

    def test_make_move(self):
        # test rectangular board
        board = Board((5, 4), 3)
        board.make_move(9, 2)
        board.make_move(14, 2)
        board.make_move(19, 2)
        board.show()
        self.assertTrue(board.is_win(19, 2), True)

        # test square
        board = Board((3, 3), 2)
        board.show()
        # board.make_move(0, 1)
        # board.make_move(6, 1)
        # board.make_move(12, 1)
        # print(f'{board.is_win(12, 1)=}')
        # board.show()
        # print(board)

    def test_get_emtpy_cell_neighbor_count(self):
        """
        Using a 3s3 board, count the empty neighbors from the middle (cell 4)
        Fill the neighboring cells and verify neighbor count increases
        :return:
        """
        board = Board((3, 3), 3)

        neighbors = 0  # cell 4 starts with 0 occupied neighbors (board is empty)
        for cell in range(9):
            if cell == 4:  # do not occupy cell 4
                continue
            board.make_move(cell, 1)
            neighbors += 1

            neighbor_dict = board.get_emtpy_cell_neighbor_count()
            # print(f'Take cell {cell}')            # DEBUG
            # board.show()
            # print(neighbor_dict)
            self.assertEqual(neighbor_dict[4],
                             neighbors)  # after a new cell taken, ensure cell 4 (middle) neighbor count increased

    def test_get_emtpy_cell_priority_queue(self):
        """

        :return:
        """
        board = Board((3, 3), 3)

        board.make_move(0, 1)
        board.make_move(1, 1)
        board.make_move(3, 1)
        queue = board.get_emtpy_cell_priority_queue(player=1)
        best = queue.get()
        # with cells 0, 1, and 3 taken this means that cell 4 is the best since it has 3 occupied neighbors
        self.assertEqual(best[1], 2)

        # once cells 4 and 6 are taken, cell 7 is the best (3 neighbors)
        board.make_move(4, 1)
        board.make_move(6, 1)
        queue = board.get_emtpy_cell_priority_queue(player=1)
        best = queue.get()
        # with cells 0, 1, and 3 taken this means that cell 4 is the best since it has 3 occupied neighbors
        self.assertEqual(best[1], 2)

    def test_get_emtpy_cell_priority_queue_winning_move(self):
        """
        Test the priority queue algo returns the winning move (even though it does not have the most neighbors)

        :return:
        """
        board = Board((3, 3), 3)

        # setup the board so that X is looking to win with diagonal from top left to bottom right
        board.make_move(0, 1)
        board.make_move(1, 2)
        board.make_move(4, 1)
        board.make_move(2, 2)
        board.show()
        # when the priority queue is created, cells 3 and 5 will have the most nieghors (3 each)
        # however, if X picks the bottom right, it will win so that cell should be at the front of the queue
        # even though it only has 1 neighbor
        queue = board.get_emtpy_cell_priority_queue(player=1)
        best = queue.get()
        # with cells 0, 1, and 3 taken this means that cell 4 is the best since it has 3 occupied neighbors
        self.assertEqual(best[1], 8)

    def test_empty_cells(self):
        b = Board((4, 3), 3)
        b.make_move(2, 1)
        print('print')
        b.show()
        print(b.get_empty_squares())
        # print(b)


if __name__ == '__main__':
    unittest.main()
    # test_empty_cells()
