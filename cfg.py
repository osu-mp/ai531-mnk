#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

uct_const = 1.2 # math.sqrt(2)            # constant term in uct evaluation
max_mcts_loops = 200               # number of times to run mcts at each eval
DEBUG = False                       # set to True for verbose debugging messages

data_collection_loops = 500         # default number of loops for each data collection test
