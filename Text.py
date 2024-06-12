import pygame
class Text:
    def __init__(self, content, color, x, y, font_size=120, font_type="Ink Free"):
        self.content = content
        self.color = color
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.text_surface = self.font.render(self.content, True, self.color)

    def draw(self, screen):
        screen.blit(self.text_surface, (self.x - self.text_surface.get_width() // 2,
                                        self.y - self.text_surface.get_height() // 2))