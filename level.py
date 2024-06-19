import pygame, sys, random

from settings import HEIGHT, WIDTH, GRID_SIZE


class Level:
    """
    Klasa reprezentująca poziom gry.

    Atrybuty:
    player (Player): Obiekt gracza na poziomie.
    set_of_bullets (pygame.sprite.Group): Grupa pocisków na poziomie.
    enemies (pygame.sprite.Group): Grupa przeciwników na poziomie.
    obstacles (None): Przeszkody na poziomie (na razie brak implementacji).
    images (dict): Słownik zawierający obrazy używane w grze.
    entry_door_direction (str or None): Kierunek, z którego gracz wszedł na poziom (opcjonalnie).
    closed_doors (list): Lista zamkniętych drzwi na poziomie.
    width (int): Szerokość poziomu w jednostkach siatki.
    height (int): Wysokość poziomu w jednostkach siatki.
    grid (list): Dwuwymiarowa lista reprezentująca siatkę gry.
    walls (list): Lista prostokątów reprezentujących ściany na poziomie.
    doors (list): Lista prostokątów reprezentujących drzwi na poziomie.
    door_player_enter (pygame.Rect): Drzwi, przez które gracz wszedł na poziom.
    doors_to_open (list): Lista drzwi, które należy otworzyć na poziomie.
    player_invulnerable (bool): Określa, czy gracz jest nietykalny.
    invulnerable_start_time (int): Czas rozpoczęcia nietykalności gracza.
    """

    level_count = 0

    def __init__(self, player, images, entry_door_direction=None):
        """
        Inicjalizacja poziomu gry.

        Args:
        player (Player): Obiekt gracza.
        images (dict): Słownik obrazów używanych w grze.
        entry_door_direction (str or None): Kierunek, z którego gracz wszedł na poziom (opcjonalnie).
        """
        self.player = player
        self.set_of_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.obstacles = None
        self.images = images
        self.entry_door_direction = entry_door_direction
        self.closed_doors = []

        # Siatka gry
        self.width = WIDTH // GRID_SIZE
        self.height = HEIGHT // GRID_SIZE
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # Obiekty statyczne na mapie
        self.walls = [
            pygame.Rect(0, 0, 675, 80),
            pygame.Rect(880, 0, 550, 80),
            pygame.Rect(0, 658, 675, 80),
            pygame.Rect(870, 658, 550, 80),
            pygame.Rect(1270, 0, 100, 250),
            pygame.Rect(1270, 420, 100, 350),
            pygame.Rect(0, 0, 90, 250),
            pygame.Rect(0, 420, 90, 350)
        ]

        # Drzwi do różnych sekcji mapy
        self.doors = [
            pygame.Rect(720, 0, 170, 80),  # Górne drzwi
            pygame.Rect(720, 658, 170, 80),  # Dolne drzwi
            pygame.Rect(1270, 280, 100, 130),  # Prawe drzwi
            pygame.Rect(0, 277, 90, 120)  # Lewe drzwi
        ]

        # Drzwi, przez które gracz wchodzi na poziom
        _opposite_door_index = {'up': 1, 'down': 0, 'right': 3, 'left': 2}
        self.door_player_enter = self.doors[_opposite_door_index.get(entry_door_direction, -1)]
        self.doors_to_open = self._get_random_doors()

        # Parametry invulnerability gracza
        self.player_invulnerable = False
        self.invulnerable_start_time = 0

    def update_grid(self):
        """
        Aktualizuje siatkę gry na podstawie obecnych przeszkód i ścian.
        """
        for obstacle in self.obstacles + self.walls:
            top = max((obstacle.top // GRID_SIZE) - 1, 0)
            bottom = min((obstacle.bottom // GRID_SIZE) + 1, len(self.grid))
            left = max((obstacle.left // GRID_SIZE) - 1, 0)
            right = min((obstacle.right // GRID_SIZE) + 1, len(self.grid[0]))

            for i in range(top, bottom):
                for j in range(left, right):
                    self.grid[i][j] = 1

    def _get_random_doors(self):
        """
        Zwraca listę 1 lub 2 losowych drzwi, poza tymi, przez które wszedł gracz.
        """
        num_doors_to_open = random.randint(1, 2)
        available_doors = [door for door in self.doors if door != self.door_player_enter]
        return random.sample(available_doors, num_doors_to_open)

    def update(self):
        """
        Aktualizuje wszystkie elementy na poziomie gry.
        """
        self.set_of_bullets.update()
        self.enemies.update(self.player.rect.center)

        # Usuwa pociski, które opuściły ekran
        for b in self.set_of_bullets:
            if b.rect.bottom < 0 or b.rect.top > HEIGHT or b.rect.left > WIDTH or b.rect.right < 0:
                b.kill()

        # Kolizje pocisków z wrogami
        for enemy in self.enemies:
            collisions = pygame.sprite.spritecollide(enemy, self.set_of_bullets, False)
            for bullet in collisions:
                if bullet.owner == self.player:
                    bullet.kill()
                    enemy.take_damage(1)
                    enemy.kill_if_dead()

        # Kolizje pocisków z przeszkodami (ścianami i drzwiami)
        all_collidables = self.obstacles + self.walls + self.doors
        for bullet in self.set_of_bullets:
            for collidable in all_collidables:
                if collidable.colliderect(bullet.rect):
                    bullet.kill()
                    break

        # Kolizje pocisków z graczem
        if not self.player.invulnerable:
            collisions = pygame.sprite.spritecollide(self.player, self.set_of_bullets, False)
            for bullet in collisions:
                if bullet.owner != self.player:
                    bullet.kill()
                    self.player.take_damage(1)

        # Kolizje gracza z wrogami i odpychanie
        collisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in collisions:
            self.player.take_damage(1)
            self.player.push(self.player, enemy, all_collidables)
            self.player.push(enemy, self.player)

        # Otwiera drzwi po pokonaniu wszystkich wrogów
        if self.closed_doors and not self.enemies:
            self.closed_doors = [door for door in self.doors if door not in self.doors_to_open]

        # Ustawia granice ekranu dla gracza
        if self.enemies:
            if self.player.rect.top < 5:
                self.player.rect.top = 5
            if self.player.rect.bottom > HEIGHT - 5:
                self.player.rect.bottom = HEIGHT - 5
            if self.player.rect.left < 5:
                self.player.rect.left = 5
            if self.player.rect.right > WIDTH - 5:
                self.player.rect.right = WIDTH - 5

    def draw(self, surface):
        """
        Rysuje wszystkie elementy poziomu na powierzchni.

        Args:
        surface (pygame.Surface): Powierzchnia, na której mają być rysowane elementy.
        """
        self.set_of_bullets.draw(surface)
        self.enemies.draw(surface)

        # Rysuje zamknięte drzwi
        if self.closed_doors:
            for door in self.closed_doors:
                surface.blit(self.images['OBSTACLE4'], door)

        # Rysuje serca reprezentujące życia gracza
        for i in range(self.player.lives - 1):
            surface.blit(self.images['HEART'], (20 + i * 45, 20))

        # Rysuje aktualny boost gracza
        if self.player.boostType is not None:
            surface.blit(self.images[self.player.boostType], (1300, 20))

    def reset(self, direction=None):
        """
        Resetuje poziom gry.

        Args:
        direction (str or None): Kierunek, z którego gracz powinien wejść na poziom (opcjonalnie).
        """
        self.__init__(self.player, self.images, entry_door_direction=direction)

    def trigger_doors(self):
        """
        Zamyka wszystkie drzwi na poziomie.
        """
        self.closed_doors = self.doors
