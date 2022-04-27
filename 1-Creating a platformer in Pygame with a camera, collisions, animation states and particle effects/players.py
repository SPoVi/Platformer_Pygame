import pygame
from settings import player_speed
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft= pos)

        # player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = player_speed
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle' # not moving
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = '../RESOURCES/1 - Basic platformer/graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]} #subfolder names as a key of de dict
        '''
        idle: direction.y == 0 and direction.x ==0
        run: direction.y == 0 and direction.x !=0
        jump: direction.y < 0
        fall: direction.y > 0
        '''
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over fram index
        self.frame_index  += self.animation_speed
        if self.frame_index >=len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = animation[int(self.frame_index)]
        else:
            flipped_image = pygame.transform.flip(image,True,False) #img,hor,vert
            self.image = flipped_image

        # set rect
        if self.on_ground and self.on_right: # touching ground and sth in right
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        elif self.on_ceiling and self.on_right: # touching ground and sth in right
            self.rect = self.image.get_rect(topight=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)





    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        # Se podria añadir mas condiciones, como que la barra del jetpack no este a cero
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0: # going upwards
            self.status = 'jump'
        elif self.direction.y > 1: #goind downwards. number > than gravity
            self.status = 'fall'

        else:
            if self.direction.x !=0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()

