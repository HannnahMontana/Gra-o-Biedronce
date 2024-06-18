import pygame
from text import Text


class Button:
    def __init__(self, text, text_color, background_color, width, height,
                 pc_x, pc_y, font_size=36, font_type=None):
        self.background_color = background_color
        self.width = width
        self.height = height
        self.text = Text(text, text_color, pc_x, pc_y, font_size, font_type)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.text.rect.center

    def draw(self, surface):
        surface.fill(self.background_color, self.rect)
        self.text.update()
        self.text.draw(surface)