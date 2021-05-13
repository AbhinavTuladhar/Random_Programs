import pygame, sys
from pygame.locals import *

class Ball:
	def __init__(self, screen, colour, posX, posY, radius):
		self.screen = screen
		self.colour = colour
		self.posX = posX
		self.posY = posY
		self.radius = radius

		self.dx = 0
		self.dy = 0

		self.show()

	def show(self):
		pygame.draw.circle(self.screen, self.colour, (self.posX, self.posY), self.radius)

	def start_moving(self):
		self.dx = 10
		self.dy = 5

	def move(self):
		self.posX += self.dx
		self.posY += self.dy

	def paddle_collision(self):
		self.dx= -self.dx

	def wall_collision(self):
		self.dy = -self.dy

	def other_wall_collision(self):
		self.dx = -self.dx
		

class Paddle:
	def __init__(self, screen, colour, posX, posY, width, height):
		self.screen = screen
		self.colour = colour
		self.posX = posX
		self.posY = posY
		self.width = width
		self.height = height

		self.state = 'stopped'

		self.show()

	def show(self):
		pygame.draw.rect(self.screen, self.colour, (self.posX, self.posY, self.width, self.height))

	def move(self):
		if self.state == 'up':
			self.posY -= 5
		elif self.state == 'down':
			self.posY += 5

	def clamp(self):
		if self.posY <= 0:
			self.posY = 0
		if (self.posY + self.height) >= HEIGHT:
			self.posY = HEIGHT - self.height

class CollisionManager:
	def between_ball_and_paddle1(self, ball, paddle1):
		if ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height:
			if ball.posX - ball.radius <= paddle1.posX + paddle1.width:
				return True

		return False

	def between_ball_and_paddle2(self, ball, paddle2):
		if ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height:
			if ball.posX + ball.radius >= paddle2.posX:
				return True

		return False

	def between_ball_and_walls(self, ball):
		# For top wall collision
		if ball.posY - ball.radius <= 0:
			return True

		# For bottom wall collision
		if ball.posY + ball.radius >= HEIGHT:
			return True

		return False

	def between_ball_and_player_walls(self, ball):
		# For left wall:
		if ball.posX - ball.radius <= 0:
			return True

		if ball.posX + ball.radius >= WIDTH:
			return True

		return False

	def check_goal_player1(self, ball):
		return ball.posX + ball.radius >= WIDTH

	def check_goal_player2(self, ball):
		return ball.posX - ball.radius <= 0

class Score:
	def __init__(self, screen, points, posX, posY):
		self.screen = screen
		self.points = points
		self.posX = posX
		self.posY = posY
		self.font = pygame.font.SysFont("helvetica", 60, bold = True)
		self.label = self.font.render(self.points, 0, WHITE)
		self.show()

	def show(self):
		self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

	def increase_score(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 0, WHITE)

pygame.init()

# For setting the frame rate
FPS = 60
fpsClock = pygame.time.Clock()

# Numerical constants
WIDTH = 1024
HEIGHT = 576

# Colour constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

def paint_black():
	screen.fill(BLACK)
	pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 10)

paint_black()

# Creating the objects
ball = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, 9)
paddle1 = Paddle(screen, WHITE, 15, HEIGHT // 2 - 60, 10, 120)
paddle2 = Paddle(screen, WHITE, WIDTH - 10 - 15, HEIGHT // 2 - 60, 10, 120)
collision = CollisionManager()
score1 = Score(screen, '0', WIDTH // 4, 15)
score2 = Score(screen, '0', WIDTH - WIDTH // 4, 15)

# Variables
playing = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				ball.start_moving()
				playing = True

			if event.key == pygame.K_w:
				paddle1.state = 'up'

			if event.key == pygame.K_s:
				paddle1.state = 'down'

			if event.key == pygame.K_UP:
				paddle2.state = 'up'

			if event.key == pygame.K_DOWN:
				paddle2.state = 'down'

		if event.type == pygame.KEYUP:
			paddle1.state = 'stopped'
			paddle2.state = 'stopeed'

	if playing:
		paint_black()

		# Ball movement
		ball.move()
		ball.show()

		# Show the paddles
		paddle1.clamp()
		paddle1.show()
		paddle1.move()

		paddle2.clamp()
		paddle2.show()
		paddle2.move()

		# Checking for collisions
		if collision.between_ball_and_paddle1(ball, paddle1):
			ball.paddle_collision()

		if collision.between_ball_and_paddle2(ball, paddle2):
			ball.paddle_collision()

		if collision.between_ball_and_walls(ball):
			ball.wall_collision()

		if collision.between_ball_and_player_walls(ball):
			ball.other_wall_collision()

		if collision.check_goal_player1(ball):
			score1.increase_score()

		if collision.check_goal_player2(ball):
			score2.increase_score()

	score1.show()
	score2.show()

	pygame.display.update()
	fpsClock.tick(FPS)