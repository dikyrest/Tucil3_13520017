# puzzle.py
# Containing Puzzle class to represent states

import copy
class Puzzle:
    # Constructor
    def __init__(self, path):
        # Define board and size
        self.board = []
        self.n = 0

        f = open(path, "r")
        for line in f:
            self.board.append(list(map(lambda x : int(x), line.split())))
        
        self.n = len(self.board)

    # Find empty cell position
    # Returns : (row, colunn)
    def find_empty(self):
        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                if (value == self.n**2):
                    return (i,j)

    # Move empty cell to (r+dr, c+dc)
    def move(self, dr, dc):
        (r, c) = self.find_empty()
        if(r+dr>=0 and r+dr<self.n and c+dc>=0 and c+dc<self.n):
            moved_puzzle = copy.deepcopy(self)
            moved_puzzle.board[r][c], moved_puzzle.board[r+dr][c+dc] = moved_puzzle.board[r+dr][c+dc], moved_puzzle.board[r][c]
            return moved_puzzle
        else:
            return None

    # Test whether the puzzle is solvable or not, inversion, parity, total, and kurang(i) array 
    def is_solveable(self):
        # Get empty cell location
        (r, c) = self.find_empty()

        # Flatten board
        tmp = self.flattened_board()

        # Find empty cell parity
        x = (r+c) % 2

        sum = 0
        kurang_i = [0 for i in range(self.n**2)]
        for i in range(0,self.n**2):
            sum_ubin = 0
            for j in range(i+1,self.n**2):
                if(tmp[i]>tmp[j]):
                    sum+=1
                    sum_ubin+=1
            kurang_i[tmp[i]-1] = sum_ubin

        return (sum + x) % 2 == 0, sum, x, sum+x, kurang_i

    # Return flattened board
    def flattened_board(self):
        return [val for arr in self.board for val in arr]