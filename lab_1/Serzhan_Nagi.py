import pygame
import random

pygame.init()

HEIGHT = 600
WIDTH = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

road = pygame.image.load("/Users/madinatabyldy/Desktop/Python2025/lab8/images_racer/AnimatedStreet.png")
coin_i = pygame.image.load("/Users/madinatabyldy/Desktop/Python2025/lab8/images_racer/Coin.png")

coin_im = pygame.transform.scale(coin_i, (100, 100))
player_im = pygame.image.load("/Users/madinatabyldy/Desktop/Python2025/lab8/images_racer/Player.png")

font = pygame.font.SysFont("Verdana", 30)
count = 0

#Игрок: картинка, скорость, старт снизу
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_im
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

#Монета: картинка, выпадение сверху
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_im
        self.speed = 10
        self.rect = self.image.get_rect()
        self.generate() 

    def generate(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()

player = Player()
coin = Coin()

all_sprites = pygame.sprite.Group(player, coin)
coin_sprites = pygame.sprite.Group(coin)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()
    coin.move()
    
    if pygame.sprite.spritecollideany(player, coin_sprites):
        count += 1
        coin.generate()  
    
    #Фон дороги
    screen.blit(road, (0, 0))
    all_sprites.draw(screen)
    
    #Отображение счёта
    score_text = font.render(f"Score: {count}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()