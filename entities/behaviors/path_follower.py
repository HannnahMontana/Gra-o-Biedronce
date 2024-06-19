import math
import random

from ai.astar import Astar
from settings import GRID_SIZE


class PathFollower:
    def __init__(self, enemy):
        """
        Inicjalizuje obiekt PathFollower dla danego wroga.

        :param enemy: Obiekt wroga, który będzie podążał za ścieżką
        """
        self.enemy = enemy

    def move_along_path(self, random_goal=False):
        """
        Przesuwa wroga wzdłuż wyznaczonej ścieżki.

        :param random_goal: Flaga określająca, czy losować nowy cel po dotarciu do obecnego
        """
        # Sprawdzenie, czy wróg ma ścieżkę do celu i czy nie osiągnął jeszcze końca ścieżki
        if self.enemy.path and self.enemy.target_index < len(self.enemy.path):
            next_move = self.enemy.path[self.enemy.target_index]  # następny punkt docelowy na ścieżce
            target_pos = (next_move[0] * GRID_SIZE, next_move[1] * GRID_SIZE)  # pozycja docelowa w pikselach
            direction_x, direction_y = target_pos[0] - self.enemy.rect.x, target_pos[1] - self.enemy.rect.y
            distance = math.hypot(direction_x, direction_y)  # odległość do celu

            if distance < self.enemy.speed:
                # jeśli odległość jest mniejsza od prędkości, przesuwa na cel
                self.enemy.rect.x, self.enemy.rect.y = target_pos[0], target_pos[1]
                self.enemy.target_index += 1  # następny punkt docelowy
            else:
                # w przeciwnym razie przesuwa w kierunku celu
                self.enemy.move_towards_target(target_pos)

        if random_goal:
            # Jeśli dotarł do celu, losuje nowy cel
            if self.enemy.target_index >= len(self.enemy.path):
                self.enemy.random_goal = self.get_random_goal()  # ustaw nowy losowy cel
                self.enemy.path = None  # resetowanie ścieżki

    def get_random_goal(self):
        """
        Losuje nowy cel, który nie jest przeszkodą.

        :return: tuple(int, int) - nowy losowy cel
        """
        while True:
            random_goal = (
                random.randint(0, self.enemy.level.width - 1), random.randint(0, self.enemy.level.height - 1))
            if self.enemy.level.grid[random_goal[1]][random_goal[0]] != 1:  # sprawdzenie, czy punkt nie jest przeszkodą
                return random_goal

    def find_path_to_goal(self, goal):
        """
        Znajduje ścieżkę do celu.

        :param goal: Cel, do którego wróg ma się udać
        :return: None
        """
        astar = Astar(self.enemy.level)  # inicjalizacja algorytmu A*
        start = (self.enemy.rect.x // GRID_SIZE, self.enemy.rect.y // GRID_SIZE)  # aktualna pozycja

        # Sprawdzenie, czy ścieżka nie istnieje lub jeśli istnieje, to czy jej końcowy punkt jest różny od nowego celu
        if not self.enemy.path or self.enemy.path[-1] != goal:
            self.enemy.path = astar.find_path(start, goal)  # znalezienie nowej ścieżki
            self.enemy.target_index = 0  # index na początek ścieżki
