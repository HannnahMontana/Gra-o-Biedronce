from level import Level
from grandma import Grandma


class Level_1(Level):
    def __init__(self, player, images):
        super().__init__(player, images)

        # Tworzymy wrogów
        grandma = Grandma(self.images['PLAYER'], self.images['METEORBROWN_SMALL1'], 300, 300, 2)

        # Przypisujemy obecny level do postaci
        grandma.level = self
        player.level = self

        self.enemies.add(grandma)   # dodaj babcię do grupy wrogów w levelu

