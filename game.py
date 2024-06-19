import pygame, os, sys

from level import Level
from level_start import Level_start
from settings import SIZESCREEN, FPS, HEIGHT, WIDTH, WHITE, YELLOW, RED
from player import Player
from utils import load_images
from level_1 import Level_1
from boss_level import Boss_level
from boost_level import Boost_level
from button import Button
from text import Text


def load_level(player, images, direction=None):
    Level.level_count += 1
    if Level.level_count == 1:
        return Level_start(player, images, direction)
    elif Level.level_count == 4:
        return Boost_level(player, images, direction)
    elif Level.level_count == 7:
        return Boss_level(player, images, direction)
    else:
        return Level_1(player, images, direction)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('music/background3.mp3')
        pygame.mixer.music.play(loops=-1)
        self.end_sound = pygame.mixer.Sound('music/end.mp3')
        self.win_sound = pygame.mixer.Sound('music/win.mp3')

        self.screen = pygame.display.set_mode(SIZESCREEN)
        self.clock = pygame.time.Clock()
        self.images = self.load_images()
        self.background = self.images.pop('BACKGROUND')
        self.background_start = self.images.pop('BACKGROUND2')
        self.end = self.images.pop('END')
        self.win = self.images.pop('WIN')
        self.plot2 = self.images.pop('PLOT2')
        self.plot3 = self.images.pop('PLOT3')
        self.plot4 = self.images.pop('PLOT4')

        self.player = Player(683, 360, player_images={
            'front': [self.images[f'FRONT{i}'] for i in range(1, 5)],
            'back': [self.images[f'BACK{i}'] for i in range(1, 5)],
            'left': [self.images[f'LEFT{i}'] for i in range(1, 5)],
            'right': [self.images[f'RIGHT{i}'] for i in range(1, 5)]
        }, bullet_img=self.images['PLAYER_BULLET'])

        self.current_level = load_level(self.player, self.images)
        self.start_image = self.images['TITLE']
        self.start_image_rect = self.start_image.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        self.finish_text = Text("KONIEC GRY", WHITE, *self.screen.get_rect().center, font_size=120,
                                font_type="Times New Roman")
        self.start_button = Button("START", YELLOW, RED, 200, 100, WIDTH // 4, 600, 70, "Arial")
        self.quit_button = Button("QUIT", YELLOW, RED, 200, 100, 3 * WIDTH // 4, 600, 70, "Arial")
        self.hard_button = Button("HARD", YELLOW, RED, 200, 100, WIDTH // 2, 600, 70, "Arial")

        self.window_open = True
        self.active_game = False

    def load_images(self):
        path = os.path.join(os.getcwd(), 'images')
        return load_images(path)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_level.reset()
                self.active_game = False

            if event.type == pygame.QUIT:
                self.window_open = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)

    def handle_mouse_click(self, event):
        if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.display_plots()
            self.start_game(0)

        elif self.quit_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.window_open = False
            pygame.time.delay(200)

        elif self.hard_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.display_plots()
            self.start_game(0, 2)

    def display_plots(self):
        pygame.time.delay(500)
        self.screen.blit(self.plot2, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)
        self.screen.blit(self.plot3, (3, 3))
        pygame.display.update()
        pygame.time.delay(3000)
        self.screen.blit(self.plot4, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)

    def start_game(self, level_count, player_lives=3):
        Level.level_count = level_count
        self.current_level = load_level(self.player, self.images)
        self.player.reset_player()
        self.active_game = True
        self.player.lives = player_lives
        pygame.time.delay(200)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_buttons(self):
        if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.start_button.background_color = YELLOW
            self.start_button.text.text_color = RED
        else:
            self.start_button.background_color = RED
            self.start_button.text.text_color = YELLOW
        if self.quit_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.quit_button.background_color = YELLOW
            self.quit_button.text.text_color = RED
        else:
            self.quit_button.background_color = RED
            self.quit_button.text.text_color = YELLOW
        if self.hard_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.hard_button.background_color = YELLOW
            self.hard_button.text.text_color = RED
        else:
            self.hard_button.background_color = RED
            self.hard_button.text.text_color = YELLOW

        self.screen.blit(self.background_start, (-100, -300))
        self.screen.blit(self.start_image, self.start_image_rect)
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.hard_button.draw(self.screen)

    def check_screen_edges(self):
        if self.player.rect.bottom >= HEIGHT:
            self.player.rect.top = 0
            self.reset_level('down')
        elif self.player.rect.top <= 0:
            self.player.rect.bottom = HEIGHT
            self.reset_level('up')
        elif self.player.rect.right > WIDTH:
            self.player.rect.left = 0
            self.reset_level('right')
        elif self.player.rect.left < 0:
            self.player.rect.right = WIDTH
            self.reset_level('left')

    def reset_level(self, direction):
        self.current_level.reset()
        self.current_level = load_level(self.player, self.images, direction)

    def update_game(self):
        self.player.update(pygame.key.get_pressed())
        self.current_level.update()
        self.current_level.draw(self.screen)
        self.player.draw(self.screen)
        if self.player.lives == 1:
            self.end_sound.play(0)
            self.active_game = False
            pygame.time.delay(1000)
            self.screen.blit(self.end, (0, 0))
            self.finish_text.draw(self.screen)
            pygame.display.update()
            pygame.time.delay(1000)
        if Level.level_count == 8:
            self.win_sound.play(0)
            self.active_game = False
            pygame.time.delay(500)
            self.screen.blit(self.win, (0, 0))
            pygame.display.update()
            pygame.time.delay(1000)

    def run(self):
        while self.window_open:
            self.draw_background()
            self.handle_events()

            if self.active_game:
                self.update_game()
            else:
                self.draw_buttons()

            self.check_screen_edges()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.time.delay(500)
        pygame.display.update()
        pygame.quit()
        sys.exit()
