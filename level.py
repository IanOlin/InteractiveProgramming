import pygame
from pygame.locals import *
from spritesheet_functions import SpriteSheet
import random

class Level(object):
	#inherit from spritesheet? probably no, but we will need some sort of visual level as well as the programatic level
	def __init__(self):
		pass

	def random_gen():
		#probably should take size
		#15 strings of 20 characters

		#generate top wall
		twall = ''
		for x in range(15):
			twall += random.choice('W','W','W','W','X')

		bwall = ''
		for x in range(15):
			bwall += random.choice('W','W','W','W','X')

		middlewalls = []
		for x in range(18):
			wall = ''
			wall += random.choice('W','W','W','W','X')
			wall += '.................'
			wall += random.choice('W','W','W','W','X')
			middlewalls.append(wall)

		walls = []
		walls.append(twall)
		for wall in middlewalls:
			walls.append(wall)
		walls.append(bwall)
		print walls

Level.random_gen



