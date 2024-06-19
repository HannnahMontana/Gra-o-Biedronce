from settings import GRID_SIZE

from shooting_enemy import ShootingEnemy
from animation import Animation
from path_follower import PathFollower


class Grandma(ShootingEnemy):
    """
    Klasa reprezentująca przeciwnika - babcię.
    Dziedziczy po ShootingEnemy, co oznacza, że potrafi strzelać do gracza.

    Attributes:
    image (pygame.Surface): Aktualny obraz babci.
    target_index (int): Indeks celu na ścieżce.
    path (list): Ścieżka do celu.
    animation (Animation): Animacja ruchu babci.

    Methods:
    __init__: Inicjalizuje obiekt babci.
    update: Aktualizuje zachowanie babci, w tym śledzenie gracza i strzelanie w jego kierunku.
    """
    def __init__(self, enemy_images, bullet_img, cx, cy, speed=0.8):
        """
        Inicjalizuje obiekt babci.

        Args:
        enemy_images (list): Lista obrazów dla animacji babci.
        bullet_img (pygame.Surface): Obrazek pocisku.
        cx (int): Początkowa pozycja X babci.
        cy (int): Początkowa pozycja Y babci.
        speed (float): Prędkość poruszania się babci (domyślnie 0.8).
        """
        self.image = None
        self.target_index = None
        self.path = None

        super().__init__(enemy_images[0], bullet_img, cx, cy, speed, lives=2, shoot_delay=1250,
                         bullet_speed=4.5, bullet_lifetime=1000, shooting_distance=500)

        self.animation = Animation(enemy_images, 120)

    def update(self, player_pos):
        """
        Aktualizuje zachowanie babci, która śledzi gracza i strzela w jego kierunku.

        Args:
        player_pos (tuple): Pozycja gracza (x, y).

        Returns:
        None
        """
        path_follower = PathFollower(self)
        path_follower.find_path_to_goal((player_pos[0] // GRID_SIZE, player_pos[1] // GRID_SIZE))
        path_follower.move_along_path()
        self.shoot_at_player(player_pos)
        self.animation.update()
        self.image = self.animation.current_image
