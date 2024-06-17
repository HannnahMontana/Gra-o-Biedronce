import math
import pygame
import random
from astar import Astar
from following_enemy import FollowingEnemy
from settings import GRID_SIZE
from animation import Animation


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
        self.animation = Animation(enemy_images, 2.8, 120)

        # Początkowy losowy cel będzie ustawiony później
        self.random_goal = None

    def update(self, player_pos=None):
        """
        aktualizuje studenta, który podąża do losowego punktu
        :param player_pos: pozycja gracza (nieużywane)
        :return: None
        """
        # Ustaw losowy cel, jeśli jeszcze nie został ustawiony
        if not self.random_goal:
            self.random_goal = self.get_random_goal()

        self.find_path_to_goal(self.random_goal)  # znajdź ścieżkę do losowego punktu
        self.move_along_path()  # poruszaj się wzdłuż ścieżki
        self.animation.update()  # aktualizacja animacji
        self.image = self.animation.current_image  # aktualizacja obrazu studenta

    def get_random_goal(self):
        """
        Losuje nowy cel, który nie jest przeszkodą
        :return: tuple(int, int) - nowy losowy cel
        """
        while True:
            random_goal = (random.randint(0, self.level.width - 1), random.randint(0, self.level.height - 1))
            if self.level.grid[random_goal[1]][random_goal[0]] != 1:  # Sprawdzenie, czy punkt nie jest przeszkodą
                return random_goal

    def find_path_to_goal(self, goal):
        """
        znajduje ścieżkę do celu, jeśli to konieczne
        :param goal: cel
        :return: None
        """
        astar = Astar(self.level)  # inicjalizacja algorytmu A*
        start = (self.rect.x // GRID_SIZE, self.rect.y // GRID_SIZE)  # aktualna pozycja studenta

        # sprawdzenie, czy ścieżka nie istnieje lub jest inna niż ostatnio znaleziona
        if not self.path or self.path[-1] != goal:
            self.path = astar.find_path(start, goal)  # znalezienie nowej ścieżki
            self.target_index = 0  # index na początek ścieżki

    def move_along_path(self):
        """
        porusza studenta wzdłuż ścieżki
        :return: None
        """
        # AI studenta - porusza się do losowego punktu
        # sprawdzenie, czy istnieje ścieżka i indeks celu jest w granicach długości ścieżki
        if self.path and self.target_index < len(self.path):
            next_move = self.path[self.target_index]  # następny punkt docelowy na ścieżce
            # pozycja docelowa
            target_pos = (next_move[0] * GRID_SIZE, next_move[1] * GRID_SIZE)
            # oblicza wektor
            direction_x, direction_y = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
            # obliczanie odległości studenta od celu
            distance = math.hypot(direction_x, direction_y)

            # jeśli odległość jest mniejsza od prędkości, przesuwa na cel
            if distance < self.speed:
                self.rect.x, self.rect.y = target_pos[0], target_pos[1]
                self.target_index += 1  # następny punkt docelowy
            else:
                self.move_towards_target(target_pos)  # przesuwa w kierunku celu

        # Jeśli dotarł do celu, losuje nowy cel
        if self.target_index >= len(self.path):
            self.random_goal = self.get_random_goal()
            self.path = None  # resetowanie ścieżki
