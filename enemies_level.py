import pygame, random

from ladybug import Ladybug
from level import Level
from grandma import Grandma
from hobo import Hobo
from student import Student

# planowanie poziomów
plans = {
    1: {
        'obstacles': [
            pygame.Rect(300, 250, 100, 100),
            pygame.Rect(300, 350, 100, 100),
            pygame.Rect(400, 350, 100, 100),
            pygame.Rect(1000, 250, 100, 100),
            pygame.Rect(1000, 350, 100, 80),
            pygame.Rect(695, 450, 100, 80),
            pygame.Rect(695, 350, 100, 80),
            pygame.Rect(900, 350, 100, 80),
        ],
        'enemies_locations': [
            (188, 153),
            (1194, 153),
            (295, 518),
            (1169, 518),
            (528, 300),
        ]
    },
    2: {
        'obstacles': [
            pygame.Rect(119, 102, 100, 100),
            pygame.Rect(119, 550, 100, 100),
            pygame.Rect(1150, 100, 100, 100),
            pygame.Rect(1150, 550, 100, 100),
            pygame.Rect(868, 300, 100, 100),
            pygame.Rect(468, 300, 100, 100),
            pygame.Rect(568, 300, 100, 100),
            pygame.Rect(668, 300, 100, 100),
            pygame.Rect(768, 300, 100, 100),
        ],
        'enemies_locations': [
            (344, 201),
            (350, 531),
            (1009, 215),
            (1009, 204)
        ]
    },
    3: {
        'obstacles': [
            pygame.Rect(250, 136, 100, 100),
            pygame.Rect(250, 236, 100, 100),
            pygame.Rect(250, 336, 100, 100),
            pygame.Rect(527, 336, 100, 100),
            pygame.Rect(527, 436, 100, 100),
            pygame.Rect(923, 136, 100, 100),
            pygame.Rect(923, 236, 100, 100),
            pygame.Rect(1023, 336, 100, 100),
            pygame.Rect(923, 336, 100, 100),
        ],
        'enemies_locations': [
            (1126, 137),
            (450, 360),
            (696, 344),
        ]
    },
    4: {
        'obstacles': [
            pygame.Rect(210, 240, 100, 90),
            pygame.Rect(310, 340, 100, 90),
            pygame.Rect(410, 440, 100, 90),
            pygame.Rect(510, 340, 100, 90),
            pygame.Rect(310, 240, 100, 90),
            pygame.Rect(410, 340, 100, 90),
            pygame.Rect(915, 220, 100, 90),
            pygame.Rect(915, 420, 100, 90),
            pygame.Rect(1150, 150, 100, 90),
            pygame.Rect(1050, 150, 100, 90),
            pygame.Rect(915, 320, 100, 90),
        ],
        'enemies_locations': [
            (461, 188),
            (907, 516),
            (678, 400),
            (200, 500),
            (1100, 350)
        ]
    },
}


class EnemiesLevel(Level):
    """
    Klasa reprezentująca zwykły poziom z wrogami.

    Metody:
    __init__(self, player, images, entry_door_direction=None):
        Inicjalizacja poziomu.

    draw(self, surface):
        Rysowanie elementów na powierzchni poziomu.
    """

    def __init__(self, player, images, entry_door_direction=None):
        """
        Inicjalizacja poziomu.

        :param player: Obiekt gracza
        :param images: Słownik zawierający obrazy używane w grze
        :param entry_door_direction: Kierunek, z którego gracz wszedł na poziom (opcjonalny)
        """
        super().__init__(player, images, entry_door_direction)

        # słownik mapujący nazwy typów wrogów na ich klasy
        enemy_types = {
            'GRANDMA': Grandma,
            'LADYBUG': Ladybug,
            'HOBO': Hobo,
            'STUDENT': Student
        }

        self.obstacles_with_images = []

        # losowanie planu i ustawienie przeszkód oraz lokalizacji wrogów
        self.plan = random.choice(list(plans.keys()))
        self.obstacles = plans[self.plan]['obstacles']
        self.enemies_locations = plans[self.plan]['enemies_locations']

        # tworzenie listy obrazów przeszkód
        obstacle_images = [images[key] for key in images if key.startswith('OBSTACLE')]

        # przypisanie losowego obrazu do każdej przeszkody
        for obstacle in self.obstacles:
            obstacle_image = random.choice(obstacle_images)
            self.obstacles_with_images.append((obstacle, obstacle_image))

        self.update_grid()

        # tworzenie wrogów losowo na podstawie lokalizacji
        for (x, y) in self.enemies_locations:
            # losowanie czy na danej pozycji będzie wróg
            has_enemy = random.choice([True, True, False])
            if has_enemy:
                # losowanie typu wroga
                enemy_type = random.choice(list(enemy_types.keys()))
                enemy_images = [images[key] for key in images if key.startswith(enemy_type)]
                enemy_bullet = images.get(f'BULLET_{enemy_type}', None)

                # tworzenie obiektu wroga
                if enemy_bullet:
                    enemy = enemy_types[enemy_type](enemy_images, enemy_bullet, x, y)
                else:
                    enemy = enemy_types[enemy_type](enemy_images, x, y)
                enemy.level = self  # przypisanie poziomu do wroga
                self.enemies.add(enemy)  # dodanie wroga do grupy wrogów na poziomie

        player.level = self

    def draw(self, surface):
        """
        Rysowanie elementów na powierzchni poziomu.

        :param surface: Powierzchnia, na której mają być narysowane elementy
        """
        # rysowanie przeszkód
        for obstacle, obstacle_image in self.obstacles_with_images:
            surface.blit(obstacle_image, obstacle.topleft)

        super().draw(surface)  # wywołanie metody draw() z klasy nadrzędnej
