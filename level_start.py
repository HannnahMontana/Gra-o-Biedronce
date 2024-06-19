from level import Level

class Level_start(Level):
    def __init__(self, player, images, entry_door_direction=None):
        """
        Inicjalizuje poziom początkowy.

        :param player: Obiekt gracza
        :param images: Zestaw obrazów poziomu
        :param entry_door_direction: Kierunek drzwi wejściowych
        """
        super().__init__(player, images, entry_door_direction)  # inicjalizacja klasy bazowej
        self.images = images  # przypisanie obrazów poziomu
        self.obstacles = []  # lista przeszkód na poziomie (początkowo pusta)

        player.level = self  # ustawienie poziomu dla gracza
