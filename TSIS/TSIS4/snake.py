import pygame          # game library
import random          # for random positions and events
import psycopg2        # PostgreSQL database connection

# ================= DATABASE CONNECTION =================

# connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="phonebook_db",   # database name
    user="postgres",         # database user
    password="123",          # password
    host="localhost",        # server address
    port="5432"              # default PostgreSQL port
)

cur = conn.cursor()  # cursor used to execute SQL queries


# ================= PLAYER FUNCTIONS =================

# get existing player or create a new one
def get_or_create_player(username):

    # search player by username
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    res = cur.fetchone()

    # if player exists, return ID
    if res:
        return res[0]

    # if not exists, create new player
    cur.execute(
        "INSERT INTO players(username) VALUES(%s) RETURNING id",
        (username,)
    )
    conn.commit()  # save changes in database

    return cur.fetchone()[0]


# ================= SAVE GAME DATA =================

# save game result into database
def save_game(player_id, score, level):

    cur.execute(
        "INSERT INTO game_sessions(player_id, score, level_reached) VALUES(%s,%s,%s)",
        (player_id, score, level)
    )

    conn.commit()  # commit transaction


# ================= TOP 10 PLAYERS =================

# get top 10 highest scores
def get_top10():

    cur.execute("""
        SELECT username, score
        FROM game_sessions
        JOIN players ON players.id = game_sessions.player_id
        ORDER BY score DESC
        LIMIT 10
    """)

    return cur.fetchall()  # return list of results


# ================= BEST SCORE =================

# get best score of a specific player
def get_best(player_id):

    cur.execute(
        "SELECT MAX(score) FROM game_sessions WHERE player_id=%s",
        (player_id,)
    )

    res = cur.fetchone()[0]

    return res if res else 0  # return 0 if no score exists


# ================= GAME SETTINGS =================

settings = {
    "difficulty": 1,   # game difficulty level
    "controls": "WASD", # control type
    "grid": True       # grid background toggle
}


# ================= PYGAME INITIALIZATION =================

pygame.init()  # initialize pygame

WIDTH, HEIGHT = 800, 600   # window size
CELL = 20                  # snake grid size
PADDING = 4                # visual padding

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # game window
clock = pygame.time.Clock()  # FPS controller
font = pygame.font.SysFont("Bandal", 28)  # font for text


# ================= COLORS =================

LIGHT_GREEN = (34, 139, 34)
DARK_GREEN = (44, 160, 44)
WHITE = (255, 255, 255)

SNAKE_COLOR = (180, 0, 0)
APPLE = (247, 10, 109)
PEAR = (0, 255, 0)
PEACH = (247, 137, 10)
POISON = (11, 26, 4)
OBST = (50, 50, 50)

# power-up colors
SPEED = (255, 255, 255)
SLOW = (255, 255, 255)
SHIELD = (56, 54, 179)


# ================= TEXT DRAW FUNCTION =================

# draw text on screen
def draw_text(text, x, y, selected=False):

    color = (255, 255, 0) if selected else WHITE  # highlight selected option

    screen.blit(font.render(text, True, color), (x, y))


# ================= DRAW BACKGROUND GRID =================

# draw checkerboard-style grid background
def draw_bg():

    for r in range(HEIGHT // CELL):  # rows
        for c in range(WIDTH // CELL):  # columns

            color = LIGHT_GREEN if (r + c) % 2 == 0 else DARK_GREEN

            rect = pygame.Rect(c * CELL, r * CELL, CELL, CELL)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 60, 0), rect, 1)


# ================= RANDOM POSITION GENERATOR =================

# generate safe random position
def random_position(snake, obstacles):

    while True:
        pos = (
            random.randint(0, WIDTH // CELL - 1) * CELL,
            random.randint(0, HEIGHT // CELL - 1) * CELL
        )

        # avoid spawning inside snake or obstacles
        if pos not in snake and pos not in obstacles:
            return pos


# ================= POWERUP SPAWN =================

# randomly spawn powerups
def spawn_powerup(snake, obstacles):

    if random.random() < 0.01:  # 1% chance
        return random.choice(["speed", "slow", "shield"]), random_position(snake, obstacles)

    return None, None


# ================= USERNAME INPUT SCREEN =================

def get_username():

    name = ""  # player name input

    while True:
        screen.fill((0, 0, 0))  # clear screen

        draw_text("Enter Username:", 280, 250)
        draw_text(name, 280, 300)

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_RETURN and name:
                    return name  # confirm name

                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # delete last letter

                else:
                    name += e.unicode  # add typed character

        pygame.display.flip()


# ================= MAIN MENU =================

def main_menu():

    options = ["Play", "Leaderboard", "Settings", "Exit"]
    selected = 0

    while True:
        screen.fill((0, 0, 0))

        # draw menu options
        for i, opt in enumerate(options):
            draw_text(opt, 350, 200 + i * 50, i == selected)

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)

                if e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)

                if e.key == pygame.K_RETURN:
                    return options[selected]

        pygame.display.flip()


# ================= MAIN GAME =================

def game(player_id, best):

    snake = [(100, 100)]  # initial snake position
    direction = (CELL, 0)  # moving right

    obstacles = []  # obstacle list

    food = random_position(snake, obstacles)
    food_type = "apple"
    food_value = 1

    score = 0
    level = 1
    lives = 3

    base_speed = {1: 8, 2: 10, 3: 14}[settings["difficulty"]]
    speed = base_speed

    # ================= GAME LOOP =================

    while True:

        draw_bg()

        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:

                # WASD controls
                if settings["controls"] == "WASD":

                    if e.key == pygame.K_w:
                        direction = (0, -CELL)

                    if e.key == pygame.K_s:
                        direction = (0, CELL)

                    if e.key == pygame.K_a:
                        direction = (-CELL, 0)

                    if e.key == pygame.K_d:
                        direction = (CELL, 0)

        # move snake head
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # collision with wall
        if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            break

        snake.insert(0, head)

        # food collision
        if head == food:
            score += food_value
            food = random_position(snake, obstacles)
        else:
            snake.pop()

        pygame.display.flip()
        clock.tick(speed)

    return score, level


# ================= START GAME =================

username = get_username()
player_id = get_or_create_player(username)

while True:

    best = get_best(player_id)
    choice = main_menu()

    if choice == "Play":
        score, level = game(player_id, best)
        save_game(player_id, score, level)

    elif choice == "Exit":
        break

pygame.quit()