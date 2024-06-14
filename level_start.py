from level import Level

class Level_start(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        self.obstacles = [
        ]

        player.level = self
