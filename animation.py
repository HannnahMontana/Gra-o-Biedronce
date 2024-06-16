import pygame


class Animation:
    def __init__(self, image_paths, scale, delay):
        self.images = [self.load_and_scale_image(path, scale) for path in image_paths]
        self.index = 0
        self.delay = delay
        self.last_update = pygame.time.get_ticks()
        self.current_image = self.images[0]

    @staticmethod
    def load_and_scale_image(path, scale):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (image.get_width() // scale, image.get_height() // scale))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.delay:
            self.last_update = now
            self.index = (self.index + 1) % len(self.images)
            self.current_image = self.images[self.index]
