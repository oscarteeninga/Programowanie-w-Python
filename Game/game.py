"""
U gory jest bramka przeciwnika, na dole "nasza"

wrzucić to w pisaniu tekstu w statystykach

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)

textsurface = myfont.render('Some Text', False, (0, 0, 0))

screen.blit(textsurface,(0,0))
"""

import pygame
import sys
import pygameMenu
import time
from pygameMenu.locals import *
from enum import Enum
import math

# screen resolution - must be even
H_SIZE = 800
W_SIZE = 1100
SCREEN_SIZE = 800

# colours
LIGHT_GRAY = (240, 240, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 64, 0)


class Opponent(Enum):
    CPU = 1
    HUMAN = 2


class CPULevel(Enum):
    EASY = 1
    MEDIUM = 2


class Turn(Enum):
    PLAYER1 = 1
    PLAYER2 = 2


def menu_background():
    pass


# class, which holds statistics about current game
# and also shows statistics on screen
class Statistics(object):
    # type of opponent # level of CPU
    def __init__(self, player2, cpu_level, player1_color, player2_color):
        # beginning of game
        self.timer_start = time.time()
        # actual time
        self.timer_actual = time.time()

        # players moves
        self.player1_moves = 0
        self.player2_moves = 0

        # opponent
        self.player2 = player2
        self.cpu_level = cpu_level

        # whos turn
        self.turn = Turn.PLAYER1

        # plauer colors
        self.player1_color = player1_color
        self.player2_color = player2_color

    def player1_add_move(self):
        self.player1_moves += 1

    def player2_add_move(self):
        self.player2_moves += 1

    def draw_statistics(self, surface):

        self.timer_actual = time.time()
        game_time = (self.timer_actual - self.timer_start) % 1

        minutes = game_time / 60
        seconds = game_time % 60

        # drawing timer
        pygame.draw.rect(surface, BLACK, (860, 380, 100, 40), 2)

        # drawing your move
        if self.turn == Turn.PLAYER1:
            pygame.draw.rect(surface, self.player1_color, (780, 570, 260, 40), 3)



        else:
            pygame.draw.rect(surface, self.player2_color, (780, 330, 260, 40), 3)

        # drawing statistics for player 2 (up)
        pygame.draw.rect(surface, self.player2_color, (780, 30, 260, 120), 4)

        if self.player2 == Opponent.CPU:
            pass

        # drawing statistics for player 1 (down)
        pygame.draw.rect(surface, self.player1_color, (780, 650, 260, 120), 4)


# game object
def translate_position(x):
    if x < 80:
        return 0
    if x > 640:
        return 640
    return x - 80


