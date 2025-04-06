import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0
LIVES = 1 
CHEAT_USED = False 

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(r"C:\ALL_Labs_By_ISA\lab8\assets\images\AnimatedStreet.png")
pygame.mixer.music.load(r"C:\ALL_Labs_By_ISA\lab8\assets\sounds\background.wav")
pygame.mixer.music.play(-1)  

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\ALL_Labs_By_ISA\lab8\assets\images\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\ALL_Labs_By_ISA\lab8\assets\images\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (300, 500)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:\ALL_Labs_By_ISA\lab8\assets\images\coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def reset_game():
    global SPEED, SCORE, COINS_COLLECTED, LIVES, CHEAT_USED, enemies, coins, all_sprites, P1
    SPEED = 5
    SCORE = 0
    COINS_COLLECTED = 0
    LIVES = 1
    CHEAT_USED = False
    P1 = Player()
    E1 = Enemy()
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    coins = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

reset_game()

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

ADD_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_COIN, 1500)

cheat_input = ""

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == ADD_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (300, 10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(P1, enemies):
        if CHEAT_USED:
            LIVES = 1
        else:
            LIVES -=1
        if LIVES > 0:
            pygame.mixer.Sound(r'C:\ALL_Labs_By_ISA\lab8\assets\sounds\crash.wav').play()
            time.sleep(0.5)
            P1.rect.center = (160, 520)
            continue
        else:
            pygame.mixer.Sound(r'C:\ALL_Labs_By_ISA\lab8\assets\sounds\crash.wav').play()
            time.sleep(1)
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30, 200))
            retry_text = font_small.render("Press R to Rematch or Q to Quit", True, BLACK)
            DISPLAYSURF.blit(retry_text, (50, 300))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_r:
                            reset_game()
                            waiting = False
                        elif event.key == K_q:
                            pygame.quit()
                            sys.exit()

    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    COINS_COLLECTED += len(collected_coins)

    pygame.display.update()
    FramePerSec.tick(FPS)
    