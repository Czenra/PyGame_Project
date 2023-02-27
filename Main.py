import os
import pygame
import sys

FPS = 50

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    name_text = 'Flappy Knight'
    new_game_text = 'Начать новую игру'
    see_results_text = 'Посмотреть лучшие результаты'
    author_text = 'by Alex Rybka, 2023'

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('fonts/Vinque.ttf', 50)
    string_rendered = font.render(name_text, 1, pygame.Color('gold'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 10
    intro_rect.x = 100
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font('fonts/Vinque.ttf', 30)
    string_rendered = font.render(new_game_text, 1, pygame.Color('gold'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 150
    intro_rect.x = 120
    screen.blit(string_rendered, intro_rect)
    string_rendered = font.render(see_results_text, 1, pygame.Color('gold'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 200
    intro_rect.x = 50
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font('fonts/Vinque.ttf', 15)
    string_rendered = font.render(author_text, 1, pygame.Color('gold'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 480
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def load_game(game):
    pass


start_screen()