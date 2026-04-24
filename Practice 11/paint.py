import pygame
import math

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint Program")
    clock = pygame.time.Clock()

    background_color = (255, 255, 255)
    screen.fill(background_color)

    radius = 5
    current_color = (0, 0, 255)

    # Tools:
    # 1 brush, 2 rectangle, 3 circle, 4 eraser
    # 5 square, 6 right triangle, 7 equilateral triangle, 8 rhombus
    tool = "brush"

    drawing = False
    start_pos = None
    end_pos = None

    canvas = pygame.Surface(screen.get_size())
    canvas.fill(background_color)

    while True:
        pressed = pygame.key.get_pressed()

        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                # Colors
                if event.key == pygame.K_r:
                    current_color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    current_color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    current_color = (0, 0, 255)
                elif event.key == pygame.K_k:
                    current_color = (0, 0, 0)
                elif event.key == pygame.K_w:
                    current_color = (255, 255, 255)

                # Tools
                elif event.key == pygame.K_1:
                    tool = "brush"
                elif event.key == pygame.K_2:
                    tool = "rect"
                elif event.key == pygame.K_3:
                    tool = "circle"
                elif event.key == pygame.K_4:
                    tool = "eraser"
                elif event.key == pygame.K_5:
                    tool = "square"
                elif event.key == pygame.K_6:
                    tool = "right_triangle"
                elif event.key == pygame.K_7:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_8:
                    tool = "rhombus"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    end_pos = event.pos

                elif event.button == 3:
                    radius = max(1, radius - 1)

                elif event.button == 4:
                    radius = min(200, radius + 1)

                elif event.button == 5:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    end_pos = event.pos

                    # Brush draws small circles continuously
                    if tool == "brush":
                        pygame.draw.circle(canvas, current_color, event.pos, radius)

                    # Eraser draws white circles
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, background_color, event.pos, radius)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    # Rectangle
                    if tool == "rect" and start_pos and end_pos:
                        rect = make_rect(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, rect, 2)

                    # Circle
                    elif tool == "circle" and start_pos and end_pos:
                        center, circle_radius = make_circle(start_pos, end_pos)
                        pygame.draw.circle(canvas, current_color, center, circle_radius, 2)

                    # Square
                    elif tool == "square" and start_pos and end_pos:
                        rect = make_square(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, rect, 2)

                    # Right triangle
                    elif tool == "right_triangle" and start_pos and end_pos:
                        points = make_right_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, 2)

                    # Equilateral triangle
                    elif tool == "equilateral_triangle" and start_pos and end_pos:
                        points = make_equilateral_triangle(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, 2)

                    # Rhombus
                    elif tool == "rhombus" and start_pos and end_pos:
                        points = make_rhombus(start_pos, end_pos)
                        pygame.draw.polygon(canvas, current_color, points, 2)

        screen.fill(background_color)
        screen.blit(canvas, (0, 0))

        # Shape preview while dragging
        if drawing and start_pos and end_pos:

            if tool == "rect":
                rect = make_rect(start_pos, end_pos)
                pygame.draw.rect(screen, current_color, rect, 2)

            elif tool == "circle":
                center, circle_radius = make_circle(start_pos, end_pos)
                pygame.draw.circle(screen, current_color, center, circle_radius, 2)

            elif tool == "square":
                rect = make_square(start_pos, end_pos)
                pygame.draw.rect(screen, current_color, rect, 2)

            elif tool == "right_triangle":
                points = make_right_triangle(start_pos, end_pos)
                pygame.draw.polygon(screen, current_color, points, 2)

            elif tool == "equilateral_triangle":
                points = make_equilateral_triangle(start_pos, end_pos)
                pygame.draw.polygon(screen, current_color, points, 2)

            elif tool == "rhombus":
                points = make_rhombus(start_pos, end_pos)
                pygame.draw.polygon(screen, current_color, points, 2)

        font = pygame.font.SysFont("Arial", 20)

        info = (
            "1 Brush | 2 Rect | 3 Circle | 4 Eraser | "
            "5 Square | 6 Right Triangle | 7 Equilateral | 8 Rhombus"
        )
        text = font.render(info, True, (0, 0, 0))
        screen.blit(text, (10, 10))

        tool_text = font.render(f"Current tool: {tool} | Radius: {radius}", True, (0, 0, 0))
        screen.blit(tool_text, (10, 35))

        pygame.draw.rect(screen, current_color, (10, 65, 40, 20))

        pygame.display.flip()
        clock.tick(60)


# Create rectangle from two mouse positions
def make_rect(start, end):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x1 - x2)
    height = abs(y1 - y2)

    return pygame.Rect(left, top, width, height)


# Create circle using start point as center
def make_circle(start, end):
    x1, y1 = start
    x2, y2 = end

    center = start
    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

    return center, radius


# Create square from two mouse positions
def make_square(start, end):
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    # Decide direction of drawing
    if x2 < x1:
        x1 -= side
    if y2 < y1:
        y1 -= side

    return pygame.Rect(x1, y1, side, side)


# Create right triangle from two mouse positions
def make_right_triangle(start, end):
    x1, y1 = start
    x2, y2 = end

    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]

    return points


# Create equilateral triangle
def make_equilateral_triangle(start, end):
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    height = int((math.sqrt(3) / 2) * side)

    # Direction depends on mouse movement
    if x2 >= x1:
        left = x1
        right = x1 + side
    else:
        left = x1 - side
        right = x1

    if y2 >= y1:
        top = y1 + height
        bottom = y1
    else:
        top = y1 - height
        bottom = y1

    points = [
        (left, bottom),
        (right, bottom),
        ((left + right) // 2, top)
    ]

    return points


# Create rhombus from two mouse positions
def make_rhombus(start, end):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    return points


main()