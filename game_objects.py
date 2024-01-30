from random import randint

import pygame.sprite

from constants import CELL_SIZE, HEIGHT, WIDTH
from functions import load_image
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
        map = args[1]
        move_or_not = args[-1]

        # проверяем касается ли наш персонаж врагов
        if pygame.sprite.spritecollideany(self, enemies_group):
            self.hp = 0

        # если нажата кнопка мыши, то мы делаем выстрел
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shot(self.images.index(self.image))

        # далее следует проверка на то в какую сторону нам идти и вообще можем ли мы это сделать
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if map[self.y - 1][self.x] not in '01234567bq':
                    self.y -= 1
                    if move_or_not:
                        self.rect.y -= 75
                self.image = self.images[0]

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if map[self.y + 1][self.x] not in '01234567b':
                    self.y += 1
                    if move_or_not:
                        self.rect.y += 75
                self.image = self.images[2]

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if map[self.y][self.x - 1] not in '01234567b':
                    self.x -= 1
                    if move_or_not:
                        self.rect.x -= 75
                if not move_or_not:
                    self.image = self.images[1]

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if map[self.y][self.x + 1] not in '01234567b':
                    self.x += 1
                    if move_or_not:
                        self.rect.x += 75
                if not move_or_not:
                    self.image = self.images[3]

    def shot(self, number):
        """Функция выстрела"""
        patron = None
        # проверка на ту в какую сторону повернут игрок и создание объекта пули
        if number == 0:
            patron = Patron(self.rect.x + 22, self.rect.y + 5, 0, -7)
        if number == 1:
            patron = Patron(self.rect.x + 5, self.rect.y + 22, -7, 0)
        if number == 2:
            patron = Patron(self.rect.x + 22, self.rect.y + 20, 0, 7)
        if number == 3:
            patron = Patron(self.rect.x + 20, self.rect.y + 22, 7, 0)

        pygame.mixer.init()
        pygame.mixer.music.load('data/shot.mp3')
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.5)

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
        self.meet_wall = False

    def update(self, *args, **kwargs):
        """Обновление патрона"""
        # если касаемся стены, то остаемся на месте
        if pygame.sprite.spritecollideany(self, walls_group) and not self.meet_wall:
            self.speed_y = 0
            self.speed_x = 0
        # если касаемся бочки, то исчезаем
        if pygame.sprite.spritecollideany(self, barrels_group) or pygame.sprite.spritecollideany(self,
                                                                                                 enemies_group):
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

    def __init__(self, x, y, dx, dy, color):
        super().__init__(particles_group)
        if color == 1:
            self.image = load_image('red_hands.png')
        if color == 0:
            self.image = load_image('yellow_hand.png', 1)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x + 30, y + 30
        self.dx, self.dy = dx, dy

    def update(self, *args, **kwargs):
        self.rect.x += self.dx
        self.rect.y += self.dy


class Sword(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, dx, dy):
        super().__init__(enemies_group, all_sprites_group)

        if dx:
            if dx > 0:
                self.image = load_image('sword_0.png')
                self.rect = self.image.get_rect()
                self.rect.x = start_x + 20
                self.rect.y = start_y + 25

                self.start_x = start_x - 15
                self.start_y = start_y

                self.end_x = start_x + 55
                self.end_y = start_y

                self.dx = dx
                self.dy = 0
                self.fast_dx = dx
                self.slow_dx = -1

            if dx < 0:
                self.image = load_image('sword_2.png')
                self.rect = self.image.get_rect()
                self.rect.x = start_x
                self.rect.y = start_y + 25

                self.start_x = start_x + 35
                self.start_y = start_y

                self.end_x = start_x - 35
                self.end_y = start_y

                self.dx = dx
                self.dy = 0
                self.fast_dx = dx
                self.slow_dx = 1

        if dy:
            if dy > 0:
                self.image = load_image('sword_1.png')
                self.rect = self.image.get_rect()
                self.rect.y = start_y + 20
                self.rect.x = start_x + 25

                self.start_x = start_x
                self.start_y = start_y - 15

                self.end_x = start_x
                self.end_y = start_y + 55

                self.dx = 0
                self.dy = dy
                self.fast_dy = dy
                self.slow_dy = -1

            if dy < 0:
                self.image = load_image('sword_3.png')
                self.rect = self.image.get_rect()
                self.rect.y = start_y
                self.rect.x = start_x + 25

                self.start_x = start_x
                self.start_y = start_y + 35

                self.end_x = start_x
                self.end_y = start_y - 35

                self.dx = 0
                self.dy = dy
                self.fast_dy = dy
                self.slow_dy = 1

    def update(self, *args, **kwargs):
        if self.dx:
            if abs(self.rect.x - self.end_x) <= 1:
                self.dx = self.slow_dx
            if abs(self.rect.x - self.start_x) <= 1:
                self.dx = self.fast_dx

            self.rect.x += self.dx

        if self.dy:
            if abs(self.rect.y - self.end_y) <= 1:
                self.dy = self.slow_dy
            if abs(self.rect.y - self.start_y) <= 1:
                self.dy = self.fast_dy
            self.rect.y += self.dy


