import pygame, sys
from pygame.locals import *
import random, time

# Initializing
pygame.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 3
SCORE = 0
COINS = 0

# Load sound effects
crash_sound = pygame.mixer.Sound("car-crash.mp3")
coin_sound = pygame.mixer.Sound("coin.mp3")

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load Background Image
background = pygame.image.load("AnimatedStreet.png")

# Create a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Racer")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Coin collection system
c1, c2, c3, c4, c5 = False, False, False, False, False

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))

    def move(self):
        global COINS, SPEED
        global c1, c2, c3, c4, c5

        if self.rect.bottom < SCREEN_HEIGHT // 3:
            COINS += 3
        elif self.rect.bottom < SCREEN_HEIGHT // 1.5:
            COINS += 2
        else:
            COINS += 1

        if not c1 and COINS >= 10:
            SPEED += 1
            c1 = True
        if not c2 and COINS >= 20:
            SPEED += 1
            c2 = True
        if not c3 and COINS >= 30:
            SPEED += 1
            c3 = True
        if not c4 and COINS >= 40:
            SPEED += 1
            c4 = True
        if not c5 and COINS >= 50:
            SPEED += 1
            c5 = True

        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)

# Setting up Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins_group = pygame.sprite.Group()
coins_group.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

def handle_crash():
    crash_sound.play()  # Play crash sound
    time.sleep(2)       # Pause after crash

background_y = 0  # Background scrolling position

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Collision detection between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        handle_crash()
        pygame.quit()
        sys.exit()

    # Scroll the background
    background_y = (background_y + SPEED) % background.get_height()
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - background.get_height()))

    # Display scores
    scores = font_small.render(str(SCORE), True, BLACK)
    screen.blit(scores, (10, 10))

    coins = font_small.render(str(COINS), True, BLACK)
    screen.blit(coins, (370, 10))

    # Moves and redraws all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

        if entity == C1:
            if pygame.sprite.spritecollideany(P1, coins_group):
                coin_sound.play()  # Play coin sound
                entity.move()
        else:
            entity.move()

    # Move enemies
    for enemy in enemies:
        enemy.move()

    # Move coins
    for coin in coins_group:
        coin.rect.y += SPEED

        # Respawn coins if they go off-screen
        if coin.rect.top > SCREEN_HEIGHT:
            coin.rect.y = -coin.rect.height
            coin.rect.x = random.randint(40, SCREEN_WIDTH - 40)

    pygame.display.update()
    FramePerSec.tick(FPS)