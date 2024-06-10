import pygame
from settings import HEIGHT, WIDTH, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED
from shooter import Shooter
from character import Character

#todo: zmniejszyć prędkaość gracza albo zwiększyć prędkość pocisków bo gracz jest szybszy niż własne pociski
class Player(Character, Shooter):
    def __init__(self, image, cx, cy, bullet_img):
        Character.__init__(self, image, cx, cy, speed=4)
        Shooter.__init__(self, bullet_img, PLAYER_SHOOT_DELAY, PLAYER_BULLET_SPEED)
        self.lives = 5
        self.level = None

    def update(self, key_pressed):
        """
        Atualizuje stan gracza.
        """
        self.handle_movement(key_pressed)
        self.handle_shooting(key_pressed)
        self.check_boundaries() #up
        self.check_boundary_cross()
        '''
        # blokowanie wyjścia poza ekran gry
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH
        '''

    def check_boundaries(self):
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH

    def check_boundary_cross(self): #sprawdza czy przekroczyło granicę sciany
        if (self.rect.left > 75 and self.rect.right < WIDTH - 75 and
                self.rect.top > 75 and self.rect.bottom < HEIGHT - 75):
            self.level.trigger_doors()


    def _move_and_handle_collision(self, dx, dy):
        self.rect.move_ip(dx, dy) # przesuwamy gracza

        # Sprawdzenie kolizji z przeszkodami
        for obstacle in self.level.obstacles:
            if self.rect.colliderect(obstacle):
                # jeśli wystąpiła kolizja, cofamy przesunięcie
                self.rect.move_ip(-dx, -dy)

        for sciany in self.level.sciany:
            if self.rect.colliderect(sciany):
                # jeśli wystąpiła kolizja, cofamy przesunięcie
                self.rect.move_ip(-dx, -dy)

        if self.level.doors_closed:
            for door in self.level.doors:
                if self.rect.colliderect(door):
                    # jeśli wystąpiła kolizja, cofamy przesunięcie
                    self.rect.move_ip(-dx, -dy)


    def handle_movement(self, key_pressed):
        """
        Obsługuje ruch gracza na podstawie przycisków WSAD wykrywając przeszkody
        :param key_pressed:
        :return:
        """
        dx, dy = 0, 0   # wartości przesunięcia gracza w osi X i Y
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
