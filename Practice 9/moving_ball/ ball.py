import pygame   # Library for creating games (graphics, input, window)
import sys      # Used to properly exit the program


def run_ball_game():

    # Initialize all pygame modules (must be called first)
    pygame.init()

    # Screen size (width and height of window)
    WIDTH = 800
    HEIGHT = 600

    # Create game window with given size
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set window title
    pygame.display.set_caption("Moving Ball Game")

    # Clock object to control FPS (frame rate)
    timer = pygame.time.Clock()

    # Define colors using RGB (Red, Green, Blue)
    WHITE = (255, 255, 255)   # background color
    RED = (255, 0, 0)         # ball color
    BLACK = (0, 0, 0)         # text color

    # Ball properties
    ball_radius = 25                  # size of the ball
    ball_x = WIDTH // 2               # start position X (center horizontally)
    ball_y = HEIGHT // 2              # start position Y (center vertically)

    # How many pixels ball moves per key press
    move_step = 20

    # Create font for text
    font = pygame.font.SysFont("Arial", 28)

    # Main game loop (runs until window is closed)
    running = True
    while running:

        # Loop through all events (keyboard, mouse, close, etc.)
        for event in pygame.event.get():

            # If user clicks "X" button → close window
            if event.type == pygame.QUIT:
                running = False

            # Only react when a key is pressed DOWN (not held)
            if event.type == pygame.KEYDOWN:

                # Move LEFT
                if event.key == pygame.K_LEFT:

                    # Check boundary (so ball doesn't go outside screen)
                    # New position must still be >= 0
                    if ball_x - move_step - ball_radius >= 0:
                        ball_x = ball_x - move_step   # move left

                # Move RIGHT
                elif event.key == pygame.K_RIGHT:

                    # Check right boundary (must not exceed WIDTH)
                    if ball_x + move_step + ball_radius <= WIDTH:
                        ball_x = ball_x + move_step   # move right

                # Move UP
                elif event.key == pygame.K_UP:

                    # Check top boundary
                    if ball_y - move_step - ball_radius >= 0:
                        ball_y = ball_y - move_step   # move up

                # Move DOWN
                elif event.key == pygame.K_DOWN:

                    # Check bottom boundary
                    if ball_y + move_step + ball_radius <= HEIGHT:
                        ball_y = ball_y + move_step   # move down

        # Fill screen with white color (clears previous frame)
        screen.fill(WHITE)

        # Draw the ball (circle)
        # Parameters: surface, color, (x, y), radius
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        # Create text surface (render text)
        text = font.render("Use arrow keys to move the ball", True, BLACK)

        # Draw text on screen at position (200, 30)
        screen.blit(text, (200, 30))

        # Update screen (show everything we drew)
        pygame.display.flip()

        # Limit FPS to 60 (smooth animation)
        timer.tick(60)

    # Quit pygame when loop ends
    pygame.quit()

    # Close program completely
    sys.exit()