import pygame
from pygame.locals import *
from spritesheet_functions import SpriteSheet
import random

class Level(object):
	#inherit from spritesheet? probably no, but we will need some sort of visual level as well as the programatic level
	def __init__(self, x=0):
            self.x = x

	def random_gen(self):
		#probably should take size
		#15 strings of 20 characters

		#generate top wall
		twall = ''
		for x in range(15):
			twall += random.choice(['W','W','W','W','X'])

		bwall = ''
		for x in range(15):
			bwall += random.choice(['W','W','W','W','X'])

		middlewalls = []
		for x in range(18):
			wall = ''
			wall += random.choice(['W','W','W','W','X'])
			wall += '.................'
			wall += random.choice(['W','W','W','W','X'])
			middlewalls.append(wall)

		walls = []
		walls.append(twall)
		for wall in middlewalls:
			walls.append(wall)
		walls.append(bwall)
		return walls


class WallSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(WallSprite, self).__init__()

        self.tiles = []

        #sprite_sheet = SpriteSheet('images/rooms/Tileset.png')
        sprite_sheet = SpriteSheet('images/room2.png')
        self.tiles.append(sprite_sheet.get_image(256,256,100,100))
    
