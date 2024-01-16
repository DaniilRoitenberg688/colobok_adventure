import pygame

from functions import *

from constants import CELL_SIZE, HEIGHT, WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()

        self.images = [load_image('full_red.png'), load_image('full_red_left.png'), load_image('full_red_down.png'),
                       load_image('full_red_right.png')]

        self.image = self.images[0]

        self.rect = self.image.get_rect()

        self.rect.x = start_x + 5.5
        self.rect.y = start_y + 5.5

        self.x = start_x // 75
        self.y = start_y // 75


    def update(self, *args, **kwargs):
        event = args[0]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.image = self.images[0]
                self.y -= 1
            if event.key == pygame.K_DOWN:
                self.image = self.images[2]
                self.y += 1

            if event.key == pygame.K_LEFT:
                self.image = self.images[1]
                self.x -= 1

            if event.key == pygame.K_RIGHT:
                self.image = self.images[3]
                self.x += 1


class EmptyGround(pygame.sprite.Sprite):
    def __init__(self, x, y, number=1):
        super().__init__()

        self.image = load_image(f'floor_{number}.png')

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__()
        if number == '0':
            self.image = load_image('wall_0.png')
        if number == '1':
            self.image = load_image('wall_1.png')
        if number == '2':
            self.image = load_image('wall_2.png')
        if number == '3':
            self.image = load_image('wall_3.png')

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



class Camera:
    def __init__(self, x, y):
        self.x_shift = WIDTH // 2 - x - 37
        self.y_shift = HEIGHT // 2 - y
        self.x = x
        self.y = y

    def update(self, object):
        object.rect.x += self.x_shift
        object.rect.y += self.y_shift

    def change(self, new_x, new_y):
        self.x_shift = self.x - new_x
        self.x = new_x
        self.y_shift = self.y - new_y
        self.y = new_y


def generate_level(level, player_group: pygame.sprite.Group, main_group: pygame.sprite.Group):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                continue
            if level[y][x] in '01234':
                main_group.add(Wall(x * CELL_SIZE, y * CELL_SIZE, level[y][x]))
            elif level[y][x] == 's':
                main_group.add(EmptyGround(x * CELL_SIZE, y * CELL_SIZE))
            elif level[y][x] == '@':
                main_group.add(EmptyGround(x * CELL_SIZE, y * CELL_SIZE))
                new_player = Player(x * CELL_SIZE, y * CELL_SIZE)
                player_group.add(new_player)
    # вернем игрока, а также размер поля в клетках
    return new_player


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map
