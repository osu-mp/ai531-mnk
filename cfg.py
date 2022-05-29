#!/usr/bin/python3

# AI 531 - m,n,k
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

uct_const = 1.2 # math.sqrt(2)            # constant term in uct evaluation
max_mcts_loops = 200               # number of times to run mcts at each eval

# dial for which node is expanded; if random number between 0 and 1 is greater than this, random node
# will be generated; else best node will be expanded using policy
expand_random_chance = 0.5
DEBUG = False                       # set to True for verbose debugging messages

data_collection_loops = 500         # default number of loops for each data collection test
