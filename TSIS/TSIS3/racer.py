import pygame
import random
import json
import os

# Initialize pygame modules (graphics + sound)
pygame.init()
pygame.mixer.init()  # Initialize sound system

# ================= CONFIGURATION =================

WIDTH, HEIGHT = 500, 700  # window size
FPS = 60                  # frames per second
ROAD_SCROLL = 6           # background movement speed

# Fonts for UI text
FONT = pygame.font.SysFont("Arial", 20)
BIG = pygame.font.SysFont("Arial", 40)

# ================= COLORS =================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 120, 255)
ORANGE = (255, 140, 0)
GRAY = (120, 120, 120)
YELLOW = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Power-up colors
SHIELD_COLOR = (0, 120, 255)
NITRO_COLOR = (255, 140, 0)
REPAIR_COLOR = (200, 0, 0)

# File for leaderboard saving
LEADERBOARD_FILE = "leaderboard.json"


# ================= SOUND LOADING =================

try:
    # Load background music (looped during gameplay)
    BACKGROUND_SOUND = pygame.mixer.Sound("background.wav")

    # Load sound effects
    CRASH_SOUND = pygame.mixer.Sound("crash.wav")

    # Optional sounds (only if files exist)
    COIN_SOUND = pygame.mixer.Sound("coin.wav") if os.path.exists("coin.wav") else None
    POWERUP_SOUND = pygame.mixer.Sound("powerup.wav") if os.path.exists("powerup.wav") else None
    HURT_SOUND = pygame.mixer.Sound("hurt.wav") if os.path.exists("hurt.wav") else None
    BOOST_SOUND = pygame.mixer.Sound("boost.wav") if os.path.exists("boost.wav") else None
    GAMEOVER_SOUND = pygame.mixer.Sound("gameover.wav") if os.path.exists("gameover.wav") else None

except:
    # If sound files are missing, disable audio safely
    print("Warning: Sound files not found")
    BACKGROUND_SOUND = None
    CRASH_SOUND = None
    COIN_SOUND = None
    POWERUP_SOUND = None
    HURT_SOUND = None
    BOOST_SOUND = None
    GAMEOVER_SOUND = None


# ================= IMAGES =================

# Load and scale game assets
ROAD = pygame.transform.scale(pygame.image.load("AnimatedStreet.png"), (WIDTH, HEIGHT))
PLAYER_IMG = pygame.transform.scale(pygame.image.load("Player.png"), (50, 90))
ENEMY_IMG = pygame.transform.scale(pygame.image.load("Enemy.png"), (50, 90))


# ================= LEADERBOARD FUNCTIONS =================

# Load leaderboard from JSON file
def load_lb():
    if os.path.exists(LEADERBOARD_FILE):
        return json.load(open(LEADERBOARD_FILE))
    return []

# Save leaderboard to file
def save_lb(data):
    json.dump(data, open(LEADERBOARD_FILE, "w"), indent=4)


# ================= BUTTON CLASS =================

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)  # button area
        self.text = text                     # button label

    # draw button
    def draw(self, s):
        pygame.draw.rect(s, GRAY, self.rect)
        s.blit(FONT.render(self.text, True, WHITE),
               (self.rect.x + 10, self.rect.y + 10))

    # check if clicked
    def click(self, pos):
        return self.rect.collidepoint(pos)


# ================= PLAYER CLASS =================

class Player:
    def __init__(self):
        self.x = WIDTH // 2      # start position X
        self.y = HEIGHT - 120    # start position Y
        self.speed = 6           # movement speed
        self.hp = 3              # health points
        self.shield = 0         # shield timer
        self.nitro = 0          # speed boost timer

    # reset player after game over
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 120
        self.hp = 3
        self.shield = 0
        self.nitro = 0

    # move player
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

        # keep player inside screen
        self.x = max(0, min(WIDTH - 50, self.x))
        self.y = max(0, min(HEIGHT - 100, self.y))

    # update timers
    def update(self):
        if self.shield > 0:
            self.shield -= 1  # decrease shield duration
        if self.nitro > 0:
            self.nitro -= 1   # decrease nitro duration

    # draw player and shield effect
    def draw(self, s):
        s.blit(PLAYER_IMG, (self.x, self.y))

        # shield visual effect
        if self.shield > 0:
            pygame.draw.circle(s, SHIELD_COLOR,
                               (self.x + 25, self.y + 40), 50, 2)


# ================= COIN CLASS =================

class Coin:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -20

        # random coin type
        self.t = random.choices(["bronze", "silver", "gold"], [60, 30, 10])[0]

        # define value and color
        if self.t == "bronze":
            self.v = 1
            self.c = BRONZE
            self.r = 10
        elif self.t == "silver":
            self.v = 3
            self.c = SILVER
            self.r = 8
        else:
            self.v = 5
            self.c = YELLOW
            self.r = 6

    # move coin downward
    def update(self):
        self.y += ROAD_SCROLL

    # draw coin
    def draw(self, s):
        pygame.draw.circle(s, self.c, (int(self.x), int(self.y)), self.r)


