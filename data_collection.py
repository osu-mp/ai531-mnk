#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import unittest

from games import mcts_vs_mcts

import cfg

class MNKDataCollection(unittest.TestCase):
    '''
    Performance monitoring and parameter refinement for mnk bots
    '''

    def test_uct_const(self):
        '''
        Collect game data for varying constants in the uct algo
        Generic algo default is usually square root of 2
        :return:
        '''
        iterations = 50
        m = 3
        n = 3
        k = 3

        with open('uct.csv', 'w') as csv:
            csv.write(f'player1_wins,player2_wins,ties,player1_pct,player2_pct,tie_pct,mcts_loops,uct_const,m,n,k')
            for uct_val in [0.5, 1., 1.2, 1.4, 1.6, 1.8, 2., 2.5, 3]:
                cfg.uct_const = uct_val
                player1_wins, player2_wins, ties = mcts_vs_mcts(iterations, m, n, k)

                line = ','.join([str(val) for val in [
                    player1_wins,
                    player2_wins,
                    ties,
                    player1_wins / iterations * 100,
                    player2_wins / iterations * 100,
                    ties / iterations * 100,
                    cfg.max_mcts_loops,
                    uct_val,
                    m,
                    n,
                    k]
                ])
                csv.write(line)

                print(f'\nuct const = {uct_val}')
                print(line)


if __name__ == '__main__':
    unittest.main()
