import pygame
import datetime
import math

# Load the Mickey Mouse hand image from the images folder
# This image will be used for both the minute and second hands
hand_img = pygame.image.load("images/mickey_hand.png")

def rotate_hand(image, angle):
    """
    Rotate the hand image by a given angle
    Args:
        image: The pygame surface to rotate
        angle: Rotation angle in degrees (negative = clockwise)
    Returns:
        A new rotated surface
    """
    return pygame.transform.rotate(image, angle)

def draw_clock(screen):
    # Fill the entire screen with white color (clearing previous frame)
    screen.fill((255, 255, 255))

    # Define the center point of the clock (middle of 600x600 screen)
    center = (300, 300)

    # Get the current system time
    now = datetime.datetime.now()
    # Extract minutes (0-59) and seconds (0-59)
    minutes = now.minute
    seconds = now.second

    # Calculate rotation angles for the hands
    # Each minute = 6 degrees (360° / 60 minutes)
    # Each second = 6 degrees (360° / 60 seconds)
    # Negative angle makes the hand rotate clockwise (Pygame rotates counter-clockwise by default)
    min_angle = -(minutes * 6)  # Minute hand angle based on current minute
    sec_angle = -(seconds * 6)  # Second hand angle based on current second

    # Rotate the hand image for the minute hand (right hand of Mickey)
    min_hand = rotate_hand(hand_img, min_angle)
    # Get the rectangle that surrounds the rotated image
    min_rect = min_hand.get_rect(center=center)
    # Draw the minute hand at the center of the screen
    screen.blit(min_hand, min_rect)

    # Rotate the SAME hand image for the second hand (left hand of Mickey)
    sec_hand = rotate_hand(hand_img, sec_angle)
    # Get the rectangle for the second hand
    sec_rect = sec_hand.get_rect(center=center)
    # Draw the second hand on top (order determines which hand appears on top)
    screen.blit(sec_hand, sec_rect)