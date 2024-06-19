import pygame, os, sys
from level import Level
from level_start import Level_start
from settings import SIZESCREEN, FPS, HEIGHT, WIDTH, WHITE, YELLOW, RED
from player import Player
from utils import load_images
from level_1 import Level_1
from boss_level import Boss_level
from boost_level import BoostLevel
from button import Button
from text import Text


def load_level(player, images, direction=None):
    """
    tworzy i zwraca nowy poziom gry na podstawie numeru poziomu

    args:
    player (Player): obiekt gracza
    images (dict): słownik zawierający załadowane obrazy
    direction (str, optional): kierunek wejściowy do poziomu, domyślnie None

    returns:
    Level: obiekt reprezentujący nowy poziom gry
    """
    Level.level_count += 1
    if Level.level_count == 1:
        return Level_start(player, images, direction)  # tworzy poziom startowy
    elif Level.level_count == 4:
        return BoostLevel(player, images, direction)  # tworzy poziom z boostami
    elif Level.level_count == 7:
        return Boss_level(player, images, direction)  # tworzy poziom z bossem
    else:
        return Level_1(player, images, direction)  # domyślnie tworzy poziom 1


class Game:
    """
    główna klasa gry, zarządza jej stanem i przebiegiem
    """
    def __init__(self):
        # inicjalizacja pygame i modułu mixer do obsługi dźwięku
        pygame.init()
        pygame.mixer.init()

        # ładowanie muzyki tła i odtwarzanie jej w pętli nieskończonej
        pygame.mixer.music.load('music/background3.mp3')
        pygame.mixer.music.play(loops=-1)

        # ładowanie dźwięków końca gry i wygranej
        self.end_sound = pygame.mixer.Sound('music/end.mp3')
        self.win_sound = pygame.mixer.Sound('music/win.mp3')

        # ustawienie ekranu gry i zegara do kontrolowania FPS
        self.screen = pygame.display.set_mode(SIZESCREEN)
        self.clock = pygame.time.Clock()

        # ładowanie obrazów gry i pobranie niektórych do zmiennych
        self.images = load_images(os.path.join(os.getcwd(), 'images'))
        self.background = self.images.pop('BACKGROUND')
        self.background_start = self.images.pop('BACKGROUND2')
        self.end = self.images.pop('END')
        self.win = self.images.pop('WIN')
        self.plot2 = self.images.pop('PLOT2')
        self.plot3 = self.images.pop('PLOT3')
        self.plot4 = self.images.pop('PLOT4')

        # inicjalizacja gracza na podstawie załadowanych obrazów animacji postaci i pocisku
        self.player = Player(683, 360, player_images={
            'front': [self.images[f'FRONT{i}'] for i in range(1, 5)],
            'back': [self.images[f'BACK{i}'] for i in range(1, 5)],
            'left': [self.images[f'LEFT{i}'] for i in range(1, 5)],
            'right': [self.images[f'RIGHT{i}'] for i in range(1, 5)]
        }, bullet_img=self.images['PLAYER_BULLET'])

        # początkowy poziom gry
        self.current_level = load_level(self.player, self.images)

        # obrazy ekranu startowego i ich pozycja
        self.start_image = self.images['TITLE']
        self.start_image_rect = self.start_image.get_rect(center=(WIDTH // 2, HEIGHT // 4))

        # tekst końca gry
        self.finish_text = Text("KONIEC GRY", WHITE, *self.screen.get_rect().center, font_size=120,
                                font_type="Times New Roman")

        # przyciski na ekranie startowym: start, quit, hard
        self.start_button = Button("START", YELLOW, RED, 200, 100, WIDTH // 4, 600, 70, "Arial")
        self.quit_button = Button("QUIT", YELLOW, RED, 200, 100, 3 * WIDTH // 4, 600, 70, "Arial")
        self.hard_button = Button("HARD", YELLOW, RED, 200, 100, WIDTH // 2, 600, 70, "Arial")

        # flagi kontrolujące stan gry
        self.window_open = True  # czy okno gry jest otwarte
        self.active_game = False  # czy gra jest aktywna (czy gracz gra)

    def handle_events(self):
        """
        obsługuje zdarzenia użytkownika, takie jak naciśnięcie klawiszy czy kliknięcie myszą
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_level.reset()  # resetuje bieżący poziom
                self.active_game = False  # kończy grę

            if event.type == pygame.QUIT:
                self.window_open = False  # zamyka okno gry

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click()  # obsługuje kliknięcie myszą

    def handle_mouse_click(self):
        """
        obsługuje kliknięcia myszą na przyciski na ekranie startowym
        """
        if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.display_plots()  # wyświetla sekwencję wstępną
            self.start_game(0)  # rozpoczyna grę od pierwszego poziomu

        elif self.quit_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.window_open = False  # zamyka okno gry
            pygame.time.delay(200)  # opóźnienie przed zamknięciem

        elif self.hard_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.display_plots()  # wyświetla sekwencję wstępną
            self.start_game(0)  # rozpoczyna grę od pierwszego poziomu

    def display_plots(self):
        """
        wyświetla sekwencję wstępną między poziomami
        """
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

    def start_game(self, level_count):
        """
        rozpoczyna grę od określonego poziomu

        args:
        level_count (int): numer poziomu, od którego zaczyna się gra
        """
        Level.level_count = level_count  # ustawia numer poziomu
        self.current_level = load_level(self.player, self.images)  # wczytuje nowy poziom
        self.player.reset_player()  # resetuje gracza do stanu początkowego
        self.active_game = True  # ustawia stan gry na aktywny

        pygame.time.delay(200)  # opóźnienie przed rozpoczęciem gry

    def draw_background(self):
        """
        rysuje tło gry
        """
        self.screen.blit(self.background, (0, 0))

    def draw_buttons(self):
        """
        rysuje przyciski na ekranie startowym
        """
        # zmiana koloru przycisków w zależności od położenia kursora myszy
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

        # rysowanie tła ekranu startowego i obrazka tytułowego
        self.screen.blit(self.background_start, (-100, -300))
        self.screen.blit(self.start_image, self.start_image_rect)

        # rysowanie przycisków
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        self.hard_button.draw(self.screen)

    def check_screen_edges(self):
        """
        sprawdza, czy gracz wychodzi poza granice ekranu i resetuje poziom w odpowiednim kierunku
        """
        if self.player.rect.bottom >= HEIGHT:
            self.player.rect.top = 0
            self.reset_level('down')  # resetuje poziom w dół
        elif self.player.rect.top <= 0:
            self.player.rect.bottom = HEIGHT
            self.reset_level('up')  # resetuje poziom w górę
        elif self.player.rect.right > WIDTH:
            self.player.rect.left = 0
            self.reset_level('right')  # resetuje poziom w prawo
        elif self.player.rect.left < 0:
            self.player.rect.right = WIDTH
            self.reset_level('left')  # resetuje poziom w lewo

    def reset_level(self, direction):
        """
        resetuje bieżący poziom gry w określonym kierunku

        args:
        direction (str): kierunek, w którym następuje resetowanie poziomu
        """
        self.current_level.reset()  # resetuje bieżący poziom
        self.current_level = load_level(self.player, self.images, direction)  # wczytuje nowy poziom w danym kierunku

    def update_game(self):
        """
        aktualizuje stan gry: gracza, poziomu oraz rysuje je na ekranie
        """
        self.player.update(pygame.key.get_pressed())  # aktualizuje gracza na podstawie wciśniętych klawiszy
        self.current_level.update()  # aktualizuje bieżący poziom gry
        self.current_level.draw(self.screen)  # rysuje bieżący poziom gry na ekranie
        self.player.draw(self.screen)  # rysuje gracza na ekranie

        # obsługa końca gry
        if self.player.lives == 1:
            self.end_sound.play(0)  # odtwarza dźwięk końca gry
            self.active_game = False  # kończy grę
            pygame.time.delay(1000)
            self.screen.blit(self.end, (0, 0))  # rysuje ekran końca gry
            self.finish_text.draw(self.screen)  # rysuje tekst "KONIEC GRY"
            pygame.display.update()
            pygame.time.delay(1000)

        # obsługa wygranej
        if Level.level_count == 8:
            self.win_sound.play(0)  # odtwarza dźwięk wygranej
            self.active_game = False  # kończy grę
            pygame.time.delay(500)
            self.screen.blit(self.win, (0, 0))  # rysuje ekran wygranej
            pygame.display.update()
            pygame.time.delay(1000)

    def run(self):
        """
        główna pętla gry, która obsługuje zdarzenia, aktualizuje stan gry i rysuje elementy na ekranie
        """
        while self.window_open:
            self.draw_background()  # rysuje tło gry
            self.handle_events()  # obsługuje zdarzenia użytkownika (klawiatura, mysz)

            if self.active_game:
                self.update_game()  # aktualizuje stan gry, jeśli gra jest aktywna
            else:
                self.draw_buttons()  # rysuje przyciski na ekranie startowym, jeśli gra nie jest aktywna

            self.check_screen_edges()  # sprawdza, czy gracz wychodzi poza ekran
            pygame.display.flip()  # odświeża ekran
            self.clock.tick(FPS)  # ustawia FPS

        pygame.time.delay(500)
        pygame.display.update()
        pygame.quit()  # zamyka Pygame
        sys.exit()  # kończy program
