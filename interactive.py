#vim : tabstop=8 expandtab shiftwidth=4 softtabstop=4
import pygame
from pygame.locals import *
import time
from random import choice

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

        self.char = CharacterSprite(256,256)

        self.game_map = ["....................",
                         "....................",
                         "....................",
                         "....................",
                         "....................",
                         "......WXWW..........",
                         "....WWW..WWWWW......",
                         "....W........W......",
                         "....W........W......",
                         "....W..........W....",
                         "....W..........W....",
                         "....W..........W....",
                         "....WWWWWXXWWWWW....",
                         "....WWWWWXXWWWWW....",
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


class SpriteSheet(object):
    """Class used to grab images out of a sprite sheet.

    attributes: sprite_sheet"""
    def __init__(self, file_name= 'images/smallspritesheet.png'):
        self.sprite_sheet = pygame.image.load(file_name)
    def get_image(self, x, y, width, height):
        """grab an image out of the spritesheet"""
        image = pygame.Surface([width, height])

        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))

        image.set_colorkey((0,0,0))

        return image


class CharacterSprite(pygame.sprite.Sprite):
    """Sprite representation of the character.

    attributes: x, y, walking_frames_l, walking_frames_r, walking_frames_u,
    walking_frames_d, step_size, direction, image, rect"""
    def __init__(self, x_coor, y_coor):
        self.x = x_coor
        self.y = y_coor
        self.step_size = 5

        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.effect = pygame.mixer.Sound('sounds/step.wav')

        self.direction = 'd'
        #list of colisions would go here  #(maybe)
        sprite_sheet = SpriteSheet('images/smallspritesheet.png')
        for i in range(0,109, 36):
            image = sprite_sheet.get_image(i,0,36, 60)
            self.walking_frames_d.append(image)
        for i in range(0,109, 36):
            image = sprite_sheet.get_image(i,62,36, 60)
            self.walking_frames_l.append(image)
        for i in range(0,109, 36):
            image = sprite_sheet.get_image(i,126,36, 60)
            self.walking_frames_r.append(image)
        for i in range(0,109, 36):
            image = sprite_sheet.get_image(i,185,36, 70)
            self.walking_frames_u.append(image)

        self.walking_frames_d[3] = self.walking_frames_d[1]
        self.walking_frames_l[3] = (self.walking_frames_l[1])
        self.walking_frames_u[3] = (self.walking_frames_u[1])
        self.walking_frames_r[3] = (self.walking_frames_r[1])
        self.image = self.walking_frames_d[1]
        self.rect = self.image.get_rect().inflate(-4,-32)
        self.rect.move_ip(self.x,self.y + 16)

    """These functions move the thing. Should check for collisions and adjust
    accordingly now? Untested cause the wall rects don't exist yet"""
    def move_left(self, li):
        self.x -= self.step_size
        self.rect.move_ip(-self.step_size, 0)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.left = wall.rect.right
                self.x += self.step_size

        self.image = self.walking_frames_l[li]
        self.effect.play()

    def move_right(self, ri):
        self.x += self.step_size
        self.rect.move_ip(self.step_size, 0)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.right = wall.rect.left
                self.x -= self.step_size

        self.image = self.walking_frames_r[ri]
        self.effect.play()

    def move_up(self, ui):
        self.y -= self.step_size
        self.rect.move_ip(0, -self.step_size)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.top = wall.rect.bottom
                self.y += self.step_size

        self.image = self.walking_frames_u[ui]
        self.effect.play()

    def move_down(self, di):
        self.y += self.step_size
        self.rect.move_ip(0, self.step_size)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.bottom = wall.rect.top
                self.y -= self.step_size

        self.image = self.walking_frames_d[di]
        self.effect.play()


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
    #size = (VideoInfo.current_w, VideoInfo.current_h)#sets the game to fill screen
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
