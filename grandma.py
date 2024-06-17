import math
import pygame

from astar import Astar
from following_enemy import FollowingEnemy
from settings import GRID_SIZE
from animation import Animation
from shooting_enemy import ShootingEnemy


class Grandma(ShootingEnemy, FollowingEnemy):
    def __init__(self, enemy_images, bullet_img, cx, cy, speed=0.8):
        # inicjalizacja zmiennych
        self.image = None  # aktualny obraz babci
        self.target_index = None  # indeks celu na ścieżce
        self.path = None  # ścieżka do celu

        # skalowanie obrazów
        enemy_img_scaled = pygame.transform.scale(enemy_images[0], (enemy_images[0].get_width() // 2.8, enemy_images[0].get_height() // 2.8))
        bullet_img_scaled = pygame.transform.scale(bullet_img, (bullet_img.get_width() // 2.4, bullet_img.get_height() // 2.4))

        # inicjalizacja klasy bazowej
        super().__init__(enemy_img_scaled, bullet_img_scaled, cx, cy, speed, lives=2, shoot_delay=1250, bullet_speed=4.5, bullet_lifetime=1000, shooting_distance=500)

        # inicjalizacja animacji
        self.animation = Animation(enemy_images, 2.8, 120)

    def update(self, player_pos):
        """
        aktualizuje babcię, która nas śledzi i rzuca w nas pomarańczami
        :param player_pos: pozycja gracza
        :return: None
        """
        self.find_path_to_goal(player_pos)  # znajdź ścieżkę do gracza
        self.move_along_path()  # poruszaj się wzdłuż ścieżki
        self.shoot_at_player(player_pos)  # strzelaj w kierunku gracza
        self.animation.update()  # aktualizacja animacji
        self.image = self.animation.current_image  # aktualizacja obrazu babci

    def find_path_to_goal(self, player_pos):
        """
        znajduje ścieżkę do celu, jeśli to konieczne
        :param player_pos: pozycja gracza
        :return: None
        """
        astar = Astar(self.level)  # inicjalizacja algorytmu A*
        player_x, player_y = player_pos  # pozycja gracza
        start = (self.rect.x // GRID_SIZE, self.rect.y // GRID_SIZE)  # aktualna pozycja babci
        goal = (player_x // GRID_SIZE, player_y // GRID_SIZE)  # cel - pozycja gracza

        # sprawdzenie, czy ścieżka nie istnieje lub jest inna niż ostatnio znaleziona
        if not self.path or self.path[-1] != goal:
            self.path = astar.find_path(start, goal)  # znalezienie nowej ścieżki
            self.target_index = 0  # index na początek ścieżki

    def move_along_path(self):
        """
        porusza babcię wzdłuż ścieżki
        :return: None
        """
        # AI babci -  porusza się w naszym kierunku
        # sprawdzenie, czy istnieje ścieżka i indeks celu jest w granicach długości ścieżki
        if self.path and self.target_index < len(self.path):
            next_move = self.path[self.target_index]  # następny punkt docelowy na ścieżce
            # pozycja docelowa
            target_pos = (next_move[0] * GRID_SIZE, next_move[1] * GRID_SIZE)
            # oblicza wektor
            direction_x, direction_y = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
            # obliczanie odległości babci od gracza twierdzeniem Pitagorasa
            distance = math.hypot(direction_x, direction_y)

            # jeśli odległość jest mniejsza od prędkości, przesuwa na cel
            if distance < self.speed:
                self.rect.x, self.rect.y = target_pos[0], target_pos[1]
                self.target_index += 1  # następny punkt docelowy
            else:
                self.move_towards_target(target_pos)  # przesuwa w kierunku celu

    def shoot_at_player(self, player_pos):
        """
        strzela w kierunku gracza
        :param player_pos: pozycja gracza
        :return: None
        """
        player_x, player_y = player_pos
        # wektor kierunku strzału
        direction_x = player_x - self.rect.x
        direction_y = player_y - self.rect.y
        distance = math.hypot(direction_x, direction_y) or 1

        # normalizacja wektora kierunku
        direction_x /= distance
        direction_y /= distance

        # strzał
        self.shoot(self.rect.center, direction_x, direction_y, self)
