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
        scaled_bg = pygame.transform.scale(background, size)
        self.screen.blit(scaled_bg, (0,0))
        char = self.model.char.image
        self.screen.blit(char, (self.model.char.x,self.model.char.y))
        pygame.display.flip()

class GameModel(object):
    """This is a test model for my game"""
    def __init__(self, width, height):
        self.height = height
        self.width = width

        # Define things like brick height and width here for BB
        # Also creates list of bricks, paddle, and ball
        
        self.char = CharacterSprite(0,0)

        #self.char = Character(0,0)
        #self.char.set_image()

    def update(self, control=0):
        """ update the model state"""
        self.char.update(control)

class SpriteSheet(object):
    """Class used to grab images out of a sprite sheet."""
    def __init__(self, file_name= 'images/smallspritesheet.png'):
        self.sprite_sheet = pygame.image.load(file_name)
    def get_image(self, x, y, width, height):
        """grab an image out of the spritesheet"""
        image = pygame.Surface([width, height])

        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        
        image.set_colorkey((0,0,0))

        return image
class CharacterSprite(pygame.sprite.Sprite):
    """Sprite representation of the character"""
    def __init__(self, x_coor, y_coor):
        self.x = x_coor
        self.y = y_coor

        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []

        self.direction = 'd'
        #list of colisions
        sprite_sheet = SpriteSheet('images/smallspritesheet.png')
        for i in range(0,109, 35):
            image = sprite_sheet.get_image(i,0,35, 64)
            self.walking_frames_d.append(image)
        for i in range(0,109, 35):
            image = sprite_sheet.get_image(i,65,35, 64)
            self.walking_frames_l.append(image)
        for i in range(0,109, 35):
            image = sprite_sheet.get_image(i,130,35, 64)
            self.walking_frames_r.append(image)
        for i in range(0,109, 35):
            image = sprite_sheet.get_image(i,195,35, 64)
            self.walking_frames_u.append(image)
       
        self.image = self.walking_frames_d[1]
        self.rect = self.image.get_rect()


class GameController(object):
    """This is the controller for the game. It contains all the animation data """
    def __init__(self, model):
        """ initializes the model and all of the image banks for the character"""
        self.model = model

    def update(self):
        """ Updates the game state based on keypresses. Also animates walking right now"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.model.char.x -= 5
            self.model.char.image = self.model.char.walking_frames_l[2]
#            self.li = (self.li + 1)%4
        if pressed[pygame.K_RIGHT]:
           # self.model.char.update('right')
             self.model.char.x += 5
#            self.model.char.set_image(self.rightimages[self.ri])
             self.model.char.image = self.model.char.walking_frames_r[2]
#            self.li = (self.li + 1)%4
#            self.ri = (self.ri + 1)%4
        if pressed[pygame.K_UP]:
          #  self.model.char.update('up')
            self.model.char.y -= 5
            self.model.char.image = self.model.char.walking_frames_u[2]
#            self.li = (self.li + 1)%4
#            self.model.char.set_image(self.upimages[self.ui])
#            self.ui = (self.ui + 1)%4
        if pressed[pygame.K_DOWN]:
           # self.model.char.update('down')
            self.model.char.image = self.model.char.walking_frames_d[2]
#            self.li = (self.li + 1)%4
            self.model.char.y += 5 
#            self.model.char.set_image(self.downimages[self.di])
#            self.di = (self.di + 1)%4
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
        time.sleep(.01)
