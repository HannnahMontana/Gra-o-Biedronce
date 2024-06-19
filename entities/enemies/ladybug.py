import math

from effects.animation import Animation
from entities.enemies.enemy import Enemy


class Ladybug(Enemy):
    """
    Klasa reprezentująca przeciwnika - Ladybug.

    Dziedziczy po klasie Enemy, co oznacza, że potrafi poruszać się i atakować gracza.

    Attributes:
    angle (float): Aktualny kąt obrotu ladybuga wokół własnej orbity.
    circle_radius (float): Promień orbity ladybuga.
    circle_speed (float): Prędkość obrotu ladybuga wokół orbity.
    animation (Animation): Animacja ruchu ladybuga.

    Methods:
    __init__: Inicjalizuje obiekt Ladybug.
    update: Aktualizuje zachowanie Ladybuga, w tym poruszanie się w kierunku gracza i ruch po orbicie.
    """
    def __init__(self, enemy_images, cx, cy, speed=1):
        """
        Inicjalizuje obiekt Ladybug, ustawiając obraz i prędkość wroga oraz
        inicjując parametry orbity i animacji.

        Args:
        enemy_images (list): Lista obrazów dla animacji Ladybug.
        cx (int): Początkowa pozycja X Ladybug.
        cy (int): Początkowa pozycja Y Ladybug.
        speed (float): Prędkość poruszania się Ladybug (domyślnie 1).
        """
        super().__init__(enemy_images[0], cx, cy, speed)
        self.lives = 2
        self.angle = 0
        self.circle_radius = 5
        self.circle_speed = 0.1
        self.animation = Animation(enemy_images, 60)

    def update(self, player_pos):
        """
        Aktualizuje zachowanie Ladybug, poruszając się w kierunku gracza i wykonując ruch po orbicie.

        Args:
        player_pos (tuple): Pozycja gracza (x, y).

        Returns:
        None
        """
        self.move_towards_target(player_pos)

        self.angle += self.circle_speed
        orbit_x = math.cos(self.angle) * self.circle_radius
        orbit_y = math.sin(self.angle) * self.circle_radius

        self.rect.x += orbit_x
        self.rect.y += orbit_y

        self.animation.update()
        self.image = self.animation.current_image
