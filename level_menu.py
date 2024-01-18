import pygame

from zero_level import zero_level

from constants import WIDTH, HEIGHT, main_exit, GREY, BACKGROUND_GREY

def level_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True

    first_font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 70)
    second_font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', size=100)
    third_font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 40)

    text = first_font.render('LEVELS', True, GREY)
    text_zero = second_font.render('0', True, BACKGROUND_GREY)
    text_one = second_font.render('1', True, BACKGROUND_GREY)
    text_second = second_font.render('2', True, BACKGROUND_GREY)
    level_text = third_font.render('level', True, BACKGROUND_GREY)

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                main_exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 30 < x < 230 and 170 < y < 370:
                    zero_level()

        pygame.draw.rect(screen, GREY, (45, 170, 200, 200))
        screen.blit(level_text, (75, 180))
        screen.blit(text_zero, (110, 210))

        pygame.draw.rect(screen, GREY, (350, 170, 200, 200))
        screen.blit(level_text, (380, 180))
        screen.blit(text_one, (415, 210))

        pygame.draw.rect(screen, GREY, (45, 470, 200, 200))
        screen.blit(level_text, (75, 480))
        screen.blit(text_second, (110, 510))

        screen.blit(text, (140, 20))

        pygame.display.flip()


if __name__ == '__main__':
    level_menu()