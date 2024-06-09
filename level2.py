import pygame


class Level:
    def __init__(self, player, images):
        """
        Inicjalizuje bazowy poziom.

        :param player: Obiekt gracza.
        :param images: Słownik z załadowanymi obrazami.
        """
        self.player = player
        self.images = images
        self.rooms = []
        self.current_room = None
        self.generate_dungeon()
        self.player.level = self
        self.set_of_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def generate_dungeon(self):
        """Generuje sklep. Metoda do nadpisania."""
        pass

    def update(self):
        """Aktualizuje stan poziomu."""
        new_room = self.get_current_room()
        if new_room and new_room != self.current_room:
            self.current_room = new_room
        self.set_of_bullets.update()

        # self.enemies.update(self.player.rect.center)

    def draw(self, screen):
        """Rysuje aktualny pokój."""
        # rysowanie żyć
        for i in range(self.player.lives - 1):
            screen.blit(self.images['PLAYERLIFE'], (20 + i * 45, 20))

        # todo: to poprawić ten offset musi byc gdzies indziej obliczany i to -50 do poprawy jakoś
        if self.current_room:
            offset_x = screen.get_width() // 2 - self.current_room.rect.centerx - 50
            offset_y = screen.get_height() // 2 - self.current_room.rect.centery - 50
            self.current_room.draw(screen, offset_x, offset_y)

        self.set_of_bullets.draw(screen)

    def get_current_room(self):
        """Zwraca pokój, w którym znajduje się gracz."""
        for room in self.rooms:
            if room.rect.colliderect(self.player.rect):
                return room
        return None
