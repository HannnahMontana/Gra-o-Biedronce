import pygame, sys, random
from settings import HEIGHT, WIDTH, GRID_SIZE


class Level:
    def __init__(self, player, images, entry_door_direction=None):
        self.player = player
        self.set_of_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.obstacles = None
        self.images = images
        self.entry_door_direction = entry_door_direction
        self.closed_doors = []


        self.walls = [
            # szerokość ściany - 550 albo 250, przejście - 266 na poziomie i 240 na pionie
            # placeholder (left, top, width, height)
            # góra
            pygame.Rect(0, 0, 550, 75),
            pygame.Rect(816, 0, 550, 75),
            # dol
            pygame.Rect(0, 665, 550, 75),
            pygame.Rect(816, 665, 550, 75),
            # prawo
            pygame.Rect(1294, 0, 75, 250),
            pygame.Rect(1294, 490, 75, 250),
            # lewo
            pygame.Rect(0, 0, 75, 250),
            pygame.Rect(0, 490, 75, 250)
        ]

        self.doors = [
            pygame.Rect(550, 0, 266, 75),  # Top door
            pygame.Rect(550, 665, 266, 75),  # Bottom door
            pygame.Rect(1294, 250, 75, 240),  # Right door
            pygame.Rect(0, 250, 75, 240)  # Left door
        ]

        # drzwi przeciwne do tych z ktorych przychodzimy
        _opposite_door_index = {'up': 1, 'down': 0, 'right': 3, 'left': 2}
        self.door_player_enter = self.doors[_opposite_door_index.get(entry_door_direction, -1)]
        # self.doors_to_open = self._get_random_doors()
        self.doors_to_open = self.doors[1]

        self.width = WIDTH // GRID_SIZE
        self.height = HEIGHT // GRID_SIZE
        print(f"width: {self.width} height: {self.height}")

        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for row in self.grid:
            print(row)

        self.player_invulnerable = False
        self.invulnerable_start_time = 0

    # todo: wrogowie mogą przechodzić przez siatkę - do poprawy
    def update_grid(self):
        # for obstacle in self.obstacles:
        #     for i in range(obstacle.top // GRID_SIZE, (obstacle.bottom // GRID_SIZE)):
        #         for j in range(obstacle.left // GRID_SIZE, (obstacle.right // GRID_SIZE)):
        #             self.grid[i][j] = 1
        #
        # print("Updated grid:")
        # for row in self.grid:
        #     print(row)

        for obstacle in self.obstacles:
            # oblicza zakresy iteracji dodając komórki wokół przeszkód
            top = max((obstacle.top // GRID_SIZE) - 1, 0)
            bottom = min((obstacle.bottom // GRID_SIZE) + 1, len(self.grid))
            left = max((obstacle.left // GRID_SIZE) - 1, 0)
            right = min((obstacle.right // GRID_SIZE) + 1, len(self.grid[0]))

            # zaznacza obszar zajmowany przez przeszkodę (+ komórki dookoła)
            for i in range(top, bottom):
                for j in range(left, right):
                    self.grid[i][j] = 1

        print("Updated grid:")
        for row in self.grid:
            print(row)

    def _get_random_doors(self):
        """
        Zwraca listę 1 lub 2 losowych drzwi, poza tymi z których wyszedł gracz.
        :return:
        """
        num_doors_to_open = random.randint(1, 2)
        available_doors = [door for door in self.doors if door != self.door_player_enter]
        return random.sample(available_doors, num_doors_to_open)

    def update(self):
        """
        Aktualizuje rzeczy widoczne na ekranie w grze
        :return:
        """
        self.set_of_bullets.update()
        self.enemies.update(self.player.rect.center)

        # Usuwanie pocisków znajdujących się poza ekranem
        for b in self.set_of_bullets:
            if b.rect.bottom < 0 or b.rect.top > HEIGHT or b.rect.left > WIDTH or b.rect.right < 0:
                b.kill()

        # todo: trzeba to na pewno skrócić i uprościć - kolizje
        # Kolizja pocisków z wrogami
        for enemy in self.enemies:
            collisions = pygame.sprite.spritecollide(enemy, self.set_of_bullets, False)
            for bullet in collisions:
                if bullet.owner == self.player:
                    bullet.kill()
                    enemy.take_damage(1)
                    enemy.kill_if_dead()

        # kolizje pocisków i ścian, przeszkód, drzwi
        all_collidables = self.obstacles + self.walls + self.doors
        for bullet in self.set_of_bullets:
            for collidable in all_collidables:
                if collidable.colliderect(bullet.rect):
                    bullet.kill()
                    break

        # Kolizja pocisków z graczem
        if not self.player.invulnerable:
            collisions = pygame.sprite.spritecollide(self.player, self.set_of_bullets, False)
            for bullet in collisions:
                if bullet.owner != self.player:
                    bullet.kill()
                    self.player.take_damage(1)

        # Obsługa kolizji gracza z wrogiem i odpychanie
        collisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in collisions:
            self.player.take_damage(1)
            self.player.push(self.player, enemy, all_collidables)
            self.player.push(enemy, self.player, all_collidables, self.enemies)

        for enemy in self.enemies:
            for other_enemy in self.enemies:
                if enemy != other_enemy and enemy.rect.colliderect(other_enemy.rect):
                    self.player.push(enemy, other_enemy, self.obstacles, self.enemies)

        # otwiera drzwi gdy zabijemy wszystkich enemies
        if self.closed_doors and not self.enemies:
            self.closed_doors = [door for door in self.doors if door not in self.doors_to_open]

        if self.enemies:
            if self.player.rect.top < 5:
                self.player.rect.top = 5
            if self.player.rect.bottom > HEIGHT-5:
                self.player.rect.bottom = HEIGHT -5
            if self.player.rect.left < 5:
                self.player.rect.left = 5
            if self.player.rect.right > WIDTH-5:
                self.player.rect.right = WIDTH-5



    def draw(self, surface):
        """
        Rysuje elementy poziomu
        :param surface:
        :return:
        """
        self.set_of_bullets.draw(surface)
        self.enemies.draw(surface)

        for wall in self.walls:
            pygame.draw.rect(surface, (0, 0, 0), wall)

        # rysuje zamknięte drzwi
        if self.closed_doors:
            for door in self.closed_doors:
                pygame.draw.rect(surface, (139, 69, 19), door)

        # rysowanie żyć
        for i in range(self.player.lives - 1):
            surface.blit(self.images['PLAYERLIFE'], (20 + i * 45, 20))

    def reset(self, direction=None):
        """
        Resetuje poziom (np. po przejściu przez krawędź ekranu)
        :param direction:
        :return:
        """
        # Resetowanie poziomu (np. po przejściu przez krawędź ekranu)
        self.__init__(self.player, self.images, entry_door_direction=direction)
        print(self.entry_door_direction)

    def trigger_doors(self):
        """
        Zamyka wszystkie drzwi
        :return:
        """
        # Zamknięcie drzwi wszystkich
        self.closed_doors = self.doors
        # self.update_grid()  # Zaktualizuj siatkę po zamknięciu drzwi
