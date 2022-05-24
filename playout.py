#!/usr/bin/python3

# AI 531 - m,n,k (MCTS)
# Wadood Alam
# Joe Nguyen
# Matthew Pacey


class Playout:
    '''
    Playout data used for Monte Carlo Tree Search
    Maintains number of wins and total games simulated
    '''

    def __init__(self, games=0, wins=0):
        self.games = games
        self.wins = wins

    def add_win(self):
        self.wins += 1

    def add_game(self):
        self.games += 1

    def get_win_ratio(self):
        if self.games == 0:                 # avoid divide by zero
            return 0.
        return self.wins / self.games

    def __str__(self):
        return f'{self.wins} / {self.games} ({self.get_win_ratio() * 100}%)'
