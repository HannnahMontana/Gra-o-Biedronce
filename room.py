import pygame, random

# Stałe wymiary pokoju
ROOM_WIDTH = 1266
ROOM_HEIGHT = 640

# Stałe kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Klasa reprezentująca pokój
class Room:
    def __init__(self, x, y):
        """
        Inicjalizuje pokój na podstawie podanych współrzędnych.

        :param x: Współrzędna x lewego górnego rogu pokoju.
        :param y: Współrzędna y lewego górnego rogu pokoju.
        """
        self.rect = pygame.Rect(x, y, ROOM_WIDTH, ROOM_HEIGHT)
        self.doors = {'top': False, 'bottom': False, 'left': False, 'right': False}
        self.obstacles = [
            pygame.Rect(200, 200, 100, 100),
            pygame.Rect(400, 300, 150, 50)
        ]

    def draw(self, screen, offset_x, offset_y):
        """
        Rysuje pokój na ekranie z przesunięciem.

        :param screen: Ekran, na którym rysujemy.
        :param offset_x: Przesunięcie w osi X.
        :param offset_y: Przesunięcie w osi Y.
        """
        pygame.draw.rect(screen, WHITE, self.rect.move(offset_x, offset_y), 2)

        if self.doors['top']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.centerx + offset_x, self.rect.top + offset_y),
                             (self.rect.centerx + offset_x, self.rect.top - 10 + offset_y), 2)
        if self.doors['bottom']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.centerx + offset_x, self.rect.bottom + offset_y),
                             (self.rect.centerx + offset_x, self.rect.bottom + 10 + offset_y), 2)
        if self.doors['left']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.left + offset_x, self.rect.centery + offset_y),
                             (self.rect.left - 10 + offset_x, self.rect.centery + offset_y), 2)
        if self.doors['right']:
            pygame.draw.line(screen, WHITE,
                             (self.rect.right + offset_x, self.rect.centery + offset_y),
                             (self.rect.right + 10 + offset_x, self.rect.centery + offset_y), 2)

        for obstacle in self.obstacles:
            pygame.draw.rect(screen, BLACK, obstacle.move(self.rect.x + offset_x, self.rect.y + offset_y))
