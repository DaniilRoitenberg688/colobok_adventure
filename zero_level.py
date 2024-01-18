import pygame

from constants import *
from objects import *


def zero_level():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True

    clock = pygame.time.Clock()

    map = load_level('map0.txt')

    player = generate_level(map)

    camera = Camera(player.rect.x, player.rect.y)
    for object in all_sprites_group:
        camera.update(object)
    camera.update(player)

    is_pause = False

    while running:
        screen.fill(BACKGROUND_GREY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_pause = True
            if is_pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    y = event.pos[1]
                    if 100 < x < 500 and 100 < y < 500:
                        if 130 < x < 280 and 295 < y < 445:
                            is_pause = False
                            continue
                        if 325 < x < 625 and 295 < y < 445:
                            running = False
                            clear_groups()


            if not is_pause:
                player_group.update(event, map)
                camera.change(player.x * CELL_SIZE + 5.5, player.y * CELL_SIZE + 5.5)
                for object in all_sprites_group:
                    camera.update(object)

        all_sprites_group.update()
        all_sprites_group.draw(screen)
        player_group.draw(screen)
        if is_pause:
            pause_menu(screen, 100, 100)
        pygame.display.flip()
        clock.tick(FPS)






if __name__ == '__main__':
    zero_level()
