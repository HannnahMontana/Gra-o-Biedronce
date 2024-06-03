from enemy import Enemy
from shooter import Shooter


class Grandma(Enemy, Shooter):
    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, 1000, 5)

    def update(self, player_pos):
        """
        Aktualizuje babcię, która nas śledzi i rzuca w nas pomarańczami
        :param player_pos:
        :return:
        """
        # AI babci -  porusza sie w naszym kierunku
        player_x, player_y = player_pos
        # obliczanie odleglosci w danym kierunku (wektor odleglosci)
        direction_x = player_x - self.rect.x
        direction_y = player_y - self.rect.y
        # obliczanie odległości babci od gracza twierdzeniem Pitagorasa
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        # normalizacja wektora kierunku (zeby przesuwac babcie w naszym kierunku ze stala predkoscia)
        if distance == 0:
            distance = 1
        direction_x /= distance
        direction_y /= distance

        # ruch w kierunku gracza
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

        # strzelanie
        self.shoot(self.rect.center, direction_x, direction_y)
