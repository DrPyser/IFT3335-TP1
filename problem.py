from search import (Problem)
from sudoku import Sudoku

def has_redundancy(iterable):
    return len(list(iterable)) > len(set(iterable))

class SudokuProblem(Problem):
    def __init__(self, initial):
        super().__init__(initial)

    def actions(self, state):
        for i in range(9):
            for j in range(9):
                if state.get(i,j) == 0:                    
                    for x in state.possible_values(i,j):
                        yield (i,j,x)

    def result(self, state, action):
        (i,j,x) = action
        return state.set(i,j,x)

    def goal_test(self, state):
        test = lambda x: x == set(range(1,10))
        return (state.is_full()
                and all(map(test, state.iter_lines()))
                and all(map(test, state.iter_columns()))
                and all(map(test, state.iter_blocks())))
    



    
