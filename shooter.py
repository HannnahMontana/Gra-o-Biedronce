import pygame
from bullet import Bullet


class Shooter:
    def __init__(self, bullet_img, shoot_delay, bullet_speed):
        self.bullet_img = bullet_img
        self.shoot_delay = shoot_delay
        self.bullet_speed = bullet_speed
        self.level = None
        self.last_shoot_time = 0

    def shoot(self, position, direction_x, direction_y, owner):
        """
        Obsługuje strzelanie
        :param owner:
        :param position:
        :param direction_x:
        :param direction_y:
        :return:
        """
        # sprawdza aktualny czas
        current_time = pygame.time.get_ticks()
        # strzela tylko kiedy upłynie odpowiednia ilość ms (delay)
        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time  # aktualizacja czasu ostatniego wystrzału

            # tworzenie pocisku i dodanie go do grupy pociasków obecnego levelu
            bullet = Bullet(self.bullet_img, position[0], position[1], direction_x * self.bullet_speed,
                            direction_y * self.bullet_speed, owner)
            self.level.set_of_bullets.add(bullet)
