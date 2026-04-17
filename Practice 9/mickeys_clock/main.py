
import pygame
import sys
from clock import draw_clock

# Initialize all imported Pygame modules
pygame.init()

# Set up the display window dimensions (600x600 pixels)
WIDTH, HEIGHT = 600, 600
# Create the game window with specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the title that appears on the window title bar
pygame.display.set_caption("Mickey Clock")

# Create a Clock object to control the frame rate
clock = pygame.time.Clock()

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

    # Call the draw_clock function from clock.py
    # This function draws the Mickey Mouse clock face with moving hands
    draw_clock(screen)

    # Update the full display surface to the screen
    # Without this, nothing would be visible
    pygame.display.flip()

    # Control the frame rate to 60 frames per second
    # This keeps the clock smooth and prevents using 100% CPU
    clock.tick(60)
