#vim : tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygame
from pygame.locals import *
import time
from random import choice

#TODO split the model view and controller into different files maybe?

class GameView(object):
    """ This is a test view for my game"""
    def __init__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size, HWSURFACE|DOUBLEBUF|RESIZABLE)

    def draw(self):
        """ Draw the game to the pygame window """
        background = pygame.image.load('images/room2.png')
#        self.screen.blit(pygame.transform.scale(background, size), (0,0))
        self.screen.blit(background, (0,0))
#        char = pygame.image.load('character.png')
        char = self.model.char.img
#       should algorithmically be scaling character to the same scaling
#       ratio that the bg gets scaled. For now, I won't.
#        charR = pygame.transform.scale(char, (100,100))
    #   roughtly the correct size
        charR = char
    # worth noting that the character image is shit with a huge border
        self.screen.blit(charR, (self.model.char.x,self.model.char.y)) #that tuple should be based on the char model
        pygame.display.flip()
        #draw the rest of the game
        #pygame.display.update()

class GameModel(object):
    """This is a test model for my game"""
    def __init__(self, width, height):
        self.height = height
        self.width = width

        # Define things like brick height and width here for BB
        # Also creates list of bricks, paddle, and ball
        self.char = Character(0,0)
        self.char.set_image()

    def update(self):
        """ update the model state"""
        # self.ball.update() is what BB calls.
        # should call game objects update functions


# Here Paul defined some other objects like Ball and Paddle
class Character(object):
    "represents the character"
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #should probably do the image loading in here
    def set_image(self, imagename = 'images/character.png'):
        self.img = pygame.image.load(imagename)

class GameController(object):
    """This is a test controller for my object"""
    def __init__(self, model):
        self.model = model

    def update(self):
        """ Look for keypresses and modify positions"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.model.char.x -= 5
        if pressed[pygame.K_RIGHT]:
            self.model.char.x += 5
        if pressed[pygame.K_UP]:
            self.model.char.y -= 5
            self.model.char.set_image()
        if pressed[pygame.K_DOWN]:
            self.model.char.y += 5 
            self.model.char.set_image('images/character-back.png')
#TODO: build a list for each direction, on pres, iterate through the set of images for that direction.
if __name__ == '__main__':
    pygame.init()
    #VideoInfo = pygame.display.Info()#gets the display info
    #size = (VideoInfo.current_w, VideoInfo.current_h)#sets the game to fill creen
    #That works, but it doesn't geneate in the right aspect ratio
   # size = (640, 480)
    size = (320,240)
    model = GameModel(size[0], size[1])
    view = GameView(model, size)
    controller = GameController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type ==QUIT:
                running = False
        model.update()
        controller.update()
        view.draw()
        time.sleep(.1)
