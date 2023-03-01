import os
import pygame
import sys
import math
import random
import pandas as pd
import datetime

FPS = 12

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Knight")
clock = pygame.time.Clock()
dragon_group = pygame.sprite.Group()
knight_group = pygame.sprite.Group()
game_speed = 20
global obstacles, points
obstacles = []
points = 0


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


class Obstacle:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = width
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, scr):
        scr.blit(self.image, self.rect)


class SmallBush(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 375


class LargeBush(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 375


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def jumping(knight, time):
    if time > 5:
        velocity = time * 2
        knight.rect.top -= velocity
    elif time <= 5:
        velocity = time * 2
        knight.rect.top += velocity


def dragon_move(dragon, dragon_timer):
    velocity = 1
    dragon.rect.x -= dragon_timer * velocity


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global obstacles
    obstacles = []
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
    base_font = pygame.font.Font('fonts/Vinque.ttf', 32)
    background = load_image('background.png')
    screen.blit(background, (0, 0))
    pygame.display.update()
    back_to_main_text = 'Назад'
    back_to_main = Button(back_to_main_text, 30, 10, 10, 'gold')
    title = Button('Введите имя и нажмите Tab', 30, 125, 55, 'gold')
    input_rect = pygame.Rect(190, 200, 100, 50)
    active = False
    user_text = ''
    color_active = pygame.Color('white')
    color_passive = pygame.Color('gold')
    color = color_passive
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_main.button_clicked():
                    start_screen()
                elif input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_TAB:
                    new_game_page(user_text)
                else:
                    user_text += event.unicode
        back_to_main.button_mentioned('white')
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.update()
        clock.tick(FPS)


def results_page():
    result_screen = pygame.Surface((width, height))
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    result_screen.blit(fon, (0, 0))
    screen.blit(result_screen, (0, 0))
    pygame.display.update()
    back_to_main_text = 'Назад'
    back_to_main = Button(back_to_main_text, 30, 10, 10, 'gold')
    players = pd.read_csv('users_scores.csv')
    players.sort_values(by=['score'])
    num = players.shape[0]
    result_list = []
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
                     'Чтобы спрятаться от дракона, нажмите down.',
                     'С кустами сложнее, они бывают двух видов:',
                     'маленькие и большие',
                     'Чтобы перепрыгнуть  куст, нужно нажать up.',
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
            c_x += 52
        else:
            text = Button(text, 21, c_x, c_y, 'yellow')
            c_x += 52
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


def new_game_page(text):
    background = load_image('background.png')
    background = pygame.transform.scale(background, (width, height))
    screen.blit(background, (0, 0))
    pygame.display.update()
    back_to_main_text = 'Назад'
    back_to_main = Button(back_to_main_text, 30, 10, 10, 'gold')
    title = Button('Нажмите пробел чтобы начать', 30, 125, 35, 'gold')
    knight = AnimatedSprite(load_image("idle.png"), 5, 1, 10, 350)
    knight_group.add(knight)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_main.button_clicked():
                    start_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    knight_group.remove(knight)
                    start_game(text)
        background = load_image('background.png')
        screen.blit(background, (0, 0))
        back_to_main.button_mentioned('white')
        title.button_mentioned('gold')
        knight_group.update()
        screen.blit(screen, (0, 0))
        knight_group.draw(screen)
        pygame.display.update()
        clock.tick(5)


def start_game(text):
    global obstacles, points
    obstacles = []
    background = load_image('background.png')
    bg_width = background.get_width()
    bg_rect = background.get_rect()
    tiles = math.ceil(width / bg_width) + 1
    screen.blit(background, (0, 0))
    pygame.display.update()
    text = text
    scroll = 0
    points = 0
    jump_timer = 0
    gallop_timer = 0
    dragon_timer = 50

    back_to_main_text = 'Назад'
    back_to_main = Button(back_to_main_text, 30, 10, 10, 'gold')

    knight_walking = AnimatedSprite(load_image('walk.png'), 8, 1, 10, 350)
    knight_gallop = AnimatedSprite(load_image('gallop.png'), 5, 1, 10, 350)
    knight_jump = AnimatedSprite(load_image('jump.png'), 13, 1, 10, 350)
    knight_jump.mask = pygame.mask.from_surface(knight_jump.image)
    knight_gallop.mask = pygame.mask.from_surface(knight_gallop.image)
    knight_walking.mask = pygame.mask.from_surface(knight_walking.image)
    knight_group.add(knight_walking)

    dragon = AnimatedSprite(load_image('reddragonfly3.png'), 4, 4, 500, 266)
    dragon_group.add(dragon)
    dragon_flag = False

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        score_text = Button(str(points), 30, 10, 350, 'gold')
        score_text.button_mentioned('gold')

    while True:
        for i in range(0, tiles):
            screen.blit(background, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll
        scroll -= 15
        if abs(scroll) > bg_width:
            scroll = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_main.button_clicked():
                    start_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    knight_group.remove(knight_walking)
                    knight_group.add(knight_jump)
                    jump_timer = 10
                elif event.key == pygame.K_DOWN:
                    knight_group.remove(knight_walking)
                    knight_group.add(knight_gallop)
                    gallop_timer = 10
        if len(obstacles) == 0:
            if random.randint(0, 3) == 0:
                obstacles.append(SmallBush(load_image('bush_1.png')))
            elif random.randint(0, 3) == 1:
                obstacles.append(LargeBush(load_image('bush_2.png')))
            else:
                if dragon_flag is True:
                    pass
                else:
                    dragon_flag = True
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if pygame.sprite.collide_mask(knight_group.sprites()[0], obstacle) is not None:
                knight_group.remove(knight_walking)
                knight_group.remove(knight_jump)
                knight_group.remove(knight_gallop)
                dragon_group.remove(dragon)
                end_game(points, text)
        score()
        background = load_image('background.png')
        back_to_main.button_mentioned('white')
        screen.blit(screen, (0, 0))
        if dragon_flag is True:
            dragon_group.update()
            dragon_group.draw(screen)
            if pygame.sprite.collide_mask(knight_group.sprites()[0], dragon_group.sprites()[0]) is not None:
                knight_group.remove(knight_walking)
                knight_group.remove(knight_jump)
                knight_group.remove(knight_gallop)
                dragon_group.remove(dragon)
                end_game(points, text)
            if dragon_timer > 0:
                dragon_move(dragon, dragon_timer)
                dragon_timer -= 1
            else:
                dragon_flag = False
                dragon.rect.x = width
                dragon_timer = 50
        knight_group.update()
        knight_group.draw(screen)
        if jump_timer > 0:
            jumping(knight_jump, jump_timer)
            jump_timer -= 1
            if jump_timer == 0:
                knight_group.remove(knight_jump)
                knight_group.add(knight_walking)
                knight_jump.rect.top = 350
        if gallop_timer > 0:
            gallop_timer -= 1
            if gallop_timer == 0:
                knight_group.remove(knight_gallop)
                knight_group.add(knight_walking)
        pygame.display.update()
        clock.tick(8)


def end_game(points, text):
    background = load_image('background.png')
    screen.blit(background, (0, 0))
    pygame.display.update()
    back_to_main_text = 'В главное меню'
    restart_text = 'Начать заново'
    game_over_text = 'Game Over!'
    results_text = text + ', ' + str(points)
    game_over = Button(game_over_text, 40, 30, 145, 'gold')
    back_to_main = Button(back_to_main_text, 30, 250, 140, 'gold')
    restart = Button(restart_text, 30, 290, 145, 'gold')
    results = Button(results_text, 30, 125, 190, 'gold')
    add_name_and_score(text, points)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_to_main.button_clicked():
                    start_screen()
                if restart.button_clicked():
                    new_game_page(text)
        back_to_main.button_mentioned('white')
        restart.button_mentioned('white')
        pygame.display.update()
        clock.tick(FPS)


def add_name_and_score(name, points):
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%d:%m:%Y_%H:%M')
    if name == '':
        name = 'the_one_without_name'
    old = pd.read_csv('users_scores.csv')
    new = pd.DataFrame({'name': [name], 'score': [str(points)], 'data_time': [dt_now]})
    pd.concat([old, new], ignore_index=True).to_csv('users_scores.csv', index=False)


start_screen()