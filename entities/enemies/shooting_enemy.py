import math
import pygame

from entities.behaviors.shooter import Shooter
from entities.enemies.enemy import Enemy


class ShootingEnemy(Enemy, Shooter):
    """
    Klasa ShootingEnemy reprezentuje wroga, który potrafi strzelać.
    Dziedziczy zarówno po klasie Enemy, jak i Shooter.

    Atrybuty:
    __init__(self, enemy_img, bullet_img, cx, cy, speed, lives, shoot_delay, bullet_speed, bullet_lifetime,
             shooting_distance):
        Inicjalizacja strzelającego wroga.

    Metody:
    shoot_at_player(self, player_pos, mode='one'):
        Strzela w kierunku gracza.

    update_bullets(self):
        Aktualizuje stan pocisków wrogich.
    """

    def __init__(self, enemy_img, bullet_img, cx, cy, speed, lives, shoot_delay, bullet_speed, bullet_lifetime,
                 shooting_distance):
        """
        Inicjalizacja strzelającego wroga.

        :param enemy_img: Obrazek wroga
        :param bullet_img: Obrazek pocisku
        :param cx: Początkowa pozycja X wroga
        :param cy: Początkowa pozycja Y wroga
        :param speed: Prędkość wroga
        :param lives: Ilość żyć wroga
        :param shoot_delay: Opóźnienie między strzałami (w milisekundach)
        :param bullet_speed: Prędkość pocisku wroga
        :param bullet_lifetime: Czas życia pocisku wroga (w milisekundach)
        :param shooting_distance: Maksymalna odległość, na jaką wróg potrafi strzelać
        """
        # Inicjalizacja klas bazowych
        Enemy.__init__(self, enemy_img, cx, cy, speed)
        Shooter.__init__(self, bullet_img, shoot_delay, bullet_speed)

        # Ustawienie parametrów wroga
        self.lives = lives
        self.speed = speed
        self.path = []  # Ścieżka do celu (puste na początku)

        # Parametry strzelania
        self.bullet_lifetime = bullet_lifetime
        self.shooting_distance = shooting_distance

    def shoot_at_player(self, player_pos, mode='one'):
        """
        Strzela w kierunku gracza.

        :param player_pos: Pozycja gracza (x, y)
        :param mode: Tryb strzału ('one', 'many' lub 'both')
        """
        player_x, player_y = player_pos
        direction_x = player_x - self.rect.x
        direction_y = player_y - self.rect.y
        distance = math.hypot(direction_x, direction_y) or 1
        direction_x /= distance
        direction_y /= distance

        if mode == 'both':
            if distance >= self.shooting_distance:
                self.shoot(self.rect.center, direction_x, direction_y, self)
            else:
                self.shoot_many(self.rect.center, direction_x, direction_y, self)
        else:
            if distance <= self.shooting_distance:
                if mode == 'many':
                    self.shoot_many(self.rect.center, direction_x, direction_y, self)
                else:
                    self.shoot(self.rect.center, direction_x, direction_y, self)

    def update_bullets(self):
        """
        Aktualizuje stan pocisków wrogich.
        """
        current_time = pygame.time.get_ticks()
        for bullet in self.level.set_of_bullets:
            if hasattr(bullet, 'owner') and bullet.owner == self:
                if current_time - bullet.spawn_time > self.bullet_lifetime:
                    bullet.kill()
