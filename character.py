import pygame


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
        :param offset_y:
        :param offset_x:
        :param surface:
        :return:
        """
        # surface.blit(self.image, self.rect)
        offset_x = surface.get_width() // 2 - self.level.current_room.rect.centerx
        offset_y = surface.get_height() // 2 - self.level.current_room.rect.centery
        surface.blit(self.image, self.rect.move(offset_x, offset_y))

    def take_damage(self, amount):
        self.lives -= amount
