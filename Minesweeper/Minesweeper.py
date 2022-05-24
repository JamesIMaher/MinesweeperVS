from itertools import filterfalse
import sys
import random
from telnetlib import SE
import pygame

class Board:

    board_width = 9
    board_height = 9
    numBombs = 10

    def __init__ (self):
        self.board_array = self.createBoard(self.board_width, self.board_height)
        #self.printBoardText(self.board_height, self.board_height)
        self.placeBombs()
        self.determineCounts(self.board_width, self.board_height)
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
            #for y in range (height): 
            print(*self.board_array[x], sep="\t", end="\n")
            #print()

    def placeBombs (self):
        for bomb in range(self.numBombs):
            randX = random.randint(0,(self.board_width-1))
            randY = random.randint(0,(self.board_height-1))
            self.board_array[randX][randY] = -1

    def determineCounts (self, width, height):
        #Determine how many bombs are surrounding each square
        for x in range(width):
            for y in range(height):
                if self.board_array[y][x] != -1: #There is not a mine in this square
                    bombCount = 0 #Start a count of each cell
                    #check left
                    if self.isValidBombCell(y-1,x+1):
                        bombCount += 1
                    if self.isValidBombCell(y-1,x):
                        bombCount += 1
                    if self.isValidBombCell(y-1,x-1):
                        bombCount += 1
                    #Check top and bottom
                    if self.isValidBombCell(y,x+1):
                        bombCount += 1
                    if self.isValidBombCell(y,x-1):
                        bombCount += 1
                    #Check right
                    if self.isValidBombCell(y+1,x+1):
                        bombCount += 1
                    if self.isValidBombCell(y+1,x):
                        bombCount += 1
                    if self.isValidBombCell(y+1,x-1):
                        bombCount += 1
                    self.board_array[y][x] = bombCount #set the board array to hold the number of bombs surrounding each cell

    def isValidBombCell (self, yPos, xPos):
        if xPos >= self.board_width or xPos < 0:
            return False
        elif yPos >= self.board_height or yPos < 0:
            return False
        else: #Cell is valid, check for bomb
            if self.board_array[yPos][xPos] == -1:
                return True #Bomb found
            else:
                return False #No bomb


class Screen:

    def __init__ (self,width,height):
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])

    def initialize_screen (self):
        self.screen.fill((255, 255, 255))
        #pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
        pygame.display.flip()

class Cell (pygame.sprite.Sprite):
    
    def __init__(self):
        super(Cell, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
    
    def draw_sprite (self, screen):
        screen.screen.blit(self.surf, (250, 250))
        pygame.display.flip()



#pygame.init()
game_board = Board()
#screen = Screen(500, 500)
#cell = Cell()

#running = True
#while running:

#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False

#    cell.draw_sprite(screen)
#    screen.initialize_screen()
    

#pygame.quit()
