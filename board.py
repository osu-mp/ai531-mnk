from typing import Tuple, Literal
from termcolor import colored
import numpy as np


class Board:
    def __init__(self, size: Tuple[int, int], k: int):
        self.k = k
        self.size = size
        self.board = np.zeros(self.size, dtype=np.int)
        self.gameover = False
        self.winner = 0

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
        empty_squares = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i][j] == 0:
                    empty_squares += [i * self.size + j]
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


if __name__ == '__main__':
    test()
