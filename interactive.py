#vim : tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygame
from pygame.locals import *
import time
from random import choice
from spritesheet_functions import SpriteSheet
from player import CharacterSprite
from level import Level, WallSprite, DoorSprite, FloorSprite

#TODO split the model view and controller into different files maybe?
# docs:
# pygame.org/project-Rect+collision+Reponse-1061-.html
# that link was hand typed so fuck off
# the screen is a 20x15 grid of 16x16 pixel tiles
# at least in 320 I guess it's 32x32 in 640
"""globals: walls, exit_blocks"""


class GameView(object):
    """this view handles displaying most of the things.

    attributes: model, screen, background"""
    def __init__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size)
        pygame.mixer.music.load('sounds/TheDarkLake.mp3') #this music plays
        pygame.mixer.music.play(-1)
        self.background = 'images/room2.png'
        self.wallsprite = WallSprite()
        self.x = 0
        self.y = 0

    def draw(self, filename):
        """ Draw the game to the pygame window"""
        background = pygame.image.load(filename).convert()
        # print filename
        scaled_bg = pygame.transform.scale(background, size)
        self.screen.blit(scaled_bg, (0,0))
        char = self.model.char.image
        self.screen.blit(char, (self.model.char.x,self.model.char.y))
        
        pygame.display.flip()

    def build_surface(self, room_map):
        surf = pygame.Surface(size)
        x = 0
        y = 0
        wallsprite = WallSprite()
        wall = wallsprite.image
        doorsprite = DoorSprite()
        door = doorsprite.image
        floorsprite = FloorSprite()
        floor = floorsprite.image
        for row in room_map:
            for col in row:
                if col == "W":
                    surf.blit(wall,(x, y))
                if col == "C":
                    surf.blit(door,(x, y))
                if col == ".":
                    surf.blit(floor,(x,y))
                x += 32
            y += 32
            x = 0
        pygame.image.save(surf, 'currentroom.png')


class GameModel(object):
    """This is a test model for my game

    attributes: height, width, char, room_map"""
    def __init__(self, width, height):
        self.height = height
        self.width = width

        # Define things like brick height and width here for BB
        # Also creates list of bricks, paddle, and ball

        self.room_map = ["....................",
                         "....................",
                         "....................",
                         "....................",
                         "....................",
                         "......WCWW..........",
                         "....WWW..WWWWW......",
                         "....W........W......",
                         "....W........WWW....",
                         "....W..........W....",
                         "....W..........W....",
                         "....W..........W....",
                         "....WWWWWXXWWWWW....",
                         "....................",
                         "...................."]

        self.generate_room(self.room_map)

        self.char = CharacterSprite(384,224,walls)

        # Parse the level string above. W = wall, X = exit, C = connection
    def generate_room(self, room):
        """feed it a list of strings and it populates the globals with rects"""
        del walls[:] # List to hold the walls
        del exit_blocks[:] # List to hold the exits
        del connections[:] # List to hold all connections
        self.room_map = room
        x = y = 0
        for row in self.room_map:
            for col in row:
                if col == "W":
                    Wall((x, y))
                if col == "X":
                    ExitBlock((x, y))
                if col == "C":
                    Connection((x,y))
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

class Connection(object):

    def __init__(self, pos):
        connections.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


class GameController(object):
    """This is the controller for the game. It contains a counter for each
    direction that controls animation state.

    attributes: model, li, di, ri, ui"""
    def __init__(self, model, view):
        """ initializes the model and counters"""
        self.model = model
        self.view = view
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
        for connection in connections:
            if self.model.char.rect.colliderect(connection):
                new_spaces = [(40, 200), (560,200), (240,40),(240, 340)]
                new_space = choice(new_spaces)
                self.model.char.x = new_space[0]
                self.model.char.y = new_space[1]

                self.model.char.image = self.model.char.walking_frames_d[1]
                self.model.char.rect = self.model.char.image.get_rect().inflate(-4,-32)
                self.model.char.rect.move_ip(self.model.char.x,self.model.char.y + 16)


                self.model.room_map = level.random_gen()
                self.model.generate_room(self.model.room_map)
                self.view.build_surface(self.model.room_map)
                self.view.background = 'currentroom.png'
                self.model.char.walls = walls

if __name__ == '__main__':
    pygame.init()
    #size = (VideoInfo.current_w, VideoInfo.current_h)
    # sets the game to fillscreen
    #That works, but it doesn't generate in the right aspect ratio
    size = (640, 480) # useful
    # size = (320, 240)  # 'native'
    walls = [] # List to hold the walls
    exit_blocks = [] # List to hold the exits
    connections = [] # List to hold all connections
    model = GameModel(size[0], size[1])
    view = GameView(model, size)
    controller = GameController(model, view)
    level = Level()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        model.update()
        controller.update()
        view.draw(view.background)
        time.sleep(.05)
