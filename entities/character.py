import pygame

class Character(pygame.sprite.Sprite):
    """
    Klasa reprezentująca postać w grze.

    Attributes:
    image (pygame.Surface): Obrazek postaci.
    rect (pygame.Rect): Prostokąt okalający postać.
    speed (int): Prędkość poruszania się postaci.
    lives (int): Liczba żyć postaci.
    level (Level): Obecny poziom, na którym znajduje się postać.
    """

    def __init__(self, image, cx, cy, speed):
        """
        Inicjalizuje postać.

        Args:
        image (pygame.Surface): Obrazek postaci.
        cx (int): Początkowa pozycja X postaci.
        cy (int): Początkowa pozycja Y postaci.
        speed (int): Prędkość poruszania się postaci.

        Ustawia parametry początkowe postaci.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.speed = speed
        self.lives = 3  # domyślne życia
        self.level = None

    def draw(self, surface):
        """
        Rysuje postać na ekranie.

        Args:
        surface (pygame.Surface): Powierzchnia, na której rysujemy postać.
        """
        surface.blit(self.image, self.rect)

    def take_damage(self, amount):
        """
        Zmniejsza liczbę żyć postaci po otrzymaniu obrażeń.

        Args:
        amount (int): Ilość obrażeń do zadania postaci.
        """
        self.lives -= amount