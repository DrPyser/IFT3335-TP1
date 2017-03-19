import copy
import operator
from functools import reduce

class Sudoku:
    def __init__(self, line):
        self.sudoku = []
        self.fixed = []
        line = list(map(int, line.strip()))
        if len(line) != 81:
            raise ValueError('Must be exactly 81 characters')
        line_number = []
        for (i, n) in enumerate(line):
            line_number.append(n)
            if n != 0:
                self.fixed.append((int(i/9), i % 9))
            if ((i + 1) % 9) == 0:
                self.sudoku.append(line_number)
                line_number = []
        self._generate_possibilities()
            
    def get_line(self, l):
        return self.sudoku[l]
               
    def get_column(self, c):
        column = []
        for i in range(9):
            column.append(self.sudoku[i][c])
        return column
    
    def get_square(self, l, c):
        min_l = int(l/3)*3
        min_c = int(c/3)*3
        
        square = []
        for i in range(min_l, min_l + 3):
            for j in range(min_c, min_c + 3):
                square.append(self.sudoku[i][j])
        return square

    def __getitem__(self, i):
        return self.sudoku[i]

    def get(self, i, j):
        return self.sudoku[i][j]
    
    def set(self, i, j, x):
        new = copy.deepcopy(self)
        new.sudoku[i][j] = x
        return new

    def iter_lines(self):
        for row in self.sudoku:
            yield row

    def iter_columns(self):
        for i in range(9):
            yield map(lambda x: x[i], self.sudoku)

    def iter_blocks(self):
        for b in range(9):
            yield [self.sudoku[i][j] for i in range(b//3*3,b//3*3+3) for j in range(b*3%9, (b*3+3)//3)]    

    def iter_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.get(i,j) == 0:
                    yield (i,j)
            
    def is_full(self):
        return 0 not in reduce(operator.add, self.sudoku)

    def possible_values(self, i, j):
        #return possible values for position (i,j)
        if (i,j) not in self.fixed:
            values = set(range(1,10)) - set(self.get_line(i)) - set(self.get_column(j)) - set(self.get_square(i,j))
            for x in values:
                yield x
            if self.get(i,j) != 0:
                yield self.get(i,j)
                
    def _generate_possibilities(self):
        self.possibilities = dict()
        # Naive possibilities (only consider square, row and column)
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0:
                    self.possibilities[(i, j)] = set(range(1,10)) - set(self.get_line(i)) - set(self.get_column(j)) - set(self.get_square(i,j))
                    
        # Hidden unique: find unique numbers in...
        # Row
        for r in range(9):
            possib = set(range(1, 10)) - set(self.get_line(r))
            if not possib:
                continue
            cases = []
            for c in range(9):
                if self.sudoku[r][c] == 0:
                    cases.append((r, c))
            for p in possib:
                tmp = None
                for case in cases:
                    if p in self.possibilities[case]:
                        if tmp is None: # First to have p as a possibility
                            tmp = case
                        else: # Not the first - make it None and stop looking for that possibility
                            tmp = None
                            break
                if tmp is not None:
                    self.possibilities[tmp] = set([p])
        # Column
        for c in range(9):
            possib = set(range(1, 10)) - set(self.get_column(c))
            if not possib:
                continue
            cases = []
            for r in range(9):
                if self.sudoku[r][c] == 0:
                    cases.append((r, c))
            for p in possib:
                tmp = None
                for case in cases:
                    if p in self.possibilities[case]:
                        if tmp is None: # First to have p as a possibility
                            tmp = case
                        else: # Not the first - make it None and stop looking for that possibility
                            tmp = None
                            break
                if tmp is not None:
                    self.possibilities[tmp] = set([p])
        # Square
        for rs in range(9, 3):
            for cs in range(9, 3):
                possib = set(range(1, 10)) - set(self.get_square(rs, cs))
                if not possib:
                    continue
                cases = []
                for r in range(rs, rs+3):
                    for c in range(cs, cs+3):
                        if self.sudoku[r][c] == 0:
                            cases.append((r, c))
                for p in possib:
                    tmp = None
                    for case in cases:
                        if p in self.possibilities[case]:
                            if tmp is None: # First to have p as a possibility
                                tmp = case
                            else: # Not the first - make it None and stop looking for that possibility
                                tmp = None
                                break
                    if tmp is not None:
                        self.possibilities[tmp] = set([p])

    def swap(self, i, j, l, k):
        new = copy.deepcopy(self)
        new.sudoku[i][j], new.sudoku[l][k] = new.sudoku[l][k], new.sudoku[i][j]
        return new

    def __str__(self):
        s = '+---------'*3 + '+\n'
        for i in range(9):
            s += '|'
            for j in range(9):
                n = self.sudoku[i][j]
                s += ' ' + (' ' if n == 0 else str(n)) + ' '
                if j % 3 == 2:
                    s += '|'
            s += '\n'
            if i % 3 == 2:
                s += '+---------'*3 + '+\n'
        return s

    def __lt__(self, other):
        return id(self) < id(other)

    def __gt__(self, other):
        return id(self) > id(other)

    def __eq__(self, other):
        return (isinstance(other, type(self)) and self.sudoku == other.sudoku)

    def __hash__(self):
        return int("".join(map(str, reduce(lambda x, y:x+y, self.sudoku))))
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    # @static
    # def from_line(line):
    #     line = list(map(int, line.strip()))
    #     if len(line) != 81:
    #         raise ValueError('Must be exactly 81 characters')
    #     line_number = []
    #     for (i, n) in enumerate(line):
    #         line_number.append(n)
    #         if n != 0:
    #             self.fixed.append((int(i/9), i % 9))
    #         if ((i + 1) % 9) == 0:
    #             self.sudoku.append(line_number)
    #             line_number = []
    