# ================= ENEMY CLASS =================

class Enemy:
    def __init__(self, speed):
        self.x = random.randint(50, WIDTH - 100)
        self.y = -100
        self.speed = speed

    # movement
    def update(self):
        self.y += self.speed

    # draw enemy car
    def draw(self, s):
        s.blit(ENEMY_IMG, (self.x, self.y))


# ================= OBSTACLE CLASS =================

class Obstacle:
    def __init__(self, t):
        self.x = random.randint(50, WIDTH - 100)
        self.y = -50
        self.t = t  # type of obstacle

    def update(self):
        self.y += ROAD_SCROLL

    def draw(self, s):
        # different obstacle types
        if self.t == "barrier":
            pygame.draw.rect(s, BLACK, (self.x, self.y, 50, 50))
        elif self.t == "speed_bump":
            pygame.draw.rect(s, GRAY, (self.x, self.y, 50, 20))
        elif self.t == "boost":
            pygame.draw.rect(s, ORANGE, (self.x, self.y, 50, 20))


# ================= POWERUP CLASS =================

class PowerUp:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -40
        self.t = random.choice(["shield", "nitro", "repair"])

    def update(self):
        self.y += ROAD_SCROLL

    def draw(self, s):
        color = SHIELD_COLOR if self.t == "shield" else NITRO_COLOR if self.t == "nitro" else REPAIR_COLOR
        pygame.draw.circle(s, color, (self.x, int(self.y)), 12)


# ================= GAME CLASS =================

class Game:
    def __init__(self):
        self.s = pygame.display.set_mode((WIDTH, HEIGHT))
        self.c = pygame.time.Clock()

        self.state = "menu"  # game state
        self.player = Player()

        self.background_playing = False  # music flag

        self.reset_game()

        # UI buttons
        self.buttons = {
            "play": Button(180, 200, 120, 40, "PLAY"),
            "lb": Button(180, 260, 120, 40, "LEADERBOARD"),
            "quit": Button(180, 320, 120, 40, "QUIT"),

            "retry": Button(180, 400, 120, 40, "RESTART"),
            "back": Button(180, 460, 120, 40, "MENU")
        }

    # safe sound play function
    def play_sound(self, sound):
        if sound is not None:
            sound.play()

    # start background music loop
    def start_background(self):
        if BACKGROUND_SOUND and not self.background_playing:
            BACKGROUND_SOUND.play(-1)
            self.background_playing = True

    # stop background music
    def stop_background(self):
        if BACKGROUND_SOUND and self.background_playing:
            BACKGROUND_SOUND.stop()
            self.background_playing = False

    # reset game state
    def reset_game(self):
        self.coins = []
        self.enemies = []
        self.obs = []
        self.pups = []
        self.score = 0
        self.dist = 0
        self.enemy_speed = 4

        self.stop_background()

    # spawn game objects
    def spawn(self):
        if random.random() < 0.5:
            self.coins.append(Coin())
        if random.random() < 0.3:
            self.enemies.append(Enemy(self.enemy_speed))
        if random.random() < 0.3:
            self.obs.append(Obstacle(random.choice(["barrier", "speed_bump", "boost"])))
        if random.random() < 0.25:
            self.pups.append(PowerUp())

    # collision detection
    def hit(self, a, b):
        return abs(a.x - b.x) < 40 and abs(a.y - b.y) < 60

    # handle collisions + game logic
    def check(self):
        for c in self.coins[:]:
            if self.hit(c, self.player):
                self.score += c.v * 10
                self.coins.remove(c)
                self.play_sound(COIN_SOUND)

        for e in self.enemies[:]:
            if self.hit(e, self.player):
                if self.player.shield <= 0:
                    self.player.hp -= 1
                self.enemies.remove(e)
                self.play_sound(CRASH_SOUND)

        # game over condition
        if self.player.hp <= 0:
            self.state = "gameover"
            self.play_sound(GAMEOVER_SOUND)
            self.stop_background()

    # update game logic
    def update(self):
        self.player.update()

        for group in [self.coins, self.enemies, self.obs, self.pups]:
            for obj in group:
                obj.update()

        # remove off-screen objects
        self.coins = [c for c in self.coins if c.y < HEIGHT]

        self.check()

        # spawn new objects randomly
        if random.random() < 0.05:
            self.spawn()

        # start music when playing
        if self.state == "play":
            self.start_background()

    # draw everything
    def draw(self):
        self.s.blit(ROAD, (0, 0))
        self.player.draw(self.s)

        for group in [self.coins, self.enemies, self.obs, self.pups]:
            for obj in group:
                obj.draw(self.s)

        self.s.blit(FONT.render(f"Score:{self.score} HP:{self.player.hp}", True, WHITE), (10, 10))

    # main loop
    def run(self):
        running = True

        while running:
            self.c.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            if self.state == "play":
                self.update()
                self.draw()

            pygame.display.flip()

        pygame.quit()


# ================= START GAME =================

if __name__ == "__main__":
    Game().run()