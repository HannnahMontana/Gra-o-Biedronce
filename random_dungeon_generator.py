import pygame
import random

# Constants
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 740
ROOM_WIDTH = 1266
ROOM_HEIGHT = 640
ROOMS = 5
MINIMAP_SCALE = 0.1
MINIMAP_MARGIN = 10
MINIMAP_SIZE = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Dungeon Generator")


# Room class
class Room:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ROOM_WIDTH, ROOM_HEIGHT)
        self.doors = {'top': False, 'bottom': False, 'left': False, 'right': False}
        self.rectangles = self.generate_rectangles()

    def generate_rectangles(self):
        rectangles = []
        for _ in range(5):
            width = random.randint(20, 50)
            height = random.randint(20, 50)
            rect_x = random.randint(self.rect.x, self.rect.x + ROOM_WIDTH - width)
            rect_y = random.randint(self.rect.y, self.rect.y + ROOM_HEIGHT - height)
            rectangles.append(pygame.Rect(rect_x, rect_y, width, height))
        return rectangles

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.rect(screen, WHITE, self.rect.move(offset_x, offset_y), 2)
        if self.doors['top']:
            pygame.draw.line(screen, WHITE, (self.rect.centerx + offset_x, self.rect.top + offset_y),
                             (self.rect.centerx + offset_x, self.rect.top - 10 + offset_y), 2)
        if self.doors['bottom']:
            pygame.draw.line(screen, WHITE, (self.rect.centerx + offset_x, self.rect.bottom + offset_y),
                             (self.rect.centerx + offset_x, self.rect.bottom + 10 + offset_y), 2)
        if self.doors['left']:
            pygame.draw.line(screen, WHITE, (self.rect.left + offset_x, self.rect.centery + offset_y),
                             (self.rect.left - 10 + offset_x, self.rect.centery + offset_y), 2)
        if self.doors['right']:
            pygame.draw.line(screen, WHITE, (self.rect.right + offset_x, self.rect.centery + offset_y),
                             (self.rect.right + 10 + offset_x, self.rect.centery + offset_y), 2)
        for rect in self.rectangles:
            pygame.draw.rect(screen, WHITE, rect.move(offset_x, offset_y), 2)

    def draw_minimap(self, screen, offset_x, offset_y):
        minimap_rect = pygame.Rect(
            offset_x + self.rect.x * MINIMAP_SCALE,
            offset_y + self.rect.y * MINIMAP_SCALE,
            self.rect.width * MINIMAP_SCALE,
            self.rect.height * MINIMAP_SCALE
        )
        pygame.draw.rect(screen, WHITE, minimap_rect, 2)


# Character class (base class for Player)
class Character:
    def __init__(self, image, cx, cy, speed):
        self.image = image
        self.rect = self.image.get_rect(center=(cx, cy))
        self.speed = speed

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(offset_x, offset_y))


# Shooter class (not used in this version, but included for completeness)
class Shooter:
    def __init__(self, bullet_img, shoot_delay, bullet_speed):
        self.bullet_img = bullet_img
        self.shoot_delay = shoot_delay
        self.bullet_speed = bullet_speed


# Player class
class Player(Character):
    def __init__(self, image, cx, cy):
        super().__init__(image, cx, cy, speed=8)
        self.lives = 5
        self.level = None  # Placeholder for level (used for obstacles)

    def update(self, key_pressed):
        self.handle_movement(key_pressed)

    def _move_and_handle_collision(self, dx, dy):
        self.rect.move_ip(dx, dy)
        if self.level:
            for obstacle in self.level.obstacles:
                if self.rect.colliderect(obstacle):
                    self.rect.move_ip(-dx, -dy)

    def handle_movement(self, key_pressed):
        dx, dy = 0, 0
        if key_pressed[pygame.K_LEFT]:
            dx = -self.speed
        if key_pressed[pygame.K_RIGHT]:
            dx = self.speed
        if key_pressed[pygame.K_UP]:
            dy = -self.speed
        if key_pressed[pygame.K_DOWN]:
            dy = self.speed

        if dx != 0:
            self._move_and_handle_collision(dx, 0)
        if dy != 0:
            self._move_and_handle_collision(0, dy)

    def draw_minimap(self, screen, offset_x, offset_y):
        minimap_rect = pygame.Rect(
            offset_x + self.rect.x * MINIMAP_SCALE,
            offset_y + self.rect.y * MINIMAP_SCALE,
            self.rect.width * MINIMAP_SCALE,
            self.rect.height * MINIMAP_SCALE
        )
        pygame.draw.rect(screen, BLUE, minimap_rect)


# Base Level class
class Level:
    def __init__(self):
        self.rooms = []
        self.obstacles = []

    def generate_dungeon(self):
        raise NotImplementedError("This method should be overridden by subclasses")


# Level_1 class
class Level_1(Level):
    def __init__(self):
        super().__init__()
        self.generate_dungeon()

    def generate_dungeon(self):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        start_x = 0
        start_y = 0

        self.rooms.append(Room(start_x, start_y))

        while len(self.rooms) < ROOMS:
            current_room = random.choice(self.rooms)
            direction = random.choice(directions)
            new_x = current_room.rect.x + direction[0] * (ROOM_WIDTH + 10)
            new_y = current_room.rect.y + direction[1] * (ROOM_HEIGHT + 10)

            new_room = Room(new_x, new_y)
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


# Find the room containing the player
def get_current_room(player, rooms):
    for room in rooms:
        if room.rect.colliderect(player.rect):
            return room
    return None


# Main game loop
def main():
    clock = pygame.time.Clock()
    level = Level_1()
    rooms = level.rooms
    start_room = rooms[0]

    player_image = pygame.Surface((20, 20))
    player_image.fill(RED)
    player = Player(player_image, start_room.rect.centerx, start_room.rect.centery)
    player.level = level  # Set the level for the player to handle collisions

    current_room = start_room
    offset_x = SCREEN_WIDTH // 2 - current_room.rect.centerx
    offset_y = SCREEN_HEIGHT // 2 - current_room.rect.centery
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys)

        new_room = get_current_room(player, rooms)
        if new_room and new_room != current_room:
            current_room = new_room
            offset_x = SCREEN_WIDTH // 2 - current_room.rect.centerx
            offset_y = SCREEN_HEIGHT // 2 - current_room.rect.centery

        screen.fill(BLACK)

        if current_room:
            current_room.draw(screen, offset_x, offset_y)
            player.draw(screen, offset_x, offset_y)

        minimap_center_x = player.rect.centerx * MINIMAP_SCALE
        minimap_center_y = player.rect.centery * MINIMAP_SCALE
        minimap_offset_x = SCREEN_WIDTH - MINIMAP_SIZE - MINIMAP_MARGIN
        minimap_offset_y = MINIMAP_MARGIN

        minimap_view_offset_x = minimap_center_x - MINIMAP_SIZE // 2
        minimap_view_offset_y = minimap_center_y - MINIMAP_SIZE // 2

        for room in rooms:
            room.draw_minimap(screen, minimap_offset_x - minimap_view_offset_x,
                              minimap_offset_y - minimap_view_offset_y)
        player.draw_minimap(screen, minimap_offset_x - minimap_view_offset_x, minimap_offset_y - minimap_view_offset_y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
