import pygame, random
from level import Level
from grandma import Grandma
from hobo import Hobo

enemies_locations = [
    (783, 370)

]


class Boss_level(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        self.obstacles = [

        ]

        for (x, y) in enemies_locations:
            # dodajemy babcie na pozycji x, y
            grandma = Grandma(self.images['PLAYER'], self.images['METEORBROWN_SMALL1'], x, y, 2)
            grandma.level = self  # Przypisujemy obecny level do wroga
            self.enemies.add(grandma)  # dodaj babcię do grupy wrogów w levelu

        player.level = self




