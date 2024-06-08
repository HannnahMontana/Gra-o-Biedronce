import pygame, os, sys
from settings import SIZESCREEN, FPS
from player import Player
from utils import load_images
# from level_1 import Level_1
from Level_12 import Level_1


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZESCREEN)
    pygame.display.set_caption("The Binding of Biedronka")
    clock = pygame.time.Clock()

    # ścieżka do obrazów
    path = os.path.join(os.getcwd(), 'images')

    # ładowanie obrazów
    images = load_images(path)
    background = images.pop('BACKGROUND')

    # tworzenie obiektu gracz
    player = Player(images['PLAYER'], 100, 100, images['METEORBROWN_SMALL1'])

    # aktualizacja i tworzenie levelu
    current_level = Level_1(player, images)

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

        # aktualizacja obiektów
        player.update(pygame.key.get_pressed())
        current_level.update()

        # rysowanie
        current_level.draw(screen)
        player.draw(screen)

        # aktualizacja okna co ileś FPS
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
