import math

import pygame
from settings import HEIGHT, WIDTH, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED, DOOR_TRIGGER_POINT, VULNERABILITY_TIME, \
    PLAYER_START_LIVES
from shooter import Shooter
from character import Character
from animation import Animation


class Player(Character, Shooter):
    """
    Klasa reprezentująca gracza.
    """

    def __init__(self, cx, cy, player_images, bullet_img):
        """
        Inicjalizacja gracza.

        :param cx: Początkowa pozycja X gracza
        :param cy: Początkowa pozycja Y gracza
        :param player_images: Słownik zawierający obrazy gracza
        :param bullet_img: Obrazek pocisku gracza
        """
        Character.__init__(self, player_images['front'][0], cx, cy, speed=6)
        Shooter.__init__(self, bullet_img, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED)
        self.lives = PLAYER_START_LIVES
        self.level = None

        self.invulnerable = False  # Flaga nietykalności
        self.invulnerable_start_time = 0  # Czas rozpoczęcia nietykalności

        self.animations = {
            "front": Animation(player_images['front'], 120),
            "back": Animation(player_images['back'], 120),
            "left": Animation(player_images['left'], 120),
            "right": Animation(player_images['right'], 120)
        }

        self.default_image = player_images['front'][0]
        self.current_animation = self.animations["front"]

    def apply_boost(self, boost_type):
        """
        Zastosowuje boost do gracza.

        :param boost_type: Typ boosta do zastosowania
        """
        if boost_type == 'beer':
            self.lives = PLAYER_START_LIVES
            self.boostB = True
            self.boostType = 'BEER'

        elif boost_type == 'energy_drink':
            self.speed *= 1.3
            self.boostE = True
            self.boostType = 'ENERGY_DRINK'

        elif boost_type == 'scratch_lottery':
            self.shoot_delay = 200
            self.boostS = True
            self.boostType = 'SCRATCH_LOTTERY'

    def push(self, entity, target, obstacles=None):
        """
        Przesuwa entity w kierunku lub od targetu, z uwzględnieniem kolizji z przeszkodami.

        :param entity: Obiekt do przesunięcia
        :param target: Cel przesunięcia
        :param obstacles: Lista przeszkód do uwzględnienia
        """
        dx = target.rect.centerx - entity.rect.centerx
        dy = target.rect.centery - entity.rect.centery
        distance = math.hypot(dx, dy) or 1
        dx /= distance
        dy /= distance

        entity.rect.x -= dx
        entity.rect.y -= dy

        if obstacles:
            for obstacle in obstacles:
                if entity.rect.colliderect(obstacle):
                    entity.rect.x += dx
                    entity.rect.y += dy
                    break

    def update(self, key_pressed):
        """
        Aktualizuje stan gracza.

        :param key_pressed: Klawisze wciśnięte przez gracza
        """
        self.handle_movement(key_pressed)
        self.handle_shooting(key_pressed)
        self.check_boundary_cross()

        if self.invulnerable and pygame.time.get_ticks() - self.invulnerable_start_time > VULNERABILITY_TIME:
            self.invulnerable = False

    def make_invulnerable(self):
        """
        Ustawia gracza w stan nietykalności na 3 sekundy.
        """
        self.invulnerable = True
        self.invulnerable_start_time = pygame.time.get_ticks()

    def take_damage(self, damage):
        """
        Redukuje życie gracza, jeśli nie jest w stanie nietykalności.

        :param damage: Ilość obrażeń do zadania graczowi
        """
        dmg_sound = pygame.mixer.Sound('music/dmg.mp3')

        if not self.invulnerable:
            if self.lives != 2:
                dmg_sound.play(0)
            super().take_damage(damage)
            self.make_invulnerable()

    def check_boundary_cross(self):
        """
        Sprawdza, czy gracz przekroczył granicę poziomu.
        """
        if (self.rect.left > DOOR_TRIGGER_POINT and self.rect.right < WIDTH - DOOR_TRIGGER_POINT and
                self.rect.top > DOOR_TRIGGER_POINT and self.rect.bottom < HEIGHT - DOOR_TRIGGER_POINT):
            self.level.trigger_doors()

    def _move_and_handle_collision(self, dx, dy):
        """
        Przesuwa gracza i sprawdza kolizje z obiektami.

        :param dx: Przesunięcie w osi X
        :param dy: Przesunięcie w osi Y
        """
        self.rect.move_ip(dx, dy)

        all_collidables = self.level.obstacles + self.level.walls + list(self.level.enemies)
        if self.level.closed_doors:
            all_collidables += self.level.closed_doors

        for collidable in all_collidables:
            collidable_rect = collidable.rect if hasattr(collidable, 'rect') else collidable
            if self.rect.colliderect(collidable_rect):
                self.rect.move_ip(-dx, -dy)
                break

    def handle_movement(self, key_pressed):
        """
        Obsługuje ruch gracza na podstawie przycisków WSAD.

        :param key_pressed: Klawisze wciśnięte przez gracza
        """
        dx, dy = 0, 0

        if key_pressed[pygame.K_a]:
            dx = -self.speed
            self.current_animation = self.animations["left"]
        if key_pressed[pygame.K_d]:
            dx = self.speed
            self.current_animation = self.animations["right"]
        if key_pressed[pygame.K_w]:
            dy = -self.speed
            self.current_animation = self.animations["back"]
        if key_pressed[pygame.K_s]:
            dy = self.speed
            self.current_animation = self.animations["front"]

        if dx != 0 or dy != 0:
            self.current_animation.update()
            self.image = self.current_animation.current_image
        else:
            self.image = self.default_image

        if dx != 0:
            self._move_and_handle_collision(dx, 0)

        if dy != 0:
            self._move_and_handle_collision(0, dy)
        self.check_boundary_cross()

    def handle_shooting(self, key_pressed):
        """
        Obsługuje strzelanie gracza na podstawie klawiszy strzałek.

        :param key_pressed: Klawisze wciśnięte przez gracza
        """
        shoot_sound = pygame.mixer.Sound('music/shot.mp3')
        if key_pressed[pygame.K_UP]:
            self.shoot(self.rect.center, 0, -1, self)
            shoot_sound.play(0)
        if key_pressed[pygame.K_LEFT]:
            self.shoot(self.rect.center, -1, 0, self)
            shoot_sound.play(0)
        if key_pressed[pygame.K_RIGHT]:
            self.shoot(self.rect.center, 1, 0, self)
            shoot_sound.play(0)
        if key_pressed[pygame.K_DOWN]:
            self.shoot(self.rect.center, 0, 1, self)
            shoot_sound.play()

    def alive(self):
        """
        Sprawdza, czy gracz żyje.

        :return: True, jeśli gracz żyje (ma życie większe niż 0)
        """
        return self.lives > 0

    def reset_player(self):
        """
        Resetuje gracza do stanu początkowego.
        """
        self.rect.x = 683
        self.rect.y = 370
        self.lives = PLAYER_START_LIVES
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.speed = 6
        self.boostB = False
        self.boostE = False
        self.boostS = False
