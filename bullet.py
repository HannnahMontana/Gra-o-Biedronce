import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy, movement_x, movement_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.movement_x = movement_x
        self.movement_y = movement_y

    def update(self):
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y
