import pygame, sys


# Pygame setup
pygame.init()
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

while True:
    # Close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # background color
    screen.fill('black')

    # Update status
    pygame.display.update()
    clock.ticj(60)