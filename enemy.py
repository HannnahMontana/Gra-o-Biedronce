import math
from character import Character


class Enemy(Character):
    """
    Klasa reprezentująca wroga w grze.

    Attributes:
    image (pygame.Surface): Obrazek wroga.
    rect (pygame.Rect): Prostokąt okalający wroga.
    speed (int): Prędkość poruszania się wroga.
    lives (int): Liczba żyć wroga.
    level (Level): Obecny poziom, na którym znajduje się wróg.
    """

    def __init__(self, image, cx, cy, speed):
        """
        Inicjalizuje wroga.

        Args:
        image (pygame.Surface): Obrazek wroga.
        cx (int): Początkowa pozycja X wroga.
        cy (int): Początkowa pozycja Y wroga.
        speed (int): Prędkość poruszania się wroga.

        Ustawia parametry początkowe wroga.
        """
        super().__init__(image, cx, cy, speed)

    def kill_if_dead(self):
        """
        Zabija wroga, jeśli jego liczba żyć jest mniejsza lub równa zero.
        """
        if self.lives <= 0:
            self.kill()  # wywołanie metody kill() klasy Sprite

    def move_towards_target(self, target_pos):
        """
        Porusza wroga w kierunku określonego celu.

        Args:
        target_pos (tuple): Pozycja celu, do którego porusza się wróg.
        """
        # obliczenie kierunku ruchu wroga
        target_x, target_y = target_pos
        direction_x = target_x - self.rect.x    # różnica między pozycją wroga a pozycją celu
        direction_y = target_y - self.rect.y
        distance = math.hypot(direction_x, direction_y) or 1    # obliczenie odległości między wrogiem a celem
        direction_x /= distance # normalizacja wektora kierunku
        direction_y /= distance

        self.rect.x += direction_x * self.speed # przesunięcie wroga w ustalonym kierunku
        self.rect.y += direction_y * self.speed
