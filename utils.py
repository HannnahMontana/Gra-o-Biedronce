import os
import pygame


def load_images(path):
    """
    Ładuje wszystkie obrazy z podanej ścieżki i zwraca je w słowniku.
    """
    file_names = os.listdir(path)
    images = {}
    for file_name in file_names:
        image_name = file_name[:-4].upper()
        images[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
    return images
