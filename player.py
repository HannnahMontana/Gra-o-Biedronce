import math

import pygame, time
from settings import HEIGHT, WIDTH, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED, DOOR_TRIGGER_POINT, VULNERABILITY_TIME, \
    PLAYER_START_LIVES
from shooter import Shooter
from character import Character


class Player(Character, Shooter):
    def __init__(self, image, cx, cy, bullet_img):
        Character.__init__(self, image, cx, cy, speed=6)
        Shooter.__init__(self, bullet_img, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED)
        self.lives = PLAYER_START_LIVES
        self.level = None

        self.invulnerable = False  # Flaga nietykalności
        self.invulnerable_start_time = 0  # Czas rozpoczęcia nietykalności

    def apply_pushing(self, enemy):
        """
        Nakłada efekt odpychania po kolizji z wrogiem.
        """
        dx = self.rect.centerx - enemy.rect.centerx     # różnica na osi x między nami a enemy
        dy = self.rect.centery - enemy.rect.centery
        distance = math.hypot(dx, dy) or 1  # dystans tw. hipokratesa
        dx /= distance  # normalizacja wektora kierunku
        dy /= distance
        self.rect.x += dx   # przesuwamy playera o dx odleglosc
        self.rect.y += dy

    def update(self, key_pressed):
        """
        Atualizuje stan gracza.
        """
        self.handle_movement(key_pressed)
        self.handle_shooting(key_pressed)
        self.check_boundary_cross()

        # Sprawdzenie, czy czas nietykalności minął
        if self.invulnerable and pygame.time.get_ticks() - self.invulnerable_start_time > VULNERABILITY_TIME:
            # jeśli jest aktywna nietykalność i jeśli minęły odpowiednie sekundy to wyłącza ją
            self.invulnerable = False

    def make_invulnerable(self):
        """
        Ustawia gracza w stan nietykalności na 3 sekund.
        """
        self.invulnerable = True
        self.invulnerable_start_time = pygame.time.get_ticks()  # rozpoczyna odliczanie

    def take_damage(self, damage):
        """
        Redukuje życie gracza, jeśli nie jest w stanie nietykalności.
        """
        if not self.invulnerable:
            super().take_damage(damage)
            self.make_invulnerable()  # Ustawienie nietykalności po otrzymaniu obrażeń

    def check_boundary_cross(self):
        """
        sprawdza czy player przekroczył granicę sciany
        :return:
        """
        # sprawdzamy czy gracz przekroczyl wartosc
        if (self.rect.left > DOOR_TRIGGER_POINT and self.rect.right < WIDTH - DOOR_TRIGGER_POINT and
                self.rect.top > DOOR_TRIGGER_POINT and self.rect.bottom < HEIGHT - DOOR_TRIGGER_POINT):
            self.level.trigger_doors()

    def _move_and_handle_collision(self, dx, dy):
        """
        Przesuwa gracza i sprawdza kolizje z obiektami
        """
        self.rect.move_ip(dx, dy)

        # Sprawdzenie kolizji z przeszkodami i wrogami
        all_collidables = self.level.obstacles + self.level.walls + list(self.level.enemies)
        if self.level.closed_doors:
            all_collidables += self.level.closed_doors

        for collidable in all_collidables:
            # jeśli collidable posiada atrybut rect, to jest to Sprite (wrogowie)
            collidable_rect = collidable.rect if hasattr(collidable, 'rect') else collidable
            if self.rect.colliderect(collidable_rect):
                # jeśli wystąpiła kolizja, cofamy przesunięcie
                self.rect.move_ip(-dx, -dy)
                break

    def handle_movement(self, key_pressed):
        """
        Obsługuje ruch gracza na podstawie przycisków WSAD wykrywając przeszkody
        :param key_pressed:
        :return:
        """
        dx, dy = 0, 0  # wartości przesunięcia gracza w osi X i Y
        # ustawiamy przesunięcie na podstawie klawiszy
        if key_pressed[pygame.K_a]:
            dx = -self.speed
        if key_pressed[pygame.K_d]:
            dx = self.speed
        if key_pressed[pygame.K_w]:
            dy = -self.speed
        if key_pressed[pygame.K_s]:
            dy = self.speed

        # ruch pionowy
        if dx != 0:
            self._move_and_handle_collision(dx, 0)

        # ruch poziomy
        if dy != 0:
            self._move_and_handle_collision(0, dy)
        self.check_boundary_cross()

    def handle_shooting(self, key_pressed):
        """
        Obsługuje strzelanie gracza na podstawie klawiszy strzałek
        :param key_pressed:
        :return:
        """
        if key_pressed[pygame.K_UP]:
            self.shoot(self.rect.center, 0, -1, self)
        if key_pressed[pygame.K_LEFT]:
            self.shoot(self.rect.center, -1, 0, self)
        if key_pressed[pygame.K_RIGHT]:
            self.shoot(self.rect.center, 1, 0, self)
        if key_pressed[pygame.K_DOWN]:
            self.shoot(self.rect.center, 0, 1, self)

    def alive(self):
        return self.lives > 0
