import pygame


# Main function where the program runs
def main():
    # Initialize all pygame modules
    pygame.init()

    # Create game window (width=640, height=480)
    screen = pygame.display.set_mode((640, 480))

    # Set window title
    pygame.display.set_caption("Paint")

    # Clock object to control FPS
    clock = pygame.time.Clock()

    # Current drawing color (blue by default)
    color = (0, 0, 255)

    # List to store brush points (used for smooth drawing)
    points = []

    # Current drawing mode: brush, rectangle, circle, eraser
    mode = "brush"

    # Starting position for shapes (rectangle/circle)
    start_pos = None

    # Brush radius (thickness)
    radius = 15

    # Main loop flag
    run = True

    # Main game loop
    while run:
        # Event handling loop
        for event in pygame.event.get():

            # If user closes window
            if event.type == pygame.QUIT:
                run = False

            # Keyboard input handling
            if event.type == pygame.KEYDOWN:

                # Change color to red
                if event.key == pygame.K_r:
                    color = (255, 0, 0)

                # Change color to green
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)

                # Change color to blue
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)

                # Change color to yellow
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)

                # Switch to brush mode
                elif event.key == pygame.K_1:
                    mode = 'brush'

                # Switch to rectangle mode
                elif event.key == pygame.K_2:
                    mode = 'rectangle'

                # Switch to circle mode
                elif event.key == pygame.K_3:
                    mode = 'circle'

                # Switch to eraser mode
                elif event.key == pygame.K_4:
                    mode = 'eraser'

            # Mouse button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    start_pos = event.pos  # Save starting position

            # Mouse button released
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    end_pos = event.pos  # Save ending position

                    # Draw rectangle
                    if mode == 'rectangle':
                        rect = pygame.Rect(
                            start_pos,
                            (end_pos[0] - start_pos[0],
                             end_pos[1] - start_pos[1])
                        )
                        pygame.draw.rect(screen, color, rect, 2)

                    # Draw circle
                    elif mode == 'circle':
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]

                        # Calculate radius using distance formula
                        radius_circle = int((dx ** 2 + dy ** 2) ** 0.5)

                        pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

                    # Reset starting position
                    start_pos = None

            # Mouse movement handling
            if event.type == pygame.MOUSEMOTION:

                # If left mouse button is held down
                if pygame.mouse.get_pressed()[0]:

                    # Brush drawing mode
                    if mode == 'brush':
                        points.append(event.pos)

                        # Keep only last 256 points (performance optimization)
                        points = points[-256:]

                    # Eraser mode
                    elif mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, 20)

        # Smooth brush drawing between stored points
        if mode == 'brush':
            for i in range(len(points) - 1):
                drawLineBetween(screen, points[i], points[i + 1], radius, color)

        # Update the display
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)


# Function to draw smooth line between two points
def drawLineBetween(screen, start, end, width, color):
    # Distance in x and y directions
    dx = start[0] - end[0]
    dy = start[1] - end[1]

    # Number of steps between points
    iterations = max(abs(dx), abs(dy))

    # Interpolate points between start and end
    for i in range(iterations):
        progress = i / iterations

        # Linear interpolation for x and y
        x = int(start[0] + (end[0] - start[0]) * progress)
        y = int(start[1] + (end[1] - start[1]) * progress)

        # Draw small circle to create smooth line effect
        pygame.draw.circle(screen, color, (x, y), width)


# Run the program
main()