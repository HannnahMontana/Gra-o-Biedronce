import pygame, os, sys
from settings import SIZESCREEN, FPS, HEIGHT, WIDTH
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

    # tworzenie obiektu gracz
    player = Player(images['PLAYER'], 683, 360, images['METEORBROWN_SMALL1'])

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

        # sprawdzanie przejścia przez krawędzie ekranu
        if player.rect.bottom >= HEIGHT:
            player.rect.top = 0
            current_level.reset('down')
        elif player.rect.top <= 0:
            player.rect.bottom = HEIGHT
            current_level.reset('up')
        elif player.rect.right > WIDTH:
            player.rect.left = 0
            current_level.reset('right')
        elif player.rect.left < 0:
            player.rect.right = WIDTH
            current_level.reset('left')


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
