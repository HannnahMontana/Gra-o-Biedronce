import random, math, pygame

from animation import Animation
from following_enemy import FollowingEnemy
from path_finder import PathFinder


class Student(FollowingEnemy):
    def __init__(self, enemy_images, cx, cy, speed=0.8):
        # inicjalizacja zmiennych
        self.image = None  # aktualny obraz studenta
        self.target_index = None  # indeks celu na ścieżce
        self.path = None  # ścieżka do celu

        # skalowanie obrazów
        enemy_img_scaled = pygame.transform.scale(enemy_images[0], (enemy_images[0].get_width() // 2.8,
                                                                    enemy_images[0].get_height() // 2.8))

        # inicjalizacja klasy bazowej
        super().__init__(enemy_img_scaled, cx, cy, speed)

        # inicjalizacja animacji
        self.animation = Animation(enemy_images, 2.8, 200)

        # Początkowy losowy cel będzie ustawiony później
        self.random_goal = None

    def update(self, player_pos=None):
        """
        aktualizuje studenta, który podąża do losowego punktu
        :param player_pos: pozycja gracza (nieużywane)
        :return: None
        """
        path_finder = PathFinder(self)  # inicjalizacja klasy PathFinder

        # Ustaw losowy cel, jeśli jeszcze nie został ustawiony
        if not self.random_goal:
            self.random_goal = path_finder.get_random_goal()

        # znajdź ścieżkę do losowego punktu
        path_finder.find_path_to_goal(self.random_goal)
        path_finder.move_along_path(random_goal=True)  # poruszaj się wzdłuż ścieżki
        self.animation.update()  # aktualizacja animacji
        self.image = self.animation.current_image  # aktualizacja obrazu studenta
