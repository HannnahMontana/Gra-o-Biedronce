from entities.enemies.boss import Boss
from levels.level import Level


boss_location = (783, 370)  # miejsce, gdzie będzie się znajdować boss


class BossLevel(Level):
    """
    poziom gry, gdzie spotykamy bosasa.

    atrybuty:
    obstacles (list): lista przeszkód na poziomie, początkowo pusta.
    boss (Boss): instancja Boss, reprezentująca bossa na poziomie.
    """

    def __init__(self, player, images, entry_door_direction=None):
        """
        inicjuje poziom z bossem.

        args:
        player (Player): obiekt gracza na poziomie.
        images (dict): słownik z obrazkami używanymi na poziomie.
        entry_door_direction (str lub None): kierunek drzwi wejściowych, opcjonalny.

        tworzy poziom z bossem i dodaje go do gry.
        """
        super().__init__(player, images, entry_door_direction)

        self.obstacles = []

        enemy_images = [self.images[key] for key in self.images if key.startswith('WORKER')]

        # Tworzenie instancji bossa i dodawanie go do grupy wrogów na poziomie
        boss = Boss(enemy_images, self.images['BULLET_GRANDMA'], boss_location[0], boss_location[1], 2)
        boss.level = self
        self.enemies.add(boss)
        self.boss = boss
        player.level = self

    def draw(self, screen):
        """
        rysuje wszystkie elementy na poziomie, w tym pasek życia bossa.

        args:
        screen (pygame.Surface): powierzchnia ekranu do rysowania.
        """
        super().draw(screen)  # wywołanie metody rysowania z klasy nadrzędnej
        self.boss.draw_health_bar(screen)  # rysowanie paska życia bossa
