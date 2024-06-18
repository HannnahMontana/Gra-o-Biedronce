import math
import pygame

from following_enemy import FollowingEnemy
from animation import Animation


class Ladybug(FollowingEnemy):

    def __init__(self, enemy_images, cx, cy, speed=1):


        FollowingEnemy.__init__(self, enemy_images[0], cx, cy, speed)

        self.lives = 5
        # aspekty kręcenia
        self.angle = 0  # początkowy kąt
        self.circle_radius = 5  # promień okręgu
        self.circle_speed = 0.1  # prędkość obrotu

        self.animation = Animation(enemy_images, 60)

    def update(self, player_pos):
        self.move_towards_target(player_pos)

        # dodanie ruchu po własnej orbicie
        self.angle += self.circle_speed
        orbit_x = math.cos(self.angle) * self.circle_radius
        orbit_y = math.sin(self.angle) * self.circle_radius

        self.rect.x += orbit_x
        self.rect.y += orbit_y

        self.animation.update()
        self.image = self.animation.current_image
