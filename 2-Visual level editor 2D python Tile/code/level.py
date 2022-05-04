import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height
from tile import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water

class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = -4

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')

        # coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout,'coins')

        # foreground palms
        fg_palms_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, 'fg palms')

        # backgroudn palms
        bg_palms_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, 'bg palms')

        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        cosntraint_layout = import_csv_layout(level_data['cosntraints'])
        self.constraint_sprites = self.create_tile_group(cosntraint_layout,'cosntraints')

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0] * tile_size)
        self.water = Water(screen_height -20, level_width)


    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)] # get the right tile
                        sprite = StaticTile(tile_size,x,y,tile_surface)


                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)] # get the right tile
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size,x,y)

                    if type == 'coins':
                        if val == '0': # gold
                            sprite = Coin(tile_size,x,y,'../graphics/coins/gold')
                        elif val == '1': # silver
                            sprite = Coin(tile_size,x,y,'../graphics/coins/silver')

                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_small',38)
                        if val == '1':
                            sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_large',69)

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)

                    if type == 'cosntraints':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0': # player
                    print('player goes here')
                if val == '1':
                    hat_surface = pygame.image.load('../../RESOURCES/2 - Level/graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites(): # check enemies in sprites
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False): # if enemy is colliding with any constr
               enemy.reverse()

    def run(self):

        # run the entire game/level

        # decoration
        self.sky.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface,self.world_shift)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # background palms
        self.bg_palms_sprites.update(self.world_shift)
        self.bg_palms_sprites.draw(self.display_surface)

        #crate
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        # foreground palms
        self.fg_palms_sprites.update(self.world_shift)
        self.fg_palms_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)    # cosntraints
        self.enemy_collision_reverse()                      # check collisions
        self.enemy_sprites.draw(self.display_surface)
        #self.constraint_sprites.draw(self.display_surface)   # not drawing them

        # player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)


