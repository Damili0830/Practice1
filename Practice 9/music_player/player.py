import pygame      # Library for graphics, window, input and sound
import os          # Work with folders/files
import sys         # For exiting program


def run_player():

    # Initialize pygame (graphics, events)
    pygame.init()

    # Initialize mixer (responsible for playing music)
    pygame.mixer.init()

    # Window settings
    WIDTH = 900
    HEIGHT = 500

    # Create window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set window title
    pygame.display.set_caption("Music Player")

    # Clock to control FPS
    timer = pygame.time.Clock()

    # Colors (RGB)
    WHITE = (255, 255, 255)     # background
    BLACK = (0, 0, 0)           # text
    BLUE = (0, 100, 255)        # track info
    GREEN = (0, 180, 0)         # playing status
    RED = (220, 0, 0)           # stopped status
    GRAY = (200, 200, 200)      # progress bar background
    LIGHT_BLUE = (0, 150, 255)  # progress bar fill

    # Fonts for text (different sizes)
    title_font = pygame.font.SysFont("Arial", 36)   # big title
    text_font = pygame.font.SysFont("Arial", 28)    # normal text
    small_font = pygame.font.SysFont("Arial", 22)   # small text

    # Path to folder with music
    music_folder = os.path.join("music", "sample_tracks")

    # Playlist (list of file paths)
    playlist = []

    # Read all files from folder
    if os.path.exists(music_folder):

        # Loop through all files in folder
        for file_name in os.listdir(music_folder):

            # Add only .wav or .mp3 files
            # lower() makes checking safer, because file extension can be .MP3, .WAV, etc.
            if file_name.lower().endswith((".wav", ".mp3")):

                # Save FULL path (important!)
                playlist.append(os.path.join(music_folder, file_name))

    # Sort tracks alphabetically
    playlist.sort()

    # Index of current track
    current_index = 0

    # Flags (state of player)
    playing = False        # is music playing now?
    music_loaded = False   # is track loaded?

    # Variable for total length of current track in seconds
    track_length = 0

    # Function to load current track again
    def load_current_track():
        nonlocal music_loaded, track_length   # allows modifying outer variables

        if len(playlist) > 0:
            # Load selected music file
            pygame.mixer.music.load(playlist[current_index])

            # Create Sound object to get track length
            # get_length() returns duration in seconds
            sound = pygame.mixer.Sound(playlist[current_index])
            track_length = sound.get_length()

            music_loaded = True
        else:
            music_loaded = False
            track_length = 0

    # Load first track (if exists)
    if len(playlist) > 0:
        load_current_track()

    # MAIN LOOP (runs until user quits)
    running = True
    while running:

        # Handle events (keyboard, window, etc.)
        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                running = False

            # Only react when key is pressed
            if event.type == pygame.KEYDOWN:

                # Q = quit program
                if event.key == pygame.K_q:
                    running = False

                # P = play music
                elif event.key == pygame.K_p:

                    # Only play if track is loaded
                    if music_loaded:
                        pygame.mixer.music.play()
                        playing = True

                # S = stop music
                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    playing = False

                # N = next track
                elif event.key == pygame.K_n:

                    if len(playlist) > 0:

                        # Move index forward (loop using 😵
                        current_index = (current_index + 1) % len(playlist)

                        # Load selected track
                        load_current_track()

    def current(self):
        return self.playlist[self.index]
        # Start playing new track
        pygame.mixer.music.play()
        playing = True

        # B = previous track

    elif event.key == pygame.K_b:

    if len(playlist) > 0:
        # Move index backward (loop)
        current_index = (current_index - 1) % len(playlist)

        # Load selected track
        load_current_track()

        # Start playing new track
        pygame.mixer.music.play()
        playing = True

    # Get current playback time in milliseconds
    # get_pos() returns how long current music has been playing
    # divide by 1000 to convert milliseconds to seconds


current_time = pygame.mixer.music.get_pos() / 1000

# If music is stopped, sometimes get_pos() returns -1
# In that case we set current time to 0
if current_time < 0:
    current_time = 0

# Clear screen (draw new frame)
screen.fill(WHITE)

# ===== DRAW UI =====

# Title
title_text = title_font.render(
    "Music Player with Keyboard Controller",
    True,
    BLACK
)
screen.blit(title_text, (120, 30))

# Current track name
if len(playlist) > 0:
    # Get only file name without folder path
    file_name = os.path.basename(playlist[current_index])

    # Remove extension (.mp3 / .wav), keep only clean name
    current_track_name = os.path.splitext(file_name)[0]
else:
    current_track_name = "No tracks found"

track_text = text_font.render(
    f"Current track: {current_track_name}",
    True,
    BLUE
)
screen.blit(track_text, (80, 120))

# Player status (playing / stopped)
if playing:
    status_text = text_font.render("Status: Playing", True, GREEN)
else:
    status_text = text_font.render("Status: Stopped", True, RED)

screen.blit(status_text, (80, 180))

# Track position (e.g. 2/5)
if len(playlist) > 0:
    position_text = text_font.render(
        f"Track position: {current_index + 1}/{len(playlist)}",
        True,
        BLACK
    )
else:
    position_text = text_font.render(
        "Track position: 0/0",
        True,
        BLACK
    )

screen.blit(position_text, (80, 240))

# Current time / total time text
# int() is used to show only whole seconds
# Convert current time to minutes and seconds
current_minutes = int(current_time) // 60
current_seconds = int(current_time) % 60

# Convert total track length to minutes and seconds
total_minutes = int(track_length) // 60
total_seconds = int(track_length) % 60

# Format as MM:SS (02 means always 2 digits, e.g. 01:05)
time_text = small_font.render(
    f"{current_minutes:02}:{current_seconds:02} / {total_minutes:02}:{total_seconds:02}",
    True,
    BLACK
)
screen.blit(time_text, (80, 270))

# ===== PROGRESS BAR =====

# Progress bar position and size
bar_x = 80
bar_y = 300
bar_width = 700
bar_height = 10

# Draw gray background bar
pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

# Calculate progress from 0 to 1
if track_length > 0:
    progress = current_time / track_length
else:
    progress = 0

# Progress should not be more than 1
if progress > 1:
    progress = 1

# Draw filled progress bar
pygame.draw.rect(
    screen,
    LIGHT_BLUE,
    (bar_x, bar_y, int(bar_width * progress), bar_height)
)
# Controls title
        controls_title = text_font.render("Controls:", True, BLACK)
        screen.blit(controls_title, (80, 340))

        # Controls instructions
        c1 = small_font.render("P = Play", True, BLACK)
        c2 = small_font.render("S = Stop", True, BLACK)
        c3 = small_font.render("N = Next track", True, BLACK)
        c4 = small_font.render("B = Previous track", True, BLACK)
        c5 = small_font.render("Q = Quit", True, BLACK)

        # Draw controls on screen
        screen.blit(c1, (100, 380))
        screen.blit(c2, (100, 410))
        screen.blit(c3, (250, 380))
        screen.blit(c4, (250, 410))
        screen.blit(c5, (480, 380))

        # Folder instruction
        note_text = small_font.render(
            "Put .wav or .mp3 files inside music/sample_tracks",
            True,
            BLACK
        )
        screen.blit(note_text, (80, 450))

        # Update screen (show everything)
        pygame.display.flip()

        # Limit FPS (smooth performance)
        timer.tick(60)

    # Quit pygame
    pygame.quit()

    # Exit program completely
    sys.exit()