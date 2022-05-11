import pygame
from sprites import *
from config import *
import sys

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		#self.font = pygame.font.Font('Arial', 32)
		self.running = True

		self.character_spritesheet = Spritesheet("img/character.png")
		self.terrain_spritesheet = Spritesheet("img/terrain.png")

	def createTilemap(self):
		for i, row in enumerate(tilemap):
			for j, column in enumerate(row):
				Ground(self, j, i)
				if column == "B":
					Block(self, j, i, column)
				if column == "P":
					Player(self, j, i)
				if column == "T":
					Block(self, j, i, column)
				if column == "D":
					Block(self, j, i, column)
				if column == "d":
					Block(self, j, i, column)

	def new(self):
		self.playing = True

		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()

		self.createTilemap()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False

	def update(self):
		self.all_sprites.update()

	def draw(self):
		self.screen.fill(WHITE)
		self.all_sprites.draw(self.screen)
		self.clock.tick(FPS)
		pygame.display.update()

	def main(self):
		while self.playing:
			self.events()
			self.update()
			self.draw()
		self.running = False

	def game_over(self):
		pass

	def intro_screen(self):
		pass
g = Game()
g.intro_screen()
g.new()
while g.running:
	g.main()
	g.game_over()
pygame.quit()
sys.exit()