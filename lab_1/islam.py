import pygame
import sys
import random

pygame.init()

# Константы для экрана и цветов
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 36)

# Количество объектов и монет
NUM_OBSTACLES = 1
NUM_COINS = 1

# Окно приложения
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("kolik aidau")

# Фон
background = pygame.image.load("AnimatedStreet.png")
background_y = 0

# Класс для игрока (машины)
class Car:
    def __init__(self, x, y):
        self.image = pygame.image.load("Player.png")  # Изображение машины
        self.rect = self.image.get_rect(topleft=(x, y))  # Позиция машины
        self.speed = 4  # Скорость машины

    def draw(self):
        screen.blit(self.image, self.rect)  # Отображаем машину на экране

    def move(self, dx, dy):
        # Ограничиваем движение машины по экрану
        self.rect.x = max(0, min(self.rect.x + dx, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + dy, SCREEN_HEIGHT - self.rect.height))

# Класс для врагов (машин-препятствий)
class Obstacle:
    def __init__(self, x, y):
        self.image = pygame.image.load("Enemy.png")  # Изображение препятствия
        self.rect = self.image.get_rect(topleft=(x, y))  # Позиция препятствия
        self.speed = 2  # Скорость движения препятствия

    def draw(self):
        screen.blit(self.image, self.rect)  # Отображаем препятствие на экране

    def move(self):
        # Перемещаем препятствие вниз
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            # Если препятствие вышло за экран, перемещаем его в верхнюю часть экрана
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

# Класс для монет
class Coin:
    def __init__(self, x, y):
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))  # Масштабируем изображение монеты
        self.rect = self.image.get_rect(topleft=(x, y))  # Позиция монеты
        self.speed = 1  # Скорость монеты

    def draw(self):
        screen.blit(self.image, self.rect)  # Отображаем монету на экране

    def move(self):
        self.rect.y += self.speed  # Монета движется вниз
        if self.rect.y > SCREEN_HEIGHT:
            # Если монета вышла за экран, перемещаем ее в верхнюю часть экрана
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(50, SCREEN_WIDTH - 50)

# Функция для сброса игры (инициализация объектов)
def reset_game():
    global car, obstacles, coins, coin_count, game_over
    car = Car(170, 500)  # Инициализация машины игрока
    obstacles = [Obstacle(random.randint(0, SCREEN_WIDTH - 64), -random.randint(64, 300)) for _ in range(NUM_OBSTACLES)]
    coins = [Coin(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(NUM_COINS)]
    coin_count = 0  # Счетчик монет
    game_over = False  # Состояние игры

# Инициализация игры
reset_game()

# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)  # Заполняем экран белым цветом

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Закрытие игры

        # Перезапуск игры по клику мышью, если игра окончена
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_rect.collidepoint(event.pos):
                reset_game()

    if not game_over:
        # Движение игрока
        keys = pygame.key.get_pressed()  # Получаем состояние клавиш
        if keys[pygame.K_LEFT]:
            car.move(-car.speed, 0)  # Двигаем машину влево
        if keys[pygame.K_RIGHT]:
            car.move(car.speed, 0)  # Двигаем машину вправо
        if keys[pygame.K_UP]:
            car.move(0, -car.speed)  # Двигаем машину вверх
        if keys[pygame.K_DOWN]:
            car.move(0, car.speed)  # Двигаем машину вниз

        # Движение фона
        background_y = (background_y + car.speed) % SCREEN_HEIGHT
        screen.blit(background, (0, background_y - SCREEN_HEIGHT))  # Отображаем фон
        screen.blit(background, (0, background_y))

        # Движение препятствий
        for obstacle in obstacles:
            obstacle.move()  # Двигаем препятствие
            obstacle.draw()  # Отображаем препятствие
            if car.rect.colliderect(obstacle.rect):  # Если машина сталкивается с препятствием
                game_over = True

        # Движение монет
        for coin in coins:
            coin.move()  # Двигаем монету
            if car.rect.colliderect(coin.rect):  # Если машина собирает монету
                coin_count += 1  # Увеличиваем счетчик монет
                # Перемещаем монету
                coin.rect.y = -coin.rect.height
                coin.rect.x = random.randint(50, SCREEN_WIDTH - 50)
            coin.draw()  # Отображаем монету

        car.draw()  # Отображаем машину игрока

        # Отображение количества собранных монет
        coin_text = FONT.render(f"Coins: {coin_count}", True, (255, 255, 0))
        screen.blit(coin_text, (10, 10))

    else:
        # Текст "Game Over"
        game_over_text = FONT.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50))

        # Кнопка для начала новой игры
        play_again_text = FONT.render("Play Again", True, (0, 255, 0))
        play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        pygame.draw.rect(screen, (0, 0, 0), play_again_rect.inflate(20, 10))  # Отображаем кнопку
        screen.blit(play_again_text, play_again_rect)

    pygame.display.flip()  # Обновляем экран

pygame.quit()  # Закрытие pygame
sys.exit()  # Завершаем работу программы
