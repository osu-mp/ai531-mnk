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
from util import get_other_player, log

import cfg

DEBUG = cfg.DEBUG                       # set to True for verbose debugging messages


class Node:
    """
    Node for tree search. Maintain parent, children, baard state and move to get to this node
    Maintain the number of wins and games for each node (propagates up tree after simulation)
    """
    def __init__(self, board, player, parent=None, square=None):
        self.board = deepcopy(board)            # ensure any edits made to the board do not bubble up
        self.player = player
        self.parent = parent
        self.square = square
        self.children = []
        self.wins = 0
        self.games = 0

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
            return self.wins / self.games

        # else uct = wins / games + C * sqrt(log n * Parent(n) / n)
        n = self.games  # number of games simulated at this level
        value = self.wins / n  # exploitation
        value += cfg.uct_const * math.sqrt(math.log(n) * self.parent.get_uct() / n)

        return value


def mcts_new(board: Board, player):
    # TODO add time tracker?
    loops = 0
    root = Node(board, player, None, None)
    for square in board.get_empty_squares():
        node = Node(board, player, root, square)
        root.children.append(node)

    log('\nNEW MCTS RUN')

    while loops < cfg.max_mcts_loops:
        loops += 1
        # selection
        node = select_node(root)
        # print(f'Selected node at square: {node.square}')

        # expansion
        leaf = expand_node(node)

        # simulation
        result = playout(leaf)
        log(f'Result of playout ({node.square}): {result}')

        # backpropagation
        back_propagate(leaf, result)

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

def expand_node(node):
    """
    The given node is the bottom of the current tree. Pick a random child of this node
    and expand it to a new leaf/node. The playout will occur on the newly created leaf
    :param node:
    :return:
    """
    empty_squares = node.board.get_empty_squares()
    selected_square = empty_squares[random.randrange(len(empty_squares))]
    leaf = Node(node.board, node.player, node, selected_square)
    leaf.board.make_move(selected_square, leaf.player)

    return leaf

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
    selected_square = node.square
    board.make_move(node.square, node.player)
    empty_squares = board.get_empty_squares()
    curr_player = get_other_player(node.player)     # player2 should make first move since player1 selected square prior to trial
    while empty_squares:                            # keep picking squares until board is filled
        selected_square = empty_squares[random.randrange(len(empty_squares))]
        board.make_move(selected_square, curr_player)

        if board.is_win(selected_square, node.player):
            log(f'Result of playout of {node.square}: WIN')
            if DEBUG:
                board.show()
            return 1
        elif board.is_tie():
            log(f'Result of playout of {node.square}: TIE')
            if DEBUG:
                board.show()
            return 0.5
        elif board.is_gameover(selected_square, curr_player):
            log(f'Result of playout of {node.square}: LOSS')
            if DEBUG:
                board.show()
            return 0

        empty_squares = board.get_empty_squares()
        curr_player = get_other_player(curr_player)  # alternate between player 1 and 2 each loop

    #raise Exception('not here')

    if board.is_win(selected_square, curr_player) and curr_player == node.player:      # return 1 if the target player won (use node.square since they may have not made the last move)
        log(f'Result of playout of {node.square}: WIN')
        if DEBUG:
            board.show()
        return 1
    elif board.is_tie():
        log(f'Result of playout of {node.square}: TIE')
        if DEBUG:
            board.show()

        return 0.5
    log(f'Result of playout of {node.square}: LOSS')
    if DEBUG:
        board.show()
    return 0


def back_propagate(node: Node, result: int):
    """
    Once a node has been simulated increase the game and (possibly) win counters for it and all parent nodes
    :param node:
    :param result:
    :return:
    """
    node.games += 1
    node.wins += result     # 0 = loss, 0.5 = tie, 1 = win
    if not node.parent:
        return
    back_propagate(node.parent, result)


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
        from games import mcts_vs_mcts          # put import inside inner scope to avoid circular references

        player1_wins, player2_wins, ties = mcts_vs_mcts(1, 3, 3, 3)
        self.assertTrue(player2_wins == 0, 'Player 2 should never win if strategy is correct')


if __name__ == '__main__':
    unittest.main()
