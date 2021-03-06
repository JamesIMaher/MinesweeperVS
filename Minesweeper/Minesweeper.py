from itertools import filterfalse
from re import X
import sys
import random
from telnetlib import SE
#import pygame

class GameCell:

    probabilitiesMine = []

    def __init__ (self, xPos, yPos, board_width, board_height):
        self.xPos = xPos
        self.yPos = yPos
        self.bombPresent = False
        self.numSurroundingMines = 0
        self.visible = False
        self.board_width = board_width
        self.board_height = board_height

        #Initialize the probabilities of this cell being in each state
        self.initialize_y_prob()

    def initialize_y_prob(self):
        self.y_probs = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7:0.0, 8:0.0} #Probability of each state. Probability will be equal until the cell is selected.
        self.setNumValidSurroudingCells(self.board_width, self.board_height)
        #Keep probabilities 
        for key, values in self.y_probs.items():
           self.y_probs[key] = 1/9
        
    def setMine (self):
        self.bombPresent = True

    def countSurroundingMines (self, numMines):
        self.numSurroundingMines = numMines

    def userClicked (self):
        self.visible = True

    #Function that will set the Bayes probability for each cell.
    #surMines: List of the number of bombs in each surrounding mine. 
    #Funciton will add the number of bombs for each surrounding cell
    def setBayesProbability (self, surMines):
        print()

    #Function that will set the number of surrounding valid cells around the current cell. 
    #This will be the denominator in the the Bayes probability of the cell
    def setNumValidSurroudingCells (self, width, height):
        #If 2 conditions met, -5 valid cells. If 1 condition met, -3 valid cells 
        twoConditionsMet = 0
        if self.xPos - 1 < 0 or self.xPos + 1 > width:
            twoConditionsMet += 1;
        if self.yPos -1 < 0 or self.yPos + 1 > height:
            twoConditionsMet += 1;
        if twoConditionsMet == 1:
            self.numValidSurroundingCells = 5
        elif twoConditionsMet == 2:
            self.numValidSurroundingCells = 3
        else:
            self.numValidSurroundingCells = 8

class Board:
    

    def __init__ (self, width, height, numMines, visible):
        self.board_width = width
        self.board_height = height
        self.numMines = numMines
        self.board_array = []
        self.gameOver = False

        self.createBoard(self.board_width, self.board_height)
        #Initial Board Setup
        self.placeBombs()
        self.determineCounts(self.board_width, self.board_height)
        #Test print of the board (diagnostic)
        self.printBoardText(self.board_height, self.board_height) #print the board with all zeros
        #Print the user view of the board
        print()
        print()
        self.printUserBoardText()


    # Function to create the back-end array that will hold whether there is a bomb or not at each square.
    # Function will evolve to contain the number of bombs in surrounding squares and a graphical representation
    
    def createBoard (self, width, height):
        #Initialize the board to zeros. -1 will represent a bomb, number will represent the number of bombs in adjactent spaces.
        
        x = 0
        for y in range(height):
            new_row = []
            for x in range(width):
                new_cell = GameCell(x, y)
                #new_cell.setNumValidSurroudingCells(self.board_width, self.board_height)
                new_row.append(new_cell)
            self.board_array.append(new_row)

    #Prints the solution to the minesweeper board
    def printBoardText (self, width, height):
        for y in range(height):
            for x in range (width):
               #check if this cell should be shown to the user
                #if self.board_array[x][y].visible ==True:
                if self.board_array[y][x].bombPresent == True:
                    print("-1\t", end='')
                else:
                    #print(self.board_array[y][x].numSurroundingMines + "\t")
                    print(self.board_array[y][x].numSurroundingMines, end='')
                    print("\t", end='')
            print("\n")
                #print(*self.board_array[y][x], sep="\t", end="\n")

    #Prints the user view of the minesweeper board
    def printUserBoardText (self):
        for y in range (self.board_height):
            for x in range (self.board_width):
                if self.board_array[y][x].visible == True:
                    if self.board_array[y][x].bombPresent == True:
                        print ("-1", end='')
                    else:
                        print (self.board_array[y][x].numSurroundingMines, end='')
                    print("\t", end='')
                else:
                    print ("X\t", end='')
            print()

    def placeBombs (self):
        for bomb in range(self.numMines):
            randX = random.randint(0,(self.board_width-1))
            randY = random.randint(0,(self.board_height-1))
            self.board_array[randY][randX].setMine()

    def determineCounts (self, width, height):
        #Determine how many bombs are surrounding each square
        for y in range(height):
            for x in range(width):
                if self.board_array[y][x].bombPresent == False: #There is not a mine in this square
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
                    self.board_array[y][x].numSurroundingMines = bombCount #set the board array to hold the number of bombs surrounding each cell

    def isValidBombCell (self, xPos, yPos):
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
        self.gameOver = False

        if userInput == "small":
            self.game_board = Board(9, 9, 10,False)

        elif userInput == "medium":
            self.game_board = Board(16, 16, 40,False)

        elif userInput == "large":
            self.game_board = Board(30, 16, 99, False)

        else:
            print("error")

    def userPickCell(self):
        x_pos = input("Enter the X (horizontal position) of the cell you would like to select: ")
        y_pos = input("Enter the Y (vertical position) of the cell you would like to select: ")
        print()

        #Make the cell visible
        self.game_board.board_array[int(y_pos)][int(x_pos)].visible = True
        
        #Check if this is a mine
        if self.game_board.board_array[int(y_pos)][int(x_pos)].bombPresent == True:
            self.gameOver = True
            return
        


        

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
#Main game loop
while user_input.gameOver == False:
    user_input.userPickCell()
    user_input.game_board.printUserBoardText()
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
