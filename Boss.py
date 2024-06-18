
import pygame

from animation import Animation
from following_enemy import FollowingEnemy
from path_follower import PathFollower
from settings import GRID_SIZE
from shooting_enemy import ShootingEnemy


class Boss(FollowingEnemy, ShootingEnemy):
    def __init__(self, enemy_images, bullet_img, cx, cy, speed):
        enemy_img_scaled = pygame.transform.scale(enemy_images[0], (
            enemy_images[0].get_width() // 2.8, enemy_images[0].get_height() // 2.8))
        bullet_img_scaled = pygame.transform.scale(bullet_img,
                                                   (bullet_img.get_width() // 2.2, bullet_img.get_height() // 2.2))

        ShootingEnemy.__init__(self, enemy_img_scaled, bullet_img_scaled, cx, cy, speed, lives=10, shoot_delay=1000,
                               bullet_speed=5, bullet_lifetime=1000, shooting_distance=500)
        # FollowingEnemy.__init__(self, enemy_img_scaled, cx, cy, speed)
        self.target_index = None
        self.lives = 10
        self.path = []

        self.shooting_distance = 400

        self.animation_walking = Animation(enemy_images[:-2], scale=2.8, delay=110)
        self.animation_hands = Animation(enemy_images[-2:], scale=2.8, delay=150)

    def update(self, player_pos):
        """
        Aktualizuje bossa, który nas śledzi i rzuca w nas pomarańczami
        :param player_pos:
        :return:
        """
        path_follower = PathFollower(self)
        path_follower.find_path_to_goal((player_pos[0] // GRID_SIZE, player_pos[1] // GRID_SIZE))
        path_follower.move_along_path()
        self.shoot_at_player(player_pos, mode='both')
        self.animation_walking.update()  # aktualizacja animacji
        self.image = self.animation_walking.current_image  # aktualizacja obrazu bossa