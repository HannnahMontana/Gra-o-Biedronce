import random, math

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

    # Obliczenie przyszłego położenia na podstawie kierunku
        future_rect = self.rect.move(self.direction[0] * self.speed, self.direction[1] * self.speed)

        # Sprawdzenie kolizji z przeszkodami
        if not self.check_collision(future_rect):
            self.rect = future_rect  # Przesuń do przyszłego położenia
        else:
            # Jeśli jest kolizja, losujemy nowy kierunek
            self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

    def check_collision(self, future_rect):
        """
        Sprawdza kolizję z przeszkodami.
        """
        all_collidables = self.level.obstacles + self.level.walls + list(self.level.enemies)
        if self.level.closed_doors:
            all_collidables += self.level.closed_doors

        for collidable in all_collidables:
            collidable_rect = collidable.rect if hasattr(collidable, 'rect') else collidable
            if future_rect.colliderect(collidable_rect):
                return True  # Jest kolizja

        return False  # Brak kolizji