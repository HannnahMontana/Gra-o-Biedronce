import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boss Health Bar Example")

# Health bar dimensions
BAR_WIDTH = 400
BAR_HEIGHT = 30

# Boss health
max_health = 100
current_health = max_health

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_color = BLACK
bullet_speed = 7

# Boss settings
boss_width = 100
boss_height = 100
boss_color = RED

# Player settings
player_width = 50
player_height = 60
player_color = BLACK
player_speed = 5


# Player class
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, player_width, player_height)
        self.color = player_color
        self.speed = player_speed

    def move(self, dx):
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - player_width:
            self.rect.x += dx

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def shoot(self):
        bullet_x = self.rect.centerx - bullet_width // 2
        bullet_y = self.rect.y
        return pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)


# Boss class
class Boss:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, boss_width, boss_height)
        self.max_health = max_health
        self.current_health = max_health

    def draw(self, screen):
        pygame.draw.rect(screen, boss_color, self.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_percentage = self.current_health / self.max_health
        current_bar_width = int(BAR_WIDTH * health_percentage)
        pygame.draw.rect(screen, RED, (200, 10, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, GREEN, (200, 10, current_bar_width, BAR_HEIGHT))


# Main game function
def main():
    clock = pygame.time.Clock()

    player = Player(SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - player_height - 10)
    boss = Boss(SCREEN_WIDTH // 2 - boss_width // 2, 50)
    bullets = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player_speed)
        if keys[pygame.K_RIGHT]:
            player.move(player_speed)
        if keys[pygame.K_SPACE]:
            bullets.append(player.shoot())

        # Move bullets
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.colliderect(boss.rect):
                bullets.remove(bullet)
                boss.current_health = max(0, boss.current_health - 1)

        # Remove off-screen bullets
        bullets[:] = [bullet for bullet in bullets if bullet.y > 0]

        # Clear the screen
        screen.fill(WHITE)

        # Draw the player
        player.draw(screen)

        # Draw the boss
        boss.draw(screen)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.rect(screen, bullet_color, bullet)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)


if __name__ == "__main__":
    main()
