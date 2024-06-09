import pygame
from settings import HEIGHT, WIDTH, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED
from shooter import Shooter
from character import Character


# todo: zmniejszyć prędkaość gracza albo zwiększyć prędkość pocisków bo gracz jest szybszy niż własne pociski
class Player(Character, Shooter):
    def __init__(self, image, cx, cy, bullet_img):
        Character.__init__(self, image, cx, cy, speed=8)
        Shooter.__init__(self, bullet_img, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED)
        self.lives = 5
        self.level = None

    def update(self, key_pressed):
        """
        Atualizuje stan gracza.
        """
        self.handle_movement(key_pressed)
        self.handle_shooting(key_pressed)

        # blokowanie wyjścia poza ekran gry
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.rect.centerx < 0:
        #     self.rect.centerx = 0
        # if self.rect.centerx > WIDTH:
        #     self.rect.centerx = WIDTH

    def _move_and_handle_collision(self, dx, dy):
        self.rect.move_ip(dx, dy)  # przesuwamy gracza

        if self.level.current_room:
            for obstacle in self.level.current_room.obstacles:
                # Przesunięcie przeszkody zgodnie z pozycją pokoju
                shifted_obstacle = obstacle.move(self.level.current_room.rect.topleft)

                if self.rect.colliderect(shifted_obstacle):
                    # jeśli wystąpiła kolizja, cofamy przesunięcie
                    self.rect.move_ip(-dx, -dy)

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

    def handle_shooting(self, key_pressed):
        """
        Obsługuje strzelanie gracza na podstawie klawiszy strzałek
        :param key_pressed:
        :return:
        """

        if self.level.current_room:
            current_room_rect = self.level.current_room.rect

            # Pozycje startowe pocisków skorygowane o przesunięcie pokoju
            shoot_position_x = self.rect.centerx - current_room_rect.x
            shoot_position_y = self.rect.centery - current_room_rect.y

            if key_pressed[pygame.K_UP]:
                self.shoot((shoot_position_x, shoot_position_y), 0, -1, self)
            if key_pressed[pygame.K_LEFT]:
                self.shoot((shoot_position_x, shoot_position_y), -1, 0, self)
            if key_pressed[pygame.K_RIGHT]:
                self.shoot((shoot_position_x, shoot_position_y), 1, 0, self)
            if key_pressed[pygame.K_DOWN]:
                self.shoot((shoot_position_x, shoot_position_y), 0, 1, self)

    def alive(self):
        return self.lives > 0
