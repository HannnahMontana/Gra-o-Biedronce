import pygame



#todo: Ważne!!! pociski wrogów ranią też innych wrogów i mogą się wzajemnie zabijać
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy, movement_x, movement_y, owner):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.movement_x = movement_x
        self.movement_y = movement_y
        self.owner = owner # Rozróżnienie kto strzela
    def update(self):
        """
        Aktualizuje pozycje pocisku w każdej klatce
        :return:
        """
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y


