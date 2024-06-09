import random
from level2 import Level
from room import Room

ROOM_WIDTH = 1266
ROOM_HEIGHT = 640


class Level_1(Level):
    def __init__(self, player, images):
        super().__init__(player, images)
        self.player.level = self

    def generate_dungeon(self):
        """Generuje rozkład sklepu dla poziomu 1."""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        start_x, start_y = 0, 0

        # Dodanie pierwszego pokoju
        self.rooms.append(Room(start_x, start_y, self.images, self.player))

        while len(self.rooms) < 5:
            current_room = random.choice(self.rooms)
            direction = random.choice(directions)
            new_x = current_room.rect.x + direction[0] * (ROOM_WIDTH + 10)
            new_y = current_room.rect.y + direction[1] * (ROOM_HEIGHT + 10)

            # Sprawdzenie kolizji
            new_room = Room(new_x, new_y, self.images, self.player)
            if not any(r.rect.colliderect(new_room.rect) for r in self.rooms):
                if direction == (0, -1):
                    current_room.doors['top'] = True
                    new_room.doors['bottom'] = True
                elif direction == (0, 1):
                    current_room.doors['bottom'] = True
                    new_room.doors['top'] = True
                elif direction == (-1, 0):
                    current_room.doors['left'] = True
                    new_room.doors['right'] = True
                elif direction == (1, 0):
                    current_room.doors['right'] = True
                    new_room.doors['left'] = True

                self.rooms.append(new_room)
