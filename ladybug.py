import math, heapq

import pygame

from enemy import Enemy
from settings import GRID_SIZE
from astar import Astar


class Ladybug(Enemy):
    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)

        self.target_index = None
        self.lives = 2
        self.path = []

        self.angle = 0
        self.circle_radius = 3  # promień okręgu
        self.circle_speed = 0.03  # prędkość kątowa
    def update(self, player_pos):
        """
        Aktualizuje babcię, która nas śledzi i rzuca w nas pomarańczami
        :param player_pos:
        :return:
        """

        self.find_path_to_goal(player_pos)
        self.move_along_path()


        # # Sprawdzenie kolizji z graczem
        # collisions = pygame.sprite.spritecollide(self, [self.level.player], False)
        # for player in collisions:
        #     player.apply_pushing(self)

    def find_path_to_goal(self, player_pos):
        """
        Znajduje ścieżkę do celu, jeśli to konieczne
        :param player_pos:
        :return:
        """
        astar = Astar(self.level)

        player_x, player_y = player_pos
        start = (self.rect.x // GRID_SIZE, self.rect.y // GRID_SIZE)    # aktualna pozycja babci
        goal = (player_x // GRID_SIZE, player_y // GRID_SIZE)   # cel - pozycja gracza

        # Sprawdzenie, czy ścieżka nie istnieje lub jest inna niż ostatnio znaleziona
        if not self.path or self.path[-1] != goal:
            self.path = astar.find_path(start, goal)    # Znalezienie nowej ścieżki
            self.target_index = 0   # index na początek ścieżki

    def move_along_path(self):
        """
        Porusza babcię wzdłuż ścieżki
        :return:
        """
        # AI babci -  porusza sie w naszym kierunku
        # Sprawdzenie, czy istnieje ścieżka i indeks celu jest w granicach długości ścieżki
        if self.path and self.target_index < len(self.path):
            next_move = self.path[self.target_index]    # następny punkt docelowy na ścieżce
            # pozcja docelowa
            target_x = next_move[0] * GRID_SIZE
            target_y = next_move[1] * GRID_SIZE
            # oblicza wektor
            direction_x = target_x - self.rect.x
            direction_y = target_y - self.rect.y
            # obliczanie odległości babci od gracza twierdzeniem Pitagorasa
            distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

            # Jeśli odległość jest mniejsza od prędkości, przesuwa na cel
            if distance < self.speed:
                self.rect.x = target_x
                self.rect.y = target_y
                self.target_index += 1  # następny punkt docelowy
            else:
                # normalizacja wektora kierunku (zeby przesuwac babcie w naszym kierunku ze stala predkoscia)
                direction_x /= distance
                direction_y /= distance
                # ruch w kierunku gracza
                self.rect.x += direction_x * self.speed
                self.rect.y += direction_y * self.speed

                self.angle += self.circle_speed
                orbit_x = math.cos(self.angle) * self.circle_radius
                orbit_y = math.sin(self.angle) * self.circle_radius

                self.rect.x += orbit_x
                self.rect.y += orbit_y

