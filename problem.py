from search import (Problem)
from sudoku import Sudoku
import copy
import random

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

class LewisSudokuProblem(Problem):

    def __init__(self, initial_sudoku, goal=None):
        self.goal = None

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                numbers = set(range(1, 10)) - set(initial_sudoku.get_square(i, j))
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        if initial_sudoku.sudoku[x][y] == 0:
                            n = random.choice(list(numbers))
                            initial_sudoku.sudoku[x][y] = n
                            numbers -= set([n])
        self.initial = initial_sudoku

    def actions(self, state):
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square_non_fixed = []
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        if (x, y) not in state.fixed:
                            square_non_fixed.append((x, y))
                while len(square_non_fixed) > 1:
                    s1 = square_non_fixed.pop()
                    for s2 in square_non_fixed:
                        yield (s1, s2)

    def result(self, state, action):
        (x1, y1), (x2, y2) = action
        state_copy = copy.deepcopy(state)
        state_copy.sudoku[x1][y1], state_copy.sudoku[x2][y2] = state_copy.sudoku[x2][y2], state_copy.sudoku[x1][y1]
        return state_copy

    def goal_test(self, state):
        return self.value(state) == 0

    def value(self, state):
        one_to_nine = set(range(1, 10))
        s = 0
        for i in range(0, 9):
            s += len(one_to_nine - set(state.get_line(i)))
            s += len(one_to_nine - set(state.get_column(i)))
        return -s
