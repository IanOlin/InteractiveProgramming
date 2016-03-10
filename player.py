import pygame
from pygame.locals import *
from spritesheet_functions import SpriteSheet
class CharacterSprite(pygame.sprite.Sprite):
    """Sprite representation of the character.

    attributes: x, y, walking_frames_l, walking_frames_r, walking_frames_u,
    walking_frames_d, step_size, direction, image, rect"""
    def __init__(self, x_coor, y_coor, walls):

        super(CharacterSprite, self).__init__()

        self.x = x_coor
        self.y = y_coor
        self.step_size = 5
        self.walls = walls

        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.effect = pygame.mixer.Sound('sounds/step.wav')

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
        self.rect = self.image.get_rect().inflate(-10,-32)
        self.rect.move_ip(self.x,self.y + 16)

    def move_left(self, li):
        self.x -= self.step_size
        self.rect.move_ip(-self.step_size, 0)

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.left = wall.rect.right
                self.x += self.step_size

        self.image = self.walking_frames_l[li]
        self.effect.play()

    def move_right(self, ri):
        self.x += self.step_size
        self.rect.move_ip(self.step_size, 0)

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.right = wall.rect.left
                self.x -= self.step_size

        self.image = self.walking_frames_r[ri]
        self.effect.play()

    def move_up(self, ui):
        self.y -= self.step_size
        self.rect.move_ip(0, -self.step_size)

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.top = wall.rect.bottom
                self.y += self.step_size

        self.image = self.walking_frames_u[ui]
        self.effect.play()

    def move_down(self, di):
        self.y += self.step_size
        self.rect.move_ip(0, self.step_size)

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.bottom = wall.rect.top
                self.y -= self.step_size

        self.image = self.walking_frames_d[di]
        self.effect.play()
