import pygame.sprite

from constants import CELL_SIZE, HEIGHT, WIDTH, GREY
from functions import *
from groups import *


class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, ):
        super().__init__(player_group)

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
        map = args[-1]

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shot(self.images.index(self.image))

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
        if number == 0:
            patron = Patron(self.rect.x + 22, self.rect.y + 5 , 0, -7)
        if number == 1:
            patron = Patron(self.rect.x + 5, self.rect.y + 22, -7, 0)
        if number == 2:
            patron = Patron(self.rect.x + 22, self.rect.y + 20, 0, 7)
        if number == 3:
            patron = Patron(self.rect.x + 20, self.rect.y + 22, 7, 0)
        return patron


class EmptyGround(pygame.sprite.Sprite):
    def __init__(self, x, y, number=1):
        super().__init__(all_sprites_group)

        self.image = load_image(f'floor_{number}.png')

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, number):
        super().__init__(walls_group, all_sprites_group)
        self.image = load_image(f'wall_{number}.png')

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Patron(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__(patrons_group, all_sprites_group)

        self.image = load_image('red_hands.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, *args, **kwargs):
        if pygame.sprite.spritecollideany(self, walls_group):
            self.speed_y = 0
            self.speed_x = 0
        if pygame.sprite.spritecollideany(self, barrels_group):
            self.kill()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y, map):
        super().__init__(barrels_group, all_sprites_group)
        self.image = load_image('barrel.png')

        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x * CELL_SIZE, y * CELL_SIZE

        self.map = map

        self.hp = 50

    def update(self, *args, **kwargs):
        if self.hp <= 25:
            self.image = load_image('barrel_25.png')

        if self.hp <= 0:
            self.map[self.y][self.x] = 's'
            self.kill()

        if pygame.sprite.spritecollideany(self, patrons_group):
            self.hp -= 25





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
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                continue
            if level[y][x] == 'b':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                Barrel(x, y, level)
            if level[y][x] in '01234567':
                Wall(x * CELL_SIZE, y * CELL_SIZE, level[y][x])
            elif level[y][x] == 's':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
            elif level[y][x] == '@':
                EmptyGround(x * CELL_SIZE, y * CELL_SIZE)
                new_player = Player(x * CELL_SIZE, y * CELL_SIZE)
    # вернем игрока, а также размер поля в клетках
    return new_player


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    return level_map


def pause_menu(screen, x, y):
    pygame.init()
    font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 70)
    text = font.render("PAUSE", True, GREY)
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 400, 400))
    screen.blit(text, (x + 65, y + 20))
    pygame.draw.rect(screen, GREY, (x + 30, y + 195, 150, 150))
    pygame.draw.polygon(screen, (255, 255, 255), ((x + 60, y + 225), (x + 60, y + 320), (x + 150, y + 275)))
    font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 40)
    text = font.render("EXIT", True, (255, 255, 255))
    pygame.draw.rect(screen, GREY, (x + 225, y + 195, 150, 150))
    screen.blit(text, (x + 250, y + 235))
    pygame.display.flip()


if __name__ == '__main__':
    pause_menu()


