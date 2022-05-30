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
        uct = wins / games + C * sqrt(log Parent(n) / n)
        :return:
        """
        if self.games == 0:         # avoid divide by zero
            return 0

        if not self.parent:         # return raw win percentage for root node
            return self.wins / self.games

        # else uct = wins / games + C * sqrt(log n * Parent(n) / n)
        n = self.games  # number of games simulated at this level
        value = self.wins / n  # exploitation
        log_parent = math.log(self.parent.games)
        #value += cfg.uct_const * math.sqrt(math.log(n) * self.parent.get_uct() / n)     # exploration
        value += cfg.uct_const * math.sqrt(log_parent / n)

        # TODO : is this new algo correct/better?

        return value


def mcts_new(board: Board, player):
    # TODO add time tracker?
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
    if not node.board.get_empty_squares():
        # print('Unable to expand terminal node')
        return node

    rand = random.random()
    if rand > cfg.select_random_chance:
        rand_child = random.randrange(len(node.children))
        node = node.children[rand_child]

    else:
    # if any nodes are unvisited, try them first
    # for child in node.children:
    #     if child.games == 0:
    #         log(f'Returning unvisited node: {child.square}')
    #         return child

        # else select the node with the best uct value
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

    # expansion policy: half the time pick a random sqaure, the other half pick an empty square with the most neighbors
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

        games = 1
        player1_wins, player2_wins, ties = mcts_vs_mcts(games, 3, 3, 3)
        print(f'Player1 Wins: {player1_wins} ({(int)(player1_wins / games * 100)} %%)')
        print(f'Player2 Wins: {player2_wins} ({(int)(player2_wins / games * 100)} %%)')
        print(f'        Ties: {ties} ({(int)(ties / games * 100)} %%)')
        # self.assertTrue(player2_wins == 0, 'Player 2 should never win if strategy is correct')


if __name__ == '__main__':
    unittest.main()
