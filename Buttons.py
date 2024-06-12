import pygame

class Button:
    def __init__(self, text, color, hover_color, width, height, x, y, font_size, font_name):
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font_name = font_name
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.x + (self.width - self.text_surface.get_width()) // 2,
                                        self.y + (self.height - self.text_surface.get_height()) // 2))
