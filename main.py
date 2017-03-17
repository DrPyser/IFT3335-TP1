#!/usr/bin/env python3

from search import (depth_first_tree_search, best_first_tree_search, hill_climbing, simulated_annealing, compare_searchers)
from problem1 import SudokuProblem
from sudoku import Sudoku

import sys

if __name__ == '__main__':
    sudokus = []
    for line in open("100sudoku.txt"):
        sudokus.append(SudokuProblem(Sudoku(line.strip())))

    #heuristique: nombre de possibilités permettant cet état - 1
    def h1(node):
        if node.action:
            (i,j,val) = node.action 
            possibilities = (set(range(1,10)) - set(node.state.get_line(i)) - set(node.state.get_column(j))
                         - set(node.state.get_square(i,j)))
            return len(possibilities) - 1
        else:
            return 0


    choices = {
        'depth_first': depth_first_tree_search,
        # 'best_first_uniform': uniform_cost_tree_search,
        'best_first_h1': lambda x: best_first_tree_search(x, h1),
        'best_first_h2': lambda x: best_first_tree_search(x, h2),
        'best_first_rec_h1': lambda x: recursive_best_first_search(x, h1),
        'best_first_rec_h2': lambda x: recursive_best_first_search(x, h2)
    }

    searchers = map(lambda x: choices[x], sys.argv[1:])
    compare_searchers(sudokus, header=["Searcher"], searchers=searchers)
    # print(sudokus[0].initial)
    # best_first_tree_search(sudokus[0], h1)
    

    
