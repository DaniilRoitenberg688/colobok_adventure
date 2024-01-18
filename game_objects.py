import pygame.sprite

from constants import CELL_SIZE, HEIGHT, WIDTH
from functions import *
from groups import *


class Player(pygame.sprite.Sprite):
    """Класс игрока"""
    def __init__(self, start_x, start_y, ):
        super().__init__(player_group)
        # список изображений повернутого спрайта
        self.images = [load_image('full_red.png'), load_image('full_red_left.png'), load_image('full_red_down.png'),
                       load_image('full_red_right.png')]

        # настройка персонажа
        self.image = self.images[0]

        self.rect = self.image.get_rect()

        self.rect.x = start_x + 5.5

        self.rect.y = start_y + 5.5

        self.x = start_x // 75
        self.y = start_y // 75

        self.hp = 25

    def update(self, *args, **kwargs):
        """Обновление персонажа"""
        # получаем событие и карту нашего уровня для дальнейшей проверки
        event = args[0]
        map = args[-1]

        # проверяем касается ли наш персонаж врагов
        if pygame.sprite.spritecollideany(self, enemies_group):
            self.hp = 0

        # если нажата кнопка мыши, то мы делаем выстрел
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shot(self.images.index(self.image))

        # далее следует проверка на то в какую сторону нам идти и вообще можем ли мы это сделать
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if map[self.y - 1][self.x] not in '01234567b':
                    self.y -= 1
                self.image = self.images[0]

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if map[self.y + 1][self.x] not in '01234567b':
                    self.y += 1
                self.image = self.images[2]

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if map[self.y][self.x - 1] not in '01234567b':
                    self.x -= 1
                self.image = self.images[1]

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if map[self.y][self.x + 1] not in '01234567b':
                    self.x += 1
                self.image = self.images[3]

    def shot(self, number):
        """Функция выстрела"""
        # проверка на ту в какую сторону повернут игрок и создание объекта пули
        if number == 0:
            patron = Patron(self.rect.x + 22, self.rect.y + 5, 0, -7)
        if number == 1:
            patron = Patron(self.rect.x + 5, self.rect.y + 22, -7, 0)
        if number == 2:
            patron = Patron(self.rect.x + 22, self.rect.y + 20, 0, 7)
        if number == 3:
            patron = Patron(self.rect.x + 20, self.rect.y + 22, 7, 0)
        return patron


class EmptyGround(pygame.sprite.Sprite):
    """Класс пола"""

    def __init__(self, x, y, number=1):
        super().__init__(all_sprites_group)
        # настройка
        self.image = load_image(f'floor_{number}.png')

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y


class Wall(pygame.sprite.Sprite):
    """Класс стены"""

    def __init__(self, x, y, number):
        super().__init__(walls_group, all_sprites_group)
        # настройка
        self.image = load_image(f'wall_{number}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Patron(pygame.sprite.Sprite):
    """Класс пули"""

    def __init__(self, x, y, speed_x, speed_y):
        super().__init__(patrons_group, all_sprites_group)
        # настройка
        self.image = load_image('red_hands.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, *args, **kwargs):
        """Обновление патрона"""
        # если касаемся стены, то остаемся на месте
        if pygame.sprite.spritecollideany(self, walls_group):
            self.speed_y = 0
            self.speed_x = 0
        # если касаемся бочки, то исчезаем
        if pygame.sprite.spritecollideany(self, barrels_group):
            self.kill()
        # изменение положения объекта
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


class Barrel(pygame.sprite.Sprite):
    """Класс бочка"""

    def __init__(self, x, y, map):
        super().__init__(barrels_group, all_sprites_group)
        # настройка
        self.image = load_image('barrel.png')

        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * CELL_SIZE, y * CELL_SIZE

        self.map = map

        self.hp = 50

    def update(self, *args, **kwargs):
        # если хп ноль или хп 25, в бочку врезался враг, то она исчезает и меняет себя на пустой пол
        if pygame.sprite.spritecollideany(self, enemies_group) and self.hp <= 25 or self.hp <= 0:
            self.map[self.y][self.x] = 's'
            self.kill()

        # если здоровья меньше 25, то меняем изображение спрайта
        if self.hp <= 25:
            self.image = load_image('barrel_25.png')

        # если бочки касается пуля, то снимаем 25 хп
        if pygame.sprite.spritecollideany(self, patrons_group):
            self.hp -= 25


class Enemy(pygame.sprite.Sprite):
    """Класс врага"""
    def __init__(self, x, y, speed):
        super().__init__(enemies_group, all_sprites_group)

        # настройка
        self.image = load_image('enemy_1.png')

        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 10
        self.rect.y = y * CELL_SIZE + 10
        self.x_speed = speed[0]
        self.y_speed = speed[1]

    def update(self, *args, **kwargs):
        """Обновление спрайта"""
        # если враг касается стены или бочки, то меняет свое направление
        if pygame.sprite.spritecollideany(self, barrels_group):
            self.x_speed *= -1
            self.y_speed *= -1
        if pygame.sprite.spritecollideany(self, walls_group):
            self.x_speed *= -1
            self.y_speed *= -1

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


class Particles(pygame.sprite.Sprite):
    """Класс частиц(сделан для анимации смерти игрока)"""
    def __init__(self, x, y, dx, dy):
        super().__init__(particles_group)
        self.image = load_image('red_hands.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 30, y + 30
        self.dx, self.dy = dx, dy

    def update(self, *args, **kwargs):
        self.rect.x += self.dx
        self.rect.y += self.dy


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


def generate_level(level):
    """Создание уровня"""
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # создание бочки
            if level[y][x] == 'b':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                Barrel(x, y, level)
            # создание стены
            if level[y][x] in '01234567':
                Wall(x * CELL_SIZE, y * CELL_SIZE, level[y][x])
            # создание пола
            if level[y][x] == 's':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
            # создание врага который движется горизонтально
            if level[y][x] == 'h':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                Enemy(x, y, (4, 0))
            # создание врага который движется вертикально
            if level[y][x] == 'v':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                Enemy(x, y, (0, 4))
            # создание персонажа
            elif level[y][x] == '@':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                new_player = Player(x * CELL_SIZE, y * CELL_SIZE)
    return new_player


def die_of_hero(x, y):
    """Функция, которая создает группу частиц для анимации смерти героя"""
    for dx, dy in ((6, 0), (5, 5), (0, 6), (-6, 0), (-5, -5), (0, -6), (5, -5), (-5, 5)):
        Particles(x, y, dx, dy)
