import pygame
from random import randint

class Game():
	def __init__(self):
		self.is_working = False
		self.is_finished = False
		self.win = False
		self.lose = False
		self.current_frame = 0
	def start(self): 
		self.is_working = True
	def stop(self):
		self.is_working = False
	def set_win(self):
		self.win = True
	def set_lose(self):
		self.lose = True

class Hitbox():
	def __init__(self, x, y, width, height, hitbox_color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.hitbox_color = hitbox_color

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

	def draw_hitbox(self):
		pygame.draw.rect(screen, self.hitbox_color, self.rect, 1)

	def collidepoint(self, mouse_position):
		return self.rect.collidepoint(mouse_position[0], mouse_position[1])

class Model(Hitbox):
	def __init__(self, x, y, width, height, hitbox_color, img_url):
		Hitbox.__init__(self, x, y, width, height, hitbox_color)
		self.img_url = img_url

		self.image = pygame.transform.scale(pygame.image.load(self.img_url).convert_alpha(), (self.width, self.height))
	
	def draw_model(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))

class Ball(Model):
	def __init__(self, x, y, width, height, hitbox_color, img_url, speed):
		Model.__init__(self, x, y, width, height,hitbox_color, img_url)
		self.speed = speed
		self.dx = 1
		self.dy = 1

	def move(self):
		self.rect.y += int(self.speed * self.dy)
		self.rect.x += int(self.speed * self.dx)

	def draw_ball(self):
		self.draw_model()

	def collide_screen(self):
		if self.rect.top < 0:
			self.rect.top = 0
			self.dy *= -1
		elif self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			self.dy *= -1
class Player(Model):
	def __init__(self, x, y, width, height, hitbox_color, img_url, speed, player_id):
		Model.__init__(self, x, y, width, height,hitbox_color, img_url)
		self.speed = speed
		self.dy = 0
		self.points = 0
		self.player_id = player_id

	def move(self):
		self.rect.y += int(self.speed * self.dy)

	def controller(self,):
		keys = pygame.key.get_pressed()
		if self.player_id == 1:
			if keys[pygame.K_w] and not keys[pygame.K_s]:
				self.dy = -1
			elif keys[pygame.K_s] and not keys[pygame.K_w]:
				self.dy = 1
			else:
				self.dy = 0
		elif self.player_id == 2:
			if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
				self.dy = -1
			elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
				self.dy = 1
			else:
				self.dy = 0
		  
	def collide_screen(self):
		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > screen_height:
			self.rect.bottom = screen_height

	def collide_ball(self, sprite):
		if self.rect.colliderect(sprite.rect):
			if self.player_id == 1 and sprite.rect.centerx > self.rect.right:
				if sprite.rect.left < self.rect.right:
					sprite.rect.left = self.rect.right
					sprite.dx *= -1
			if self.player_id == 2 and sprite.rect.centerx < self.rect.left:
				if sprite.rect.right > self.rect.left:
					sprite.rect.right = self.rect.left
					sprite.dx *= -1

	def draw_player(self):
		self.draw_model()

pygame.init()
screen_title = 'Maze'
screen_width = 2560
screen_height = 1440
screen_color = (200, 200, 200)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption(screen_title)

clock = pygame.time.Clock()
fps = 60

game = Game()
game.start()

ball = Ball(0, 0, 64, 64, (250, 30, 30), 'ball.png', 6)
ball.rect.centerx = screen_width // 2
ball.rect.centery = screen_height // 2
player1 = Player(100, 200, 50, 100, (200, 30, 30), 'platform.png', 8, 1)
player2 = Player(screen_width - 150, 600, 50, 100, (200, 30, 30), 'platform.png', 8, 2)

main_font = pygame.font.SysFont(None, 50)

while game.is_working:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.stop()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				game.stop()
			if event.key == pygame.K_r:
				player1.points = 0
				player2.points = 0
				ball.rect.centerx = screen_width // 2
				ball.rect.centery = screen_height // 2
				player1.rect.centery = 200
				player2.rect.centery = 600

	screen.fill(screen_color)
	player1.move()
	player1.draw_player()
	player1.controller()
	player1.collide_screen()
	player1.collide_ball(ball)
	player2.move()
	player2.draw_player()
	player2.controller()
	player2.collide_screen()
	player2.collide_ball(ball)
	ball.draw_ball()
	ball.move()
	ball.collide_screen()
	
	if not game.win and not game.lose:
		if ball.rect.right <= 0:
			player2.points += 1
			ball.rect.centerx = screen_width // 2
			ball.rect.centery = screen_height // 2
			ball.dx *= -1
		elif ball.rect.left >= screen_width:
			player1.points += 1
			ball.rect.centerx = screen_width // 2
			ball.rect.centery = screen_height // 2
			ball.dx *= -1

		if player1.points == 3:
			game.set_win()

		if player2.points == 3:
			game.set_lose()

		screen.blit(main_font.render('POINTS1:' + str(player1.points), True, (255, 255, 255)), (20, 20))
		screen.blit(main_font.render('POINTS2:' + str(player2.points), True, (255, 255, 255)), (20, 80))
	elif game.win:
		screen.blit(main_font.render('PLAYER1 WIN!', True, (20, 255, 20)), (700, 500))
		screen.blit(main_font.render('Нажмите "r" что бы начать сначала', True, (255, 255, 255)), (screen_width // 2, screen_height // 2))
	elif game.lose:
		screen.blit(main_font.render('PLAYER2 WIN!', True, (255, 20, 20)), (700, 500))
		screen.blit(main_font.render('Нажмите "r" что бы начать сначала', True, (255, 255, 255)), (screen_width // 2, screen_height // 2))
	pygame.display.update()
	clock.tick(fps)