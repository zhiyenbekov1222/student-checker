import pygame
import random
 
pygame.init()
 
WIDTH, HEIGHT = 400, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаем окно 400 на 600
pygame.display.set_caption("Racer Game") # заголовок окна
 
BLUE  = (0, 0, 255) # определяем цвета
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
speed = 12 # скорость противиника
speed_coin = 10 # скорость монетки
score = 0 # счет
font = pygame.font.Font(None, 60) # шрифт и размер надписи
font_small = pygame.font.Font(None, 20) # шрифт и размер надписи
game_over = font.render("Game Over", True, BLACK) # визуализируем надпись гейм овер
 
 # загружаем картинки и меняем их размер
player_image = pygame.image.load("C:\\Users\\aruzh\\OneDrive\\Рабочий стол\\git\\pp2-5\\pp2-10\\Player.png") 
player_image = pygame.transform.scale(player_image, (50,100))
enemy_image = pygame.image.load("C:\\Users\\aruzh\\OneDrive\\Рабочий стол\\git\\pp2-5\\pp2-10\\Enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (50,100))
coin_image = pygame.image.load("C:\\Users\\aruzh\\OneDrive\\Рабочий стол\\git\\pp2-5\\pp2-10\\coin.png")
coin_image = pygame.transform.scale(coin_image, (30,30))
background_image = pygame.image.load("C:\\Users\\aruzh\\OneDrive\\Рабочий стол\\git\\pp2-5\\pp2-10\\AnimatedStreet.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
  # загружаем музыку
crash_sound = pygame.mixer.Sound("C:\\Users\\aruzh\\OneDrive\\Рабочий стол\\git\\pp2-5\\pp2-10\\crash.wav")
background_sound = pygame.mixer.Sound("C:\\Users\\aruzh\\OneDrive\\Рабочий стол\\git\\pp2-5\\pp2-10\\background.wav")
background_sound.play(-1) # музыка играет бесконечно
  # создаем класс машина
class Car:
    def __init__(self, x, y, image): # принимаем картинку и координаты
        self.image = pygame.transform.scale(image, (50, 100))  
        self.rect = self.image.get_rect(topleft=(x, y)) # создаем прямоуг картинки
    
    def draw(self): # рисуем картинку и прямоуг
        screen.blit(self.image, self.rect) 
 
class Player(Car): # наследуем класс кар
    def move(self, keys): # функция управления машинкой
        if keys[pygame.K_LEFT] and self.rect.left > 50: # если нажата кнопка влево и машинка не за пределами
            self.rect.x -= 10 # сдвигаем машинку на 10 пикселей влево
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 50: # машинка не выходит за  правую границу с отступом 50
            self.rect.x += 10 # сдвигаем на 50 вправо
 
class Enemy(Car): 
    def update(self): 
        self.rect.y += speed # двигаем машинку вниз по оси у
        if self.rect.top > HEIGHT:
            self.rect.y = -100 # если машинка выходит за границы перемещаем вверх 
            self.rect.x = random.choice([75, 175, 275]) # появляется в одном из трех мест
 
class Coin: # класс монетки
    def __init__(self): 
        self.image = pygame.transform.scale(coin_image, (30,30))
        self.radius = 15
        self.rect = pygame.Rect(random.choice([75, 175, 275]), -100, self.radius * 2, self.radius * 2)
    # создаем прям для монетки размером 30 на 30
            
    def update_coin(self): # движение монеты
        self.rect.y += speed_coin
        if self.rect.top > HEIGHT:
            self.rect.y = -100 # если вышла за границу появляется сверху
            self.rect.x = random.choice([75, 175, 275])
    
    def draw(self):
        screen.blit(self.image, self.rect)  # выводим картинку на экран
 
player = Player(WIDTH//2 - 25, HEIGHT - 120, player_image) # передаем нач координаты и картинку
enemies = [Enemy(random.choice([75, 175, 275]), -100, enemy_image)] # также передаем координаты начала
coins = [Coin()] # создается монетка
 
running = True
clock = pygame.time.Clock()


while running:
    screen.blit(background_image, (0, 0)) # заполняем экран картинкой
    
    keys = pygame.key.get_pressed() # получаем все нажатые кнопки
    player.move(keys) # передаем список нажатых кнопок
    
    for enemy in enemies: # цикл по списку enemies
        enemy.update()
        enemy.draw() 
    
        if player.rect.colliderect(enemy.rect): # проверяет если игрок столкн с врагом
            crash_sound.play() # если столкн воспроизводим звук
            pygame.time.delay(1000) # останавливаем игру 
            screen.fill(RED) # заполняем экран красным
            screen.blit(game_over, (30, 250)) # выводим текст
            pygame.display.update() # обновляем
            pygame.time.delay(2000) 
            running = False # завершаем игру 
    
    for coin in coins: # движение и отрисовка монеты
        coin.update_coin()
        coin.draw()
        if player.rect.colliderect(coin.rect): # если игрок касается монеты
            score +=random.randint(1,5) # счет +(1-5)
            coin.rect.y = -100 # моетка появляется сверху
            coin.rect.x = random.choice([75, 175, 275]) 
            if score % 10 == 0:
             speed +=5 # каждый раз как счет делится на 10 скорость противника увеличивается
    player.draw() # рисуем игрока
    
    
    score_text = font_small.render(f"Счет: {score}", True, (255, 255, 255)) # отображаем счет 
    screen.blit(score_text, (300, 10)) # в правом верхнем углу
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # если закрыли окно игра завершается
    pygame.display.flip() # обновляем экран
    clock.tick(30) # частота кадров
 
pygame.quit()