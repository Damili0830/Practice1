import pygame
import math

def main():
    pygame.init()

    # Create window
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint Program")
    clock = pygame.time.Clock()

    # Canvas background color
    background_color = (255, 255, 255)
    screen.fill(background_color)

    # Current brush radius
    radius = 5

    # Current selected color
    current_color = (0, 0, 255)   # blue by default

    # Current tool:
    # brush, rect, circle, eraser
    tool = "brush"

    # Variables for drawing shapes
    drawing = False
    start_pos = None
    end_pos = None

    # This surface stores the final drawing
    canvas = pygame.Surface(screen.get_size())
    canvas.fill(background_color)

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            # Exit conditions
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # -------------------------
                # Color selection
                # -------------------------
                if event.key == pygame.K_r:
                    current_color = (255, 0, 0)   # red
                elif event.key == pygame.K_g:
                    current_color = (0, 255, 0)   # green
                elif event.key == pygame.K_b:
                    current_color = (0, 0, 255)   # blue
                elif event.key == pygame.K_k:
                    current_color = (0, 0, 0)     # black
                elif event.key == pygame.K_w:
                    current_color = (255, 255, 255)  # white

                # -------------------------
                # Tool selection
                # -------------------------
                elif event.key == pygame.K_1:
                    tool = "brush"
                elif event.key == pygame.K_2:
                    tool = "rect"
                elif event.key == pygame.K_3:
                    tool = "circle"
                elif event.key == pygame.K_4:
                    tool = "eraser"

            # -------------------------
            # Mouse button pressed
            # -------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    drawing = True
                    start_pos = event.pos
                    end_pos = event.pos

                elif event.button == 3:  # right click decreases radius
                    radius = max(1, radius - 1)

                elif event.button == 4:  # mouse wheel up increases radius
                    radius = min(200, radius + 1)

                elif event.button == 5:  # mouse wheel down decreases radius
                    radius = max(1, radius - 1)

            # -------------------------
            # Mouse movement
            # -------------------------
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    end_pos = event.pos

                    # Free drawing with brush
                    if tool == "brush":
                        pygame.draw.circle(canvas, current_color, event.pos, radius)

                    # Eraser draws with background color
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, background_color, event.pos, radius)

            # -------------------------
            # Mouse button released
            # -------------------------
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    # Draw rectangle when mouse released
                    if tool == "rect" and start_pos and end_pos:
                        rect = make_rect(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, rect, 2)

                    # Draw circle when mouse released
                    elif tool == "circle" and start_pos and end_pos:
                        center, circle_radius = make_circle(start_pos, end_pos)
                        pygame.draw.circle(canvas, current_color, center, circle_radius, 2)

        # -------------------------
        # Draw everything
        # -------------------------
        screen.fill(background_color)
        screen.blit(canvas, (0, 0))

        # Preview shapes while dragging
        if drawing and start_pos and end_pos:
            if tool == "rect":
                rect = make_rect(start_pos, end_pos)
                pygame.draw.rect(screen, current_color, rect, 2)

            elif tool == "circle":
                center, circle_radius = make_circle(start_pos, end_pos)
                pygame.draw.circle(screen, current_color, center, circle_radius, 2)

        # -------------------------
        # Show current tool and size
        # -------------------------
        font = pygame.font.SysFont("Arial", 20)
        info = f"Tool: {tool} | Radius: {radius}"
        text = font.render(info, True, (0, 0, 0))
        screen.blit(text, (10, 10))

        # Show color preview
        pygame.draw.rect(screen, current_color, (10, 40, 40, 20))

        pygame.display.flip()
        clock.tick(60)


# Function to create correct rectangle from 2 points
def make_rect(start, end):
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    return pygame.Rect(left, top, width, height)


# Function to define circle center and radius
def make_circle(start, end):
    x1, y1 = start
    x2, y2 = end

    # Center is the starting point
    center = start

    # Radius is distance between start and end
    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    return center, radius


main()