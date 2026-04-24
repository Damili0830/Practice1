# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame
pygame.init()

# Background music
pygame.mixer.music.load("/Users/miraskulbaev/Practice1/Practice 10/images/background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 5
SCORE = 0
COINS = 0

# Enemy speed increases after every N coin points
N = 5
last_speed_increase = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load images
background = pygame.image.load("/Users/miraskulbaev/Practice1/Practice 10/images/AnimatedStreet.png")

# Create window
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/miraskulbaev/Practice1/Practice 10/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        # Enemy appears at random x position from the top
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # Move enemy down
        self.rect.move_ip(0, SPEED)

        # If enemy leaves screen, reset and add score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.reset_position()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/miraskulbaev/Practice1/Practice 10/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Move left
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        # Move right
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load original coin image
        self.original_image = pygame.image.load(
            "/Users/miraskulbaev/Practice1/Practice 10/images/Coin.png"
        ).convert_alpha()

        self.weight = 1
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.reset_position()

    def reset_position(self):
        # Coin weight is randomly selected
        # Weight means how many points player earns
        self.weight = random.choice([1, 2, 3])

        # Different weight = different coin size
        if self.weight == 1:
            size = 30
        elif self.weight == 2:
            size = 40
        else:
            size = 50

        # Scale coin image
        self.image = pygame.transform.scale(self.original_image, (size, size))
        self.rect = self.image.get_rect()

        # Coin appears randomly above the screen
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-300, -50)
        )

    def move(self):
        # Coin falls down with same speed as road/enemy
        self.rect.move_ip(0, SPEED)

        # If coin leaves screen, generate a new coin
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


# Create objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)


# Main game loop
while True:

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Show score
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Show coins
    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coins_text, (270, 10))

    # Show speed
    speed_text = font_small.render("Speed: " + str(round(SPEED, 1)), True, BLACK)
    DISPLAYSURF.blit(speed_text, (10, 35))

    # Draw and move sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Check coin collision
    collected_coin = pygame.sprite.spritecollideany(P1, coins)

    if collected_coin:
        # Add coins according to coin weight
        COINS += collected_coin.weight

        # Generate new random coin
        collected_coin.reset_position()

        # Increase enemy speed when player earns every N coins
        if COINS // N > last_speed_increase:
            SPEED += 1
            last_speed_increase = COINS // N

    # Check enemy collision
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("/Users/miraskulbaev/Practice1/Practice 10/images/crash.wav").play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        time.sleep(2)

        pygame.quit()
        sys.exit()

    # Update screen
    pygame.display.update()
    FramePerSec.tick(FPS)