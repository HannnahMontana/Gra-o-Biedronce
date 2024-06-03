import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.speed = speed

    def draw(self, surface):
        """
        Rysuje postać na ekranie
        :param surface:
        :return:
        """
        surface.blit(self.image, self.rect)
