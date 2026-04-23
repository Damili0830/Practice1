import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# ВАЖНО: путь к папке
player = MusicPlayer("music")

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                running = False

    text = font.render(f"Track: {player.current()}", True, (255, 255, 255))
    screen.blit(text, (50, 150))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()