import pygame, os, random, sys
from settings import SIZESCREEN, FPS
from player import Player
from utils import load_images
from level_1 import Level_1


def main():
    pygame.init()

    screen = pygame.display.set_mode(SIZESCREEN)
    clock = pygame.time.Clock()

    # ścieżka do obrazów
    path = os.path.join(os.getcwd(), 'images')

    # ładowanie obrazów
    images = load_images(path)
    background = images.pop('BACKGROUND')

    # tworzenie obiektu gracza
    player = Player(images['PLAYER'], 100, 100, images['METEORBROWN_SMALL1'])
    # aktualizacja levelu
    current_level = Level_1(player)
    player.level = current_level

    # pętla gry
    window_open = True
    while window_open:
        # tło
        screen.blit(background, (-300, -300))

        # pętla zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_open = False
            if event.type == pygame.QUIT:
                window_open = False

        # rysowanie i aktualizacja obiektów
        player.update(pygame.key.get_pressed())
        current_level.update()
        current_level.draw(screen)
        player.draw(screen)

        # aktualizacja okna co ileś FPS
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
