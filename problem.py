import search
from sudoku import Sudoku
import random
import copy

def has_redundancy(iterable):
    return len(list(iterable)) > len(set(iterable))

class SudokuProblem(search.Problem):
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
        print("Node tested: id %s"%(id(state)))
        test = lambda x: set(x) == set(range(1,10))#fonction de test
        return (state.is_full()
                and all(map(test, state.iter_lines()))#vérification des lignes
                and all(map(test, state.iter_columns()))#vérification des colonnes
                and all(map(test, state.iter_blocks())))#vérification des blocs


    def value(self, state):
        one_to_nine = set(range(1, 10))
        s = 0
        for i in range(0, 9):
            s += len(one_to_nine - set(state.get_line(i)))
            s += len(one_to_nine - set(state.get_column(i)))
        return -s


class LewisSudokuProblem(search.Problem):
    def __init__(self, initial_sudoku, goal=None):
        self.goal = None
        initial = copy.deepcopy(initial_sudoku)
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                numbers = set(range(1, 10)) - set(initial.get_square(i, j))
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        if initial.sudoku[x][y] == 0:
                            n = random.choice(list(numbers))
                            initial.sudoku[x][y] = n
                            numbers -= set([n])
        self.initial = initial
        
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
        (i, j), (k, l) = action
        
        # state_copy = copy.deepcopy(state)
        # state_copy.sudoku[x1][y1], state_copy.sudoku[x2][y2] = state_copy.sudoku[x2][y2], state_copy.sudoku[x1][y1]
        return state.swap(i,j,k,l)
    
    def goal_test(self, state):
        test = self.value(state) == 0
        print("Goal!") if test else print("Goal test failed.")
        return test
    
    def value(self, state):
        one_to_nine = set(range(1, 10))
        s = 0
        for i in range(0, 9):
            s += len(one_to_nine - set(state.get_line(i)))
            s += len(one_to_nine - set(state.get_column(i)))
        return -s

def sim(t):
    p = 0.8*0.99**t
    if p < 0.01:
        return 0
    return p    

def true_goal_test(state):
    test = lambda x: set(x) == set(range(1,10))
    return (state.is_full()
            and all(map(test, state.iter_lines()))
            and all(map(test, state.iter_columns()))
            and all(map(test, state.iter_blocks())))
    
    
