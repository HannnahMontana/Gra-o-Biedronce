import pygame, random

from ladybug import Ladybug
from level import Level
from grandma import Grandma
from hobo import Hobo
from student import Student


# todo: stworzyc kilka wzorów pokojów
# todo: oczywiście musimy to przenieść do jakiegoś innego plikuw
# chwilowo tutaj mamy pozycje w ktorych mogą się znajdować enemies (przypadkowe)


# todo: nie wiem czy ta klasa ma sens, żeby była, można przenieść coś z klasy Level tutaj
class Level_1(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        # todo: zamianic to w dict
        self.plan = random.choice([1, 2, 3, 4])
        if self.plan == 1:
            self.obstacles = [
                pygame.Rect(300, 250, 100, 100),
                pygame.Rect(300, 350, 100, 100),
                pygame.Rect(400, 350, 100, 100),
                pygame.Rect(1000, 250, 100, 100),
                pygame.Rect(1000, 350, 100, 80),
                pygame.Rect(695, 450, 100, 80),
                pygame.Rect(695, 350, 100, 80),
                pygame.Rect(900, 350, 100, 80),

            ]

            self.enemies_locations = [
                (188, 153),
                (1194, 153),
                (295, 518),
                (1169, 518),
                (528, 300),
            ]

        elif self.plan == 2:
            self.obstacles = [
                pygame.Rect(119, 102, 100, 100),
                pygame.Rect(119, 550, 100, 100),
                pygame.Rect(1150, 100, 100, 100),
                pygame.Rect(1150, 550, 100, 100),
                pygame.Rect(868, 300, 100, 100),
                pygame.Rect(468, 300, 100, 100),
                pygame.Rect(568, 300, 100, 100),
                pygame.Rect(668, 300, 100, 100),
                pygame.Rect(768, 300, 100, 100),
            ]

            self.enemies_locations = [
                (344, 201),
                (350, 531),
                (1009, 215),
                (1009, 204)
            ]
        elif self.plan == 3:
            self.obstacles = [
                pygame.Rect(250, 136, 100, 100),
                pygame.Rect(250, 236, 100, 100),
                pygame.Rect(250, 336, 100, 100),
                pygame.Rect(527, 336, 100, 100),
                pygame.Rect(527, 436, 100, 100),
                pygame.Rect(923, 136, 100, 100),
                pygame.Rect(923, 236, 100, 100),
                pygame.Rect(1023, 336, 100, 100),
                pygame.Rect(923, 336, 100, 100),

            ]

            self.enemies_locations = [
                (1126, 137),
                (450, 360),
                (696, 344),
            ]
        else:
            self.obstacles = [

                pygame.Rect(210, 250, 100, 90),
                pygame.Rect(310, 350, 100, 90),
                pygame.Rect(410, 450, 100, 90),
                pygame.Rect(510, 350, 100, 90),
                pygame.Rect(310, 250, 100, 90),
                pygame.Rect(410, 350, 100, 90),

                pygame.Rect(915, 220, 100, 90),

                pygame.Rect(915, 420, 100, 90),
                pygame.Rect(1150, 150, 100, 90),
                pygame.Rect(1050, 150, 100, 90),
                pygame.Rect(915, 320, 100, 90),
            ]

            self.enemies_locations = [
                (461, 188),
                (907, 516),
                (678, 400),
                (200, 500),
                (1100, 350)
            ]

        # dl75-1291 wys75-665 zakres

        # Słownik mapujący nazwy typów wrogów do ich klas
        enemy_types = {
            'GRANDMA': Grandma,
            'LADYBUG': Ladybug,
            'HOBO': Hobo,
            # 'STUDENT': Student
        }

        self.update_grid()

        # Tworzenie wrogów losowo
        for (x, y) in self.enemies_locations:
            # losowanie czy na danej pozycji może się znaleźć wrog
            has_enemy = random.choice([True, True, False])
            # jesli na danej pozycji zostalo wylosowane ze bedzie wrog to go dodajemy
            if has_enemy:
                # losowanie rodzaju wroga
                # enemy_type = random.choice(list(enemy_types.keys()))
                enemy_type = 'GRANDMA'
                enemy_images = [self.images[key] for key in self.images if key.startswith(enemy_type)]
                enemy_bullet = self.images.get(f'BULLET_{enemy_type}', None)
                # tworzenie nowego obiektu wroga
                if enemy_bullet:
                    enemy = enemy_types[enemy_type](enemy_images, enemy_bullet, x, y)
                else:
                    enemy = enemy_types[enemy_type](enemy_images, x, y)
                enemy.level = self  # Przypisujemy obecny level do wroga
                self.enemies.add(enemy)  # dodaj wroga do grupy wrogów w levelu

        player.level = self

    def draw(self, surface):

        """
        Rysuje elementy dla poziomu 1
        :param surface:
        :return:
        """

        # rysowanie przeszkód
        for obstacle in self.obstacles:
            surface.blit(self.images['METEORBROWN_BIG1'], obstacle.topleft)

        super().draw(surface)
