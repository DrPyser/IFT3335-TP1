class Sudoku:
    
    def __init__(self, line=None):
        self.sudoku = []
        if line is None:
            for _ in range(9):
                self.sudoku.append(9*[0])
        else:
            for i in range(9):
                self.sudoku.append(list(map(int, list(line[9*i:9*i+9]))))  
            
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
