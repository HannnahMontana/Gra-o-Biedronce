import random

import pygame

from enemy import Enemy
from shooter import Shooter


# todo: wziac AI babci, ale zamiast podążać za graczem, to niech wybiera sobie losowy punkt, ktory nie jest przeszkoda
class Student(Enemy, Shooter):
    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, 0, 0)
        self.lives = 2
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.change_direction_time = pygame.time.get_ticks() + random.choice(
            [2000, 5000])  # zmiana kierunku co 2-5 sekundy
        self.rect = self.image.get_rect(center=(cx, cy))

    def update(self, player_pos):
        """
        Aktualizuje Ladybug, która porusza się w liniach prostych i zmienia kierunek co kilka sekund.
        :param player_pos:
        :param screen_rect: prostokąt ekranu używany do wykrywania kolizji z krawędziami
        :return:
        """
        current_time = pygame.time.get_ticks()
        if current_time > self.change_direction_time:
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
            self.change_direction_time = current_time + random.randint(2000, 5000)

        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
