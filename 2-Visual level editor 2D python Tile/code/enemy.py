import pygame
from tile import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,'../graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1] #64 - tamaño imagen (1 = vertical)
