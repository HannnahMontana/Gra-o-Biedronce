import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.speed = speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, player_pos):
        pass
