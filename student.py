import random, math, pygame

from animation import Animation
from enemy import Enemy
from path_follower import PathFollower


class Student(Enemy):
    def __init__(self, enemy_images, cx, cy, speed=0.8):
        # inicjalizacja zmiennych
        self.image = None  # aktualny obraz studenta
        self.target_index = None  # indeks celu na ścieżce
        self.path = None  # ścieżka do celu

        # skalowanie obrazów

        # inicjalizacja klasy bazowej
        super().__init__(enemy_images[0], cx, cy, speed)

        # inicjalizacja animacji
        self.animation = Animation(enemy_images, 200)

        # Początkowy losowy cel będzie ustawiony później
        self.random_goal = None

    def update(self, player_pos=None):
        """
        aktualizuje studenta, który podąża do losowego punktu
        :param player_pos: pozycja gracza (nieużywane)
        :return: None
        """
        path_follower = PathFollower(self)  # inicjalizacja klasy PathFinder

        # Ustaw losowy cel, jeśli jeszcze nie został ustawiony
        if not self.random_goal:
            self.random_goal = path_follower.get_random_goal()

        # znajdź ścieżkę do losowego punktu
        path_follower.find_path_to_goal(self.random_goal)
        path_follower.move_along_path(random_goal=True)  # poruszaj się wzdłuż ścieżki
        self.animation.update()  # aktualizacja animacji
        self.image = self.animation.current_image  # aktualizacja obrazu studenta
