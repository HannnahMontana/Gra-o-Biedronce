from character import Character


class Enemy(Character):
    def __init__(self, image, cx, cy, speed):
        super().__init__(image, cx, cy, speed)
        # tu będą jakieś cechy wspólne wrogów np życie

    def update(self, player_pos):
        pass
