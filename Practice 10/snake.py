import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Initial game variables
dx, dy = 1, 0  # Initial movement direction (Right)
snake = [(5, 5)]  # List of tuples representing snake segments
speed = 5
score = 0
level = 1


def gen_food():
    """Generates a random position for food that isn't on the snake's body."""
    while True:
        x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1)
        y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1)
        if (x, y) not in snake:
            return (x, y)


food = gen_food()
run = True

# --- Main Game Loop ---
while run:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # Prevent the snake from reversing directly onto itself
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, 1
            elif event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -1
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = 1, 0
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -1, 0

    # 2. Movement Logic
    head = snake[0]
    new_head = (head[0] + dx, head[1] + dy)

    # 3. Collision Detection
    x, y = new_head

    # Check wall collisions
    if x < 0 or x >= WIDTH // BLOCK_SIZE or y < 0 or y >= HEIGHT // BLOCK_SIZE:
        run = False

    # Check self-collision
    if new_head in snake:
        run = False

    if not run:
        break

    # Add new head to the snake
    snake.insert(0, new_head)

    # 4. Food & Scoring Logic
    if new_head == food:
        score += 1
        food = gen_food()
        # Level up every 3 points
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        # Remove the tail if no food was eaten
        snake.pop()

    # 5. Rendering (Drawing)
    screen.fill(BLACK)  # Clear screen with black

    # Draw food
    pygame.draw.rect(screen, RED, (food[0] * BLOCK_SIZE, food[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Draw snake segments
    for seg in snake:
        pygame.draw.rect(
            screen,
            GREEN,
            (seg[0] * BLOCK_SIZE, seg[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        )

    # Draw UI (Score and Level)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    # Update display and control game speed
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()