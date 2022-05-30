#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

uct_const = 1.1 # math.sqrt(2)            # constant term in uct evaluation
max_mcts_loops = 500               # number of times to run mcts at each eval

# dial for which node is selected; if random number between 0 and 1 is greater than this, random node
# will be selected; else best node will be selected using uct policy
# this var was used to collect data, is not needed though (policy performed much better)
# select_random_chance = 1

# dial for which node is expanded; if random number between 0 and 1 is greater than this, random node
# will be generated; else best node will be expanded using policy
expand_random_chance = 0.9 # .3
DEBUG = False                       # set to True for verbose debugging messages
show_each_move = False

data_collection_loops = 150         # default number of loops for each data collection test


mcts_time_filname = 'mctsTime.txt'

def reset():
    '''
    Reset mcts constants. Useful for data collection runs where some tests may change constants
    :return:
    '''
    global uct_const, max_mcts_loops, expand_random_chance

    uct_const = 1.1
    max_mcts_loops = 500
    expand_random_chance = 0.9

