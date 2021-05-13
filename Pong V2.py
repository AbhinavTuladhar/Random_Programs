import pygame, random, sys, time

reset_counter = 0

pygame.init()

WIDTH = 1200
HEIGHT = 720

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BALL_RADIUS = 8
PAD_WIDTH = 8
PAD_HEIGHT = 100
PAD_SPEED = 10
AI_EFFICIENCY = 75

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")
screen.fill(BLACK)

fps = 240
fpsClock = pygame.time.Clock()

# Initialise the screen
def init_screen():
	screen.fill(BLACK)
	pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 10)

def starting_message():
	font = pygame.font.SysFont("Times New Roman", 30)
	text_to_display = "Press Enter to  play and x to exit."
	length = len(text_to_display)
	text = font.render(text_to_display,  0, WHITE)
	screen.blit(text, (WIDTH // 2 - length * 5, 0))

# Define the paddle class
class Paddle:
	def __init__(self, screen, colour, posX, posY, width, height, player, speed, location):
		self.screen = screen
		self.colour = colour
		self.posX = posX
		self.posY = posY
		self.width = width
		self.height = height
		self.player = player
		self.speed = speed
		self.location = location

		self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
		self.state = 'stopped'

		self.show()

	def show(self):
		# Draw the actual paddle
		pygame.draw.rect(self.screen, self.colour, self.rect)

	def move(self, ball):
		# Statements if the player is controlling
		if self.player == 'player':
			if self.state == 'up':
				self.rect.y -= self.speed

			if self.state == 'down':
				self.rect.y += self.speed

		# For the computer
		if self.player == 'computer':
			if AI_EFFICIENCY < random.randint(0, 100):
				speed = 0
			else:
				speed = self.speed

			if (self.rect.top + self.rect.bottom) // 2 > ball.rect.y:
					self.rect.y -= speed
			if (self.rect.top + self.rect.bottom) // 2 < ball.rect.y:
					self.rect.y += speed

	def clamp(self):
		# Restrict the paddle in the screen
		if self.rect.y <= 0:
			self.rect.y = 0
		if self.rect.bottom >= HEIGHT:
			self.rect.bottom = HEIGHT

class Ball:
	def __init__(self, screen, colour, posX, posY):
		self.screen = screen
		self.colour = colour
		self.posX = posX
		self.posY = posY
		self.radius = BALL_RADIUS

		self.rect = pygame.Rect(self.posX, self.posY, self.radius * 2, self.radius * 2)

		self.dx = 0
		self.dy = 0

		self.show()

	def show(self):
		pygame.draw.circle(self.screen, self.colour, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

		# Reset the position if the ball goes out of bounds
		#if self.rect.x <= -20 or self.rect.x >= WIDTH + 20 or self.rect.y <= -20 or self.rect.y >= HEIGHT + 20:
		#	self.reset_to_center()

	def start_moving(self):
		# Exclude slow choices
		exclude = [-2, -1, 0, 1, 2]
		choices = [x for x in range(-10, 11) if not abs(x) <= 4]

		self.dx = random.choice(choices)
		self.dy = random.choice(choices)

	def move(self):
		self.rect.x += self.dx
		self.rect.y += self.dy

	def vertical_collision(self):
		self.dy = -self.dy

	def horizontal_collision(self):
		self.dx = -self.dx

	def paddle_collision(self):
		self.dx = -self.dx

		exclude = [-2, -1, 0, 1, 2]
		dy = [x for x in range(-10, 11) if not abs(x) <= 4]
		self.dy = int(random.choice(dy))

	# Call this function if a faulty collision is detected
	def reset_to_center(self):
		self.rect.x = self.posX
		self.rect.y = self.posY

class Collision_Manager:
	def ball_vertical_wall_collision(self, ball):
		if ball.rect.top <= 0:
			return True
		if ball.rect.bottom >= HEIGHT:
			return True
		return False

	def ball_horizontal_wall_collision(self, ball):
		if ball.rect.left <= 0:
			return True
		if ball.rect.right >= WIDTH:
			return True
		return False

	def ball_paddle_collision(self, ball, paddle):
		if ball.rect.colliderect(paddle):
			return True
		return False

	def player1_goal(self, ball):
		if ball.rect.right >= WIDTH:
			return True
		return False

	def player2_goal(self, ball):
		if ball.rect.left <= 0:
			return True
		return False

	def faulty_collision(self, ball, paddle):
		global reset_count
		# Check if the ball gets stuck inside the paddles. If so, reset the ball to the central position
		if (paddle.rect.left < ball.rect.centerx and ball.rect.centerx < paddle.rect.right) and (paddle.rect.bottom < ball.rect.centery and ball.rect.centery < paddle.rect.top):
			return True

		if paddle.location == 'left':
			if (paddle.rect.left > ball.rect.left) and (ball.rect.top < paddle.rect.bottom and ball.rect.bottom > paddle.rect.top):
				return True

		if paddle.location == 'right':
			if (ball.rect.top < paddle.rect.bottom and ball.rect.bottom > paddle.rect.top) and (paddle.rect.right < ball.rect.right):
				return True

		return False

	def ball_out_of_bounds(self, ball):
		if ball.rect.left <= -2 * BALL_RADIUS or ball.rect.right >= WIDTH + 2 * BALL_RADIUS or ball.rect.top <= -2 * BALL_RADIUS or ball.rect.bottom >= HEIGHT + 2 * BALL_RADIUS:
			return True
		return False

class Score:
	def __init__(self, screen, points, posX, posY):
		self.screen = screen
		self.points = points
		self.posX = posX
		self.posY = posY
		self.font = pygame.font.SysFont("helvetica", 60, bold = True)
		self.label = self.font.render(self.points, 2, WHITE)
		self.show()

	def show(self):
		self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

	def increase_score(self):
		points = int(self.points) + 1
		self.points = str(points)
		self.label = self.font.render(self.points, 2, WHITE)

class Reset_Counter:
	def __init__(self, screen, reset_count, posX, posY):
		self.screen = screen
		self.posX = posX
		self.posY = posY
		self.reset_count = reset_count
		self.font = pygame.font.SysFont("helvetica", 20, bold = True)
		text = "Reset counter: " + str(self.reset_count)
		self.label = self.font.render(text, 2, WHITE)
		self.show()

	def show(self):
		self.screen.blit(self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

	def increase_resets(self):
		count = int(self.reset_count) + 1
		self.reset_count = str(count)
		text = "Reset counter: " + str(count)
		self.label = self.font.render(text, 2, WHITE)

	def check_glitch(self):
		if int(self.reset_count) > 20:
			print("Possible glitch. Exiting...")
			pygame.quit()

init_screen()
starting_message()

pad1 = Paddle(screen, WHITE, 2 * BALL_RADIUS, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT, 'computer', PAD_SPEED, 'left')
pad2 = Paddle(screen, WHITE, WIDTH - 2 * BALL_RADIUS - PAD_WIDTH, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT, 'computer', PAD_SPEED, 'right')
ball = Ball(screen, WHITE, WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS)
score1 = Score(screen, '0', WIDTH // 4, 20)
score2 = Score(screen, '0', WIDTH - WIDTH // 4, 20)
manager = Collision_Manager()
counter = Reset_Counter(screen, '0', WIDTH - 80, 0)

condition = True
playing = False

while condition:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
			condition = False

		if event.type == pygame.KEYDOWN:
			# Events for paddle1
			if event.key == pygame.K_w:
				pad1.state = 'up'
			if event.key == pygame.K_s:
				pad1.state = 'down'

			# Events for paddle2
			if event.key == pygame.K_UP:
				pad2.state = 'up'
			if event.key == pygame.K_DOWN:
				pad2.state = 'down'

			if event.key == pygame.K_RETURN:
				ball.start_moving()
				playing = True

		if event.type == pygame.KEYUP:
			pad1.state = 'stopped'
			pad2.state = 'stopped'

	if playing:
		init_screen()

		ball.move()
		ball.show()

		pad1.move(ball)
		pad1.clamp()
		pad1.show()

		pad2.move(ball)
		pad2.clamp()
		pad2.show()

		# Check for collision of the ball with vertical wall
		if manager.ball_vertical_wall_collision(ball):
			ball.vertical_collision()

		# Check for collision of the ball with horizontal wall
		if manager.ball_horizontal_wall_collision(ball):
			ball.horizontal_collision()

		# Check for collision of ball with the respective paddles
		if manager.ball_paddle_collision(ball, pad1) or manager.ball_paddle_collision(ball, pad2):
			ball.paddle_collision()

		# Check to increase scores
		if manager.player1_goal(ball):
			score1.increase_score()

		if manager.player2_goal(ball):
			score2.increase_score()

		# Check for faulty collision
		if manager.faulty_collision(ball, pad1) or manager.faulty_collision(ball, pad2):
			ball.reset_to_center()
			counter.increase_resets()
			reset_counter += 1

		if manager.ball_out_of_bounds(ball):
			ball.reset_to_center()
			counter.increase_resets()
			reset_counter += 1

		counter.check_glitch()

		score1.show()
		score2.show()

		counter.show()

	pygame.display.update()
	fpsClock.tick(fps)

# Printing the number of times reset for debugging purposes
print(reset_counter)

pygame.quit()
