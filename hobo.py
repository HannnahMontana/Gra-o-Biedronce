import math, pygame, random
from enemy import Enemy
from shooter import Shooter
from bullet import Bullet

class Hobo(Enemy, Shooter):

    def __init__(self, image, bullet_img, cx, cy, speed):
        Enemy.__init__(self, image, cx, cy, speed)
        Shooter.__init__(self, bullet_img, 2000, 5)
        self.lives = 5


        # aspekty spraiające że ma się kręcić

        self.angle = random.choice([0, 10, 5])       #początkowy kąt
        self.circle_radius = random.choice([7.5, 5, 2.5])  # promień okręgu lsoowo z zakresu
        self.circle_speed = random.choice([0.10, 0.15, 0.075])  # prędkość obrotu
        self.circle_direction = random.choice([1, -1])# Wybieranie losowego kierunku obrotu

        self.bullet_lifetime = 1000  # Czas życia pocisków w milisekundach
        self.shooting_distance = 500  # Maksymalna odległość od gracza, przy której Hobo strzela

        self.vx = 0
        self.vy = 0
    def update(self, player_pos):

        # AI Hobo - porusza się w naszym kierunku
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
        self.angle += self.circle_speed * self.circle_direction
        orbit_x = math.cos(self.angle) * self.circle_radius
        orbit_y = math.sin(self.angle) * self.circle_radius

        self.rect.x += orbit_x
        self.rect.y += orbit_y

        # strzelanie jeśli jest  wystarczająco blisko
        if distance <= self.shooting_distance:
            self.shoot(self.rect.center, direction_x, direction_y, self)

        # Aktualizacja pocisków Hobo

        for bullet in self.level.set_of_bullets:
            if hasattr(bullet, 'hobo_bullet'): #sprawdza kto strzelił
                current_time = pygame.time.get_ticks()
                if current_time - bullet.spawn_time > self.bullet_lifetime:
                    bullet.kill()  # Usunięcie pocisku, jeśli czas życia upłynął


#przyrwa metodę shoot by był unikalny strzał
    def shoot(self, position, direction_x, direction_y, owner):
        """
        Specjalny sposób strzału Hobo: trzy pociski jednocześnie na krótki dystans.
        :param owner:
        :param position:
        :param direction_x:
        :param direction_y:
        :return:
        """
        # sprawdza aktualny czas
        current_time = pygame.time.get_ticks()
        # strzela tylko kiedy upłynie odpowiednia ilość ms (delay)
        if current_time - self.last_shoot_time >= self.shoot_delay:
            self.last_shoot_time = current_time  # aktualizacja czasu ostatniego wystrzału

            # kąt rozproszenia pocisków
            spread_angle = 15  # kąt rozproszenia w stopniach
            radians = math.radians(spread_angle)

            # tworzenie trzech pocisków z różnymi kątami
            for angle in [-radians, 0, radians]: #Ta linijka uruchamia pętle 3 razy że każdy pocisk będzie pod kątem radians, 0 i -radians
                # Obliczenie nowych kierunków dla każdego pocisku
                new_direction_x = direction_x * math.cos(angle) - direction_y * math.sin(angle)
                new_direction_y = direction_x * math.sin(angle) + direction_y * math.cos(angle)
                # te linijki sprawiają że się rozchodzą, oblicza kierunki
                bullet = Bullet(self.bullet_img, position[0], position[1], new_direction_x * self.bullet_speed,
                                new_direction_y * self.bullet_speed, owner)
                #tworzy pocisk o określonym obrazie, pozycji, kierunku, szybkości i właścicelu

                bullet.spawn_time = pygame.time.get_ticks() #mirzy czas ile istnieje pocisk
                bullet.hobo_bullet = True  # oznaczenie pocisku jako pocisku Hobo
                self.level.set_of_bullets.add(bullet)