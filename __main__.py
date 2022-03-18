from pygame import*
from random import randint

max_width = 700
max_height = 500
num_of_enemies = 3


class Sprite:
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (80, 80))
        self.speed = player_speed
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        # класс главного игрока


class Player(Sprite):
    # метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < max_width - 80:
            self.rect.x += self.speed


# класс спрайта-врага
class Enemy(Sprite):

    def __init__(self, player_image, player_speed):
        # рандомный спавн:
        self.player_x = randint(0, 700)
        self.player_y = 0
        Sprite.__init__(self, player_image, self.player_x, self.player_y, player_speed)

    def update(self):
        # движение
        if self.rect.y < max_height - 5:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, 700)
            self.reset()


# класс снаряда
class Bullet(Sprite):
    def update(self):
        # движение
        if self.rect.y < max_height - 5:
            self.rect.y -= self.speed


# Создаем окошко
display.set_caption("Шутер")
window = display.set_mode((max_width, max_height))

# создаем спрайты
player = Player('green_triangle.jpg', max_width//2, 455, 10)
enemies,bullets = [],[]
for i in range(num_of_enemies):
    enemies.append(Enemy('red_circle.jpg', 20))
 
# переменная, отвечающая за то, как кончилась игра
finish = False

fon_img = image.load('background.jpg')
# игровой цикл
while not finish:
    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)

    # перебираем все события, которые могли произойти
    for x in event.get():

      #событие нажатия на крестик окошка
        if x.type == QUIT:
            finish = True

    # обновляем фон каждую итерацию
    window.blit(fon_img,(0,0))

    #запускаем движения спрайтов и обновляем их в новом местоположении при каждой итерации цикла
    player.update()
    player.reset()

    for enemy in enemies:
        enemy.update()
        enemy.reset()
        #print(enemy.rect.y)

    for bullet in bullets:
        bullet.update()
        bullet.reset()

    # игровая логика
    keys = key.get_pressed()
    if keys[K_SPACE]: # выстрел
        bullets.append(Bullet('orange.jpg', player.rect.x,player.rect.y, 10))

    k=0
    for i in range(len(bullets)):
        for ii in range(len(enemies)):
            if sprite.collide_rect(bullets[i],enemies[ii]):
                bullets.pop(i)
                enemies[ii] = Enemy('red_circle.jpg', 20)
                k=1
                break
        if k ==1:
            break

        if bullets[i].rect.y == max_height - 5:
            bullets.pop(i)

    for i in range(len(enemies)):
        if sprite.collide_rect(player, enemies[i]) and enemies[i].rect.x - player.rect.x < 90 and enemies[i].rect.x - player.rect.x > -90:
            enemies.pop(i)
            finish = True
            break

    display.update()
