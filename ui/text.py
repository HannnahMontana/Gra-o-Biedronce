import pygame

class Text:
    def __init__(self, text, text_color, pc_x, pc_y, font_size=36, font_type=None):
        """
        Inicjalizacja obiektu tekstu.

        :param text: Treść tekstu do wyświetlenia.
        :param text_color: Kolor tekstu.
        :param pc_x: Pozycja X środka tekstu na ekranie.
        :param pc_y: Pozycja Y środka tekstu na ekranie.
        :param font_size: Rozmiar czcionki (domyślnie 36).
        :param font_type: Typ czcionki (None dla domyślnej czcionki systemowej).
        """
        self.rect = None
        self.image = None
        self.text = str(text)
        self.text_color = text_color
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.pc_x = pc_x
        self.pc_y = pc_y
        self.update()

    def draw(self, surface):
        """
        Metoda rysująca tekst na podanej powierzchni.

        :param surface: Powierzchnia, na której ma być narysowany tekst.
        """
        surface.blit(self.image, self.rect)

    def update(self):
        """
        Metoda aktualizująca obrazek i prostokąt tekstu na podstawie bieżących parametrów.
        """
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pc_x, self.pc_y

    def set_text(self, new_text):
        """
        Metoda ustawiająca nowy tekst do wyświetlenia.

        :param new_text: Nowy tekst do wyświetlenia.
        """
        self.text = str(new_text)
        self.update()

    def set_color(self, new_color):
        """
        Metoda ustawiająca nowy kolor tekstu.

        :param new_color: Nowy kolor tekstu.
        """
        self.text_color = new_color
        self.update()

    def set_position(self, new_pc_x, new_pc_y):
        """
        Metoda ustawiająca nową pozycję środka tekstu.

        :param new_pc_x: Nowa pozycja X środka tekstu.
        :param new_pc_y: Nowa pozycja Y środka tekstu.
        """
        self.pc_x = new_pc_x
        self.pc_y = new_pc_y
        self.update()
