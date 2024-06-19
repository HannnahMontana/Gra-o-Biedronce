from effects.animation import Animation
from entities.enemies.shooting_enemy import ShootingEnemy


class Hobo(ShootingEnemy):
    """
    Klasa reprezentująca przeciwnika - Hobo.

    Dziedziczy po ShootingEnemy, co oznacza, że potrafi strzelać do gracza.

    Attributes:
    last_shoot_time (int or None): Czas ostatniego strzału.
    is_shooting (bool): Flaga śledząca, czy Hobo aktualnie strzela.
    animation (Animation): Animacja ruchu Hobo.

    Methods:
    __init__: Inicjalizuje obiekt Hobo.
    update: Aktualizuje zachowanie Hobo, w tym strzelanie w kierunku gracza i animację.
    """
    def __init__(self, enemy_images, bullet_img, cx, cy, speed=0.5):
        """
        Inicjalizuje obiekt Hobo, skalując obrazy wroga i pocisków oraz wywołując
        konstruktor klasy bazowej ShootingEnemy.

        Args:
        enemy_images (list): Lista obrazów dla animacji Hobo.
        bullet_img (pygame.Surface): Obrazek pocisku.
        cx (int): Początkowa pozycja X Hobo.
        cy (int): Początkowa pozycja Y Hobo.
        speed (float): Prędkość poruszania się Hobo (domyślnie 0.5).
        """
        self.last_shoot_time = None
        super().__init__(enemy_images[0], bullet_img, cx, cy, speed, lives=5, shoot_delay=2000,
                         bullet_speed=5, bullet_lifetime=1000, shooting_distance=500)
        self.is_shooting = False
        self.animation = Animation(enemy_images, delay=100)

    def update(self, player_pos):
        """
        Aktualizuje zachowanie Hobo, w tym strzelanie w kierunku gracza i aktualizację pocisków.

        Args:
        player_pos (tuple): Pozycja gracza (x, y).

        Returns:
        None
        """
        self.shoot_at_player(player_pos, mode='many')
        self.update_bullets()

        if self.is_shooting:
            self.animation.update()
            self.image = self.animation.current_image
            self.is_shooting = False