class Game(object):

    def __init__(self):
        pygame.init()

        # resolution
        self.res = (W_SIZE, H_SIZE)

        # screen initialisation
        self.surface = pygame.display.set_mode(self.res)
        # game title
        pygame.display.set_caption('Paperball 2020')

        # game clock
        self.clock = pygame.time.Clock()

        self.margin = SCREEN_SIZE / 10

        self.board_size = 8 * SCREEN_SIZE / 10

        # Szerokość obramowania - musi być nieparzysta
        self.board_border_width = 3

        # Ilość wierszy/kolumny - musi być parzysta
        self.board_rows = 10

        self.row_size = self.board_size / self.board_rows

        # Szerokość bramki
        self.goal_width = 2 * self.row_size

        # Wielkość piłki
        self.ball_size = 7

        self.game_board = pygame.Surface((self.board_size, self.board_size))

        # help menu
        self.help_menu = pygameMenu.TextMenu(
            self.surface,
            font=pygameMenu.fonts.FONT_NEVIS,
            title='Help',
            title_offsety=5,
            window_height=H_SIZE,
            window_width=W_SIZE,
            menu_height=H_SIZE,
            menu_width=W_SIZE,
            dopause=True,
            menu_color=WHITE,
            menu_color_title=WHITE,
            font_color=BLACK,
            title_offsetx=510,
            bgfun=menu_background,
            text_color=BLACK,
            text_fontsize=30)

        with open('help.txt') as f:
            lines = f.readlines()
            for line in lines:
                self.help_menu.add_line(line)

        self.help_menu.add_option('Return to menu', PYGAME_MENU_BACK)

        # options menu
        self.options_menu = pygameMenu.Menu(self.surface,
                                            font=pygameMenu.fonts.FONT_NEVIS,
                                            title='Options',
                                            title_offsety=5,
                                            window_height=H_SIZE,
                                            window_width=W_SIZE,
                                            menu_height=H_SIZE,
                                            menu_width=W_SIZE,
                                            dopause=True,
                                            menu_color=WHITE,
                                            menu_color_title=WHITE,
                                            font_color=BLACK,
                                            title_offsetx=450,
                                            bgfun=menu_background,
                                            )

        self.options_menu.add_selector("Opponent", [("Human", "h"), ("CPU", "c")],
                                       onchange=self.change_opponent,
                                       onreturn=self.change_opponent)
        self.options_menu.add_selector("CPU Level", [("Easy", "EASY"), ("Medium", "MEDIUM")],
                                       onchange=self.change_cpu_level,
                                       onreturn=self.change_cpu_level)
        self.options_menu.add_selector("Player1 Color",
                                       [("Red", RED), ("Blue", BLUE), ("Green", GREEN),
                                        ("Yellow", YELLOW), ("Orange", ORANGE)],
                                       onchange=self.change_player1_color,
                                       onreturn=self.change_player1_color
                                       )
        self.options_menu.add_selector("Player2 Color",
                                       [("Blue", BLUE), ("Red", RED), ("Green", GREEN),
                                        ("Yellow", YELLOW), ("Orange", ORANGE)],
                                       onchange=self.change_player2_color,
                                       onreturn=self.change_player2_color
                                       )
        self.options_menu.add_selector("Music", [("ON", True), ("OFF", False)],
                                       onchange=self.toogle_music,
                                       onreturn=self.toogle_music
                                       )
        self.options_menu.add_selector("Music Volume",
                                       [("5", 1), ("4", 0.8), ("3", 0.6), ("2", 0.4), ("1", 0.2),
                                        ("0", 0)], onchange=self.change_volume,
                                       onreturn=self.change_volume)
        self.options_menu.add_option('Return to menu', PYGAME_MENU_BACK)

        # controls menu
        self.control_menu = pygameMenu.TextMenu(
            self.surface,
            font=pygameMenu.fonts.FONT_NEVIS,
            title='Controls',
            title_offsety=5,
            window_height=H_SIZE,
            window_width=W_SIZE,
            menu_height=H_SIZE,
            menu_width=W_SIZE,
            dopause=True,
            menu_color=WHITE,
            menu_color_title=WHITE,
            font_color=BLACK,
            title_offsetx=455,
            bgfun=menu_background,
            text_color=BLACK,
            text_fontsize=30)

        with open('controls.txt') as f:
            lines = f.readlines()
            for line in lines:
                self.control_menu.add_line(line)

        self.control_menu.add_option('Return to menu', PYGAME_MENU_BACK)

        # game main menu
        self.main_menu = pygameMenu.Menu(
            self.surface,
            font=pygameMenu.fonts.FONT_8BIT,
            title='Paper Ball',
            title_offsety=5,
            window_height=H_SIZE,
            window_width=W_SIZE,
            menu_height=H_SIZE,
            menu_width=W_SIZE,
            dopause=True,
            menu_color=WHITE,
            menu_color_title=WHITE,
            font_color=BLACK,
            title_offsetx=310,
            bgfun=menu_background)

        self.main_menu.add_option("Play prototype", self.game)
        self.main_menu.add_option("Options", self.options_menu)
        self.main_menu.add_option("Controls", self.control_menu)
        self.main_menu.add_option("Help", self.help_menu)
        self.main_menu.add_option('Exit', PYGAME_MENU_EXIT)

        # by default play with human
        self.opponent = Opponent.HUMAN
        # with easy level
        self.difficulty = CPULevel.EASY

        # player colours
        self.player1_colour = RED
        self.player2_colour = BLUE

        # music mode
        self.music = True
        self.volume = 1.0
        pygame.mixer_music.load("music.mp3")
        pygame.mixer_music.play(loops=-1, start=0.0)

        """
            here should be things like:
            * moves, time of actual game etc 
            *some map of football field
            *Maybe some class which holds everything about actual game?
            ...
        """

    def run(self):

        while True:
            self.clock.tick(15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.main_menu.enable()

            self.main_menu.mainloop(pygame.event.get())

            pygame.display.flip()

    def gen_board(self):
        self.surface.fill(WHITE)
        self.game_board.fill(WHITE)

        for i in range(0, self.board_rows + 1, 1):
            pygame.draw.line(self.game_board, LIGHT_GRAY, (0, i * self.row_size), (self.board_size, i * self.row_size),
                             1)
            pygame.draw.line(self.game_board, LIGHT_GRAY, (i * self.row_size, 0), (i * self.row_size, self.board_size),
                             1)
            pygame.draw.line(self.game_board, LIGHT_GRAY, (i * self.row_size, 0),
                             (self.board_size, self.board_size - i * self.row_size), 1)
            pygame.draw.line(self.game_board, LIGHT_GRAY, (0, i * self.row_size),
                             (self.board_size - i * self.row_size, self.board_size), 1)
            pygame.draw.line(self.game_board, LIGHT_GRAY, (self.board_size - i * self.row_size, 0),
                             (0, self.board_size - i * self.row_size), 1)
            pygame.draw.line(self.game_board, LIGHT_GRAY, (self.board_size, self.board_size - i * self.row_size),
                             (self.board_size - i * self.row_size, self.board_size), 1)

        pygame.draw.rect(self.game_board, BLACK, (0, 0, self.board_size, self.board_size), self.board_border_width)
        pygame.draw.line(self.game_board, RED, ((self.board_size - self.goal_width) / 2, 0),
                         ((self.board_size + self.goal_width) / 2, 0), self.board_border_width)
        pygame.draw.line(self.game_board, RED, ((self.board_size - self.goal_width) / 2, self.board_size - 1),
                         ((self.board_size + self.goal_width) / 2, self.board_size - 1), self.board_border_width)

    def game(self):

        self.gen_board()
        statistics = Statistics(self.opponent, self.difficulty, self.player1_colour, self.player2_colour)
        self.surface.blit(self.game_board, (self.margin, self.margin))

        # Obsługa rysowania kresek i koła
        (x, y) = (int(self.board_size / 2), int(self.board_size / 2))
        # (x_old, u_old) = (x, y)
        (x_dir, y_dir) = (0, 0)

        # clicked = False

        while True:
            pygame.time.delay(10)
            # if clicked:
            #     clicked = False
            #     pygame.time.delay(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.toogle_music(True)
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.toogle_music(not self.music)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.increase_volume()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    self.decrease_volume()

                if pygame.mouse.get_pressed() == (1, 0, 0):
                    # (x_old, u_old) = (x, y)
                    (x, y) = (x + x_dir * self.row_size, y + y_dir * self.row_size)
                    self.gen_board()
                    self.surface.blit(self.game_board, (self.margin, self.margin))
                    # clicked = True
            (x_n, y_n) = pygame.mouse.get_pos()

            x_n = translate_position(x_n)
            y_n = translate_position(y_n)
            if (x_n, y_n) == (x, y):
                continue
            else:
                if x_n - x != 0 and y_n - y != 0:
                    x_dir = (x_n - x) / abs(x_n - x)
                    y_dir = (y_n - y) / abs(y_n - y)
                    if abs((x_n - x) / (y_n - y)) > 2:
                        y_dir = 0
                    if abs((x_n - x) / (y_n - y)) < 1 / 2:
                        x_dir = 0
                # print(x_dir, y_dir)  #o ile ma sie poruszyc
                # print(x_n,y_n)       #pozycja kursora
                self.gen_board()
                pygame.draw.circle(self.game_board, RED, (int(x), int(y)), self.ball_size, 0)
                pygame.draw.line(self.game_board, GREEN, (x, y), (x + x_dir * self.row_size, y + y_dir * self.row_size),
                                 self.board_border_width)
                self.surface.blit(self.game_board, (self.margin, self.margin))
            statistics.draw_statistics(self.surface)
            pygame.display.update()

    # changes opponent type
    def change_opponent(self, c):
        if c == "h":
            self.opponent = Opponent.HUMAN
        else:
            self.opponent = Opponent.CPU

    # changes cpu level
    def change_cpu_level(self, c):
        if c == "EASY":
            self.difficulty = CPULevel.EASY

        elif c == "MEDIUM":
            self.difficulty = CPULevel.MEDIUM

    def change_player1_color(self, c):
        if c == GREEN:
            self.player1_colour = GREEN
        elif c == RED:
            self.player1_colour = RED

        elif c == BLUE:
            self.player1_colour = BLUE

        elif c == YELLOW:
            self.player1_colour = YELLOW

        elif c == ORANGE:
            self.player1_colour = ORANGE

    def change_player2_color(self, c):
        if c == GREEN:
            self.player2_colour = GREEN
        elif c == RED:
            self.player2_colour = RED

        elif c == BLUE:
            self.player2_colour = BLUE

        elif c == YELLOW:
            self.player2_colour = YELLOW

        elif c == ORANGE:
            self.player2_colour = ORANGE

    def toogle_music(self, c):
        if c:
            if self.music is False:
                self.music = True
                pygame.mixer_music.unpause()
        else:
            if self.music is True:
                self.music = False
                pygame.mixer_music.pause()

    def change_volume(self, c):
        pygame.mixer_music.set_volume(c)
        self.volume = c

    def decrease_volume(self):
        if self.volume > 0.0:
            self.volume -= 0.2
        pygame.mixer_music.set_volume(self.volume)

    def increase_volume(self):
        if self.volume < 1.0:
            self.volume += 0.2
        pygame.mixer_music.set_volume(self.volume)


def main():
    paperball = Game()
    paperball.run()


if __name__ == '__main__':
    main()
