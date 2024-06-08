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

    def generate_dungeon(self):
        """Generuje lochy. Metoda do nadpisania w klasach dziedziczących."""
        pass

    def update(self):
        """Aktualizuje stan poziomu."""
        new_room = self.get_current_room()
        if new_room and new_room != self.current_room:
            self.current_room = new_room

    def draw(self, screen):
        """Rysuje aktualny pokój."""
        # rysowanie żyć
        for i in range(self.player.lives - 1):
            screen.blit(self.images['PLAYERLIFE'], (20 + i * 45, 20))

        if self.current_room:
            offset_x = screen.get_width() // 2 - self.current_room.rect.centerx
            offset_y = screen.get_height() // 2 - self.current_room.rect.centery
            self.current_room.draw(screen, offset_x, offset_y)

    def get_current_room(self):
        """Zwraca pokój, w którym znajduje się gracz."""
        for room in self.rooms:
            if room.rect.colliderect(self.player.rect):
                return room
        return None
