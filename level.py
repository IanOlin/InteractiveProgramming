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
		for x in range(20):
			twall += random.choice(['W','W','W','W','W','W','C'])

		bwall = ''
		for x in range(20):
			bwall += random.choice(['W','W','W','W','W','W','C'])

		middlewalls = []
		for x in range(13):
			wall = ''
			wall += random.choice(['W','W','W','W','W','W','C'])
			wall += '..................'
			wall += random.choice(['W','W','W','W','W','W','C'])
			wall += '..................'
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
        sprite_sheet = SpriteSheet('images/tilesets/walls.png')#3 x 4
        horiz = [0, 32, 64]
        vert= [0, 32, 64, 96]
        self.image = sprite_sheet.get_image(random.choice(horiz),random.choice(vert),32,32)

class DoorSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(DoorSprite, self).__init__()

        self.tiles = []

        sprite_sheet = SpriteSheet('images/tilesets/doors.png')#4 x 1
        horiz = [0, 32, 64, 96]
        vert= [0]

        self.image = sprite_sheet.get_image(random.choice(horiz),random.choice(vert),32,32)
#floor 7x 6
#door 4x1
class FloorSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(FloorSprite, self).__init__()

        self.tiles = []

        sprite_sheet = SpriteSheet('images/tilesets/floors.png')#7x6
        horiz = [0, 32, 64, 96, 128, 160, 192]
        vert= [0, 32, 64, 96, 128, 160]

        self.image = sprite_sheet.get_image(random.choice(horiz),random.choice(vert),32,32)
