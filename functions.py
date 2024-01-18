import os
import sys

import pygame

from constants import GREY
from groups import all_groups


def load_image(name, colorkey=None):
    """Функция для загрузки изображения"""
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def clear_groups():
    """Функция для отчистки всех групп спрайтов"""
    for group in all_groups:
        for item in group:
            item.kill()


def load_level(filename):
    """Функция для загрузки уровня"""
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    return level_map


def pause_menu(screen, x, y):
    """Функция, которая рисует окошко паузы"""
    pygame.init()
    # инициализация шрифта для надписи пауза
    font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 70)
    text = font.render("PAUSE", True, GREY)

    # отрисовка основного окошка
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 400, 400))

    # отображение текста паузы
    screen.blit(text, (x + 65, y + 20))

    # отрисовка кнопки для продолжения игры
    pygame.draw.rect(screen, GREY, (x + 30, y + 195, 150, 150))

    # отрисовка треугольничка, который обычно отображает продолжение
    pygame.draw.polygon(screen, (255, 255, 255), ((x + 60, y + 225), (x + 60, y + 320), (x + 150, y + 275)))

    # создание шрифта для надписи "Выход"
    font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 40)
    text = font.render("EXIT", True, (255, 255, 255))

    # отрисовка кнопки выхода
    pygame.draw.rect(screen, GREY, (x + 225, y + 195, 150, 150))

    # отображение надписи выход
    screen.blit(text, (x + 250, y + 235))

    # обновление экрана
    pygame.display.flip()
