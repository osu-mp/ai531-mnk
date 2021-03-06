#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import importlib
import unittest

from alphaBeta import ab_bot
from games import mcts_vs_mcts, ab_vs_ab, mcts_vs_ab, ab_vs_mcts, bot_vs_bot
from mcts import mcts_new

import cfg


class MNKDataCollection(unittest.TestCase):
    '''
    Performance monitoring and parameter refinement for mnk bots
    '''

    def setUp(self):
        '''
        Reset some of the mcts constants
        :return:
        '''
        cfg.reset()

    def test_mcts_consts(self):
        '''
        Collect data on the mcts algo as configured in cfg.py
        Other tests in this script vary the params and collect data
        :return:
        '''
        print('Skipping mcts consts (uncomment to manually run)')
        return
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts.csv', 'w') as csv:
            csv.write(f'player1_wins,player2_wins,ties,player1_pct,p2_pct,tie_pct,mcts_loops,uct_const,m,n,k\n')
            for sim_num in range(1):
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
                    cfg.uct_const,
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')
                print(f'MCTS (default): p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_uct_const(self):
        '''
        Collect game data for varying constants in the uct algo
        Generic algo default is usually square root of 2
        :return:
        '''
        print('Skipping mcts uct consts (uncomment to manually run)')
        return
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_uct.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,uct_const,m,n,k\n')
            for uct_val in [1., 1.1, 1.2, 1.4, 2., 3]:
                cfg.uct_const = uct_val
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
                    cfg.uct_const,
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')

                print(f'MCTS (uct const = {uct_val}): p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_mcts_loops(self):
        '''
        Collect game data for varying loop count in the mcts main loop
        :return:
        '''
        print('Skipping mcts loops (uncomment to manually run)')
        return
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_loop_count.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,uct_const,m,n,k\n')
            for loop_count in [50, 250, 500, 1000]:
                cfg.max_mcts_loops = loop_count
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
                    cfg.uct_const,
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')

                print(f'MCTS (loop count = {loop_count}): p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_selection_policy(self):
        '''
        Collect game data for varying constants in the algo that selects which child node to select
        :return:
        '''
        print('Skipping selection data collection, policy is significantly better than random')
        return

        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_select_chance.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,random_pct,m,n,k\n')
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
                    cfg.select_random_chance,
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')

                print(f'\nrandom_pct = {random_pct}\n')
                print(f'MCTS (selection ratio={random_pct}: p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_expansion_policy(self):
        '''
        Collect game data for varying constants in the algo that selects which square to expand from an unexplored node
        :return:
        '''
        print('Skipping mcts expansion (uncomment to manually run)')
        return
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_varying_expand_chance.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,mcts_loops,random_pct,m,n,k')
            for random_pct in [0, 0.25, 0.5, 0.75, 1]:
                cfg.expand_random_chance = random_pct
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
                print(f'MCTS (expand rand pct)={random_pct}: p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_ab_basic(self):
        '''
        Collect data on the alpha-beta algo in basic configuration
        Other tests in this script may vary the params and collect data
        :return:
        '''
        print('Skipping ab basic (uncomment to manually run)')
        return
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/alpha-beta.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,m,n,k\n')
            for sim_num in range(1):
                player1_wins, player2_wins, ties = ab_vs_ab(iterations, m, n, k)

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
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')
                print(f'AB vs AB: p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_mcts_vs_ab(self):
        '''
        Collect data on the mcts algo vs alpha-beta
        Other tests in this script may vary the params and collect data
        :return:
        '''
        print('Skipping mcts vs ab (uncomment to manually run)')
        return
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/mcts_vs_ab.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,m,n,k\n')
            for sim_num in range(1):
                player1_wins, player2_wins, ties = mcts_vs_ab(iterations, m, n, k)

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
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')
                print(f'MCTS vs AB: p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_ab_vs_mcts(self):
        '''
        Collect data on the ab vs mcts
        Other tests in this script may vary the params and collect data
        :return:
        '''
        print('Skipping ab vs mcts (uncomment to manually run)')
        return
        iterations = cfg.data_collection_loops
        m = 3
        n = 3
        k = 3

        with open('data/ab_vs_mcts.csv', 'w') as csv:
            csv.write(f'p1_wins,p2_wins,ties,p1_pct,p2_pct,tie_pct,m,n,k\n')
            for sim_num in range(1):
                player1_wins, player2_wins, ties = ab_vs_mcts(iterations, m, n, k)

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
                    m,
                    n,
                    k]
                                 ])
                csv.write(f'{line}\n')
                print(f'AB vs MCTS: p1 wins {p1_pct}% p2 wins {p2_pct}% ties {tie_pct}%')

    def test_collect_report_data(self):
        '''
        Collect data for various board sizes
        :return:
        '''
        print('Collecting report data')
        iterations = cfg.data_collection_loops

        # start log new each time, only add headers
        filename = 'data/report_numbers.csv'
        # with open(filename, 'w') as csv:
        #     csv.write(f'm,n,k,p1,p2,p1_pct,p2_pct,tie_pct,games,p1_avg_runtime,p2_avg_runtime\n')

        print(f'MCTS Loops={cfg.max_mcts_loops}')

        for m, n in [(3, 3), (3, 4), (4, 4), (5, 4), (5, 5), (6, 6), (7, 7)]:
        # for m, n in [(6, 6)]:
            for k in range(3, m + 1):  # test for board to require 3 to m cells in a row to win
            # for k in [3]:
                if k > m or k > n:  # skip cases where board cannot support winning condition
                    continue

                print(f'Running {iterations} for each matchup with m={m}, n={n}, k={k}')
                # # mcts vs mcts
                # print('mcts vs mcts')
                # bot_vs_bot(mcts_new, mcts_new, iterations, m, n, k, filename)

                # print('mcts vs ab')
                bot_vs_bot(mcts_new, ab_bot, iterations, m, n, k, filename)

                # # ab vs ab
                # print('ab vs ab')
                # bot_vs_bot(ab_bot, ab_bot, iterations, m, n, k, filename)

                # print('ab vs mcts')
                bot_vs_bot(ab_bot, mcts_new, iterations, m, n, k, filename)

        # continue_run = input(f'Completed m={m}, k={k}, continue?')
        # if continue_run.lower() != 'y':
        #     break

        print(f'DONE: report {filename}')
    #
    # def test_collect_report_data_mcts(self):
    #     '''
    #     Collect data for mcts vs mcts with different loop count per player
    #     :return:
    #     '''
    #     print('Collecting report data')
    #     iterations = cfg.data_collection_loops
    #     # m = 4
    #     # n = 4
    #     # k = 3
    #
    #     # start log new each time, only add headers
    #     filename = 'data/report_numbers_mcts_loop_difference2.csv'
    #     with open(filename, 'w') as csv:
    #         csv.write(f'm,n,k,p1,p2,p1_pct,p2_pct,tie_pct,games,p1_avg_runtime,p2_avg_runtime,p1_max_loops,p2_max_loops\n')
    #
    #     for m, n in [(3, 3), (3, 4), (4, 4), (5, 4), (5, 5), (6, 6), (7, 7)].__reversed__():
    #         for k in range(3, m):           # test for board to require 3 to 6 cells in a row to win
    #             if k > m or k > n:                   # skip cases where board cannot support winning condition
    #                 continue
    #
    #             for max_loops in [
    #                 # {1: 10, 2: 50},
    #                 # {1: 50, 2: 10},
    #                 # {1: 10, 2: 100},
    #                 # {1: 100, 2: 10},
    #                 # {1: 100, 2: 1000},
    #                 # {1: 1000, 2: 100},
    #                 {1: 5, 2: 500},
    #                 {1: 500, 2: 5},
    #             ]:
    #
    #                 print(f'Running {iterations} for each {m}x{n} (k={k}) with p1 loops={max_loops[1]}, p2 loops={max_loops[2]}')
    #                 bot_vs_bot(mcts_new, mcts_new, iterations, m, n, k, filename, max_loops)


            
if __name__ == '__main__':
    unittest.main()
