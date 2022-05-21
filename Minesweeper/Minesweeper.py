from itertools import filterfalse
import sys
import random
import pygame

class Board:

    board_width = 9
    board_height = 9
    numBombs = 10

    def __init__ (self):
        self.board_array = self.createBoard(self.board_width, self.board_height)
        self.printBoardText(self.board_height, self.board_height)
        self.placeBombs()
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

    def placeBombs (self):
        for bomb in range(self.numBombs):
            randX = random.randint(0,(self.board_width-1))
            randY = random.randint(0,(self.board_height-1))
            self.board_array[randX][randY] = -1

pygame.init()
game_board = Board()
screen = pygame.display.set_mode([500,500])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0,0,255), (250, 250), 75)

    pygame.display.flip()

pygame.quit()
