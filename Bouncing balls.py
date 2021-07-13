import pygame, sys
import random, math

class Ball:
	def __init__(self, screen, colour, posX, posY, radius, x_start, y_start):
		self.screen = screen
		self.colour = colour
		self.posX = posX
		self.posY = posY
		self.radius = radius
		self.x_start = x_start
		self.y_start = y_start

		self.dx = 0
		self.dy = 0

		self.show()

	def show(self):
		pygame.draw.circle(self.screen, self.colour, (self.posX, self.posY), self.radius)

	def start_moving(self):
		self.dx = self.x_start
		self.dy = self.y_start

	def move(self):
		self.posX += self.dx
		self.posY += self.dy

	def left_and_right_collision(self):
		self.dx = -self.dx

	def lower_and_upper_collision(self):
		self.dy = -self.dy

	def ball_and_ball_collision(self):
		self.dx = -self.dx
		self.dy = -self.dy

class CollisionManager:
	def ball_and_horizontal_wall_collision(self, ball):
		# For left wall
		if ball.posX - ball.radius <= 0:
			return True

		# For right wall
		if ball.posX + ball.radius >= WIDTH:
			return True

		return False

	def ball_and_vertical_wall_collision(self, ball):

		# For upper wall
		if ball.posY - ball.radius <= 0:
			return True

		# For lower wall
		if ball.posY + ball.radius >= HEIGHT:
			return True

		return False

	def ball_and_ball_collision(self, ball1, ball2):
		"""V1 = pygame.math.Vector2(ball1.posX, ball1.posY)
		V2 = pygame.math.Vector2(ball2.posX, ball2.posY)

		print("LHS = ", V1.distance_to(V2))
		print("\n")

		if V1.distance_to(V2) <= (ball1.radius + ball2.radius):
			return True
		return False"""
		centre_distance = math.sqrt((ball2.posX - ball1.posX) ** 2 + (ball2.posY - ball1.posY) ** 2)
		if centre_distance <= (ball1.radius + ball2.radius):
			print("HIT!")
			return True

		return False

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

WIDTH = 1080
HEIGHT = 608
NUMBER_OF_BALLS = 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame practice again")

def init_screen():
	screen.fill(BLACK)
	font = pygame.font.SysFont("Times New Roman", 30)
	text_to_display = "Press Enter to play and Esc to exit."
	length = len(text_to_display)
	text = font.render(text_to_display,  0, WHITE)
	screen.blit(text, (WIDTH // 2 - length * 5, 0))

balls = []

init_screen()

# Making multiple balls
for number in range(NUMBER_OF_BALLS):
	x_vel = random.randint(5, 15)
	y_vel = random.randint(5, 15)
	R_value = random.randint(0, 255)
	G_value = random.randint(0, 255)
	B_value = random.randint(0, 255)
	rand_colour = (R_value, G_value, B_value)
	radius = random.randint(5, 10)
	x_pos = random.randint(10, WIDTH - radius)
	y_pos = random.randint(10, HEIGHT - radius)

	if R_value <= 10 and G_value <= 10 and B_value <= 10:
		rand_colour = WHITE

	balls.append(Ball(screen, WHITE, x_pos, y_pos, 10, x_vel, y_vel))

#ball1 = Ball(screen, WHITE, WIDTH // 2, HEIGHT // 2, 10, 12, 5)
#ball2 = Ball(screen, WHITE, random.randint(10, WIDTH - 10), random.randint(10, HEIGHT - 10), 10, 10, 8)

manager = CollisionManager()

playing = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				for ball in balls:
					ball.start_moving()
				playing =  True

			if event.key == pygame.K_ESCAPE:
				sys.exit()


	if playing:
		init_screen()
		for ball in balls:
			ball.move()
			ball.show()

		for ball1 in balls:
			if manager.ball_and_horizontal_wall_collision(ball1):
				ball1.left_and_right_collision()

			if manager.ball_and_vertical_wall_collision(ball1):
				ball1.lower_and_upper_collision()

			"""for ball2 in balls:
				if manager.ball_and_ball_collision(ball2, ball1):
					ball1.ball_and_ball_collision()
					ball2.ball_and_ball_collision()
			"""

	pygame.display.update()
	fpsClock.tick(fps)