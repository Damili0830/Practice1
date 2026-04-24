import pygame
import sys
import random

# -----------------------------
# Initialize pygame
# -----------------------------
pygame.init()

# -----------------------------
# Screen settings
# -----------------------------
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Number of cells in the grid
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Create game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# -----------------------------
# Colors
# -----------------------------
BLACK = (255, 255, 255)      # background color
WHITE = (0, 0, 0)            # text color
GREEN = (0, 200, 0)          # snake body
DARK_GREEN = (0, 120, 0)     # snake head
RED = (220, 0, 0)            # normal food
ORANGE = (255, 140, 0)       # medium food
PURPLE = (160, 32, 240)      # heavy food
BLUE = (50, 150, 255)        # speed text

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 40)

# -----------------------------
# Clock and game speed
# -----------------------------
clock = pygame.time.Clock()
BASE_SPEED = 7

# Food disappears after this time
FOOD_LIFETIME = 5000  # milliseconds = 5 seconds

# Number of score points needed to level up
FOODS_PER_LEVEL = 4


# -----------------------------
# Function: draw text on screen
# -----------------------------
def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))


# -----------------------------
# Function: draw one grid cell
# -----------------------------
def draw_cell(color, position):
    x, y = position
    rect = pygame.Rect(
        x * CELL_SIZE,
        y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(screen, color, rect)


# -----------------------------
# Function: generate random food
# Food has:
# - position
# - weight
# - color
# - spawn time
# -----------------------------
def generate_food(snake):
    while True:
        food_position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

        # Food must not appear on the snake body
        if food_position not in snake:
            break

    # Random food weight
    # Weight means how many points snake gets
    weight = random.choice([1, 2, 3])

    # Food color depends on weight
    if weight == 1:
        color = RED
    elif weight == 2:
        color = ORANGE
    else:
        color = PURPLE

    # Save time when food appeared
    spawn_time = pygame.time.get_ticks()

    return {
        "position": food_position,
        "weight": weight,
        "color": color,
        "spawn_time": spawn_time
    }


# -----------------------------
# Function: show game over screen
# -----------------------------
def game_over_screen(score, level):
    screen.fill(BLACK)

    game_over_text = big_font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    exit_text = font.render("Press any key to exit", True, WHITE)

    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 80))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
    screen.blit(level_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 30))
    screen.blit(exit_text, (WINDOW_WIDTH // 2 - 110, WINDOW_HEIGHT // 2 + 80))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()


# -----------------------------
# Main game function
# -----------------------------
def main():
    # Snake starts with 3 blocks
    snake = [(5, 5), (4, 5), (3, 5)]

    # Initial direction
    direction = (1, 0)

    # Create first food
    food = generate_food(snake)

    # Score and level
    score = 0
    level = 1

    # Snake speed
    speed = BASE_SPEED

    # Game loop
    while True:

        # -----------------------------
        # Handle events
        # -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Move up
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)

                # Move down
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)

                # Move left
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)

                # Move right
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # -----------------------------
        # Move snake
        # -----------------------------
        head_x, head_y = snake[0]
        dx, dy = direction

        new_head = (head_x + dx, head_y + dy)

        # -----------------------------
        # Border collision
        # Snake dies if it leaves the map
        # -----------------------------
        if (
            new_head[0] < 0 or
            new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or
            new_head[1] >= GRID_HEIGHT
        ):
            game_over_screen(score, level)

        # -----------------------------
        # Self collision
        # -----------------------------
        if new_head in snake:
            game_over_screen(score, level)

        # Add new head
        snake.insert(0, new_head)

        # -----------------------------
        # Check if food disappeared
        # -----------------------------
        current_time = pygame.time.get_ticks()

        if current_time - food["spawn_time"] > FOOD_LIFETIME:
            food = generate_food(snake)

        # -----------------------------
        # Check if snake eats food
        # -----------------------------
        if new_head == food["position"]:

            # Add score according to food weight
            score += food["weight"]

            # Snake grows depending on food weight
            # If weight is 3, snake becomes longer faster
            for i in range(food["weight"] - 1):
                snake.append(snake[-1])

            # Generate new food
            food = generate_food(snake)

            # Level system
            if score // FOODS_PER_LEVEL + 1 > level:
                level += 1
                speed += 2

        else:
            # If food is not eaten, remove tail
            snake.pop()

        # -----------------------------
        # Draw everything
        # -----------------------------
        screen.fill(BLACK)

        # Draw snake head
        draw_cell(DARK_GREEN, snake[0])

        # Draw snake body
        for part in snake[1:]:
            draw_cell(GREEN, part)

        # Draw food
        draw_cell(food["color"], food["position"])

        # -----------------------------
        # Draw food timer
        # -----------------------------
        time_left = FOOD_LIFETIME - (pygame.time.get_ticks() - food["spawn_time"])
        seconds_left = max(0, time_left // 1000)

        draw_text(f"Food disappears in: {seconds_left}s", font, WHITE, 10, 35)

        # Draw score, level, speed
        draw_text(f"Score: {score}", font, WHITE, 10, 10)
        draw_text(f"Level: {level}", font, WHITE, 500, 10)
        draw_text(f"Speed: {speed}", font, BLUE, 250, 10)

        # Show food weight
        draw_text(f"Food weight: {food['weight']}", font, WHITE, 10, 60)

        # Update screen
        pygame.display.update()

        # Control game speed
        clock.tick(speed)


# -----------------------------
# Run game
# -----------------------------
main()