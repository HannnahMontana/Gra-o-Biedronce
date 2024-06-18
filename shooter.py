import math

import pygame

from bullet import Bullet


class Shooter:
    def __init__(self, bullet_img, shoot_delay, bullet_speed):
        self.is_shooting = None
        self.bullet_img = bullet_img
        self.shoot_delay = shoot_delay
        self.bullet_speed = bullet_speed
        self.last_shoot_time = 0

    def shoot(self, position, direction_x, direction_y, owner):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time
            bullet = Bullet(self.bullet_img, position[0], position[1], direction_x * self.bullet_speed,
                            direction_y * self.bullet_speed, owner)
            owner.level.set_of_bullets.add(bullet)

    def shoot_many(self, position, direction_x, direction_y, owner):
        """
        Specjalny sposób strzału Hobo: trzy pociski jednocześnie na krótki dystans.

        :param position: pozycja początkowa strzału
        :param direction_x: kierunek strzału w osi X
        :param direction_y: kierunek strzału w osi Y
        :param owner: właściciel pocisku
        """
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time  # aktualizacja czasu ostatniego wystrzału
            self.is_shooting = True  # flaga śledząca, czy Hobo aktualnie strzela

            spread_angle = 15  # kąt rozproszenia pocisków w stopniach
            radians = math.radians(spread_angle)

            # tworzenie trzech pocisków z różnymi kątami
            for angle in [-radians, 0, radians]:
                # obliczenie nowych kierunków dla każdego pocisku
                new_direction_x = direction_x * math.cos(angle) - direction_y * math.sin(angle)
                new_direction_y = direction_x * math.sin(angle) + direction_y * math.cos(angle)
                # tworzy pocisk o określonym obrazie, pozycji, kierunku, szybkości i właścicelu
                bullet = Bullet(self.bullet_img, position[0], position[1], new_direction_x * self.bullet_speed,
                                new_direction_y * self.bullet_speed, owner)

                bullet.spawn_time = pygame.time.get_ticks()  # mierzy czas ile istnieje pocisk
                bullet.hobo_bullet = True  # oznaczenie pocisku jako pocisku Hobo

                owner.level.set_of_bullets.add(bullet)  # dodanie pocisku do zestawu pocisków poziomu
