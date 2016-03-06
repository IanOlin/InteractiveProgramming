#vim : tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygame
from pygame.locals import *
import time
from random import choice

#TODO split the model view and controller into different files maybe?

class GameView(object):
    """this view handles displaying most o the things"""
    def __init__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size, HWSURFACE|DOUBLEBUF|RESIZABLE)

    def draw(self):
        """ Draw the game to the pygame window """
        background = pygame.image.load('images/room2.png')
#        self.screen.blit(pygame.transform.scale(background, size), (0,0))
        scaled_bg = pygame.transform.scale(background, size)
        self.screen.blit(scaled_bg, (0,0))
        char = self.model.char.img
        self.screen.blit(char, (self.model.char.x,self.model.char.y))
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
        #TODO:consider  actually having the character model update in here rather than in the controlller.
        # self.ball.update() is what BB calls.
        # should call game objects update functions


# Here Paul defined some other objects like Ball and Paddle
class Character(object):
    """represents the character, sets it's position and image"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def set_image(self, imagename = 'images/up2.png'):
        """ loads a given image as the character model"""
        self.img = pygame.image.load(imagename)

class GameController(object):
    """This is the controller for the game. It contains all the animation data """
    def __init__(self, model):
        """ initializes the model and all of the image banks for the character"""
        self.model = model
        self.leftimages =  ['images/left1.png',
                            'images/left2.png',
                            'images/left3.png',
                            'images/left4.png']
        self.li = 0
        self.upimages =    ['images/up1.png',
                            'images/up2.png',
                            'images/up3.png',
                            'images/up4.png']
        self.ui = 0
        self.downimages =  ['images/down1.png',
                            'images/down2.png',
                            'images/down3.png',
                            'images/down4.png']
        self.di = 0
        self.rightimages = ['images/right1.png',
                            'images/right2.png',
                            'images/right3.png',
                            'images/right4.png']
        self.ri = 0

    def update(self):
        """ Updates the game state based on keypresses. Also animates walking right now"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.model.char.x -= 5
            self.model.char.set_image(self.leftimages[self.li])
            self.li = (self.li + 1)%4
        if pressed[pygame.K_RIGHT]:
            self.model.char.x += 5
            self.model.char.set_image(self.rightimages[self.ri])
            self.ri = (self.ri + 1)%4
        if pressed[pygame.K_UP]:
            self.model.char.y -= 5
            self.model.char.set_image(self.upimages[self.ui])
            self.ui = (self.ui + 1)%4
        if pressed[pygame.K_DOWN]:
            self.model.char.y += 5 
            self.model.char.set_image(self.downimages[self.di])
            self.di = (self.di + 1)%4
if __name__ == '__main__':
    pygame.init()
    #size = (VideoInfo.current_w, VideoInfo.current_h)#sets the game to fill creen
    #That works, but it doesn't geneate in the right aspect ratio
    size = (640, 480) # useful
    # size = (320,240)  #'native'
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
        time.sleep(.3)
