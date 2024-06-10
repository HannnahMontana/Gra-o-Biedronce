import pygame, sys

from settings import HEIGHT, WIDTH


class Level:
    def __init__(self, player, images):
        self.player = player
        self.set_of_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.images = images

        self.sciany = [
            pygame.Rect(0, 0, 0, 0),
            pygame.Rect(100, 0, 0, 0),
            pygame.Rect(200, 0, 0, 0),
            pygame.Rect(300, 0, 0, 0),
            pygame.Rect(400, 0, 0, 0),
            pygame.Rect(500, 0, 0, 0),

            pygame.Rect(770, 0, 0, 0),
            pygame.Rect(870, 0, 0, 0),
            pygame.Rect(970, 0, 0, 0),
            pygame.Rect(1070, 0, 0, 0),
            pygame.Rect(1170, 0, 0, 0),
            pygame.Rect(1270, 0, 0, 0),

            pygame.Rect(1275, 100, 0, 0),
            pygame.Rect(1275, 200, 0, 0),

            pygame.Rect(1275, 460, 0, 0),
            pygame.Rect(1275, 560, 0, 0),

            pygame.Rect(1270, 660, 0, 0),
            pygame.Rect(1170, 660, 0, 0),
            pygame.Rect(1070, 660, 0, 0),
            pygame.Rect(970, 660, 0, 0),
            pygame.Rect(870, 660, 0, 0),
            pygame.Rect(770, 660, 0, 0),

            pygame.Rect(0, 660, 0, 0),
            pygame.Rect(100, 660, 0, 0),
            pygame.Rect(200, 660, 0, 0),
            pygame.Rect(300, 660, 0, 0),
            pygame.Rect(400, 660, 0, 0),
            pygame.Rect(500, 660, 0, 0),

            pygame.Rect(0, 100, 0, 0),
            pygame.Rect(0, 200, 0, 0),

            pygame.Rect(0, 460, 0, 0),
            pygame.Rect(0, 560, 0, 0)


        ]

        self.imagesP = pygame.image.load('images-from-shooting-game/meteorBrown_big1.png')


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

        # Kolizja pocisków z przeszkodami
        for obstacle in self.obstacles:
            for bullet in self.set_of_bullets:
                if obstacle.colliderect(bullet.rect):
                    bullet.kill()
        for sciany in self.sciany:
            for bullet in self.set_of_bullets:
                if sciany.colliderect(bullet.rect):
                    bullet.kill()

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



        for sciany in self.sciany:
            surface.blit(self.imagesP, sciany.topleft)

            # rysowanie żyć
        for i in range(self.player.lives - 1):
            surface.blit(self.images['PLAYERLIFE'], (20 + i * 45, 20))

    def reset(self):
            self.__init__(self.player, self.images)