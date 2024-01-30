import time

from constants import *
from functions import load_level, clear_groups, pause_menu, win_window
from game_objects import *


def first_level():
    """Функция для запуска обучения"""
    now_time = time.time()

    # создание и настройка экрана
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # создание условия завершения цикла и часов
    running = True
    clock = pygame.time.Clock()

    # загрузка уровня
    level = load_level('map1.txt')

    # отображение уровня
    player, _ = generate_level(level)

    # создание камеры и настройка уровня
    camera = Camera(player.rect.x, player.rect.y)
    for sprite in all_sprites_group:
        camera.update(sprite)
    camera.update(player)

    # флаг паузы
    is_pause = False

    # жив ли игрок или нет
    alive_or_not = True

    # идет ли анимация смерти
    animation_is_running = False

    win_or_not = False

    animation_time = 0

    FollowingPacman(2.5)

    while running:
        # закрашиваем в серый
        screen.fill(BACKGROUND_GREY)

        # пробегаемся по событиям
        for event in pygame.event.get():
            # выходим
            if event.type == pygame.QUIT:
                clear_groups()
                running = False

            if win_or_not:
                if event.type == pygame.KEYDOWN:
                    running = False

            # если нажата клавиша ESCAPE запускаем паузу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_pause = True

            # если пауза отслеживаем нажатие игрока
            if is_pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # получаем координаты клика
                    x = event.pos[0]
                    y = event.pos[1]

                    if 100 < x < 500 and 100 < y < 500:
                        # если нажата кнопка продолжить убираем паузу
                        if 130 < x < 280 and 295 < y < 445:
                            is_pause = False
                            continue

                        # если нажата кнопка выход выходим
                        if 325 < x < 625 and 295 < y < 445:
                            running = False
                            clear_groups()

            # если нет паузы обновляем игрока и камеру(это сделано для того чтобы во время паузы игрок не бегал)
            if not is_pause:
                player_group.update(event, level, False)

                camera.change(player.x * CELL_SIZE + 5.5, player.y * CELL_SIZE + 5.5)
                for sprite in all_sprites_group:
                    camera.update(sprite)

        # проверка на то жив ли наш персонаж
        if pygame.sprite.spritecollideany(player, enemies_group):
            alive_or_not = False

        if pygame.sprite.spritecollideany(player, win_place_group):
            win_or_not = True
            pygame.mixer.music.load('data/si.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(1)
            finish_time = time.time() - now_time
            clear_groups()

        # если персонаж умер, то запускаем анимацию смерти
        if not alive_or_not:
            if not animation_is_running:
                die_of_hero(player.rect.x, player.rect.y, 1)
                pygame.mixer.music.load('data/player_die.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(1)
            animation_is_running = True

        # если нет паузы и анимации смерти, то обновляем и рисуем всех спрайтов
        if not is_pause and not animation_is_running and not win_or_not:
            all_sprites_group.update()
            particles_group.update()
            all_sprites_group.draw(screen)
            pacman_group.update()
            player_group.draw(screen)
            enemies_group.draw(screen)
            pacman_group.draw(screen)
            particles_group.draw(screen)

        # если идет анимация смерти, то рисуем всех спрайтов и обновляем только частицы
        if animation_is_running:
            # это счет чик времени, чтобы анимация сразу не исчезла
            if animation_time >= 40:
                clear_groups()
                return
            screen.fill(BACKGROUND_GREY)
            particles_group.update()
            all_sprites_group.draw(screen)
            enemies_group.draw(screen)
            particles_group.draw(screen)

            animation_time += 1

        # если пауза рисуем меню паузы
        if is_pause:
            pause_menu(screen, 100, 100)

        if win_or_not:
            win_window(screen, 100, 100, finish_time - 10)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    first_level()
