import math
import pygame

from enemy import Enemy
from shooter import Shooter


class ShootingEnemy(Enemy, Shooter):
    def __init__(self, enemy_img, bullet_img, cx, cy, speed, lives, shoot_delay, bullet_speed, bullet_lifetime,
                 shooting_distance):
        # inicjalizacja klas bazowych
        Enemy.__init__(self, enemy_img, cx, cy, speed)
        Shooter.__init__(self, bullet_img, shoot_delay, bullet_speed)

        # ustawienie parametrów wroga
        self.lives = lives  # liczba żyć
        self.speed = speed  # prędkość
        self.path = []  # ścieżka do celu

        # parametry strzelania
        self.bullet_lifetime = bullet_lifetime  # czas życia pocisków w milisekundach
        self.shooting_distance = shooting_distance  # maksymalna odległość od gracza, przy której wróg strzela

    def shoot_at_player(self, player_pos):
        """
        strzela w kierunku gracza
        :param player_pos: pozycja gracza
        :return: None
        """
        player_x, player_y = player_pos  # pozycja gracza
        # obliczanie wektora kierunku
        direction_x = player_x - self.rect.x
        direction_y = player_y - self.rect.y
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2) or 1

        # normalizacja wektora kierunku
        direction_x /= distance
        direction_y /= distance

        # strzelanie, jeśli gracz jest w zasięgu
        if distance <= self.shooting_distance:
            self.shoot(self.rect.center, direction_x, direction_y, self)

    def update_bullets(self):
        """
        aktualizacja stanu pocisków
        :return: None
        """
        current_time = pygame.time.get_ticks()  # aktualny czas
        for bullet in self.level.set_of_bullets:  # iteracja po wszystkich pociskach
            if hasattr(bullet, 'owner') and bullet.owner == self:  # sprawdzenie, czy pocisk należy do tego wroga
                # sprawdzenie, czy czas życia pocisku przekroczył jego limit
                if current_time - bullet.spawn_time > self.bullet_lifetime:
                    bullet.kill()  # usunięcie pocisku, jeśli jego czas życia się skończył
