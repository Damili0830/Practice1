# Import all required libraries
import pygame              # main graphics library
import math                # math operations (triangles, angles, etc.)
import sys                 # system exit control
import tkinter as tk       # file dialog window
from tkinter import filedialog

pygame.init()              # initialize pygame modules


# ================= WINDOW SETTINGS =================

TOOLBAR_W = 180            # width of left toolbar
CANVAS_W  = 1100           # drawing area width
CANVAS_H  = 800            # drawing area height

WIN_W = TOOLBAR_W + CANVAS_W  # total window width
WIN_H = CANVAS_H              # window height

CANVAS_X = TOOLBAR_W          # canvas starts after toolbar


# ================= COLORS =================

BG      = (30, 30, 40)        # background color
TOOLBAR = (22, 22, 32)        # toolbar background
BORDER  = (55, 55, 75)        # borders
ACCENT  = (99, 102, 241)      # highlight color
WHITE   = (255, 255, 255)     # white text
MUTED   = (110, 110, 135)     # secondary text
CANVAS_C = (255, 255, 255)    # canvas background (white)


# ================= COLOR PALETTE =================

# available drawing colors
PALETTE = [
    (255, 0, 0),       # red
    (255, 127, 0),     # orange
    (255, 255, 0),     # yellow
    (0, 200, 0),       # green
    (0, 0, 255),       # blue
    (75, 0, 130),      # indigo
    (148, 0, 211),     # violet
]


# ================= TOOL LIST =================

# available drawing tools
TOOLS = [
    "freehand", "line", "rectangle", "square",
    "circle", "right_triangle", "eq_triangle",
    "rhombus", "fill", "text", "eraser",
]


# tool labels shown in UI
TOOL_LABELS = {
    "freehand": "[H] Freehand",
    "line": "[L] Line",
    "rectangle": "[G] Rectangle",
    "square": "[S] Square",
    "circle": "[C] Circle",
    "right_triangle": "[R] Right Triangle",
    "eq_triangle": "[T] Equilateral Triangle",
    "rhombus": "[P] Rhombus",
    "fill": "[F] Fill Tool",
    "text": "[A] Text Tool",
    "eraser": "[E] Eraser",
}


# keyboard shortcuts → tool mapping
KEY_TO_TOOL = {
    pygame.K_h: "freehand",
    pygame.K_l: "line",
    pygame.K_g: "rectangle",
    pygame.K_s: "square",
    pygame.K_c: "circle",
    pygame.K_r: "right_triangle",
    pygame.K_t: "eq_triangle",
    pygame.K_p: "rhombus",
    pygame.K_f: "fill",
    pygame.K_a: "text",
    pygame.K_e: "eraser",
}


# ================= SHAPE FUNCTIONS =================

# draw equilateral triangle using geometry (math-based)
def draw_eq_triangle(surf, col, p1, p2, size, fill=False):
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]     # direction vector
    length = math.hypot(dx, dy) or 1     # distance

    bx = p2[0] - dx / 2                  # base center X
    by = p2[1] - dy / 2                  # base center Y

    # perpendicular vector (height direction)
    perp_x = -dy / length * (math.sqrt(3)/2 * length)
    perp_y =  dx / length * (math.sqrt(3)/2 * length)

    # triangle points
    pts = [
        p1,
        (int(bx + perp_x/2), int(by + perp_y/2)),
        (int(bx - perp_x/2), int(by - perp_y/2))
    ]

    # draw filled or outline
    if fill:
        pygame.draw.polygon(surf, col, pts)
    else:
        pygame.draw.polygon(surf, col, pts, max(1, size))


# right triangle (simple geometric shape)
def draw_right_triangle(surf, col, p1, p2, size, fill=False):
    pts = [p1, (p1[0], p2[1]), p2]
    if fill:
        pygame.draw.polygon(surf, col, pts)
    else:
        pygame.draw.polygon(surf, col, pts, max(1, size))


# rhombus shape
def draw_rhombus(surf, col, p1, p2, size, fill=False):
    cx = (p1[0]+p2[0])//2   # center X
    cy = (p1[1]+p2[1])//2   # center Y

    w2 = abs(p2[0]-p1[0])//2  # half width
    h2 = abs(p2[1]-p1[1])//2  # half height

    pts = [
        (cx, cy-h2),
        (cx+w2, cy),
        (cx, cy+h2),
        (cx-w2, cy)
    ]

    if fill:
        pygame.draw.polygon(surf, col, pts)
    else:
        pygame.draw.polygon(surf, col, pts, max(1, size))


# ================= FLOOD FILL TOOL =================

# fill tool (paint bucket)
def flood_fill(surface, x, y, new_col):
    old_col = surface.get_at((x, y))[:3]  # original color

    if old_col == new_col:
        return  # no need to fill

    w, h = surface.get_size()
    stack = [(x, y)]
    visited = set()

    surface.lock()  # speed optimization

    while stack:
        cx, cy = stack.pop()

        if (cx, cy) in visited:
            continue
        if not (0 <= cx < w and 0 <= cy < h):
            continue
        if surface.get_at((cx, cy))[:3] != old_col:
            continue

        surface.set_at((cx, cy), new_col)
        visited.add((cx, cy))

        # check neighbors
        stack += [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]

    surface.unlock()


# ================= SAVE FUNCTION =================

# save canvas as image file
def save_file(canvas):
    root = tk.Tk()
    root.withdraw()  # hide main tkinter window

    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG","*.png"),("JPEG","*.jpg"),("BMP","*.bmp")],
        title="Save canvas"
    )

    root.destroy()

    if path:
        pygame.image.save(canvas, path)


# ================= MAIN APPLICATION =================

class PaintApp:

    def __init__(self):
        # create window
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Paint Application")

        # create drawing surface (canvas)
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(CANVAS_C)

        # current tool settings
        self.tool = "freehand"
        self.color = (0, 0, 0)
        self.brush_size = 4
        self.fill_shapes = False

        # drawing state
        self.drawing = False
        self.start_pos = None
        self.last_pos = None
        self.prev_canvas = None

        # text tool state
        self.typing = False
        self.text_input = ""
        self.text_pos = None
        self.font_size = 26

        # fonts
        self.font_ui = pygame.font.SysFont("Segoe UI", 14)
        self.font_bold = pygame.font.SysFont("Segoe UI", 14, bold=True)
        self.font_title = pygame.font.SysFont("Segoe UI", 17, bold=True)

        self._build_rects()


    # ================= UI SETUP =================

    def _build_rects(self):
        self.tool_rects = {}
        self.color_rects = {}

        # tool buttons
        x0, y0 = 8, 46
        for i, t in enumerate(TOOLS):
            self.tool_rects[t] = pygame.Rect(x0, y0 + i*36, TOOLBAR_W-16, 30)

        # color palette buttons
        self._pal_top = y0 + len(TOOLS)*36 + 20

        sw = (TOOLBAR_W - 16) // 7
        for i in range(7):
            self.color_rects[i] = pygame.Rect(8 + i*sw, self._pal_top, sw-2, 28)

        # save button
        self.btn_save = pygame.Rect(8, WIN_H - 46, TOOLBAR_W-16, 32)


    # ================= MAIN LOOP =================

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            # background
            self.screen.fill(BG)

            # draw UI + canvas
            self.draw_canvas()
            self.draw_toolbar()

            pygame.display.flip()
            clock.tick(120)


# ================= PROGRAM START =================

if __name__ == "__main__":
    PaintApp().run()