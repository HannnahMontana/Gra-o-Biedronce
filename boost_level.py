import pygame, random

from ladybug import Ladybug
from level import Level
from settings import HEIGHT, WIDTH
from boost import Boost  # Zakładamy, że mamy klasę Boost


class Boost_level(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        self.boost = self.create_random_boost(images)
        self.obstacles = [
        ]




        player.level = self

    def create_random_boost(self, images):
        """
        Tworzy losowy Boost i umieszcza go na środku pokoju.
        """
        boost_types = ['beer', 'energy_drink', 'scratch_lottery']
        chosen_boost = random.choice(boost_types)
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        return Boost(chosen_boost, center_x, center_y, images)


    def update(self):
        """
        Aktualizuje stan poziomu, w tym sprawdzanie kolizji gracza z boostem.
        """
        super().update()

        # Sprawdzamy kolizję gracza z boostem
        if self.boost and self.player.rect.colliderect(self.boost.rect):
            self.player.apply_boost(self.boost.boost_type)
            self.boost = None  # Usuwamy boost po zebraniu

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

        if self.boost:
            self.boost.draw(surface)




