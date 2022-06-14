import pygame, sys

class BoardGUI:

    def __init__(self):
        pygame.init()
        self.surfObj = pygame.display.set_mode(size=(173,200))

class Box:

    def __init__ (self, boxPos):
        self.boxPos = boxPos
        self.status = 'hidden'

#Code for debugging

gui = BoardGUI()
testbox = Box()




