import pygame
import sys
import datetime
from clock import Clock

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

# создаём объект часов (ПОСЛЕ WIDTH)
clock = Clock(WIDTH // 2, HEIGHT // 2)

# загрузка картинки
image = pygame.image.load("images/mickeyclock.jpeg")
image = pygame.transform.scale(image, (600, 600))

running = True
while running:
    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute

    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # рисуем фон
    screen.blit(image, (0, 0))

    center_x, center_y = WIDTH // 2, HEIGHT // 2 + 20

    sec_x, sec_y = clock.get_second_hand(seconds)
    min_x, min_y = clock.get_minute_hand(minutes)

    # рисуем стрелки
    pygame.draw.line(screen, (255, 0, 0), (center_x, center_y), (sec_x, sec_y), 3)
    pygame.draw.line(screen, (0, 0, 0), (center_x, center_y), (min_x, min_y), 6)

    pygame.display.flip()

pygame.quit()
sys.exit()
