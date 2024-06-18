import math

from character import Character


class Enemy(Character):
    def __init__(self, image, cx, cy, speed):
        super().__init__(image, cx, cy, speed)

    def kill_if_dead(self):
        if self.lives <= 0:
            self.kill()

    def move_towards_target(self, target_pos):
        target_x, target_y = target_pos
        direction_x = target_x - self.rect.x
        direction_y = target_y - self.rect.y
        distance = math.hypot(direction_x, direction_y) or 1
        direction_x /= distance
        direction_y /= distance

        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

    def update(self, player_pos):
        pass
