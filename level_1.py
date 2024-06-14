import pygame, random

from ladybug import Ladybug
from level import Level
from grandma import Grandma
from hobo import Hobo

# todo: stworzyc kilka wzorów pokojów
# todo: oczywiście musimy to przenieść do jakiegoś innego pliku
# chwilowo tutaj mamy pozycje w ktorych mogą się znajdować enemies (przypadkowe)
enemies_locations = [
    (250, 587),
    (1150, 550),
    (413, 164),
    (776, 204),
    (674, 300),
]
#dl75-1291 wys75-665 zakres

# todo: nie wiem czy ta klasa ma sens, żeby była, można przenieść coś z klasy Level tutaj
class Level_1(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        # placeholder (left, top, width, height)
        # todo: to musi byc obiekt Obstacle dziedziczacy po sprite
        self.obstacles = [
            pygame.Rect(200, 200, 100, 80),
            pygame.Rect(400, 300, 100, 80),
            pygame.Rect(300, 300, 100, 80),
            pygame.Rect(200, 300, 100, 80),
        ]

        self.update_grid()

        # Tworzenie wrogów losowo
        for (x, y) in enemies_locations:
            # losowanie czy na danej pozycji może się znaleźć wrog
            has_enemy = random.choice([True, False])
            # jesli na danej pozycji zostalo wylosowane ze bedzie wrog to go dodajemy
            if has_enemy:
                # todo: potem tu sie bedzie losowal rodzaj wroga
                # dodajemy babcie na pozycji x, y
                grandma = Ladybug(self.images['PLAYER'], self.images['METEORBROWN_SMALL1'], x, y, 2)
                grandma.level = self  # Przypisujemy obecny level do wroga
                self.enemies.add(grandma)  # dodaj babcię do grupy wrogów w levelu

        player.level = self

    def draw(self, surface):
        """
        Rysuje elementy dla poziomu 1
        :param surface:
        :return:
        """
        super().draw(surface)
        # rysowanie przeszkód
        for obstacle in self.obstacles:
            surface.blit(self.images['METEORBROWN_BIG1'], obstacle.topleft)
