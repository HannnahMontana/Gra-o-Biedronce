
import pygame, sys

from settings import HEIGHT, WIDTH


class Level:
    def __init__(self, player, images):
        self.player = player
        self.set_of_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.images = images

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

        # Kolizja pocisków z wrogami
        for enemy in self.enemies:
            collisions = pygame.sprite.spritecollide(enemy, self.set_of_bullets, False)
            for bullet in collisions:
                if bullet.owner == self.player:
                    bullet.kill()
                    enemy.take_damage(1)
                    enemy.kill_if_dead()



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

    def draw(self, surface):
        """
        Rysuje na ekranie rzeczy dla levelu
        :param surface:
        :return:
        """
        self.set_of_bullets.draw(surface)
        self.enemies.draw(surface)

        # rysowanie żyć
        for i in range(self.player.lives - 1):
            surface.blit(self.images['PLAYERLIFE'], (20 + i * 45, 20))
