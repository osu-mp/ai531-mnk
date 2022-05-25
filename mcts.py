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

uct_const = math.sqrt(2)            # constant term in uct evaluation
max_mcts_loops = 5000               # number of times to run mcts at each eval
DEBUG = False                       # set to True for verbose debugging messages

def log(msg: str):
    # print log messages to console if debugging enabled
    if DEBUG:
        print(msg)

class Node:
    """
    Node for tree search. Maintain parent, children, baard state and move to get to this node
    Maintain the number of wins and games for each node (propagates up tree after simulation)
    """
    def __init__(self, board, player, parent=None, square=None):
        self.board = deepcopy(board)            # ensure any edits made to the board do not bubble up
        self.parent = parent
        self.square = square
        self.children = []
        self.wins = 0
        self.games = 0
        self.player = player

    def get_uct(self):
        """
        Upper confidence bounds applied to trees
        Page 163 in AI book
        uct = wins / games + C * sqrt(log n * Parent(n) / n)
        :return:
        """
        if self.games == 0:         # avoid divide by zero
            return 0

        if not self.parent:         # return raw win percentage for root node
            return 1# self.wins / self.games

        # else uct = wins / games + C * sqrt(log n * Parent(n) / n)
        n = self.games  # number of games simulated at this level
        value = self.wins / n  # exploitation
        value += uct_const * math.sqrt(math.log(n) * self.parent.get_uct() / n)

        return value


def mcts_new(board: Board, player):
    # TODO add time tracker?
    loops = 0
    root = Node(board, player, None, None)
    for square in board.get_empty_squares():
        node = Node(board, player, root, square)
        root.children.append(node)

    log('\nNEW MCTS RUN')

    while loops < max_mcts_loops:
        loops += 1
        # selection / expansion
        node = select_node(root)
        # print(f'Selected node at square: {node.square}')

        # simulation
        result = playout(node)
        log(f'Result of playout ({node.square}): {result}')

        # backpropagation
        back_propagate(node, result)

    best_node = select_node(root)
    log(f'Best node of current root: {best_node.square}')
    return best_node.square


def select_node(node: Node):

    # if any nodes are unvisited, try them first
    for child in node.children:
        if child.games == 0:
            log(f'Returning unvisited node: {child.square}')
            return child

    # else select the node with the best uct value
    while len(node.children) > 0:
        best_uct = -1
        # pick the child node with the highest uct
        for child in node.children:
            uct = child.get_uct()
            log(f'UCT of {child.square} = {uct}')
            if uct > best_uct:
                best_uct = uct
                node = child

    return node

def playout(node):
    """
    For the given node, simulate a playout by selecting random moves for each player
    Start with the opposite player since the previous selection was done by current player
    Return 1 if the current player wins, else 0
    :param node:
    :return:
    """
    # create local copy of board to simulate playout
    board = Board(size=node.board.size, k=node.board.k, board=node.board.board)
    board.make_move(node.square, node.player)
    empty_squares = board.get_empty_squares()
    curr_player = get_other_player(node.player)     # player2 should make first move since player1 selected square prior to trial
    while empty_squares:                            # keep picking squares until board is filled
        selected_square = empty_squares[random.randrange(len(empty_squares))]
        board.make_move(selected_square, curr_player)
        empty_squares = board.get_empty_squares()
        curr_player = get_other_player(curr_player)  # alternate between player 1 and 2 each loop

    if board.is_win(node.square, node.player):      # return 1 if the target player won (use node.square since they may have not made the last move)
        return 1
    return 0


def back_propagate(node: Node, result: int):
    """
    Once a node has been simulated increase the game and (possibly) win counters for it and all parent nodes
    :param node:
    :param result:
    :return:
    """
    node.games += 1
    if result:
        node.wins += 1
    if not node.parent:
        return
    back_propagate(node.parent, result)


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


# TODO : not used yet since no other policies exist yet
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

    def test_mcts_new(self):
        """
        Work in progress test for mcts
        :return:
        """
        # mcts = MCTS(self.board, 1)
        player = 1
        while len(self.board.get_empty_squares()) > 0:
            best_move = mcts_new(self.board, player)
            self.board.make_move(best_move, player)
            if self.board.is_win(best_move, player):
                print(f'Player {player} wins!')
                self.board.show()
                break
            print(f'Best move for player {player} is: {best_move}')
            self.board.show()
            player = get_other_player(player)

        print(f'Winning player: {self.board.winner}')
        self.assertTrue(self.board.winner != 2, 'Player 2 should never win if strategy is correct')


if __name__ == '__main__':
    unittest.main()
