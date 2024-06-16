import pygame, random

from ladybug import Ladybug
from level import Level
from settings import HEIGHT, WIDTH


class Boost_level(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        self.obstacles = [
        ]
        # Losowanie jednego z trzech boostów
        self.boost_types = ['METEORBROWN_BIG1', 'METEORBROWN_BIG2', 'METEORBROWN_BIG3']
        self.current_boost = random.choice(self.boost_types)
        self.boost_rect = pygame.Rect(WIDTH / 2 - 50, HEIGHT / 2 - 50, 100, 100)
        self.boost_active = True

        player.level = self





    def draw(self, surface):
        """
        Rysuje elementy dla poziomu 1
        :param surface:
        :return:
        """
        super().draw(surface)
        # rysowanie przeszkód
        for obstacle in self.obstacles:
            surface.blit(self.images['METEORBROWN_BIG1'], obstacle.topleft)

        if self.boost_active:
            boost_image = self.images[self.current_boost]
            surface.blit(boost_image, self.boost_rect)

    def update(self):
        self.check_boost_collision()

    def check_boost_collision(self):
        if self.boost_active and self.player.rect.colliderect(self.boost_rect):
            self.player.apply_boost(self.current_boost)
            
            self.boost_active = False