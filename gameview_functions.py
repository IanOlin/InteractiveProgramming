import pygame
from pygame.locals import *

class GameView(object):
    """this view handles displaying most of the things.

    attributes: model, screen"""
    def __init__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size)
        pygame.mixer.music.load('sounds/TheDarkLake.mp3') #this music plays
        pygame.mixer.music.play(-1)


    def draw(self):
        """ Draw the game to the pygame window"""
        background = pygame.image.load('images/room2.png').convert()
        scaled_bg = pygame.transform.scale(background, size)
        self.screen.blit(scaled_bg, (0,0))
        char = self.model.char.image
        self.screen.blit(char, (self.model.char.x,self.model.char.y))
        pygame.draw.rect(self.screen, (255, 200, 0), self.model.char.rect)
        # draws a yellow box where the rect is
        pygame.display.flip()