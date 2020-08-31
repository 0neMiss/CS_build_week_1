import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text = None,  colour = (73,73,73), hilightedColour = (189,189,189), function = None, params = None, mouse = None):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.colour = colour
        self.hilightedColour = hilightedColour
        self.function = function
        self.params = params
        self.adjacentCells = {}
        self.highlighted = False
        self.clicked = pygame.mouse.get_pressed()
        self.mouse = None




    def update(self, mouse):
        self.mouse =pygame.mouse.get_pos()
        if self.rect.collidepoint(self.mouse):
            self.highlighted = True

        else:

            self.highlighted = False
    def mouseInBox(self):
        if self.highlighted and self.clicked[0] == 1:

            self.click()



    def draw(self, window):
        
        if self.highlighted:
            self.image.fill(self.hilightedColour if self.highlighted else self.colour)
        window.blit(self.image, self.pos)

    #for handling if a button has been clicked, runs the function attached to the button
    def click(self):
        if self.params:
            self.functions(self.params)
        else:
            self.function()
