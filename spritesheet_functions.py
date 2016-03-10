import pygame

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
