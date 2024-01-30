import pygame

from constants import WIDTH, HEIGHT, GREY, BACKGROUND_GREY
from first_level import first_level
from second_level import second_level
from zero_level import zero_level


def level_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True

    first_font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 70)
    second_font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 100)
    third_font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 40)
    exit_font = pygame.font.Font('data/minecraft-ten-font-cyrillic.ttf', 50)

    text = first_font.render('LEVELS', True, GREY)
    text_zero = second_font.render('0', True, BACKGROUND_GREY)
    text_one = second_font.render('1', True, BACKGROUND_GREY)
    text_second = second_font.render('2', True, BACKGROUND_GREY)
    level_text = third_font.render('level', True, BACKGROUND_GREY)
    exit_text = exit_font.render("EXIT", True, BACKGROUND_GREY)

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                if 45 < x < 245 and 170 < y < 370:
                    zero_level()
                if 350 < x < 550 and 17 < y < 370:
                    first_level()

                if 45 < x < 245 and 470 < y < 670:
                    second_level()

                if 350 < x < 550 and 470 < y < 670:
                    running = False

        pygame.draw.rect(screen, GREY, (45, 170, 200, 200))
        screen.blit(level_text, (75, 180))
        screen.blit(text_zero, (110, 210))

        pygame.draw.rect(screen, GREY, (350, 170, 200, 200))
        screen.blit(level_text, (380, 180))
        screen.blit(text_one, (415, 210))

        pygame.draw.rect(screen, GREY, (45, 470, 200, 200))
        screen.blit(level_text, (75, 480))
        screen.blit(text_second, (110, 510))

        pygame.draw.rect(screen, GREY, (350, 470, 200, 200))
        screen.blit(exit_text, (383, 520))

        screen.blit(text, (140, 20))

        pygame.display.flip()

    pygame.mixer.music.stop()


if __name__ == '__main__':
    level_menu()
