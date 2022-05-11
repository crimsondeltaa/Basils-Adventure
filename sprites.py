import pygame
from config import *
import math
import random

class Spritesheet:
	def __init__(self, file):
		self.sheet = pygame.image.load(file).convert()

	def get_sprite(self, x, y, width, height):
		sprite = pygame.Surface([width, height])
		sprite.blit(self.sheet, (0,0), (x, y, width, height))
		return sprite

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):

		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.x_change = 0
		self.y_change = 0

		self.facing = 'down'
		self.animation_loop = 1

		image_to_load = pygame.image.load("img/basildownstand.png")

		self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32).convert_alpha()
		self.image.blit(image_to_load, (0,0))

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.movement()
		self.animate()

		self.rect.x += self.x_change
		self.collide_blocks('x')
		self.rect.y += self.y_change
		self.collide_blocks('y')

		self.x_change = 0
		self.y_change = 0

	def movement(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.x_change -= PLAYER_SPEED
			self.facing = 'left'
		if keys[pygame.K_RIGHT]:
			self.x_change += PLAYER_SPEED
			self.facing = 'right'
		if keys[pygame.K_UP]:
			self.y_change -= PLAYER_SPEED
			self.facing = 'up'
		if keys[pygame.K_DOWN]:
			self.y_change += PLAYER_SPEED
			self.facing = 'down'

	def collide_blocks(self, direction):
		if direction == "x":
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.x_change > 0:
					self.rect.x = hits[0].rect.left - self.rect.width
				if self.x_change < 0:
					self.rect.x = hits[0].rect.right
		if direction == "y":
			hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
			if hits:
				if self.y_change > 0:
					self.rect.y = hits[0].rect.top - self.rect.height
				if self.y_change < 0:
					self.rect.y = hits[0].rect.bottom
	def animate(self):
		down_animations = [pygame.image.load("img/basildownstand.png"),pygame.image.load("img/basildownright.png"),pygame.image.load("img/basildownleft.png")]
		up_animations = [pygame.image.load("img/basilbackstand.png"),pygame.image.load("img/basilupright.png"),pygame.image.load("img/basilupleft.png")]
		left_animations = [pygame.image.load("img/basilleftstand.png"),pygame.image.load("img/basilleftright.png"),pygame.image.load("img/basilleftleft.png")]
		right_animations = [pygame.image.load("img/basilrightstand.png"),pygame.image.load("img/basilrightright.png"),pygame.image.load("img/basilrightleft.png")]
		if self.facing == "down":
			if self.y_change == 0:
				self.image = pygame.image.load("img/basildownstand.png")
			else:
				self.image = down_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 3:
					self.animation_loop = 1
		if self.facing == "up":
			if self.y_change == 0:
				self.image = pygame.image.load("img/basilbackstand.png")
			else:
				self.image = up_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 3:
					self.animation_loop = 1
		if self.facing == "left":
			if self.x_change == 0:
				self.image = pygame.image.load("img/basilleftstand.png")
			else:
				self.image = left_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 3:
					self.animation_loop = 1
		if self.facing == "right":
			if self.x_change == 0:
				self.image = pygame.image.load("img/basilrightstand.png")
			else:
				self.image = right_animations[math.floor(self.animation_loop)]
				self.animation_loop += 0.1
				if self.animation_loop >= 3:
					self.animation_loop = 1

class Block(pygame.sprite.Sprite):
	def __init__(self, game, x, y, typeof):

		self.game = game
		self._layer = BLOCK_LAYER
		self.typeof = typeof
		self.groups = self.game.all_sprites, self.game.blocks
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE
		if self.typeof == "B":
			self.image = pygame.image.load("img/black.png")
			self.rect = self.image.get_rect()
			self.rect.x = self.x
			self.rect.y = self.y
		if self.typeof == "T":
			self.image = pygame.image.load("img/table.png")
			self.rect = self.image.get_rect()
			self.rect.x = self.x
			self.rect.y = self.y
		if self.typeof == "D":
			self.image = pygame.image.load("img/whitedoor.png")
			self.rect = self.image.get_rect()
			self.rect.x = self.x
			self.rect.y = self.y
		if self.typeof == "d":
			self.image = pygame.image.load("img/whitedoor2.png")
			self.rect = self.image.get_rect()
			self.rect.x = self.x
			self.rect.y = self.y
		

class Ground(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self,self.groups)

		self.x = x * TILESIZE
		self.y = y * TILESIZE
		self.width = TILESIZE
		self.height = TILESIZE

		self.image = self.game.terrain_spritesheet.get_sprite(224,416,self.width, self.height)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y