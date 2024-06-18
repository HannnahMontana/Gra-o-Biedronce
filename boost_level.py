import random

from level import Level
from settings import HEIGHT, WIDTH
from boost import Boost


def create_random_boost(images):
    """
    Tworzy losowy Boost i umieszcza go na środku pokoju.

    Args:
    images (dict): Słownik zawierający obrazy dla różnych typów boostów.

    Returns:
    Boost: Obiekt Boost utworzony na środku pokoju.
    """
    boost_types = ['beer', 'energy_drink', 'scratch_lottery']
    chosen_boost = random.choice(boost_types)
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    return Boost(chosen_boost, center_x, center_y, images)


class BoostLevel(Level):
    """
    Klasa reprezentująca poziom z boostem.

    Attributes:
    boost (Boost): Obiekt Boost na poziomie.
    obstacles (list): Lista przeszkód na poziomie.
    """

    def __init__(self, player, images, entry_door_direction=None):
        """
        Inicjalizuje poziom z boostem.

        Args:
        player (object): Obiekt gracza na poziomie.
        images (dict): Słownik zawierający obrazy dla różnych typów boostów.
        entry_door_direction (str, optional): Kierunek wejściowych drzwi na poziomie.
        """
        super().__init__(player, images, entry_door_direction)

        self.boost = create_random_boost(images)  # Tworzenie losowego boosta
        self.obstacles = []  # Lista przeszkód na poziomie (na razie pusta)

        player.level = self  # Przypisanie poziomu do gracza

    def update(self):
        """
        Aktualizuje stan poziomu, w tym sprawdzanie kolizji gracza z boostem.
        """
        super().update()  # Wywołanie metody update z klasy nadrzędnej (Level)

        # Sprawdzamy kolizję gracza z boostem
        if self.boost and self.player.rect.colliderect(self.boost.rect):
            self.player.apply_boost(self.boost.boost_type)  # Zastosowanie boosta do gracza
            self.boost = None  # Usunięcie boosta po zebraniu przez gracza

    def draw(self, surface):
        """
        Rysuje elementy na poziomie, w tym boost, jeśli istnieje.

        Args:
        surface (pygame.Surface): Powierzchnia, na której rysowane są elementy.
        """
        super().draw(surface)  # Wywołanie metody draw z klasy nadrzędnej (Level)

        if self.boost:
            self.boost.draw(surface)  # Rysowanie boosta na powierzchni
