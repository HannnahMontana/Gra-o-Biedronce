import pygame

from ui.text import Text


class Button:
    """
    Klasa reprezentująca przycisk w grze.

    Attributes:
    background_color (tuple): Kolor tła przycisku.
    width (int): Szerokość przycisku.
    height (int): Wysokość przycisku.
    text (Text): Obiekt reprezentujący tekst na przycisku.
    rect (pygame.Rect): Prostokąt okalający przycisk.
    """

    def __init__(self, text, text_color, background_color, width, height,
                 pc_x, pc_y, font_size=36, font_type=None):
        """
        Inicjalizuje przycisk.

        Args:
        text (str): Tekst wyświetlany na przycisku.
        text_color (tuple): Kolor tekstu.
        background_color (tuple): Kolor tła przycisku.
        width (int): Szerokość przycisku.
        height (int): Wysokość przycisku.
        pc_x (int): Pozycja X środka przycisku w procentach.
        pc_y (int): Pozycja Y środka przycisku w procentach.
        font_size (int): Rozmiar czcionki tekstu (opcjonalny, domyślnie 36).
        font_type (str): Typ czcionki (opcjonalny, domyślnie None).

        Ustawia parametry przycisku i tworzy obiekt reprezentujący tekst na przycisku.
        """
        self.background_color = background_color
        self.width = width
        self.height = height
        self.text = Text(text, text_color, pc_x, pc_y, font_size, font_type)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.text.rect.center

    def draw(self, surface):
        """
        Rysuje przycisk na powierzchni.

        Args:
        surface (pygame.Surface): Powierzchnia, na której rysujemy przycisk.

        Aktualizuje tło przycisku, aktualizuje tekst i rysuje oba elementy na podanej powierzchni.
        """
        surface.fill(self.background_color, self.rect)
        self.text.update()
        self.text.draw(surface)
