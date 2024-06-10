import pygame, sys, random

from settings import HEIGHT, WIDTH


class Level:
    def __init__(self, player, images, entry_door=None):
        self.player = player
        self.set_of_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.obstacles = None
        self.images = images
        self.doors_closed = False  # Stan drzwi(są otawrte bo się zamkną jak przjdziemy przez granicę)
        self.entry_door = entry_door
        # self.opened_doors = []

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
            pygame.Rect(550, 75, 266, 10),  # Top door
            pygame.Rect(550, 665, 266, 10),  # Bottom door
            pygame.Rect(1294, 250, 10, 240),  # Right door
            pygame.Rect(0, 250, 10, 240)  # Left door
        ]

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
        collisions = pygame.sprite.spritecollide(self.player, self.set_of_bullets, False)
        for bullet in collisions:
            if bullet.owner != self.player:
                bullet.kill()
                self.player.take_damage(1)

        # Kolizja player z enemy (do poprawy)
        collisions = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in collisions:
            self.player.take_damage(1)

        # otwiera drzwi jak kill all
        if self.doors_closed and not self.enemies:
            self.doors_closed = False

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

        if self.doors_closed:
            for door in self.doors:
                pygame.draw.rect(surface, (139, 69, 19), door)

        # rysowanie żyć
        for i in range(self.player.lives - 1):
            surface.blit(self.images['PLAYERLIFE'], (20 + i * 45, 20))

    def reset(self, direction):
        # Resetowanie poziomu (np. po przejściu przez krawędź ekranu)
        self.__init__(self.player, self.images, entry_door=direction)
        print(self.entry_door)

    def trigger_doors(self):
        # Zamknięcie drzwi
        self.doors_closed = True
