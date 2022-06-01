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
        uct = wins / games + C * sqrt(log(Parent games)/ (this node games))
        :return:
        """
        if self.games == 0:         # avoid divide by zero
            return 0

        if not self.parent:         # return raw win percentage for root node
            return self.wins / self.games

        n = self.games              # number of games simulated at this level
        value = self.wins / n                                       # exploitation
        log_parent = math.log(self.parent.games)
        value += cfg.uct_const * math.sqrt(log_parent / n)          # exploration

        return value


def mcts_new(board: Board, player):
    """
    Main Monte Carlo Tree Search algo
    :param board:
    :param player:
    :return: best move given current board
    """
    loops = 0
    root = Node(board, player, None, None)

    # initialize children as every possible empty square at root node
    for square in board.get_empty_squares():
        node = Node(board, player, root, square)
        root.children.append(node)

    log('\nNEW MCTS RUN')

    while loops < cfg.max_mcts_loops:
        loops += 1

        # selection
        node = select_node(root)

        # expansion
        leaf = expand_node(node)

        # simulation
        result = playout(leaf)
        log(f'Result of playout ({node.square}): {result}')

        # backpropagation
        back_propagate(leaf, result)

    best_node = select_node(root)           # after running as long as allowed, return the best node from root
    log(f'Best node of current root: {best_node.square}')
    return best_node.square


def select_node(node: Node):
    """
    Select the node with the best uct value
    :param node:
    :return:
    """

    while len(node.children) > 0:
        best_uct = -1
        best_nodes = []  # list of all nodes with max uct

        # pick the child node with the highest uct
        for child in node.children:
            # if either player can win with the square, take it
            if node.board.is_game_ending_move(child.square):
                return child
            uct = child.get_uct()
            log(f'UCT of {child.square} = {uct}')
            if uct > best_uct:          # new max uct found, reset list
                best_uct = uct
                # node = child
                best_nodes = [child]
            elif uct == best_uct:
                best_nodes.append(child)

        if len(best_nodes) == 1:          # if only one best node, return that
            node = best_nodes[0]
            # print(f'Single node with best uct: {node.square}')
        else:                               # else if multiple nodes have the same uct, pick a random one
            node = best_nodes[random.randrange(len(best_nodes))]
            # print(f'{len(best_nodes)} best nodes, random picked: {node.square}')

    log(f'Selected node at square: {node.square}')
    return node

def expand_node(node):
    """
    The given node is the bottom of the current tree. Pick a random child of this node
    and expand it to a new leaf/node. The playout will occur on the newly created leaf
    :param node:
    :return:
    """
    if not node.board.get_empty_squares(): # node.square and node.board.is_gameover(node.square, node.player):
        # print('Unable to expand terminal node')
        return node

    # expansion policy: pick using the policy most often, allow some randomness
    rand = random.random()
    if rand > cfg.expand_random_chance:
        selected_square = node.board.get_random_empty_square()
    else:
        queue = node.board.get_emtpy_cell_priority_queue(node.player)
        if queue.empty():
            selected_square = node.board.get_random_empty_square()      # if queue is empty, pick a random square
        else:
            best = queue.get()
            selected_square = best[1]

    leaf = Node(node.board, node.player, node, selected_square)
    leaf.board.make_move(selected_square, leaf.player)

    return leaf

def playout(node):
    """
    For the given node, simulate a playout by selecting random moves for each player
    Start with the opposite player since the previous selection was done by current player
    Return 1 if the current player wins, 0.5 for a tie, 0 for a loss
    :param node:
    :return:
    """
    # create local copy of board to simulate playout
    board = Board(size=node.board.size, k=node.board.k, board=node.board.board)
    selected_square = node.square
    board.make_move(node.square, node.player)       # player1 makes its move
    empty_squares = board.get_empty_squares()
    curr_player = get_other_player(node.player)     # player2 moves next
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


class TestMCTS(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board((3, 3), 3)

    def test_mcts_new(self):
        """
        Work in progress test for mcts
        :return:
        """
        from games import mcts_vs_mcts, bot_vs_bot          # put import inside inner scope to avoid circular references

        games = 5

        p1_win_pct, p2_win_pct, tie_pct, p1_runtime, p2_runtime = bot_vs_bot(mcts_new, mcts_new, games, 3, 3, 3)
        print(f'Player1 Won : {p1_win_pct}%')
        print(f'Player2 Won : {p2_win_pct}%')
        print(f'Ties        : {tie_pct}%')
        print(f'Player1 Avg Time/Move: {p1_runtime}')
        print(f'Player2 Avg Time/Move: {p2_runtime}')


if __name__ == '__main__':
    unittest.main()
