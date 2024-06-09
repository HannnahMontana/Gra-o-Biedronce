import pygame
from settings import OFFSET_CORRECTION


class Character(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.speed = speed
        self.lives = 3
        self.level = None

    def draw(self, surface):
        """
        Rysuje postać na ekranie
        :param surface:
        :return:
        """
        # todo: dodać obliczanie offsetu gdzieś indziej. Najlepiej do klasy Level
        offset_x = surface.get_width() // 2 - self.level.current_room.rect.centerx - OFFSET_CORRECTION
        offset_y = surface.get_height() // 2 - self.level.current_room.rect.centery - OFFSET_CORRECTION

        new_rect = self.rect.move(offset_x, offset_y)

        surface.blit(self.image, new_rect)

    def take_damage(self, amount):
        self.lives -= amount
