import os
import pygame


def load_images(path):
    """
    Ładuje wszystkie obrazy z podanej ścieżki i zwraca je w słowniku.

    :param path: Ścieżka do katalogu zawierającego obrazy.
    :return: Słownik, gdzie klucze to nazwy obrazów (bez rozszerzenia, wielkie litery),
             a wartości to obiekty pygame.Surface.
    """
    file_names = os.listdir(path)
    images = {}

    for file_name in file_names:
        # Usunięcie rozszerzenia i konwersja na wielkie litery
        image_name = file_name[:-4].upper()
        # Ładowanie obrazu z pełną ścieżką do pliku i konwersja na format z przezroczystością
        images[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha()

    return images
