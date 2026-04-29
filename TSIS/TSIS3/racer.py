import pygame
import random
import json
import os

pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# CONFIG
WIDTH, HEIGHT = 500, 700
FPS = 60
ROAD_SCROLL = 6
FONT = pygame.font.SysFont("Arial", 20)
BIG = pygame.font.SysFont("Arial", 40)

# Colors
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

# Powerup colors
SHIELD_COLOR = (0, 120, 255)
NITRO_COLOR = (255, 140, 0)
REPAIR_COLOR = (200, 0, 0)

LEADERBOARD_FILE = "leaderboard.json"

# Load your sound files
try:
    BACKGROUND_SOUND = pygame.mixer.Sound("background.wav")  # background sound
    CRASH_SOUND = pygame.mixer.Sound("crash.wav")  # crash sound
    # Optional sounds (create simple beeps if files don't exist)
    COIN_SOUND = pygame.mixer.Sound("coin.wav") if os.path.exists("coin.wav") else None
    POWERUP_SOUND = pygame.mixer.Sound("powerup.wav") if os.path.exists("powerup.wav") else None
    HURT_SOUND = pygame.mixer.Sound("hurt.wav") if os.path.exists("hurt.wav") else None
    BOOST_SOUND = pygame.mixer.Sound("boost.wav") if os.path.exists("boost.wav") else None
    GAMEOVER_SOUND = pygame.mixer.Sound("gameover.wav") if os.path.exists("gameover.wav") else None
except:
    # If sound files are missing, disable audio safely
    print("Warning: Could not load sound files. Make sure background.wav and crash.wav exist.")
    BACKGROUND_SOUND = None
    CRASH_SOUND = None
    COIN_SOUND = None
    POWERUP_SOUND = None
    HURT_SOUND = None
    BOOST_SOUND = None
    GAMEOVER_SOUND = None

# IMAGES
# If sound files are missing, disable audio safely
ROAD = pygame.image.load("AnimatedStreet.png")
ROAD = pygame.transform.scale(ROAD, (WIDTH, HEIGHT))
PLAYER_IMG = pygame.transform.scale(pygame.image.load("Player.png"), (50, 90))
ENEMY_IMG = pygame.transform.scale(pygame.image.load("Enemy.png"), (50, 90))


# DATA
# Load and scale game assets
def load_lb():
    if os.path.exists(LEADERBOARD_FILE):
        return json.load(open(LEADERBOARD_FILE))
    return []

# Load leaderboard from JSON file
def save_lb(data):
    json.dump(data, open(LEADERBOARD_FILE, "w"), indent=4)


# BUTTON
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h) # button area
        self.text = text # button area

    # button label
    def draw(self, s):
        pygame.draw.rect(s, GRAY, self.rect)
        s.blit(FONT.render(self.text, True, WHITE), (self.rect.x + 10, self.rect.y + 10))

    # check if clicked
    def click(self, pos):
        return self.rect.collidepoint(pos)


# ENTITIES
# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 120
        self.speed = 6
        self.hp = 3 # health points
        self.shield = 0
        self.nitro = 0 # speed boost timer
        self.last_hurt_time = 0

    # speed boost timer
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 120
        self.hp = 3
        self.shield = 0
        self.nitro = 0

    # reset player after game over
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        # move player
        self.x = max(0, min(WIDTH - 50, self.x))
        self.y = max(0, min(HEIGHT - 100, self.y))

    # update timers
    def update(self):
        if self.shield > 0: self.shield -= 1 # decrease shield duration
        if self.nitro > 0: self.nitro -= 1 # decrease shield duration

    def draw(self, s):
        s.blit(PLAYER_IMG, (self.x, self.y))
        if self.shield > 0:
            pygame.draw.circle(s, SHIELD_COLOR, (self.x + 25, self.y + 40), 50, 2)


# Coin class
class Coin:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -20
        # random coin type
        self.t = random.choices(["bronze", "silver", "gold"], [60, 30, 10])[0]
        if self.t == "bronze":
            self.v = 1;self.c = BRONZE;self.r = 10
        elif self.t == "silver":
            self.v = 3;self.c = SILVER;self.r = 8
        else:
            self.v = 5;self.c = YELLOW;self.r = 6

    def update(self):
        self.y += ROAD_SCROLL

    def draw(self, s):
        pygame.draw.circle(s, self.c, (int(self.x), int(self.y)), self.r)


# Enemy class
class Enemy:
    def __init__(self, speed):
        self.x = random.randint(50, WIDTH - 100)
        self.y = -100
        self.speed = speed

    def update(self): self.y += self.speed

    def draw(self, s): s.blit(ENEMY_IMG, (self.x, self.y))


