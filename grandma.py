import math, heapq

from enemy import Enemy
from shooter import Shooter
from settings import GRID_SIZE
from astar import Astar


class Grandma(Enemy, Shooter):
    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, shoot_delay=1000, bullet_speed=5)
        self.target_index = None
        self.lives = 2
        self.path = []

    def update(self, player_pos):
        """
        Aktualizuje babcię, która nas śledzi i rzuca w nas pomarańczami
        :param player_pos:
        :return:
        """
        self.find_path_to_goal(player_pos)
        self.move_along_path()
        self.shoot_at_player(player_pos)

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
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2) or 1

        # Normalizacja wektora kierunku
        direction_x /= distance
        direction_y /= distance

        self.shoot(self.rect.center, direction_x, direction_y, self)

