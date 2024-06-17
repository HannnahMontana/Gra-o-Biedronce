import math


from enemy import Enemy
from shooter import Shooter



class PalletTruck(Enemy):
    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, 0, 0)
        self.lives = 1
        self.speed = 15
        self.is_moving = False
        self.direction_x = 0
        self.direction_y = 0
        self.tolerance = 2  # tolerancja dla sprawdzenia osi

        self.rect.center = cx, cy


    def update(self, player_pos):
        """
        Aktualizuje pozycję PalletTruck.
        PalletTruck leci w stronę gracza w linii prostej, gdy ten przetnie jego oś X lub Y, pod warunkiem, że nie ma przeszkody między nimi.
        :param player_pos: Tuple zawierający pozycję gracza (player_x, player_y)
        """
        player_x, player_y = player_pos

        if not self.is_moving:
            # Sprawdź, czy gracz przecina oś X lub Y z tolerancją i czy nie ma przeszkody między nimi
            if abs(self.rect.x - player_x) <= self.tolerance :
                self.is_moving = True
                self.direction_x = 0
                self.direction_y = 1 if player_y > self.rect.y else -1
            elif abs(self.rect.y - player_y) <= self.tolerance:
                self.is_moving = True
                self.direction_x = 1 if player_x > self.rect.x else -1
                self.direction_y = 0

        if self.is_moving:
            # ruch w ustalonym kierunku
            self.rect.x += self.direction_x * self.speed
            self.rect.y += self.direction_y * self.speed