class FollowingPacman(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__(pacman_group, enemies_group, all_sprites_group)
        self.images = [load_image('pacman_openned.png'), load_image('pacman_closed.png')]
        self.current = 0
        self.image = self.images[self.current]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 800
        self.number = number

        self.time = 0

    def update(self, *args, **kwargs):
        self.rect.y += -1
        if pygame.sprite.spritecollideany(self, player_group):
            self.image = self.images[1]
            self.rect.y -= 20


class Bow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(enemies_group, all_sprites_group)

        if direction == 0:
            self.arrow_speed = (5, 0)
        if direction == 1:
            self.arrow_speed = (0, 5)
        if direction == 2:
            self.arrow_speed = (-5, 0)
        if direction == 3:
            self.arrow_speed = (0, -5)

        self.images = [load_image(f'bow_{direction}.png'), load_image(f'bow_with_arrow_{direction}.png')]

        self.current = 0

        self.image = self.images[self.current]

        self.rect = self.image.get_rect()
        self.rect.x = x + 5
        self.rect.y = y

        self.time = 0

        self.how_long_wait = randint(40, 70)

    def update(self, *args, **kwargs):
        if self.time == self.how_long_wait:
            if self.current == 0:
                self.current = 1
            else:
                Arrow(self.rect.x, self.rect.y, self.arrow_speed[0], self.arrow_speed[1])
                self.current = 0
            self.time = 0

        self.time += 1

        self.image = self.images[self.current]


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__(enemies_group, all_sprites_group)
        if dx:
            if dx > 0:
                self.image = load_image('arrow_0.png')
            if dx < 0:
                self.image = load_image('arrow_2.png')
        if dy:
            if dy > 0:
                self.image = load_image('arrow_1.png')
            if dy < 0:
                self.image = load_image('arrow_3.png')

        self.rect = self.image.get_rect()
        self.rect.x = x + dx * 4 + 20
        self.rect.y = y + dy * 4 + 20
        self.dx = dx
        self.dy = dy

    def update(self, *args, **kwargs):
        if pygame.sprite.spritecollideany(self, walls_group) or pygame.sprite.spritecollideany(self, barrels_group):
            self.kill()
        self.rect.x += self.dx
        self.rect.y += self.dy


class WinPlace(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites_group, win_place_group)
        self.image = load_image('win_place.png')
        self.rect = self.image.get_rect()
        self.rect.x = x + 10
        self.rect.y = y + 10


class BossPacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemies_group)

        self.images = [load_image('pacman_boss_open.png'), load_image('pacman_boss_close.png')]
        self.image = self.images[1]

        self.rect = self.image.get_rect()

        self.rect.x = x * CELL_SIZE - 90
        self.rect.y = y * CELL_SIZE + 50

        self.dx = 2

        self.current = 4
        self.possible_coordinates = [self.rect.x - 3 * CELL_SIZE, self.rect.x - 2 * CELL_SIZE, self.rect.x - CELL_SIZE,
                                     self.rect.x,
                                     self.rect.x + CELL_SIZE, self.rect.x + 2 * CELL_SIZE, self.rect.x + 3 * CELL_SIZE]

        self.wait = False
        self.wait_counter = 0

        self.hp = 20

    def update(self, *args, **kwargs):

        if pygame.sprite.spritecollideany(self, patrons_group):
            self.hp -= 1

        if self.wait:
            if self.wait_counter == 60:
                self.wait_counter = 0
                self.wait = False
            self.wait_counter += 1

        if not self.wait:
            if abs(self.rect.x - self.possible_coordinates[self.current]) <= 1:
                self.image = self.images[0]
                new = self.current
                while new == self.current:
                    self.current = randint(0, 6)

                if self.rect.x > self.possible_coordinates[self.current]:
                    self.dx = -2
                if self.rect.x < self.possible_coordinates[self.current]:
                    self.dx = 2

                self.wait = True

                self.shot(self.rect.x, self.rect.y)
                pygame.mixer.music.load('data/pacman_shot.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(1)

        if not self.wait and self.rect.x != self.possible_coordinates[self.current]:
            self.image = self.images[1]
            self.rect.x += self.dx

    def shot(self, x, y):
        PacPatron(x + 50, y + 100)


class PacPatron(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemies_group)
        self.image = load_image('pac_patron.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dy = 5

    def update(self, *args, **kwargs):
        if pygame.sprite.spritecollideany(self, walls_group):
            self.dy = 0
        self.rect.y += self.dy


class Camera:
    """Класс камеры"""

    def __init__(self, x, y):
        # первичный сдвиг и установка координат игрока
        self.x_shift = WIDTH // 2 - x - 37
        self.y_shift = HEIGHT // 2 - y
        self.shift_for_pacman = 0
        self.x = x
        self.y = y

    def update(self, object):
        """Смещение всех объектов"""

        if type(object) == Sword:
            object.end_x += self.x_shift
            object.start_x += self.x_shift
            object.end_y += self.y_shift
            object.start_y += self.y_shift

        if type(object) == FollowingPacman:
            object.rect.y += self.y_shift * object.number
            object.rect.x += -self.x_shift


        object.rect.x += self.x_shift
        object.rect.y += self.y_shift

    def change(self, new_x, new_y):
        """Изменение сдвига относительно движения игрока"""
        self.x_shift = self.x - new_x
        self.x = new_x
        self.y_shift = self.y - new_y
        self.y = new_y


def generate_level(level):
    """Создание уровня"""
    new_player = None
    pacman = None
    for y in range(len(level)):
        for x in range(len(level[y])):

            if level[y][x] == 'B':
                pacman = BossPacman(x, y)

            # создание бочки
            if level[y][x] == 'b':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                Barrel(x, y, level)

            if level[y][x] == '!':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                WinPlace(x * CELL_SIZE, y * CELL_SIZE)

            if level[y][x] == 't':
                Bow(x * CELL_SIZE, y * CELL_SIZE, 0)
            if level[y][x] == 'y':
                Bow(x * CELL_SIZE, y * CELL_SIZE, 1)
            if level[y][x] == 'u':
                Bow(x * CELL_SIZE, y * CELL_SIZE, 2)
            if level[y][x] == 'i':
                Bow(x * CELL_SIZE, y * CELL_SIZE, 3)

            if level[y][x] == 'q':
                Sword(x * CELL_SIZE, y * CELL_SIZE, 2, 0)
            if level[y][x] == 'e':
                Sword(x * CELL_SIZE, y * CELL_SIZE, -2, 0)
            if level[y][x] == 'w':
                Sword(x * CELL_SIZE, y * CELL_SIZE, 0, 2)
            if level[y][x] == 'r':
                Sword(x * CELL_SIZE, y * CELL_SIZE, 0, -2)

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
    return new_player, pacman


def die_of_hero(x, y, color):
    """Функция, которая создает группу частиц для анимации смерти героя"""
    for dx, dy in ((6, 0), (5, 5), (0, 6), (-6, 0), (-5, -5), (0, -6), (5, -5), (-5, 5)):
        Particles(x, y, dx, dy, color)
