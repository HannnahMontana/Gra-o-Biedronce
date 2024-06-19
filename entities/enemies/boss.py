import pygame

from effects.animation import Animation
from entities.behaviors.path_follower import PathFollower
from entities.enemies.shooting_enemy import ShootingEnemy
from settings import GRID_SIZE


class Boss(ShootingEnemy):
    """
    klasa reprezentująca bossa w grze.

    attributes:
    target_index (int or None): indeks celu (nie używany w aktualnej implementacji).
    lives (int): aktualna ilość życia bossa.
    max_lives (int): maksymalna ilość życia bossa.
    path (list): ścieżka bossa (nie używana w aktualnej implementacji).
    shooting_distance (int): zasięg strzału bossa.
    animation_walking (Animation): animacja chodzenia bossa.
    animation_hands (Animation): animacja ruchu rąk bossa.
    current_animation (Animation): aktualnie odtwarzana animacja bossa.
    last_animation_change_time (int): czas ostatniej zmiany animacji bossa.
    animation_change_interval (int): interwał zmiany animacji bossa.
    """

    def __init__(self, enemy_images, bullet_img, cx, cy, speed):
        """
        inicjalizuje obiekt bossa.

        args:
        enemy_images (list): lista obrazków bossa.
        bullet_img (pygame.Surface): obrazek pocisku bossa.
        cx (int): współrzędna x pozycji startowej bossa na ekranie.
        cy (int): współrzędna y pozycji startowej bossa na ekranie.
        speed (int): prędkość poruszania się bossa.
        """


        # inicjalizacja klasy nadrzędnej ShootingEnemy
        ShootingEnemy.__init__(self, enemy_images[0], bullet_img, cx, cy, speed,
                               lives=10, shoot_delay=1000, bullet_speed=5,
                               bullet_lifetime=1000, shooting_distance=500)

        # inicjalizacja atrybutów specyficznych dla bossa
        self.target_index = None
        self.lives = 20
        self.max_lives = 20
        self.path = []
        self.shooting_distance = 400

        # inicjalizacja animacji bossa
        self.animation_walking = Animation(enemy_images[:-2], delay=110)  # animacja chodzenia
        self.animation_hands = Animation(enemy_images[-2:], delay=150)  # animacja ruchu rąk
        self.current_animation = self.animation_walking  # startujemy od animacji chodzenia
        self.last_animation_change_time = pygame.time.get_ticks()  # czas ostatniej zmiany animacji
        self.animation_change_interval = 3000  # interwał zmiany animacji (co 3 sekundy)

    def update(self, player_pos):
        """
        aktualizuje stan bossa, wykonując ruch i strzał w kierunku gracza.

        args:
        player_pos (tuple): pozycja gracza (x, y) na ekranie.
        """
        current_time = pygame.time.get_ticks()

        # sprawdzanie czasu od ostatniej zmiany animacji
        if current_time - self.last_animation_change_time >= self.animation_change_interval:
            if self.current_animation == self.animation_walking:
                self.current_animation = self.animation_hands
            else:
                self.current_animation = self.animation_walking

            self.last_animation_change_time = current_time  # aktualizacja czasu zmiany animacji

        # inicjalizacja i obliczenie ścieżki do gracza
        path_follower = PathFollower(self)
        path_follower.find_path_to_goal((player_pos[0] // GRID_SIZE, player_pos[1] // GRID_SIZE))
        path_follower.move_along_path()

        # wywołanie metody strzelania do gracza
        self.shoot_at_player(player_pos, mode='both')

        # aktualizacja bieżącej animacji bossa
        self.current_animation.update()
        self.image = self.current_animation.current_image  # aktualizacja obrazu bossa

    def draw_health_bar(self, screen):
        """
        rysuje pasek życia bossa na ekranie.

        args:
        screen (pygame.Surface): powierzchnia ekranu gry.
        """
        if self.lives <= 0:
            return

        # obliczenia dla paska życia
        bar_width = 400
        bar_height = 20
        bar_x = (screen.get_width() - bar_width) // 2
        bar_y = screen.get_height() - bar_height - 10
        fill = (self.lives / self.max_lives) * bar_width
        outline_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        fill_rect = pygame.Rect(bar_x, bar_y, fill, bar_height)

        # rysowanie paska życia
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)  # wypełnienie paska
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)  # ramka paska
