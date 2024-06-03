import pygame, time
from settings import HEIGHT, WIDTH, SHOOT_DELAY, BULLET_SPEED
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy, bullet_img):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.bullet_img = bullet_img
        self.level = None
        self.lives = 3
        self.last_shoot_time = 0
        self.shoot_delay = SHOOT_DELAY  # ms

    def draw(self, surface):
        """
        Rysuje gracza na ekranie.
        """
        surface.blit(self.image, self.rect)

    def update(self, key_pressed):
        """
        Atualizuje stan gracza.
        """
        self.get_event(key_pressed)

        # blokowanie wyjścia poza ekran gry
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > WIDTH:
            self.rect.centerx = WIDTH

    def shoot(self, direction):
        """
        obsluguje strzelanie
        """
        current_time = pygame.time.get_ticks()
        # strzela co iles ms
        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time     # aktualizacja czasu osttaniego wystrzalu

            # ustawienie ruchu pocisku na podstawie kierunku
            movement_x, movement_y = 0, 0
            if direction == 'up':
                movement_y = -BULLET_SPEED
            elif direction == 'down':
                movement_y = BULLET_SPEED
            elif direction == 'left':
                movement_x = -BULLET_SPEED
            elif direction == 'right':
                movement_x = BULLET_SPEED

            # tworzenie pocisku
            bullet = Bullet(self.bullet_img, self.rect.centerx, self.rect.centery, movement_x, movement_y)
            # dodawanie pocisku do grupy
            self.level.set_of_bullets.add(bullet)

    def get_event(self, key_pressed):
        """
        Obsługuje zdarzenia klawiatury
        """
        # ruchy gracza (WSAD)
        if key_pressed[pygame.K_a]:
            self.rect.move_ip([-8, 0])
        if key_pressed[pygame.K_d]:
            self.rect.move_ip([8, 0])
        if key_pressed[pygame.K_w]:
            self.rect.move_ip([0, -8])
        if key_pressed[pygame.K_s]:
            self.rect.move_ip([0, 8])

        # strzelanie (strzalki)
        if key_pressed[pygame.K_UP]:
            self.shoot("up")
        if key_pressed[pygame.K_LEFT]:
            self.shoot("left")
        if key_pressed[pygame.K_RIGHT]:
            self.shoot("right")
        if key_pressed[pygame.K_DOWN]:
            self.shoot("down")


