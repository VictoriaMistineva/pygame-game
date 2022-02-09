import random
import pygame

# Tek=os.path.dirname(__file__)
# image_folder=os.path.join(Tek,'Game_god')
# #plimage=pygame.image.load(os.path.join(image_folder,'Ёлка1.png')).convert()


width = 600  # Окно игры
height = 800
Black = (150, 255, 234)

FPS = 60

pygame.init()  # Запуск игры
pygame.mixer.init()  # Звук
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра Бога")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):  # Игрок
    def __init__(self):  # Инициализация игрока
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((30, 30))  # Размер прямоуголника
        self.image.fill((255, 145, 3))  # Цвет прямоуголника

        self.rect = self.image.get_rect()  # Создание прямоуголника
        self.rect.center = (width / 2, height / 2)  # Центр прямоуголника


    def update(self):

        speeds = 6
        self.speedX = 0
        self.speedY = 0

        key_tracking = pygame.key.get_pressed()  # Словар совсеми клавишоми

        if key_tracking[pygame.K_LEFT]:
            self.speedX = -speeds

        if key_tracking[pygame.K_RIGHT]:
            self.speedX = speeds

        if key_tracking[pygame.K_a]:
            self.speedX = -speeds

        if key_tracking[pygame.K_d]:
            self.speedX = speeds

        if key_tracking[pygame.K_UP]:
            self.speedY = -speeds

        if key_tracking[pygame.K_DOWN]:
            self.speedY = speeds

        if key_tracking[pygame.K_w]:
            self.speedY = -speeds

        if key_tracking[pygame.K_s]:
            self.speedY = speeds

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        # блок запрета движения
        if self.rect.right > width:
            self.rect.right = width

        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        a = Ammo(self.rect.centerx, self.rect.top)
        all_sprites.add(a)
        ammon.add(a)

class Enemy(pygame.sprite.Sprite):  # врага
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 50))  # Размер врага (форма не определена)
        self.image.fill((255, 54, 41))  # Цвет врага

        self.rect = self.image.get_rect()  # Создание врага по форме прямоугольника
        # self.rect.center = (width / 3, height / 3)  # Центр врага
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4, 15)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 2))
        self.image.fill((255, 54, 41))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()  # Добовление спрайта в групу
enemy = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
ammon = pygame.sprite.Group()


for i in range(4):  # спавн мабов
    mob = Enemy()
    all_sprites.add(mob)
    enemy.add(mob)

run = True
while run:

    clock.tick(FPS)  # Ограничения FPS

    for event in pygame.event.get():  # Выход на крестик
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    collision = pygame.sprite.groupcollide(enemy,ammon,True,True) #столкновение пули и врага
    for i in collision:
        mob = Enemy()
        all_sprites.add(mob)
        enemy.add(mob)

    all_sprites.update()
    collision = pygame.sprite.spritecollide(player, enemy, False) #столкновение пули и игрока
    if collision:
        run = False
    screen.fill(Black)  # Заливка0
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()