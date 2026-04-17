import pygame


class Ball:
    """A movable red ball that stays within screen boundaries"""

    def __init__(self, width, height):
        # Set the ball's radius in pixels
        self.radius = 25

        # Start the ball at the center of the screen horizontally
        self.x = width // 2
        # Start the ball at the center of the screen vertically
        self.y = height // 2

        # Store screen dimensions for boundary checking
        self.width = width
        self.height = height

    def move(self, dx, dy):
        """Move the ball by dx (delta x) and dy (delta y) pixels"""
        # Calculate potential new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Check horizontal boundaries (left and right edges)
        # Ball cannot go beyond left edge (x = radius) or right edge (x = width - radius)
        if self.radius <= new_x <= self.width - self.radius:
            self.x = new_x  # Update x only if within bounds

        # Check vertical boundaries (top and bottom edges)
        # Ball cannot go beyond top edge (y = radius) or bottom edge (y = height - radius)
        if self.radius <= new_y <= self.height - self.radius:
            self.y = new_y  # Update y only if within bounds

    def draw(self, screen):
        """Draw the ball on the given screen surface"""
        # Draw a red circle at current (x, y) position with specified radius
        # Parameters: (surface, color, center, radius)
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)