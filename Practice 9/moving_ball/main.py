import pygame
import sys
from ball import Ball

pygame.init()

# Set the game window dimensions: 600 pixels wide, 400 pixels tall
WIDTH, HEIGHT = 600, 400

# Create the game window with the specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title that appears on the window title bar
pygame.display.set_caption("Moving Ball")

# Create a Ball object, passing the screen boundaries so the ball knows its limits
ball = Ball(WIDTH, HEIGHT)

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

    # Get the current state of all keyboard keys
    # Returns a list where each key is either pressed (True) or not (False)
    keys = pygame.key.get_pressed()

    # Move the ball UP if the UP arrow key is pressed
    # Negative Y moves the ball upward on the screen
    if keys[pygame.K_UP]:
        ball.move(0, -20)   # dx=0 (no horizontal movement), dy=-20 (move up)

    # Move the ball DOWN if the DOWN arrow key is pressed
    # Positive Y moves the ball downward on the screen
    if keys[pygame.K_DOWN]:
        ball.move(0, 20)    # dx=0 (no horizontal movement), dy=20 (move down)

    # Move the ball LEFT if the LEFT arrow key is pressed
    # Negative X moves the ball leftward on the screen
    if keys[pygame.K_LEFT]:
        ball.move(-20, 0)   # dx=-20 (move left), dy=0 (no vertical movement)

    # Move the ball RIGHT if the RIGHT arrow key is pressed
    # Positive X moves the ball rightward on the screen
    if keys[pygame.K_RIGHT]:
        ball.move(20, 0)    # dx=20 (move right), dy=0 (no vertical movement)

    # Clear the entire screen with white color (RGB: 255, 255, 255)
    # This erases the ball from its previous position
    screen.fill((255, 255, 255))

    # Draw the ball at its current (x, y) position on the screen
    ball.draw(screen)

    # Update the full display surface to make the ball visible
    # Without this, nothing would appear on the screen
    pygame.display.flip()

    # Control the frame rate to 60 frames per second
    # This keeps movement smooth and prevents using 100% CPU
    clock.tick(60)