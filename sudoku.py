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
