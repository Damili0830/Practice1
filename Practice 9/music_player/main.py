import pygame
import sys
from player import MusicPlayer

# Initialize all imported Pygame modules (required for sound, display, etc.)
pygame.init()

# Create the game window: 600 pixels wide, 400 pixels tall
screen = pygame.display.set_mode((600, 400))

# Set the title that appears on the window title bar
pygame.display.set_caption("Music Player")

# Create a MusicPlayer object to handle playback, track switching, etc.
player = MusicPlayer()

# Create a font object for rendering text on the screen
# None = use default system font, 36 = font size in pixels
font = pygame.font.SysFont(None, 36)

# Start the main game loop (runs forever until user quits)
while True:
    # Check all events that have happened since the last frame
    for event in pygame.event.get():
        # If the user clicked the close button (X) on the window
        if event.type == pygame.QUIT:
            # Uninitialize all Pygame modules (cleanup)
            pygame.quit()
            # Exit the program completely
            sys.exit()

        # Check if a keyboard key was pressed down
        if event.type == pygame.KEYDOWN:
            # P key - Play the current track
            if event.key == pygame.K_p:
                player.play()

            # S key - Stop the current playback
            elif event.key == pygame.K_s:
                player.stop()

            # N key - Skip to the next track in the playlist
            elif event.key == pygame.K_n:
                player.next()

            # B key - Go back to the previous track in the playlist
            elif event.key == pygame.K_b:
                player.previous()

            # Q key - Quit the music player application
            elif event.key == pygame.K_q:
                pygame.quit()  # Clean up Pygame
                sys.exit()  # Exit the program

    # Fill the entire screen with black color (RGB: 0, 0, 0)
    # This clears any previous text or graphics
    screen.fill((0, 0, 0))

    # Render the current track name as a text surface
    # f-string displays the track name dynamically
    # True = anti-aliasing (smoother text)
    # (255, 255, 255) = white color
    text = font.render(f"Track: {player.current_track_name()}", True, (255, 255, 255))

    # Draw the text at position (50 pixels from left, 150 pixels from top)
    screen.blit(text, (50, 150))

    # Update the full display surface to show the text
    # Without this, nothing would appear on the screen
    pygame.display.flip()