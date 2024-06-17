import pygame
from utils import load_images
class Boost(pygame.sprite.Sprite):
    def __init__(self, boost_type, x, y, images):
        super().__init__()
        self.images = images
        self.boost_type = boost_type
        self.image = self.load_image(boost_type)
        self.rect = self.image.get_rect(center=(x, y))

    def load_image(self, boost_type):
        """
        Ładuje odpowiedni obrazek dla danego typu boosta.
        """
        if boost_type == 'beer':
            return self.images['BEER']
        elif boost_type == 'energy_drink':
            return self.images['ENERGY_DRINK']
        elif boost_type == 'scratch_lottery':
            return self.images['SCRATCH_LOTTERY']

    def draw(self, surface):
        """
        Rysuje boost na powierzchni.
        """
        surface.blit(self.image, self.rect)