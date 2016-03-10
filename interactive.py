#vim : tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygame
from pygame.locals import *
import time
from random import choice
from spritesheet_functions import SpriteSheet
from player import CharacterSprite
#TODO split the model view and controller into different files maybe?
# docs:
# pygame.org/project-Rect+collision+Reponse-1061-.html
# that link was hand typed so fuck off
# the screen is a 20x15 grid of 16x16 pixel tiles
# at least in 320 I guess it's 32x32 in 640
"""globals: walls, exit_blocks"""


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


class GameModel(object):
    """This is a test model for my game

    attributes: height, width, char, game_map"""
    def __init__(self, width, height):
        self.height = height
        self.width = width

        # Define things like brick height and width here for BB
        # Also creates list of bricks, paddle, and ball

        self.char = CharacterSprite(256,256,walls)

        self.game_map = ["....................",
                         "....................",
                         "....................",
                         "....................",
                         "....................",
                         "......WXWW..........",
                         "....WWW..WWWWW......",
                         "....W........W......",
                         "....W........WWW....",
                         "....W..........W....",
                         "....W..........W....",
                         "....W..........W....",
                         "....WWWWWXXWWWWW....",
                         "....................",
                         "...................."]

        # Parse the level string above. W = wall, X = exit
        x = y = 0
        for row in self.game_map:
            for col in row:
                if col == "W":
                    Wall((x, y))
                if col == "X":
                    ExitBlock((x, y))
                x += 32
            y += 32
            x = 0

    def update(self, control=0):
        """ update the model state"""
        self.char.update(control)


class Wall(object):
    """it walls

    attribute: rect"""
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


class ExitBlock(object):
    """It exits

    attribute: rect"""
    def __init__(self, pos):
        exit_blocks.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


class GameController(object):
    """This is the controller for the game. It contains a counter for each
    direction that controls animation state.

    attributes: model, li, di, ri, ui"""
    def __init__(self, model):
        """ initializes the model and counters"""
        self.model = model
        self.li = 0
        self.di = 0
        self.ri = 0
        self.ui = 0

    def update(self):
        """ Updates the game state based on keypresses.
        Also animates walking ALL DIRECTIONS now"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.li = (self.li + 1) % 4
            self.model.char.move_left(self.li)

        if pressed[pygame.K_RIGHT]:
            self.ri = (self.ri + 1) % 4
            self.model.char.move_right(self.ri)

        if pressed[pygame.K_UP]:
            self.ui = (self.ui + 1) % 4
            self.model.char.move_up(self.ui)

        if pressed[pygame.K_DOWN]:
            self.di = (self.di + 1) % 4
            self.model.char.move_down(self.di)

        for exit_block in exit_blocks:
            if self.model.char.rect.colliderect(exit_block):
                raise SystemExit, "You lose, fucker!"


if __name__ == '__main__':
    pygame.init()
    #size = (VideoInfo.current_w, VideoInfo.current_h)
    # sets the game to fillscreen
    #That works, but it doesn't generate in the right aspect ratio
    size = (640, 480) # useful
    # size = (320, 240)  # 'native'
    walls = [] # List to hold the walls
    exit_blocks = [] # List to hold the exits
    model = GameModel(size[0], size[1])
    view = GameView(model, size)
    controller = GameController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        model.update()
        controller.update()
        view.draw()
        time.sleep(.05)
