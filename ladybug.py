import math, pygame
from enemy import Enemy
from shooter import Shooter
from following_enemy import FollowingEnemy


class Ladybug(FollowingEnemy, Shooter):

    def __init__(self, image, bullet_img, cx, cy, speed):
        FollowingEnemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, 2000, 5)
        self.lives = 5
        # aspekty spraiające że ma się kręcić
        self.angle = 0  # początkowy kąt
        self.circle_radius = 5  # promień okręgu
        self.circle_speed = 0.10  # prędkość obrotu
        self.bullet_lifetime = 1000  # Czas życia pocisków w milisekundach
        self.shooting_distance = 500  # Maksymalna odległość od gracza, przy której Hobo strzela

    def update(self, player_pos):
        self.move_towards_target(player_pos)

        # dodanie ruchu po własnej orbicie
        self.angle += self.circle_speed
        orbit_x = math.cos(self.angle) * self.circle_radius
        orbit_y = math.sin(self.angle) * self.circle_radius

        self.rect.x += orbit_x
        self.rect.y += orbit_y
