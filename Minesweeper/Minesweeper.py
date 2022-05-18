import sys
from unicodedata import bidirectional

class Board:

    board_width = 9
    board_height = 9


    def __init__ (self):
        self.board_array = self.createBoard(self.board_width, self.board_height)
        self.printBoardText(self.board_height, self.board_height)
    # Function to create the back-end array that will hold whether there is a bomb or not at each square.
    # Function will evolve to contain the number of bombs in surrounding squares and a graphical representation
    
    def createBoard (self, width, height):
        #Initialize the board to zeros. -1 will represent a bomb, number will represent the number of bombs in adjactent spaces.
        board_array = []
        for y in range(height):
           board_array.append([0] * width)
        return board_array

    def printBoardText (self, width, height):
        for x in range(width):
            for y in range (height): 
                print(self.board_array[x][y], end=" ")
            print()

game_board = Board()
