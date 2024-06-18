import pygame

from animation import Animation
from following_enemy import FollowingEnemy
from path_follower import PathFollower
from settings import GRID_SIZE
from shooting_enemy import ShootingEnemy


class Boss(FollowingEnemy, ShootingEnemy):
    def __init__(self, enemy_images, bullet_img, cx, cy, speed):


        ShootingEnemy.__init__(self, enemy_images[0], bullet_img, cx, cy, speed, lives=10, shoot_delay=1000,
                               bullet_speed=5, bullet_lifetime=1000, shooting_distance=500)
        # FollowingEnemy.__init__(self, enemy_img_scaled, cx, cy, speed)
        self.target_index = None
        self.lives = 10
        self.max_lives = 10
        self.path = []

        self.shooting_distance = 400

        self.animation_walking = Animation(enemy_images[:-2], delay=110)
        self.animation_hands = Animation(enemy_images[-2:], delay=150)

        self.current_animation = self.animation_walking  # Startujemy od animacji chodzenia
        self.last_animation_change_time = pygame.time.get_ticks()  # czas ostatniej zmiany animacji
        self.animation_change_interval = 5000  # co 5 sekund zmienia animację

    def update(self, player_pos):
        """
        Aktualizuje bossa, który nas śledzi i rzuca w nas pomarańczami
        :param player_pos:
        :return:
        """
        current_time = pygame.time.get_ticks()

        # Sprawdzanie czasu od ostatniej zmiany animacji
        if current_time - self.last_animation_change_time >= self.animation_change_interval:
            if self.current_animation == self.animation_walking:
                self.current_animation = self.animation_hands
            else:
                self.current_animation = self.animation_walking

            self.last_animation_change_time = current_time  # aktualizacja czasu zmiany

        path_follower = PathFollower(self)
        path_follower.find_path_to_goal((player_pos[0] // GRID_SIZE, player_pos[1] // GRID_SIZE))
        path_follower.move_along_path()
        self.shoot_at_player(player_pos, mode='both')

        self.current_animation.update()  # aktualizacja bieżącej animacji
        self.image = self.current_animation.current_image  # aktualizacja obrazu bossa

    def draw_health_bar(self, screen):
        if self.lives <= 0:
            return

        bar_width = 400
        bar_height = 20
        bar_x = (screen.get_width() - bar_width) // 2
        bar_y = screen.get_height() - bar_height - 10
        fill = (self.lives / self.max_lives) * bar_width
        outline_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        fill_rect = pygame.Rect(bar_x, bar_y, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)