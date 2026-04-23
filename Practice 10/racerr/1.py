import pygame
import random
import os

# Initialize pygame (starts all pygame modules)
pygame.init()

# Get the base directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build full paths to image files
car_path = os.path.join(BASE_DIR, "resources", "player.png")
road_path = os.path.join(BASE_DIR, "resources", "road.png")
coin_path = os.path.join(BASE_DIR, "resources", "coin.png")

# Debug print to check file path
print(road_path)

# Load images into pygame
car_img = pygame.image.load(car_path)
road_img = pygame.image.load(road_path)
coin_img = pygame.image.load(coin_path)

# Set screen size
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window title
pygame.display.set_caption("Racer Game")

# Resize images to fit the game properly
car_img = pygame.transform.scale(car_img, (50, 120))
coin_img = pygame.transform.scale(coin_img, (50, 50))
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Initial position of the car
car_x = WIDTH // 2 - 25
car_y = HEIGHT - 120

# Speed of the car
car_speed = 5

# List to store coins (each coin = [x, y])
coins = []

# Speed of falling coins
coin_speed = 5

# Score counter
score = 0

# Font for displaying score
font = pygame.font.SysFont(None, 36)

# Game clock (controls FPS)
clock = pygame.time.Clock()

# Game loop flag
running = True

while running:
    # Draw background (road image)
    screen.blit(road_img, (0, 0))

    # Check all events (like closing window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys for movement
    keys = pygame.key.get_pressed()

    # Move car left (with boundary check)
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed

    # Move car right (with boundary check)
    if keys[pygame.K_RIGHT] and car_x < WIDTH - 50:
        car_x += car_speed

    # Randomly spawn coins (1/50 chance each frame)
    if random.randint(1, 50) == 1:
        coin_x = random.randint(0, WIDTH - 30)
        coin_y = -30
        coins.append([coin_x, coin_y])

    # Move each coin downward
    for coin in coins:
        coin[1] += coin_speed

    # Define car collision rectangle
    car_rect = pygame.Rect(car_x, car_y, 50, 100)

    new_coins = []

    # Check collision between car and coins
    for coin in coins:
        coin_rect = pygame.Rect(coin[0], coin[1], 30, 30)

        # If collision happens, increase score
        if car_rect.colliderect(coin_rect):
            score += 1
        else:
            # Keep coin if not collected
            new_coins.append(coin)

    # Update coin list
    coins = new_coins

    # Draw all coins on screen
    for coin in coins:
        screen.blit(coin_img, (coin[0], coin[1]))

    # Draw car on screen
    screen.blit(car_img, (car_x, car_y))

    # Render score text
    text = font.render(f"Coins: {score}", True, (0, 0, 0))

    # Show score in top-right corner
    screen.blit(text, (WIDTH - 150, 10))

    # Update screen (refresh display)
    pygame.display.update()

    # Limit FPS to 60 frames per second
    clock.tick(60)

# Quit pygame properly
pygame.quit()