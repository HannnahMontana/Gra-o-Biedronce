import math
import random

from astar import Astar
from settings import GRID_SIZE


class PathFollower:
    def __init__(self, enemy):
        self.enemy = enemy

    def move_along_path(self, random_goal=False):
        if self.enemy.path and self.enemy.target_index < len(self.enemy.path):
            next_move = self.enemy.path[self.enemy.target_index]  # następny punkt docelowy na ścieżce
            # pozycja docelowa
            target_pos = (next_move[0] * GRID_SIZE, next_move[1] * GRID_SIZE)
            # oblicza wektor
            direction_x, direction_y = target_pos[0] - self.enemy.rect.x, target_pos[1] - self.enemy.rect.y
            # obliczanie odległości babci od gracza twierdzeniem Pitagorasa
            distance = math.hypot(direction_x, direction_y)

            # jeśli odległość jest mniejsza od prędkości, przesuwa na cel
            if distance < self.enemy.speed:
                self.enemy.rect.x, self.enemy.rect.y = target_pos[0], target_pos[1]
                self.enemy.target_index += 1  # następny punkt docelowy
            else:
                self.enemy.move_towards_target(target_pos)  # przesuwa w kierunku celu

        if random_goal:
            # Jeśli dotarł do celu, losuje nowy cel
            if self.enemy.target_index >= len(self.enemy.path):
                self.enemy.random_goal = self.get_random_goal()
                self.enemy.path = None  # resetowanie ścieżki

    def get_random_goal(self):
        """
        Losuje nowy cel, który nie jest przeszkodą
        :return: tuple(int, int) - nowy losowy cel
        """
        while True:
            random_goal = (random.randint(0, self.enemy.level.width - 1), random.randint(0, self.enemy.level.height - 1))
            if self.enemy.level.grid[random_goal[1]][random_goal[0]] != 1:  # Sprawdzenie, czy punkt nie jest przeszkodą
                return random_goal

    def find_path_to_goal(self, goal):
        """
        znajduje ścieżkę do celu, jeśli to konieczne
        :param goal: cel
        :return: None
        """
        astar = Astar(self.enemy.level)  # inicjalizacja algorytmu A*
        start = (self.enemy.rect.x // GRID_SIZE, self.enemy.rect.y // GRID_SIZE)  # aktualna pozycja

        # sprawdzenie, czy ścieżka nie istnieje lub jest inna niż ostatnio znaleziona
        if not self.enemy.path or self.enemy.path[-1] != goal:
            self.enemy.path = astar.find_path(start, goal)  # znalezienie nowej ścieżki
            self.enemy.target_index = 0  # index na początek ścieżki
