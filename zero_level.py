import pygame


from constants import *

from objects import *

from groups import *

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


    while running:
        screen.fill(GREY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            player_group.update(event, map)
            camera.change(player.x * CELL_SIZE + 5.5, player.y * CELL_SIZE + 5.5)
            for object in all_sprites_group:
                camera.update(object)

        all_sprites_group.update()
        all_sprites_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    zero_level()

