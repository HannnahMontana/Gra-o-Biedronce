
import math

import pygame

from bullet import Bullet
from enemy import Enemy
from shooter import Shooter
from settings import GRID_SIZE
from astar import Astar


class Boss(Enemy, Shooter):
    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, shoot_delay=1000, bullet_speed=5)
        self.target_index = None
        self.lives = 10
        self.path = []

        self.shooting_distance = 400
    def update(self, player_pos):
        """
        Aktualizuje bossa, która nas śledzi i rzuca w nas pomarańczami
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
        start = (self.rect.x // GRID_SIZE, self.rect.y // GRID_SIZE)    # aktualna pozycja bossa
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
        # AI bossa -  porusza sie w naszym kierunku
        # Sprawdzenie, czy istnieje ścieżka i indeks celu jest w granicach długości ścieżki
        if self.path and self.target_index < len(self.path):
            next_move = self.path[self.target_index]    # następny punkt docelowy na ścieżce
            # pozcja docelowa
            target_x = next_move[0] * GRID_SIZE
            target_y = next_move[1] * GRID_SIZE
            # oblicza wektor
            direction_x = target_x - self.rect.x
            direction_y = target_y - self.rect.y
            # obliczanie odległości bossa od gracza twierdzeniem Pitagorasa
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


        #w zależnośc od odległosci zmienia schemat strzalu
        if distance >= self.shooting_distance:
            self.shoot(self.rect.center, direction_x, direction_y, self)
        else:
            self.shootv2(self.rect.center, direction_x, direction_y, self)


    def shootv2(self, position, direction_x, direction_y, owner):
        """
        Specjalny sposób strzału Hobo: trzy pociski jednocześnie na krótki dystans.
        :param owner:
        :param position:
        :param direction_x:
        :param direction_y:
        :return:
        """
        # sprawdza aktualny czas
        current_time = pygame.time.get_ticks()
        # strzela tylko kiedy upłynie odpowiednia ilość ms (delay)
        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time  # aktualizacja czasu ostatniego wystrzału

            # kąt rozproszenia pocisków
            spread_angle = 15  # kąt rozproszenia w stopniach
            radians = math.radians(spread_angle)

            # tworzenie trzech pocisków z różnymi kątami
            for angle in [-radians, 0,
                          radians]:  # Ta linijka uruchamia pętle 3 razy że każdy pocisk będzie pod kątem radians, 0 i -radians
                # Obliczenie nowych kierunków dla każdego pocisku
                new_direction_x = direction_x * math.cos(angle) - direction_y * math.sin(angle)
                new_direction_y = direction_x * math.sin(angle) + direction_y * math.cos(angle)
                # te linijki sprawiają że się rozchodzą, oblicza kierunki
                bullet = Bullet(self.bullet_img, position[0], position[1], new_direction_x * self.bullet_speed,
                                new_direction_y * self.bullet_speed, owner)
                # tworzy pocisk o określonym obrazie, pozycji, kierunku, szybkości i właścicelu

                bullet.spawn_time = pygame.time.get_ticks()  # mirzy czas ile istnieje pocisk
                bullet.hobo_bullet = True  # oznaczenie pocisku jako pocisku Hobo
                self.level.set_of_bullets.add(bullet)


