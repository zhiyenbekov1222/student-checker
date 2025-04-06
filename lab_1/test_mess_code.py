import pygame
import random
import time

'''
Class storage, from snake's meal to gold and cars
'''

pygame.init()
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 1024 - 40), 0)
        self.speed = 4
    def move(self):
        self.rect.move_ip(0, self.speed)
        if (self.rect.bottom > 720):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 1024), 76)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pixil-frame-0.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] and self.rect.top -5 > 76:
           self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN] and self.rect.bottom + 5 <720:
           self.rect.move_ip(0,5)

        if self.rect.left > 0 and self.rect.left -5 > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < 1024:
            if pressed_keys[pygame.K_RIGHT] and self.rect.right + 5 <1024:
                self.rect.move_ip(5, 0)
class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.randint(1, 3) #Random choice of value and image
        if self.value == 1:
           self.image = pygame.image.load("Coin.png")
        elif self.value == 2:
           self.image = pygame.image.load("Coin_2.png")
        else:
            self.image = pygame.image.load("Coin_3.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 1024 - 40), random.randint(76, 720 ))
    def respawn(self): #respawning
        self.value = random.randint(1, 3)
        if self.value == 1:
           self.image = pygame.image.load("Coin.png")
        elif self.value == 2:
           self.image = pygame.image.load("Coin_2.png")
        else:
           self.image = pygame.image.load("Coin_3.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 1024 - 40), random.randint(76, 720))
    def move(self):
        self.rect.move_ip(0, 1)
        if (self.rect.bottom > 720):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 1024), 76)

class Snake_meal():
    def __init__(self):
        super().__init__()
        self.value = random.randint(10, 41)
        self.time = time.time()
        self.rect = pygame.Rect(random.randint(1, 983), random.randint(22, 667), self.value//10*10, self.value//10*10)
    def respawn(self): #Respawning
        self.value = random.randint(10, 41)
        self.time = time.time()
        self.rect = pygame.Rect(random.randint(1, 983), random.randint(22, 667), self.value // 10 * 10,
                                self.value // 10 * 10)
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0 ,0),  self.rect)