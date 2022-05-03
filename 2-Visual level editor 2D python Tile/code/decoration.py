import pygame
from settings import vertical_tile_number, tile_size, screen_width

mainpath = '../../RESOURCES/2 - Level/graphics/'
class Sky:
    def __init__(self,horizon):
        self.top = pygame.image.load(mainpath + 'decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load(mainpath + 'decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load(mainpath + 'decoration/sky/sky_middle.png').convert()

        self.horizon = horizon

        # strech
        self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))
        self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))

    def draw(self,surface):
        for row in range(vertical_tile_number):
            x = 0
            y = row * tile_size

            if row < self.horizon:
                surface.blit(self.top,(x,y))
            elif row == self.horizon:
                surface.blit(self.middle,(x,y))
            elif row > self.horizon:
                surface.blit(self.bottom,(x,y))