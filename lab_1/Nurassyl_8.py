import pygame
import random
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# Экран параметрлері
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# FPS
FPS = 60
clock = pygame.time.Clock()

# Түстер
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Шрифттер
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 40)

# Суреттер
background = pygame.image.load(r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\Road.png").convert_alpha()
player_img = pygame.image.load(r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\Player.png").convert_alpha()
enemy_img = pygame.image.load(r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\Enemy.png").convert_alpha()
coin_img = pygame.image.load(r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (40, 40))

# Дыбыстар
crash_sound = pygame.mixer.Sound(r"C:\Users\Мой док\OneDrive\Desktop\PP2\labs\lab8\image\lab8_img_Lab8_pictures_crash.wav")

# Ойын параметрлері
SPEED = 5
SCORE = 0
COINS = 0
road_y = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = SPEED

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
            self.speed = SPEED * random.uniform(0.9, 1.1)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -300)

    def move(self):
        self.rect.y += SPEED
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed


# Объектілер
player = Player()
enemy = Enemy()
coin = Coin()

# Ойын циклі
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    road_y += SPEED
    if road_y >= SCREEN_HEIGHT:
        road_y = 0

    # Объектілерді жаңарту
    player.move()
    enemy.move()
    coin.move()

    # Балл қосу
    SCORE += 0.1

    # Монетамен соқтығысу
    if pygame.sprite.collide_mask(player, coin):
        COINS += 1
        coin.reset_position()

    # Жол апаты
    if pygame.sprite.collide_mask(player, enemy):
        crash_sound.play()
        
        # Game Over экраны
        SCREEN.fill(RED)
        game_over_text = font_large.render("GAME OVER", True, BLACK)
        score_text = font.render(f"Final Score: {int(SCORE)}", True, BLACK)
        coins_text = font.render(f"Coins: {COINS}", True, BLACK)

        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(coins_text, (SCREEN_WIDTH // 2 - coins_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # Фонды көрсету
    SCREEN.blit(background, (0, road_y - SCREEN_HEIGHT))
    SCREEN.blit(background, (0, road_y))

    # Объектілерді көрсету
    SCREEN.blit(enemy.image, enemy.rect)
    SCREEN.blit(coin.image, coin.rect)
    SCREEN.blit(player.image, player.rect)

    # Баллдар мен монеталарды көрсету
    score_display = font.render(f"Score: {int(SCORE)}", True, BLACK)
    coins_display = font.render(f"Coins: {COINS}", True, YELLOW)

    SCREEN.blit(score_display, (10, 10))
    SCREEN.blit(coins_display, (10, 40))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
