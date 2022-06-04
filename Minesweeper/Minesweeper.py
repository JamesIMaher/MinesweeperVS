from itertools import filterfalse
from re import X
import sys
import random
from telnetlib import SE
#import pygame

class GameCell:

    probabilitiesMine = []

    def __init__ (self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.bombPresent = False
        self.numSurroundingMines = 0
        self.visible = True

    def setMine (self):
        self.bombPresent = True

    def countSurroundingMines (self, numMines):
        self.numSurroundingMines = numMines

    def userClicked (self):
        self.visible = True

class Board:
    

    def __init__ (self, width, height, numMines, visible):
        self.board_width = width
        self.board_height = height
        self.numMines = numMines
        self.board_array = []
        self.createBoard(self.board_width, self.board_height)
        #Initial Board Setup
        self.placeBombs()
        self.determineCounts(self.board_width, self.board_height)
        #Test print of the board
        self.printBoardText(self.board_height, self.board_height) #print the board with all zeros


    # Function to create the back-end array that will hold whether there is a bomb or not at each square.
    # Function will evolve to contain the number of bombs in surrounding squares and a graphical representation
    
    def createBoard (self, width, height):
        #Initialize the board to zeros. -1 will represent a bomb, number will represent the number of bombs in adjactent spaces.
        
        x = 0
        for y in range(height):
            new_row = []
            for x in range(width):
                new_cell = GameCell(x, y)
                new_row.append(new_cell)
            self.board_array.append(new_row)

    def printBoardText (self, width, height):
        for y in range(height):
            for x in range (width):
               #check if this cell should be shown to the user
                if self.board_array[x][y].visible ==True:
                    if self.board_array[x][y].bombPresent == True:
                        print("-1\t", end='')
                    else:
                        #print(self.board_array[y][x].numSurroundingMines + "\t")
                        print(self.board_array[x][y].numSurroundingMines, end='')
                        print("\t", end='')
            print("\n")
                #print(*self.board_array[y][x], sep="\t", end="\n")


    def placeBombs (self):
        for bomb in range(self.numMines):
            randX = random.randint(0,(self.board_width-1))
            randY = random.randint(0,(self.board_height-1))
            self.board_array[randX][randY].setMine()

    def determineCounts (self, width, height):
        #Determine how many bombs are surrounding each square
        for x in range(width):
            for y in range(height):
                if self.board_array[x][y].bombPresent == False: #There is not a mine in this square
                    bombCount = 0 #Start a count of each cell
                    #check left
                    if self.isValidBombCell(x-1,y+1):
                        bombCount += 1
                    if self.isValidBombCell(x-1,y):
                        bombCount += 1
                    if self.isValidBombCell(x-1,y-1):
                        bombCount += 1
                    #Check top and bottom
                    if self.isValidBombCell(x,y+1):
                        bombCount += 1
                    if self.isValidBombCell(x,y-1):
                        bombCount += 1
                    #Check right
                    if self.isValidBombCell(x+1,y+1):
                        bombCount += 1
                    if self.isValidBombCell(x+1,y):
                        bombCount += 1
                    if self.isValidBombCell(x+1,y-1):
                        bombCount += 1
                    self.board_array[x][y].numSurroundingMines = bombCount #set the board array to hold the number of bombs surrounding each cell

    def isValidBombCell (self, yPos, xPos):
        if xPos >= self.board_width or xPos < 0:
            return False
        elif yPos >= self.board_height or yPos < 0:
            return False
        else: #Cell is valid, check for bomb
            if self.board_array[yPos][xPos].bombPresent == True:
                return True #Bomb found
            else:
                return False #No bomb

    def returnBoardNumber (self, yPos, xPos):
        return self.board_array[yPos][xPos]


class UserInteraction:

    def __init__ (self):
        userInput = input("Welcome to Minesweeper. Would you like a small, medium, or large board?\n")
        if userInput == "small":
            self.game_board = Board(9, 9, 10,False)

        elif userInput == "medium":
            self.game_board = Board(16, 16, 40,False)

        elif userInput == "large":
            self.game_board = Board(30, 16, 99, False)

        else:
            print("error")
        

#class Screen:

#    def __init__ (self,width,height):
#        pygame.init()
#        self.screen = pygame.display.set_mode([width, height])

#    def initialize_screen (self):
#        self.screen.fill((255, 255, 255))
#        #pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
#        pygame.display.flip()

#class Cell (pygame.sprite.Sprite):
    
#    def __init__(self):
#        super(Cell, self).__init__()
#        self.surf = pygame.Surface((75, 25))
#        self.surf.fill((0, 0, 0))
#        self.rect = self.surf.get_rect()
    
#    def draw_sprite (self, screen):
#        screen.screen.blit(self.surf, (250, 250))
#        pygame.display.flip()



#pygame.init()
user_input = UserInteraction()
#game_board = Board()
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
