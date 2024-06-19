from animation import Animation
from enemy import Enemy
from path_follower import PathFollower


class Student(Enemy):
    """
    Klasa Student reprezentuje wroga typu Student, który podąża do losowego punktu na mapie.
    Dziedziczy po klasie Enemy.

    Atrybuty:
    __init__(self, enemy_images, cx, cy, speed=0.8):
        Inicjalizacja studenta.

    Metody:
    update(self, player_pos=None):
        Aktualizacja stanu studenta.
    """

    def __init__(self, enemy_images, cx, cy, speed=0.8):
        """
        Inicjalizacja studenta.

        :param enemy_images: Lista obrazków wroga (animacje)
        :param cx: Początkowa pozycja X wroga
        :param cy: Początkowa pozycja Y wroga
        :param speed: Prędkość poruszania się wroga
        """
        # Inicjalizacja klasy bazowej (Enemy)
        super().__init__(enemy_images[0], cx, cy, speed)

        # Inicjalizacja animacji
        self.animation = Animation(enemy_images, 200)  # Animation(enemy_images, frame_duration)

        # Początkowo losowy cel będzie ustawiony później
        self.random_goal = None

    def update(self, player_pos=None):
        """
        Aktualizacja stanu studenta, który podąża do losowego punktu.

        :param player_pos: Pozycja gracza (nieużywane)
        :return: None
        """
        path_follower = PathFollower(self)  # Inicjalizacja klasy PathFollower

        # Ustaw losowy cel, jeśli jeszcze nie został ustawiony
        if not self.random_goal:
            self.random_goal = path_follower.get_random_goal()

        # Znajdź ścieżkę do losowego punktu
        path_follower.find_path_to_goal(self.random_goal)

        # Poruszaj się wzdłuż ścieżki do celu
        path_follower.move_along_path(random_goal=True)

        # Aktualizacja animacji
        self.animation.update()
        self.image = self.animation.current_image
