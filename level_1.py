import pygame
from level import Level
from grandma import Grandma


class Level_1(Level):
    def __init__(self, player, images):
        super().__init__(player, images)
        self.obstacles = [
            pygame.Rect(200, 200, 100, 100),
            pygame.Rect(400, 300, 150, 50)
        ]

        # Tworzymy wrogów
        grandma = Grandma(self.images['PLAYER'], self.images['METEORBROWN_SMALL1'], 300, 300, 2)

        # Przypisujemy obecny level do postaci
        grandma.level = self
        player.level = self

        self.enemies.add(grandma)   # dodaj babcię do grupy wrogów w levelu

    def draw(self, surface):
        super().draw(surface)
        # przeszkody
        for obstacle in self.obstacles:
            pygame.draw.rect(surface, (0, 0, 0), obstacle)
