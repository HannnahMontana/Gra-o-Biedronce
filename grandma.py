import math
import pygame

from astar import Astar
from following_enemy import FollowingEnemy
from settings import GRID_SIZE
from shooter import Shooter
from animation import Animation


class Grandma(FollowingEnemy, Shooter):
    def __init__(self, enemy_images, bullet_img, cx, cy, speed=0.8):
        enemy_img_scaled = pygame.transform.scale(enemy_images[0], (enemy_images[0].get_width() // 2.8,
                                                                    enemy_images[0].get_height() // 2.8))
        bullet_img_scaled = pygame.transform.scale(bullet_img, (bullet_img.get_width() // 2.4,
                                                                bullet_img.get_height() // 2.4))

        FollowingEnemy.__init__(self, enemy_img_scaled, cx, cy, speed)
        Shooter.__init__(self, bullet_img_scaled, shoot_delay=1250, bullet_speed=4.5)
        self.target_index = None
        self.lives = 2
        self.path = []
        self.animation = Animation(enemy_images, 2.8, 120)

    def update(self, player_pos):
        """
        Aktualizuje babcię, która nas śledzi i rzuca w nas pomarańczami
        :param player_pos:
        :return:
        """

        self.find_path_to_goal(player_pos)
        self.move_along_path()

        self.shoot_at_player(player_pos)

        self.animation.update()
        self.image = self.animation.current_image

    def find_path_to_goal(self, player_pos):
        """
        Znajduje ścieżkę do celu, jeśli to konieczne
        :param player_pos:
        :return:
        """
        astar = Astar(self.level)
        player_x, player_y = player_pos
        start = (self.rect.x // GRID_SIZE, self.rect.y // GRID_SIZE)  # aktualna pozycja babci
        goal = (player_x // GRID_SIZE, player_y // GRID_SIZE)  # cel - pozycja gracza

        # Sprawdzenie, czy ścieżka nie istnieje lub jest inna niż ostatnio znaleziona
        if not self.path or self.path[-1] != goal:
            self.path = astar.find_path(start, goal)  # Znalezienie nowej ścieżki
            self.target_index = 0  # index na początek ścieżki

    def move_along_path(self):
        """
        Porusza babcię wzdłuż ścieżki
        :return:
        """
        # AI babci -  porusza sie w naszym kierunku
        # Sprawdzenie, czy istnieje ścieżka i indeks celu jest w granicach długości ścieżki
        if self.path and self.target_index < len(self.path):
            next_move = self.path[self.target_index]  # następny punkt docelowy na ścieżce
            # pozcja docelowa
            target_pos = (next_move[0] * GRID_SIZE, next_move[1] * GRID_SIZE)
            # oblicza wektor
            direction_x, direction_y = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
            # obliczanie odległości babci od gracza twierdzeniem Pitagorasa
            distance = math.hypot(direction_x, direction_y)

            # Jeśli odległość jest mniejsza od prędkości, przesuwa na cel
            if distance < self.speed:
                self.rect.x, self.rect.y = target_pos[0], target_pos[1]
                self.target_index += 1  # następny punkt docelowy
            else:
                self.move_towards_target(target_pos)  # przesuwa w kierunku celu

    def shoot_at_player(self, player_pos):
        """
        Strzela w kierunku gracza
        :param player_pos:
        :return:
        """
        player_x, player_y = player_pos
        # Wektor kierunku strzału
        direction_x = player_x - self.rect.x
        direction_y = player_y - self.rect.y
        distance = math.hypot(direction_x, direction_y) or 1

        # Normalizacja wektora kierunku
        direction_x /= distance
        direction_y /= distance

        self.shoot(self.rect.center, direction_x, direction_y, self)
