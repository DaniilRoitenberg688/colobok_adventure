import time

from constants import *
from functions import load_level, clear_groups, pause_menu, win_window, draw_pacman_hp
from game_objects import generate_level, die_of_hero
from groups import *


def second_level():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    map = load_level('map2.txt')

    player, pacman = generate_level(map)

    alive = True
    die_animation_is_running = False

    clock = pygame.time.Clock()

    animation_time = 0

    running = True

    for object in all_sprites_group:
        object.rect.x -= 50
        object.rect.y += 150
    player.rect.x -= 50
    player.rect.y += 150

    is_pause = False

    win_or_not = False

    pacman_die_animation = False

    start_time = time.time()

    while running:
        screen.fill(BACKGROUND_GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clear_groups()
                running = False
            if alive and not is_pause and not win_or_not:
                player_group.update(event, map, True)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_pause = True

            if win_or_not:
                if event.type == pygame.KEYDOWN:
                    running = False

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

        if pacman.hp == 0 and not pacman_die_animation and not win_or_not:
            pygame.mixer.music.load('data/pacman_die.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(0)
            die_of_hero(pacman.rect.x, pacman.rect.y, 0)
            pacman.kill()
            pacman_die_animation = True
            end_time = time.time()

        if pygame.sprite.spritecollideany(player, enemies_group):
            alive = False

        if not alive and not die_animation_is_running:
            pygame.mixer.music.load('data/player_die.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(0)
            die_animation_is_running = True
            die_of_hero(player.rect.x, player.rect.y, 1)
            player.kill()

        if alive and not is_pause and not win_or_not and not pacman_die_animation:
            all_sprites_group.update()
            enemies_group.update()
            all_sprites_group.draw(screen)
            player_group.draw(screen)
            enemies_group.draw(screen)
            draw_pacman_hp(screen, pacman.hp)

        if die_animation_is_running:
            if animation_time == 40:
                clear_groups()
                running = False
            particles_group.update()
            all_sprites_group.draw(screen)
            player_group.draw(screen)
            enemies_group.draw(screen)
            particles_group.draw(screen)
            draw_pacman_hp(screen, pacman.hp)
            animation_time += 1

        if pacman_die_animation and not win_or_not:
            if animation_time == 80:
                clear_groups()
                pygame.mixer.music.load('data/si.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(1)
                win_or_not = True
                pacman_die_animation = False
            particles_group.update()
            all_sprites_group.draw(screen)
            player_group.draw(screen)
            enemies_group.draw(screen)
            particles_group.draw(screen)
            draw_pacman_hp(screen, pacman.hp)
            animation_time += 1

        if is_pause:
            pause_menu(screen, 100, 100)

        if win_or_not:
            clear_groups()
            win_window(screen, 100, 100, end_time - start_time - 20)

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    second_level()
