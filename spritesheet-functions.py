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
