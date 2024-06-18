import pygame


class Animation:
    """
    Klasa Animation zarządza animacją poprzez zmianę obrazków w określonych odstępach czasu.

    Atrybuty:
    images (list): Lista ścieżek do obrazków animacji.
    index (int): Aktualny indeks obrazka w liście.
    delay (int): Czas w milisekundach między zmianami obrazków.
    last_update (int): Czas ostatniej aktualizacji obrazka.
    current_image (str): Aktualnie wyświetlany obrazek.
    """

    def __init__(self, image_paths, delay):
        """
        Inicjalizuje obiekt Animation.

        Parametry:
        image_paths (list): Lista ścieżek do obrazków animacji.
        delay (int): Czas w milisekundach między zmianami obrazków.
        """
        # image_paths - lista ścieżek do obrazków
        # delay - czas (w ms) między zmianami obrazków
        self.images = image_paths
        self.index = 0  # aktualny indeks obrazka
        self.delay = delay  # opóźnienie między obrazkami
        self.last_update = pygame.time.get_ticks()  # czas ostatniej aktualizacji
        self.current_image = self.images[0]  # ustawienie pierwszego obrazka

    def update(self):
        """
        Aktualizuje animację, zmieniając obrazek, jeśli upłynęło wystarczająco dużo czasu.
        """
        now = pygame.time.get_ticks()  # aktualny czas
        if now - self.last_update > self.delay:
            # jeżeli minęło więcej czasu niż delay, to zmieniamy obrazek
            self.last_update = now  # aktualizujemy czas ostatniej zmiany
            self.index = (self.index + 1) % len(
                self.images)  # przechodzimy do następnego obrazka, wracając do początku, jeśli to konieczne
            self.current_image = self.images[self.index]  # ustawiamy aktualny obrazek
