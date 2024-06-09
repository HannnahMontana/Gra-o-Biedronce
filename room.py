import pygame, random
from grandma import Grandma
from hobo import Hobo
from settings import ROOM_WIDTH, ROOM_HEIGHT


# Stałe kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

enemies_locations = [
    (250, 587),
    (1329, 665),
    (413, 164),
    (776, 204),
    (674, 548),
]


# Klasa reprezentująca pokój
class Room:
    def __init__(self, x, y, images, player):
        """
        Inicjalizuje pokój na podstawie podanych współrzędnych.

        :param x: Współrzędna x lewego górnego rogu pokoju.
        :param y: Współrzędna y lewego górnego rogu pokoju.
        """
        self.images = images
        self.player = player
        self.rect = pygame.Rect(x, y, ROOM_WIDTH, ROOM_HEIGHT)
        self.doors = {'top': False, 'bottom': False, 'left': False, 'right': False}
        self.obstacles = [
            pygame.Rect(200, 200, 100, 100),
            pygame.Rect(450, 300, 100, 100)
        ]
        #obraz skały jako imagesP2
        self.imagesP2 = pygame.image.load('images-from-shooting-game/meteorBrown_big1.png')

        self.enemies = pygame.sprite.Group()
        # self.player.level = player.level
        self.generate_enemies()




    def generate_enemies(self):
        for pos in enemies_locations:
            if random.choice([True, False]):
                x, y = pos
                grandma = Hobo(self.images['PLAYER'], self.images['METEORBROWN_SMALL1'], x, y, 2)
                grandma.level = self.player.level
                self.enemies.add(grandma)
                self.player.level.enemies.add(grandma)

    def draw(self, screen, offset_x, offset_y):
        """
        Rysuje pokój na ekranie z przesunięciem.

        :param screen: Ekran, na którym rysujemy.
        :param offset_x: Przesunięcie w osi X.
        :param offset_y: Przesunięcie w osi Y.
        """
        # todo: tutaj dodajemy 50 do offsetu, trzeba coś z tym zrobić i naprawić, //
        #  ale narazie mi sie nie chce nad tym myśleć
        pygame.draw.rect(screen, WHITE, self.rect.move(offset_x + 50, offset_y + 50), 2)

        if self.doors['top']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.centerx + offset_x + 50, self.rect.top + offset_y + 50),
                             (self.rect.centerx + offset_x + 50, self.rect.top - 10 + offset_y + 50), 2)
        if self.doors['bottom']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.centerx + offset_x + 50, self.rect.bottom + offset_y + 50),
                             (self.rect.centerx + offset_x + 50, self.rect.bottom + 10 + offset_y + 50), 2)
        if self.doors['left']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.left + offset_x + 50, self.rect.centery + offset_y + 50),
                             (self.rect.left - 10 + offset_x + 50, self.rect.centery + offset_y + 50), 2)
        if self.doors['right']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.right + offset_x + 50, self.rect.centery + offset_y + 50),
                             (self.rect.right + 10 + offset_x + 50, self.rect.centery + offset_y + 50), 2)

        for obstacle in self.obstacles:
            #pygame.draw.rect(screen, BLACK, obstacle.move(self.rect.x + offset_x, self.rect.y + offset_y))
            #tutaj rysuje kamienie w miejscach gdzie są obstacle
            screen.blit(self.imagesP2, obstacle.topleft)
        print(self.player.rect.x, self.player.rect.y)
        print(self.enemies)

        self.enemies.draw(screen)
        self.enemies.update((self.player.rect.centerx + offset_x, self.player.rect.centery + offset_y))

        self.handle_bullet_collisions()
    def handle_bullet_collisions(self):
        # Sprawdzenie kolizji pocisków z przeszkodami
        for bullet in list(self.player.level.set_of_bullets):
            for obstacle in self.obstacles:
                if bullet.rect.colliderect(obstacle):
                    bullet.kill()