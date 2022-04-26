import pygame
from tile import Tile
from settings import tile_size, player_speed, screen_width
from players import Player

class Level:
    def __init__(self,level_data,surface): #surface to draw on

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self,layout):
        # Groups
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout): #enumerate gives a tuple
            for col_index, cell in enumerate(row): #individual char in the str
                #print(f'{row_index},{col_index}:{cell}') # row,col,val
                x = col_index * tile_size
                y = row_index * tile_size
                # level tiles
                if cell == 'X':

                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                # player
                if cell == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)

    # Camera movement
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x



        if player_x < (screen_width / 4) and direction_x < 0: # move left
            self.world_shift = player_speed
            player.speed = 0

        elif player_x > (screen_width - screen_width / 4) and direction_x > 0: # move right
            self.world_shift = -player_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player_speed

    # Collisions
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            # LEFT ADN RIGHT collisions
            if sprite.rect.colliderect(player.rect): # rect is for tile
                if player.direction.x < 0: # moving left
                    player.rect.left = sprite.rect.right # move player to de right of the tile (rect)
                elif player.direction.x > 0: # moving right
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            # UP AND DOWN collisions
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # moving down
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 #reset gravity effect
                elif player.direction.y < 0:  # moving up
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 # Avoids sticks to the ceiling (spiderman effect)

    def run(self):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)