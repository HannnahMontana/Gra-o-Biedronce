import pygame


class Level:
    def __init__(self, player):
        self.player = player
        self.set_of_bullets = pygame.sprite.Group()

    def update(self):
        self.set_of_bullets.update()

        # Usuwanie pocisków znajdujących się poza ekranem
        for b in self.set_of_bullets:
            if b.rect.bottom < 0:
                b.kill()

    def draw(self, surface):
        self.set_of_bullets.draw(surface)
        # Rysowanie żyć gracza
        # for i in range(self.player.lives - 1):
        #     surface.blit(IMAGES['PLAYERLIFE'], (20 + i * 45, 20))
