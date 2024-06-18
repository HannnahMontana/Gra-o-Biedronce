from boss import Boss
from level import Level

boss_location = (783, 370)


class Boss_level(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        self.obstacles = []

        enemy_images = [self.images[key] for key in self.images if key.startswith('WORKER')]
        boss = Boss(enemy_images, self.images['BULLET_GRANDMA'], boss_location[0], boss_location[1], 2)
        boss.level = self  # Przypisujemy obecny level do wroga
        self.enemies.add(boss)  # dodaj bossa do grupy wrogów w levelu

        player.level = self


