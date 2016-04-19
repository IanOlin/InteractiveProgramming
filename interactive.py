#vim : tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygame
from pygame.locals import *
import time
from random import choice, random
from spritesheet_functions import SpriteSheet
from player import CharacterSprite
from level import Level, WallSprite, DoorSprite, FloorSprite

"""
This is the main function for the game; run to initialize and play.
Try to escape the dream.
Arrow keys to move, 9 to wake up.

classes: GameView, GameModel, GameController, Wall, ExitBlock, Connection
globals: walls, exit_blocks
"""


class GameView(object):
    """this view handles displaying most of the things.

    attributes: model, screen, background"""
    def __init__(self, model, size):
        self.model = model
        self.screen = pygame.display.set_mode(size)

        # this music plays
        pygame.mixer.music.load('sounds/TheDarkLake.mp3')
        pygame.mixer.music.play(-1)

        # starting room image
        self.background = 'images/room2.png'

    def draw(self, filename):
        """ Draw the game to the pygame window"""
        # draws the background
        background = pygame.image.load(filename).convert()
        scaled_bg = pygame.transform.scale(background, size)
        self.screen.blit(scaled_bg, (0,0))

        # draws the character model
        char = self.model.char.image
        self.screen.blit(char, (self.model.char.x,self.model.char.y))

        # update
        pygame.display.flip()

    def build_surface(self, room_map):
        """Builds the random rooms image for our procedurally generated rooms"""

        # initialize room surface and sprites to use for the specific room
        surf = pygame.Surface(size)
        wallsprite = WallSprite()
        wall = wallsprite.image
        doorsprite = DoorSprite()
        door = doorsprite.image
        floorsprite = FloorSprite()
        floor = floorsprite.image

        # build room image based on character map
        x = 0
        y = 0
        for row in room_map:
            for col in row:
                if col == "W":
                    surf.blit(wall,(x, y))
                if col in ["T","B","L","R"]:
                    surf.blit(door,(x, y))
                if col == ".":
                    surf.blit(floor,(x,y))
                x += 32
            y += 32
            x = 0

        # save to file
        pygame.image.save(surf, 'currentroom.png')


class GameModel(object):
    """This is the model for the game. It contains most of the functional bits
    of the level.

    attributes: height, width, char, start_map, room_map"""
    def __init__(self, width, height):
        self.height = height
        self.width = width

        # character map of the starting room
        self.start_map = ["....................",
                         "....................",
                         "....................",
                         "....................",
                         "....................",
                         "......WTWW..........",
                         "....WWW..WWWWW......",
                         "....W........W......",
                         "....W........WWW....",
                         "....W..........W....",
                         "....W..........W....",
                         "....W..........W....",
                         "....WWWWWXXWWWWW....",
                         "....................",
                         "...................."]
        self.room_map = self.start_map

        self.generate_room(self.room_map)

        self.char = CharacterSprite(384,224,walls)


    def generate_room(self, room):
        """Parses the level string above and populates the globals with rects
        W = wall, X = exit, C = connection"""

        # clears the global rect lists
        del walls[:] # List to hold the walls
        del exit_blocks[:] # List to hold the exits
        del connections[:] # List to hold all connections
        self.room_map = room

        # build global rect lists based on character map
        x = 0
        y = 0
        for row in self.room_map:
            for col in row:
                if col == "W":
                    Wall((x, y))
                if col == "X":
                    ExitBlock((x, y))
                if col in ["T","B","L","R"]:
                    Connection((x, y), col)
                x += 32
            y += 32
            x = 0


    def update(self, control=0):
        """ update the model state"""
        self.char.update(control)


class GameController(object):
    """This is the controller for the game. It contains a counter for each
    direction that controls animation state.

    attributes: model, li, di, ri, ui, room_counter"""

    def __init__(self, model, view):
        """ initializes the model and counters"""
        self.model = model
        self.view = view
        self.li = 0
        self.di = 0
        self.ri = 0
        self.ui = 0
        self.waking = 0
        self.room_counter = 0

    def reset_state(self):
        """clean slate for initial room generation, all subsequent resets"""
        global timer
        self.waking += 1
        if self.waking * random() > 2:
            timer = True
        self.model.room_map = self.model.start_map
        self.model.generate_room(self.model.start_map)
        self.view.background = 'images/room2.png'
        self.model.char.walls = walls
        self.model.char.x = 384
        self.model.char.y = 224
        self.room_counter = 0

        self.model.char.image = self.model.char.walking_frames_d[1]
        self.model.char.rect = self.model.char.image.get_rect().inflate(-4,-32)
        self.model.char.rect.move_ip(self.model.char.x,self.model.char.y + 16)


    def update(self):
        """ Updates the game state based on keypresses.
        Also animates walking ALL DIRECTIONS now"""
        self.effect = pygame.mixer.Sound('sounds/Uboa_short.wav')
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_9]:
            #This is the wake up function
            self.reset_state()

        # move in directions
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

        #these functions check for collisions with interactive blocks
        for exit_block in exit_blocks:
            if self.model.char.rect.colliderect(exit_block):
                print "You won't go out there."
                self.effect.play()
                time.sleep(0.50)
                self.reset_state()

        for connection in connections:
            if self.model.char.rect.colliderect(connection):
                #maps directions from which you exit the old room to positions in
                #the new room, so directional continuity
                new_spaces = {"R":(40, 200), "L":(560,200), "B":(240,10), "T":(240, 380)}
                new_space = new_spaces[connection.side]
                self.model.char.x = new_space[0]
                self.model.char.y = new_space[1]

                self.model.char.image = self.model.char.walking_frames_d[1]
                self.model.char.rect = self.model.char.image.get_rect().inflate(-4,-32)
                self.model.char.rect.move_ip(self.model.char.x,self.model.char.y + 16)

                # increments counter to gradually decrease likelihood of doors generating
                self.room_counter += 1
                self.model.room_map = level.random_gen(self.room_counter)
                self.model.generate_room(self.model.room_map)
                self.view.build_surface(self.model.room_map)
                self.view.background = 'currentroom.png'
                self.model.char.walls = walls


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
    """Links to a new room. Tracks which side of the room it is on.

    attribute: rect, side"""

    def __init__(self, pos, side):
        connections.append(self)
        self.side = side
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.rect.inflate_ip(2,2)


if __name__ == '__main__':
    pygame.init()
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
    timer = False
    countdown = 5
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        model.update()
        controller.update()
        view.draw(view.background)
        time.sleep(.05)
        if timer == True:
            countdown -= .05
            pygame.mixer.music.load('sounds/Uboa_long.wav')
            if countdown < .25:
                pygame.mixer.music.play(0)
                size = (1920,1080)
                pygame.display.set_mode(size)
                uboa = pygame.image.load('images/UBOAAAAA.png')
                uboa = pygame.transform.scale(uboa, size)
                view.screen.blit(uboa,(0,0))
                pygame.display.update()
            if countdown < 0:
                running = False
