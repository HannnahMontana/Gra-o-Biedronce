import pygame, random
from level import Level

class Boost_level(Level):
    def __init__(self, player, images, entry_door_direction=None):
        super().__init__(player, images, entry_door_direction)

        self.obstacles = [
        ]

        player.level = self
