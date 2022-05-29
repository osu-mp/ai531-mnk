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
