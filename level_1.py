import pygame, random
from level import Level
from grandma import Grandma
from hobo import Hobo

# todo: stworzyc kilka wzorów pokojów
# todo: oczywiście musimy to przenieść do jakiegoś innego pliku
# chwilowo tutaj mamy pozycje w ktorych mogą się znajdować enemies (przypadkowe)
enemies_locations = [
    (250, 587),
    (1329, 665),
    (413, 164),
    (776, 204),
    (674, 548),
]


class Level_1(Level):
    def __init__(self, player, images):
        super().__init__(player, images)

        # placeholder (left, top, width, height)
        self.obstacles = [
            pygame.Rect(200, 200, 100, 50),
            pygame.Rect(400, 300, 100, 50),
            pygame.Rect(300, 300, 100, 50),
            pygame.Rect(200, 300, 100, 50),
        ]

        # Tworzenie wrogów losowo
        for pos in enemies_locations:
            # losowanie czy na danej pozycji może się znaleźć wrog
            has_enemy = random.choice([True, False])
            # jesli na danej pozycji zostalo wylosowane ze bedzie wrog to go dodajemy
            if has_enemy:
                x, y = pos
                # todo: potem tu sie bedzie losowal rodzaj wroga
                # dodajemy babcie na pozycji pos
                grandma = Grandma(self.images['PLAYER'], self.images['METEORBROWN_SMALL1'], x, y, 2)
                grandma.level = self  # Przypisujemy obecny level do wroga
                self.enemies.add(grandma)  # dodaj babcię do grupy wrogów w levelu

        player.level = self

    def draw(self, surface):
        super().draw(surface)
        # rysowanie przeszkód
        for obstacle in self.obstacles:
            surface.blit(self.images['METEORBROWN_BIG1'], obstacle.topleft)
