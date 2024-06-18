import pygame

from animation import Animation
from shooting_enemy import ShootingEnemy


class Hobo(ShootingEnemy):
    def __init__(self, enemy_images, bullet_img, cx, cy, speed=0.5):
        """
        Inicjalizuje obiekt Hobo, skalując obrazy wroga i pocisków oraz wywołując
        konstruktor klasy bazowej ShootingEnemy.

        :param enemy_images: lista obrazów wroga
        :param bullet_img: obraz pocisku
        :param cx: pozycja x wroga
        :param cy: pozycja y wroga
        :param speed: prędkość wroga
        """
        self.last_shoot_time = None

        super().__init__(enemy_images[0], bullet_img, cx, cy, speed, lives=5, shoot_delay=2000, bullet_speed=5,
                         bullet_lifetime=1000, shooting_distance=500)

        self.is_shooting = False  # flaga śledząca, czy Hobo aktualnie strzela
        self.animation = Animation(enemy_images, delay=100)

    def update(self, player_pos):
        """
        Aktualizuje stan Hobo, wywołując metody strzelania w kierunku gracza i
        aktualizacji pocisków.

        :param player_pos: pozycja gracza
        """
        self.shoot_at_player(player_pos, mode='many')
        self.update_bullets()

        if self.is_shooting:
            self.animation.update()  # aktualizacja animacji tylko gdy Hobo strzela
            self.image = self.animation.current_image  # aktualizacja obrazu Hobo
            self.is_shooting = False  # resetowanie flagi po zakończeniu animacji strzału