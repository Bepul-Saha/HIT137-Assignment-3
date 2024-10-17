import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Side Scroller Game")

# Asset paths
ASSETS_PATH = r"D:\Asn\assets"

# Load and scale images
PLAYER_SIZE = (80, 80)
ENEMY_SIZE = (80, 80)
PROJECTILE_SIZE = (20, 10)
COLLECTIBLE_SIZE = (40, 40)

player_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_PATH, 'player.png')).convert_alpha(), PLAYER_SIZE
)
enemy_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_PATH, 'enemy.png')).convert_alpha(), ENEMY_SIZE
)
projectile_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_PATH, 'projectile.png')).convert_alpha(), PROJECTILE_SIZE
)
collectible_img = pygame.transform.scale(
    pygame.image.load(os.path.join(ASSETS_PATH, 'collectible.png')).convert_alpha(), COLLECTIBLE_SIZE
)

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height - 50
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -20  # Increased jump power for higher jumps
        self.gravity = 0.8
        self.jumping = False

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.y >= HEIGHT - self.rect.height - 50:
            self.rect.y = HEIGHT - self.rect.height - 50
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.vel_y = self.jump_power
            self.jumping = True

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.reset_position()

    def reset_position(self):
        self.rect.x = WIDTH + random.randint(50, 150)
        self.rect.y = HEIGHT - self.rect.height - 50
        self.speed = random.randint(3, 6)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = projectile_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = collectible_img
        self.rect = self.image.get_rect(center=(x, y))

    def reset_position(self):
        # Spawn collectibles at a height that is reachable by the player's jump
        self.rect.x = random.randint(50, WIDTH - 50)
        self.rect.y = random.randint(HEIGHT // 2, HEIGHT // 2 + 100)  # Adjusted height range for collectibles

# Initialize groups
player = Player()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

# Function to spawn a new enemy
def spawn_enemy():
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)

# Function to spawn a new collectible
def spawn_collectible():
    collectible = Collectible(random.randint(50, WIDTH - 50), random.randint(HEIGHT // 2, HEIGHT // 2 + 100))
    collectibles.add(collectible)
    all_sprites.add(collectible)

# Game variables
score = 0
clock = pygame.time.Clock()
running = True
game_over = False
collectible_timer = pygame.USEREVENT + 1
pygame.time.set_timer(collectible_timer, 5000)  # Spawn collectible every 5 seconds

# Spawn the first enemy
spawn_enemy()

# Main game loop
while running:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == collectible_timer and not game_over:
            spawn_collectible()
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_f:
                projectile = Projectile(player.rect.right, player.rect.centery)
                projectiles.add(projectile)
                all_sprites.add(projectile)

    if not game_over:
        keys = pygame.key.get_pressed()
        player.update(keys)
        enemies.update()
        projectiles.update()

        # Check for projectile and enemy collision
        for projectile in projectiles:
            enemy_hit = pygame.sprite.spritecollideany(projectile, enemies)
            if enemy_hit:
                projectile.kill()
                enemy_hit.reset_position()
                score += 10

        # Check for player and collectible collision
        collectible_hit = pygame.sprite.spritecollideany(player, collectibles)
        if collectible_hit:
            collectible_hit.kill()
            score += 20

        # Check for player and enemy collision
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

    # Drawing on the screen
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

    # Restart game logic
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            score = 0
            player.rect.x, player.rect.y = 50, HEIGHT - player.rect.height - 50
            enemies.empty()
            collectibles.empty()
            projectiles.empty()
            all_sprites.empty()
            all_sprites.add(player)
            spawn_enemy()

# Quit Pygame
pygame.quit()
