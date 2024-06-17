import math
from enemy import Enemy
from shooter import Shooter

class Ladybug(Enemy, Shooter):
    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, 0, 0)
        self.lives = 1
        self.angle = 0
        self.circle_radius = 3  # promień okręgu
        self.circle_speed = 0.05  # prędkość kątowa

    def update(self, player_pos):
        """
        Aktualizuje Ladybug, który nas śledzi i porusza się po własnej orbicie.
        :param player_pos:
        :return:
        """

        # AI Ladubug - porusza się w naszym kierunku
        player_x, player_y = player_pos
        # obliczanie odległości w danym kierunku (wektor odległości)
        direction_x = player_x - self.rect.x
        direction_y = player_y - self.rect.y
        # obliczanie odległości Hobo od gracza twierdzeniem Pitagorasa
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        # normalizacja wektora kierunku (żeby przesuwać Hobo w naszym kierunku ze stałą prędkością)
        if distance == 0:
            distance = 1
        direction_x /= distance
        direction_y /= distance

        # ruch w kierunku gracza
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

        # dodanie ruchu po własnej orbicie
        self.angle += self.circle_speed
        orbit_x = math.cos(self.angle) * self.circle_radius
        orbit_y = math.sin(self.angle) * self.circle_radius

        self.rect.x += orbit_x
        self.rect.y += orbit_y


