from character import Character
from shooter import Shooter

class Enemy(Character):
    def __init__(self, image, cx, cy, speed):
        super().__init__(image, cx, cy, speed)



    def kill_if_dead(self):
        if self.lives <= 0:
            self.kill()

    def update(self, player_pos):
        pass
