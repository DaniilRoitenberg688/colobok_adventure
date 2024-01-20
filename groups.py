import pygame

player_group = pygame.sprite.Group()
barrels_group = pygame.sprite.Group()
all_sprites_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
patrons_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
particles_group = pygame.sprite.Group()
pacman_group = pygame.sprite.Group()
win_place_group = pygame.sprite.Group()

all_groups = [player_group, barrels_group, all_sprites_group, walls_group, patrons_group, enemies_group,
              particles_group, pacman_group, win_place_group]
