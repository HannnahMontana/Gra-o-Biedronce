import pygame
import sys
import math

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kolizja i Spychanie")

# Definicje kolorów
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Klasa obiektu
class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.vel_x = 0
        self.vel_y = 0

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collide_with(self, other):
        if self.rect.colliderect(other.rect):
            dx = self.rect.centerx - other.rect.centerx
            dy = self.rect.centery - other.rect.centery
            distance = math.hypot(dx, dy)
            if distance == 0:
                return
            dx /= distance
            dy /= distance
            self.rect.x += dx
            self.rect.y += dy
            other.rect.x -= dx
            other.rect.y -= dy


# Tworzenie obiektów
player = GameObject(100, 100, 50, 50, RED)
enemy = GameObject(300, 300, 50, 50, BLUE)


def move_towards(target, mover, speed):
    dx = target.rect.centerx - mover.rect.centerx
    dy = target.rect.centery - mover.rect.centery
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    dx /= distance
    dy /= distance
    mover.vel_x = dx * speed
    mover.vel_y = dy * speed


# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obsługa klawiatury dla playera
    keys = pygame.key.get_pressed()
    player.vel_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    player.vel_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

    # Ruch gracza
    player.move()

    # Ruch wroga w kierunku gracza
    move_towards(player, enemy, 1)
    enemy.move()

    # Wykrywanie kolizji i reakcja
    player.collide_with(enemy)

    # Rysowanie wszystkiego
    screen.fill(WHITE)
    player.draw(screen)
    enemy.draw(screen)
    pygame.display.flip()

    # Ograniczenie FPS
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
