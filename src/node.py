# Node.py
# Contains the class Node to represent the state space tree in BnB

class Node:
    def __init__(self, puzzle, parent=None, depth=0, move=""):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.depth = depth