import math
import pygame

from bullet import Bullet
from shooting_enemy import ShootingEnemy


class Hobo(ShootingEnemy):
    def __init__(self, enemy_images, bullet_img, cx, cy, speed=0.5):
        """
        Inicjalizuje obiekt Hobo, skalując obrazy wroga i pocisków oraz wywołując
        konstruktor klasy bazowej ShootingEnemy.

        :param enemy_images: lista obrazów wroga
        :param bullet_img: obraz pocisku
        :param cx: pozycja x wroga
        :param cy: pozycja y wroga
        :param speed: prędkość wroga
        """
        self.last_shoot_time = None
        enemy_img_scaled = pygame.transform.scale(enemy_images[0], (
        enemy_images[0].get_width() // 2.8, enemy_images[0].get_height() // 2.8))
        bullet_img_scaled = pygame.transform.scale(bullet_img,
                                                   (bullet_img.get_width() // 2.4, bullet_img.get_height() // 2.4))
        super().__init__(enemy_img_scaled, bullet_img_scaled, cx, cy, speed, lives=5, shoot_delay=2000, bullet_speed=5,
                         bullet_lifetime=1000, shooting_distance=500)

    def update(self, player_pos):
        """
        Aktualizuje stan Hobo, wywołując metody strzelania w kierunku gracza i
        aktualizacji pocisków.

        :param player_pos: pozycja gracza
        """
        self.shoot_at_player(player_pos)
        self.update_bullets()

    def shoot(self, position, direction_x, direction_y, owner):
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

                self.level.set_of_bullets.add(bullet)  # dodanie pocisku do zestawu pocisków poziomu
