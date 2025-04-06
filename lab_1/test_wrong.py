import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20  # Each block size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Snake Initialization
snake = [(100, 100), (80, 100), (60, 100)]  # Start with 3 blocks
direction = (GRID_SIZE, 0)  # Moving right
food = (200, 200)  # Initial food position

# Game Variables
speed = 10  # Initial speed
score = 0
level = 1
foods_eaten = 0  # Counter for food eaten before level up

# Font for displaying score and level
font = pygame.font.Font(None, 36)

def generate_food():
    """ Generates food in a random position that does not overlap the snake. """
    while True:
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        if (x, y) not in snake:  # Ensure food does not spawn inside snake
            return (x, y)

def check_collision():
    """ Checks if the snake collides with walls or itself. """
    x, y = snake[0]

    # Check for wall collision
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    # Check for self-collision
    if (x, y) in snake[1:]:
        return True

    return False

# Main game loop
running = True
while running:
    pygame.time.delay(100 - speed * 2)  # Adjust speed based on level
    screen.fill(BLACK)  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != (0, GRID_SIZE):
                direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_s and direction != (0, -GRID_SIZE):
                direction = (0, GRID_SIZE)
            elif event.key == pygame.K_a and direction != (GRID_SIZE, 0):
                direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_d and direction != (-GRID_SIZE, 0):
                direction = (GRID_SIZE, 0)

    # Move snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Check collision with food
    if new_head == food:
        food = generate_food()
        score += 10
        foods_eaten += 1
        if foods_eaten >= 3:  # Increase speed and level every 3 foods
            level += 1
            speed += 2
            foods_eaten = 0  # Reset food counter
    else:
        snake.pop()  # Remove tail if no food is eaten

    # Check game over conditions
    if check_collision():
        print(f"Game Over! Your final score: {score}")
        running = False

    # Draw Snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

    # Draw Food
    pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))

    # Display Score  and Level
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()  # Refresh screen

# Quit Pygame
pygame.quit()