# Obstacles
class Obstacle:
    def __init__(self, t):
        self.x = random.randint(50, WIDTH - 100)
        self.y = -50
        self.t = t

    def update(self):
        self.y += ROAD_SCROLL

    def draw(self, s):
        if self.t == "barrier":
            pygame.draw.rect(s, BLACK, (self.x, self.y, 50, 50))
        elif self.t == "speed_bump":
            pygame.draw.rect(s, GRAY, (self.x, self.y, 50, 20))
        elif self.t == "boost":
            pygame.draw.rect(s, ORANGE, (self.x, self.y, 50, 20))


# Powerups
class PowerUp:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -40
        self.t = random.choice(["shield", "nitro", "repair"])

    def update(self): self.y += ROAD_SCROLL

    def draw(self, s):
        c = SHIELD_COLOR if self.t == "shield" else NITRO_COLOR if self.t == "nitro" else REPAIR_COLOR
        pygame.draw.circle(s, c, (self.x, int(self.y)), 12)


# Game
class Game:
    def __init__(self):
        self.s = pygame.display.set_mode((WIDTH, HEIGHT))
        self.c = pygame.time.Clock()
        pygame.display.set_caption("Racing Game")

        self.state = "menu"
        self.player = Player()

        # Sound flags
        self.background_playing = False

        self.reset_game()

        self.buttons = {
            "play": Button(180, 200, 120, 40, "PLAY"),
            "lb": Button(180, 260, 120, 40, "LEADERBOARD"),
            "quit": Button(180, 320, 120, 40, "QUIT"),

            "retry": Button(180, 400, 120, 40, "RESTART"),
            "back": Button(180, 460, 120, 40, "MENU")
        }

    def play_sound(self, sound):
        """Safely play a sound if it exists"""
        if sound is not None:
            sound.play()

    def stop_background(self):
        """Stop background sound if playing"""
        if self.background_playing and BACKGROUND_SOUND is not None:
            BACKGROUND_SOUND.stop()
            self.background_playing = False

    def start_background(self):
        """Start background sound (looping)"""
        if not self.background_playing and BACKGROUND_SOUND is not None and self.state == "play":
            BACKGROUND_SOUND.play(-1)  # -1 loops forever
            self.background_playing = True

    # Restarting the parameters
    def reset_game(self):
        self.coins = []
        self.enemies = []
        self.obs = []
        self.pups = []
        self.score = 0
        self.dist = 0
        self.enemy_speed = 4

        # Stop background sound
        self.stop_background()

    # SAFE SPAWN
    def safe_x(self):
        while True:
            x = random.randint(50, WIDTH - 100)
            if abs(x - self.player.x) > 100:
                return x

    # Spawn items
    def spawn(self):
        if random.random() < 0.5: self.coins.append(Coin())
        if random.random() < 0.3:
            e = Enemy(self.enemy_speed)
            e.x = self.safe_x()
            self.enemies.append(e)
        if random.random() < 0.3:
            o = Obstacle(random.choice(["barrier", "speed_bump", "boost"]))
            o.x = self.safe_x()
            self.obs.append(o)
        if random.random() < 0.25:
            p = PowerUp()
            p.x = self.safe_x()
            self.pups.append(p)

    # Collisions
    def hit(self, a, b):
        return abs(a.x - b.x) < 40 and abs(a.y - b.y) < 60

    # Checking for collisions
    def check(self):
        for c in self.coins[:]:
            if self.hit(c, self.player):
                self.score += c.v * 10
                self.coins.remove(c)
                # Play coin sound
                self.play_sound(COIN_SOUND)

        for e in self.enemies[:]:
            if self.hit(e, self.player):
                if self.player.shield <= 0:
                    self.player.hp -= 1
                    self.play_sound(HURT_SOUND)
                else:
                    self.play_sound(POWERUP_SOUND)
                self.enemies.remove(e)
                # Play crash sound
                self.play_sound(CRASH_SOUND)

        for o in self.obs[:]:
            if self.hit(o, self.player):
                if o.t == "boost":
                    self.enemy_speed += 1
                    self.play_sound(BOOST_SOUND)
                elif o.t == "barrier" and self.player.shield <= 0:
                    self.player.hp -= 1
                    self.play_sound(HURT_SOUND)
                    self.play_sound(CRASH_SOUND)
                self.obs.remove(o)

        for p in self.pups[:]:
            if self.hit(p, self.player):
                if p.t == "shield":
                    self.player.shield = 300
                    self.play_sound(POWERUP_SOUND)
                elif p.t == "nitro":
                    self.player.nitro = 200
                    self.enemy_speed += 1
                    self.play_sound(BOOST_SOUND)
                elif p.t == "repair":
                    self.player.hp = min(3, self.player.hp + 1)
                    self.play_sound(POWERUP_SOUND)
                self.pups.remove(p)

        if self.player.hp <= 0 and self.state != "gameover":
            self.save_score()
            self.state = "gameover"
            self.play_sound(GAMEOVER_SOUND)
            # Stop background sound on game over
            self.stop_background()

    # Saving the score
    def save_score(self):
        data = load_lb()
        data.append({"name": "Player", "score": self.score, "dist": self.dist})
        data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
        save_lb(data)

    def update(self):
        self.dist += 1
        self.score += 1

        self.player.update()

        for l in [self.coins, self.enemies, self.obs, self.pups]:
            for i in l: i.update()

        self.coins = [c for c in self.coins if c.y < HEIGHT]
        self.enemies = [e for e in self.enemies if e.y < HEIGHT]
        self.obs = [o for o in self.obs if o.y < HEIGHT]
        self.pups = [p for p in self.pups if p.y < HEIGHT]

        self.check()

        if random.random() < 0.05: self.spawn()

        # Start background sound if not playing and game is active
        if not self.background_playing and self.state == "play" and self.player.hp > 0:
            self.start_background()

    def draw(self):
        self.s.blit(ROAD, (0, 0))
        self.player.draw(self.s)

        for l in [self.coins, self.enemies, self.obs, self.pups]:
            for i in l: i.draw(self.s)

        # Draw HUD
        self.s.blit(FONT.render(f"Score:{self.score} HP:{self.player.hp}", True, WHITE), (10, 10))

        # Draw nitro bar if active
        if self.player.nitro > 0:
            nitro_width = int((self.player.nitro / 200) * 100)
            pygame.draw.rect(self.s, ORANGE, (10, 40, nitro_width, 10))

        # Draw shield indicator
        if self.player.shield > 0:
            shield_text = FONT.render(f"SHIELD: {self.player.shield // 60}", True, SHIELD_COLOR)
            self.s.blit(shield_text, (WIDTH - 100, 10))

    def leaderboard(self):
        self.s.fill(BLACK)
        self.s.blit(BIG.render("LEADERBOARD", True, WHITE), (120, 30))

        y = 120
        data = load_lb()
        if not data:
            self.s.blit(FONT.render("No scores yet!", True, WHITE), (150, y))
        else:
            for i, d in enumerate(data):
                self.s.blit(FONT.render(f"{i + 1}. Score:{d['score']} Dist:{d['dist']}", True, WHITE), (120, y))
                y += 30

        self.buttons["back"].draw(self.s)

    def gameover(self):
        self.s.fill(BLACK)
        self.s.blit(BIG.render("GAME OVER", True, RED), (140, 200))
        self.s.blit(FONT.render(f"Score:{self.score}", True, WHITE), (180, 280))

        self.buttons["retry"].draw(self.s)
        self.buttons["back"].draw(self.s)

    def menu(self):
        self.s.fill(BLACK)
        self.s.blit(BIG.render("RACER", True, WHITE), (180, 100))
        for b in [self.buttons["play"], self.buttons["lb"], self.buttons["quit"]]: b.draw(self.s)

    def run(self):
        run = True
        while run:
            self.c.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT: run = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.state == "menu":
                        if self.buttons["play"].click(pos):
                            self.state = "play"
                            self.player.reset()
                            self.reset_game()
                        if self.buttons["lb"].click(pos): self.state = "leaderboard"
                        if self.buttons["quit"].click(pos): run = False

                    elif self.state == "gameover":
                        if self.buttons["retry"].click(pos):
                            self.player.reset()
                            self.reset_game()
                            self.state = "play"
                        if self.buttons["back"].click(pos):
                            self.state = "menu"
                            self.stop_background()

                    elif self.state == "leaderboard":
                        if self.buttons["back"].click(pos): self.state = "menu"

            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT]: dx = -1
            if keys[pygame.K_RIGHT]: dx = 1
            if keys[pygame.K_UP]: dy = -1
            if keys[pygame.K_DOWN]: dy = 1

            self.player.move(dx, dy)

            if self.state == "menu":
                self.menu()
            elif self.state == "play":
                self.update();self.draw()
            elif self.state == "leaderboard":
                self.leaderboard()
            elif self.state == "gameover":
                self.gameover()

            pygame.display.flip()

        # Cleanup
        self.stop_background()
        pygame.quit()


if __name__ == "__main__":
    Game().run()