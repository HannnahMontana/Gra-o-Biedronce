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
        # todo: wartość 50 - korekcja offset. Czemu akurat 50?
        offset_x = surface.get_width() // 2 - self.level.current_room.rect.centerx - 50
        offset_y = surface.get_height() // 2 - self.level.current_room.rect.centery - 50

        new_rect = self.rect.move(offset_x, offset_y)

        surface.blit(self.image, new_rect)

    def take_damage(self, amount):
        self.lives -= amount
