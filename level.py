import pygame
from settings import HEIGHT, WIDTH


class Level:
    def __init__(self, player, grandma):
        self.player = player
        self.set_of_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        grandma.level = self
        player.level = self

        self.enemies.add(grandma)   # dodaj babcię do grupy wrogów w levelu

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

    def draw(self, surface):
        """
        Rysuje na ekranie rzeczy dla levelu
        :param surface:
        :return:
        """
        self.set_of_bullets.draw(surface)
        self.enemies.draw(surface)

