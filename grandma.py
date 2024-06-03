import pygame
import random
from enemy import Enemy
from bullet import Bullet


class Grandma(Enemy):
    def __init__(self, image, bullet_img, cx, cy, speed):
        super().__init__(image, cx, cy, speed)
        self.bullet_img = bullet_img
        self.level = None
        self.shoot_delay = 1000  # opoznienie kolejnego wystrzalu w ms
        self.last_shot_time = 0

    def update(self, player_pos):
        """
        Aktualizuje babcię - pozycję i strzelanie
        :param player_pos:
        :return:
        """
        # AI babci -  porusza sie w naszym kierunku
        player_x, player_y = player_pos     # wspolrzedne x i y gracza
        # obliczanie odleglosci w danym kierunku (wektor odleglosci)
        direction_x = player_x - self.rect.x    # poz gracza - babci
        direction_y = player_y - self.rect.y
        # obliczanie odległości
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5     # twoerdzenie Pitagorasa

        # normalizacja wektora kierunku (zeby przesuwac babcie w naszym kierunku ze stala predkoscia)
        if distance == 0:
            distance = 1
        direction_x /= distance
        direction_y /= distance

        # ruch w kierunku gracza
        self.rect.x += direction_x * self.speed     # aktualizacja pozycji babci na osi X
        self.rect.y += direction_y * self.speed

        # strzelanie
        self.shoot(player_pos)

    def shoot(self, player_pos):
        """
        Obsługuje strzelanie babci
        :param player_pos:
        :return:
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time
            bullet = Bullet(self.bullet_img, self.rect.centerx, self.rect.centery, 0, 0)
            # obliczanie wektora kierunku strzału
            direction_x = player_pos[0] - self.rect.centerx
            direction_y = player_pos[1] - self.rect.centery
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

            if distance == 0:
                distance = 1
            direction_x /= distance
            direction_y /= distance

            # ustawienie prędkości pocisku
            bullet.movement_x = direction_x * 5  # Prędkość pocisku
            bullet.movement_y = direction_y * 5
            self.level.set_of_bullets.add(bullet)
