#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import unittest

from games import mcts_vs_mcts, ab_vs_ab

import cfg

class MNKDataCollection(unittest.TestCase):
    '''
    Performance monitoring and parameter refinement for mnk bots
    '''

    def test_mcts_consts(self):
        '''
        Collect data on the mcts algo as configured in cfg.py
        Other tests in this script vary the params and collect data
        :return:
        '''
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts.csv', 'w') as csv:
            csv.write(f'player1_wins,player2_wins,ties,player1_pct,p2_pct,tie_pct,mcts_loops,uct_const,m,n,k\n')
            for sim_num in range(10):
                player1_wins, player2_wins, ties = mcts_vs_mcts(iterations, m, n, k)

                line = ','.join([str(val) for val in [
                    player1_wins,
                    player2_wins,
                    ties,
                    int(player1_wins / iterations * 100),
                    int(player2_wins / iterations * 100),
                    int(ties / iterations * 100),
                    cfg.max_mcts_loops,
                    cfg.uct_const,
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')
                print(line)

    def test_uct_const(self):
        '''
        Collect game data for varying constants in the uct algo
        Generic algo default is usually square root of 2
        :return:
        '''
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_uct.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,uct_const,m,n,k\n')
            for uct_val in [1., 1.05, 1.1, 1.15, 1.2, 1.4, 2., 3, 4]:
                cfg.uct_const = uct_val
                player1_wins, player2_wins, ties = mcts_vs_mcts(iterations, m, n, k)

                line = ','.join([str(val) for val in [
                    player1_wins,
                    player2_wins,
                    ties,
                    int(player1_wins / iterations * 100),
                    int(player2_wins / iterations * 100),
                    int(ties / iterations * 100),
                    cfg.max_mcts_loops,
                    cfg.uct_const,
                    m,
                    n,
                    k]
                ])
                csv.write(f'{line}\n')

                print(f'\nuct const = {uct_val}\n')
                print(line)

    def test_mcts_loops(self):
        '''
        Collect game data for varying loop count in the mcts main loop
        :return:
        '''
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_loop_count.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,uct_const,m,n,k\n')
            for loop_count in [50, 250, 500, 1000]:
                cfg.max_mcts_loops = loop_count
                player1_wins, player2_wins, ties = mcts_vs_mcts(iterations, m, n, k)

                line = ','.join([str(val) for val in [
                    player1_wins,
                    player2_wins,
                    ties,
                    int(player1_wins / iterations * 100),
                    int(player2_wins / iterations * 100),
                    int(ties / iterations * 100),
                    cfg.max_mcts_loops,
                    cfg.uct_const,
                    m,
                    n,
                    k]
                ])
                csv.write(f'{line}\n')

                print(f'\nloop count = {loop_count}\n')
                print(line)

    def test_selection_policy(self):
        '''
        Collect game data for varying constants in the algo that selects which child node to select
        :return:
        '''
        iterations = 20 # cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_select_chance.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,random_pct,m,n,k')
            for random_pct in [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1]:
                cfg.select_random_chance = random_pct
                player1_wins, player2_wins, ties = mcts_vs_mcts(iterations, m, n, k)

                p1_pct = int(player1_wins / iterations * 100)
                p2_pct = int(player2_wins / iterations * 100)
                tie_pct = int(ties / iterations * 100)
                line = ','.join([str(val) for val in [
                    player1_wins,
                    player2_wins,
                    ties,
                    p1_pct,
                    p2_pct,
                    tie_pct,
                    cfg.max_mcts_loops,
                    cfg.expand_random_chance,
                    m,
                    n,
                    k]
                ])
                csv.write(f'{line}\n')

                print(f'\nrandom_pct = {random_pct}\n')
                print(f'MCTS (selection ratio={random_pct}: p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%%')

    def test_expansion_policy(self):
        '''
        Collect game data for varying constants in the algo that selects which square to expand from an unexplored node
        :return:
        '''
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_expand_chance.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,random_pct,m,n,k')
            for random_pct in [0, 0.25, 0.5, 0.75, 1]:
                cfg.expand_random_chance = random_pct
                player1_wins, player2_wins, ties = mcts_vs_mcts(iterations, m, n, k)

                line = ','.join([str(val) for val in [
                    player1_wins,
                    player2_wins,
                    ties,
                    int(player1_wins / iterations * 100),
                    int(player2_wins / iterations * 100),
                    int(ties / iterations * 100),
                    cfg.max_mcts_loops,
                    cfg.expand_random_chance,
                    m,
                    n,
                    k]
                ])
                csv.write(f'{line}\n')

                print(f'\nrandom_pct = {random_pct}\n')
                print(line)

    def test_ab_basic(self):
        '''
        Collect data on the alpha-beta algo in basic configuration
        Other tests in this script may vary the params and collect data
        :return:
        '''
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/alpha-beta.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,m,n,k\n')
            for sim_num in range(1):
                player1_wins, player2_wins, ties = ab_vs_ab(iterations, m, n, k)

                line = ','.join([str(val) for val in [
                    player1_wins,
                    player2_wins,
                    ties,
                    int(player1_wins / iterations * 100),
                    int(player2_wins / iterations * 100),
                    int(ties / iterations * 100),
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')
                print(line)

if __name__ == '__main__':
    unittest.main()
