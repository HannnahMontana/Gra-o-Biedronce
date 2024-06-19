import pygame, math
from bullet import Bullet


class Shooter:
    """
    Klasa Shooter odpowiedzialna za strzelanie pociskami.

    Atrybuty:
    __init__(self, bullet_img, shoot_delay, bullet_speed):
        Inicjalizacja strzelca.

    Metody:
    shoot(self, position, direction_x, direction_y, owner):
        Strzela pojedynczym pociskiem w określonym kierunku.

    shoot_many(self, position, direction_x, direction_y, owner):
        Strzela trzema pociskami jednocześnie w różnych kierunkach (metoda specjalna dla Hobo).
    """

    def __init__(self, bullet_img, shoot_delay, bullet_speed):
        """
        Inicjalizacja strzelca.

        :param bullet_img: Obrazek pocisku
        :param shoot_delay: Opóźnienie między strzałami (w milisekundach)
        :param bullet_speed: Prędkość pocisku
        """
        self.is_shooting = None
        self.bullet_img = bullet_img
        self.shoot_delay = shoot_delay
        self.bullet_speed = bullet_speed
        self.last_shoot_time = 0

    def shoot(self, position, direction_x, direction_y, owner):
        """
        Strzela pojedynczym pociskiem w określonym kierunku.

        :param position: Pozycja początkowa strzału
        :param direction_x: Kierunek strzału w osi X
        :param direction_y: Kierunek strzału w osi Y
        :param owner: Właściciel pocisku
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time
            bullet = Bullet(self.bullet_img, position[0], position[1], direction_x * self.bullet_speed,
                            direction_y * self.bullet_speed, owner)
            owner.level.set_of_bullets.add(bullet)

    def shoot_many(self, position, direction_x, direction_y, owner):
        """
        Strzela trzema pociskami jednocześnie w różnych kierunkach (metoda specjalna dla Hobo).

        :param position: Pozycja początkowa strzału
        :param direction_x: Kierunek strzału w osi X
        :param direction_y: Kierunek strzału w osi Y
        :param owner: Właściciel pocisków
        """
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time
            self.is_shooting = True

            spread_angle = 15  # Kąt rozproszenia pocisków w stopniach
            radians = math.radians(spread_angle)

            for angle in [-radians, 0, radians]:
                new_direction_x = direction_x * math.cos(angle) - direction_y * math.sin(angle)
                new_direction_y = direction_x * math.sin(angle) + direction_y * math.cos(angle)

                bullet = Bullet(self.bullet_img, position[0], position[1], new_direction_x * self.bullet_speed,
                                new_direction_y * self.bullet_speed, owner)

                bullet.spawn_time = pygame.time.get_ticks()
                bullet.hobo_bullet = True

                owner.level.set_of_bullets.add(bullet)
