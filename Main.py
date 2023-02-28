import os
import pygame
import sys

FPS = 12

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
dragon_group = pygame.sprite.Group()
knight_group = pygame.sprite.Group()
bush_group = pygame.sprite.Group()


class Button(pygame.sprite.Sprite):

    def __init__(self, text, font_size, coord_x, coord_y, color):
        super().__init__()
        self.color = color
        self.text = text
        self.font_size = font_size
        font = pygame.font.Font('fonts/Vinque.ttf', self.font_size)
        self.string_rendered = font.render(self.text, 1, pygame.Color(color))
        intro_rect = self.string_rendered.get_rect()
        intro_rect.top = coord_x
        intro_rect.x = coord_y
        self.rect = intro_rect
        screen.blit(self.string_rendered, intro_rect)

    def button_mentioned(self, color):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if hit:
            font = pygame.font.Font('fonts/Vinque.ttf', self.font_size)
            self.string_rendered = font.render(self.text, 1, pygame.Color(color))
            screen.blit(self.string_rendered, self.rect)
        else:
            font = pygame.font.Font('fonts/Vinque.ttf', self.font_size)
            self.string_rendered = font.render(self.text, 1, pygame.Color(self.color))
            screen.blit(self.string_rendered, self.rect)

    def button_clicked(self):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)
        if hit:
            return True
        else:
            return False


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(pygame.sprite.Group())
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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
    rules_text = 'Правила игры'

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    name = Button(name_text, 50, 10, 100, 'gold')
    new_game = Button(new_game_text, 30, 150, 120, 'gold')
    see_results = Button(see_results_text, 30, 200, 50, 'gold')
    author = Button(author_text, 15, 480, 10, 'gold')
    rules = Button(rules_text, 30, 250, 155, 'gold')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game.button_clicked():
                    load_game()
                elif see_results.button_clicked():
                    results_page()
                elif rules.button_clicked():
                    rules_page()
        new_game.button_mentioned('white')
        see_results.button_mentioned('white')
        rules.button_mentioned('white')
        pygame.display.update()
        clock.tick(FPS)


def load_game():
    pass


def results_page():
    result_screen = pygame.Surface((width, height))
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    result_screen.blit(fon, (0, 0))
    screen.blit(result_screen, (0, 0))
    pygame.display.update()
    back_to_main_text = 'Назад'
    back_to_main = Button(back_to_main_text, 30, 10, 10, 'gold')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_main.button_clicked():
                    start_screen()
        back_to_main.button_mentioned('white')
        pygame.display.update()
        clock.tick(FPS)


def rules_page():
    rules_in_text = ['Вам предстоит играть за рыцаря.',
                     'Несмотря на то, что Вы рыцарь,',
                     'необходимо избегать кустов и драконов.',
                     'Чтобы спрятаться от дракона, нужно нажать down.',
                     'С кустами сложнее, они бывают трёх видов:',
                     'маленькие, средние и большие',
                     'Чтобы перепрыгнуть маленький или средний куст,',
                     ' нужно нажать up.',
                     'Чтобы перепрыгнуть большой куст,',
                     'нужно нажать up ДВА раза.',
                     'Удачи!',
                     'P.S. Принцессу спасать не нужно']
    result_screen = pygame.Surface((width, height))
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    result_screen.blit(fon, (0, 0))
    screen.blit(result_screen, (0, 0))
    pygame.display.update()
    back_to_main_text = 'Назад'
    back_to_main = Button(back_to_main_text, 30, 10, 10, 'gold')
    c_y = 10
    c_x = 50
    for text in rules_in_text:
        if rules_in_text.index(text) == 1 or rules_in_text.index(text) == 2:
            text = Button(text, 22, c_x, c_y, 'darkturquoise')
            c_x += 35
        else:
            text = Button(text, 20, c_x, c_y, 'white')
            c_x += 35
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_main.button_clicked():
                    start_screen()
        back_to_main.button_mentioned('white')
        pygame.display.update()
        clock.tick(FPS)


start_screen()