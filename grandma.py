from settings import GRID_SIZE

import pygame
from shooting_enemy import ShootingEnemy
from following_enemy import FollowingEnemy
from animation import Animation
from path_finder import PathFinder


class Grandma(ShootingEnemy, FollowingEnemy):
    def __init__(self, enemy_images, bullet_img, cx, cy, speed=0.8):
        # inicjalizacja zmiennych
        self.image = None  # aktualny obraz babci
        self.target_index = None  # indeks celu na ścieżce
        self.path = None  # ścieżka do celu

        # skalowanie obrazów
        enemy_img_scaled = pygame.transform.scale(enemy_images[0], (enemy_images[0].get_width() // 2.8,
                                                                    enemy_images[0].get_height() // 2.8))
        bullet_img_scaled = pygame.transform.scale(bullet_img, (bullet_img.get_width() // 2.4,
                                                                bullet_img.get_height() // 2.4))

        # inicjalizacja klasy bazowej
        super().__init__(enemy_img_scaled, bullet_img_scaled, cx, cy, speed, lives=2, shoot_delay=1250,
                         bullet_speed=4.5, bullet_lifetime=1000, shooting_distance=500)

        # inicjalizacja animacji
        self.animation = Animation(enemy_images, 2.8, 120)

    def update(self, player_pos):
        """
        aktualizuje babcię, która nas śledzi i rzuca w nas pomarańczami
        :param player_pos: pozycja gracza
        :return: None
        """
        path_finder = PathFinder(self)  # inicjalizacja klasy PathFinder

        # self.find_path_to_goal(player_pos)  # znajdź ścieżkę do gracza
        path_finder.find_path_to_goal((player_pos[0] // GRID_SIZE, player_pos[1] // GRID_SIZE))
        path_finder.move_along_path()  # poruszaj się wzdłuż ścieżki
        self.shoot_at_player(player_pos)  # strzelaj w kierunku gracza
        self.animation.update()  # aktualizacja animacji
        self.image = self.animation.current_image  # aktualizacja obrazu babci

