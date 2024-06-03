import pygame
from settings import HEIGHT, WIDTH, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED
from shooter import Shooter
from character import Character


class Player(Character, Shooter):
    def __init__(self, image, cx, cy, bullet_img):
        Character.__init__(self, image, cx, cy, 8)
        Shooter.__init__(self, bullet_img, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED)

    def update(self, key_pressed):
        """
        Atualizuje stan gracza.
        """
        self.handle_movement(key_pressed)
        self.handle_shooting(key_pressed)

        # blokowanie wyjścia poza ekran gry
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH

    def handle_movement(self, key_pressed):
        """
        Obsługuje ruch gracza na podstawie przycisków WSAD
        :param key_pressed:
        :return:
        """
        if key_pressed[pygame.K_a]:
            self.rect.move_ip([-self.speed, 0])
        if key_pressed[pygame.K_d]:
            self.rect.move_ip([self.speed, 0])
        if key_pressed[pygame.K_w]:
            self.rect.move_ip([0, -self.speed])
        if key_pressed[pygame.K_s]:
            self.rect.move_ip([0, self.speed])

    def handle_shooting(self, key_pressed):
        """
        Obsługuje strzelanie gracza na podstawie klawiszy strzałek
        :param key_pressed:
        :return:
        """
        if key_pressed[pygame.K_UP]:
            self.shoot(self.rect.center, 0, -1)
        if key_pressed[pygame.K_LEFT]:
            self.shoot(self.rect.center, -1, 0)
        if key_pressed[pygame.K_RIGHT]:
            self.shoot(self.rect.center, 1, 0)
        if key_pressed[pygame.K_DOWN]:
            self.shoot(self.rect.center, 0, 1)
