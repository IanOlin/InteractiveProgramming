#vim : tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygame
from pygame.locals import * 
import time
from random import choice

#TODO split the model view and controller into different files maybe?

class PyGameTestView(object):
    """ This is a test view for my game"""
    def __init__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size, HWSURFACE|DOUBLEBUF|RESIZABLE)

    def draw(self):
        """ Draw the game to the pygame window """
        #self.screen.fill(pygame.Color('black')) #want to replace with image
        background = pygame.image.load('room2.png')
        self.screen.blit(pygame.transform.scale(background, size), (0,0))
        pygame.display.flip()
        # see pygame window resizing to find docs for this. current broked
        #self.screen.blit(background, (0,0))
        #draw the rest of the game
        #pygame.display.update()

class PyGameTestModel(object):
    """This is a test model for my game"""
    def __init__(self, width, height):
        self.height = height
        self.width = width

        # Define things like brick height and width here for BB
        # Also creates list of bricks, paddle, and ball

    def update(self):
        """ update the model state"""
        # self.ball.update() is what BB calls. 
        # should call game objects update functions

# Here Paul defined some other objects like Ball and Paddle 

class PyGameTestController(object):
    """This is a test controller for my object"""
    def __init__(self, model):
        self.model = model

    def update(self):
        """ Look for keypresses and modify positions"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            # do a thing
            pass
if __name__ == '__main__':
    pygame.init()
    VideoInfo = pygame.display.Info()#gets the display info
    size = (VideoInfo.current_w, VideoInfo.current_h)#sets the game to fill creen

    model = PyGameTestModel(size[0], size[1])
    view = PyGameTestView(model, size)
    controller = PyGameTestController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type ==QUIT:
                running = False
        model.update()
        controller.update()
        view.draw()
        time.sleep(.001)

