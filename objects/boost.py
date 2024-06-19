import pygame


class Boost(pygame.sprite.Sprite):
    """
    Klasa reprezentująca boosty (bonusy) w grze.

    Attributes:
    boost_type (str): Typ boosta ('beer', 'energy_drink', 'scratch_lottery').
    images (dict): Słownik zawierający obrazy dla różnych typów boostów.
    image (pygame.Surface): Aktualny obrazek boosta.
    rect (pygame.Rect): Prostokąt okalający obrazek boosta na ekranie.
    """

    def __init__(self, boost_type, x, y, images):
        """
        Inicjalizuje obiekt boosta.

        Args:
        boost_type (str): Typ boosta do załadowania ('beer', 'energy_drink', 'scratch_lottery').
        x (int): Współrzędna x pozycji startowej boosta na ekranie.
        y (int): Współrzędna y pozycji startowej boosta na ekranie.
        images (dict): Słownik obrazków dla różnych typów boostów.
        """
        super().__init__()
        self.boost_type = boost_type
        self.images = images
        self.image = self.load_image(boost_type)
        self.rect = self.image.get_rect(center=(x, y))

    def load_image(self, boost_type):
        """
        Ładuje odpowiedni obrazek dla danego typu boosta.

        Args:
        boost_type (str): Typ boosta ('beer', 'energy_drink', 'scratch_lottery').

        Returns:
        pygame.Surface: Obrazek boosta.
        """
        if boost_type == 'beer':
            return self.images['BEER']
        elif boost_type == 'energy_drink':
            return self.images['ENERGY_DRINK']
        elif boost_type == 'scratch_lottery':
            return self.images['SCRATCH_LOTTERY']

    def draw(self, surface):
        """
        Rysuje boost na powierzchni.

        Args:
        surface (pygame.Surface): Powierzchnia, na której ma być narysowany boost.
        """
        surface.blit(self.image, self.rect)
