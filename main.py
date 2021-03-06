#!/usr/bin/env python3

from search import (depth_first_tree_search, best_first_greedy_tree_search, best_first_tree_search, best_first_graph_search, hill_climbing, simulated_annealing, compare_searchers, InstrumentedProblem)
from utils import name
from problem import *
from sudoku import Sudoku

import sys

if __name__ == '__main__':
    sudokus = []
    for line in open("100sudoku.txt"):
        sudokus.append(Sudoku(line.strip()))

    #heuristique: nombre de possibilités permettant cet état - 1
    def h1(node):
        if node.action:
            (i,j,val) = node.action
            possibilities = list(node.state.possible_values(i,j))
            return len(possibilities) - 1
        else:
            return 0

    def h2(node):
        #count = 0
        for (i,j) in node.state.iter_empty_cell():
            if len(list(node.state.possible_values(i,j))) == 0:
                return None
        if node.action:
            (i,j,val) = node.action
            possibilities = list(node.state.possible_values(i,j))
            return len(possibilities) - 1
        return 0

        
    choices = {
        'depth_first': depth_first_tree_search,
        # 'best_first_uniform': uniform_cost_tree_search,
        'best_first_h1': lambda x: best_first_tree_search(x, h1),
        'best_first_h2': lambda x: best_first_tree_search(x, h2),
        'best_first_greedy_h1': lambda x: best_first_greedy_tree_search(x, h1),
        'best_first_greedy_h2': lambda x: best_first_greedy_tree_search(x, h2),
        'best_first_h3': lambda x: best_first_tree_search(x, h3),
        'best_first_greedy_h3': lambda x: best_first_greedy_tree_search(x, h3),
        'best_first_graph_h1': lambda x: best_first_graph_search(x, h1),
        'best_first_graph_h2': lambda x: best_first_graph_search(x, h2),
        'hill_climbing': lambda x: hill_climbing(x),
        'annealing': lambda x: simulated_annealing(x, schedule=sim)
    }

#    print(sys.argv)
    searchers = sys.argv[1:]
    lewisProblems = map(LewisSudokuProblem, sudokus)
    naiveProblems = map(SudokuProblem, sudokus)
    #csv header
    print("problem,searcher,explored,states,tests,solution,value")
    for (i, (p1, p2)) in enumerate(zip(lewisProblems,naiveProblems)):        
        #print("Initial state:")        

        for s in searchers:
            if s in ['hill_climbing', 'annealing']:
                ip = InstrumentedProblem(p1)
            else:
                ip = InstrumentedProblem(p2)

            #print(ip.initial)
            
            result = choices[s](ip)
            print("%d,%s,%d,%d,%d,%s,%s"%(i,s,ip.succs,ip.states,ip.goal_tests,
                                          bool(result) and true_goal_test(result.state),
                                          ip.value(result.state)) if result else "")

            # if result:
            #     print("Stats: %s"%(ip))
            #     print("Result:\n %s"%(result.state))
            #     print("Is a solution: %s"%(ip.goal_test(result.state)))
            #     print("value: %d"%(ip.value(result.state)))
            # else:
            #     print("No solution found.")
                
            
    # print(sudokus[0].initial)
    # best_first_tree_search(sudokus[0], h1)
    #print(hill_climbing(LewisSudokuProblem(sudokus[0])))
    
    
    
