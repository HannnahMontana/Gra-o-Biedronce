import pygame


class Bullet(pygame.sprite.Sprite):
    """
    Klasa reprezentująca pocisk wystrzelony w grze.

    Attributes:
    image (pygame.Surface): Obrazek pocisku.
    rect (pygame.Rect): Prostokąt okalający pocisk.
    movement_x (int): Prędkość poruszania się pocisku w osi X.
    movement_y (int): Prędkość poruszania się pocisku w osi Y.
    owner (object): Obiekt właściciela pocisku, np. gracz lub wróg.
    """

    def __init__(self, image, cx, cy, movement_x, movement_y, owner):
        """
        Inicjalizuje pocisk.

        Args:
        image (pygame.Surface): Obrazek pocisku.
        cx (int): Początkowa pozycja X pocisku.
        cy (int): Początkowa pozycja Y pocisku.
        movement_x (int): Prędkość poruszania się pocisku w osi X.
        movement_y (int): Prędkość poruszania się pocisku w osi Y.
        owner (object): Obiekt właściciela pocisku.

        Ustawia początkowe parametry pocisku.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy  # ustawienie środka pocisku na podanej pozycji (cx, cy)
        self.movement_x = movement_x  # ustawienie prędkości ruchu w osi X
        self.movement_y = movement_y
        self.owner = owner  # określenie, kto wystrzelił ten pocisk

    def update(self):
        """
        Aktualizuje pozycję pocisku w każdej klatce gry.
        """
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y
