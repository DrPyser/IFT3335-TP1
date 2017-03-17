from copy import deepcopy
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
        new = deepcopy(self)
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
            yield [self.sudoku[i][j] for i in range(b//3*3,b//3*3+3) for j in range(b*3, b*3+3)]

    def is_full(self):
        return 0 not in reduce(operator.add, self.sudoku)

    def possible_values(self, i, j):
        #return possible values for position (i,j)
        if (i,j) not in self.fixed:
            values = set(range(1,10)) - set(self.get_line(i)) - set(self.get_column(j)) - set(self.get_square(i,j))
            for x in values:
                yield x
        
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
    
